import unittest
from datetime import timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_selected50_kickoff_source_evidence import validate


def queue_row(fid="1"):
    return {
        "fixture_id": fid, "fixture": "Home vs Away",
        "runtime_kickoff_utc": "2026-11-01T17:00:00+00:00",
        "archive_kickoff_utc": "2026-11-01T18:00:00+00:00",
        "schedule_reconciliation_status": "REVIEW_REQUIRED",
        "resolution_action": "MANUAL_AUTHORITATIVE_EVENT_TIME_REVIEW_ONLY_NO_AUTO_CORRECTION",
        "schedule_auto_correction": "NO", "production_eligible": "NO",
        "betting_eligible": "NO",
    }


def evidence_row(fid="1"):
    return {
        "fixture_id": fid, "fixture": "Home vs Away",
        "runtime_kickoff_utc": "2026-11-01T17:00:00Z",
        "archive_kickoff_utc": "2026-11-01T18:00:00Z",
        "external_source_status": "AUTHORITATIVE_TIME_CORROBORATES_RUNTIME",
        "source_local_kickoff": "2026-11-01 19:00",
        "source_timezone": "Europe/Athens",
        "source_converted_utc": "2026-11-01T17:00:00Z",
        "source_url": "https://example.org/fixture",
        "decision": "CORROBORATES_RUNTIME_NO_AUTO_CORRECTION",
    }


class KickoffEvidenceRegisterTests(unittest.TestCase):
    def test_exact_join_and_timezone_conversion_pass(self):
        result = validate([queue_row()], [evidence_row()])
        self.assertEqual(result["status"], "PASS_REPORT_ONLY_KICKOFF_EVIDENCE_REGISTER")
        self.assertEqual(result["authoritative_runtime_corroborations"], 1)
        self.assertEqual(result["schedule_auto_corrections"], 0)
        self.assertFalse(result["production_eligible"])

    def test_authoritative_source_can_corroborate_archive_without_rewriting_runtime(self):
        queue = queue_row()
        queue["runtime_kickoff_utc"] = "2026-11-01T14:00:00+00:00"
        queue["archive_kickoff_utc"] = "2026-10-30T18:00:00+00:00"
        evidence = evidence_row()
        evidence.update({
            "runtime_kickoff_utc": "2026-11-01T14:00:00Z",
            "archive_kickoff_utc": "2026-10-30T18:00:00Z",
            "external_source_status": "AUTHORITATIVE_TIME_CORROBORATES_ARCHIVE",
            "source_local_kickoff": "2026-10-30 18:00",
            "source_timezone": "Europe/Lisbon",
            "source_converted_utc": "2026-10-30T18:00:00Z",
            "decision": "CORROBORATES_ARCHIVE_NO_AUTO_CORRECTION",
        })
        result = validate([queue], [evidence])
        self.assertEqual(result["authoritative_archive_corroborations"], 1)
        self.assertEqual(result["authoritative_runtime_corroborations"], 0)
        self.assertEqual(result["schedule_auto_corrections"], 0)

    def test_partial_fixture_scope_is_explicitly_review_required(self):
        result = validate([queue_row("1")], [evidence_row("2")])
        self.assertEqual(result["status"], "REVIEW_REQUIRED_EVIDENCE_REGISTER_SCOPE_MISMATCH")
        self.assertEqual(result["validated_in_scope_evidence_rows"], 0)
        self.assertEqual(result["uncovered_queue_fixture_ids"], ["1"])
        self.assertEqual(result["out_of_scope_evidence_fixture_ids"], ["2"])
        self.assertEqual(result["schedule_auto_corrections"], 0)

    def test_timezone_conversion_mismatch_fails_closed(self):
        row = evidence_row()
        row["source_converted_utc"] = "2026-11-01T18:00:00Z"
        with self.assertRaisesRegex(ValueError, "conversion mismatch"):
            validate([queue_row()], [row])

    def test_runtime_disagreement_fails_closed(self):
        row = evidence_row()
        row["source_local_kickoff"] = "2026-11-01 20:00"
        with self.assertRaisesRegex(ValueError, "source local-to-UTC conversion mismatch"):
            validate([queue_row()], [row])

    def test_unresolved_source_stays_review_required(self):
        row = evidence_row()
        row.update({
            "external_source_status": "SECONDARY_ONLY_OFFICIAL_KICKOFF_NOT_VERIFIED",
            "source_local_kickoff": "not accepted", "source_timezone": "Europe/Athens",
            "source_converted_utc": "",
            "decision": "REVIEW_REQUIRED_NO_CORRECTION",
        })
        result = validate([queue_row()], [row])
        self.assertEqual(result["unresolved_or_conflicted_sources"], 1)
        self.assertEqual(result["authoritative_runtime_corroborations"], 0)

    def test_auto_correction_cannot_be_authorized(self):
        row = queue_row()
        row["schedule_auto_correction"] = "YES"
        with self.assertRaisesRegex(ValueError, "auto-correction"):
            validate([row], [evidence_row()])


if __name__ == "__main__":
    unittest.main()
