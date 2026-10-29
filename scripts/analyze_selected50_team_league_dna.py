#!/usr/bin/env python3
"""Research-only coverage and league/team context analytics for Oracle Selected-50 artifacts.

This script intentionally does NOT use the locked primary H2H paired holdout to rank
teams or markets. The current artifact does not contain fixture-level, team-attributed
walk-forward predictions; therefore team performance DNA and team exclusion flags are
not inferred from holdout outcomes. Outputs are diagnostics only, never betting advice.
"""
from __future__ import annotations
import argparse, csv, json, math
from collections import Counter
from pathlib import Path

VALID_MARKETS = {"BTTS", "DC_HOME", "DC_AWAY"}
POSITIVE_STATUS = "POSITIVE_BRIER_SKILL_ALL_FOLDS_DIAGNOSTIC_ONLY"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows, fieldnames=None):
    rows = list(rows)
    if fieldnames is None:
        fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def form_counts(seq):
    seq = (seq or "").strip().upper()
    return {"form_sequence": seq,
            "form_wins": seq.count("W"),
            "form_draws": seq.count("D"),
            "form_losses": seq.count("L"),
            "form_symbols": sum(seq.count(c) for c in "WDL")}


def build_team_context(fixtures):
    # Keep the latest as-of fixture context per team and role, while separately
    # counting appearances so repeated fixtures do not distort the form sample.
    latest = {}
    appearances = Counter()
    for r in fixtures:
        for side in ("home", "away"):
            team = (r.get(f"{side}_team") or "").strip()
            if not team:
                continue
            key = (r.get("country", ""), r.get("league", ""), team, side)
            appearances[key] += 1
            row = {
                "country": r.get("country", ""), "league": r.get("league", ""),
                "team": team, "role": side,
                "latest_fixture_kickoff_utc": r.get("date_utc", ""),
                "upcoming_fixture_appearances": 0,
                "recent_form_n": int(float(r.get(f"{side}_recent5_n") or 0)),
                **form_counts(r.get(f"{side}_recent5_results", "")),
                "context_status": "UPCOMING_FIXTURE_FORM_CONTEXT_ONLY_NOT_TEAM_PERFORMANCE_DNA",
            }
            if key not in latest or row["latest_fixture_kickoff_utc"] > latest[key]["latest_fixture_kickoff_utc"]:
                latest[key] = row
    out = []
    for key, row in latest.items():
        row["upcoming_fixture_appearances"] = appearances[key]
        n = row["recent_form_n"]
        row["recent_form_completeness_pct"] = round(100 * min(n, 5) / 5, 2)
        row["wins_pct_of_observed_form"] = round(100 * row["form_wins"] / n, 2) if n else ""
        row["draws_pct_of_observed_form"] = round(100 * row["form_draws"] / n, 2) if n else ""
        row["losses_pct_of_observed_form"] = round(100 * row["form_losses"] / n, 2) if n else ""
        out.append(row)
    return sorted(out, key=lambda x: (x["country"], x["league"], x["team"], x["role"]))


