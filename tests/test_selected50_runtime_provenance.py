import hashlib
import json
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from scripts.write_selected50_runtime_provenance import build_provenance


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Selected50RuntimeProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source.zip"
        self.overlay = self.root / "overlay.zip"
        self.snapshot = self.root / "snapshot.json"
        self.qa = self.root / "overlay-qa.json"
        self.metadata = self.root / "snapshot-artifact-metadata.json"
        self.report = self.root / "prediction.csv"
        self.snapshot_time = "2026-10-28T18:00:00+00:00"
        with zipfile.ZipFile(self.source, "w") as archive:
            archive.writestr("archive.json", "source")
        with zipfile.ZipFile(self.overlay, "w") as archive:
            archive.writestr("archive.json", "overlay")
        self.snapshot.write_text(json.dumps({
            "retrieved_utc": self.snapshot_time,
            "per_season": [{"selected_season_id": f"S{i}"} for i in range(50)],
            "fixture_rows": [{"id": "F1"}],
        }), encoding="utf-8")
        self.report.write_text("fixture_id,probability\nF1,55.0\n", encoding="utf-8")
        self.write_qa()
        self.metadata.write_text(json.dumps({
            "artifact_id": "789",
            "artifact_name": "oracle-selected50-current-fixture-snapshot",
            "artifact_digest": "sha256:" + "a" * 64,
            "artifact_size_bytes": 103738,
            "artifact_created_at": "2026-10-28T17:22:29Z",
            "artifact_expires_at": "2026-11-11T17:22:27Z",
            "artifact_expired": False,
            "artifact_workflow_run_id": "123",
            "artifact_head_branch": "research/oracle-50-league-readiness-audit",
            "artifact_head_sha": "deadbeef",
        }), encoding="utf-8")
        self.kwargs = dict(
            snapshot_path=self.snapshot,
            overlay_qa_path=self.qa,
            source_archive_path=self.source,
            selected_archive_path=self.overlay,
            runtime_report_path=self.report,
            include_current_snapshot=True,
            snapshot_run_id="123",
            runtime_run_id="456",
            runtime_run_number="7",
            runtime_run_attempt="1",
            runtime_sha="abc123",
            runtime_ref="refs/heads/research/oracle-50-league-readiness-audit",
            archive_release_tag="research-selected50-footystats-history-40447419806",
            runtime_archive_env=str(self.overlay),
            selected_archive_sha256_before_runtime=sha(self.overlay),
            snapshot_artifact_metadata_path=self.metadata,
        )

    def tearDown(self):
        self.temp.cleanup()

    def write_qa(self, **updates):
        qa = {
            "status": "PASS_RESEARCH_ONLY_STAGED",
            "snapshot_retrieved_utc": self.snapshot_time,
            "snapshot_file_sha256": sha(self.snapshot),
            "source_archive_sha256": sha(self.source),
            "overlay_archive_sha256": sha(self.overlay),
            "candidate_rows_added": 1,
            "refreshed_present_exact_fixture_ids": 2,
            "quarantined_or_invalid_rows": 3,
        }
        qa.update(updates)
        self.qa.write_text(json.dumps(qa), encoding="utf-8")

    def test_exact_snapshot_and_runtime_archive_hashes_are_verified(self):
        result = build_provenance(**self.kwargs)
        self.assertEqual(result["snapshot_consumption_status"], "PASS_SNAPSHOT_TO_RUNTIME_INPUT_HASH_VERIFIED")
        self.assertTrue(result["snapshot_consumption_verified"])
        self.assertTrue(result["selected_input_matches_overlay"])
        self.assertEqual(result["snapshot_file_sha256"], sha(self.snapshot))
        self.assertEqual(result["selected_runtime_input_archive_sha256"], sha(self.overlay))
        self.assertEqual(result["overlay_archive_sha256"], sha(self.overlay))
        self.assertEqual(result["runtime_report_sha256"], sha(self.report))
        self.assertEqual(result["snapshot_artifact_id"], "789")
        self.assertEqual(result["snapshot_artifact_digest"], "sha256:" + "a" * 64)
        self.assertEqual(result["snapshot_artifact_workflow_run_id"], "123")
        self.assertEqual(result["selected_runtime_input_archive_sha256_before_runtime"], sha(self.overlay))
        self.assertFalse(result["production_eligible"])
        self.assertFalse(result["betting_eligible"])

    def test_mismatched_snapshot_hash_fails_closed(self):
        self.write_qa(snapshot_file_sha256="wrong")
        with self.assertRaisesRegex(SystemExit, "snapshot SHA-256"):
            build_provenance(**self.kwargs)

    def test_mismatched_selected_archive_hash_fails_closed(self):
        self.write_qa(overlay_archive_sha256="wrong")
        with self.assertRaisesRegex(SystemExit, "selected runtime input archive SHA-256"):
            build_provenance(**self.kwargs)

    def test_runtime_archive_environment_must_match_selected_input_path(self):
        self.kwargs["runtime_archive_env"] = str(self.source)
        with self.assertRaisesRegex(SystemExit, "ORACLE_ARCHIVE path"):
            build_provenance(**self.kwargs)

    def test_pre_runtime_archive_hash_mismatch_fails_closed(self):
        self.kwargs["selected_archive_sha256_before_runtime"] = "0" * 64
        with self.assertRaisesRegex(SystemExit, "changed between pre-runtime fingerprint"):
            build_provenance(**self.kwargs)

    def test_snapshot_artifact_run_mismatch_fails_closed(self):
        metadata = json.loads(self.metadata.read_text(encoding="utf-8"))
        metadata["artifact_workflow_run_id"] = "999"
        self.metadata.write_text(json.dumps(metadata), encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "artifact metadata run ID"):
            build_provenance(**self.kwargs)

    def test_missing_snapshot_artifact_metadata_fails_closed(self):
        self.kwargs["snapshot_artifact_metadata_path"] = self.root / "missing-metadata.json"
        with self.assertRaisesRegex(SystemExit, "exact GitHub artifact metadata is missing"):
            build_provenance(**self.kwargs)

    def test_disabled_overlay_explicitly_does_not_claim_snapshot_consumption(self):
        self.kwargs["include_current_snapshot"] = False
        result = build_provenance(**self.kwargs)
        self.assertEqual(result["snapshot_consumption_status"], "NOT_CONSUMED_OVERLAY_DISABLED")
        self.assertFalse(result["snapshot_consumption_verified"])
        self.assertIsNone(result["snapshot_file_sha256"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
