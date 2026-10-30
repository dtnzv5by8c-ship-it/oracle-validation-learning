#!/usr/bin/env python3
"""Research-only Selected-50 team/market exposure map.

This module uses only the existing fixture prediction report and runtime
provenance. It deliberately does not read H2H fields, historical paired
predictions, settlement files, or provider APIs. Outputs describe forecast
exposure and recent-form context; they are NOT team-performance rankings.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from statistics import median
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = {
    "fixture_id", "date_utc", "selected_id", "country", "league",
    "home_team_provider_id", "away_team_provider_id", "home_team", "away_team",
    "home_recent5_results", "away_recent5_results", "home_recent5_n",
    "away_recent5_n", "prediction_status", "feature_support_status",
    "BTTS_probability_pct", "DC_HOME_probability_pct", "DC_AWAY_probability_pct",
    "canonical_fixture_join_status", "canonical_team_join_status",
    "settlement_truth_status", "production_eligible", "calibration_status",
}
MARKET_SPECS = {
    "BTTS_FIXTURE_EXPOSURE": {
        "scope": "Fixture-level BTTS probability shared by both participating teams",
    },
    "DOUBLE_CHANCE_TEAM_SIDE": {
        "scope": "Probability that this team avoids defeat (win or draw) in its current home/away role",
    },
}


def parse_time(value: str | None):
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (TypeError, ValueError, OverflowError):
        return None
    if dt.tzinfo is None:
        return None
    return dt.astimezone(timezone.utc)


def as_float(value):
    try:
        x = float(value)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError, OverflowError):
        return None


def as_int(value, default=0):
    x = as_float(value)
    return int(x) if x is not None else default


def clean_wdl(value):
    return "".join(c for c in str(value or "").upper() if c in "WDL")


def probability_pct(value):
    x = as_float(value)
    return x if x is not None and 0 <= x <= 100 else None


def wilson_interval(successes: int, n: int, z: float = 1.959963984540054):
    if n <= 0:
        return None, None
    p = successes / n
    den = 1 + z * z / n
    center = (p + z * z / (2 * n)) / den
    half = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / den
    return max(0.0, center - half), min(1.0, center + half)


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _fixture_team_rows(fixtures):
    for row in fixtures:
        for role, id_key, name_key, form_key, n_key, dc_key in (
            ("HOME", "home_team_provider_id", "home_team", "home_recent5_results", "home_recent5_n", "DC_HOME_probability_pct"),
            ("AWAY", "away_team_provider_id", "away_team", "away_recent5_results", "away_recent5_n", "DC_AWAY_probability_pct"),
        ):
            team_id = str(row.get(id_key) or "").strip()
            team_name = str(row.get(name_key) or "").strip()
            if not team_id or not team_name:
                raise ValueError(f"Missing provider team ID/name for fixture {row.get('fixture_id')} role {role}")
            yield {
                "fixture": row,
                "role": role,
                "team_id": team_id,
                "team_name": team_name,
                "form": clean_wdl(row.get(form_key)),
                "reported_form_n": as_int(row.get(n_key), -1),
                "dc_team_side_probability": as_float(row.get(dc_key)),
            }


def _team_key(item):
    r = item["fixture"]
    return (
        str(r.get("selected_id") or ""),
        str(r.get("country") or ""),
        str(r.get("league") or ""),
        item["team_id"],
        item["team_name"],
        item["role"],
    )


def _team_profile(key, items):
    selected_id, country, league, team_id, team_name, role = key
    items = sorted(
        items,
        key=lambda x: (parse_time(x["fixture"].get("date_utc")) or datetime.min.replace(tzinfo=timezone.utc),
                      str(x["fixture"].get("fixture_id") or "")),
    )
    latest = items[-1]
    seq = latest["form"]
    n = len(seq)
    wins, draws, losses = seq.count("W"), seq.count("D"), seq.count("L")
    lo, hi = wilson_interval(wins, n)
    raw = [x for x in items if x["fixture"].get("prediction_status") == "RAW_RESEARCH_ONLY"]
    blocked = [x for x in items if x["fixture"].get("prediction_status") != "RAW_RESEARCH_ONLY"]
    complete = [x for x in items if x["fixture"].get("feature_support_status") == "PASS_ALL_20_REQUIRED_FEATURES"]
    mismatch = sum(1 for x in items if x["reported_form_n"] != len(x["form"]))
    btts_probs = [
        p for x in items
        if x["fixture"].get("prediction_status") == "RAW_RESEARCH_ONLY"
        and (p := probability_pct(x["fixture"].get("BTTS_probability_pct"))) is not None
    ]
    dc_probs = [
        p for x in items
        if x["fixture"].get("prediction_status") == "RAW_RESEARCH_ONLY"
        and (p := probability_pct(x["dc_team_side_probability"])) is not None
    ]
    latest_dt = parse_time(latest["fixture"].get("date_utc"))
    return {
        "selected_season_id_surrogate": selected_id,
        "country": country,
        "league": league,
        "provider_team_id": team_id,
        "team_name": team_name,
        "fixture_role": role,
        "fixture_appearances": len(items),
        "raw_prediction_appearances": len(raw),
        "blocked_appearances": len(blocked),
        "feature_complete_appearances": len(complete),
        "feature_incomplete_appearances": len(items) - len(complete),
        "latest_fixture_asof_utc": latest_dt.isoformat() if latest_dt else "",
        "latest_form_sequence": seq,
        "latest_form_n_observed": n,
        "latest_form_n_reported": latest["reported_form_n"],
        "latest_form_n_below_5": n < 5,
        "latest_form_n_mismatch": latest["reported_form_n"] != n,
        "latest_form_wins": wins,
        "latest_form_draws": draws,
        "latest_form_losses": losses,
        "latest_form_win_rate_pct": round(100 * wins / n, 2) if n else None,
        "latest_form_win_wilson95_low_pct": round(100 * lo, 2) if lo is not None else None,
        "latest_form_win_wilson95_high_pct": round(100 * hi, 2) if hi is not None else None,
        "latest_form_win_beta11_smoothed_pct": round(100 * (wins + 1) / (n + 2), 2) if n else None,
        "distinct_form_sequences_across_fixture_contexts": len({x["form"] for x in items}),
        "reported_vs_observed_form_n_mismatches": mismatch,
        "btts_fixture_probability_exposures": len(btts_probs),
        "btts_mean_probability_pct": round(sum(btts_probs) / len(btts_probs), 2) if btts_probs else None,
        "dc_team_side_probability_exposures": len(dc_probs),
        "dc_team_side_mean_probability_pct": round(sum(dc_probs) / len(dc_probs), 2) if dc_probs else None,
        "canonical_team_join_statuses": ";".join(sorted({str(x["fixture"].get("canonical_team_join_status") or "") for x in items})),
        "settlement_truth_statuses": ";".join(sorted({str(x["fixture"].get("settlement_truth_status") or "") for x in items})),
        "production_eligibility_statuses": ";".join(sorted({str(x["fixture"].get("production_eligible") or "") for x in items})),
        "calibration_statuses": ";".join(sorted({str(x["fixture"].get("calibration_status") or "") for x in items})),
    }


def _market_exposure(key, items, market):
    selected_id, country, league, team_id, team_name, role = key
    if market == "BTTS_FIXTURE_EXPOSURE":
        probs = [
            p for x in items
            if x["fixture"].get("prediction_status") == "RAW_RESEARCH_ONLY"
            and (p := probability_pct(x["fixture"].get("BTTS_probability_pct"))) is not None
        ]
    else:
        probs = [
            p for x in items
            if x["fixture"].get("prediction_status") == "RAW_RESEARCH_ONLY"
            and (p := probability_pct(x["dc_team_side_probability"])) is not None
        ]
    raw_n = sum(x["fixture"].get("prediction_status") == "RAW_RESEARCH_ONLY" for x in items)
    blocked_n = len(items) - raw_n
    return {
        "selected_season_id_surrogate": selected_id,
        "country": country,
        "league": league,
        "provider_team_id": team_id,
        "team_name": team_name,
        "fixture_role": role,
        "market_exposure": market,
        "probability_scope": MARKET_SPECS[market]["scope"],
        "fixture_exposures": len(items),
        "raw_prediction_exposures": raw_n,
        "blocked_exposures": blocked_n,
        "probability_observations": len(probs),
        "mean_probability_pct": round(sum(probs) / len(probs), 2) if probs else None,
        "median_probability_pct": round(median(probs), 2) if probs else None,
        "min_probability_pct": min(probs) if probs else None,
        "max_probability_pct": max(probs) if probs else None,
    }


def analyze(fixtures, provenance, as_of_utc):
    if not fixtures:
        raise ValueError("Prediction report is empty")
    missing = sorted(REQUIRED - set(fixtures[0]))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    fixture_ids = [str(r.get("fixture_id") or "").strip() for r in fixtures]
    if any(not x for x in fixture_ids) or len(fixture_ids) != len(set(fixture_ids)):
        raise ValueError("Fixture IDs must be non-empty and unique")
    if not provenance.get("generated_utc") or not provenance.get("runtime_archive_consumption_verified"):
        raise ValueError("Runtime provenance missing generation timestamp or verified archive-consumption flag")

    groups = defaultdict(list)
    team_id_names = defaultdict(set)
    for item in _fixture_team_rows(fixtures):
        groups[_team_key(item)].append(item)
        team_id_names[item["team_id"]].add(item["team_name"])

    team_rows, market_rows = [], []
    for key, items in sorted(groups.items()):
        team_rows.append(_team_profile(key, items))
        for market in MARKET_SPECS:
            market_rows.append(_market_exposure(key, items, market))

    league_groups = defaultdict(list)
    for row in team_rows:
        league_groups[(row["selected_season_id_surrogate"], row["country"], row["league"])].append(row)
    league_rows = []
    for (selected_id, country, league), items in sorted(league_groups.items()):
        league_rows.append({
            "selected_season_id_surrogate": selected_id,
            "country": country,
            "league": league,
            "distinct_provider_team_ids_in_fixture_context": len({r["provider_team_id"] for r in items}),
            "team_role_profiles": len(items),
            "fixture_exposures": sum(r["fixture_appearances"] for r in items),
            "raw_prediction_team_exposures": sum(r["raw_prediction_appearances"] for r in items),
            "blocked_team_exposures": sum(r["blocked_appearances"] for r in items),
            "profiles_latest_form_n_below_5": sum(bool(r["latest_form_n_below_5"]) for r in items),
            "profiles_with_feature_incomplete_appearances": sum(r["feature_incomplete_appearances"] > 0 for r in items),
            "mean_latest_form_n": round(sum(r["latest_form_n_observed"] for r in items) / len(items), 3) if items else None,
            "btts_fixture_probability_exposures": sum(r["btts_fixture_probability_exposures"] for r in items),
            "dc_team_side_probability_exposures": sum(r["dc_team_side_probability_exposures"] for r in items),
            "canonical_team_join_statuses": ";".join(sorted({r["canonical_team_join_statuses"] for r in items})),
            "settlement_truth_statuses": ";".join(sorted({r["settlement_truth_statuses"] for r in items})),
        })

    runtime_dt = parse_time(provenance.get("generated_utc"))
    snapshot_dt = parse_time(provenance.get("snapshot_retrieved_utc"))
    if runtime_dt is None:
        raise ValueError("Runtime generation timestamp must be timezone-aware")
    runtime_age = (as_of_utc - runtime_dt).total_seconds() / 3600
    snapshot_age = (as_of_utc - snapshot_dt).total_seconds() / 3600 if snapshot_dt else None

    status_counts = Counter(str(r.get("prediction_status") or "MISSING") for r in fixtures)
    probability_fields = {
        "BTTS": "BTTS_probability_pct",
        "DC_HOME": "DC_HOME_probability_pct",
        "DC_AWAY": "DC_AWAY_probability_pct",
        "COMBO_HOME": "COMBO_HOME_probability_pct",
        "COMBO_AWAY": "COMBO_AWAY_probability_pct",
    }
    market_probability_counts = {
        market: sum(probability_pct(r.get(field)) is not None for r in fixtures)
        for market, field in probability_fields.items()
    }
    invalid_probability_counts = {
        market: sum(
            as_float(r.get(field)) is not None and probability_pct(r.get(field)) is None
            for r in fixtures
        )
        for market, field in probability_fields.items()
    }
    canonical_fixture = Counter(str(r.get("canonical_fixture_join_status") or "") for r in fixtures)
    canonical_team = Counter(str(r.get("canonical_team_join_status") or "") for r in fixtures)
    settlement = Counter(str(r.get("settlement_truth_status") or "") for r in fixtures)
    summary = {
        "status": "RESEARCH_ONLY_TEAM_MARKET_EXPOSURE_MAP_COMPLETE",
        "analysis_asof_utc": as_of_utc.isoformat(),
        "source_runtime": {
            "runtime_run_id": provenance.get("runtime_run_id"),
            "runtime_run_number": provenance.get("runtime_run_number"),
            "runtime_generated_utc": runtime_dt.isoformat(),
            "runtime_age_hours_at_analysis": round(runtime_age, 2),
            "snapshot_retrieved_utc": snapshot_dt.isoformat() if snapshot_dt else None,
            "snapshot_age_hours_at_analysis": round(snapshot_age, 2) if snapshot_age is not None else None,
            "runtime_archive_sha256": provenance.get("overlay_archive_sha256"),
            "archive_consumption_verified": provenance.get("runtime_archive_consumption_verified"),
        },
        "fixture_context": {
            "fixture_rows": len(fixtures),
            "unique_fixture_ids": len(set(fixture_ids)),
            "selected_season_surrogates": len({str(r.get("selected_id") or "") for r in fixtures}),
            "country_league_groups": len({(r.get("country"), r.get("league")) for r in fixtures}),
            "countries": len({r.get("country") for r in fixtures}),
            "distinct_provider_team_ids": len(team_id_names),
            "provider_team_id_multiple_name_collisions": sum(len(v) > 1 for v in team_id_names.values()),
            "team_role_profiles": len(team_rows),
            "team_market_exposure_rows": len(market_rows),
            "league_rollup_rows": len(league_rows),
            "team_role_fixture_appearance_distribution": dict(Counter(str(r["fixture_appearances"]) for r in team_rows)),
        },
        "prediction_and_market_coverage": {
            "prediction_status_counts": dict(status_counts),
            "valid_probability_observation_counts_by_market": market_probability_counts,
            "invalid_numeric_probability_counts_by_market": invalid_probability_counts,
            "canonical_fixture_join_status_counts": dict(canonical_fixture),
            "canonical_team_join_status_counts": dict(canonical_team),
            "settlement_truth_status_counts": dict(settlement),
        },
        "team_context": {
            "profiles_with_latest_form_n_below_5": sum(r["latest_form_n_below_5"] for r in team_rows),
            "profiles_with_latest_form_n_mismatch": sum(r["latest_form_n_mismatch"] for r in team_rows),
            "profiles_with_multiple_distinct_form_sequences": sum(r["distinct_form_sequences_across_fixture_contexts"] > 1 for r in team_rows),
            "profiles_with_at_least_one_feature_incomplete_appearance": sum(r["feature_incomplete_appearances"] > 0 for r in team_rows),
        },
        "interpretation": {
            "performance_metrics_computed": False,
            "reason": "No verified team-attributed chronological prediction/settlement pairs are present in this fixture report.",
            "team_market_rows_are_exposure_not_accuracy": True,
            "btts_probability_is_fixture_level_and_shared_by_both_teams": True,
            "double_chance_team_side_probability_includes_draw": True,
            "canonical_identity_verified": False,
            "settlement_truth_verified": False,
            "probabilities_calibrated": False,
            "locked_h2h_holdout_read": False,
            "provider_api_calls": 0,
            "production_model_changed": False,
            "frozen_probabilities_changed": False,
            "production_eligible": False,
            "betting_eligible": False,
        },
        "next_action": "Use this exposure map only as a descriptive index. Build and validate a separate chronological team-attributed prediction/settlement ledger before calculating team-market performance or exclusions.",
    }
    return team_rows, market_rows, league_rows, summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prediction-report", required=True)
    ap.add_argument("--runtime-provenance", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--as-of-utc", default="")
    args = ap.parse_args()
    as_of = parse_time(args.as_of_utc) if args.as_of_utc else datetime.now(timezone.utc)
    if as_of is None:
        raise SystemExit("--as-of-utc must be timezone-aware ISO-8601")
    fixtures = read_csv(Path(args.prediction_report))
    provenance = json.loads(Path(args.runtime_provenance).read_text(encoding="utf-8"))
    team_rows, market_rows, league_rows, summary = analyze(fixtures, provenance, as_of)
    out = Path(args.out_dir)
    write_csv(out / "oracle_selected50_team_context_exposure.csv", team_rows, list(team_rows[0]))
    write_csv(out / "oracle_selected50_team_market_exposure.csv", market_rows, list(market_rows[0]))
    write_csv(out / "oracle_selected50_league_team_exposure_rollup.csv", league_rows, list(league_rows[0]))
    (out / "oracle_selected50_team_market_exposure_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
