import unittest

from scripts.validate_selected50_runtime_outputs import MARKETS, exact_mcnemar_two_sided_p, validate_h2h_comparison_outputs


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
            "paired_test_n": 1,
            "baseline_test_n": 10,
            "h2h_available_test_n": 8,
            "h2h_test_coverage_pct": 80.0,
            "baseline_train_n": 300,
            "candidate_train_n": 300,
            "baseline_accuracy_at_0_5": 0.60,
            "candidate_accuracy_at_0_5": 0.61,
            "baseline_brier": 0.24,
            "candidate_brier": 0.23,
            "baseline_log_loss": 1.2,
            "candidate_log_loss": 0.9,
            "baseline_auc": 0.60,
            "candidate_auc": 0.61,
            "production_eligible": "NO",
            "betting_eligible": "NO",
            "status": "PAIRED_RESEARCH_ONLY_NOT_CALIBRATED",
        })
        paired_rows.append({
            "fixture_id": "F1",
            "market": market,
            "actual": "1",
            "baseline_probability": "0.60",
            "h2h_candidate_probability": "0.61",
            "baseline_correct": "1",
            "h2h_candidate_correct": "1",
        })
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
        "unique_fixture_count": 1,
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
        self.assertEqual(result["paired_prediction_rows"], 5)
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
            row["paired_test_n"] = 5
        paired = []
        for market in sorted(MARKETS):
            for index in range(4):
                paired.append({
                    "fixture_id": f"C{index}", "market": market, "actual": "1",
                    "baseline_probability": "0.40", "h2h_candidate_probability": "0.60",
                    "baseline_correct": "0", "h2h_candidate_correct": "1",
                })
            paired.append({
                "fixture_id": "B", "market": market, "actual": "1",
                "baseline_probability": "0.60", "h2h_candidate_probability": "0.40",
                "baseline_correct": "1", "h2h_candidate_correct": "0",
            })
        inputs[2] = paired
        inputs[3]["row_count"] = 25
        inputs[3]["unique_fixture_count"] = 5
        result = validate_h2h_comparison_outputs(*inputs)
        for market in MARKETS:
            comparison = result["paired_correctness_comparison"][market]
            self.assertEqual(comparison["candidate_only_correct"], 4)
            self.assertEqual(comparison["baseline_only_correct"], 1)
            self.assertEqual(comparison["discordant_pairs"], 5)
            self.assertEqual(comparison["exact_mcnemar_p_two_sided"], 0.375)
            self.assertIn("UNADJUSTED", comparison["test"])
        self.assertIn("not a probability-quality", result["paired_correctness_interpretation"])

if __name__ == "__main__":
    unittest.main()
