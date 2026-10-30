import unittest

from scripts.audit_selected50_global_market_fold_stability import analyze, RAW_STATUS, FOLDS


MARKETS = ["BTTS", "DC_HOME", "DC_AWAY", "COMBO_HOME", "COMBO_AWAY"]


def metadata():
    return {
        "snapshot_type": "SANITIZED_AGGREGATE_WALK_FORWARD_METRICS_ONLY_NO_RAW_PROVIDER_ROWS",
        "runtime_validation": {
            "selected_groups": 50,
            "market_fold_rows": 15,
            "production_eligible": False,
            "betting_eligible": False,
        },
        "governed_fixture_qa": {
            "all_combo_probabilities_blocked": True,
            "combo_home_probabilities_remaining": 0,
            "combo_away_probabilities_remaining": 0,
        },
    }


def rows():
    result = []
    for market_index, market in enumerate(MARKETS):
        for i, fold in enumerate(FOLDS):
            brier = 0.20 + market_index * 0.005 + i * 0.001
            baseline = 0.25
            result.append({
                "market": market,
                "fold": fold,
                "status": RAW_STATUS,
                "train_n": str([100, 150, 200][i]),
                "test_n": str([40, 50, 60][i]),
                "accuracy_at_0_5": "0.60",
                "brier": str(brier),
                "log_loss": "0.60",
                "ece_10_bins": "0.02",
                "training_prevalence": "0.50",
                "baseline_brier": str(baseline),
                "brier_skill_vs_prevalence": str(round(1 - brier / baseline, 5)),
            })
    return result


class GlobalMarketFoldStabilityTests(unittest.TestCase):
    def test_test_size_weighted_brier_and_sample_total(self):
        result = analyze(rows(), metadata())["per_market"]["BTTS"]
        expected = (0.20 * 40 + 0.201 * 50 + 0.202 * 60) / 150
        self.assertAlmostEqual(result["weighted_brier"], expected, places=6)
        self.assertEqual(result["test_n_across_disjoint_folds"], 150)
        self.assertEqual(result["positive_skill_folds"], 3)

    def test_combo_remains_blocked(self):
        result = analyze(rows(), metadata())["per_market"]["COMBO_HOME"]
        self.assertEqual(result["research_disposition"], "COMBO_BLOCKED_SEMANTIC_MISMATCH")
        self.assertFalse(result["betting_eligible"])

    def test_raw_probabilities_never_become_calibrated(self):
        result = analyze(rows(), metadata())
        for market in result["per_market"].values():
            self.assertTrue(market["probabilities_raw_uncalibrated"])
            self.assertFalse(market["calibration_approved"])
            self.assertFalse(market["production_eligible"])

    def test_rejects_missing_fold(self):
        with self.assertRaises(ValueError):
            analyze(rows()[:-1], metadata())

    def test_rejects_brier_skill_arithmetic_mismatch(self):
        source = rows()
        source[0]["brier_skill_vs_prevalence"] = "0.99"
        with self.assertRaises(ValueError):
            analyze(source, metadata())

    def test_rejects_fold_gap_or_overlap(self):
        source = rows()
        source[1]["fold"] = "WF2_2025-10-01_to_2026-03-20"
        with self.assertRaises(ValueError):
            analyze(source, metadata())

    def test_rejects_inconsistent_market_partitions(self):
        source = rows()
        row = next(r for r in source if r["market"] == "DC_HOME" and r["fold"] == FOLDS[1])
        row["test_n"] = "49"
        with self.assertRaises(ValueError):
            analyze(source, metadata())

    def test_rejects_missing_combo_block_evidence(self):
        meta = metadata()
        meta["governed_fixture_qa"]["all_combo_probabilities_blocked"] = False
        with self.assertRaises(ValueError):
            analyze(rows(), meta)

    def test_rejects_source_marked_production_eligible(self):
        meta = metadata()
        meta["runtime_validation"]["production_eligible"] = True
        with self.assertRaises(ValueError):
            analyze(rows(), meta)


if __name__ == "__main__":
    unittest.main()
