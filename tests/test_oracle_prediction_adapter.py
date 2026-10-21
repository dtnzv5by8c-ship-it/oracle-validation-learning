import csv
import tempfile
import unittest
from pathlib import Path
from scripts.adapt_oracle_prediction_ledger import adapt_row, run

class OraclePredictionAdapterTests(unittest.TestCase):
    def base_row(self):
        return {
            "prediction_id":"p1", "fixture_id":"f1", "competition":"CRO",
            "fixture_date":"2026-10-09", "kickoff_time":"16:00:00+0000",
            "home_team":"Home", "away_team":"Away", "model":"BTTS_YES",
            "selection":"BTTS_YES", "raw_probability":"0.72",
            "prediction_timestamp":"2026-10-09T10:00:00Z", "model_version":"v1",
            "model_code_sha":"abc", "feature_snapshot_id":"release1",
            "source_manifest_hash":"a"*64, "model_status":"CHALLENGER"
        }

    def test_challenger_is_research_staged_not_mislabeled_production(self):
        result = adapt_row(self.base_row(), 2)
        self.assertEqual(result["quarantine_reasons"], [])
        self.assertEqual(result["adapted_prediction"]["market"], "BTTS")
        self.assertEqual(result["adapted_prediction"]["selection"], "YES")
        self.assertEqual(result["adapted_prediction"]["scheduled_kickoff_utc"], "2026-10-09T16:00:00+00:00")
        self.assertEqual(result["adapted_prediction"]["production_eligibility"], "NOT_GRANTED")
        self.assertIn("MISSING_HOME_TEAM_ID", result["evaluation_blockers"])
        self.assertIn("MISSING_AWAY_TEAM_ID", result["evaluation_blockers"])

    def test_naive_kickoff_time_is_not_assumed_utc(self):
        row = self.base_row()
        row["kickoff_time"] = "16:00:00"
        result = adapt_row(row, 2)
        self.assertIn("MISSING_OR_UNVERIFIED_KICKOFF", result["quarantine_reasons"])

    def test_prediction_at_or_after_kickoff_is_quarantined(self):
        row = self.base_row()
        row["prediction_timestamp"] = "2026-10-09T16:00:00Z"
        result = adapt_row(row, 2)
        self.assertIn("PREDICTION_NOT_STRICTLY_PRE_KICKOFF", result["quarantine_reasons"])

    def test_composite_market_is_quarantined(self):
        row = self.base_row()
        row["model"] = "HOME_1X_U45"
        result = adapt_row(row, 2)
        self.assertTrue(any(x.startswith("UNSUPPORTED_COMPOSITE_MARKET:") for x in result["quarantine_reasons"]))

    def test_manifest_hash_kept_separate_not_mislabeled_as_archive_hash(self):
        result = adapt_row(self.base_row(), 2)
        self.assertEqual(result["adapted_prediction"]["source_manifest_hash"], "a"*64)
        self.assertNotIn("archive_sha256", result["adapted_prediction"])

    def test_invalid_probability_quarantined(self):
        row = self.base_row()
        row["raw_probability"] = "1.2"
        self.assertIn("INVALID_OR_MISSING_PROBABILITY", adapt_row(row, 2)["quarantine_reasons"])

    def test_csv_run_reports_staging_and_blockers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "ledger.csv"
            with src.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(self.base_row().keys()))
                writer.writeheader()
                writer.writerow(self.base_row())
            summary = run(src, root/"accepted.jsonl", root/"quarantine.jsonl", root/"summary.json")
            self.assertEqual(summary["input_rows"], 1)
            self.assertEqual(summary["research_staged_rows"], 1)
            self.assertEqual(summary["quarantined_rows"], 0)
            self.assertEqual(summary["staged_rows_blocked_from_evaluation"], 1)

if __name__ == "__main__": unittest.main()
