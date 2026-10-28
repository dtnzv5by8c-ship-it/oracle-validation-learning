import hashlib
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from scripts.audit_selected50_snapshot_runtime_bridge import verify_runtime_provenance


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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
            "runtime_run_id": "200",
            "selected_input_matches_overlay": True,
            "selected_runtime_input_archive_sha256": "overlay-hash",
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

    def test_missing_provenance_stays_unverified(self):
        self.args.runtime_provenance = self.root / "missing.json"
        result = verify_runtime_provenance(self.args, sha(self.snapshot))
        self.assertFalse(result["verified"])
        self.assertEqual(result["status"], "UNVERIFIED_RUNTIME_PROVENANCE_MISSING")


if __name__ == "__main__":
    unittest.main(verbosity=2)
