import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "oracle_selected50_compatibility_contract_v1.json"
MANIFEST_PATH = ROOT / "data" / "oracle-footystats-selected-50-season-id-manifest.csv"

class Selected50CompatibilityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        with MANIFEST_PATH.open(encoding="utf-8-sig", newline="") as handle:
            cls.manifest = list(csv.DictReader(handle))

    def test_contract_has_exactly_50_unique_season_ids(self):
        seasons = self.contract["league_seasons"]
        ids = [str(row["season_id"]) for row in seasons]
        self.assertEqual(self.contract["expected_season_count"], 50)
        self.assertEqual(len(seasons), 50)
        self.assertEqual(len(set(ids)), 50)

    def test_contract_ids_and_labels_match_selected_manifest(self):
        expected = {
            (int(row["selected_id"]), row["country"], row["competition_name"])
            for row in self.manifest
        }
        actual = {
            (row["season_id"], row["country"], row["competition_name"])
            for row in self.contract["league_seasons"]
        }
        self.assertEqual(len(expected), 50)
        self.assertEqual(actual, expected)

    def test_contract_is_research_only_and_production_safe(self):
        self.assertEqual(
            self.contract["status"],
            "RESEARCH_ONLY_NOT_PRODUCTION_AUTHORIZATION",
        )
        governance = self.contract["governance"]
        self.assertFalse(governance["production_model_logic_may_change"])
        self.assertFalse(governance["production_probabilities_may_change"])
        self.assertFalse(governance["calibration_or_thresholds_may_change"])
        self.assertFalse(governance["paid_provider_requests_authorized"])
        self.assertTrue(governance["historical_baselines_are_immutable"])

    def test_market_gates_fail_closed(self):
        gates = self.contract["market_readiness_defaults"]
        self.assertEqual(gates["BTTS Yes"], "NOT_VERIFIED")
        self.assertEqual(gates["Double Chance"], "NOT_VERIFIED")
        self.assertEqual(gates["Double Chance + Under 4.5"], "NOT_VERIFIED")
        self.assertEqual(gates["M-1UP"], "BLOCKED")
        self.assertEqual(
            self.contract["hard_gates"]["production_eligibility_until_governed_approval"],
            "NO",
        )

    def test_no_parent_competition_ids_are_inferred(self):
        for season in self.contract["league_seasons"]:
            self.assertNotIn("parent_competition_id", season)
            self.assertNotIn("league_id", season)

if __name__ == "__main__":
    unittest.main()
