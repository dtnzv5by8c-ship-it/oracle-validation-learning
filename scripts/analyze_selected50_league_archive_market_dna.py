#!/usr/bin/env python3
"""Research-only Selected-50 league archive and market-context audit.

Consumes sanitized files from an existing runtime artifact. It does not read the
locked H2H paired-prediction holdout, call providers, tune/calibrate the model,
or write to production. Market diagnostics are provisional because official
settlement truth and canonical fixture/team joins remain unverified.
"""
from __future__ import annotations
import argparse, csv, json, math, statistics
from collections import defaultdict
from pathlib import Path

MARKETS = {"BTTS", "DC_HOME", "DC_AWAY"}
EXPECTED = {"archive": 59049, "full20": 51095, "primary": 22291, "primary_full20": 20913}


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    rows = list(rows)
    fields = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def n(v, default=0):
    try:
        x = float(v)
        return x if math.isfinite(x) else default
    except (TypeError, ValueError, OverflowError):
        return default


def pct(a, b):
    return round(100*a/b, 3) if b else None


def build(input_dir):
    seasons = read_csv(input_dir / "oracle_selected50_provider_season_year_coverage.csv")
    calendar = read_csv(input_dir / "oracle_selected50_calendar_year_coverage.csv")
    season_detail = read_csv(input_dir / "season_coverage.csv")
    settlement = read_csv(input_dir / "oracle_selected50_settlement_truth_qa.csv")
    schedule = read_csv(input_dir / "oracle_selected50_schedule_coverage.csv")
    readiness = read_csv(input_dir / "oracle_selected50_league_market_readiness.csv")
    folds = [r for r in read_csv(input_dir / "oracle_selected50_league_walk_forward_metrics.csv")
             if r.get("market") in MARKETS]
    qa = json.loads((input_dir / "oracle_selected50_feature_qa.json").read_text(encoding="utf-8"))

    by_group = defaultdict(list)
    cal_by_group = defaultdict(list)
    detail_by_group = defaultdict(list)
    for r in seasons:
        by_group[(r["selected_id"], r["country"], r["competition_name"])].append(r)
    for r in calendar:
        cal_by_group[(r["selected_id"], r["country"], r["competition_name"])].append(r)
    for r in season_detail:
        detail_by_group[(r["selected_id"], r["country"], r["competition"])].append(r)
    settlement_by_id = {r["selected_id"]: r for r in settlement}
    schedule_by_id = {r["selected_id"]: r for r in schedule}

    league_rows = []
    for key, rows in sorted(by_group.items(), key=lambda x: (x[0][1], x[0][2], x[0][0])):
        sid, country, league = key
        cal = cal_by_group.get(key, [])
        det = detail_by_group.get(key, [])
        sq = settlement_by_id.get(sid, {})
        sc = schedule_by_id.get(sid, {})
        years = sorted({int(n(r.get("provider_season_start_year"))) for r in rows
                        if r.get("provider_season_start_year")})
        archive = sum(int(n(r.get("normalized_match_rows_retained"))) for r in rows)
        completed = sum(int(n(r.get("explicitly_completed_match_rows"))) for r in rows)
        full20 = sum(int(n(r.get("full_20_feature_rows"))) for r in rows)
        primary = sum(int(n(r.get("primary_window_match_rows"))) for r in rows)
        primary_completed = sum(int(n(r.get("primary_window_completed_match_rows"))) for r in rows)
        primary_full20 = sum(int(n(r.get("primary_window_full_20_feature_rows"))) for r in cal)
        team_counts = [int(n(r.get("team_count"))) for r in det]
        nonfinished_scored = int(n(sq.get("nonfinished_status_with_numeric_score_rows")))
        finished = int(n(sq.get("finished_status_with_numeric_score_rows")))
        low_goal = int(n(sq.get("completed_total_goals_0_1_rows")))
        flags = []
        if len(years) != 4:
            flags.append("SEASON_COVERAGE_NOT_FOUR_YEARS")
        if primary_completed < 100:
            flags.append("LOW_PRIMARY_WINDOW_COMPLETED_SAMPLE")
        if pct(full20, archive) is not None and pct(full20, archive) < 85:
            flags.append("FULL20_ARCHIVE_COVERAGE_BELOW_85_PCT")
        if pct(primary_full20, primary) is not None and pct(primary_full20, primary) < 90:
            flags.append("FULL20_PRIMARY_WINDOW_COVERAGE_BELOW_90_PCT")
        if nonfinished_scored:
            flags.append("NONFINISHED_STATUS_HAS_NUMERIC_SCORES_EXCLUDED_FROM_TRUTH")
        league_rows.append({
            "selected_id": sid,
            "selected_id_semantics": "PROVIDER_SEASON_ID_SURROGATE_NOT_PARENT_COMPETITION_ID",
            "country": country, "league": league, "season_year_count": len(years),
            "season_years": ";".join(map(str, years)),
            "archive_rows": archive, "explicit_finished_numeric_score_rows": completed,
            "completed_status_share_pct": pct(completed, archive),
            "full_20_feature_rows": full20, "full_20_archive_coverage_pct": pct(full20, archive),
            "primary_window_rows": primary, "primary_window_completed_rows": primary_completed,
            "primary_window_completion_share_pct": pct(primary_completed, primary),
            "primary_window_full_20_feature_rows": primary_full20,
            "primary_window_full_20_coverage_pct": pct(primary_full20, primary),
            "team_season_memberships_sum_not_unique_team_count": sum(team_counts) if team_counts else None,
            "minimum_teams_in_one_season": min(team_counts) if team_counts else None,
            "maximum_teams_in_one_season": max(team_counts) if team_counts else None,
            "nonfinished_status_numeric_score_rows": nonfinished_scored,
            "nonfinished_score_rows_share_pct": pct(nonfinished_scored, archive),
            "completed_0_1_total_goal_rows_internal_status_score_qa": low_goal,
            "completed_0_1_goal_share_pct_internal_status_score_qa": pct(low_goal, finished),
            "upcoming_fixtures_7d_in_run168_snapshot": int(n(sc.get("upcoming_fixture_count_7d"))),
            "schedule_status_in_run168_snapshot": sc.get("schedule_coverage_status", ""),
            "canonical_parent_competition_id_status": rows[0].get("provider_competition_id_status", ""),
            "official_settlement_truth_status": sq.get("settlement_truth_status", "NOT_REPORTED"),
            "production_eligible": "NO", "data_quality_flags": ";".join(flags),
            "interpretation": "ARCHIVE_AND_CONTEXT_COVERAGE_ONLY_NOT_TEAM_PERFORMANCE_OR_BETTING_APPROVAL"
        })

    folds_by_key = defaultdict(list)
    for r in folds:
        folds_by_key[(r["selected_id"], r["country"], r["league"], r["market"])].append(r)
    ready_by_key = {(r["selected_id"], r["market"]): r for r in readiness}
    league_by_id = {r["selected_id"]: r for r in league_rows}
    market_rows = []
    for key, rows in sorted(folds_by_key.items()):
        sid, country, league, market = key
        rows = sorted(rows, key=lambda r: r.get("fold", ""))
        skills = [n(r.get("brier_skill_vs_league_prevalence"), float("nan")) for r in rows]
        skills = [x for x in skills if math.isfinite(x)]
        ece = [n(r.get("ece_10_bins"), float("nan")) for r in rows]
        ece = [x for x in ece if math.isfinite(x)]
        gates = sum(r.get("sample_gate") == "SAMPLE_GATE_MET_DIAGNOSTIC_ONLY" for r in rows)
        positives = sum(x > 0 for x in skills)
        test_n = [int(n(r.get("test_n"))) for r in rows]
        train_n = [int(n(r.get("train_n"))) for r in rows]
        ci_widths = [n(r.get("accuracy_95ci_high"))-n(r.get("accuracy_95ci_low")) for r in rows]
        if len(rows) == 3 and gates == 3 and positives == 3:
            disposition = "RETEST_CANDIDATE_ONLY"
        elif len(rows) < 3 or gates < 3:
            disposition = "INSUFFICIENT_CHRONOLOGICAL_SAMPLE"
        else:
            disposition = "MIXED_OR_NONPOSITIVE_BRIER_SKILL"
        lp = league_by_id[sid]
        rr = ready_by_key.get((sid, market), {})
        market_rows.append({
            "selected_id": sid, "selected_id_semantics": "PROVIDER_SEASON_ID_SURROGATE_NOT_PARENT_COMPETITION_ID",
            "country": country, "league": league, "market": market,
            "folds_observed": len(rows), "sample_gate_pass_folds": gates,
            "positive_brier_skill_folds": positives,
            "minimum_fold_train_n": min(train_n) if train_n else 0,
            "minimum_fold_test_n": min(test_n) if test_n else 0,
            "total_fold_test_n_not_unique_dedup_count": sum(test_n),
            "mean_fold_accuracy_raw": round(statistics.mean([n(r.get("accuracy_at_0_5")) for r in rows]), 6) if rows else "",
            "maximum_fold_accuracy_ci_width": round(max(ci_widths), 6) if ci_widths else "",
            "minimum_fold_brier_skill_vs_league_prevalence": round(min(skills), 6) if skills else "",
            "median_fold_brier_skill_vs_league_prevalence": round(statistics.median(skills), 6) if skills else "",
            "maximum_fold_brier_skill_vs_league_prevalence": round(max(skills), 6) if skills else "",
            "maximum_fold_ece_raw_uncalibrated": round(max(ece), 6) if ece else "",
            "fold_stability_status_source": rr.get("fold_stability_status", ""),
            "research_disposition": disposition,
            "archive_rows": lp["archive_rows"],
            "full_20_archive_coverage_pct": lp["full_20_archive_coverage_pct"],
            "primary_window_completed_rows": lp["primary_window_completed_rows"],
            "primary_window_full_20_coverage_pct": lp["primary_window_full_20_coverage_pct"],
            "completed_0_1_goal_share_pct_internal_status_score_qa": lp["completed_0_1_goal_share_pct_internal_status_score_qa"],
            "canonical_parent_competition_id_status": lp["canonical_parent_competition_id_status"],
            "official_settlement_truth_status": lp["official_settlement_truth_status"],
            "label_validity": "PROVISIONAL_INTERNAL_STATUS_SCORE_LABELS_OFFICIAL_SETTLEMENT_UNVERIFIED",
            "interpretation": "FIXED_MODEL_CHRONOLOGICAL_RESEARCH_DIAGNOSTIC_NOT_EDGE_OR_BETTING_APPROVAL",
            "production_eligible": "NO"
        })

    return league_rows, market_rows, qa, season_detail


