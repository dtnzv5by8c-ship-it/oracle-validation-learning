import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "config" / "omi_market_intelligence_schema_v1.json"

class TestOmiMarketIntelligenceSchema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def test_user_approved_book4_baseline_is_exactly_95_columns_a_to_cq(self):
        s = self.schema
        self.assertEqual(s["sheet_name"], "Market Intelligence")
        self.assertEqual(s["baseline_column_count"], 95)
        self.assertEqual(s["baseline_columns"], "A:CQ")
        self.assertEqual(len(s["headers"]), 95)
        self.assertEqual(s["headers"][0:3], ["Fixture Date", "League", "Fixture"])
        self.assertEqual(s["headers"][-1], "retrieved_utc")

    def test_headers_are_nonblank_and_unique(self):
        headers = self.schema["headers"]
        self.assertTrue(all(isinstance(h, str) and h.strip() for h in headers))
        self.assertEqual(len(headers), len(set(headers)))

    def test_identity_and_temporal_evidence_fields_are_present(self):
        required = {
            "Fixture ID", "Provider Season ID", "Home Team ID", "Away Team ID",
            "History Cutoff UTC", "History Source Fixture IDs",
            "Schedule Reconciliation", "settlement_status", "retrieved_utc"
        }
        self.assertTrue(required.issubset(set(self.schema["headers"])))

    def test_research_and_betting_governance_fields_are_present(self):
        required = {"Production Eligible", "Betting Eligible", "Goal Research Status",
                    "Goal Research Block Reason", "Evidence / Schedule Gate"}
        self.assertTrue(required.issubset(set(self.schema["headers"])))

    def test_reserved_columns_and_append_only_extension_policy(self):
        policy = self.schema["extension_policy"]
        self.assertEqual(policy["reserved_columns"], ["CR", "CS"])
        self.assertEqual(policy["first_new_column"], "CT")
        self.assertTrue(policy["append_only"])
        self.assertTrue(policy["never_insert_before_or_within_baseline"])
        self.assertTrue(policy["never_rename_reorder_or_delete_baseline_headers"])

if __name__ == "__main__":
    unittest.main()
