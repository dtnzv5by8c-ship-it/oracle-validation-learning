#!/usr/bin/env python3
"""Fail-closed validation of the Selected-50 research runtime outputs.

This validates report integrity and governance invariants only. It does not
change model logic, probabilities, calibration, thresholds, or release status.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

OUT = Path("selected50_runtime_output")
MARKETS = {"BTTS", "DC_HOME", "DC_AWAY", "COMBO_HOME", "COMBO_AWAY"}
FOLDS = [
    "WF1_2025-03-20_to_2025-09-20",
    "WF2_2025-09-20_to_2026-03-20",
    "WF3_2026-03-20_to_2026-09-20",
]


def load_json(name: str):
    path = OUT / name
    if not path.is_file():
        raise AssertionError(f"Missing required runtime output: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(name: str):
    path = OUT / name
    if not path.is_file():
        raise AssertionError(f"Missing required runtime output: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def number(row, key, *, low=None, high=None, allow_none=False):
    value = row.get(key)
    if value is None and allow_none:
        return None
    if value in ("", None):
        raise AssertionError(f"{key} missing")
    result = float(value)
    if not math.isfinite(result):
        raise AssertionError(f"{key} is not finite: {value}")
    if low is not None and result < low:
        raise AssertionError(f"{key} below {low}: {result}")
    if high is not None and result > high:
        raise AssertionError(f"{key} above {high}: {result}")
    return result


def main():
    wf = load_json("oracle_selected50_walk_forward_metrics.json")
    feature_qa = load_json("oracle_selected50_feature_qa.json")
    governed_qa = load_json("oracle_selected50_governed_fixture_report_qa.json")
    prediction_report = load_csv("oracle_selected50_prediction_report.csv")
    governed = load_csv("oracle_selected50_governed_fixture_report.csv")
    readiness = load_csv("oracle_selected50_league_market_readiness.csv")
    league_folds = load_csv("oracle_selected50_league_walk_forward_metrics.csv")
    schedule = load_csv("oracle_selected50_schedule_coverage.csv")
    calendar = load_csv("oracle_selected50_calendar_year_coverage.csv")
    season_year = load_csv("oracle_selected50_provider_season_year_coverage.csv")
    settlement = load_csv("oracle_selected50_settlement_truth_qa.csv")

    folds = wf.get("folds", [])
    assert len(folds) == 15, f"Expected 15 market/fold rows, got {len(folds)}"
    assert {r.get("market") for r in folds} == MARKETS
    assert wf.get("fold_design", "").startswith("Expanding-window rolling-origin")
    assert "no calibration or tuning" in wf.get("fold_design", "").lower()

    for market in sorted(MARKETS):
        rows = [r for r in folds if r["market"] == market]
        assert [r.get("fold") for r in rows] == FOLDS, (market, [r.get("fold") for r in rows])
        train_sizes = []
        for row in rows:
            assert row.get("status") == "RAW_WALK_FORWARD_NOT_CALIBRATED"
            train_sizes.append(int(row["train_n"]))
            assert int(row["train_n"]) > 0 and int(row["test_n"]) > 0
            acc = number(row, "accuracy_at_0_5", low=0, high=1)
            ci_low = number(row, "accuracy_95ci_low", low=0, high=1)
            ci_high = number(row, "accuracy_95ci_high", low=0, high=1)
            assert ci_low <= acc <= ci_high, (market, row["fold"], ci_low, acc, ci_high)
            brier = number(row, "brier", low=0, high=1)
            base = number(row, "baseline_brier", low=0)
            skill = number(row, "brier_skill_vs_prevalence")
            assert abs(skill - (1 - brier / base)) <= 0.0002, (market, row["fold"], skill, brier, base)
            number(row, "log_loss", low=0)
            number(row, "ece_10_bins", low=0, high=1)
            number(row, "training_prevalence", low=0, high=1)
            number(row, "auc", low=0, high=1, allow_none=True)
        assert train_sizes == sorted(train_sizes), (market, train_sizes)

    assert len(readiness) == 250, f"Expected 250 league-market rows, got {len(readiness)}"
    assert len({(r.get("selected_id"), r.get("market")) for r in readiness}) == 250
    assert {r.get("market") for r in readiness} == MARKETS
    assert len(league_folds) == 750, f"Expected 750 league/fold rows, got {len(league_folds)}"
    assert len({(r.get("selected_id"), r.get("market"), r.get("fold")) for r in league_folds}) == 750
    assert len({r.get("selected_id") for r in readiness}) == 50
    assert all(r.get("production_eligible") == "NO" for r in readiness + league_folds)
    assert all(r.get("edge_claim") == "NOT_APPROVED" for r in readiness)

    assert len(schedule) == 50
    assert len(settlement) == 50
    assert len(calendar) == 250
    assert len(season_year) == 200
    assert len(governed) == int(feature_qa["governed_fixture_report_rows"])
    assert len(prediction_report) == len(governed)
    assert len({r.get("fixture_id") for r in governed}) == len(governed)
    assert len({r.get("fixture_id") for r in prediction_report}) == len(prediction_report)
    # Combo probabilities must be masked in every uploaded prediction CSV, not just
    # the separately governed report, until market semantics and identity gates pass.
    assert all(r.get("COMBO_HOME_probability_pct", "") == "" and r.get("COMBO_AWAY_probability_pct", "") == "" for r in prediction_report)
    assert all(r.get("combo_probability_status") == "BLOCKED_SETTLEMENT_SPEC_MISMATCH" for r in prediction_report)
    # Blank confidence/risk percentages must carry explicit non-calculation reasons.
    assert all(r.get("confidence_score_pct", "") == "" for r in governed)
    assert all(r.get("data_risk_pct", "") == "" for r in governed)
    assert all(r.get("confidence_score_status") == "NOT_CALCULATED_UNCALIBRATED_MODEL" for r in governed)
    assert all(r.get("data_risk_status") == "NOT_QUANTIFIED_NO_VALIDATED_RISK_MAPPING" for r in governed)
    assert governed_qa.get("all_rows_production_ineligible") is True
    assert governed_qa.get("all_combo_probabilities_blocked") is True
    assert governed_qa.get("all_combo_probabilities_masked_in_prediction_report") is True
    assert int(governed_qa.get("combo_home_probabilities_remaining", -1)) == 0
    assert int(governed_qa.get("combo_away_probabilities_remaining", -1)) == 0
    assert feature_qa.get("production_model_logic_changed") is False
    assert feature_qa.get("production_probabilities_changed") is False
    assert feature_qa.get("production_readiness") == "NOT_GRANTED"
    assert feature_qa.get("provider_parent_competition_ids_verified") == 0
    assert feature_qa.get("provider_parent_competition_ids_unavailable") == 50
    assert feature_qa.get("provider_competition_id_field_matches_selected_id_in_match_probe") == 50
    assert feature_qa.get("provider_competition_id_match_probe_status") == "MATCH_RECORD_COMPETITION_ID_DOCUMENTED_AS_SEASON_ID_50_OF_50_PARENT_ID_NOT_PROVIDED"
    assert feature_qa.get("provider_competition_id_match_probe_rows") == 50
    assert feature_qa.get("provider_competition_id_field_semantics_documented_as_season_id") is True
    assert "league-matches competition_id as the league season ID" in feature_qa.get("provider_competition_id_field_semantics_source", "")
    assert "match-schedule-and-stats" in feature_qa.get("provider_competition_id_field_semantics_source_urls", "")
    assert feature_qa.get("provider_competition_id_parent_semantics_verified") is False
    assert feature_qa.get("provider_match_coverage_matrix_status") == "PASS_PROVIDER_MATCH_COVERAGE_CONTRACT_50_OF_50"
    assert feature_qa.get("provider_match_coverage_audit_run") == "40391540391"
    assert feature_qa.get("provider_match_coverage_leagues") == 50
    assert feature_qa.get("provider_match_coverage_first_page_total_rows") == 14051
    assert feature_qa.get("provider_match_coverage_unique_fixture_ids_total") == 14051
    assert feature_qa.get("provider_match_coverage_duplicate_fixture_id_rows_total") == 0
    assert feature_qa.get("provider_match_coverage_truncated_leagues") == 0
    assert feature_qa.get("provider_match_coverage_rows_with_status_total") == 14051
    assert feature_qa.get("provider_match_coverage_rows_with_both_team_ids_total") == 14051
    assert feature_qa.get("provider_match_coverage_rows_with_both_score_fields_total") == 14051
    assert feature_qa.get("provider_match_coverage_rows_with_unix_kickoff_total") == 14051
    assert feature_qa.get("provider_match_coverage_status_counts_json") == '{"complete": 7040, "incomplete": 6958, "suspended": 53}'
    assert feature_qa.get("provider_match_coverage_groups_matching_selected_id") == 50
    assert feature_qa.get("provider_explicit_season_id_field_nonempty_rows") == 0
    assert feature_qa.get("provider_to_canonical_bridges_verified") == 0
    assert feature_qa.get("provider_sample_fixture_ids_observed") == 50
    assert feature_qa.get("provider_sample_home_away_team_id_pairs_observed") == 50
    assert feature_qa.get("provider_sample_scores_are_settlement_truth") is False

    result = {
        "status": "PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT",
        "production_eligible": False,
        "betting_eligible": False,
        "market_fold_rows": len(folds),
        "league_market_rows": len(readiness),
        "league_market_fold_rows": len(league_folds),
        "selected_groups": len({r.get("selected_id") for r in readiness}),
        "governed_fixture_rows": len(governed),
        "combo_home_probabilities_remaining": governed_qa["combo_home_probabilities_remaining"],
        "combo_away_probabilities_remaining": governed_qa["combo_away_probabilities_remaining"],
        "limitations": [
            "Contract validation does not verify canonical provider IDs, official settlement truth, or point-in-time provenance.",
            "Walk-forward scores are raw and uncalibrated; no odds/ROI benchmark is approved without verified odds provenance.",
            "Combo remains blocked pending canonical fixture/team joins and official settlement truth; research target now matches the documented <=4-goal composite rule.",
        ],
    }
    (OUT / "oracle_selected50_runtime_validation.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
