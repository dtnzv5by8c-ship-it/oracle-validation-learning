#!/usr/bin/env python3
"""Research-only Selected-50 fixture context discordance screen.

Reads only oracle_selected50_prediction_report.csv and optional runtime provenance
from an existing artifact. It never reads historical paired-prediction/holdout files,
never calls a provider, and never changes model or production outputs.

Flags are exploratory review heuristics, not calibrated risk scores, team rankings,
market edges, or betting recommendations.
"""
from __future__ import annotations
import argparse, csv, json, math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

DC_MARGIN_PP = 10.0
FORM_POINTS_MARGIN = 3
BTTS_H2H_GAP_PP = 30.0
MIN_H2H_CONTEXT_N = 3
LOW_GOALS_THRESHOLD = 1.8
HIGH_GOALS_THRESHOLD = 3.2


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


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


def form_stats(value):
    seq = clean_wdl(value)
    n = len(seq)
    wins, draws, losses = seq.count("W"), seq.count("D"), seq.count("L")
    points = 3 * wins + draws
    return {
        "sequence": seq, "n": n, "wins": wins, "draws": draws, "losses": losses,
        "points": points, "points_per_match": round(points / n, 4) if n else None,
    }


def parse_utc(value):
    if not value:
        return None
    try:
        d = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if d.tzinfo is None:
            return None
        return d.astimezone(timezone.utc)
    except (TypeError, ValueError, OverflowError):
        return None