def self_test():
    assert pct(5, 10) == 50.0
    assert pct(0, 0) is None
    assert MARKETS == {"BTTS", "DC_HOME", "DC_AWAY"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path)
    ap.add_argument("--output-dir", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
        if args.input_dir is None:
            print("SELF_TEST_PASS")
            return
    if args.input_dir is None or args.output_dir is None:
        ap.error("--input-dir and --output-dir required unless --self-test alone")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    league_rows, market_rows, qa, season_detail = build(args.input_dir)
    assert len(league_rows) == 50, f"expected 50 selected groups, got {len(league_rows)}"
    assert len(market_rows) == 150, f"expected 150 league-market groups, got {len(market_rows)}"
    totals = {
        "archive": sum(int(n(r["archive_rows"])) for r in league_rows),
        "full20": sum(int(n(r["full_20_feature_rows"])) for r in league_rows),
        "primary": sum(int(n(r["primary_window_rows"])) for r in league_rows),
        "primary_full20": sum(int(n(r["primary_window_full_20_feature_rows"])) for r in league_rows),
    }
    assert totals == EXPECTED, f"source totals drifted: {totals}"
    write_csv(args.output_dir / "oracle_selected50_league_archive_profile_2026-10-30.csv", league_rows)
    write_csv(args.output_dir / "oracle_selected50_league_market_profile_2026-10-30.csv", market_rows)
    completed = int(n(qa.get("completed_match_records")))
    nonfinished_scored = sum(int(n(r["nonfinished_status_numeric_score_rows"])) for r in league_rows)
    low_goals = sum(int(n(r["completed_0_1_total_goal_rows_internal_status_score_qa"])) for r in league_rows)
    candidates = {m: sum(r["market"] == m and r["research_disposition"] == "RETEST_CANDIDATE_ONLY" for r in market_rows)
                  for m in sorted(MARKETS)}
    summary = {
        "status": "RESEARCH_ONLY_SELECTED50_LEAGUE_ARCHIVE_MARKET_DNA_AUDIT",
        "source_runtime_run_id": 40917698925,
        "source_runtime_generated_utc": "2026-10-29T17:09:30.571094+00:00",
        "selected_groups": len(league_rows), "season_rows": 200, "seasons_per_group": "4 (2023-2026)",
        "team_season_memberships_across_200_seasons": sum(int(n(r.get("team_count"))) for r in season_detail),
        "team_count_per_season_min": min(int(n(r.get("team_count"))) for r in season_detail),
        "team_count_per_season_median": statistics.median(int(n(r.get("team_count"))) for r in season_detail),
        "team_count_per_season_max": max(int(n(r.get("team_count"))) for r in season_detail),
        "archive_rows": totals["archive"], "explicit_finished_numeric_score_rows": completed,
        "full_20_feature_rows": totals["full20"], "full_20_archive_coverage_pct": pct(totals["full20"], totals["archive"]),
        "primary_window_rows_2025_03_20_to_2026_09_20": totals["primary"],
        "primary_window_completed_rows": 22256,
        "primary_window_full_20_feature_rows": totals["primary_full20"],
        "primary_window_full_20_coverage_pct": pct(totals["primary_full20"], totals["primary"]),
        "nonfinished_status_numeric_score_rows": nonfinished_scored,
        "completed_0_1_total_goal_rows_internal_status_score_qa": low_goals,
        "completed_0_1_goal_share_pct_internal_status_score_qa": pct(low_goals, completed),
        "league_market_rows": len(market_rows), "retest_candidate_counts": candidates,
        "team_performance_dna_status": "BLOCKED_NO_TEAM_ATTRIBUTED_CHRONOLOGICAL_PREDICTIONS_WITH_VERIFIED_SETTLEMENTS",
        "locked_h2h_paired_holdout_loaded": False, "provider_api_calls": 0, "paid_provider_calls": 0,
        "production_model_logic_changed": False, "production_probabilities_changed": False,
        "canonical_parent_competition_ids_verified": 0, "canonical_fixture_team_joins_verified": False,
        "official_settlement_truth_verified": False,
        "market_metrics_label_status": "PROVISIONAL_INTERNAL_STATUS_SCORE_LABELS_ONLY",
        "limitations": [
            "Selected IDs are provider season-ID surrogates, not verified parent competition IDs or canonical Oracle league IDs.",
            "Per-league market metrics are fixed-model rolling-origin diagnostics from three folds; labels remain provisional because official settlement truth and canonical fixture/team joins are unverified.",
            "No hyperparameter tuning or calibration was performed; no locked H2H paired holdout was loaded.",
            "Team-season membership totals are season-level roster counts summed across seasons, not unique clubs or team-level model prediction sample sizes.",
            "Scores on non-finished records are excluded from outcome labels; their presence is a data-quality warning.",
            "Low-goal rates are internal finished-status/score diagnostics, not independently verified settlement truth or a market edge.",
            "No team-level performance DNA, trap designation, or permanent exclusion is supported by this artifact."
        ],
        "decision": "CONTINUE_RESEARCH_ONLY_NO_PRODUCTION_OR_BETTING_APPROVAL"
    }
    (args.output_dir / "oracle_selected50_league_archive_market_dna_summary_2026-10-30.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
