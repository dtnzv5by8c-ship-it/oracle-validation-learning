import csv
import tempfile
import unittest
from pathlib import Path
from scripts.adapt_oracle_prediction_ledger import adapt_row, run

class OraclePredictionAdapterTests(unittest.TestCase):
    def test_missing_team_ids_and_utc_timestamps_are_quarantined(self):
        row = {
            "prediction_id": "p1", "fixture_id": "f1", "competition": "ENG_PL",
            "fixture_date": "2026-10-22", "kickoff_time": "19:00",
            "home_team": "Home", "away_team": "Away", "model": "BTTS_YES",
            "selection": "BTTS_YES", "raw_probability": "0.72",
            "prediction_timestamp": "2026-10-22 10:00:00", "model_version": "v1",
            "model_code_sha": "abc", "feature_snapshot_id": "release1",
            "source_manifest_hash": "a" * 64, "model_status": "CHALLENGER"
        }
        result = adapt_row(row, 2)
        reasons = result["quarantine_reasons"]
        self.assertTrue(any(x.startswith("MISSING_REQUIRED_FIELDS:") for x in reasons))
        self.assertTrue(any(x == "NOT_CONFIRMED_PRODUCTION:CHALLENGER" for x in reasons))
        self.assertTrue(any(x.startswith("TIMESTAMP_NOT_TIMEZONE_AWARE:") for x in reasons))
        self.assertEqual(result["adapted_prediction"]["probability"], 0.72)
        self.assertEqual(result["source_row"]["fixture_date"], "2026-10-22")

    def test_valid_schema_only_row_can_be_adapted_but_not_proven(self):
        row = {
            "prediction_id":"p2", "fixture_id":"f2", "competition_id":"ENG_PL",
            "scheduled_kickoff_utc":"2026-10-22T19:00:00Z",
            "home_team_id":"h2", "away_team_id":"a2", "market":"BTTS",
            "selection":"YES", "probability":"0.7",
            "prediction_timestamp_utc":"2026-10-22T10:00:00Z",
            "model_version":"v1", "model_commit":"abc",
            "archive_release_id":"r1", "archive_sha256":"b"*64,
            "model_status":"PRODUCTION"
        }
        result = adapt_row(row, 2)
        self.assertEqual(result["quarantine_reasons"], [])
        self.assertEqual(result["adapted_prediction"]["probability"], 0.7)

    def test_known_model_alias_is_normalized_explicitly(self):
        row = {
            "prediction_id":"p4", "fixture_id":"f4", "competition":"ENG_PL",
            "scheduled_kickoff_utc":"2026-10-22T19:00:00Z", "home_team_id":"h",
            "away_team_id":"a", "model":"BTTS_YES", "selection":"BTTS_YES",
            "raw_probability":"0.65", "prediction_timestamp_utc":"2026-10-22T10:00:00Z",
            "model_version":"v1", "model_code_sha":"abc", "feature_snapshot_id":"r",
            "source_manifest_hash":"b"*64, "model_status":"PRODUCTION"
        }
        result = adapt_row(row, 2)
        self.assertEqual(result["adapted_prediction"]["market"], "BTTS")
        self.assertEqual(result["adapted_prediction"]["selection"], "YES")
        self.assertFalse(any(x.startswith("UNRECOGNIZED_MARKET_LABEL") for x in result["quarantine_reasons"]))

    def test_unsupported_composite_market_is_quarantined(self):
        row = {
            "prediction_id":"p5", "fixture_id":"f5", "competition":"ENG_PL",
            "scheduled_kickoff_utc":"2026-10-22T19:00:00Z", "home_team_id":"h",
            "away_team_id":"a", "model":"HOME_1X_U45", "selection":"HOME_1X_U45",
            "raw_probability":"0.65", "prediction_timestamp_utc":"2026-10-22T10:00:00Z",
            "model_version":"v1", "model_code_sha":"abc", "feature_snapshot_id":"r",
            "source_manifest_hash":"b"*64, "model_status":"PRODUCTION"
        }
        result = adapt_row(row, 2)
        self.assertTrue(any(x.startswith("UNSUPPORTED_COMPOSITE_MARKET:") for x in result["quarantine_reasons"]))

    def test_manifest_hash_is_not_accepted_as_archive_hash(self):
        row = {
            "prediction_id":"p6", "fixture_id":"f6", "competition":"ENG_PL",
            "scheduled_kickoff_utc":"2026-10-22T19:00:00Z", "home_team_id":"h",
            "away_team_id":"a", "model":"BTTS_YES", "selection":"YES",
            "raw_probability":"0.65", "prediction_timestamp_utc":"2026-10-22T10:00:00Z",
            "model_version":"v1", "model_code_sha":"abc", "feature_snapshot_id":"r",
            "source_manifest_hash":"c"*64, "model_status":"PRODUCTION"
        }
        result = adapt_row(row, 2)
        self.assertTrue(any(x == "SOURCE_MANIFEST_HASH_IS_NOT_ARCHIVE_HASH" for x in result["quarantine_reasons"]))
        self.assertNotIn("archive_sha256", result["source_columns"])

    def test_invalid_probability_quarantined(self):
        row = {"prediction_id":"p3", "fixture_id":"f3", "competition_id":"c",
            "scheduled_kickoff_utc":"2026-10-22T19:00:00Z","home_team_id":"h",
            "away_team_id":"a","market":"BTTS","selection":"YES","probability":"1.2",
            "prediction_timestamp_utc":"2026-10-22T10:00:00Z","model_version":"v1",
            "model_commit":"abc","archive_release_id":"r","archive_sha256":"b"*64,
            "model_status":"PRODUCTION"}
        self.assertIn("INVALID_OR_MISSING_PROBABILITY", adapt_row(row, 2)["quarantine_reasons"])

    def test_csv_run_writes_counts_and_quarantine(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "ledger.csv"
            with src.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["prediction_id","fixture_id","competition","model_status"])
                writer.writeheader()
                writer.writerow({"prediction_id":"p1","fixture_id":"f1","competition":"c","model_status":"CHALLENGER"})
            summary = run(src, root/"accepted.jsonl", root/"quarantine.jsonl", root/"summary.json")
            self.assertEqual(summary["input_rows"], 1)
            self.assertEqual(summary["accepted_rows"], 0)
            self.assertEqual(summary["quarantined_rows"], 1)
            self.assertTrue((root/"quarantine.jsonl").exists())

if __name__ == "__main__": unittest.main()
