#!/usr/bin/env python3
"""Fail-closed private gateway receipt validator for Oracle historical ingestion.

This is a research/admission contract only. It never calls FootyStats, never reads
provider credentials, never publishes raw provider payloads, and never changes Oracle
V1.6. A receipt is admissible only when an approved private archive/gateway proves the
bounded batch identity, 60-league scope, 2024-current window, provider identity,
immutable artifact digest, and safety controls.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

REQUIRED = {
    "schema_version","gateway_id","provider","archive_ref","archive_sha256",
    "universe_name","expected_leagues","historical_start","historical_end",
    "batch_id","requested_rows","received_rows","request_count",
    "raw_provider_payload_persisted_publicly","credentials_persisted_publicly",
    "production_eligible","betting_eligible","transport_status","auth_status",
    "rate_limit_status","receipt_status"
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
    if receipt.get("historical_end") not in ("current", None) and not str(receipt.get("historical_end","")).startswith("2026-"): e.append("historical_end_not_current")
    if not receipt.get("gateway_id"): e.append("gateway_id_missing")
    if not receipt.get("archive_ref"): e.append("archive_ref_missing")
    if not receipt.get("batch_id"): e.append("batch_id_missing")
    for k in ("requested_rows","received_rows","request_count"):
        try:
            if int(receipt.get(k,-1)) < 0: e.append(k+"_negative")
        except (TypeError,ValueError): e.append(k+"_invalid")
    if int(receipt.get("received_rows",0) or 0) > int(receipt.get("requested_rows",0) or 0):
        e.append("received_rows_exceeds_requested_rows")
    if int(receipt.get("request_count",0) or 0) <= 0: e.append("request_count_not_bounded_positive")
    if receipt.get("raw_provider_payload_persisted_publicly") is not False: e.append("raw_provider_payload_public_visibility_not_false")
    if receipt.get("credentials_persisted_publicly") is not False: e.append("credentials_public_visibility_not_false")
    if receipt.get("production_eligible") is not False: e.append("production_eligible_must_be_false")
    if receipt.get("betting_eligible") is not False: e.append("betting_eligible_must_be_false")
    if receipt.get("transport_status") != "PASS": e.append("transport_not_pass")
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
