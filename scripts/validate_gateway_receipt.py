#!/usr/bin/env python3
"""Fail-closed validation for an approved private-provider gateway receipt."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

REQUIRED=("gateway_repo","workflow_run_id","governed_manifest_sha","archive_release_tag",
"archive_sha256","provider","provider_request_count","governed_league_count",
"history_start","history_end","raw_payloads_private_only","production_eligible",
"betting_eligible","status")
HEX64=re.compile(r"^[0-9a-f]{64}$",re.I)

def validate_receipt(r, expected_leagues=60):
    e=[]
    for k in REQUIRED:
        if k not in r or r.get(k) in (None,""): e.append(f"missing:{k}")
    if e: return e
    if r["provider"]!="FootyStats": e.append("provider_not_footystats")
    if r["gateway_repo"]!="dtnzv5by8c-ship-it/oracle-football-data": e.append("gateway_repo_not_approved_private_repo")
    if not str(r["workflow_run_id"]).isdigit() or int(r["workflow_run_id"])<=0: e.append("invalid_workflow_run_id")
    if not HEX64.match(str(r["archive_sha256"])): e.append("invalid_archive_sha256")
    if not str(r["archive_release_tag"]).startswith("research-") or not re.search(r"\d+$",str(r["archive_release_tag"])): e.append("invalid_archive_release_tag")
    try:
        if int(r["provider_request_count"])<=0: e.append("provider_request_count_not_positive")
        if int(r["governed_league_count"])!=expected_leagues: e.append(f"governed_league_count={r['governed_league_count']} expected={expected_leagues}")
    except (TypeError,ValueError): e.append("invalid_numeric_receipt_fields")
    if str(r["raw_payloads_private_only"]).lower()!="true": e.append("raw_payloads_not_private_only")
    if str(r["production_eligible"]).lower()!="false": e.append("production_must_remain_false")
    if str(r["betting_eligible"]).lower()!="false": e.append("betting_must_remain_false")
    if r["status"]!="GATEWAY_RECEIPT_VERIFIED": e.append("receipt_status_not_verified")
    if not str(r["history_start"]).startswith("2024-01-01"): e.append("history_start_not_2024")
    return e

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--receipt",required=True); ap.add_argument("--expected-leagues",type=int,default=60); ap.add_argument("--out",required=True)
    a=ap.parse_args()
    r=json.loads(Path(a.receipt).read_text(encoding="utf-8"))
    errors=validate_receipt(r,a.expected_leagues)
    out={"status":"PASS" if not errors else "BLOCK","errors":errors,"expected_leagues":a.expected_leagues,"production_eligible":False,"betting_eligible":False}
    Path(a.out).write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
    raise SystemExit(0 if not errors else 2)
if __name__=="__main__": main()
