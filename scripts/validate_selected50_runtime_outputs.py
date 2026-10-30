#!/usr/bin/env python3
"""Fail-closed validation of the Selected-50 research runtime outputs.

This validates report integrity and governance invariants only. It does not
change model logic, probabilities, calibration, thresholds, or release status.
"""
from __future__ import annotations

import csv
import json
import math
from collections import Counter
from fractions import Fraction
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


def exact_mcnemar_two_sided_p(candidate_only_correct: int, baseline_only_correct: int) -> float:
    """Exact two-sided McNemar/binomial p-value for paired 0.5-threshold correctness."""
    if candidate_only_correct < 0 or baseline_only_correct < 0:
        raise ValueError("discordant counts must be non-negative")
    discordant = candidate_only_correct + baseline_only_correct
    if discordant == 0:
        return 1.0
    tail_count = min(candidate_only_correct, baseline_only_correct)
    tail = sum(math.comb(discordant, i) for i in range(tail_count + 1))
    return min(1.0, float(Fraction(2 * tail, 2 ** discordant)))


def binary_auc(labels: list[int], probabilities: list[float]) -> float | None:
    """Rank-based binary AUC with average ranks for ties; None if one class is absent."""
    positives = sum(labels)
    negatives = len(labels) - positives
    if positives == 0 or negatives == 0:
        return None
    ordered = sorted(zip(probabilities, labels), key=lambda item: item[0])
    positive_rank_sum = 0.0
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][0] == ordered[index][0]:
            end += 1
        average_rank = ((index + 1) + end) / 2.0
        positive_rank_sum += average_rank * sum(label for _, label in ordered[index:end])
        index = end
    return (positive_rank_sum - positives * (positives + 1) / 2.0) / (positives * negatives)


def binary_probability_metrics(labels: list[int], probabilities: list[float]) -> dict[str, float | None]:
    """Recompute fixed-threshold accuracy, Brier, log loss and AUC from paired rows."""
    if not labels or len(labels) != len(probabilities):
        raise ValueError("labels and probabilities must be non-empty and equal length")
    clipped = [max(1e-15, min(1.0 - 1e-15, p)) for p in probabilities]
    return {
        "accuracy_at_0_5": sum((p >= 0.5) == bool(y) for y, p in zip(labels, probabilities)) / len(labels),
        "brier": sum((p - y) ** 2 for y, p in zip(labels, probabilities)) / len(labels),
        "log_loss": -sum(y * math.log(p) + (1 - y) * math.log(1 - p)
                         for y, p in zip(labels, clipped)) / len(labels),
        "auc": binary_auc(labels, probabilities),
    }



