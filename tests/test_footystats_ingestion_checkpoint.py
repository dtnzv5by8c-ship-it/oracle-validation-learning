import csv
import json
import hashlib
import hmac
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import footystats_ingestion_checkpoint as checkpoint


TEST_VERIFICATION_KEYS = {
    "archive": b"archive-test-key-32-bytes-minimum-0001",
    "budget": b"budget-test-key-32-bytes-minimum-0002",
}


def task(task_id="FS:101:league-matches:p1", endpoint="league-matches", page=1):
    paged = endpoint in checkpoint.PAGED_ENDPOINTS
    total = 1200 if endpoint == "league-matches" else 20 if endpoint == "league-teams" else ""
    per_page = 600 if endpoint == "league-matches" else 50 if endpoint == "league-teams" else ""
    pages = 2 if endpoint == "league-matches" else 1
    return {
        "task_id": task_id,
        "batch_id": "batch-0001",
        "provider": "FootyStats",
        "provider_league_name": "Test League",
        "provider_season_label": "2024",
        "provider_season_id": "101",
        "endpoint": endpoint,
        "page": str(page),
        "max_per_page": str(per_page) if paged else "",
        "include": "",
        "max_time_unix": "",
        "expected_total_results": str(total) if paged else "",
        "expected_page_count": str(pages),
        "request_status": "PLANNED_NOT_EXECUTED",
        "raw_storage_required": "True",
        "production_eligible": "False",
        "betting_eligible": "False",
    }


