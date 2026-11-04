import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from openpyxl import Workbook, load_workbook

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "write_selected50_unqueried_actual_results.py"
spec = importlib.util.spec_from_file_location("unqueried_actual_results", SCRIPT)
results = importlib.util.module_from_spec(spec)
spec.loader.exec_module(results)


class UnqueriedActualResultsTests(unittest.TestCase):
    def test_writes_explicit_no_credit_placeholder_without_inventing_scores(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "runtime.csv"
            workbook_path = root / "report.xlsx"
            out = root / "out"
            with runtime.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=[
                    "date_utc", "league", "home_team", "away_team", "provider_season_id",
                    "fixture_id", "home_team_provider_id", "away_team_provider_id"
                ])
                writer.writeheader()
                writer.writerow({
                    "date_utc": "2026-11-06T18:00:00Z", "league": "Test League",
                    "home_team": "Home FC", "away_team": "Away FC",
                    "provider_season_id": "S1", "fixture_id": "F1",
                    "home_team_provider_id": "H1", "away_team_provider_id": "A1"
                })
            wb = Workbook()
            wb.active.title = "Market Intelligence"
            wb.save(workbook_path)

            qa = results.write_placeholder(runtime, workbook_path, out)
            self.assertEqual(qa["status"], "NOT_RUN_CREDIT_APPROVAL_NOT_GRANTED")
            self.assertEqual(qa["provider_api_calls"], 0)
            self.assertEqual(qa["results_rows"], 1)
            self.assertFalse(qa["provider_credit_authorized"])
            self.assertFalse(qa["production_eligible"])
            self.assertFalse(qa["betting_eligible"])

            with (out / "oracle_selected50_actual_results.csv").open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["settlement_status"], "NOT_RETRIEVED_NO_CREDIT_APPROVAL")
            self.assertEqual(rows[0]["results_source"], "NOT_QUERIED")
            self.assertEqual(rows[0]["actual_home_goals"], "")
            self.assertEqual(rows[0]["actual_away_goals"], "")

            reopened = load_workbook(workbook_path, data_only=True)
            self.assertIn("Actual Results", reopened.sheetnames)
            self.assertEqual(reopened["Actual Results"].max_row, 2)
            self.assertEqual(reopened["Actual Results"]["P2"].value, "NOT_RETRIEVED_NO_CREDIT_APPROVAL")
            saved_qa = json.loads((out / "oracle_selected50_actual_results_qa.json").read_text())
            self.assertEqual(saved_qa["provider_api_calls"], 0)


if __name__ == "__main__":
    unittest.main()
