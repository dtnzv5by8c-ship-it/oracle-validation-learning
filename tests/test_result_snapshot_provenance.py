import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from scripts.validate_result_snapshot_provenance import validate_snapshot


class ResultSnapshotProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.snapshot = self.root / "results.jsonl"
        self.manifest = self.root / "manifest.json"
        self.allowlist = self.root / "allowlist.json"
        self.row = {
            "fixture_id": "f1", "competition_id": "c1",
            "scheduled_kickoff_utc": "2026-10-01T12:00:00Z",
            "home_team_id": "h1", "away_team_id": "a1",
            "home_score": 2, "away_score": 1, "match_status": "FT",
            "result_observed_at_utc": "2026-10-01T14:00:00Z",
            "result_source": "official-results"
        }
        self.write_files()
    
    def tearDown(self):
        self.tmp.cleanup()

    def write_files(self, row=None, source="official-results"):
        self.row["result_source"] = source
        self.snapshot.write_text(json.dumps(row or self.row) + "\n", encoding="utf-8")
        self.allowlist.write_text(json.dumps({
            "schema_version": "oracle-result-source-allowlist-v1",
            "approved_sources": [{"source_id": "official-results", "status": "approved"}]
        }, sort_keys=True), encoding="utf-8")
        self.manifest.write_text(json.dumps({
            "schema_version": "oracle-result-acquisition-manifest-v1",
            "snapshot_id": "snapshot-001",
            "snapshot_sha256": self.sha(self.snapshot),
            "acquired_at_utc": "2026-10-02T10:00:00Z",
            "acquisition_run_id": "workflow-123",
            "acquisition_method": "manual-export",
            "source_id": source,
            "source_uri": "https://example.invalid/results"
        }, sort_keys=True), encoding="utf-8")

    @staticmethod
    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def validate(self):
        return validate_snapshot(str(self.snapshot), str(self.manifest), str(self.allowlist),
            self.sha(self.snapshot), self.sha(self.manifest), self.sha(self.allowlist),
            "2026-10-03T00:00:00Z")

    def test_approved_source_and_hashes_pass_structural_checks(self):
        result = self.validate()
        self.assertEqual(result["rows_structurally_accepted"], 1)
        self.assertFalse(result["provider_authenticity_independently_proven"])
        self.assertEqual(result["production_eligibility"], "NOT_GRANTED")

    def test_tampered_snapshot_hash_rejected(self):
        with self.assertRaisesRegex(ValueError, "RESULT_SNAPSHOT_HASH_MISMATCH"):
            validate_snapshot(str(self.snapshot), str(self.manifest), str(self.allowlist),
                "0" * 64, self.sha(self.manifest), self.sha(self.allowlist), "2026-10-03T00:00:00Z")

    def test_tampered_manifest_hash_rejected(self):
        with self.assertRaisesRegex(ValueError, "MANIFEST_HASH_MISMATCH"):
            validate_snapshot(str(self.snapshot), str(self.manifest), str(self.allowlist),
                self.sha(self.snapshot), "0" * 64, self.sha(self.allowlist), "2026-10-03T00:00:00Z")

    def test_tampered_allowlist_hash_rejected(self):
        with self.assertRaisesRegex(ValueError, "ALLOWLIST_HASH_MISMATCH"):
            validate_snapshot(str(self.snapshot), str(self.manifest), str(self.allowlist),
                self.sha(self.snapshot), self.sha(self.manifest), "0" * 64, "2026-10-03T00:00:00Z")

    def test_unapproved_source_rejected(self):
        self.write_files(source="unknown-source")
        with self.assertRaisesRegex(ValueError, "SOURCE_NOT_IN_INDEPENDENT_ALLOWLIST"):
            self.validate()

    def test_result_observed_before_kickoff_rejected(self):
        bad = dict(self.row, result_observed_at_utc="2026-10-01T11:00:00Z")
        self.write_files(row=bad)
        result = self.validate()
        self.assertEqual(result["rows_rejected"], 1)
        self.assertEqual(result["rejected"][0]["reason"], "RESULT_OBSERVED_BEFORE_KICKOFF")

    def test_non_final_match_rejected(self):
        bad = dict(self.row, match_status="POSTPONED")
        self.write_files(row=bad)
        result = self.validate()
        self.assertEqual(result["rows_rejected"], 1)
        self.assertEqual(result["rejected"][0]["reason"], "MATCH_NOT_FINAL")

    def test_row_source_mismatch_rejected(self):
        bad = dict(self.row, result_source="different-source")
        self.write_files(row=bad)
        result = self.validate()
        self.assertEqual(result["rows_rejected"], 1)
        self.assertEqual(result["rejected"][0]["reason"], "ROW_SOURCE_DIFFERS_FROM_MANIFEST")


if __name__ == "__main__":
    unittest.main()
