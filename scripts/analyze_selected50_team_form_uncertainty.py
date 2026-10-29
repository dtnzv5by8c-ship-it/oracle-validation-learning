#!/usr/bin/env python3
"""Research-only uncertainty audit for current Selected-50 team form and fixture context.

Uses only oracle_selected50_prediction_report.csv from an existing runtime artifact.
It does not load historical paired H2H predictions, estimate team-level model accuracy,
or claim that form context identifies profitable markets. All outputs are diagnostics.
"""
from __future__ import annotations
import argparse, csv, json, math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

Z95 = 1.959963984540054

def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows):
    rows = list(rows)
    fields = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def as_int(value, default=0):
    try:
        return int(float(value)) if value not in ("", None) else default
    except (TypeError, ValueError, OverflowError):
        return default

def as_float(value):
    try:
        value = float(value)
        return value if math.isfinite(value) else None
    except (TypeError, ValueError, OverflowError):
        return None

def wilson_interval(successes: int, n: int, z: float = Z95):
    """Two-sided Wilson score interval for one binomial proportion."""
    if n <= 0 or successes < 0 or successes > n:
        return None, None
    p = successes / n
    den = 1 + z*z/n
    center = (p + z*z/(2*n)) / den
    half = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / den
    return max(0.0, center-half), min(1.0, center+half)

def clean_form(sequence):
    seq = (sequence or "").strip().upper()
    return "".join(c for c in seq if c in "WDL")

def form_metrics(sequence):
    seq = clean_form(sequence)
    n = len(seq)
    result = {"form_sequence": seq, "form_n_observed": n}
    for code in "WDL":
        k = seq.count(code)
        lo, hi = wilson_interval(k, n)
        key = code.lower()
        result[f"{key}_count"] = k
        result[f"{key}_rate_pct"] = round(100*k/n, 2) if n else ""
        result[f"{key}_wilson95_low_pct"] = round(100*lo, 2) if lo is not None else ""
        result[f"{key}_wilson95_high_pct"] = round(100*hi, 2) if hi is not None else ""
        # Beta(1,1) smoothing is descriptive only, not a calibrated forecast.
        result[f"{key}_beta11_smoothed_pct"] = round(100*(k+1)/(n+2), 2) if n else ""
    return result

def h2h_btts_interval(rate, h2h_sequence):
    """Use explicit last-meeting sequence length; fail closed if rate disagrees."""
    seq = clean_form(h2h_sequence)
    n = len(seq)
    if rate is None or n == 0:
        return n, None, None, "NOT_AVAILABLE"
    k_float = rate*n
    k = round(k_float)
    if abs(k_float-k) > 1e-6 or k < 0 or k > n:
        return n, None, None, "RATE_SAMPLE_CONSISTENCY_UNRESOLVED"
    lo, hi = wilson_interval(k, n)
    return n, round(100*lo, 2), round(100*hi, 2), "APPROXIMATE_CONTEXT_INTERVAL"

def build_team_profiles(fixtures):
    latest = {}
    appearances = Counter()
    for row in fixtures:
        for side in ("home", "away"):
            team = (row.get(f"{side}_team") or "").strip()
            if not team:
                continue
            key = (row.get("country", ""), row.get("league", ""), team, side)
            appearances[key] += 1
            kickoff = row.get("date_utc", "")
            stats = form_metrics(row.get(f"{side}_recent5_results", ""))
            reported_n = as_int(row.get(f"{side}_recent5_n"))
            profile = {
                "country": row.get("country", ""), "league": row.get("league", ""),
                "team": team, "role": side, "latest_fixture_kickoff_utc": kickoff,
                "recent_form_n_reported": reported_n,
                "recent_form_n_from_sequence": stats["form_n_observed"],
                "recent_form_completeness_pct": round(100*min(reported_n, 5)/5, 2),
                "upcoming_fixture_appearances": 0, **stats,
                "context_status": "FORM_CONTEXT_ONLY_NOT_TEAM_PERFORMANCE_DNA",
            }
            if key not in latest or kickoff > latest[key]["latest_fixture_kickoff_utc"]:
                latest[key] = profile
    output = []
    for key, row in latest.items():
        row["upcoming_fixture_appearances"] = appearances[key]
        output.append(row)
    return sorted(output, key=lambda r: (r["country"], r["league"], r["team"], r["role"]))

