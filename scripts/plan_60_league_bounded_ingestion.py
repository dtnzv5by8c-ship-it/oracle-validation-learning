#!/usr/bin/env python3
"""Deterministic offline planner for bounded 60-league historical ingestion.

Consumes only an approved 60-league season manifest. It never calls a provider,
creates credentials, or admits data. The output is a sequence of bounded batches
that can be submitted to the private gateway only after its receipt contract passes.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

REQUIRED=("league_id","league_name","provider_league_id","provider_season_id",
          "season_start","season_end")
MAX_SEASONS_PER_BATCH=20

def plan(rows, expected_leagues=60, max_per_batch=MAX_SEASONS_PER_BATCH):
    errors=[]
    if len(rows)!=expected_leagues:
        errors.append(f"league_count={len(rows)} expected={expected_leagues}")
    seen=set()
    clean=[]
    for i,r in enumerate(rows,1):
        missing=[k for k in REQUIRED if not str(r.get(k,"")).strip()]
        if missing: errors.append(f"row{i}:missing_fields:{','.join(missing)}")
        sid=str(r.get("provider_season_id","")).strip()
        if sid and sid in seen: errors.append(f"row{i}:duplicate_provider_season_id:{sid}")
        if sid: seen.add(sid)
        clean.append({
            "league_id":str(r.get("league_id","")).strip(),
            "league_name":str(r.get("league_name","")).strip(),
            "provider_league_id":str(r.get("provider_league_id","")).strip(),
            "provider_season_id":sid,
            "season_start":str(r.get("season_start","")).strip(),
            "season_end":str(r.get("season_end","")).strip(),
        })
    if max_per_batch < 1: errors.append("max_per_batch_invalid")
    batches=[]
    if not errors:
        for n in range(0,len(clean),max_per_batch):
            chunk=clean[n:n+max_per_batch]
            batches.append({"batch_number":len(batches)+1,"season_count":len(chunk),
                            "provider_season_ids":[r["provider_season_id"] for r in chunk],
                            "leagues":[r["league_id"] for r in chunk]})
    return errors,batches

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",required=True); ap.add_argument("--out",required=True)
    ap.add_argument("--expected-leagues",type=int,default=60)
    ap.add_argument("--max-per-batch",type=int,default=MAX_SEASONS_PER_BATCH)
    a=ap.parse_args()
    with open(a.manifest,encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    errors,batches=plan(rows,a.expected_leagues,a.max_per_batch)
    result={"status":"PASS" if not errors else "BLOCK","expected_leagues":a.expected_leagues,
            "rows":len(rows),"batch_count":len(batches),"batches":batches,"errors":errors,
            "governance":{"provider_called":False,"gateway_receipt_created":False,
                          "oracle_v1_6_modified":False,"fail_closed":True}}
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if not errors else 2)

if __name__=="__main__":
    main()
