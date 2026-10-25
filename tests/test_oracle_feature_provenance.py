import unittest

from scripts.validate_oracle_feature_provenance import validate


GOOD_HASH = "a" * 64


def row(**overrides):
    base = {
        "fixture_id": "fixture-001",
        "feature_name": "home_xg",
        "kickoff_utc": "2026-08-01T18:00:00Z",
        "observed_at_utc": "2026-08-01T16:00:00Z",
        "retrieved_at_utc": "2026-08-01T16:05:00Z",
        "source_id": "approved-source-pending-review",
        "snapshot_hash": GOOD_HASH,
        "value": "1.42",
    }
    base.update(overrides)
    return base


class FeatureProvenanceTests(unittest.TestCase):
    def test_pre_kickoff_timezone_aware_feature_passes_row_level_checks(self):
        report = validate([row()])
        self.assertEqual(report["rows_passing_row_level_checks"], 1)
        self.assertEqual(report["rows_rejected"], 0)
        self.assertTrue(report["feature_point_in_time_gate_passed"])
        self.assertFalse(report["source_authenticity_proven"])
        self.assertFalse(report["season_completeness_proven"])
        self.assertFalse(report["production_changes"])

    def test_feature_observed_at_kickoff_is_rejected(self):
        report = validate([row(observed_at_utc="2026-08-01T18:00:00Z")])
        self.assertFalse(report["feature_point_in_time_gate_passed"])
        self.assertEqual(report["errors"][0]["reason"], "FEATURE_NOT_PROVEN_PRE_KICKOFF")

    def test_feature_observed_after_kickoff_is_rejected(self):
        report = validate([row(observed_at_utc="2026-08-01T18:01:00Z")])
        self.assertEqual(report["errors"][0]["reason"], "FEATURE_NOT_PROVEN_PRE_KICKOFF")

    def test_missing_timestamp_is_rejected(self):
        report = validate([row(observed_at_utc="")])
        self.assertEqual(report["errors"][0]["reason"], "MISSING_REQUIRED_FIELDS")

    def test_timezone_naive_timestamp_is_rejected(self):
        report = validate([row(observed_at_utc="2026-08-01T16:00:00")])
        self.assertEqual(report["errors"][0]["reason"], "INVALID_OR_TIMEZONE_NAIVE_TIMESTAMP")

    def test_retrieval_before_observation_is_rejected(self):
        report = validate([row(retrieved_at_utc="2026-08-01T15:59:00Z")])
        self.assertEqual(report["errors"][0]["reason"], "RETRIEVAL_PRECEDES_OBSERVATION")

    def test_invalid_hash_is_rejected(self):
        report = validate([row(snapshot_hash="not-a-hash")])
        self.assertEqual(report["errors"][0]["reason"], "INVALID_SNAPSHOT_SHA256")

    def test_empty_input_fails_closed(self):
        report = validate([])
        self.assertFalse(report["feature_point_in_time_gate_passed"])


if __name__ == "__main__":
    unittest.main()