def build_fixture_context(fixtures):
    output, flag_counts = [], Counter()
    for row in fixtures:
        home = form_metrics(row.get("home_recent5_results", ""))
        away = form_metrics(row.get("away_recent5_results", ""))
        h2h_seq = row.get("h2h_last5_results_home_perspective", "")
        h2h_rate = as_float(row.get("h2h_btts_rate_last5"))
        h2h_n, h2h_lo, h2h_hi, h2h_ci_status = h2h_btts_interval(h2h_rate, h2h_seq)
        flags = []
        if row.get("prediction_status") == "BLOCKED_MISSING_REQUIRED_FEATURES":
            flags.append("BLOCKED_MISSING_REQUIRED_FEATURES")
        if as_int(row.get("home_recent5_n")) < 5:
            flags.append("HOME_FORM_SAMPLE_BELOW_5")
        if as_int(row.get("away_recent5_n")) < 5:
            flags.append("AWAY_FORM_SAMPLE_BELOW_5")
        if as_int(row.get("h2h_prior_n")) < 3:
            flags.append("LOW_OR_NO_H2H_HISTORY")
        if row.get("canonical_fixture_join_status") != "VERIFIED":
            flags.append("CANONICAL_FIXTURE_JOIN_UNVERIFIED")
        if row.get("canonical_team_join_status") != "VERIFIED":
            flags.append("CANONICAL_TEAM_JOIN_UNVERIFIED")
        if row.get("settlement_truth_status") != "VERIFIED":
            flags.append("SETTLEMENT_TRUTH_UNVERIFIED")
        if row.get("calibration_status") != "CALIBRATED":
            flags.append("PROBABILITIES_RAW_UNCALIBRATED")
        if row.get("odds_xg_provenance_status") != "VERIFIED":
            flags.append("ODDS_XG_PROVENANCE_UNVERIFIED")
        if h2h_ci_status == "RATE_SAMPLE_CONSISTENCY_UNRESOLVED":
            flags.append("H2H_RATE_SAMPLE_CONSISTENCY_UNRESOLVED")
        for flag in flags:
            flag_counts[flag] += 1
        output.append({
            "fixture_id": row.get("fixture_id", ""), "date_utc": row.get("date_utc", ""),
            "country": row.get("country", ""), "league": row.get("league", ""),
            "home_team": row.get("home_team", ""), "away_team": row.get("away_team", ""),
            "prediction_status": row.get("prediction_status", ""),
            "BTTS_probability_pct": row.get("BTTS_probability_pct", ""),
            "DC_HOME_probability_pct": row.get("DC_HOME_probability_pct", ""),
            "DC_AWAY_probability_pct": row.get("DC_AWAY_probability_pct", ""),
            "home_form_sequence": home["form_sequence"], "home_form_n": home["form_n_observed"],
            "home_recent_win_rate_pct": home["w_rate_pct"],
            "home_recent_win_wilson95_low_pct": home["w_wilson95_low_pct"],
            "home_recent_win_wilson95_high_pct": home["w_wilson95_high_pct"],
            "away_form_sequence": away["form_sequence"], "away_form_n": away["form_n_observed"],
            "away_recent_win_rate_pct": away["w_rate_pct"],
            "away_recent_win_wilson95_low_pct": away["w_wilson95_low_pct"],
            "away_recent_win_wilson95_high_pct": away["w_wilson95_high_pct"],
            "h2h_prior_n": as_int(row.get("h2h_prior_n")), "h2h_last5_sample_n": h2h_n,
            "h2h_btts_rate_last5": "" if h2h_rate is None else h2h_rate,
            "h2h_btts_wilson95_low_pct": "" if h2h_lo is None else h2h_lo,
            "h2h_btts_wilson95_high_pct": "" if h2h_hi is None else h2h_hi,
            "h2h_interval_status": h2h_ci_status,
            "h2h_avg_total_goals_last5": row.get("h2h_avg_total_goals_last5", ""),
            "context_quality_flags": "|".join(flags),
            "context_interpretation": "DESCRIPTIVE_CONTEXT_ONLY_NOT_MARKET_SUITABILITY_OR_BETTING_APPROVAL",
        })
    output.sort(key=lambda r: (r["date_utc"], r["country"], r["league"], r["home_team"]))
    return output, flag_counts