def validate_h2h_comparison_outputs(metrics, expanding, paired_rows, chronology_qa):
    """Fail closed on paired H2H evidence, chronology, fold and governance contracts."""
    assert metrics.get("status") == "RESEARCH_ONLY_ABLATION_NOT_CALIBRATED"
    market_rows = metrics.get("markets", [])
    assert len(market_rows) == len(MARKETS)
    assert {row.get("market") for row in market_rows} == MARKETS
    assert len({row.get("market") for row in market_rows}) == len(MARKETS)

    paired_counts = Counter()
    correctness_counts = {market: Counter() for market in MARKETS}
    paired_values = {market: {"actual": [], "baseline": [], "candidate": []} for market in MARKETS}
    seen_pairs = set()
    for row in paired_rows:
        fixture_id = str(row.get("fixture_id") or "").strip()
        market = str(row.get("market") or "").strip()
        assert fixture_id and market in MARKETS
        key = (fixture_id, market)
        assert key not in seen_pairs, f"Duplicate H2H fixture/market row: {key}"
        seen_pairs.add(key)
        paired_counts[market] += 1
        assert str(row.get("actual")) in {"0", "1"}
        actual = int(row["actual"])
        baseline_probability = number(row, "baseline_probability", low=0, high=1)
        candidate_probability = number(row, "h2h_candidate_probability", low=0, high=1)
        try:
            baseline_correct = int(row.get("baseline_correct"))
            candidate_correct = int(row.get("h2h_candidate_correct"))
        except (TypeError, ValueError, OverflowError):
            raise AssertionError("paired correctness flags must be integer 0/1 values") from None
        assert baseline_correct in {0, 1} and candidate_correct in {0, 1}
        expected_baseline_correct = int((baseline_probability >= 0.5) == bool(actual))
        expected_candidate_correct = int((candidate_probability >= 0.5) == bool(actual))
        paired_values[market]["actual"].append(actual)
        paired_values[market]["baseline"].append(baseline_probability)
        paired_values[market]["candidate"].append(candidate_probability)
        assert baseline_correct == expected_baseline_correct, "baseline_correct does not reconcile to actual/probability"
        assert candidate_correct == expected_candidate_correct, "h2h_candidate_correct does not reconcile to actual/probability"
        if baseline_correct and candidate_correct:
            correctness_counts[market]["both_correct"] += 1
        elif not baseline_correct and not candidate_correct:
            correctness_counts[market]["both_wrong"] += 1
        elif candidate_correct:
            correctness_counts[market]["candidate_only_correct"] += 1
        else:
            correctness_counts[market]["baseline_only_correct"] += 1

    for row in market_rows:
        market = row["market"]
        paired_n = int(row.get("paired_test_n") or 0)
        baseline_test_n = int(row.get("baseline_test_n") or 0)
        h2h_available_n = int(row.get("h2h_available_test_n") or 0)
        assert paired_n == paired_counts[market], (market, paired_n, paired_counts[market])
        assert 0 < paired_n <= h2h_available_n <= baseline_test_n
        assert int(row.get("baseline_train_n") or 0) == int(row.get("candidate_train_n") or 0)
        expected_coverage = 100 * h2h_available_n / baseline_test_n
        assert abs(float(row.get("h2h_test_coverage_pct")) - expected_coverage) <= 0.02
        assert row.get("production_eligible") == "NO"
        assert row.get("betting_eligible") == "NO"
        assert row.get("status") == "PAIRED_RESEARCH_ONLY_NOT_CALIBRATED"
        values = paired_values[market]
        baseline_metrics = binary_probability_metrics(values["actual"], values["baseline"])
        candidate_metrics = binary_probability_metrics(values["actual"], values["candidate"])
        metric_pairs = (
            ("baseline_accuracy_at_0_5", baseline_metrics["accuracy_at_0_5"]),
            ("candidate_accuracy_at_0_5", candidate_metrics["accuracy_at_0_5"]),
            ("baseline_brier", baseline_metrics["brier"]),
            ("candidate_brier", candidate_metrics["brier"]),
            ("baseline_log_loss", baseline_metrics["log_loss"]),
            ("candidate_log_loss", candidate_metrics["log_loss"]),
        )
        for field, expected_value in metric_pairs:
            published = number(row, field, low=0)
            assert abs(published - expected_value) <= 0.000011, (
                market, field, published, expected_value
            )
        for field, expected_value in (
            ("baseline_auc", baseline_metrics["auc"]),
            ("candidate_auc", candidate_metrics["auc"]),
        ):
            published = row.get(field)
            if expected_value is None:
                assert published in (None, ""), (market, field, published)
            else:
                published_value = number(row, field, low=0, high=1)
                assert abs(published_value - expected_value) <= 0.000011, (
                    market, field, published_value, expected_value
                )

    paired_metric_reconciliation = {}
    for market in sorted(MARKETS):
        values = paired_values[market]
        base_metrics = binary_probability_metrics(values["actual"], values["baseline"])
        candidate_metrics = binary_probability_metrics(values["actual"], values["candidate"])
        paired_metric_reconciliation[market] = {
            "status": "PASS_PAIRED_METRICS_RECONCILED",
            "paired_n": paired_counts[market],
            "baseline": base_metrics,
            "candidate": candidate_metrics,
            "rounding_tolerance": 0.000011,
        }

    paired_correctness_comparison = {}
    for market in sorted(MARKETS):
        counts = correctness_counts[market]
        candidate_only = counts["candidate_only_correct"]
        baseline_only = counts["baseline_only_correct"]
        paired_n = paired_counts[market]
        assert sum(counts.values()) == paired_n, (market, counts, paired_n)
        discordant = candidate_only + baseline_only
        paired_correctness_comparison[market] = {
            "paired_n": paired_n,
            "both_correct": counts["both_correct"],
            "both_wrong": counts["both_wrong"],
            "candidate_only_correct": candidate_only,
            "baseline_only_correct": baseline_only,
            "discordant_pairs": discordant,
            "exact_mcnemar_p_two_sided": round(exact_mcnemar_two_sided_p(candidate_only, baseline_only), 10),
            "test": "EXACT_TWO_SIDED_MCNEMAR_AT_FIXED_0_5_THRESHOLD_UNADJUSTED",
        }

    folds = expanding.get("folds", [])
    expected_fold_names = {
        "H2H_WF1_2024H1", "H2H_WF2_2024H2", "H2H_WF3_2025H1",
        "H2H_WF4_2025H2", "H2H_WF5_2026H1",
    }
    assert len(folds) == len(MARKETS) * len(expected_fold_names)
    assert {row.get("market") for row in folds} == MARKETS
    assert {row.get("fold") for row in folds} == expected_fold_names
    assert len({(row.get("market"), row.get("fold")) for row in folds}) == len(folds)
    for row in folds:
        assert row.get("training_cutoff_exclusive_utc") == row.get("test_start_utc")
        assert row.get("test_start_utc") < row.get("test_end_exclusive_utc")
        assert int(row.get("baseline_train_n") or 0) == int(row.get("candidate_train_n") or 0)
        assert 0 <= int(row.get("paired_test_n") or 0) <= int(row.get("test_n_h2h_available") or 0)
        assert row.get("production_eligible") == "NO"
        assert row.get("betting_eligible") == "NO"
        assert row.get("status") in {
            "EXPANDING_WINDOW_RESEARCH_ONLY_NOT_CALIBRATED",
            "INSUFFICIENT_PAIRED_TEST_PREDICTIONS",
        }

    assert chronology_qa.get("status") == "PASS_H2H_PAIRED_OUTPUT_CHRONOLOGY"
    assert int(chronology_qa.get("row_count") or 0) == len(paired_rows)
    assert int(chronology_qa.get("duplicate_fixture_market_rows") or 0) == 0
    assert int(chronology_qa.get("non_strict_prior_rows") or 0) == 0
    assert int(chronology_qa.get("days_since_last_mismatch_rows") or 0) == 0
    assert chronology_qa.get("production_eligible") is False
    assert chronology_qa.get("betting_eligible") is False
    return {
        "status": "PASS_H2H_COMPARISON_AND_CHRONOLOGY_CONTRACT",
        "paired_prediction_rows": len(paired_rows),
        "paired_fixture_count": int(chronology_qa.get("unique_fixture_count") or 0),
        "market_count": len(market_rows),
        "expanding_window_rows": len(folds),
        "paired_metric_reconciliation": paired_metric_reconciliation,
        "paired_metric_interpretation": "Accuracy, Brier, log loss and AUC independently recomputed from paired CSV rows and reconciled to published metrics.",
        "paired_correctness_comparison": paired_correctness_comparison,
        "paired_correctness_interpretation": "Unadjusted exact paired test of 0.5-threshold correctness only; not a probability-quality, calibration, ROI, or betting-edge test.",
        "production_eligible": False,
        "betting_eligible": False,
    }


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
    h2h_metrics = load_json("oracle_selected50_h2h_ablation_metrics.json")
    h2h_expanding = load_json("oracle_selected50_h2h_expanding_window_metrics.json")
    h2h_paired = load_csv("oracle_selected50_h2h_paired_predictions.csv")
    h2h_chronology = load_json("oracle_selected50_h2h_paired_chronology_qa.json")
    h2h_contract = validate_h2h_comparison_outputs(h2h_metrics, h2h_expanding, h2h_paired, h2h_chronology)

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
    # The settlement audit must calculate, not hard-code, predictor/ledger
    # disagreements. Only explicit finished integer-score rows are eligible.
    home_disagreements = sum(int(r.get("combo_home_predictor_vs_ledger_disagreement_rows") or 0) for r in settlement)
    away_disagreements = sum(int(r.get("combo_away_predictor_vs_ledger_disagreement_rows") or 0) for r in settlement)
    assert feature_qa.get("combo_home_predictor_vs_ledger_disagreement_rows") == home_disagreements
    assert feature_qa.get("combo_away_predictor_vs_ledger_disagreement_rows") == away_disagreements
    assert home_disagreements > 0, "Expected observed home Combo target/settlement disagreements were not counted"
    assert away_disagreements > 0, "Expected observed away Combo target/settlement disagreements were not counted"
    assert all(r.get("settlement_truth_status") == "INTERNAL_STATUS_SCORE_QA_ONLY_OFFICIAL_SETTLEMENT_UNVERIFIED" for r in settlement)
    assert len(calendar) == 250
    assert len(season_year) == 200
    assert len(governed) == int(feature_qa["governed_fixture_report_rows"])
    assert len(prediction_report) == len(governed)
    assert len({r.get("fixture_id") for r in governed}) == len(governed)
    assert len({r.get("fixture_id") for r in prediction_report}) == len(prediction_report)

    # Every fixture row must expose evidence-backed feature and model-training gate
    # diagnostics; a generic "feature/training gate" status alone is insufficient.
    required_support_fields = {
        "feature_support_status", "missing_required_features",
        "training_support_status", "unavailable_training_markets",
        "training_eligible_rows_by_market", "prediction_block_reason",
    }
    assert required_support_fields.issubset(set(prediction_report[0])), (
        "Prediction report is missing support-diagnostic columns",
        required_support_fields - set(prediction_report[0]),
    )
    assert required_support_fields.issubset(set(governed[0]))
    allowed_block_reasons = {
        "RESEARCH_PREDICTION_AVAILABLE",
        "BLOCKED_MISSING_REQUIRED_FEATURES",
        "BLOCKED_MODEL_TRAINING_GATE",
        "BLOCKED_MISSING_FEATURES_AND_TRAINING_GATE",
    }
    for pred, gov in zip(prediction_report, governed):
        missing = [x for x in pred.get("missing_required_features", "").split(";") if x]
        unavailable = [x for x in pred.get("unavailable_training_markets", "").split(";") if x]
        coverage = number(pred, "model_input_coverage_pct", low=0, high=100)
        expected_missing = 20 - round(coverage * 20 / 100)
        assert len(missing) == expected_missing, (
            pred.get("fixture_id"), coverage, len(missing), expected_missing
        )
        assert pred["feature_support_status"] == (
            "PASS_ALL_20_REQUIRED_FEATURES" if not missing else "BLOCKED_MISSING_REQUIRED_FEATURES"
        )
        if not unavailable:
            assert pred["training_support_status"] == "PASS_ALL_MARKET_MODELS"
        elif len(unavailable) == len(MARKETS):
            assert pred["training_support_status"] == "BLOCKED_ALL_MARKET_MODELS_UNAVAILABLE"
        else:
            assert pred["training_support_status"] == "PARTIAL_MARKET_MODEL_TRAINING_GATE"
        assert pred["prediction_block_reason"] in allowed_block_reasons, (
            pred.get("fixture_id"), pred["prediction_block_reason"]
        )
        assert pred["prediction_block_reason"] == gov["prediction_block_reason"]
        expected_prediction_status = {
            "RESEARCH_PREDICTION_AVAILABLE": "RAW_RESEARCH_ONLY",
            "BLOCKED_MISSING_REQUIRED_FEATURES": "BLOCKED_MISSING_REQUIRED_FEATURES",
            "BLOCKED_MODEL_TRAINING_GATE": "BLOCKED_MODEL_TRAINING_GATE",
            "BLOCKED_MISSING_FEATURES_AND_TRAINING_GATE": "BLOCKED_MISSING_FEATURES_AND_TRAINING_GATE",
        }.get(pred["prediction_block_reason"], "BLOCKED_UNCLASSIFIED_NO_PREDICTION")
        assert pred["prediction_status"] == expected_prediction_status, (
            pred.get("fixture_id"), pred["prediction_status"], pred["prediction_block_reason"]
        )
        assert gov["prediction_status"] == expected_prediction_status
        if expected_prediction_status != "RAW_RESEARCH_ONLY":
            assert all(pred.get(m + "_probability_pct", "") == "" for m in MARKETS)
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
    combo_reason = str(governed_qa.get("combo_block_reason", ""))
    assert "between 2 and 4 inclusive" in combo_reason
    assert "total goals < 5" in combo_reason
    assert "unresolved" in combo_reason.lower()
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
        "feature_support_blocked_rows": sum(1 for r in prediction_report if r["feature_support_status"] != "PASS_ALL_20_REQUIRED_FEATURES"),
        "rows_with_any_unavailable_market_model": sum(1 for r in prediction_report if r["training_support_status"] != "PASS_ALL_MARKET_MODELS"),
        "rows_without_any_supported_prediction": sum(1 for r in prediction_report if r["prediction_status"] != "RAW_RESEARCH_ONLY"),
        "prediction_block_reason_counts": dict(sorted(Counter(r["prediction_block_reason"] for r in prediction_report).items())),
        "combo_home_probabilities_remaining": governed_qa["combo_home_probabilities_remaining"],
        "combo_away_probabilities_remaining": governed_qa["combo_away_probabilities_remaining"],
        "h2h_paired_output_contract": h2h_contract,
        "limitations": [
            "Contract validation does not verify canonical provider IDs, official settlement truth, or point-in-time provenance.",
            "Walk-forward scores are raw and uncalibrated; no odds/ROI benchmark is approved without verified odds provenance.",
            "Combo remains blocked because the documented predictor target is Double Chance AND 2-4 total goals, while the current settlement helper uses Double Chance AND total goals <5 (including 0-1 goals); the authoritative market definition remains unresolved.",
        ],
    }
    (OUT / "oracle_selected50_runtime_validation.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
