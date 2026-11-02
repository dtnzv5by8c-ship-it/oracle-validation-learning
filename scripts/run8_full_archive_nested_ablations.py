#!/usr/bin/env python3
"""Research-only full Selected-50 Run 8 event-time reconstruction and nested ablations.

Raw provider rows, the event-time panel and fixture-level predictions remain ephemeral.
Only aggregate metrics, reliability bins, coverage and governance metadata are exported.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, sys, zipfile
from bisect import bisect_left
from collections import Counter, defaultdict
from datetime import date
from itertools import groupby
from pathlib import Path, PurePosixPath

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_footystats_archive_features import (
    DATE_KEYS, ID_KEYS, HOME_ID_KEYS, AWAY_ID_KEYS, HG_KEYS, AG_KEYS,
    as_date, first, score, settled, map_archive_seasons_to_selected_ids,
)
from scripts.audit_run8_pinned_archive_venue_flag_coverage import parse_no_home_away

EXPECTED_ARCHIVE_SHA256 = "bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261"
TRAIN_START = date(2024, 3, 20)
PRIMARY_START = date(2025, 3, 20)
PRIMARY_END = date(2026, 9, 20)
FOLDS = [
    ("FOLD_1", date(2025, 3, 20), date(2025, 10, 1)),
    ("FOLD_2", date(2025, 10, 1), date(2026, 4, 1)),
    ("FOLD_3", date(2026, 4, 1), date(2026, 9, 21)),
]
MAIN_NUMERIC = [
    "home_ppg5", "away_ppg5", "home_gf5", "away_gf5", "home_ga5", "away_ga5",
    "home_home_ppg5", "home_home_gf5", "home_home_ga5",
    "away_away_ppg5", "away_away_gf5", "away_away_ga5",
]
INTERACTIONS = {
    "home_strength_x_away_weakness": {
        "formula": "(home_ppg5 - away_ppg5) * away_ga5",
        "constituents": ["home_ppg5", "away_ppg5", "away_ga5"],
    },
    "home_attack_x_away_defence": {
        "formula": "home_gf5 * away_ga5",
        "constituents": ["home_gf5", "away_ga5"],
    },
}
MARKETS = {
    "DC_HOME": lambda d: int(d["home_goals"] >= d["away_goals"]),
    "DC_AWAY": lambda d: int(d["away_goals"] >= d["home_goals"]),
    "BTTS": lambda d: int(d["home_goals"] > 0 and d["away_goals"] > 0),
}
MODEL_FEATURES = {
    "league_only": [],
    "main_effects": MAIN_NUMERIC,
    "main_plus_home_strength_x_away_weakness": MAIN_NUMERIC + ["home_strength_x_away_weakness"],
    "main_plus_home_attack_x_away_defence": MAIN_NUMERIC + ["home_attack_x_away_defence"],
    "main_plus_both_interactions": MAIN_NUMERIC + list(INTERACTIONS),
}
COMPARISONS = [
    ("main_effects_vs_league_only", "main_effects", "league_only"),
    ("home_strength_interaction_vs_main_effects", "main_plus_home_strength_x_away_weakness", "main_effects"),
    ("home_attack_interaction_vs_main_effects", "main_plus_home_attack_x_away_defence", "main_effects"),
    ("both_interactions_vs_main_effects", "main_plus_both_interactions", "main_effects"),
]
METRICS = ["brier", "log_loss", "auc", "ece10"]


def classify_home_away_flag(value):
    """Flag 1 means home/away is undistinguished, not proof of a neutral venue."""
    parsed = parse_no_home_away(value)
    return {"NEUTRAL": "UNDISTINGUISHED", "NON_NEUTRAL": "DISTINGUISHED"}.get(parsed, parsed)


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_archive(archive_path, manifest_path, expected_sha256=EXPECTED_ARCHIVE_SHA256):
    archive_path = Path(archive_path)
    actual_sha = sha256_file(archive_path)
    if actual_sha != expected_sha256:
        raise ValueError(f"Pinned archive SHA-256 mismatch: {actual_sha}")
    with Path(manifest_path).open(encoding="utf-8-sig", newline="") as handle:
        selected_rows = list(csv.DictReader(handle))
    selected_ids = {str(row.get("selected_id") or "").strip() for row in selected_rows}
    if len(selected_rows) != 50 or len(selected_ids) != 50 or "" in selected_ids:
        raise ValueError(f"Expected exactly 50 unique selected groups; got rows={len(selected_rows)}, ids={len(selected_ids)}")

    records, raw_rows = [], 0
    parse_error_files, date_parse_failures, identity_missing = [], 0, 0
    primary_flags = Counter()
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        match_files = sorted(n for n in names if PurePosixPath(n).name == "matches.json")
        ingestion_files = [n for n in names if PurePosixPath(n).name == "ingestion_manifest.json"]
        if len(match_files) != 200 or len(ingestion_files) != 1:
            raise ValueError(f"Unexpected archive structure: matches={len(match_files)}, manifests={len(ingestion_files)}")
        ingestion_manifest = json.loads(archive.read(ingestion_files[0]))
        season_ids = [PurePosixPath(n).parent.name for n in match_files]
        season_to_selected, mapping_qa, _ = map_archive_seasons_to_selected_ids(
            selected_rows, ingestion_manifest, season_ids
        )
        if mapping_qa.get("status") != "PASS_EXACT_SELECTED_MANIFEST_LABEL_MAPPING" or len(season_to_selected) != 200:
            raise ValueError(f"Exact Selected-50 mapping failed: {mapping_qa}")

        for filename in match_files:
            season_id = PurePosixPath(filename).parent.name
            selected_id = season_to_selected.get(str(season_id))
            if not selected_id:
                raise ValueError(f"Unmapped archive season folder: {season_id}")
            try:
                payload = json.loads(archive.read(filename))
                if not isinstance(payload, list):
                    raise ValueError("matches.json root is not a list")
            except Exception as exc:
                parse_error_files.append({"file": filename, "error": type(exc).__name__})
                continue
            for item in payload:
                if not isinstance(item, dict):
                    continue
                raw_rows += 1
                dt = as_date(first(item, DATE_KEYS))
                if dt is None:
                    date_parse_failures += 1
                    continue
                fixture_id, home_id, away_id = first(item, ID_KEYS), first(item, HOME_ID_KEYS), first(item, AWAY_ID_KEYS)
                if fixture_id in (None, "") or home_id in (None, "") or away_id in (None, ""):
                    identity_missing += 1
                    continue
                hg, _ = score(item, HG_KEYS, "homeGoals")
                ag, _ = score(item, AG_KEYS, "awayGoals")
                is_settled_score = bool(settled(item) and hg is not None and ag is not None)
                venue_state = classify_home_away_flag(item.get("no_home_away"))
                kickoff_date = dt.date()
                if PRIMARY_START <= kickoff_date <= PRIMARY_END:
                    primary_flags["identity_complete_records"] += 1
                    primary_flags[f"home_away_{venue_state.lower()}"] += 1
                    if is_settled_score:
                        primary_flags["settled_score"] += 1
                        primary_flags[f"settled_home_away_{venue_state.lower()}"] += 1
                records.append({
                    "selected_id": str(selected_id), "provider_season_id": str(season_id),
                    "fixture_id": str(fixture_id), "home_team_id": str(home_id), "away_team_id": str(away_id),
                    "kickoff_ts": float(dt.timestamp()), "kickoff_utc": dt.isoformat(),
                    "kickoff_date": kickoff_date, "home_goals": hg, "away_goals": ag,
                    "settled_score": is_settled_score, "venue_state": venue_state,
                })
    if parse_error_files:
        raise ValueError(f"Archive JSON parse errors: {parse_error_files[:5]}")

    identity_keys = [(r["selected_id"], r["provider_season_id"], r["fixture_id"]) for r in records]
    counts = Counter(identity_keys)
    duplicate_keys = {key for key, count in counts.items() if count > 1}
    duplicate_rows = sum(counts[key] for key in duplicate_keys)
    if duplicate_keys:
        records = [r for r in records if (r["selected_id"], r["provider_season_id"], r["fixture_id"]) not in duplicate_keys]

    meta = {
        "archive_sha256": actual_sha, "archive_bytes": archive_path.stat().st_size,
        "archive_match_files": 200, "archive_raw_rows": raw_rows,
        "archive_parse_error_files": len(parse_error_files), "date_parse_failures": date_parse_failures,
        "identity_missing_rows": identity_missing, "duplicate_identity_keys": len(duplicate_keys),
        "duplicate_identity_rows_quarantined": duplicate_rows,
        "records_retained_for_event_time": len(records), "selected_groups_expected": 50,
        "selected_groups_mapped": mapping_qa["selected_groups_mapped"],
        "provider_seasons_mapped": mapping_qa["mapped_archive_seasons"],
        "mapping_qa": mapping_qa, "primary_window_home_away_flag_counts": dict(primary_flags),
        "provider_api_credits_used": 0,
    }
    return records, sorted(selected_ids), meta


def _before(history, cutoff_ts, n=5):
    if not history:
        return [], 0
    stop = bisect_left([row[0] for row in history], cutoff_ts)
    return history[max(0, stop - n):stop], stop


def _mean(sample, index):
    return float(np.mean([row[index] for row in sample])) if sample else np.nan


def build_event_time_panel(records, start_date, end_date, lag_hours=0.0):
    """Features are computed before appending any result sharing the target kickoff."""
    ordered = sorted(records, key=lambda r: (r["selected_id"], r["kickoff_ts"], r["fixture_id"]))
    all_history, home_role_history, away_role_history, h2h_history = (
        defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    )
    panel, lag_seconds = [], float(lag_hours) * 3600.0
    for _, iterator in groupby(ordered, key=lambda r: (r["selected_id"], r["kickoff_ts"])):
        group = list(iterator)
        cutoff = group[0]["kickoff_ts"] - lag_seconds
        for target in group:
            if not (start_date <= target["kickoff_date"] <= end_date):
                continue
            if not target["settled_score"] or target["venue_state"] != "DISTINGUISHED":
                continue
            sid, hid, aid = target["selected_id"], target["home_team_id"], target["away_team_id"]
            h_all, h_n = _before(all_history[(sid, hid)], cutoff, 5)
            a_all, a_n = _before(all_history[(sid, aid)], cutoff, 5)
            h_home, hh_n = _before(home_role_history[(sid, hid)], cutoff, 5)
            a_away, aa_n = _before(away_role_history[(sid, aid)], cutoff, 5)
            pair = tuple(sorted((hid, aid)))
            h2h, h2h_n = _before(h2h_history[(sid, pair)], cutoff, 5)
            row = {
                "selected_id": sid, "provider_season_id": target["provider_season_id"],
                "fixture_id": target["fixture_id"], "kickoff_utc": target["kickoff_utc"],
                "kickoff_ts": target["kickoff_ts"], "kickoff_date": target["kickoff_date"],
                "home_team_id": hid, "away_team_id": aid,
                "home_goals": int(target["home_goals"]), "away_goals": int(target["away_goals"]),
                "venue_state": target["venue_state"], "history_lag_hours": float(lag_hours),
                "history_cutoff_rule": "prior_kickoff_strictly_before_target_minus_lag",
                "home_prior_n": int(h_n), "away_prior_n": int(a_n),
                "home_home_n": int(hh_n), "away_away_n": int(aa_n), "h2h_prior_n": int(h2h_n),
                "home_ppg5": _mean(h_all, 1), "home_gf5": _mean(h_all, 2), "home_ga5": _mean(h_all, 3),
                "away_ppg5": _mean(a_all, 1), "away_gf5": _mean(a_all, 2), "away_ga5": _mean(a_all, 3),
                "home_home_ppg5": _mean(h_home, 1), "home_home_gf5": _mean(h_home, 2), "home_home_ga5": _mean(h_home, 3),
                "away_away_ppg5": _mean(a_away, 1), "away_away_gf5": _mean(a_away, 2), "away_away_ga5": _mean(a_away, 3),
                "h2h_last5_btts_rate": _mean(h2h, 1) if h2h_n >= 5 else np.nan,
                "h2h_last5_over25_rate": _mean(h2h, 2) if h2h_n >= 5 else np.nan,
            }
            row["home_strength_x_away_weakness"] = (
                (row["home_ppg5"] - row["away_ppg5"]) * row["away_ga5"]
                if all(pd.notna(row[k]) for k in ("home_ppg5", "away_ppg5", "away_ga5")) else np.nan
            )
            row["home_attack_x_away_defence"] = (
                row["home_gf5"] * row["away_ga5"]
                if all(pd.notna(row[k]) for k in ("home_gf5", "away_ga5")) else np.nan
            )
            panel.append(row)

        # Same-kickoff targets are all evaluated before any result in this group enters history.
        for match in group:
            if not match["settled_score"]:
                continue
            sid, hid, aid = match["selected_id"], match["home_team_id"], match["away_team_id"]
            hg, ag = int(match["home_goals"]), int(match["away_goals"])
            btts, over25 = int(hg > 0 and ag > 0), int(hg + ag > 2)
            hp = 3 if hg > ag else 1 if hg == ag else 0
            ap = 3 if ag > hg else 1 if hg == ag else 0
            h_entry = (match["kickoff_ts"], hp, hg, ag, btts, over25)
            a_entry = (match["kickoff_ts"], ap, ag, hg, btts, over25)
            all_history[(sid, hid)].append(h_entry)
            all_history[(sid, aid)].append(a_entry)
            # H2H goal-rate evidence is pair-based and does not require home/away orientation.
            h2h_history[(sid, tuple(sorted((hid, aid)))].append((match["kickoff_ts"], btts, over25))
            if match["venue_state"] == "DISTINGUISHED":
                home_role_history[(sid, hid)].append(h_entry)
                away_role_history[(sid, aid)].append(a_entry)
    frame = pd.DataFrame(panel)
    if frame.empty:
        raise ValueError("No target fixtures available for event-time feature construction")
    return frame


def add_eligibility_and_labels(frame):
    out = frame.copy()
    out["core_eligible"] = (
        pd.to_numeric(out["home_prior_n"], errors="coerce").ge(5)
        & pd.to_numeric(out["away_prior_n"], errors="coerce").ge(5)
    )
    out["venue_eligible"] = (
        out["core_eligible"]
        & pd.to_numeric(out["home_home_n"], errors="coerce").ge(5)
        & pd.to_numeric(out["away_away_n"], errors="coerce").ge(5)
    )
    out["h2h_eligible"] = pd.to_numeric(out["h2h_prior_n"], errors="coerce").ge(5)
    out["selected_id"] = out["selected_id"].astype(str)
    for market, fn in MARKETS.items():
        out[f"y_{market}"] = out.apply(fn, axis=1)
    return out


def build_model(numeric_columns):
    transformers = []
    if numeric_columns:
        numeric = Pipeline([
            ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
            ("scale", StandardScaler()),
        ])
        transformers.append(("numeric", numeric, list(numeric_columns)))
    league = Pipeline([("onehot", OneHotEncoder(handle_unknown="ignore"))])
    transformers.append(("league", league, ["selected_id"]))
    return Pipeline([
        ("preprocess", ColumnTransformer(transformers, remainder="drop")),
        ("logistic", LogisticRegression(C=0.1, solver="lbfgs", max_iter=2500)),
    ])


def ece10(y, p):
    y = np.asarray(y, dtype=float)
    p = np.clip(np.asarray(p, dtype=float), 0.0, 1.0)
    if not len(y):
        return np.nan
    bins = np.minimum((p * 10).astype(int), 9)
    return float(sum(
        (bins == b).sum() / len(y) * abs(float(p[bins == b].mean()) - float(y[bins == b].mean()))
        for b in range(10) if (bins == b).any()
    ))


def metric_value(metric, y, p):
    y = np.asarray(y, dtype=int)
    p = np.clip(np.asarray(p, dtype=float), 1e-6, 1 - 1e-6)
    if metric == "brier":
        return float(np.mean((p - y) ** 2))
    if metric == "log_loss":
        return float(log_loss(y, p, labels=[0, 1]))
    if metric == "auc":
        return float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else np.nan
    if metric == "ece10":
        return ece10(y, p)
    raise ValueError(metric)


def reliability_rows(y, p, market, model_name, window):
    y, p = np.asarray(y, dtype=int), np.clip(np.asarray(p, dtype=float), 0.0, 1.0)
    bins, rows = np.minimum((p * 10).astype(int), 9), []
    for b in range(10):
        mask = bins == b
        rows.append({
            "window": window, "market": market, "model": model_name, "bin": b,
            "n": int(mask.sum()),
            "mean_predicted": float(p[mask].mean()) if mask.any() else np.nan,
            "observed_rate": float(y[mask].mean()) if mask.any() else np.nan,
            "absolute_gap": abs(float(p[mask].mean()) - float(y[mask].mean())) if mask.any() else np.nan,
        })
    return rows


def adjust_bh_by(p_values):
    values = np.asarray(p_values, dtype=float)
    valid = np.where(np.isfinite(values))[0]
    bh, by = np.full(len(values), np.nan), np.full(len(values), np.nan)
    m = len(valid)
    if not m:
        return bh, by
    ordered = valid[np.argsort(values[valid])]
    p = values[ordered]
    ranks = np.arange(1, m + 1, dtype=float)
    harmonic = float(np.sum(1.0 / ranks))
    bh_sorted = np.minimum.accumulate((p * m / ranks)[::-1])[::-1]
    by_sorted = np.minimum.accumulate((p * m * harmonic / ranks)[::-1])[::-1]
    bh[ordered], by[ordered] = np.clip(bh_sorted, 0, 1), np.clip(by_sorted, 0, 1)
    return bh, by


def paired_cluster_summary(y, p_challenger, p_baseline, groups, metric):
    y = np.asarray(y, dtype=int)
    pc, pb = np.asarray(p_challenger, dtype=float), np.asarray(p_baseline, dtype=float)
    groups = np.asarray(groups, dtype=str)
    pooled_delta = metric_value(metric, y, pc) - metric_value(metric, y, pb)
    deltas = []
    for group in sorted(set(groups)):
        mask = groups == group
        a, b = metric_value(metric, y[mask], pc[mask]), metric_value(metric, y[mask], pb[mask])
        if np.isfinite(a) and np.isfinite(b):
            deltas.append(a - b)
    n = len(deltas)
    mean, low, high, pvalue = np.nan, np.nan, np.nan, np.nan
    if n:
        mean = float(np.mean(deltas))
    if n >= 2:
        values = np.asarray(deltas, dtype=float)
        se = float(values.std(ddof=1) / math.sqrt(n))
        critical = float(stats.t.ppf(0.975, n - 1))
        low, high = mean - critical * se, mean + critical * se
        alternative = "greater" if metric == "auc" else "less"
        pvalue = float(stats.ttest_1samp(values, 0.0, alternative=alternative).pvalue)
    return {
        "pooled_delta": float(pooled_delta) if np.isfinite(pooled_delta) else np.nan,
        "league_cluster_mean_delta": mean,
        "ci95_low_cluster_mean": float(low) if np.isfinite(low) else np.nan,
        "ci95_high_cluster_mean": float(high) if np.isfinite(high) else np.nan,
        "league_clusters_n": n,
        "p_value_one_sided": float(pvalue) if np.isfinite(pvalue) else np.nan,
    }


def partial_spearman(y, interaction, constituents, selected_ids):
    y, x = np.asarray(y, dtype=float), np.asarray(interaction, dtype=float)
    groups = np.asarray(selected_ids, dtype=str)
    keep = np.isfinite(y) & np.isfinite(x)
    for values in constituents.values():
        keep &= np.isfinite(np.asarray(values, dtype=float))
    if keep.sum() < 30:
        return {"n": int(keep.sum()), "n_leagues": 0, "rho_partial_spearman": np.nan, "p_value_two_sided": np.nan}
    y_rank, x_rank, groups = stats.rankdata(y[keep]), stats.rankdata(x[keep]), groups[keep]
    columns = [np.ones(len(y_rank))]
    for values in constituents.values():
        columns.append(stats.rankdata(np.asarray(values, dtype=float)[keep]))
    dummies = pd.get_dummies(pd.Series(groups), drop_first=True, dtype=float).to_numpy()
    if dummies.size:
        columns.extend([dummies[:, i] for i in range(dummies.shape[1])])
    design = np.column_stack(columns)
    ry = y_rank - design @ np.linalg.lstsq(design, y_rank, rcond=None)[0]
    rx = x_rank - design @ np.linalg.lstsq(design, x_rank, rcond=None)[0]
    if np.std(ry) == 0 or np.std(rx) == 0:
        return {"n": int(len(y_rank)), "n_leagues": int(len(set(groups))), "rho_partial_spearman": np.nan, "p_value_two_sided": np.nan}
    rho, pvalue = stats.pearsonr(rx, ry)
    return {"n": int(len(y_rank)), "n_leagues": int(len(set(groups))), "rho_partial_spearman": float(rho), "p_value_two_sided": float(pvalue)}


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("status\nNO_ROWS\n", encoding="utf-8")
        return
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def run_experiment(frame, selected_ids, archive_meta, out_dir, lag_hours):
    frame = add_eligibility_and_labels(frame)
    metrics_rows, reliability, paired_rows = [], [], []
    multiplicity_tests, league_coverage, feature_coverage = [], [], []
    predictions, fold_sizes = {}, {}
    windows = [(name, start, end) for name, start, end in FOLDS]

    for fold_name, test_start, test_end in windows:
        raw_test = frame[(frame["kickoff_date"] >= test_start) & (frame["kickoff_date"] < test_end)]
        core_test = raw_test[raw_test["core_eligible"]]
        test = raw_test[raw_test["venue_eligible"]].copy()
        train = frame[
            (frame["kickoff_date"] >= TRAIN_START)
            & (frame["kickoff_date"] < test_start)
            & frame["venue_eligible"]
        ].copy()
        fold_sizes[fold_name] = {
            "train_n": int(len(train)), "test_raw_home_away_distinguished_settled_n": int(len(raw_test)),
            "test_core_5plus_n": int(len(core_test)), "test_venue_5plus_n": int(len(test)),
            "test_leagues_n": int(test["selected_id"].nunique()),
        }
        feature_coverage.append({
            "window": fold_name, "raw_home_away_distinguished_settled_n": int(len(raw_test)),
            "core_5plus_n": int(len(core_test)), "venue_5plus_n": int(len(test)),
            "h2h_5plus_n": int(raw_test["h2h_eligible"].sum()),
            "venue_eligible_pct_of_raw": round(100 * len(test) / len(raw_test), 4) if len(raw_test) else np.nan,
            "h2h_5plus_pct_of_raw": round(100 * raw_test["h2h_eligible"].mean(), 4) if len(raw_test) else np.nan,
        })
        for sid in selected_ids:
            league_coverage.append({
                "window": fold_name, "selected_id": sid,
                "raw_home_away_distinguished_settled_n": int((raw_test["selected_id"] == sid).sum()),
                "core_5plus_n": int((core_test["selected_id"] == sid).sum()),
                "venue_5plus_n": int((test["selected_id"] == sid).sum()),
                "h2h_5plus_n": int(((raw_test["selected_id"] == sid) & raw_test["h2h_eligible"]).sum()),
            })
        if len(train) < 100 or len(test) < 30:
            raise ValueError(f"{fold_name} sample too small: train={len(train)}, test={len(test)}")

        for market in MARKETS:
            y_train = train[f"y_{market}"].to_numpy(dtype=int)
            y_test = test[f"y_{market}"].to_numpy(dtype=int)
            if len(np.unique(y_train)) < 2:
                raise ValueError(f"{fold_name}/{market}: training outcome has one class")
            for model_name, numeric_columns in MODEL_FEATURES.items():
                model = build_model(numeric_columns)
                cols = ["selected_id"] + list(numeric_columns)
                model.fit(train[cols], y_train)
                p = model.predict_proba(test[cols])[:, 1]
                pred = pd.DataFrame({"selected_id": test["selected_id"].to_numpy(), "y": y_test, "p": p}, index=test.index)
                for col in MAIN_NUMERIC + list(INTERACTIONS):
                    pred[col] = test[col].to_numpy()
                predictions[(fold_name, market, model_name)] = pred
                metrics_rows.append({
                    "window": fold_name, "market": market, "model": model_name,
                    "n_train": int(len(train)), "n_test": int(len(test)),
                    "n_leagues": int(test["selected_id"].nunique()),
                    "brier": metric_value("brier", y_test, p),
                    "log_loss": metric_value("log_loss", y_test, p),
                    "auc": metric_value("auc", y_test, p),
                    "ece10": metric_value("ece10", y_test, p),
                })
                reliability.extend(reliability_rows(y_test, p, market, model_name, fold_name))

    for market in MARKETS:
        for model_name in MODEL_FEATURES:
            pooled = pd.concat([predictions[(fold, market, model_name)] for fold, _, _ in windows], axis=0).sort_index()
            predictions[("POOLED_OOS", market, model_name)] = pooled
            y, p = pooled["y"].to_numpy(dtype=int), pooled["p"].to_numpy(dtype=float)
            metrics_rows.append({
                "window": "POOLED_OOS", "market": market, "model": model_name,
                "n_train": np.nan, "n_test": int(len(p)), "n_leagues": int(pooled["selected_id"].nunique()),
                "brier": metric_value("brier", y, p), "log_loss": metric_value("log_loss", y, p),
                "auc": metric_value("auc", y, p), "ece10": metric_value("ece10", y, p),
            })
            reliability.extend(reliability_rows(y, p, market, model_name, "POOLED_OOS"))

    compare_windows = [name for name, _, _ in windows] + ["POOLED_OOS"]
    for window_name in compare_windows:
        for market in MARKETS:
            for comparison_name, challenger_name, baseline_name in COMPARISONS:
                challenger = predictions[(window_name, market, challenger_name)]
                baseline = predictions[(window_name, market, baseline_name)]
                if not challenger.index.equals(baseline.index):
                    raise ValueError(f"Paired fixture index mismatch: {window_name}/{market}/{comparison_name}")
                y, groups = challenger["y"].to_numpy(dtype=int), challenger["selected_id"].to_numpy(dtype=str)
                for metric in METRICS:
                    paired = paired_cluster_summary(y, challenger["p"].to_numpy(), baseline["p"].to_numpy(), groups, metric)
                    paired_rows.append({
                        "window": window_name, "market": market, "comparison": comparison_name,
                        "challenger": challenger_name, "baseline": baseline_name, "metric": metric,
                        "n_test": int(len(y)), **paired,
                    })
                    multiplicity_tests.append({
                        "test_id": f"{window_name}|{market}|{comparison_name}|{metric}",
                        "test_type": "PAIRED_LEAGUE_CLUSTER_IMPROVEMENT",
                        "window": window_name, "market": market, "comparison": comparison_name,
                        "metric": metric, "n": int(len(y)), "p_value": paired["p_value_one_sided"],
                    })

    partial_rows = []
    for market in MARKETS:
        pooled = predictions[("POOLED_OOS", market, "main_effects")]
        y, groups = pooled["y"].to_numpy(dtype=int), pooled["selected_id"].to_numpy(dtype=str)
        for name, spec in INTERACTIONS.items():
            result = partial_spearman(
                y, pooled[name].to_numpy(dtype=float),
                {key: pooled[key].to_numpy(dtype=float) for key in spec["constituents"]}, groups,
            )
            partial_rows.append({"window": "POOLED_OOS", "market": market, "interaction": name, "formula": spec["formula"], **result})
            multiplicity_tests.append({
                "test_id": f"POOLED_OOS|{market}|PARTIAL_SPEARMAN|{name}",
                "test_type": "CONSTITUENT_CONTROLLED_PARTIAL_SPEARMAN",
                "window": "POOLED_OOS", "market": market, "comparison": name,
                "metric": "partial_spearman", "n": int(result.get("n", 0)),
                "p_value": result.get("p_value_two_sided", np.nan),
            })

    bh, by = adjust_bh_by([row["p_value"] for row in multiplicity_tests])
    for i, row in enumerate(multiplicity_tests):
        row["q_value_bh"] = float(bh[i]) if np.isfinite(bh[i]) else np.nan
        row["q_value_by"] = float(by[i]) if np.isfinite(by[i]) else np.nan

    for fold_name, start, end in windows:
        raw = frame[(frame["kickoff_date"] >= start) & (frame["kickoff_date"] < end)]
        for column in MAIN_NUMERIC + list(INTERACTIONS):
            feature_coverage.append({
                "window": f"{fold_name}_MISSINGNESS", "feature": column,
                "raw_home_away_distinguished_settled_n": int(len(raw)),
                "missing_n": int(raw[column].isna().sum()),
                "missing_pct": round(100 * raw[column].isna().mean(), 4) if len(raw) else np.nan,
            })

    pooled_raw = frame[(frame["kickoff_date"] >= PRIMARY_START) & (frame["kickoff_date"] <= PRIMARY_END)]
    pooled_core = pooled_raw[pooled_raw["core_eligible"]]
    pooled_eligible = pooled_raw[pooled_raw["venue_eligible"]]
    for sid in selected_ids:
        league_coverage.append({
            "window": "POOLED_OOS", "selected_id": sid,
            "raw_home_away_distinguished_settled_n": int((pooled_raw["selected_id"] == sid).sum()),
            "core_5plus_n": int((pooled_core["selected_id"] == sid).sum()),
            "venue_5plus_n": int((pooled_eligible["selected_id"] == sid).sum()),
            "h2h_5plus_n": int(((pooled_raw["selected_id"] == sid) & pooled_raw["h2h_eligible"]).sum()),
        })
    feature_coverage.append({
        "window": "POOLED_OOS", "raw_home_away_distinguished_settled_n": int(len(pooled_raw)),
        "core_5plus_n": int(len(pooled_core)), "venue_5plus_n": int(len(pooled_eligible)),
        "h2h_5plus_n": int(pooled_raw["h2h_eligible"].sum()),
        "venue_eligible_pct_of_raw": round(100 * len(pooled_eligible) / len(pooled_raw), 4) if len(pooled_raw) else np.nan,
        "h2h_5plus_pct_of_raw": round(100 * pooled_raw["h2h_eligible"].mean(), 4) if len(pooled_raw) else np.nan,
    })

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "fold_metrics.csv", metrics_rows)
    write_csv(out_dir / "paired_confidence_intervals.csv", paired_rows)
    write_csv(out_dir / "multiplicity_bh_by.csv", multiplicity_tests)
    write_csv(out_dir / "partial_spearman.csv", partial_rows)
    write_csv(out_dir / "reliability_bins.csv", reliability)
    write_csv(out_dir / "league_coverage.csv", league_coverage)
    write_csv(out_dir / "feature_coverage_and_missingness.csv", feature_coverage)

    counts = {
        "primary_home_away_distinguished_settled_targets": int(len(pooled_raw)),
        "core_five_match_eligible": int(len(pooled_core)),
        "venue_five_match_eligible": int(len(pooled_eligible)),
        "h2h_five_plus": int(pooled_raw["h2h_eligible"].sum()),
        "eligible_leagues": int(pooled_eligible["selected_id"].nunique()),
    }
    bh_pass = sum(np.isfinite(r["q_value_bh"]) and r["q_value_bh"] < 0.05 for r in multiplicity_tests)
    by_pass = sum(np.isfinite(r["q_value_by"]) and r["q_value_by"] < 0.05 for r in multiplicity_tests)
    summary = {
        "run": "ORACLE_MARKET_INTELLIGENCE_SIGNAL_DISCOVERY_RUN6_FULL_SELECTED50",
        "archive": archive_meta,
        "event_time_panel": {
            "rows": int(len(frame)), "history_lag_hours": float(lag_hours),
            "history_cutoff_rule": "prior kickoff strictly earlier than target kickoff; same-kickoff results appended after all targets",
            "training_start": TRAIN_START.isoformat(), "primary_window_start": PRIMARY_START.isoformat(),
            "primary_window_end_inclusive": PRIMARY_END.isoformat(), "folds": fold_sizes,
            "pooled_eligible_counts": counts,
        },
        "models": {
            "estimator": "LogisticRegression(C=0.1, solver=lbfgs, max_iter=2500)",
            "league_baseline": "selected_id one-hot only", "main_effects": MAIN_NUMERIC,
            "candidate_interactions": INTERACTIONS, "calibration": "NOT_APPLIED", "hyperparameter_tuning": "NONE",
        },
        "multiplicity": {
            "joint_tests": len(multiplicity_tests), "bh_q_lt_0_05": int(bh_pass), "by_q_lt_0_05": int(by_pass),
            "family": "all paired model-improvement tests across markets/folds/pooled windows plus pooled constituent-controlled partial-Spearman tests",
        },
        "oracle_v16_baseline": {
            "status": "BLOCKED_NO_MATCHING_HISTORICAL_FIXTURE_LEVEL_V1_6_LEDGER",
            "reason": "The accessible canonical archive contains 210 predictions, all model_version FOUR_MODEL_PREDICTION_ENGINE_V1.2 and model_status CHALLENGER; settlement and feature-snapshot manifests are header-only. No matching V1.6 fixture probabilities exist for these historical folds.",
        },
        "original_run8_assets": {
            "workbook_recovered": False, "workbook_sha256": "66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7",
            "workbook_bytes": 17301081, "companion_bundle_recovered": False,
            "companion_bundle_sha256": "b44e99c3ee9b1e1e4515739d810ec10b0bab1c8c718ef2918ec3f1bf78a08e2f",
            "companion_bundle_bytes": 29242558,
            "blocker": "Neither binary is present in the 402-file Library spreadsheet/ZIP inventory or the research repository tree; only manifests, summaries and checksums are committed.",
        },
        "provenance_limits": {
            "provider_publication_timestamps_verified": False, "event_time_is_not_source_publication_time": True,
            "official_settlement_truth_verified": False, "xg_used": False, "provisional_standings_used": False,
            "no_home_away_flag_1_means": "home/away undistinguished; not proof of neutral venue",
            "venue_role_eligibility": "only explicit no_home_away=0 records",
        },
        "governance": {
            "provider_api_credits_used": 0, "raw_provider_rows_exported": False,
            "fixture_level_predictions_exported": False, "feature_panel_exported": False,
            "production_logic_changed": False, "production_probabilities_changed": False,
            "canonical_ledgers_changed": False, "production_workflows_changed": False,
            "production_eligible": False, "betting_eligible": False,
        },
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    report = [
        "# Project Oracle — Run 6 Full Selected-50 Event-Time Nested Ablations",
        "", "**Research-only.** No production or betting eligibility is granted.",
        f"- Pinned archive SHA-256: {archive_meta['archive_sha256']}",
        f"- Raw archive rows: {archive_meta['archive_raw_rows']:,}; retained event-time records: {archive_meta['records_retained_for_event_time']:,}.",
        f"- Primary home/away-distinguished settled targets: {counts['primary_home_away_distinguished_settled_targets']:,}.",
        f"- Core five-match eligible: {counts['core_five_match_eligible']:,}; venue five-match eligible: {counts['venue_five_match_eligible']:,}.",
        f"- Eligible league groups: {counts['eligible_leagues']}/50.",
        "- History rule: strict earlier-than-kickoff; no extra 24-hour lag. This follows the original Run 8 methodology document; a later checkpoint note mentioning 24 hours conflicted with that source specification.",
        "- The source no_home_away flag is interpreted conservatively: 1 means home/away undistinguished, not proof of a neutral venue; only explicit 0 is used for venue-role histories and target eligibility.",
        "", "## Pooled nested interaction deltas", "",
        "Deltas are challenger minus main-effects. Negative Brier/log-loss/ECE is better; positive AUC is better.",
        "", "| Market | Comparison | Metric | Pooled delta | League-cluster 95% CI | BY q |",
        "|---|---|---|---:|---:|---:|",
    ]
    mult_lookup = {r["test_id"]: r for r in multiplicity_tests}
    for row in paired_rows:
        if row["window"] != "POOLED_OOS" or row["comparison"] == "main_effects_vs_league_only":
            continue
        key = f"{row['window']}|{row['market']}|{row['comparison']}|{row['metric']}"
        q = mult_lookup.get(key, {}).get("q_value_by", np.nan)
        report.append(
            f"| {row['market']} | {row['comparison']} | {row['metric']} | {row['pooled_delta']:.6f} | "
            f"[{row['ci95_low_cluster_mean']:.6f}, {row['ci95_high_cluster_mean']:.6f}] | {q:.6f} |"
        )
    report += [
        "", "## Baselines and blockers", "",
        "- League-only and main-effects models use the same eligible fixtures in each fold.",
        "- Frozen Oracle V1.6 comparison is BLOCKED: no matching fixture-level V1.6 probabilities or settlements are available.",
        "- Original Run 8 v18 workbook and companion bundle remain unavailable; this is a transparent full-Selected-50 rebuild from the checksum-pinned archive, not a byte-identical recovery.",
        "- Provider publication timestamps are unavailable; event-time chronology is not proof of source publication time.",
        "- xG without verified capture timestamps and provisional standings were excluded.",
        "- No raw provider rows, fixture-level predictions or feature panel are exported.",
        "", f"Joint multiplicity family: {len(multiplicity_tests)} tests; BH q<0.05: {bh_pass}; BY q<0.05: {by_pass}.",
    ]
    (out_dir / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (out_dir / "archive_sha256.txt").write_text(archive_meta["archive_sha256"] + "\n", encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--selected-manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--expected-sha256", default=EXPECTED_ARCHIVE_SHA256)
    parser.add_argument("--history-lag-hours", type=float, default=0.0)
    args = parser.parse_args()
    if args.history_lag_hours < 0:
        raise ValueError("history lag hours must be nonnegative")
    records, selected_ids, archive_meta = read_archive(args.archive, args.selected_manifest, args.expected_sha256)
    panel = build_event_time_panel(records, TRAIN_START, PRIMARY_END, lag_hours=args.history_lag_hours)
    summary = run_experiment(panel, selected_ids, archive_meta, args.out, args.history_lag_hours)
    print(json.dumps({
        "status": "SUCCESS_RESEARCH_ONLY", "archive_sha256": archive_meta["archive_sha256"],
        "panel_rows": len(panel), "pooled_eligible": summary["event_time_panel"]["pooled_eligible_counts"],
        "v16_baseline": summary["oracle_v16_baseline"]["status"], "provider_api_credits_used": 0,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
