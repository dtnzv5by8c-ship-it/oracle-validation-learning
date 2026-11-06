#!/usr/bin/env python3
"""Deterministic offline planner for bounded 50-league historical ingestion.

Consumes only the governed 50-league season manifest. It never calls a provider,
creates credentials, or admits data. The output is a sequence of bounded batches
that can be submitted to the private gateway only after its receipt contract passes.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path

REQUIRED=("league_id","league_name","provider_league_id","provider_season_id",
          "season_start","season_end")
MAX_SEASONS_PER_BATCH=20

def plan(rows, expected_leagues=50, max_per_batch=MAX_SEASONS_PER_BATCH):
    errors=[]
    if len(rows)!=expected_leagues:
        errors.append(f"league_count={len(rows)} expected={expected_leagues}")
    seen_seasons=set(); seen_leagues=set(); clean=[]
    for i,r in enumerate(rows,1):
        missing=[k for k in REQUIRED if not str(r.get(k,"")).strip()]
        if missing: errors.append(f"row{i}:missing_fields:{','.join(missing)}")
        lid=str(r.get("league_id","")).strip()
        sid=str(r.get("provider_season_id","")).strip()
        if lid and lid in seen_leagues: errors.append(f"row{i}:duplicate_league_id:{lid}")
        if sid and sid in seen_seasons: errors.append(f"row{i}:duplicate_provider_season_id:{sid}")
        if lid: seen_leagues.add(lid)
        if sid: seen_seasons.add(sid)
        start=str(r.get("season_start","")).strip()
        end=str(r.get("season_end","")).strip().lower()
        if start[:4] != "2024": errors.append(f"row{i}:season_start_must_be_2024")
        if end != "current":
            try:
                if int(end[:4]) < 2024: errors.append(f"row{i}:season_end_before_2024")
            except ValueError: errors.append(f"row{i}:invalid_season_end")
        clean.append({"league_id":lid,"league_name":str(r.get("league_name","")).strip(),
                      "provider_league_id":str(r.get("provider_league_id","")).strip(),
                      "provider_season_id":sid,"season_start":start,"season_end":end})
    if max_per_batch < 1 or max_per_batch > MAX_SEASONS_PER_BATCH:
        errors.append(f"max_per_batch_must_be_1_to_{MAX_SEASONS_PER_BATCH}")
    batches=[]
    if not errors:
        for n in range(0,len(clean),max_per_batch):
            chunk=clean[n:n+max_per_batch]
            payload={"batch_number":len(batches)+1,"season_count":len(chunk),
                     "provider_season_ids":[r["provider_season_id"] for r in chunk],
                     "leagues":[r["league_id"] for r in chunk]}
            payload["batch_manifest_sha256"]=hashlib.sha256(
                json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
            ).hexdigest()
            batches.append(payload)
    return errors,batches

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",required=True); ap.add_argument("--out",required=True)
    ap.add_argument("--expected-leagues",type=int,default=50)
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