def success_receipt(t, **overrides):
    value = {
        "status": "SUCCESS",
        "task_id": t["task_id"],
        "provider": "FootyStats",
        "provider_season_id": t["provider_season_id"],
        "endpoint": t["endpoint"],
        "page": int(t["page"]),
        "request_timestamp_utc": "2026-11-04T18:00:00Z",
        "request_gateway": "central_footystats_gateway",
        "budget_reservation_id": "gha-123-1",
        "budget_ledger_attested": True,
        "global_rolling_hour_limit": 1800,
        "reserved_headroom": 300,
        "response_http_status": 200,
        "provider_success": True,
        "response_shape_verified": True,
        "page_complete": True,
        "response_total_results": int(t["expected_total_results"]) if t["endpoint"] in checkpoint.PAGED_ENDPOINTS else None,
        "response_page": int(t["page"]),
        "response_page_count": int(t["expected_page_count"]),
        "returned_rows": min(
            int(t["max_per_page"]),
            max(0, int(t["expected_total_results"]) - ((int(t["page"]) - 1) * int(t["max_per_page"])))
        ) if t["endpoint"] in checkpoint.PAGED_ENDPOINTS else 1,
        "unique_ids_on_page": min(
            int(t["max_per_page"]),
            max(0, int(t["expected_total_results"]) - ((int(t["page"]) - 1) * int(t["max_per_page"])))
        ) if t["endpoint"] in checkpoint.PAGED_ENDPOINTS else None,
        "required_fields_present": sorted(checkpoint.REQUIRED_FIELDS_BY_ENDPOINT[t["endpoint"]] | (
            {"homeGoalCount", "awayGoalCount", "totalGoalCount"} if t["endpoint"] == "league-matches" else set()
        )),
        "required_fields_missing": [],
        "completed_match_rows": 580 if t["endpoint"] == "league-matches" else None,
        "completed_match_goal_field_gaps": 0 if t["endpoint"] == "league-matches" else None,
        "no_home_away_rows": 10 if t["endpoint"] == "league-matches" else None,
        "xg_fields_missing": ["fixture_level_xg_provenance"],
        "payload_sha256": "a" * 64,
        "private_archive_receipt_sha256": "b" * 64,
        "private_archive_write_verified": True,
        "raw_payload_stored_privately": True,
        "public_raw_payload_written": False,
    }
    value.update(overrides)
    identity = {
        "task_id": t["task_id"], "provider": "FootyStats",
        "provider_season_id": t["provider_season_id"], "endpoint": t["endpoint"],
        "page": int(t["page"]),
    }
    archive_claims = {
        **identity,
        "archive_object_id": f"private-test-archive/{t['task_id']}",
        "archive_object_version_id": "version-1",
        "archive_object_size_bytes": 4096,
        "payload_sha256": value["payload_sha256"],
        "archive_object_bytes_hash_verified": True,
        "archive_receipt_object_id": f"private-test-receipts/{t['task_id']}",
        "archive_receipt_sha256": value["private_archive_receipt_sha256"],
        "archive_receipt_bytes_hash_verified": True,
        "writer_receipt_signature_verified": True,
        "private_visibility_verified": True,
        "private_archive_write_verified": value["private_archive_write_verified"],
        "raw_payload_stored_privately": value["raw_payload_stored_privately"],
        "public_raw_payload_written": value["public_raw_payload_written"],
        "response_metadata_sha256": checkpoint.response_metadata_digest(value),
        "verified_at_utc": "2026-11-04T18:00:02Z",
    }
    budget_claims = {
        **identity,
        "reservation_id": value["budget_reservation_id"],
        "ledger_entry_id": f"ledger-entry-{t['task_id']}",
        "request_event_id": f"request-event-{t['task_id']}",
        "request_count": 1,
        "request_timestamp_utc": value["request_timestamp_utc"],
        "rolling_60m_request_count_after": 1,
        "hard_limit": 1800,
        "operational_limit": 1500,
        "reserved_headroom": value["reserved_headroom"],
        "provider_limit_enforced": True,
        "ledger_record_resolved": value["budget_ledger_attested"],
        "request_event_resolved": value["budget_ledger_attested"],
        "verified_at_utc": "2026-11-04T18:00:03Z",
    }
    def sign(claims, signer_id, key_id, key):
        signature = hmac.new(key, checkpoint.canonical_json_bytes(claims), hashlib.sha256).hexdigest()
        return {"algorithm": "HMAC-SHA256", "signer_id": signer_id, "key_id": key_id,
                "claims": claims, "signature_hex": signature}
    value["archive_verification"] = sign(
        archive_claims, checkpoint.ARCHIVE_VERIFIER_ID,
        checkpoint.ARCHIVE_VERIFIER_KEY_ID, TEST_VERIFICATION_KEYS["archive"]
    )
    value["budget_verification"] = sign(
        budget_claims, checkpoint.BUDGET_VERIFIER_ID,
        checkpoint.BUDGET_VERIFIER_KEY_ID, TEST_VERIFICATION_KEYS["budget"]
    )
    return value


def build_resume_plan(tasks, receipts, max_batch_requests, verification_keys=TEST_VERIFICATION_KEYS):
    return checkpoint.build_resume_plan(tasks, receipts, max_batch_requests, verification_keys)


def failure_receipt(t, code="HTTP_429"):
    return {
        "status": "FAILED",
        "task_id": t["task_id"],
        "provider": "FootyStats",
        "provider_season_id": t["provider_season_id"],
        "endpoint": t["endpoint"],
        "page": int(t["page"]),
        "request_timestamp_utc": "2026-11-04T18:00:00Z",
        "failure_code": code,
    }


