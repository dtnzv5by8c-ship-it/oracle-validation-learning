from pathlib import Path
import json
import unittest

WF = Path(".github/workflows/oracle-master-omi-excel.yml")
BUILDER = Path("scripts/build_master_omi_current.py")
CONTRACT = Path("docs/master_omi/CANONICAL_V2_1_1_CONTRACT.json")
SCHEMA = Path("docs/master_omi/CANONICAL_V2_1_1_SCHEMA.json")

class TestMasterOMIExactMatchingContract(unittest.TestCase):
    def test_workflow_exists(self):
        self.assertTrue(WF.exists())

    def test_builder_exists_and_has_explicit_identity_architecture(self):
        self.assertTrue(BUILDER.exists())
        text = BUILDER.read_text(encoding="utf-8")
        self.assertIn('ledger_by={str(r["fixture_id"]).strip():r for r in ledger}', text)
        self.assertIn('intel_by={str(r["fixture_id"]).strip():r for r in intel}', text)
        self.assertIn('set(spine_ids).issubset(set(intel_ids))', text)
        self.assertIn('MASTER_OMI_BLOCKED_LEDGER_FIXTURE_ID_SET_MISMATCH', text)
        self.assertIn('MASTER_OMI_BLOCKED_INTELLIGENCE_FIXTURE_ID_SET_MISMATCH', text)
        self.assertIn('MASTER_OMI_BLOCKED_INTELLIGENCE_PIT', text)

    def test_no_normalized_name_admission_in_current_builder(self):
        text = BUILDER.read_text(encoding="utf-8")
        forbidden = [
            'map(norm)',
            'norm(team)',
            'teammask("home_team",home)',
            'teammask("away_team",away)',
        ]
        for token in forbidden:
            self.assertNotIn(token, text, token)

    def test_variable_row_and_264_column_contract_is_locked(self):
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(contract.get("market_intelligence_columns"), 264)
        self.assertEqual(contract.get("market_intelligence_rows"), "VARIABLE_CURRENT_ROLLING_SPINE")
        self.assertEqual(schema.get("market_intelligence_columns"), 264)
        self.assertIs(schema.get("variable_fixture_rows"), True)
        self.assertEqual(len(schema.get("headers", [])), 264)

    def test_a_et_boundary_is_explicitly_protected(self):
        text = BUILDER.read_text(encoding="utf-8")
        self.assertIn('locked_ws["A1"].value', text)
        self.assertIn('locked_ws["ET1"].value', text)
        self.assertIn('A_ET_CONTRACT', text)

if __name__ == "__main__":
    unittest.main()
