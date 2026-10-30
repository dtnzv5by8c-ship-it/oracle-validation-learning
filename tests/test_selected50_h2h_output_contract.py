import unittest

from scripts.validate_selected50_runtime_outputs import (MARKETS, binary_auc, binary_probability_metrics,
    exact_mcnemar_two_sided_p, validate_h2h_comparison_outputs)


FOLD_STARTS = {
    "H2H_WF1_2024H1": ("2024-01-01T00:00:00+00:00", "2024-07-01T00:00:00+00:00"),
    "H2H_WF2_2024H2": ("2024-07-01T00:00:00+00:00", "2025-01-01T00:00:00+00:00"),
    "H2H_WF3_2025H1": ("2025-01-01T00:00:00+00:00", "2025-07-01T00:00:00+00:00"),
    "H2H_WF4_2025H2": ("2025-07-01T00:00:00+00:00", "2026-01-01T00:00:00+00:00"),
    "H2H_WF5_2026H1": ("2026-01-01T00:00:00+00:00", "2026-07-01T00:00:00+00:00"),
}


def valid_inputs():
    market_rows = []
    paired_rows = []
    expanding_rows = []
    for market in sorted(MARKETS):
        market_rows.append({
            "market": market,
            "paired_test_n": 2,
            "baseline_test_n": 10,
            "h2h_available_test_n": 8,
            "h2h_test_coverage_pct": 80.0,
            "baseline_train_n": 300,
            "candidate_train_n": 300,
            "baseline_accuracy_at_0_5": 1.0,
            "candidate_accuracy_at_0_5": 1.0,
            "baseline_brier": 0.16,
            "candidate_brier": 0.1521,
            "baseline_log_loss": 0.51083,
            "candidate_log_loss": 0.49430,
            "baseline_auc": 1.0,
            "candidate_auc": 1.0,
            "production_eligible": "NO",
            "betting_eligible": "NO",
            "status": "PAIRED_RESEARCH_ONLY_NOT_CALIBRATED",
        })
        paired_rows.extend([
            {
                "competition_id": "C1", "fixture_id": "F1",
                "market": market,
                "actual": "1",
                "baseline_probability": "0.60",
                "h2h_candidate_probability": "0.61",
                "baseline_correct": "1",
                "h2h_candidate_correct": "1",
            },
            {
                "competition_id": "C1", "fixture_id": "F2",
                "market": market,
                "actual": "0",
                "baseline_probability": "0.40",
                "h2h_candidate_probability": "0.39",
                "baseline_correct": "1",
                "h2h_candidate_correct": "1",
            },
        ])
        for fold, (start, end) in FOLD_STARTS.items():
            expanding_rows.append({
                "market": market,
                "fold": fold,
                "training_cutoff_exclusive_utc": start,
                "test_start_utc": start,
                "test_end_exclusive_utc": end,
                "baseline_train_n": 300,
                "candidate_train_n": 300,
                "paired_test_n": 1,
                "test_n_h2h_available": 1,
                "production_eligible": "NO",
                "betting_eligible": "NO",
                "status": "EXPANDING_WINDOW_RESEARCH_ONLY_NOT_CALIBRATED",
            })
    chronology = {
        "status": "PASS_H2H_PAIRED_OUTPUT_CHRONOLOGY",
        "row_count": len(paired_rows),
        "unique_fixture_count": 2,
        "duplicate_fixture_market_rows": 0,
        "non_strict_prior_rows": 0,
        "days_since_last_mismatch_rows": 0,
        "production_eligible": False,
        "betting_eligible": False,
    }
    metrics = {"status": "RESEARCH_ONLY_ABLATION_NOT_CALIBRATED", "markets": market_rows}
    expanding = {"folds": expanding_rows}
    return metrics, expanding, paired_rows, chronology