class FootyStatsIngestionCheckpointTests(unittest.TestCase):
    def test_pending_batch_is_deterministic_and_never_dispatches(self):
        tasks = [
            task("FS:101:league-matches:p1", page=1),
            task("FS:101:league-matches:p2", page=2),
            task("FS:101:league-teams:p1", endpoint="league-teams", page=1),
        ]
        next_batch, statuses, summary = build_resume_plan(tasks, [], 2)
        self.assertEqual([row["task_id"] for row in next_batch], [
            "FS:101:league-matches:p1", "FS:101:league-matches:p2"
        ])
        self.assertEqual(summary["execution_gate"], "READY_FOR_CENTRAL_BUDGET_RESERVATION")
        self.assertFalse(summary["dispatch_allowed"])
        self.assertTrue(summary["central_budget_reservation_required"])
        self.assertEqual(summary["receipt_authentication"], "REQUIRES_HMAC_AUTHENTICATED_PRIVATE_ARCHIVE_READBACK_AND_CENTRAL_LEDGER_ATTESTATIONS")
        self.assertTrue(summary["receipt_verification_keys_required_for_success"])
        self.assertFalse(summary["production_eligible"])
        self.assertFalse(summary["betting_eligible"])
        self.assertTrue(all(row["requires_central_budget_reservation"] for row in next_batch))

    def test_exact_receipt_completes_only_one_task_and_records_xg_quarantine(self):
        first = task()
        second = task("FS:101:league-teams:p1", endpoint="league-teams")
        second["expected_total_results"] = "20"
        second["expected_page_count"] = "1"
        second["max_per_page"] = "50"
        receipt = success_receipt(first)
        next_batch, statuses, summary = build_resume_plan([first, second], [receipt], 10)
        self.assertEqual(summary["completed_verified_private_archive_task_count"], 1)
        self.assertEqual(summary["pending_task_count"], 1)
        self.assertEqual(next_batch[0]["task_id"], second["task_id"])
        self.assertEqual(summary["xg_missing_field_counts"], {"fixture_level_xg_provenance": 1})
        self.assertEqual(statuses[0]["task_status"], "COMPLETE_VERIFIED_PRIVATE_ARCHIVE")

    def test_success_receipt_requires_both_independently_signed_attestations(self):
        t = task()
        receipt = success_receipt(t)
        next_batch, statuses, summary = build_resume_plan([t], [receipt], 10)
        self.assertEqual(statuses[0]["task_status"], "COMPLETE_VERIFIED_PRIVATE_ARCHIVE")
        self.assertEqual(summary["completed_verified_private_archive_task_count"], 1)

        legacy = success_receipt(t)
        legacy.pop("archive_verification")
        legacy.pop("budget_verification")
        _, statuses, summary = build_resume_plan([t], [legacy], 10)
        self.assertEqual(statuses[0]["task_status"], "BLOCKED_RECEIPT_VALIDATION")
        self.assertIn("missing authenticated private archive", statuses[0]["reason"])

        tampered_archive = success_receipt(t)
        tampered_archive["archive_verification"]["claims"]["archive_object_id"] = "attacker-object"
        _, statuses, _ = build_resume_plan([t], [tampered_archive], 10)
        self.assertEqual(statuses[0]["task_status"], "BLOCKED_RECEIPT_VALIDATION")
        self.assertIn("signature verification failed", statuses[0]["reason"])

        tampered_budget = success_receipt(t)
        tampered_budget["budget_verification"]["claims"]["request_event_id"] = "reused-event"
        _, statuses, _ = build_resume_plan([t], [tampered_budget], 10)
        self.assertEqual(statuses[0]["task_status"], "BLOCKED_RECEIPT_VALIDATION")
        self.assertIn("signature verification failed", statuses[0]["reason"])

        no_keys = checkpoint.build_resume_plan([t], [success_receipt(t)], 10, verification_keys={})
        self.assertEqual(no_keys[1][0]["task_status"], "BLOCKED_RECEIPT_VALIDATION")
        self.assertIn("verifier key is unavailable", no_keys[1][0]["reason"])

    def test_archive_signature_binds_response_metadata_and_payload_hashes(self):
        t = task()
        receipt = success_receipt(t)
        receipt["returned_rows"] = 599
        _, statuses, _ = build_resume_plan([t], [receipt], 10)
        self.assertEqual(statuses[0]["task_status"], "BLOCKED_RECEIPT_VALIDATION")
        self.assertIn("response metadata digest mismatch", statuses[0]["reason"])

    def test_receipt_requires_central_budget_and_private_archive_attestations(self):
        t = task()
        receipt = success_receipt(t, budget_ledger_attested=False)
        next_batch, statuses, summary = build_resume_plan([t], [receipt], 10)
        self.assertEqual(next_batch, [])
        self.assertEqual(summary["execution_gate"], "STOPPED_REQUIRES_OPERATOR_REVIEW")
        self.assertEqual(statuses[0]["task_status"], "BLOCKED_RECEIPT_VALIDATION")

        receipt = success_receipt(t, private_archive_write_verified=False)
        _, statuses, summary = build_resume_plan([t], [receipt], 10)
        self.assertEqual(statuses[0]["task_status"], "BLOCKED_RECEIPT_VALIDATION")
        self.assertEqual(summary["blocked_task_count"], 1)

    def test_short_page_is_blocked(self):
        t = task()
        receipt = success_receipt(t, returned_rows=599, unique_ids_on_page=599)
        next_batch, statuses, summary = build_resume_plan([t], [receipt], 10)
        self.assertEqual(next_batch, [])
        self.assertEqual(statuses[0]["task_status"], "BLOCKED_RECEIPT_VALIDATION")
        self.assertIn("page row count mismatch", statuses[0]["reason"])

    def test_429_failure_stops_batch_without_automatic_retry(self):
        t = task()
        next_batch, statuses, summary = build_resume_plan([t], [failure_receipt(t)], 10)
        self.assertEqual(next_batch, [])
        self.assertEqual(statuses[0]["task_status"], "BLOCKED_FAILURE")
        self.assertEqual(statuses[0]["reason"], "HTTP_429")
        self.assertEqual(summary["execution_gate"], "STOPPED_REQUIRES_OPERATOR_REVIEW")

    def test_conflicting_receipts_for_one_task_are_quarantined(self):
        t = task()
        first = success_receipt(t)
        second = success_receipt(t, payload_sha256="c" * 64)
        next_batch, statuses, summary = build_resume_plan([t], [first, second], 10)
        self.assertEqual(next_batch, [])
        self.assertEqual(statuses[0]["task_status"], "BLOCKED_RECEIPT_CONFLICT")
        self.assertEqual(summary["conflicting_receipt_task_count"], 1)

    def test_orphan_receipt_blocks_resume(self):
        t = task()
        orphan = success_receipt(t, task_id="NOT_IN_MANIFEST")
        next_batch, statuses, summary = build_resume_plan([t], [orphan], 10)
        self.assertEqual(next_batch, [])
        self.assertEqual(summary["orphan_receipt_count"], 1)
        self.assertEqual(summary["execution_gate"], "STOPPED_REQUIRES_OPERATOR_REVIEW")

    def test_raw_payload_fields_are_rejected(self):
        t = task()
        receipt = success_receipt(t, raw_payload={"private": "must-not-be-present"})
        next_batch, statuses, summary = build_resume_plan([t], [receipt], 10)
        self.assertEqual(next_batch, [])
        self.assertEqual(statuses[0]["task_status"], "BLOCKED_RECEIPT_VALIDATION")
        self.assertIn("raw field is prohibited", statuses[0]["reason"])

    def test_output_files_are_sanitized_and_research_only(self):
        t = task()
        next_batch, statuses, summary = build_resume_plan([t], [], 1)
        with tempfile.TemporaryDirectory() as directory:
            checkpoint.write_outputs(Path(directory), next_batch, statuses, summary)
            output = Path(directory)
            text = (output / "summary.json").read_text(encoding="utf-8")
            self.assertNotIn("payload_sha256", text)
            self.assertNotIn("private_archive_receipt_sha256", text)
            self.assertIn('"production_eligible": false', text)
            self.assertIn('"betting_eligible": false', text)
            self.assertTrue((output / "resume-plan.csv").is_file())
            self.assertTrue((output / "task-status.csv").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
