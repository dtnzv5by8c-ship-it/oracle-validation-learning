import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_footystats_xg_manifest_provenance import audit_archive  # noqa: E402


class FootyStatsXgManifestProvenanceTests(unittest.TestCase):
    def make_archive(self, root, manifest, matches, extra_manifest=False, include_manifest=True):
        path = root / "archive.zip"
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            if include_manifest:
                archive.writestr("ingestion_manifest.json", json.dumps(manifest))
            if extra_manifest:
                archive.writestr("backup/ingestion_manifest.json", json.dumps(manifest))
            archive.writestr("seasons/S1/matches.json", json.dumps(matches))
        return path

    def test_season_manifest_is_not_misclassified_as_fixture_capture(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = self.make_archive(
                root,
                [{"season_id": "S1", "selected_country": "Test", "selected_competition_name": "League"}],
                [{"id": "M1", "team_a_xg_prematch": 1.2, "team_b_xg_prematch": 0.9,
                  "total_xg_prematch": 2.1}],
            )
            summary, fields = audit_archive(archive)
            self.assertEqual(summary["manifest_grain_candidate"], "SEASON_LEVEL")
            self.assertEqual(summary["manifest_rows_with_capture_timestamp_candidate"], 0)
            self.assertEqual(summary["match_records_with_any_prematch_xg_field"], 1)
            self.assertFalse(summary["xg_point_in_time_provenance_verified"])
            self.assertTrue(summary["xg_quarantine_required"])
            self.assertEqual(summary["provider_api_calls"], 0)

    def test_fixture_linked_timestamp_and_hash_are_candidates_not_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = self.make_archive(
                root,
                [{"season_id": "S1", "match_id": "M1",
                  "response_received_at_utc": "2026-01-01T12:00:00Z",
                  "raw_response_sha256": "DO_NOT_EMIT_SECRET_SENTINEL",
                  "revision_id": "r1"}],
                [{"id": "M1", "team_a_xg_prematch": 1.2}],
            )
            summary, fields = audit_archive(archive)
            self.assertEqual(summary["manifest_grain_candidate"], "FIXTURE_AND_SEASON_FIELDS_PRESENT")
            self.assertEqual(summary["manifest_rows_with_fixture_capture_and_hash_candidates"], 1)
            self.assertFalse(summary["xg_point_in_time_provenance_verified"])
            serialized = json.dumps(summary) + json.dumps(fields)
            self.assertNotIn("DO_NOT_EMIT_SECRET_SENTINEL", serialized)
            self.assertIn("response_received_at_utc", serialized)
            self.assertIn("raw_response_sha256", serialized)

    def test_duplicate_ingestion_manifests_are_reported_as_ambiguous(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = self.make_archive(root, [{"season_id": "S1"}], [], extra_manifest=True)
            summary, fields = audit_archive(archive)
            self.assertEqual(summary["manifest_status"], "AMBIGUOUS")
            self.assertEqual(summary["status"], "BLOCKED_MANIFEST_AMBIGUOUS")
            self.assertEqual(summary["manifest_rows"], 0)
            self.assertTrue(summary["xg_quarantine_required"])

    def test_missing_ingestion_manifest_does_not_hide_match_metadata_inventory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = self.make_archive(
                root, [], [{"id": "M1", "team_a_xg_prematch": 1.2}], include_manifest=False
            )
            summary, fields = audit_archive(archive)
            self.assertEqual(summary["manifest_status"], "MISSING")
            self.assertEqual(summary["status"], "BLOCKED_MANIFEST_MISSING")
            self.assertEqual(summary["match_records_with_any_prematch_xg_field"], 1)
            self.assertFalse(summary["xg_point_in_time_provenance_verified"])
            self.assertTrue(summary["xg_quarantine_required"])

    def test_expected_archive_digest_is_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = self.make_archive(root, [{"season_id": "S1"}], [{"id": "M1"}])
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                audit_archive(archive, "0" * 64)


if __name__ == "__main__":
    unittest.main()
