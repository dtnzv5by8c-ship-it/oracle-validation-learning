#!/usr/bin/env python3
"""Offline contract validator for the sanitized Selected-50 FootyStats fixture snapshot."""
import argparse
import json
from collections import Counter
from pathlib import Path

def validate(path):
    d=json.loads(Path(path).read_text(encoding="utf-8"))
    errors=[]
    if d.get("diagnostic")!="BOUNDED_SELECTED50_CURRENT_FIXTURE_SNAPSHOT":
        errors.append("wrong diagnostic marker")
    for key,expected in (("selected_leagues",50),("requests_planned",50),("requests_attempted",50),("http_200_success",50),("request_failures",0)):
        if d.get(key)!=expected: errors.append(f"{key}: expected {expected}, got {d.get(key)!r}")
    if d.get("seasons_needing_pagination")!=[]: errors.append("one or more seasons require pagination")
    if d.get("production_eligibility")!="NOT_GRANTED" or d.get("betting_eligibility")!="NOT_GRANTED":
        errors.append("release eligibility must remain NOT_GRANTED")
    if d.get("raw_provider_payload_persisted") is not False: errors.append("raw provider payload must not be persisted")
    if d.get("api_key_persisted") is not False: errors.append("API key must not be persisted")
    if d.get("production_ledger_written") is not False: errors.append("production ledger must not be written")
    seasons=d.get("per_season")
    rows=d.get("fixture_rows")
    if not isinstance(seasons,list) or len(seasons)!=50: errors.append("per_season must contain exactly 50 rows")
    if not isinstance(rows,list): errors.append("fixture_rows must be a list"); rows=[]
    if isinstance(seasons,list):
        season_ids=[str(x.get("selected_season_id","")) for x in seasons]
        if len(set(season_ids))!=50: errors.append("selected season IDs are not unique")
        for x in seasons:
            if x.get("http_status")!=200 or x.get("provider_success") is not True:
                errors.append(f"provider request failed for season {x.get('selected_season_id')}")
            if x.get("schedule_status")!="ONE_PAGE_RESPONSE": errors.append(f"unexpected pagination state for season {x.get('selected_season_id')}")
    seen=set(); classes=Counter(); statuses=Counter(); no_home=0; missing_fields=Counter()
    for i,r in enumerate(rows):
        mid=str(r.get("id") or "")
        if not mid: errors.append(f"row {i}: missing match id")
        elif mid in seen: errors.append(f"duplicate match id {mid}")
        seen.add(mid)
        if str(r.get("competition_id") or "")!=str(r.get("selected_season_id") or ""):
            errors.append(f"row {i}: competition_id does not match selected season ID")
        for key in ("homeID","awayID","home_name","away_name","date_unix","kickoff_utc","status"):
            if r.get(key) in (None,""): missing_fields[key]+=1
        cls=r.get("window_class")
        if cls not in ("FUTURE_14D","RECENT_30D"): errors.append(f"row {i}: invalid window_class {cls!r}")
        classes[cls]+=1; statuses[str(r.get("status",""))]+=1
        if str(r.get("no_home_away","0"))=="1": no_home+=1
    future=sum(1 for r in rows if r.get("window_class")=="FUTURE_14D")
    recent_complete=sum(1 for r in rows if r.get("window_class")=="RECENT_30D" and str(r.get("status","")).lower()=="complete")
    if future!=d.get("future_14d_fixture_rows"): errors.append("future fixture count does not match summary")
    if recent_complete!=d.get("recent_completed_30d_rows"): errors.append("recent completed count does not match summary")
    if any(missing_fields.values()): errors.append("one or more fixture rows have missing required fields")
    return {
        "status":"PASS" if not errors else "FAIL",
        "errors":errors,
        "selected_seasons":len(seasons) if isinstance(seasons,list) else 0,
        "fixture_rows":len(rows),
        "future_14d_rows":future,
        "recent_completed_30d_rows":recent_complete,
        "no_home_away_rows":no_home,
        "duplicate_match_ids":len(rows)-len(seen),
        "status_counts":dict(statuses),
        "window_class_counts":dict(classes),
        "missing_required_field_counts":dict(missing_fields),
        "production_eligibility":d.get("production_eligibility"),
        "betting_eligibility":d.get("betting_eligibility")
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("snapshot_json")
    a=p.parse_args()
    result=validate(a.snapshot_json)
    print(json.dumps(result,indent=2,sort_keys=True))
    if result["status"]!="PASS": raise SystemExit(1)
if __name__=="__main__": main()
