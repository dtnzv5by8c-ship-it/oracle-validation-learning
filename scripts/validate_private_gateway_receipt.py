#!/usr/bin/env python3
"""Fail-closed private gateway receipt validator for Oracle historical ingestion.

This is a research/admission contract only. It never calls FootyStats, never reads
provider credentials, never publishes raw provider payloads, and never changes Oracle
V1.6. A receipt is admissible only when an approved private archive/gateway proves the
bounded batch identity, 50-league scope, 2024-current window, provider identity,
immutable artifact digest, recent transport verification, and safety controls.
"""
from __future__ import annotations
import argparse, hashlib, json
from datetime import date, datetime, timezone, timedelta
from pathlib import Path

MAX_BOUNDED_REQUESTS = 100
MAX_TRANSPORT_PROOF_AGE = timedelta(hours=24)

REQUIRED = {
    "schema_version","gateway_id","provider","archive_ref","archive_sha256",
    "universe_name","undefined","historical_start","historical_end",
    "batch_id","requested_rows","received_rows","request_count",
    "raw_provider_payload_persisted_publicly","credentials_persisted_publicly",
    "production_eligible","betting_eligible","transport_status","auth_status",
    "rate_limit_status","receipt_status","transport_mode","transport_evidence_ref",
    "transport_verified_at_utc"
}

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def _nonnegative_int(receipt: dict, key: str, errors: list[str]) -> int | None:
    raw = receipt.get(key, None)
    # JSON booleans are integers in Python; reject them explicitly. Also reject
    # floats/strings that merely coerce to integers so receipt counts stay exact.
    if isinstance(raw, bool) or not isinstance(raw, (int, str)):
        errors.append(key + "_invalid")
        return None
    if isinstance(raw, str):
        try:
            canonical = str(int(raw.strip()))
        except (TypeError, ValueError):
            errors.append(key + "_invalid")
            return None
        if not raw.strip() or raw.strip() != canonical:
            errors.append(key + "_invalid")
            return None
    value = int(raw)
    if value < 0:
        errors.append(key + "_negative")
    return value

def validate(receipt: dict, artifact: Path|None=None) -> list[str]:
    e=[]
    missing=sorted(REQUIRED-set(receipt))
    if missing: e.append("missing_fields:"+",".join(missing))
    if receipt.get("schema_version") != 1: e.append("schema_version_not_1")
    if receipt.get("provider") != "FootyStats": e.append("provider_not_footystats")
    if receipt.get("universe_name") != "Oracle-50-League": e.append("universe_not_60_league")
    if receipt.get("expected_leagues") != 50: e.append("expected_leagues_not_50")
    if str(receipt.get("historical_start")) != "2024-01-01": e.append("historical_start_not_2024")
    historical_end = str(receipt.get("historical_end") or "").strip()
    if historical_end != "current":
        try:
            end_date = date.fromisoformat(historical_end)
            start_date = date.fromisoformat("2024-01-01")
            today = datetime.now(timezone.utc).date()
            if end_date < start_date or end_date > today:
                e.append("historical_end_out_of_range")
        except ValueError:
            e.append("historical_end_invalid")
    verified_raw = str(receipt.get("transport_verified_at_utc") or "").strip()
    verified_at = None
    if verified_raw:
        try:
            verified_at = datetime.fromisoformat(verified_raw.replace("Z","+00:00"))
            if verified_at.tzinfo is None or verified_at.utcoffset() != timedelta(0): e.append("transport_verified_timestamp_not_utc")
            else:
                now = datetime.now(timezone.utc)
                if verified_at > now + timedelta(minutes=5): e.append("transport_verified_timestamp_in_future")
                elif now - verified_at > MAX_TRANSPORT_PROOF_AGE: e.append("transport_proof_stale")
        except ValueError:
            e.append("transport_verified_timestamp_invalid")
    if not str(receipt.get("gateway_id") or "").startswith("approved-private-gateway"):
        e.append("gateway_id_not_approved")
    archive_ref = str(receipt.get("archive_ref") or "").strip()
    if not archive_ref.startswith("private://"):
        e.append("archive_ref_not_private")
    if not receipt.get("batch_id"): e.append("batch_id_missing")
    requested_rows = _nonnegative_int(receipt, "requested_rows", e)
    received_rows = _nonnegative_int(receipt, "received_rows", e)
    request_count = _nonnegative_int(receipt, "request_count", e)
    if requested_rows is not None and received_rows is not None and received_rows > requested_rows:
        e.append("received_rows_exceeds_requested_rows")
    if requested_rows is not None and requested_rows <= 0: e.append("requested_rows_not_positive")
    if received_rows is not None and received_rows <= 0: e.append("received_rows_not_positive")
    if request_count is not None:
        if request_count <= 0: e.append("request_count_not_bounded_positive")
        elif request_count > MAX_BOUNDED_REQUESTS: e.append("request_count_exceeds_bounded_limit")
    if receipt.get("raw_provider_payload_persisted_publicly") is not False: e.append("raw_provider_payload_public_visibility_not_false")
    if receipt.get("credentials_persisted_publicly") is not False: e.append("credentials_public_visibility_not_false")
    if receipt.get("production_eligible") is not False: e.append("production_eligible_must_be_false")
    if receipt.get("betting_eligible") is not False: e.append("betting_eligible_must_be_false")
    if receipt.get("transport_status") != "PASS": e.append("transport_not_pass")
    if receipt.get("transport_mode") not in {"controlled_gateway","private_archive","private_mirror"}: e.append("transport_mode_not_approved")
    if not str(receipt.get("transport_evidence_ref") or "").startswith("private://"): e.append("transport_evidence_ref_not_private")
    if receipt.get("auth_status") != "PASS": e.append("auth_not_pass")
    if receipt.get("rate_limit_status") != "PASS": e.append("rate_limit_not_pass")
    if receipt.get("receipt_status") != "VERIFIED_PRIVATE_ARCHIVE": e.append("receipt_status_not_verified")
    digest=str(receipt.get("archive_sha256","")).lower()
    if len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest): e.append("archive_sha256_invalid")
    if artifact is not None:
        if not artifact.is_file(): e.append("archive_artifact_missing")
        elif digest != sha256(artifact).lower(): e.append("archive_sha256_mismatch")
    return e

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--receipt",required=True)
    ap.add_argument("--artifact")
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    receipt=json.loads(Path(a.receipt).read_text(encoding="utf-8"))
    errors=validate(receipt,Path(a.artifact) if a.artifact else None)
    result={"status":"PASS" if not errors else "BLOCK","errors":errors,
            "governance":{"oracle_v1_6_modified":False,"provider_called":False,
                          "raw_provider_data_public":False,"production_eligible":False,
                          "betting_eligible":False,"fail_closed":True}}
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if not errors else 2)

if __name__=="__main__":
    main()
