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

    def test_home_combo_matches_documented_settlement(self):
        for home, away in [(0,0),(1,0),(1,1),(2,1),(2,2),(4,0),(3,2)]:
            expected = int(home >= away and home + away <= 4)
            actual = self.settle("COMPOSITE", "HOME_1X_U45", home, away) == "WIN"
            self.assertEqual(actual, bool(expected), (home, away))
            self.assertEqual(runtime.MARKETS["COMBO_HOME"](home, away), expected)

    def test_away_combo_matches_documented_settlement(self):
        for home, away in [(0,0),(0,1),(1,1),(1,2),(2,2),(0,4),(2,3)]:
            expected = int(away >= home and home + away <= 4)
            actual = self.settle("COMPOSITE", "AWAY_X2_U45", home, away) == "WIN"
            self.assertEqual(actual, bool(expected), (home, away))
            self.assertEqual(runtime.MARKETS["COMBO_AWAY"](home, away), expected)

    def test_five_total_goals_fails_both_combos(self):
        self.assertEqual(runtime.MARKETS["COMBO_HOME"](3, 2), 0)
        self.assertEqual(runtime.MARKETS["COMBO_AWAY"](2, 3), 0)
        self.assertEqual(self.settle("COMPOSITE", "HOME_1X_U45", 3, 2), "LOSS")
        self.assertEqual(self.settle("COMPOSITE", "AWAY_X2_U45", 2, 3), "LOSS")

if __name__ == "__main__":
    unittest.main()
