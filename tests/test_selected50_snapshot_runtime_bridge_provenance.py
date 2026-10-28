import hashlib
import json
import tempfile
import unittest
from argparse import Namespace
from datetime import datetime, timedelta, timezone
from pathlib import Path

from scripts.audit_selected50_snapshot_runtime_bridge import (
    classify_source_eligibility, verify_runtime_provenance,
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class SnapshotRuntimeBridgeStatusTests(unittest.TestCase):
    def test_only_documented_incomplete_status_is_eligible_for_future_fixture(self):
        now = datetime(2026, 10, 28, tzinfo=timezone.utc)
        future = now + timedelta(hours=2)
        self.assertEqual(classify_source_eligibility(False, "incomplete", future, now), "FUTURE_RESEARCH_CANDIDATE")
        self.assertEqual(classify_source_eligibility(False, "complete", future, now), "QUARANTINE_STATUS_INCONSISTENT_WITH_FUTURE_KICKOFF")
        self.assertEqual(classify_source_eligibility(False, "scheduled", future, now), "QUARANTINE_UNKNOWN_STATUS")
        self.assertEqual(classify_source_eligibility(False, "", future, now), "QUARANTINE_MISSING_STATUS")
        self.assertEqual(classify_source_eligibility(False, "suspended", future, now), "QUARANTINE_NONSTANDARD_STATUS")
        self.assertEqual(classify_source_eligibility(False, "canceled", future, now), "QUARANTINE_NONSTANDARD_STATUS")
        self.assertEqual(classify_source_eligibility(True, "incomplete", future, now), "QUARANTINE_NO_HOME_AWAY")
        self.assertEqual(classify_source_eligibility(None, "incomplete", future, now), "QUARANTINE_NO_HOME_AWAY_FLAG_UNKNOWN")


class SnapshotRuntimeBridgeProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.snapshot = self.root / "snapshot.json"
        self.report = self.root / "runtime.csv"
        self.provenance_path = self.root / "runtime-provenance.json"
        self.snapshot.write_text('{"retrieved_utc":"2026-10-28T18:00:00Z","per_season":[],"fixture_rows":[]}', encoding="utf-8")
        self.report.write_text("fixture_id,provider_season_id,home_team_provider_id,away_team_provider_id\nF1,S1,H1,A1\n", encoding="utf-8")
        self.provenance = {
            "snapshot_consumption_verified": True,
            "snapshot_consumption_status": "PASS_SNAPSHOT_TO_RUNTIME_INPUT_HASH_VERIFIED",
            "snapshot_file_sha256": sha(self.snapshot),
            "snapshot_run_id": "100",
            "snapshot_artifact_name": "oracle-selected50-current-fixture-snapshot",
            "snapshot_artifact_id": "789",
            "snapshot_artifact_digest": "sha256:" + "a" * 64,
            "snapshot_artifact_metadata_sha256": "b" * 64,
            "snapshot_artifact_workflow_run_id": "100",
            "runtime_run_id": "200",
            "selected_input_matches_overlay": True,
            "selected_runtime_input_archive_sha256": "overlay-hash",
            "selected_runtime_input_archive_sha256_before_runtime": "overlay-hash",
            "overlay_archive_sha256": "overlay-hash",
            "runtime_report_sha256": sha(self.report),
            "runtime_ref": "refs/heads/research/oracle-50-league-readiness-audit",
            "runtime_commit_sha": "abc123",
            "runtime_archive_env": "private-download/oracle-selected50-runtime-selected.zip",
            "selected_runtime_input_archive": "oracle-selected50-runtime-selected.zip",
        }
        self.write_provenance()
        self.args = Namespace(
            runtime_provenance=self.provenance_path,
            expected_snapshot_run_id="100",
            expected_runtime_run_id="200",
            runtime_report=self.report,
        )

    def tearDown(self):
        self.temp.cleanup()

    def write_provenance(self):
        self.provenance_path.write_text(json.dumps(self.provenance), encoding="utf-8")

    def test_exact_hashes_and_run_ids_verify(self):
        result = verify_runtime_provenance(self.args, sha(self.snapshot))
        self.assertTrue(result["verified"])
        self.assertEqual(result["status"], "PASS_SNAPSHOT_TO_RUNTIME_PROVENANCE_VERIFIED")
        self.assertEqual(result["failed_checks"], [])

    def test_snapshot_hash_mismatch_is_a_release_blocker(self):
        result = verify_runtime_provenance(self.args, "different-snapshot-hash")
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"], "BLOCKED_RUNTIME_PROVENANCE_CHECKS_FAILED")
        self.assertIn("snapshot_sha256_matches_supplied_snapshot", result["failed_checks"])

    def test_runtime_report_hash_mismatch_is_a_release_blocker(self):
        self.provenance["runtime_report_sha256"] = "wrong"
        self.write_provenance()
        result = verify_runtime_provenance(self.args, sha(self.snapshot))
        self.assertFalse(result["verified"])
        self.assertIn("runtime_report_hash_matches_downloaded_report", result["failed_checks"])

    def test_wrong_run_id_is_not_accepted(self):
        self.provenance["runtime_run_id"] = "999"
        self.write_provenance()
        result = verify_runtime_provenance(self.args, sha(self.snapshot))
        self.assertFalse(result["verified"])
        self.assertIn("expected_runtime_run_id_matches", result["failed_checks"])

    def test_missing_artifact_identity_is_a_release_blocker(self):
        self.provenance["snapshot_artifact_id"] = None
        self.write_provenance()
        result = verify_runtime_provenance(self.args, sha(self.snapshot))
        self.assertFalse(result["verified"])
        self.assertIn("snapshot_artifact_id_present", result["failed_checks"])

    def test_snapshot_artifact_run_mismatch_is_a_release_blocker(self):
        self.provenance["snapshot_artifact_workflow_run_id"] = "999"
        self.write_provenance()
        result = verify_runtime_provenance(self.args, sha(self.snapshot))
        self.assertFalse(result["verified"])
        self.assertIn("snapshot_artifact_run_id_matches", result["failed_checks"])

    def test_runtime_input_hash_must_match_pre_runtime_fingerprint(self):
        self.provenance["selected_runtime_input_archive_sha256_before_runtime"] = "different-hash"
        self.write_provenance()
        result = verify_runtime_provenance(self.args, sha(self.snapshot))
        self.assertFalse(result["verified"])
        self.assertIn("runtime_input_hash_matches_pre_runtime_fingerprint", result["failed_checks"])

    def test_missing_provenance_stays_unverified(self):
        self.args.runtime_provenance = self.root / "missing.json"
        result = verify_runtime_provenance(self.args, sha(self.snapshot))
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"], "UNVERIFIED_RUNTIME_PROVENANCE_MISSING")


if __name__ == "__main__":
    unittest.main(verbosity=2)
