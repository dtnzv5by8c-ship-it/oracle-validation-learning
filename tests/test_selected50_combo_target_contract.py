import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runtime = load_module("selected50_runtime", "scripts/build_selected50_research_runtime.py")
settlement = load_module("settlement_rules", "scripts/settle_market_from_final_score.py")


class ComboMarketContractTests(unittest.TestCase):
    def settle(self, market, selection, home, away):
        prediction = {
            "fixture_id": "f1", "competition_id": "c1",
            "scheduled_kickoff_utc": "2026-10-01T12:00:00Z",
            "home_team_id": "h1", "away_team_id": "a1",
            "market": market, "selection": selection
        }
        result = {
            "fixture_id": "f1", "competition_id": "c1",
            "scheduled_kickoff_utc": "2026-10-01T12:00:00Z",
            "home_team_id": "h1", "away_team_id": "a1",
            "home_score": home, "away_score": away,
            "match_status": "FINISHED", "result_source": "unit-test"
        }
        return settlement.settle(prediction, result)["outcome"]

    def test_home_combo_preserves_existing_two_to_four_goal_predictor_target(self):
        # Preserve the pre-existing research/predictor definition. Do not silently
        # broaden it to all totals below five to make it match the ledger helper.
        for home in range(6):
            for away in range(6):
                expected = int(home >= away and 2 <= home + away <= 4)
                self.assertEqual(runtime.MARKETS["COMBO_HOME"](home, away), expected, (home, away))
        # The settlement helper currently treats 0-0 and 1-0 as wins; predictor
        # target treats them as losses. Keep this disagreement explicit.
        for home, away in [(0, 0), (1, 0)]:
            predictor = runtime.MARKETS["COMBO_HOME"](home, away) == 1
            ledger = self.settle("COMPOSITE", "HOME_1X_U45", home, away) == "WIN"
            self.assertNotEqual(predictor, ledger, (home, away))

    def test_away_combo_preserves_existing_two_to_four_goal_predictor_target(self):
        for home in range(6):
            for away in range(6):
                expected = int(away >= home and 2 <= home + away <= 4)
                self.assertEqual(runtime.MARKETS["COMBO_AWAY"](home, away), expected, (home, away))
        for home, away in [(0, 0), (0, 1)]:
            predictor = runtime.MARKETS["COMBO_AWAY"](home, away) == 1
            ledger = self.settle("COMPOSITE", "AWAY_X2_U45", home, away) == "WIN"
            self.assertNotEqual(predictor, ledger, (home, away))

    def test_five_total_goals_fails_both_combos(self):
        self.assertEqual(runtime.MARKETS["COMBO_HOME"](3, 2), 0)
        self.assertEqual(runtime.MARKETS["COMBO_AWAY"](2, 3), 0)
        self.assertEqual(self.settle("COMPOSITE", "HOME_1X_U45", 3, 2), "LOSS")
        self.assertEqual(self.settle("COMPOSITE", "AWAY_X2_U45", 2, 3), "LOSS")

    def test_runtime_disagreement_diagnostic_counts_only_exact_completed_scoreline_mismatches(self):
        expected = {
            (0, 0): (True, True),
            (1, 0): (True, False),
            (0, 1): (False, True),
            (1, 1): (False, False),
            (2, 0): (False, False),
            (3, 2): (False, False),
            (0, 5): (False, False),
        }
        for score, flags in expected.items():
            self.assertEqual(runtime.combo_predictor_vs_ledger_disagreements(*score), flags, score)
        # Invalid or non-integer scores are not settled truth and must be ignored.
        self.assertIsNone(runtime.combo_predictor_vs_ledger_disagreements(1.5, 0))
        self.assertIsNone(runtime.combo_predictor_vs_ledger_disagreements(-1, 0))
        self.assertIsNone(runtime.combo_predictor_vs_ledger_disagreements(None, 0))

    def test_combo_probabilities_are_masked_in_export_copy(self):
        source = [{
            "fixture_id": "f1",
            "COMBO_HOME_probability_pct": 72.5,
            "COMBO_AWAY_probability_pct": 41.2,
            "BTTS_probability_pct": 54.0,
        }]
        exported = runtime.mask_combo_probabilities_for_export(source)
        self.assertEqual(source[0]["COMBO_HOME_probability_pct"], 72.5)
        self.assertEqual(source[0]["COMBO_AWAY_probability_pct"], 41.2)
        self.assertIsNone(exported[0]["COMBO_HOME_probability_pct"])
        self.assertIsNone(exported[0]["COMBO_AWAY_probability_pct"])
        self.assertEqual(exported[0]["combo_probability_status"], "BLOCKED_SETTLEMENT_SPEC_MISMATCH")
        self.assertEqual(exported[0]["BTTS_probability_pct"], 54.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
