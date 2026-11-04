#!/usr/bin/env python3
"""Offline, fail-closed resume planner for private FootyStats ingestion receipts.

This utility makes no network calls and never reads API credentials. It consumes
only the task manifest plus sanitized receipts that attest to a verified private
archive write. It emits a resumable task plan and sanitized coverage summary.
The central rolling-hour gateway must still reserve budget before any request.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import hashlib
import hmac
import os
from collections import Counter
from pathlib import Path
from typing import Any
from datetime import datetime, timezone

ENDPOINTS = {"league-matches", "league-teams", "league-tables", "league-season"}
PAGED_ENDPOINTS = {"league-matches", "league-teams"}
REQUIRED_FIELDS_BY_ENDPOINT = {
    "league-matches": {"id", "homeID", "awayID", "date_unix", "status"},
    "league-teams": {"id", "name_or_alias"},
    "league-tables": {
        "league_table", "all_matches_table_overall",
        "all_matches_table_home", "all_matches_table_away", "specific_tables",
    },
    "league-season": {"total_goals", "home_teams_goals", "away_teams_goals"},
}
FAILURE_CODES = {
    "HTTP_401", "HTTP_403", "HTTP_429", "PROVIDER_SUCCESS_FALSE",
    "TRANSPORT_FAILURE", "TRANSPORT_TIMEOUT", "MALFORMED_RESPONSE",
    "RESPONSE_VALIDATION_FAILED", "REQUIRED_FIELD_GAP",
    "PRIVATE_ARCHIVE_WRITE_FAILED", "PROVIDER_PLAN_LIMIT",
}
FORBIDDEN_KEYS = {
    "raw_payload", "response_body", "body", "api_key", "footystats_api_key",
    "authorization", "access_token", "secret", "token",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ARCHIVE_VERIFIER_ID = "oracle-private-archive-readback-verifier"
ARCHIVE_VERIFIER_KEY_ID = "private-archive-readback-v1"
BUDGET_VERIFIER_ID = "oracle-central-budget-ledger-verifier"
BUDGET_VERIFIER_KEY_ID = "central-budget-ledger-v1"
ARCHIVE_VERIFIER_KEY_ENV = "FOOTYSTATS_ARCHIVE_VERIFIER_HMAC_KEY"
BUDGET_VERIFIER_KEY_ENV = "FOOTYSTATS_BUDGET_VERIFIER_HMAC_KEY"
RESPONSE_METADATA_FIELDS = (
    "response_http_status", "provider_success", "response_shape_verified",
    "page_complete", "response_total_results", "response_page",
    "response_page_count", "returned_rows", "unique_ids_on_page",
    "required_fields_present", "required_fields_missing",
    "completed_match_rows", "completed_match_goal_field_gaps",
    "no_home_away_rows", "xg_fields_missing",
)
TASK_FIELDS = (
    "task_id", "provider", "provider_league_name", "provider_season_label",
    "provider_season_id", "endpoint", "page", "max_per_page",
    "expected_total_results", "expected_page_count", "raw_storage_required",
    "production_eligible", "betting_eligible",
)
STATUS_FIELDS = [
    "task_id", "provider_season_id", "endpoint", "page",
    "task_status", "reason", "production_eligible", "betting_eligible",
]
RESUME_FIELDS = [
    "task_id", "batch_id", "provider", "provider_league_name",
    "provider_season_label", "provider_season_id", "endpoint", "page",
    "max_per_page", "include", "max_time_unix", "expected_total_results",
    "expected_page_count", "task_status", "requires_central_budget_reservation",
    "raw_storage_required", "production_eligible", "betting_eligible",
]


def parse_utc(value: Any) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("request_timestamp_utc must be an explicit-offset ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("request_timestamp_utc must be an explicit-offset ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("request_timestamp_utc must include an explicit timezone")
    return parsed.astimezone(timezone.utc)


def parse_int(value: Any, field: str, minimum: int = 0) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be an integer")
    try:
        number = int(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{field} must be an integer") from exc
    if str(value).strip() not in {str(number), f"{number}.0"} or number < minimum:
        raise ValueError(f"{field} is outside its valid integer range")
    return number


def reject_sensitive_fields(value: Any, path: str = "receipt") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower()
            if normalized in FORBIDDEN_KEYS:
                raise ValueError(f"sensitive/raw field is prohibited in sanitized receipt: {path}.{key}")
            reject_sensitive_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_sensitive_fields(child, f"{path}[{index}]")


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not set(TASK_FIELDS).issubset(reader.fieldnames):
            raise ValueError("ingestion manifest is missing required task fields")
        tasks = list(reader)
    if not tasks:
        raise ValueError("ingestion manifest is empty")
    seen: set[str] = set()
    for task in tasks:
        task_id = str(task.get("task_id") or "").strip()
        if not task_id or task_id in seen:
            raise ValueError("manifest task IDs must be nonblank and unique")
        seen.add(task_id)
        if task.get("provider") != "FootyStats":
            raise ValueError("manifest contains a non-FootyStats task")
        if task.get("endpoint") not in ENDPOINTS:
            raise ValueError(f"unsupported manifest endpoint for task {task_id}")
        if str(task.get("raw_storage_required", "")).lower() not in {"true", "1"}:
            raise ValueError("every ingestion task must require protected private raw storage")
        if str(task.get("production_eligible", "")).lower() not in {"false", "0"}:
            raise ValueError("manifest task must remain production-ineligible")
        if str(task.get("betting_eligible", "")).lower() not in {"false", "0"}:
            raise ValueError("manifest task must remain betting-ineligible")
        page = parse_int(task.get("page"), "manifest.page", 1)
        page_count = parse_int(task.get("expected_page_count"), "manifest.expected_page_count", 1)
        if page > page_count:
            raise ValueError(f"manifest page exceeds expected page count for task {task_id}")
        if task["endpoint"] not in PAGED_ENDPOINTS and (page != 1 or page_count != 1):
            raise ValueError(f"single-response endpoint has invalid page metadata for task {task_id}")
        if task["endpoint"] in PAGED_ENDPOINTS:
            parse_int(task.get("max_per_page"), "manifest.max_per_page", 1)
            parse_int(task.get("expected_total_results"), "manifest.expected_total_results", 0)
        expected_task_id = f"FS:{task['provider_season_id']}:{task['endpoint']}:p{page}"
        if task_id != expected_task_id:
            raise ValueError(f"manifest task ID does not match exact provider season/endpoint/page: {task_id}")
    return tasks


def read_receipts(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ValueError("sanitized private-archive receipt JSONL file is missing")
    receipts: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                receipt = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid receipt JSON on line {line_number}") from exc
            if not isinstance(receipt, dict):
                raise ValueError(f"receipt line {line_number} must contain an object")
            reject_sensitive_fields(receipt)
            receipts.append(receipt)
    return receipts


def receipt_signature(receipt: dict[str, Any]) -> str:
    return json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def response_metadata_digest(receipt: dict[str, Any]) -> str:
    metadata = {field: receipt.get(field) for field in RESPONSE_METADATA_FIELDS}
    return hashlib.sha256(canonical_json_bytes(metadata)).hexdigest()


def load_verification_keys_from_env() -> dict[str, bytes]:
    """Load protected verifier keys; no key material is logged or written to outputs."""
    values = {
        "archive": os.environ.get(ARCHIVE_VERIFIER_KEY_ENV, ""),
        "budget": os.environ.get(BUDGET_VERIFIER_KEY_ENV, ""),
    }
    keys: dict[str, bytes] = {}
    for name, value in values.items():
        if value:
            key = value.encode("utf-8")
            if len(key) < 32:
                raise ValueError(f"{name} verifier HMAC key must contain at least 32 UTF-8 bytes")
            keys[name] = key
    return keys


def verify_signed_attestation(
    attestation: Any,
    key: bytes | None,
    expected_signer: str,
    expected_key_id: str,
    label: str,
) -> dict[str, Any]:
    if not isinstance(attestation, dict):
        raise ValueError(f"missing authenticated {label} attestation")
    if not isinstance(key, bytes) or len(key) < 32:
        raise ValueError(f"trusted {label} verifier key is unavailable")
    if attestation.get("algorithm") != "HMAC-SHA256":
        raise ValueError(f"{label} attestation must use HMAC-SHA256")
    if attestation.get("signer_id") != expected_signer or attestation.get("key_id") != expected_key_id:
        raise ValueError(f"{label} attestation signer/key ID is not trusted")
    claims = attestation.get("claims")
    signature = attestation.get("signature_hex")
    if not isinstance(claims, dict) or not isinstance(signature, str) or not SHA256_RE.fullmatch(signature):
        raise ValueError(f"{label} attestation claims/signature are malformed")
    expected = hmac.new(key, canonical_json_bytes(claims), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise ValueError(f"{label} attestation signature verification failed")
    return claims


def validate_receipt(
    task: dict[str, str], receipt: dict[str, Any],
    verification_keys: dict[str, bytes] | None = None,
) -> tuple[str, str, list[str]]:
    """Return task status, reason and xG-missing fields without exposing hashes."""
    reject_sensitive_fields(receipt)
    expected_identity = {
        "task_id": str(task["task_id"]),
        "provider": "FootyStats",
        "provider_season_id": str(task["provider_season_id"]),
        "endpoint": str(task["endpoint"]),
        "page": parse_int(task["page"], "manifest.page", 1),
    }
    for key, expected in expected_identity.items():
        actual = receipt.get(key)
        if key == "page":
            actual = parse_int(actual, "receipt.page", 1)
        if actual != expected:
            raise ValueError(f"receipt exact identity mismatch for {key}")
    parse_utc(receipt.get("request_timestamp_utc"))

    status = str(receipt.get("status") or "").upper()
    if status == "FAILED":
        code = str(receipt.get("failure_code") or "")
        if code not in FAILURE_CODES:
            raise ValueError("failure receipt has an unsupported failure_code")
        return "BLOCKED_FAILURE", code, []
    if status != "SUCCESS":
        raise ValueError("receipt status must be SUCCESS or FAILED")

    keys = verification_keys if verification_keys is not None else load_verification_keys_from_env()
    archive_claims = verify_signed_attestation(
        receipt.get("archive_verification"), keys.get("archive"),
        ARCHIVE_VERIFIER_ID, ARCHIVE_VERIFIER_KEY_ID, "private archive read-back",
    )
    budget_claims = verify_signed_attestation(
        receipt.get("budget_verification"), keys.get("budget"),
        BUDGET_VERIFIER_ID, BUDGET_VERIFIER_KEY_ID, "central budget ledger",
    )
    for key, expected in expected_identity.items():
        archive_actual = archive_claims.get(key)
        budget_actual = budget_claims.get(key)
        if key == "page":
            archive_actual = parse_int(archive_actual, "archive_verification.page", 1)
            budget_actual = parse_int(budget_actual, "budget_verification.page", 1)
        if archive_actual != expected or budget_actual != expected:
            raise ValueError(f"authenticated attestation exact task identity mismatch for {key}")

    if archive_claims.get("payload_sha256") != receipt.get("payload_sha256"):
        raise ValueError("archive verifier payload hash does not match receipt payload hash")
    if archive_claims.get("archive_receipt_sha256") != receipt.get("private_archive_receipt_sha256"):
        raise ValueError("archive verifier receipt hash does not match private archive receipt hash")
    if archive_claims.get("archive_object_bytes_hash_verified") is not True:
        raise ValueError("archive verifier did not independently verify archived object bytes")
    if archive_claims.get("archive_receipt_bytes_hash_verified") is not True:
        raise ValueError("archive verifier did not independently verify archive receipt bytes")
    if archive_claims.get("writer_receipt_signature_verified") is not True:
        raise ValueError("archive verifier did not authenticate the private writer receipt")
    if archive_claims.get("private_visibility_verified") is not True:
        raise ValueError("archive object private visibility was not verified")
    if archive_claims.get("private_archive_write_verified") is not True or archive_claims.get("raw_payload_stored_privately") is not True:
        raise ValueError("archive verifier did not confirm a private raw-payload write")
    if archive_claims.get("public_raw_payload_written") is not False:
        raise ValueError("archive verifier did not confirm public raw-payload prohibition")
    if not str(archive_claims.get("archive_object_id") or "").strip():
        raise ValueError("archive verifier receipt lacks a private object identifier")
    if not str(archive_claims.get("archive_object_version_id") or "").strip():
        raise ValueError("archive verifier receipt lacks an immutable object version")
    if not str(archive_claims.get("archive_receipt_object_id") or "").strip():
        raise ValueError("archive verifier receipt lacks a private receipt object identifier")
    parse_int(archive_claims.get("archive_object_size_bytes"), "archive_verification.archive_object_size_bytes", 1)
    parse_utc(archive_claims.get("verified_at_utc"))
    if archive_claims.get("response_metadata_sha256") != response_metadata_digest(receipt):
        raise ValueError("archive-signed response metadata digest mismatch")

    if budget_claims.get("reservation_id") != receipt.get("budget_reservation_id"):
        raise ValueError("budget verifier reservation ID does not match receipt")
    if not str(budget_claims.get("ledger_entry_id") or "").strip():
        raise ValueError("budget verifier receipt lacks a resolved ledger entry ID")
    if not str(budget_claims.get("request_event_id") or "").strip():
        raise ValueError("budget verifier receipt lacks a unique request event ID")
    if parse_int(budget_claims.get("request_count"), "budget_verification.request_count", 1) != 1:
        raise ValueError("each task receipt must resolve to exactly one provider request event")
    if budget_claims.get("request_timestamp_utc") != receipt.get("request_timestamp_utc"):
        raise ValueError("budget verifier request timestamp does not match receipt")
    if budget_claims.get("hard_limit") != 1800:
        raise ValueError("budget verifier did not attest the hard 1800-request rolling-hour ceiling")
    if budget_claims.get("hard_limit") != receipt.get("global_rolling_hour_limit"):
        raise ValueError("signed budget hard limit does not match receipt")
    operational_limit = parse_int(budget_claims.get("operational_limit"), "budget_verification.operational_limit", 1)
    if operational_limit > 1500:
        raise ValueError("budget verifier operational limit exceeds 1,500 requests")
    if parse_int(budget_claims.get("reserved_headroom"), "budget_verification.reserved_headroom", 300) < 300:
        raise ValueError("budget verifier did not preserve 300 requests of headroom")
    if parse_int(budget_claims.get("rolling_60m_request_count_after"), "budget_verification.rolling_60m_request_count_after", 0) > operational_limit:
        raise ValueError("budget verifier reports the rolling-hour operational limit was exceeded")
    if budget_claims.get("provider_limit_enforced") is not True:
        raise ValueError("budget verifier did not attest enforcement of lower provider limits")
    if budget_claims.get("ledger_record_resolved") is not True or budget_claims.get("request_event_resolved") is not True:
        raise ValueError("budget verifier did not resolve the authoritative ledger and request event")
    parse_utc(budget_claims.get("verified_at_utc"))

    if receipt.get("response_http_status") != 200:
        raise ValueError("successful receipt must have HTTP 200")
    if receipt.get("provider_success") is not True:
        raise ValueError("successful receipt must explicitly attest provider success")
    if receipt.get("response_shape_verified") is not True:
        raise ValueError("successful receipt must attest verified response shape")
    if receipt.get("page_complete") is not True:
        raise ValueError("successful receipt must attest a complete response page")
    if receipt.get("request_gateway") != "central_footystats_gateway":
        raise ValueError("successful receipt must attest use of the central FootyStats gateway")
    if not str(receipt.get("budget_reservation_id") or "").strip():
        raise ValueError("successful receipt lacks the central budget reservation ID")
    if receipt.get("budget_ledger_attested") is not True:
        raise ValueError("successful receipt lacks durable rolling-ledger attestation")
    if budget_claims.get("reserved_headroom") != receipt.get("reserved_headroom"):
        raise ValueError("signed budget headroom does not match receipt")
    if receipt.get("global_rolling_hour_limit") != 1800:
        raise ValueError("successful receipt must attest the hard 1800-request rolling-hour ceiling")
    headroom = receipt.get("reserved_headroom")
    if isinstance(headroom, bool) or not isinstance(headroom, int) or headroom < 300:
        raise ValueError("successful receipt must attest at least 300 requests of headroom")
    if receipt.get("private_archive_write_verified") is not True:
        raise ValueError("successful receipt lacks verified private archive write")
    if receipt.get("raw_payload_stored_privately") is not True:
        raise ValueError("successful receipt does not attest private raw payload storage")
    if receipt.get("public_raw_payload_written") is not False:
        raise ValueError("public raw payload writes are prohibited")
    for field in ("payload_sha256", "private_archive_receipt_sha256"):
        value = receipt.get(field)
        if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
            raise ValueError(f"{field} must be a lowercase SHA-256 digest")
    missing = receipt.get("required_fields_missing")
    if not isinstance(missing, list):
        raise ValueError("required_fields_missing must be an explicit list")
    if missing:
        raise ValueError("REQUIRED_FIELD_GAP:" + ";".join(str(x) for x in missing))
    present = receipt.get("required_fields_present")
    if not isinstance(present, list):
        raise ValueError("required_fields_present must be an explicit list")
    required_fields = REQUIRED_FIELDS_BY_ENDPOINT[task["endpoint"]]
    if not required_fields.issubset({str(field) for field in present}):
        absent = sorted(required_fields - {str(field) for field in present})
        raise ValueError("REQUIRED_FIELD_PRESENCE_UNVERIFIED:" + ";".join(absent))

    if task["endpoint"] == "league-matches":
        completed_rows = parse_int(receipt.get("completed_match_rows"), "receipt.completed_match_rows", 0)
        goal_gaps = parse_int(receipt.get("completed_match_goal_field_gaps"), "receipt.completed_match_goal_field_gaps", 0)
        if goal_gaps > 0:
            raise ValueError("COMPLETED_MATCH_GOAL_FIELD_GAP")
        if completed_rows > 0:
            goal_fields = {"homeGoalCount", "awayGoalCount", "totalGoalCount"}
            if not goal_fields.issubset({str(field) for field in present}):
                raise ValueError("COMPLETED_MATCH_GOAL_FIELDS_UNVERIFIED")
        no_home_away_rows = parse_int(receipt.get("no_home_away_rows"), "receipt.no_home_away_rows", 0)
        if no_home_away_rows > parse_int(receipt.get("returned_rows"), "receipt.returned_rows", 0):
            raise ValueError("no_home_away_rows exceeds returned page rows")

    if task["endpoint"] in PAGED_ENDPOINTS:
        total = parse_int(task.get("expected_total_results"), "manifest.expected_total_results", 0)
        per_page = parse_int(task.get("max_per_page"), "manifest.max_per_page", 1)
        page = parse_int(task.get("page"), "manifest.page", 1)
        page_count = parse_int(task.get("expected_page_count"), "manifest.expected_page_count", 1)
        if parse_int(receipt.get("response_total_results"), "receipt.response_total_results", 0) != total:
            raise ValueError("provider total_results differs from the manifest")
        if parse_int(receipt.get("response_page"), "receipt.response_page", 1) != page:
            raise ValueError("provider response page differs from the manifest")
        if parse_int(receipt.get("response_page_count"), "receipt.response_page_count", 1) != page_count:
            raise ValueError("provider page count differs from the manifest")
        returned = parse_int(receipt.get("returned_rows"), "receipt.returned_rows", 0)
        expected_rows = min(per_page, max(0, total - ((page - 1) * per_page)))
        if returned != expected_rows:
            raise ValueError(f"page row count mismatch: expected {expected_rows}, received {returned}")
        unique_ids = parse_int(receipt.get("unique_ids_on_page"), "receipt.unique_ids_on_page", 0)
        if unique_ids != returned:
            raise ValueError("provider IDs are not unique on the returned page")

    xg_missing = receipt.get("xg_fields_missing")
    if not isinstance(xg_missing, list):
        raise ValueError("xg_fields_missing must be an explicit list; xG remains quarantined without provenance")
    return "COMPLETE_VERIFIED_PRIVATE_ARCHIVE", "EXACT_TASK_AND_PRIVATE_ARCHIVE_RECEIPT_VERIFIED", [
        str(field) for field in xg_missing
    ]


def build_resume_plan(
    tasks: list[dict[str, str]],
    receipts: list[dict[str, Any]],
    max_batch_requests: int,
    verification_keys: dict[str, bytes] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    if isinstance(max_batch_requests, bool) or not isinstance(max_batch_requests, int) or not 1 <= max_batch_requests <= 1500:
        raise ValueError("max_batch_requests must be between 1 and 1500")

    task_by_id = {str(task["task_id"]): task for task in tasks}
    receipts_by_id: dict[str, list[dict[str, Any]]] = {}
    orphan_receipts = 0
    for receipt in receipts:
        task_id = str(receipt.get("task_id") or "").strip()
        if task_id not in task_by_id:
            orphan_receipts += 1
            continue
        receipts_by_id.setdefault(task_id, []).append(receipt)

    status_rows: list[dict[str, Any]] = []
    completed = 0
    blocked = 0
    pending: list[dict[str, str]] = []
    duplicate_receipts = 0
    receipt_conflicts = 0
    xg_missing_counts: Counter[str] = Counter()
    no_home_away_rows_total = 0
    completed_match_rows_total = 0
    completed_match_goal_gap_rows_total = 0

    for task in tasks:
        task_id = str(task["task_id"])
        task_receipts = receipts_by_id.get(task_id, [])
        task_status = "PENDING"
        reason = "NO_VERIFIED_RECEIPT"
        if task_receipts:
            signatures = {receipt_signature(item) for item in task_receipts}
            if len(signatures) > 1:
                task_status = "BLOCKED_RECEIPT_CONFLICT"
                reason = "MULTIPLE_NONIDENTICAL_RECEIPTS_FOR_TASK"
                receipt_conflicts += 1
            else:
                duplicate_receipts += max(0, len(task_receipts) - 1)
                try:
                    task_status, reason, xg_missing = validate_receipt(task, task_receipts[0], verification_keys)
                    xg_missing_counts.update(xg_missing)
                    if task_status == "COMPLETE_VERIFIED_PRIVATE_ARCHIVE" and task["endpoint"] == "league-matches":
                        no_home_away_rows_total += int(task_receipts[0]["no_home_away_rows"])
                        completed_match_rows_total += int(task_receipts[0]["completed_match_rows"])
                        completed_match_goal_gap_rows_total += int(task_receipts[0]["completed_match_goal_field_gaps"])
                except ValueError as exc:
                    task_status = "BLOCKED_RECEIPT_VALIDATION"
                    reason = str(exc)
        if task_status == "COMPLETE_VERIFIED_PRIVATE_ARCHIVE":
            completed += 1
        elif task_status.startswith("BLOCKED"):
            blocked += 1
        else:
            pending.append(task)
        status_rows.append({
            "task_id": task_id,
            "provider_season_id": task["provider_season_id"],
            "endpoint": task["endpoint"],
            "page": task["page"],
            "task_status": task_status,
            "reason": reason,
            "production_eligible": False,
            "betting_eligible": False,
        })

    if orphan_receipts:
        blocked += orphan_receipts
    gate_blocked = blocked > 0
    next_batch = []
    if not gate_blocked:
        for task in pending[:max_batch_requests]:
            next_batch.append({
                **task,
                "task_status": "PENDING_REQUIRES_CENTRAL_BUDGET_RESERVATION",
                "requires_central_budget_reservation": True,
                "production_eligible": False,
                "betting_eligible": False,
            })

    summary = {
        "schema_version": "1.0",
        "diagnostic": "FOOTYSTATS_RESUMABLE_INGESTION_CHECKPOINT",
        "planned_task_count": len(tasks),
        "completed_verified_private_archive_task_count": completed,
        "pending_task_count": len(pending),
        "blocked_task_count": blocked,
        "orphan_receipt_count": orphan_receipts,
        "duplicate_identical_receipt_count": duplicate_receipts,
        "conflicting_receipt_task_count": receipt_conflicts,
        "next_batch_task_count": len(next_batch),
        "execution_gate": "STOPPED_REQUIRES_OPERATOR_REVIEW" if gate_blocked else "READY_FOR_CENTRAL_BUDGET_RESERVATION",
        "dispatch_allowed": False,
        "receipt_authentication": "REQUIRES_HMAC_AUTHENTICATED_PRIVATE_ARCHIVE_READBACK_AND_CENTRAL_LEDGER_ATTESTATIONS",
        "receipt_verification_keys_required_for_success": True,
        "central_budget_reservation_required": True,
        "private_raw_archive_write_required": True,
        "raw_payloads_written_to_public_repository": False,
        "xg_missing_field_counts": dict(sorted(xg_missing_counts.items())),
        "no_home_away_rows_in_completed_receipts": no_home_away_rows_total,
        "completed_match_rows_in_completed_receipts": completed_match_rows_total,
        "completed_match_goal_field_gap_rows": completed_match_goal_gap_rows_total,
        "h2h_status": "DERIVE_ONLY_FROM_EXACT_CHRONOLOGICAL_MATCH_SPINE",
        "recent_form_status": "DERIVE_ONLY_WITH_STRICT_PRE_KICKOFF_CUTOFF",
        "home_away_form_status": "DERIVE_ONLY_FROM_EXACT_ORDERED_HOME_AWAY_IDS; NO_HOME_AWAY_ROWS_EXCLUDED",
        "fixture_time_standings_status": "NOT_VERIFIED_REQUIRES_AS_OF_RECONSTRUCTION",
        "xg_usage_status": "QUARANTINED_NO_POINT_IN_TIME_CAPTURE_AND_REVISION_PROVENANCE",
        "full_history_ingested": False,
        "production_eligible": False,
        "betting_eligible": False,
    }
    return next_batch, status_rows, summary


def write_outputs(output_dir: Path, next_batch: list[dict[str, Any]], status_rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, rows, fields in (
        ("resume-plan.csv", next_batch, RESUME_FIELDS),
        ("task-status.csv", status_rows, STATUS_FIELDS),
    ):
        temp = output_dir / (filename + ".tmp")
        with temp.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
        temp.replace(output_dir / filename)
    temp_json = output_dir / "summary.json.tmp"
    temp_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp_json.replace(output_dir / "summary.json")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--receipts-jsonl", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-batch-requests", type=int, default=500)
    args = parser.parse_args()
    tasks = read_manifest(Path(args.manifest))
    receipts = read_receipts(Path(args.receipts_jsonl))
    next_batch, status_rows, summary = build_resume_plan(
        tasks, receipts, args.max_batch_requests, load_verification_keys_from_env()
    )
    write_outputs(Path(args.output_dir), next_batch, status_rows, summary)
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["execution_gate"] != "STOPPED_REQUIRES_OPERATOR_REVIEW" else 2


if __name__ == "__main__":
    raise SystemExit(main())
