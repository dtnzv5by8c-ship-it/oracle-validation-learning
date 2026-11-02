#!/usr/bin/env python3
"""Research-only chronological calibration experiment for the Run 8 Selected-50 venue model.

The pinned archive is read-only. Raw provider rows, event-time panels and fixture-level
predictions remain in memory; only aggregate metrics and coverage are exported.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import timedelta
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
from scipy.special import logit
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression

from scripts.run8_full_archive_nested_ablations import (
    FOLDS,
    TRAIN_START,
    PRIMARY_START,
    PRIMARY_END,
    MAIN_NUMERIC,
    OVERALL_NUMERIC,
    MARKETS,
    add_eligibility_and_labels,
    build_event_time_panel,
    build_model,
    metric_value,
    reliability_rows,
    paired_cluster_summary,
    adjust_bh_by,
    read_archive,
)

MODEL_FEATURES = {
    "league_only": [],
    "overall_form_only": OVERALL_NUMERIC,
    "main_effects": MAIN_NUMERIC,
}
METHODS = ("raw", "platt", "isotonic")
COMPARISONS = (
    ("main_effects_platt_vs_raw", ("main_effects", "platt"), ("main_effects", "raw")),
    ("main_effects_isotonic_vs_raw", ("main_effects", "isotonic"), ("main_effects", "raw")),
    ("overall_form_platt_vs_raw", ("overall_form_only", "platt"), ("overall_form_only", "raw")),
    ("overall_form_isotonic_vs_raw", ("overall_form_only", "isotonic"), ("overall_form_only", "raw")),
    ("league_only_platt_vs_raw", ("league_only", "platt"), ("league_only", "raw")),
    ("league_only_isotonic_vs_raw", ("league_only", "isotonic"), ("league_only", "raw")),
    ("main_effects_platt_vs_overall_form_platt", ("main_effects", "platt"), ("overall_form_only", "platt")),
    ("main_effects_isotonic_vs_overall_form_isotonic", ("main_effects", "isotonic"), ("overall_form_only", "isotonic")),
    ("main_effects_platt_vs_league_only_platt", ("main_effects", "platt"), ("league_only", "platt")),
    ("main_effects_isotonic_vs_league_only_isotonic", ("main_effects", "isotonic"), ("league_only", "isotonic")),
    ("main_effects_raw_vs_overall_form_raw", ("main_effects", "raw"), ("overall_form_only", "raw")),
    ("main_effects_raw_vs_league_only_raw", ("main_effects", "raw"), ("league_only", "raw")),
    ("main_effects_platt_vs_isotonic", ("main_effects", "platt"), ("main_effects", "isotonic")),
)
METRICS = ("brier", "log_loss", "auc", "ece10")
EXPECTED_ARCHIVE_SHA256 = "bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261"


def temporal_windows(test_start, test_end, calibration_days=90, train_start=TRAIN_START):
    """Return disjoint train/calibration/test date bounds for one expanding fold."""
    calibration_start = test_start - timedelta(days=int(calibration_days))
    return {
        "train_start": train_start,
        "train_end_exclusive": calibration_start,
        "calibration_start": calibration_start,
        "calibration_end_exclusive": test_start,
        "test_start": test_start,
        "test_end_exclusive": test_end,
    }


def fit_calibrator(method, probabilities, outcomes, min_calibration_n=500):
    """Fit a calibrator on the reserved calibration window only."""
    p = np.clip(np.asarray(probabilities, dtype=float), 1e-5, 1 - 1e-5)
    y = np.asarray(outcomes, dtype=int)
    if len(p) != len(y):
        raise ValueError("Calibration probabilities/outcomes length mismatch")
    if len(y) < int(min_calibration_n):
        return None, f"CALIBRATION_N_BELOW_MINIMUM:{len(y)}<{int(min_calibration_n)}"
    if len(np.unique(y)) < 2:
        return None, "CALIBRATION_WINDOW_HAS_ONE_OUTCOME_CLASS"
    if method == "platt":
        model = LogisticRegression(C=1000.0, solver="lbfgs", max_iter=2000)
        model.fit(logit(p).reshape(-1, 1), y)
        return model, "FITTED"
    if method == "isotonic":
        if len(np.unique(p)) < 10:
            return None, "INSUFFICIENT_DISTINCT_CALIBRATION_SCORES"
        model = IsotonicRegression(y_min=1e-5, y_max=1 - 1e-5, out_of_bounds="clip")
        model.fit(p, y)
        return model, "FITTED"
    raise ValueError(f"Unknown calibration method: {method}")


def apply_calibrator(method, calibrator, probabilities):
    p = np.clip(np.asarray(probabilities, dtype=float), 1e-5, 1 - 1e-5)
    if method == "raw":
        return p
    if calibrator is None:
        raise ValueError(f"Cannot apply unavailable {method} calibrator")
    if method == "platt":
        return np.clip(calibrator.predict_proba(logit(p).reshape(-1, 1))[:, 1], 1e-5, 1 - 1e-5)
    if method == "isotonic":
        return np.clip(calibrator.predict(p), 1e-5, 1 - 1e-5)
    raise ValueError(f"Unknown calibration method: {method}")


def calibration_slope_intercept(y, probabilities):
    """Diagnostic-only logistic recalibration slope/intercept on the held-out test set."""
    y = np.asarray(y, dtype=int)
    p = np.clip(np.asarray(probabilities, dtype=float), 1e-5, 1 - 1e-5)
    if len(np.unique(y)) < 2 or len(y) < 30:
        return np.nan, np.nan
    model = LogisticRegression(C=1e6, solver="lbfgs", max_iter=2000)
    model.fit(logit(p).reshape(-1, 1), y)
    return float(model.intercept_[0]), float(model.coef_[0, 0])


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("status\nNO_ROWS\n", encoding="utf-8")
        return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _slice(frame, start, end):
    return frame[(frame["kickoff_date"] >= start) & (frame["kickoff_date"] < end)].copy()


def run_calibration(frame, selected_ids, archive_meta, out_dir, calibration_days=90, min_calibration_n=500):
    frame = add_eligibility_and_labels(frame)
    predictions = {}
    metrics_rows, reliability, calibration_status = [], [], []
    paired_rows, coverage_rows, league_rows, missing_rows = [], [], [], []
    fold_records = {}

    for fold_name, test_start, test_end in FOLDS:
        bounds = temporal_windows(test_start, test_end, calibration_days)
        train_raw = _slice(frame, bounds["train_start"], bounds["train_end_exclusive"])
        calibration_raw = _slice(frame, bounds["calibration_start"], bounds["calibration_end_exclusive"])
        test_raw = _slice(frame, bounds["test_start"], bounds["test_end_exclusive"])
        train = train_raw[train_raw["venue_eligible"]].copy()
        calibration = calibration_raw[calibration_raw["venue_eligible"]].copy()
        test = test_raw[test_raw["venue_eligible"]].copy()

        if len(train) < 100 or len(calibration) < min_calibration_n or len(test) < 30:
            raise ValueError(
                f"{fold_name} insufficient samples: train={len(train)}, "
                f"calibration={len(calibration)}, test={len(test)}"
            )

        fold_records[fold_name] = {
            "train": train, "calibration": calibration, "test": test,
            "train_raw": train_raw, "calibration_raw": calibration_raw, "test_raw": test_raw,
            "bounds": bounds,
        }
        coverage_rows.append({
            "window": fold_name,
            "train_start": bounds["train_start"].isoformat(),
            "train_end_exclusive": bounds["train_end_exclusive"].isoformat(),
            "calibration_start": bounds["calibration_start"].isoformat(),
            "calibration_end_exclusive": bounds["calibration_end_exclusive"].isoformat(),
            "test_start": bounds["test_start"].isoformat(),
            "test_end_exclusive": bounds["test_end_exclusive"].isoformat(),
            "train_raw_n": int(len(train_raw)), "train_venue_5plus_n": int(len(train)),
            "calibration_raw_n": int(len(calibration_raw)), "calibration_venue_5plus_n": int(len(calibration)),
            "test_raw_n": int(len(test_raw)), "test_core_5plus_n": int(test_raw["core_eligible"].sum()),
            "test_venue_5plus_n": int(len(test)),
            "train_leagues_n": int(train["selected_id"].nunique()),
            "calibration_leagues_n": int(calibration["selected_id"].nunique()),
            "test_leagues_n": int(test["selected_id"].nunique()),
            "calibration_h2h_5plus_n": int(calibration["h2h_eligible"].sum()),
            "test_h2h_5plus_n": int(test["h2h_eligible"].sum()),
        })

        for sid in selected_ids:
            league_rows.append({
                "window": fold_name, "selected_id": sid,
                "train_venue_5plus_n": int((train["selected_id"] == sid).sum()),
                "calibration_venue_5plus_n": int((calibration["selected_id"] == sid).sum()),
                "test_venue_5plus_n": int((test["selected_id"] == sid).sum()),
                "test_core_5plus_n": int((test_raw.loc[test_raw["selected_id"] == sid, "core_eligible"]).sum()),
                "test_h2h_5plus_n": int(((test_raw["selected_id"] == sid) & test_raw["h2h_eligible"]).sum()),
            })

        for period_name, raw_period, eligible_period in (
            ("TRAIN", train_raw, train), ("CALIBRATION", calibration_raw, calibration), ("TEST", test_raw, test)
        ):
            for column in list(MAIN_NUMERIC) + ["h2h_last5_btts_rate", "h2h_last5_over25_rate"]:
                missing_rows.append({
                    "window": fold_name, "period": period_name, "feature": column,
                    "raw_n": int(len(raw_period)), "eligible_n": int(len(eligible_period)),
                    "missing_n_raw": int(raw_period[column].isna().sum()),
                    "missing_pct_raw": float(raw_period[column].isna().mean() * 100) if len(raw_period) else np.nan,
                    "missing_n_eligible": int(eligible_period[column].isna().sum()),
                    "missing_pct_eligible": float(eligible_period[column].isna().mean() * 100) if len(eligible_period) else np.nan,
                })

        for market in MARKETS:
            y_train = train[f"y_{market}"].to_numpy(dtype=int)
            y_cal = calibration[f"y_{market}"].to_numpy(dtype=int)
            y_test = test[f"y_{market}"].to_numpy(dtype=int)
            if len(np.unique(y_train)) < 2:
                raise ValueError(f"{fold_name}/{market}: training has one outcome class")
            if len(np.unique(y_cal)) < 2:
                raise ValueError(f"{fold_name}/{market}: calibration has one outcome class")

            for model_name, numeric_columns in MODEL_FEATURES.items():
                cols = ["selected_id"] + list(numeric_columns)
                model = build_model(numeric_columns)
                model.fit(train[cols], y_train)
                p_cal_raw = model.predict_proba(calibration[cols])[:, 1]
                p_test_raw = model.predict_proba(test[cols])[:, 1]

                predictions[(fold_name, market, model_name, "raw")] = pd.DataFrame({
                    "selected_id": test["selected_id"].to_numpy(), "y": y_test, "p": p_test_raw
                }, index=test.index)
                calibration_status.append({
                    "window": fold_name, "market": market, "model": model_name, "method": "raw",
                    "status": "AVAILABLE", "calibration_n": int(len(y_cal)),
                    "calibration_positive_n": int(y_cal.sum()), "calibration_negative_n": int((1-y_cal).sum()),
                    "minimum_n": int(min_calibration_n), "reason": "NO_CALIBRATOR_REQUIRED",
                })

                for method in ("platt", "isotonic"):
                    calibrator, status = fit_calibrator(method, p_cal_raw, y_cal, min_calibration_n)
                    calibration_status.append({
                        "window": fold_name, "market": market, "model": model_name, "method": method,
                        "status": "AVAILABLE" if calibrator is not None else "BLOCKED",
                        "calibration_n": int(len(y_cal)), "calibration_positive_n": int(y_cal.sum()),
                        "calibration_negative_n": int((1-y_cal).sum()), "minimum_n": int(min_calibration_n),
                        "reason": status,
                    })
                    if calibrator is None:
                        continue
                    p_test = apply_calibrator(method, calibrator, p_test_raw)
                    predictions[(fold_name, market, model_name, method)] = pd.DataFrame({
                        "selected_id": test["selected_id"].to_numpy(), "y": y_test, "p": p_test
                    }, index=test.index)

    for fold_name, _, _ in FOLDS:
        test = fold_records[fold_name]["test"]
        train = fold_records[fold_name]["train"]
        calibration = fold_records[fold_name]["calibration"]
        for market in MARKETS:
            y = test[f"y_{market}"].to_numpy(dtype=int)
            for model_name in MODEL_FEATURES:
                for method in METHODS:
                    key = (fold_name, market, model_name, method)
                    if key not in predictions:
                        continue
                    p = predictions[key]["p"].to_numpy(dtype=float)
                    intercept, slope = calibration_slope_intercept(y, p)
                    metrics_rows.append({
                        "window": fold_name, "market": market, "model": model_name, "method": method,
                        "n_train": int(len(train)), "n_calibration": int(len(calibration)), "n_test": int(len(test)),
                        "n_test_positive": int(y.sum()), "n_test_negative": int((1-y).sum()),
                        "n_leagues": int(test["selected_id"].nunique()),
                        "brier": metric_value("brier", y, p), "log_loss": metric_value("log_loss", y, p),
                        "auc": metric_value("auc", y, p), "ece10": metric_value("ece10", y, p),
                        "test_calibration_intercept": intercept, "test_calibration_slope": slope,
                    })
                    reliability.extend(reliability_rows(y, p, market, f"{model_name}_{method}", fold_name))

    # Concatenate disjoint chronological test predictions for pooled OOS metrics.
    for market in MARKETS:
        for model_name in MODEL_FEATURES:
            for method in METHODS:
                chunks = [predictions[(fold, market, model_name, method)]
                          for fold, _, _ in FOLDS if (fold, market, model_name, method) in predictions]
                if len(chunks) != len(FOLDS):
                    continue
                pooled = pd.concat(chunks, axis=0).sort_index()
                predictions[("POOLED_OOS", market, model_name, method)] = pooled
                y, p = pooled["y"].to_numpy(dtype=int), pooled["p"].to_numpy(dtype=float)
                intercept, slope = calibration_slope_intercept(y, p)
                metrics_rows.append({
                    "window": "POOLED_OOS", "market": market, "model": model_name, "method": method,
                    "n_train": np.nan, "n_calibration": int(sum(len(fold_records[f][ "calibration"]) for f,_,_ in FOLDS)),
                    "n_test": int(len(p)), "n_test_positive": int(y.sum()), "n_test_negative": int((1-y).sum()),
                    "n_leagues": int(pooled["selected_id"].nunique()),
                    "brier": metric_value("brier", y, p), "log_loss": metric_value("log_loss", y, p),
                    "auc": metric_value("auc", y, p), "ece10": metric_value("ece10", y, p),
                    "test_calibration_intercept": intercept, "test_calibration_slope": slope,
                })
                reliability.extend(reliability_rows(y, p, market, f"{model_name}_{method}", "POOLED_OOS"))

    paired_rows = []
    windows = [name for name, _, _ in FOLDS] + ["POOLED_OOS"]
    for window in windows:
        for market in MARKETS:
            for comparison_name, challenger_key, baseline_key in COMPARISONS:
                ch_key = (window, market, challenger_key[0], challenger_key[1])
                base_key = (window, market, baseline_key[0], baseline_key[1])
                if ch_key not in predictions or base_key not in predictions:
                    continue
                ch, base = predictions[ch_key], predictions[base_key]
                if not ch.index.equals(base.index):
                    raise ValueError(f"Paired fixture mismatch: {window}/{market}/{comparison_name}")
                y = ch["y"].to_numpy(dtype=int)
                groups = ch["selected_id"].to_numpy(dtype=str)
                for metric in METRICS:
                    result = paired_cluster_summary(
                        y, ch["p"].to_numpy(dtype=float), base["p"].to_numpy(dtype=float), groups, metric
                    )
                    paired_rows.append({
                        "window": window, "market": market, "comparison": comparison_name, "metric": metric,
                        "challenger": f"{challenger_key[0]}_{challenger_key[1]}",
                        "baseline": f"{baseline_key[0]}_{baseline_key[1]}",
                        "n_test": int(len(y)), "n_leagues": int(len(set(groups))),
                        **result,
                    })

    pvals = [r["p_value_one_sided"] for r in paired_rows]
    bh, by = adjust_bh_by(pvals)
    for i, row in enumerate(paired_rows):
        row["test_id"] = f'{row["window"]}|{row["market"]}|{row["comparison"]}|{row["metric"]}'
        row["q_value_bh"] = float(bh[i]) if np.isfinite(bh[i]) else np.nan
        row["q_value_by"] = float(by[i]) if np.isfinite(by[i]) else np.nan

    # Pooled coverage across all three test folds.
    all_test = pd.concat([fold_records[f]["test"] for f, _, _ in FOLDS], axis=0).sort_index()
    all_raw_test = pd.concat([fold_records[f]["test_raw"] for f, _, _ in FOLDS], axis=0).sort_index()
    for sid in selected_ids:
        league_rows.append({
            "window": "POOLED_OOS", "selected_id": sid,
            "train_venue_5plus_n": np.nan, "calibration_venue_5plus_n": np.nan,
            "test_venue_5plus_n": int((all_test["selected_id"] == sid).sum()),
            "test_core_5plus_n": int((all_raw_test.loc[all_raw_test["selected_id"] == sid, "core_eligible"]).sum()),
            "test_h2h_5plus_n": int(((all_raw_test["selected_id"] == sid) & all_raw_test["h2h_eligible"]).sum()),
        })

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "fold_metrics.csv", metrics_rows)
    write_csv(out / "paired_calibration_comparisons.csv", paired_rows)
    write_csv(out / "calibration_status.csv", calibration_status)
    write_csv(out / "reliability_bins.csv", reliability)
    write_csv(out / "fold_coverage.csv", coverage_rows)
    write_csv(out / "league_coverage.csv", league_rows)
    write_csv(out / "feature_missingness.csv", missing_rows)

    pooled_n = int(len(all_test))
    eligible_leagues = int(all_test["selected_id"].nunique())
    summary = {
        "run": "ORACLE_SIGNAL_DISCOVERY_RUN8_SELECTED50_CHRONOLOGICAL_CALIBRATION",
        "archive": archive_meta,
        "original_run8_assets": {
            "workbook_status": "NOT_RECOVERED_FROM_LIBRARY_OR_REPOSITORY_INVENTORY",
            "workbook_sha256": "66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7",
            "companion_bundle_status": "NOT_RECOVERED_FROM_LIBRARY_OR_REPOSITORY_INVENTORY",
            "companion_bundle_sha256": "b44e99c3ee9b1e1e4515739d810ec10b0bab1c8c718ef2918ec3f1bf78a08e2f",
            "rebuild_source": "checksum-pinned Selected-50 archive",
        },
        "event_time_panel": {
            "training_start": TRAIN_START.isoformat(), "primary_start": PRIMARY_START.isoformat(),
            "primary_end_inclusive": PRIMARY_END.isoformat(), "history_lag_hours": 0,
            "history_rule": "strict earlier-than-kickoff; same-kickoff outcomes appended after all targets",
            "folds": coverage_rows, "pooled_test_venue_eligible_n": pooled_n,
            "pooled_test_leagues_n": eligible_leagues,
            "five_observed_match_minimum": True, "venue_home_away_n_minimum": 5,
            "h2h_features_require_n_at_least": 5, "pseudo_counts_used": False,
        },
        "calibration": {
            "calibration_days": int(calibration_days), "minimum_calibration_n": int(min_calibration_n),
            "methods": ["Platt logistic scaling on logit scores", "Isotonic regression"],
            "fit_rule": "each calibrator fitted only on its fold's immediately preceding 90-day calibration window",
            "test_used_for_fitting": False, "posthoc_test_calibration_is_diagnostic_only": True,
        },
        "models": list(MODEL_FEATURES),
        "markets": list(MARKETS),
        "multiplicity": {
            "joint_test_family_n": int(len(paired_rows)),
            "bh_q_below_0_05": int(sum(np.isfinite(r["q_value_bh"]) and r["q_value_bh"] < 0.05 for r in paired_rows)),
            "by_q_below_0_05": int(sum(np.isfinite(r["q_value_by"]) and r["q_value_by"] < 0.05 for r in paired_rows)),
        },
        "oracle_v16_baseline": {
            "status": "BLOCKED_NO_MATCHING_FIXTURE_LEVEL_FROZEN_V1_6_PROBABILITY_AND_SETTLEMENT_LEDGER",
            "substitution_performed": False,
        },
        "provenance": {
            "provider_publication_capture_timestamps_verified": False,
            "xg_without_verified_capture_timestamps": "QUARANTINED",
            "provisional_standings": "QUARANTINED",
            "labels": "pinned archive settled status and score fields; not independently verified official settlement",
        },
        "governance": {
            "provider_api_credits_used": 0, "raw_provider_rows_exported": False,
            "fixture_level_predictions_exported": False, "event_time_feature_panel_exported": False,
            "oracle_v16_production_logic_or_probabilities_changed": False,
            "canonical_ledgers_changed": False, "production_workflows_changed_or_dispatched": False,
            "production_eligible": False, "betting_eligible": False,
        },
        "results": {
            "fold_metric_rows": int(len(metrics_rows)), "paired_comparison_rows": int(len(paired_rows)),
            "reliability_rows": int(len(reliability)), "calibration_status_rows": int(len(calibration_status)),
        },
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")

    lines = [
        "# Project Oracle — Selected-50 Chronological Calibration Experiment",
        "",
        "**Research only. No production or betting eligibility.**",
        "",
        f"- Pinned archive SHA-256: `{archive_meta['archive_sha256']}`",
        f"- Pooled test cohort: {pooled_n:,} fixtures across {eligible_leagues}/50 contributing league groups.",
        f"- Calibration: {calibration_days}-day immediately preceding window; minimum N={min_calibration_n}.",
        "- Methods: raw, Platt scaling and isotonic regression.",
        "- Test outcomes were never used to fit the calibrators.",
        "- Overall and venue histories require five observed matches; H2H requires five observed prior meetings.",
        "- xG without verified capture timestamps and provisional standings remain excluded.",
        "",
        "## Interpretation",
        "",
        "Read `fold_metrics.csv` for fold and pooled Brier, log loss, AUC, ECE10, and held-out calibration intercept/slope. "
        "Read `paired_calibration_comparisons.csv` for paired league-cluster confidence intervals and joint BH/BY corrections. "
        "Read `reliability_bins.csv` for reliability curves and `feature_missingness.csv` for feature coverage.",
        "",
        "The post-hoc test calibration intercept/slope are diagnostic summaries only; they are not fitted corrections. "
        "No calibrated result is eligible for production or betting.",
        "",
        "## Baseline limitation",
        "",
        "Frozen Oracle V1.6 comparison remains blocked because no matching fixture-level frozen V1.6 probabilities and settlement ledger "
        "are available for these historical folds. Challenger outputs were not substituted.",
        "",
        "## Provenance limitation",
        "",
        "Historical feature ordering is strict event-time chronology, but provider publication/capture timestamps are not verified. "
        "This is not proof that every underlying source value was published before kickoff. Labels use archive settled-score fields, "
        "not an independently verified official settlement ledger.",
        "",
    ]
    (out / "report.md").write_text("\n".join(lines), encoding="utf-8")
    (out / "archive_sha256.txt").write_text(archive_meta["archive_sha256"] + "\n", encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True)
    parser.add_argument("--selected-manifest", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--calibration-days", type=int, default=90)
    parser.add_argument("--min-calibration-n", type=int, default=500)
    args = parser.parse_args()

    records, selected_ids, archive_meta = read_archive(
        args.archive, args.selected_manifest, expected_sha256=EXPECTED_ARCHIVE_SHA256
    )
    panel = build_event_time_panel(records, TRAIN_START, PRIMARY_END, lag_hours=0.0)
    summary = run_calibration(
        panel, selected_ids, archive_meta, args.out,
        calibration_days=args.calibration_days, min_calibration_n=args.min_calibration_n,
    )
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
