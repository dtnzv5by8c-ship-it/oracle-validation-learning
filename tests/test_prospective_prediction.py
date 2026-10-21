import hashlib, unittest
from scripts.validate_prospective_prediction import validate_record

class ProspectivePredictionTests(unittest.TestCase):
    def setUp(self):
        self.record = {
            "prediction_id":"p-1", "fixture_id":"f-1", "competition_id":"ENG_PL", "scheduled_kickoff_utc":"2026-10-22T19:00:00Z",
            "home_team_id":"h-1", "away_team_id":"a-1", "market":"BTTS", "selection":"YES", "probability":0.61,
            "model_version":"research-only", "model_commit":"abc123", "archive_release_id":"release-1", "archive_sha256":hashlib.sha256(b'archive').hexdigest(),
            "prediction_created_at_utc":"2026-10-22T10:00:00Z", "max_source_timestamp_utc":"2026-10-22T09:30:00Z", "schema_version":"1"
        }
    def test_valid_prematch_record_accepted(self):
        self.assertEqual(validate_record(self.record, {})["status"], "ACCEPTED")
    def test_at_kickoff_rejected(self):
        self.record["prediction_created_at_utc"] = self.record["scheduled_kickoff_utc"]
        with self.assertRaisesRegex(ValueError, "PREDICTION_NOT_PREMATCH"): validate_record(self.record, {})
    def test_source_after_prediction_rejected(self):
        self.record["max_source_timestamp_utc"] = "2026-10-22T10:01:00Z"
        with self.assertRaisesRegex(ValueError, "SOURCE_DATA_AFTER_PREDICTION"): validate_record(self.record, {})
    def test_probability_out_of_range_rejected(self):
        self.record["probability"] = 1.1
        with self.assertRaisesRegex(ValueError, "INVALID_PROBABILITY"): validate_record(self.record, {})
    def test_identical_retry_is_idempotent(self):
        result = validate_record(self.record, {})
        existing = {result["idempotency_key"]: result["content_sha256"]}
        self.assertEqual(validate_record(self.record, existing)["status"], "DUPLICATE_IDENTICAL")
    def test_conflicting_duplicate_rejected(self):
        result = validate_record(self.record, {})
        existing = {result["idempotency_key"]: "different-hash"}
        with self.assertRaisesRegex(ValueError, "CONFLICTING_DUPLICATE"): validate_record(self.record, existing)

if __name__ == "__main__": unittest.main()