def analyze(fixtures):
    required = {"fixture_id", "date_utc", "country", "league", "home_team", "away_team",
                "home_team_provider_id", "away_team_provider_id", "home_recent5_results",
                "away_recent5_results", "home_recent5_n", "away_recent5_n",
                "h2h_last5_results_home_perspective", "h2h_btts_rate_last5",
                "h2h_avg_total_goals_last5", "h2h_last_date_utc", "prediction_status",
                "BTTS_probability_pct", "DC_HOME_probability_pct", "DC_AWAY_probability_pct"}
    missing = sorted(required - set(fixtures[0].keys() if fixtures else []))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    ids = [r.get("fixture_id", "") for r in fixtures]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("Fixture IDs must be non-empty and unique")

    output, team_id_names, team_name_ids = [], defaultdict(set), defaultdict(set)
    flag_counts = Counter()
    h2h_n_dist = Counter()
    blocked_form_rows = 0
    home_under5 = away_under5 = both_under5 = 0
    h2h_rate_available = h2h_date_missing_with_rate = h2h_chronology_violations = 0
    raw_count = blocked_count = 0

    for r in fixtures:
        home = form_stats(r.get("home_recent5_results"))
        away = form_stats(r.get("away_recent5_results"))
        h2h_seq = clean_wdl(r.get("h2h_last5_results_home_perspective"))
        h2h_n = len(h2h_seq)
        h2h_n_dist[str(h2h_n)] += 1
        reported_home_n = as_int(r.get("home_recent5_n"))
        reported_away_n = as_int(r.get("away_recent5_n"))
        home_short = reported_home_n < 5
        away_short = reported_away_n < 5
        home_under5 += int(home_short)
        away_under5 += int(away_short)
        both_under5 += int(home_short and away_short)

        status = r.get("prediction_status", "")
        is_raw = status == "RAW_RESEARCH_ONLY"
        is_blocked = status == "BLOCKED_MISSING_REQUIRED_FEATURES"
        raw_count += int(is_raw)
        blocked_count += int(is_blocked)
        if is_blocked and (home_short or away_short):
            blocked_form_rows += 1

        btts = as_float(r.get("BTTS_probability_pct"))
        dc_home = as_float(r.get("DC_HOME_probability_pct"))
        dc_away = as_float(r.get("DC_AWAY_probability_pct"))
        dc_margin = dc_home - dc_away if dc_home is not None and dc_away is not None else None
        form_margin = home["points"] - away["points"] if home["n"] and away["n"] else None

        h2h_rate = as_float(r.get("h2h_btts_rate_last5"))
        if h2h_rate is not None:
            if 1 < h2h_rate <= 100:
                h2h_rate /= 100.0
            if not 0 <= h2h_rate <= 1:
                h2h_rate = None
        h2h_avg_goals = as_float(r.get("h2h_avg_total_goals_last5"))
        h2h_gap = btts - 100 * h2h_rate if btts is not None and h2h_rate is not None else None
        if h2h_rate is not None:
            h2h_rate_available += 1
            if not r.get("h2h_last_date_utc"):
                h2h_date_missing_with_rate += 1

        kickoff_dt = parse_utc(r.get("date_utc"))
        h2h_dt = parse_utc(r.get("h2h_last_date_utc"))
        chronology_violation = bool(kickoff_dt and h2h_dt and h2h_dt >= kickoff_dt)
        h2h_chronology_violations += int(chronology_violation)

        flags = []
        dc_disagreement = bool(is_raw and dc_margin is not None and form_margin is not None and
            ((dc_margin >= DC_MARGIN_PP and form_margin <= -FORM_POINTS_MARGIN) or
             (dc_margin <= -DC_MARGIN_PP and form_margin >= FORM_POINTS_MARGIN)))
        btts_gap_flag = bool(is_raw and h2h_n >= MIN_H2H_CONTEXT_N and h2h_gap is not None and
                             abs(h2h_gap) >= BTTS_H2H_GAP_PP)
        low_goal_flag = bool(h2h_n >= MIN_H2H_CONTEXT_N and h2h_avg_goals is not None and
                             h2h_avg_goals <= LOW_GOALS_THRESHOLD)
        high_goal_flag = bool(h2h_n >= MIN_H2H_CONTEXT_N and h2h_avg_goals is not None and
                              h2h_avg_goals >= HIGH_GOALS_THRESHOLD)
        if dc_disagreement: flags.append("DC_PREFERENCE_VS_RECENT_FORM_DISAGREEMENT")
        if btts_gap_flag: flags.append("BTTS_PROBABILITY_VS_H2H_RATE_GAP_GE_30PP")
        if low_goal_flag: flags.append("LOW_GOAL_H2H_CONTEXT")
        if high_goal_flag: flags.append("HIGH_GOAL_H2H_CONTEXT")
        if chronology_violation: flags.append("H2H_DATE_NOT_BEFORE_FIXTURE")
        if is_blocked: flags.append("PREDICTION_BLOCKED_MISSING_REQUIRED_FEATURES")
        if home_short: flags.append("HOME_RECENT5_SAMPLE_BELOW_5")
        if away_short: flags.append("AWAY_RECENT5_SAMPLE_BELOW_5")
        if r.get("canonical_fixture_join_status") != "VERIFIED": flags.append("CANONICAL_FIXTURE_JOIN_UNVERIFIED")
        if r.get("canonical_team_join_status") != "VERIFIED": flags.append("CANONICAL_TEAM_JOIN_UNVERIFIED")
        if r.get("settlement_truth_status") != "VERIFIED": flags.append("SETTLEMENT_TRUTH_UNVERIFIED")
        if r.get("calibration_status") != "CALIBRATED": flags.append("RAW_PROBABILITY_UNCALIBRATED")
        if r.get("odds_xg_provenance_status") != "VERIFIED": flags.append("ODDS_XG_PROVENANCE_UNVERIFIED")
        for f in flags:
            flag_counts[f] += 1

        for side in ("home", "away"):
            tid = str(r.get(f"{side}_team_provider_id") or "").strip()
            name = str(r.get(f"{side}_team") or "").strip()
            if tid and name:
                team_id_names[tid].add(name)
                team_name_ids[(r.get("country", ""), r.get("league", ""), name)].add(tid)

        output.append({
            "fixture_id": r.get("fixture_id", ""), "date_utc": r.get("date_utc", ""),
            "country": r.get("country", ""), "league": r.get("league", ""),
            "home_team": r.get("home_team", ""), "away_team": r.get("away_team", ""),
            "prediction_status": status,
            "BTTS_probability_pct": "" if btts is None else round(btts, 2),
            "DC_HOME_probability_pct": "" if dc_home is None else round(dc_home, 2),
            "DC_AWAY_probability_pct": "" if dc_away is None else round(dc_away, 2),
            "dc_home_minus_away_preference_pp": "" if dc_margin is None else round(dc_margin, 2),
            "home_recent5_results": home["sequence"], "home_recent5_n": reported_home_n,
            "home_recent5_points": home["points"], "away_recent5_results": away["sequence"],
            "away_recent5_n": reported_away_n, "away_recent5_points": away["points"],
            "home_minus_away_form_points": "" if form_margin is None else form_margin,
            "h2h_displayed_wdl_n_proxy": h2h_n, "h2h_prior_n_all": as_int(r.get("h2h_prior_n")),
            "h2h_btts_rate_last5_pct": "" if h2h_rate is None else round(100*h2h_rate, 2),
            "btts_probability_minus_h2h_rate_pp": "" if h2h_gap is None else round(h2h_gap, 2),
            "h2h_avg_total_goals_last5": "" if h2h_avg_goals is None else round(h2h_avg_goals, 2),
            "h2h_last_date_utc": r.get("h2h_last_date_utc", ""),
            "h2h_date_pre_kickoff_check": "VIOLATION" if chronology_violation else ("PASS" if h2h_dt and kickoff_dt else "NOT_CHECKABLE"),
            "dc_form_disagreement_flag": int(dc_disagreement),
            "btts_h2h_gap_flag": int(btts_gap_flag), "low_goal_h2h_context_flag": int(low_goal_flag),
            "high_goal_h2h_context_flag": int(high_goal_flag),
            "review_flags": "|".join(flags),
            "interpretation": "EXPLORATORY_CONTEXT_TRIAGE_ONLY_NOT_TEAM_PERFORMANCE_DNA_OR_BETTING_APPROVAL",
        })

    flag_names = ["dc_form_disagreement_flag", "btts_h2h_gap_flag", "low_goal_h2h_context_flag", "high_goal_h2h_context_flag"]
    flagged_union = sum(any(int(row[k]) for k in flag_names) for row in output)
    id_name_collisions = sum(len(names) > 1 for names in team_id_names.values())
    name_id_collisions = sum(len(ids) > 1 for ids in team_name_ids.values())
    summary = {
        "status": "RESEARCH_ONLY_FIXTURE_CONTEXT_DISCORDANCE_SCREEN_COMPLETE",
        "source_fixture_rows": len(fixtures),
        "raw_research_prediction_rows": raw_count,
        "blocked_missing_required_feature_rows": blocked_count,
        "fixture_rows_with_any_context_review_flag": flagged_union,
        "selected_league_groups_in_fixture_snapshot": len({(r.get("country"), r.get("league")) for r in fixtures}),
        "country_count": len({r.get("country") for r in fixtures}),
        "team_slots": 2 * len(fixtures),
        "unique_provider_team_ids": len(team_id_names),
        "provider_team_ids_with_multiple_names_in_snapshot": id_name_collisions,
        "competition_team_names_mapped_to_multiple_provider_ids_in_snapshot": name_id_collisions,
        "home_form_samples_below_5": home_under5,
        "away_form_samples_below_5": away_under5,
        "both_home_and_away_form_samples_below_5": both_under5,
        "blocked_rows_with_home_or_away_form_below_5": blocked_form_rows,
        "h2h_displayed_wdl_sample_length_distribution": dict(sorted(h2h_n_dist.items(), key=lambda x:int(x[0]))),
        "h2h_btts_rate_available_rows": h2h_rate_available,
        "h2h_rate_rows_missing_last_meeting_date": h2h_date_missing_with_rate,
        "h2h_date_at_or_after_fixture_violations": h2h_chronology_violations,
        "context_flag_counts_nonexclusive": {
            "dc_preference_vs_recent_form_disagreement": sum(int(r["dc_form_disagreement_flag"]) for r in output),
            "btts_probability_vs_h2h_rate_gap_ge_30pp": sum(int(r["btts_h2h_gap_flag"]) for r in output),
            "low_goal_h2h_context_le_1_8": sum(int(r["low_goal_h2h_context_flag"]) for r in output),
            "high_goal_h2h_context_ge_3_2": sum(int(r["high_goal_h2h_context_flag"]) for r in output),
        },
        "thresholds_are_exploratory_not_validated": {
            "dc_preference_margin_abs_min_pp": DC_MARGIN_PP,
            "opposing_recent_form_points_margin_min": FORM_POINTS_MARGIN,
            "btts_vs_h2h_gap_abs_min_pp": BTTS_H2H_GAP_PP,
            "minimum_displayed_h2h_wdl_length_proxy": MIN_H2H_CONTEXT_N,
            "low_goal_h2h_avg_total_goals_max": LOW_GOALS_THRESHOLD,
            "high_goal_h2h_avg_total_goals_min": HIGH_GOALS_THRESHOLD,
        },
        "critical_limitations": [
            "This artifact is a point-in-time research fixture context, not a fresh current fixture slate.",
            "DC_HOME and DC_AWAY both include the draw outcome; their difference is a relative selection preference, not a home-win versus away-win probability.",
            "H2H displayed WDL sequence length is only a proxy for the last-five H2H context sample; the exact denominator for the BTTS rate is not independently present in this report.",
            "Recent form and H2H context are descriptive inputs; flags are not outcome labels or evidence of team-specific predictive accuracy.",
            "Canonical fixture/team joins, official settlement truth and point-in-time feature provenance remain unverified.",
            "All probabilities are raw and uncalibrated; no odds/ROI analysis was performed.",
            "No team-attributed chronological out-of-sample prediction ledger is present; team performance DNA cannot be established.",
            "The locked H2H paired-prediction holdout was not read or used."
        ],
        "production_eligible": False,
        "betting_eligible": False,
    }
    return output, summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fixtures = read_csv(args.input_dir / "oracle_selected50_prediction_report.csv")
    rows, summary = analyze(fixtures)
    provenance_path = args.input_dir / "oracle_selected50_runtime_provenance.json"
    if provenance_path.exists():
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        summary["source_runtime_run_id"] = provenance.get("runtime_run_id")
        summary["source_runtime_run_number"] = provenance.get("runtime_run_number")
        summary["source_runtime_generated_utc"] = provenance.get("generated_utc")
        summary["source_snapshot_retrieved_utc"] = provenance.get("snapshot_retrieved_utc")
        summary["source_runtime_archive_sha256"] = provenance.get("selected_runtime_input_archive_sha256")
    out_csv = args.output_dir / "oracle_selected50_fixture_context_discordance_2026-10-30.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    review = [r for r in rows if any(int(r[k]) for k in ("dc_form_disagreement_flag", "btts_h2h_gap_flag", "low_goal_h2h_context_flag", "high_goal_h2h_context_flag"))]
    review_csv = args.output_dir / "oracle_selected50_fixture_context_review_queue_2026-10-30.csv"
    with review_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(review[0]) if review else list(rows[0]), extrasaction="ignore")
        w.writeheader()
        w.writerows(review)
    summary["fixture_context_csv"] = out_csv.name
    summary["review_queue_csv"] = review_csv.name
    (args.output_dir / "oracle_selected50_fixture_context_discordance_summary_2026-10-30.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
