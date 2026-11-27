import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class MasterOMIVariableRowContractTests(unittest.TestCase):
    def test_schema_is_variable_and_264(self):
        contract=json.loads((ROOT/"docs/master_omi/CANONICAL_V2_1_1_CONTRACT.json").read_text())
        schema=json.loads((ROOT/"docs/master_omi/CANONICAL_V2_1_1_SCHEMA.json").read_text())
        self.assertEqual(contract["market_intelligence_columns"],264)
        self.assertEqual(contract["market_intelligence_rows"],"VARIABLE_CURRENT_ROLLING_SPINE")
        self.assertTrue(schema["variable_fixture_rows"])
        self.assertEqual(schema["market_intelligence_columns"],264)

    def test_exporter_does_not_freeze_weekly_fixture_count(self):
        wf=(ROOT/".github/workflows/oracle-master-omi-excel.yml").read_text()
        self.assertIn("scripts/build_master_omi_current.py",wf)
        self.assertNotIn("754-unique-Fixture-ID gate",wf)
        self.assertNotIn("755x264",wf)
        self.assertNotIn("MASTER_OMI_BLOCKED_NO_SAFE_OVERLAY_IMPLEMENTATION",wf)

    def test_overlay_builder_exists(self):
        self.assertTrue((ROOT/"scripts/build_master_omi_current.py").is_file())

if __name__=="__main__":
    unittest.main()