def self_test():
    lo, hi = wilson_interval(0, 5)
    assert round(lo, 4) == 0.0000 and round(hi, 4) == 0.4345
    lo, hi = wilson_interval(5, 5)
    assert round(lo, 4) == 0.5655 and round(hi, 4) == 1.0000
    assert form_metrics("WDL")["form_n_observed"] == 3
    assert form_metrics("WDL")["w_count"] == 1
    assert h2h_btts_interval(0.6, "WDLWW")[0] == 5
    assert h2h_btts_interval(0.6, "WDLWW")[3] == "APPROXIMATE_CONTEXT_INTERVAL"
    assert h2h_btts_interval(0.5, "WDLWW")[3] == "RATE_SAMPLE_CONSISTENCY_UNRESOLVED"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        if args.input_dir is None:
            print("SELF_TEST_PASS")
            return
    if args.input_dir is None or args.output_dir is None:
        parser.error("--input-dir and --output-dir are required unless --self-test is used alone")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fixtures = read_csv(args.input_dir / "oracle_selected50_prediction_report.csv")
    provenance_path = args.input_dir / "oracle_selected50_runtime_provenance.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8")) if provenance_path.exists() else {}
    generated = provenance.get("generated_utc", "")
    try:
        generated_dt = datetime.fromisoformat(generated.replace("Z", "+00:00"))
        age_hours = round((datetime.now(timezone.utc)-generated_dt.astimezone(timezone.utc)).total_seconds()/3600, 2)
    except (TypeError, ValueError):
        age_hours = None
    team_rows = build_team_profiles(fixtures)
    fixture_rows, flag_counts = build_fixture_context(fixtures)
    write_csv(args.output_dir / "oracle_selected50_team_form_uncertainty.csv", team_rows)
    write_csv(args.output_dir / "oracle_selected50_fixture_context_uncertainty.csv", fixture_rows)
    summary = {
        "status": "RESEARCH_ONLY_TEAM_FORM_AND_FIXTURE_CONTEXT_UNCERTAINTY_AUDIT",
        "source_artifact_generated_utc": generated or "NOT_RECORDED",
        "source_artifact_age_hours_at_analysis": age_hours,
        "locked_h2h_paired_holdout_loaded": False, "provider_api_calls": 0,
        "production_model_logic_changed": False, "production_probabilities_changed": False,
        "fixture_rows": len(fixtures),
        "raw_research_prediction_rows": sum(r.get("prediction_status") == "RAW_RESEARCH_ONLY" for r in fixtures),
        "blocked_missing_required_feature_rows": sum(r.get("prediction_status") == "BLOCKED_MISSING_REQUIRED_FEATURES" for r in fixtures),
        "team_role_profiles": len(team_rows),
        "unique_team_league_identities": len({(r["country"], r["league"], r["team"]) for r in team_rows}),
        "team_form_sequence_length_distribution": dict(sorted(Counter(str(r["form_n_observed"]) for r in team_rows).items())),
        "fixture_quality_flag_counts": dict(flag_counts),
        "fixtures_with_h2h_btts_rate": sum(bool(r.get("h2h_btts_rate_last5") not in ("", None)) for r in fixtures),
        "fixtures_without_h2h_btts_rate": sum(not bool(r.get("h2h_btts_rate_last5") not in ("", None)) for r in fixtures),
        "team_performance_dna_status": "BLOCKED_NO_TEAM_ATTRIBUTED_OUT_OF_SAMPLE_PREDICTIONS_AND_VERIFIED_SETTLEMENT_LABELS",
        "limitations": [
            "Recent W/D/L sequences are context only, not historical model performance or a betting edge.",
            "Wilson intervals for recent form are broad at n<=5; do not rank teams from these intervals.",
            "H2H BTTS intervals use explicit last-five-meeting sequence length and are approximate context intervals, not calibrated model uncertainty.",
            "Canonical fixture/team joins, official settlement truth, and odds/xG provenance are unverified in the current fixture report.",
            "Current market probabilities are raw and uncalibrated.",
            "Locked H2H paired holdout was not loaded or used for team ranking."
        ]
    }
    (args.output_dir / "oracle_selected50_team_form_uncertainty_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
