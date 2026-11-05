#!/usr/bin/env python3
"""Fail-closed private gateway receipt validator for Oracle historical ingestion.

This is a research/admission contract only. It never calls FootyStats, never reads
provider credentials, never publishes raw provider payloads, and never changes Oracle
V1.6. A receipt is admissible only when an approved private archive/gateway proves the
bounded batch identity, 60-league scope, 2024-current window, provider identity,
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
    "universe_name","expected_leagues","historical_start","historical_end",
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

def validate(receipt: dict, artifact: Path|None=None) -> list[str]:
    e=[]
    missing=sorted(REQUIRED-set(receipt))
    if missing: e.append("missing_fields:"+",".join(missing))
    if receipt.get("schema_version") != 1: e.append("schema_version_not_1")
    if receipt.get("provider") != "FootyStats": e.append("provider_not_footystats")
    if receipt.get("universe_name") != "Oracle-60-League": e.append("universe_not_60_league")
    if receipt.get("expected_leagues") != 60: e.append("expected_leagues_not_60")
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
            if verified_at.tzinfo is None: e.append("transport_verified_timestamp_not_utc")
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
    for k in ("requested_rows","received_rows","request_count"):
        try:
            if int(receipt.get(k,-1)) < 0: e.append(k+"_negative")
        except (TypeError,ValueError): e.append(k+"_invalid")
    if int(receipt.get("received_rows",0) or 0) > int(receipt.get("requested_rows",0) or 0):
        e.append("received_rows_exceeds_requested_rows")
    if int(receipt.get("requested_rows",0) or 0) <= 0: e.append("requested_rows_not_positive")
    if int(receipt.get("received_rows",0) or 0) <= 0: e.append("received_rows_not_positive")
    if int(receipt.get("request_count",0) or 0) <= 0: e.append("request_count_not_bounded_positive")
    elif int(receipt.get("request_count",0) or 0) > MAX_BOUNDED_REQUESTS:
        e.append("request_count_exceeds_bounded_limit")
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
