import importlib.util
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "receipt_validator", Path(__file__).parents[1] / "scripts" / "validate_private_gateway_receipt.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

BASE = {
    "schema_version": 1, "gateway_id": "approved-private-gateway-60",
    "provider": "FootyStats", "archive_ref": "private://oracle/archive",
    "archive_sha256": "a" * 64, "universe_name": "Oracle-60-League",
    "expected_leagues": 60, "historical_start": "2024-01-01",
    "historical_end": "current", "batch_id": "batch-001",
    "requested_rows": 10, "received_rows": 10, "request_count": 1,
    "raw_provider_payload_persisted_publicly": False,
    "credentials_persisted_publicly": False, "production_eligible": False,
    "betting_eligible": False, "transport_status": "PASS",
    "auth_status": "PASS", "rate_limit_status": "PASS",
    "receipt_status": "VERIFIED_PRIVATE_ARCHIVE",
    "transport_mode": "private_archive",
    "transport_evidence_ref": "private://oracle/transport",
    "transport_verified_at_utc": "2026-11-06T02:00:00Z",
}

def check(name, receipt, expected_error):
    errors = MOD.validate(receipt)
    assert expected_error in errors, f"{name}: expected {expected_error}, got {errors}"

check("bool request_count", {**BASE, "request_count": True}, "request_count_invalid")
check("float requested_rows", {**BASE, "requested_rows": 10.0}, "requested_rows_invalid")
check("noncanonical string", {**BASE, "received_rows": "010"}, "received_rows_invalid")
check("decimal string", {**BASE, "request_count": "1.0"}, "request_count_invalid")

# Canonical integer strings remain admissible by this low-level contract.
assert MOD.validate({**BASE, "requested_rows": "10"}) == []
assert MOD.validate({**BASE, "received_rows": "10", "request_count": "1"}) == []
print("PASS: private gateway receipt counters are exact and fail closed.")