def build_league_screen(readiness):
    # Exclude composite markets because their authoritative settlement definition is unresolved.
    out = []
    for r in readiness:
        market = r.get("market", "")
        if market not in VALID_MARKETS:
            continue
        folds = int(float(r.get("walk_forward_folds_with_test_data") or 0))
        ntrain = int(float(r.get("train_n") or 0))
        ntest = int(float(r.get("test_n") or 0))
        sample_folds = int(float(r.get("folds_meeting_min_100_train_and_test") or 0))
        positive_folds = int(float(r.get("folds_positive_brier_skill_vs_league_prevalence") or 0))
        status = r.get("fold_stability_status", "")
        if status == POSITIVE_STATUS and folds == 3 and sample_folds == 3 and positive_folds == 3:
            disposition = "CANDIDATE_FOR_SEPARATE_VALIDATION_ONLY"
        elif "INSUFFICIENT" in status or sample_folds < 3 or folds < 3:
            disposition = "INSUFFICIENT_EVIDENCE"
        else:
            disposition = "MIXED_OR_NONPOSITIVE_DIAGNOSTIC"
        out.append({
            "country": r.get("country", ""), "league": r.get("league", ""), "market": market,
            "train_n_reported": ntrain, "test_n_reported": ntest,
            "walk_forward_folds_with_test_data": folds,
            "folds_meeting_min_100_train_and_test": sample_folds,
            "folds_positive_brier_skill_vs_league_prevalence": positive_folds,
            "fold_brier_skill_min": r.get("fold_brier_skill_min", ""),
            "fold_brier_skill_max": r.get("fold_brier_skill_max", ""),
            "fold_stability_status": status,
            "research_disposition": disposition,
            "production_eligible": "NO", "betting_eligibility": "NOT_ASSESSED",
            "note": "Raw pooled-model league-subset diagnostic; not calibrated, not an odds/ROI edge, and not approval."
        })
    return sorted(out, key=lambda x: (x["market"], x["research_disposition"], x["country"], x["league"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True, type=Path, help="Directory extracted from the research runtime artifact")
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    d = args.input_dir
    readiness = read_csv(d / "oracle_selected50_league_market_readiness.csv")
    fixtures = read_csv(d / "oracle_selected50_prediction_report.csv")
    schedule = read_csv(d / "oracle_selected50_schedule_coverage.csv")
    feature_qa = json.loads((d / "oracle_selected50_feature_qa.json").read_text(encoding="utf-8"))
    validation = json.loads((d / "oracle_selected50_runtime_validation.json").read_text(encoding="utf-8"))
    team_rows = build_team_context(fixtures)
    league_rows = build_league_screen(readiness)
    write_csv(args.output_dir / "oracle_selected50_team_fixture_context_dna.csv", team_rows)
    write_csv(args.output_dir / "oracle_selected50_league_market_dna_screen.csv", league_rows)

    status_counts = Counter(r.get("prediction_status", "") for r in fixtures)
    fixture_leagues = len({(r.get("country", ""), r.get("league", "")) for r in fixtures})
    team_league_keys = {(r["country"], r["league"], r["team"]) for r in team_rows}
    role_coverage = Counter(r["role"] for r in team_rows)
    form_n = Counter(int(r["recent_form_n"]) for r in team_rows)
    screen_summary = {}
    for market in sorted(VALID_MARKETS):
        rr = [r for r in league_rows if r["market"] == market]
        screen_summary[market] = {
            "league_market_rows": len(rr),
            "positive_brier_skill_all_three_folds_and_sample_gate": sum(r["research_disposition"] == "CANDIDATE_FOR_SEPARATE_VALIDATION_ONLY" for r in rr),
            "insufficient_evidence": sum(r["research_disposition"] == "INSUFFICIENT_EVIDENCE" for r in rr),
            "mixed_or_nonpositive": sum(r["research_disposition"] == "MIXED_OR_NONPOSITIVE_DIAGNOSTIC" for r in rr),
        }
    summary = {
        "status": "RESEARCH_ONLY_TEAM_LEAGUE_ANALYTICS_COMPLETE_WITH_TEAM_PERFORMANCE_DNA_BLOCKED",
        "source_artifact_runtime_generated_utc": "2026-10-29T17:09:30Z",
        "selected_leagues": feature_qa.get("selected_leagues"),
        "selected_groups_with_match_rows": feature_qa.get("selected_groups_with_match_rows"),
        "historical_archive_rows": feature_qa.get("raw_match_records_retained_after_dedup"),
        "explicitly_finished_with_numeric_scores": feature_qa.get("completed_match_records"),
        "upcoming_fixtures_in_report_horizon": len(fixtures),
        "upcoming_fixture_leagues": fixture_leagues,
        "prediction_status_counts": dict(status_counts),
        "unique_team_league_role_profiles": len(team_rows),
        "unique_team_league_identities_in_fixture_context": len(team_league_keys),
        "team_role_profile_counts": dict(role_coverage),
        "recent_form_n_distribution": dict(sorted(form_n.items())),
        "league_market_screen": screen_summary,
        "schedule_coverage_groups": len(schedule),
        "schedule_groups_with_fixture_in_7d": sum(int(r.get("upcoming_fixture_count_7d") or 0) > 0 for r in schedule),
        "canonical_fixture_joins_verified": sum(1 for r in fixtures if r.get("canonical_fixture_join_status") == "VERIFIED"),
        "canonical_team_joins_verified": sum(1 for r in fixtures if r.get("canonical_team_join_status") == "VERIFIED"),
        "settlement_truth_verified": sum(1 for r in fixtures if r.get("settlement_truth_status") == "VERIFIED"),
        "odds_xg_provenance_verified": sum(1 for r in fixtures if r.get("odds_xg_provenance_status") == "VERIFIED"),
        "team_level_walk_forward_prediction_artifact_available": False,
        "locked_primary_h2h_holdout_used_for_team_ranking": False,
        "team_performance_dna_status": "BLOCKED_NO_TEAM_ATTRIBUTED_OUT_OF_SAMPLE_PREDICTIONS_AND_VERIFIED_SETTLEMENT_LABELS",
        "combo_markets_in_league_screen": False,
        "production_eligible": validation.get("production_eligible", False),
        "betting_eligible": validation.get("betting_eligible", False),
        "limitations": [
            "Upcoming fixture form context is not historical model-performance DNA and is not a team-market suitability score.",
            "No team-attributed walk-forward prediction artifact is present; do not rank teams by locked primary holdout outcomes.",
            "Canonical fixture/team joins and official settlement truth are unverified for the current fixture report.",
            "All market probabilities are raw and uncalibrated; odds/xG provenance is unverified.",
            "Composite markets are excluded because the authoritative settlement definition remains unresolved.",
            "League Brier-skill screens are research triage only, not proof of profitability or permission to bet."
        ]
    }
    (args.output_dir / "oracle_selected50_team_league_dna_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
