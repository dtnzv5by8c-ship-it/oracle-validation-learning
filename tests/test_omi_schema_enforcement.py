import json
import tempfile
import unittest
from pathlib import Path
from openpyxl import Workbook, load_workbook
from scripts.enforce_omi_market_intelligence_schema import enforce

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "config" / "omi_market_intelligence_schema_v1.json"

class TestOmiSchemaEnforcement(unittest.TestCase):
    def test_enforces_full_reference_layout_and_fixture_id_join(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "omi.xlsx"
            wb = Workbook()
            omi = wb.active
            omi.title = "OMI Report"
            market = wb.create_sheet("Market Intelligence")
            omi.append(["Fixture ID", "Fixture Date", "League"])
            omi.append(["1001", "2026-11-04", "Test League"])
            market.append(["Fixture ID", "Fixture Date", "League"])
            market.append(["1001", "old", "old"])
            wb.save(path)
            result = enforce(path, SCHEMA)
            self.assertEqual(result["status"], "PASS")
            check = load_workbook(path, read_only=True, data_only=True)
            for name in ("OMI Report", "Market Intelligence"):
                ws = check[name]
                self.assertEqual([ws.cell(1, c).value for c in range(1, 96)], schema["headers"])
                self.assertEqual(ws.cell(2, 1).value, "2026-11-04")
                self.assertEqual(ws.cell(2, 39).value, "1001") if schema["headers"][38] == "Fixture ID" else None

    def test_refuses_mismatched_fixture_sets(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "omi.xlsx"
            wb = Workbook()
            omi = wb.active; omi.title = "OMI Report"
            market = wb.create_sheet("Market Intelligence")
            omi.append(["Fixture ID"]); omi.append(["A"])
            market.append(["Fixture ID"]); market.append(["B"])
            wb.save(path)
            with self.assertRaises(ValueError):
                enforce(path, SCHEMA)

if __name__ == "__main__":
    unittest.main()
