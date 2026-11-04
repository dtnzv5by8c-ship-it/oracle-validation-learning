import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "config" / "omi_market_intelligence_schema_v1.json"

class TestOmiMarketIntelligenceSchema(unittest.TestCase):
    def test_user_reference_is_exactly_95_columns_a_to_cq(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["sheet_name"], "Market Intelligence")
        self.assertEqual(schema["baseline_column_count"], 95)
        self.assertEqual(schema["baseline_columns"], "A:CQ")
        self.assertEqual(len(schema["headers"]), 95)
        self.assertEqual(schema["headers"][0], "Fixture Date")
        self.assertEqual(schema["headers"][-1], "retrieved_utc")

    def test_extension_is_append_only_after_reserved_columns(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        policy = schema["extension_policy"]
        self.assertEqual(policy["reserved_columns"], ["CR", "CS"])
        self.assertEqual(policy["first_new_column"], "CT")
        self.assertTrue(policy["append_only"])
        self.assertTrue(policy["never_insert_before_or_within_baseline"])
        self.assertTrue(policy["never_rename_reorder_or_delete_baseline_headers"])

if __name__ == "__main__":
    unittest.main()