class Selected50H2HOutputContractTests(unittest.TestCase):
    def test_valid_paired_comparison_and_expanding_folds_pass(self):
        inputs = valid_inputs()
        result = validate_h2h_comparison_outputs(*inputs)
        self.assertEqual(result["status"], "PASS_H2H_COMPARISON_AND_CHRONOLOGY_CONTRACT")
        self.assertEqual(result["paired_prediction_rows"], 10)
        self.assertTrue(all(x["status"] == "PASS_PAIRED_METRICS_RECONCILED"
                            for x in result["paired_metric_reconciliation"].values()))
        self.assertFalse(result["betting_eligible"])

    def test_baseline_and_candidate_must_use_same_training_rows(self):
        inputs = list(valid_inputs())
        inputs[0]["markets"][0]["candidate_train_n"] = 299
        with self.assertRaises(AssertionError):
            validate_h2h_comparison_outputs(*inputs)

    def test_blocked_chronology_cannot_pass_runtime_contract(self):
        inputs = list(valid_inputs())
        inputs[3]["status"] = "BLOCKED_H2H_PAIRED_OUTPUT_INTEGRITY"
        with self.assertRaises(AssertionError):
            validate_h2h_comparison_outputs(*inputs)

    def test_duplicate_fixture_market_row_is_rejected(self):
        inputs = list(valid_inputs())
        inputs[2].append(dict(inputs[2][0]))
        inputs[3]["row_count"] += 1
        with self.assertRaises(AssertionError):
            validate_h2h_comparison_outputs(*inputs)



    def test_same_fixture_id_in_different_competitions_is_not_a_duplicate(self):
        inputs = list(valid_inputs())
        cross_competition_rows = []
        for row in inputs[2]:
            if row["fixture_id"] == "F1":
                copied = dict(row)
                copied["competition_id"] = "C2"
                cross_competition_rows.append(copied)
        inputs[2].extend(cross_competition_rows)
        inputs[3]["row_count"] = len(inputs[2])
        inputs[3]["unique_fixture_count"] = 3

        for metric_row in inputs[0]["markets"]:
            market = metric_row["market"]
            market_rows = [row for row in inputs[2] if row["market"] == market]
            labels = [int(row["actual"]) for row in market_rows]
            metric_row["paired_test_n"] = len(market_rows)
            for prefix, probability_key in (
                ("baseline", "baseline_probability"),
                ("candidate", "h2h_candidate_probability"),
            ):
                calculated = binary_probability_metrics(
                    labels, [float(row[probability_key]) for row in market_rows]
                )
                metric_row[f"{prefix}_accuracy_at_0_5"] = calculated["accuracy_at_0_5"]
                metric_row[f"{prefix}_brier"] = calculated["brier"]
                metric_row[f"{prefix}_log_loss"] = calculated["log_loss"]
                metric_row[f"{prefix}_auc"] = calculated["auc"]

        result = validate_h2h_comparison_outputs(*inputs)
        self.assertEqual(result["paired_prediction_rows"], 15)
        self.assertEqual(result["paired_fixture_count"], 3)

    def test_correctness_flags_must_reconcile_to_probabilities(self):
        inputs = list(valid_inputs())
        inputs[2][0]["baseline_correct"] = "0"
        with self.assertRaises(AssertionError):
            validate_h2h_comparison_outputs(*inputs)

    def test_exact_mcnemar_p_value_known_counts(self):
        self.assertAlmostEqual(exact_mcnemar_two_sided_p(4, 1), 0.375, places=12)
        self.assertAlmostEqual(exact_mcnemar_two_sided_p(68, 49), 0.0956727150, places=9)
        self.assertEqual(exact_mcnemar_two_sided_p(0, 0), 1.0)
        with self.assertRaises(ValueError):
            exact_mcnemar_two_sided_p(-1, 2)

    def test_paired_discordance_summary_reconciles_and_is_unadjusted(self):
        inputs = list(valid_inputs())
        for row in inputs[0]["markets"]:
            row["paired_test_n"] = 7
        paired = []
        for market in sorted(MARKETS):
            for index in range(4):
                paired.append({
                    "competition_id": "C1", "fixture_id": f"C{index}", "market": market, "actual": "1",
                    "baseline_probability": "0.40", "h2h_candidate_probability": "0.60",
                    "baseline_correct": "0", "h2h_candidate_correct": "1",
                })
            paired.extend([
                {
                    "competition_id": "C1", "fixture_id": "B", "market": market, "actual": "1",
                    "baseline_probability": "0.60", "h2h_candidate_probability": "0.40",
                    "baseline_correct": "1", "h2h_candidate_correct": "0",
                },
                {
                    "competition_id": "C1", "fixture_id": "BC", "market": market, "actual": "0",
                    "baseline_probability": "0.40", "h2h_candidate_probability": "0.39",
                    "baseline_correct": "1", "h2h_candidate_correct": "1",
                },
                {
                    "competition_id": "C1", "fixture_id": "BW", "market": market, "actual": "0",
                    "baseline_probability": "0.60", "h2h_candidate_probability": "0.61",
                    "baseline_correct": "0", "h2h_candidate_correct": "0",
                },
            ])
        inputs[2] = paired
        inputs[3]["row_count"] = 35
        inputs[3]["unique_fixture_count"] = 7
        for row in inputs[0]["markets"]:
            rs = [x for x in paired if x["market"] == row["market"]]
            labels = [int(x["actual"]) for x in rs]
            for prefix, probability_key in (("baseline", "baseline_probability"),
                                            ("candidate", "h2h_candidate_probability")):
                probabilities = [float(x[probability_key]) for x in rs]
                row[f"{prefix}_accuracy_at_0_5"] = sum(
                    (p >= 0.5) == bool(y) for y, p in zip(labels, probabilities)
                ) / len(labels)
                row[f"{prefix}_brier"] = sum((p-y)**2 for y,p in zip(labels,probabilities)) / len(labels)
                import math
                row[f"{prefix}_log_loss"] = -sum(
                    y*math.log(p)+(1-y)*math.log(1-p) for y,p in zip(labels,probabilities)
                ) / len(labels)
                row[f"{prefix}_auc"] = binary_auc(labels, probabilities)
        result = validate_h2h_comparison_outputs(*inputs)
        for market in MARKETS:
            comparison = result["paired_correctness_comparison"][market]
            self.assertEqual(comparison["candidate_only_correct"], 4)
            self.assertEqual(comparison["baseline_only_correct"], 1)
            self.assertEqual(comparison["discordant_pairs"], 5)
            self.assertEqual(comparison["exact_mcnemar_p_two_sided"], 0.375)
            self.assertIn("UNADJUSTED", comparison["test"])
        self.assertIn("not a probability-quality", result["paired_correctness_interpretation"])

    def test_published_paired_metrics_must_reconcile_to_csv(self):
        inputs = list(valid_inputs())
        inputs[0]["markets"][0]["baseline_brier"] = 0.25
        with self.assertRaises(AssertionError):
            validate_h2h_comparison_outputs(*inputs)

if __name__ == "__main__":
    unittest.main()
