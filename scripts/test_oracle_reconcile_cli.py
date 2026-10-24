"""End-to-end tests for the research CSV reconciliation command-line tool."""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "oracle_reconcile_outputs.py"


class ReconcileCliTests(unittest.TestCase):
    def write_csv(self, path, headers, rows):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    def invoke(self, schedule, predictions, report, expected_markets="BTTS_YES,BTTS_NO"):
        return subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--expected-fixtures", str(schedule),
                "--predictions", str(predictions),
                "--expected-markets", expected_markets,
                "--output-json", str(report),
            ],
            text=True, capture_output=True, check=False,
        )

    def test_cli_passes_complete_fixture_market_matrix(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            schedule, predictions, report = root / "schedule.csv", root / "predictions.csv", root / "report.json"
            self.write_csv(schedule, ["fixture_id"], [{"fixture_id": "F1"}, {"fixture_id": "F2"}])
            self.write_csv(predictions, ["fixture_id", "selection", "raw_probability"], [
                {"fixture_id": "F1", "selection": "BTTS_YES", "raw_probability": "0.61"},
                {"fixture_id": "F1", "selection": "BTTS_NO", "raw_probability": "0.39"},
                {"fixture_id": "F2", "selection": "BTTS_YES", "raw_probability": "0.52"},
                {"fixture_id": "F2", "selection": "BTTS_NO", "raw_probability": "0.48"},
            ])
            result = self.invoke(schedule, predictions, report)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(report.read_text())["status"], "PASS")

    def test_cli_fails_when_expected_fixture_has_no_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            schedule, predictions, report = root / "schedule.csv", root / "predictions.csv", root / "report.json"
            self.write_csv(schedule, ["fixture_id"], [{"fixture_id": "F1"}, {"fixture_id": "F2"}])
            self.write_csv(predictions, ["fixture_id", "selection", "raw_probability"], [
                {"fixture_id": "F1", "selection": "BTTS_YES", "raw_probability": "0.61"},
                {"fixture_id": "F1", "selection": "BTTS_NO", "raw_probability": "0.39"},
            ])
            result = self.invoke(schedule, predictions, report)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            payload = json.loads(report.read_text())
            self.assertEqual(payload["status"], "FAIL")
            self.assertIn("MISSING_FIXTURE_OUTPUT:F2", payload["errors"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
