import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "config" / "oracle_50_league_runtime_migration_contract_v1.json"
MANIFEST_PATH = ROOT / "data" / "oracle-footystats-selected-50-season-id-manifest.csv"

class Selected50RuntimeMigrationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.manifest_text = MANIFEST_PATH.read_text(encoding="utf-8-sig")

    def test_runtime_is_separate_and_historical_baseline_is_frozen(self):
        c = self.contract
        self.assertEqual(c["runtime_isolation"]["target_namespace"], "selected50_runtime_v1")
        self.assertEqual(c["runtime_isolation"]["legacy_namespace"], "legacy_27_league_runtime")
        baseline = c["runtime_isolation"]["historical_baseline"]
        self.assertEqual(baseline, {"league_count": 27, "fixture_count": 12836, "immutable": True})
        self.assertTrue(c["runtime_isolation"]["separate_50_league_artifacts_required"])
        self.assertFalse(c["runtime_isolation"]["overwrite_legacy_manifests_or_historical_ledgers"])

    def test_probability_and_model_invariants_are_locked(self):
        m = self.contract["model_invariants"]
        self.assertFalse(m["production_model_logic_may_change"])
        self.assertFalse(m["production_probabilities_may_change"])
        self.assertFalse(m["calibration_may_change"])
        self.assertFalse(m["thresholds_may_change"])
        self.assertEqual(m["parity_tolerance_absolute"], 0.0)
        self.assertTrue(m["any_unexplained_probability_difference_blocks_release"])

    def test_selected_manifest_is_the_single_source_of_governed_seasons(self):
        c = self.contract
        self.assertEqual(c["governed_universe"]["source_manifest"], "data/oracle-footystats-selected-50-season-id-manifest.csv")
        self.assertEqual(c["governed_universe"]["required_season_count"], 50)
        self.assertEqual(c["governed_universe"]["identity_key"], ["season_id"])
        self.assertFalse(c["governed_universe"]["infer_parent_or_competition_ids"])
        self.assertFalse(c["governed_universe"]["fuzzy_identity_join_allowed_for_approval"])
        self.assertIn("selected_id", self.manifest_text)

    def test_data_and_production_gates_fail_closed(self):
        c = self.contract
        self.assertEqual(c["status"], "RESEARCH_ONLY_NOT_PRODUCTION_AUTHORIZATION")
        self.assertEqual(c["governance"]["production_eligibility_until_all_gates_pass"], "NO")
        self.assertFalse(c["data_admission"]["paid_provider_requests_authorized"])
        self.assertEqual(c["market_readiness_defaults"]["BTTS Yes"], "NOT_VERIFIED")
        self.assertEqual(c["market_readiness_defaults"]["M-1UP"], "BLOCKED")
        self.assertFalse(c["data_admission"]["fuzzy_identity_join_allowed_for_approval"] if "fuzzy_identity_join_allowed_for_approval" in c["data_admission"] else c["governed_universe"]["fuzzy_identity_join_allowed_for_approval"])

    def test_contract_cannot_claim_historical_fixture_count_as_selected50(self):
        self.assertEqual(self.contract["runtime_isolation"]["historical_baseline"]["fixture_count"], 12836)
        self.assertNotIn('"historical_fixture_count"', self.contract)

if __name__ == "__main__":
    unittest.main()
