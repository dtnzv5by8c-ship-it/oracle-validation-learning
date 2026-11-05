#!/usr/bin/env python3
"""Fail-closed admission check for the governed 60-league FootyStats registry.

This is an offline structural gate. It never calls FootyStats and never creates
or infers missing league identities. A registry with fewer than 60 unique
provider leagues is explicitly blocked.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

def validate_registry(payload, expected_leagues=60, min_history_year=2024):
    errors=[]
    if not isinstance(payload, dict):
        return ["registry_not_object"]
    declared=payload.get("provider_league_count")
    try:
        if int(declared) != expected_leagues:
            errors.append(f"declared_provider_league_count={declared} expected={expected_leagues}")
    except (TypeError,ValueError):
        errors.append("invalid_provider_league_count")
    seasons=payload.get("seasons")
    if not isinstance(seasons,list) or not seasons:
        errors.append("missing_seasons")
        return errors
    league_names={str(x.get("provider_league_name") or "").strip() for x in seasons
                  if isinstance(x,dict) and str(x.get("provider_league_name") or "").strip()}
    if len(league_names) != expected_leagues:
        errors.append(f"unique_provider_leagues={len(league_names)} expected={expected_leagues}")
    ids={str(x.get("provider_season_id") or "").strip() for x in seasons
         if isinstance(x,dict) and str(x.get("provider_season_id") or "").strip()}
    if len(ids) != sum(bool(str(x.get("provider_season_id") or "").strip()) for x in seasons if isinstance(x,dict)):
        errors.append("duplicate_or_blank_provider_season_id")
    historical_leagues=set()
    for x in seasons:
        if not isinstance(x,dict):
            errors.append("non_object_season_record")
            continue
        label=str(x.get("provider_season_label") or "").strip()
        if label and label[:4].isdigit() and int(label[:4]) >= min_history_year:
            name=str(x.get("provider_league_name") or "").strip()
            if name: historical_leagues.add(name)
    if len(historical_leagues) != expected_leagues:
        errors.append(f"2024_plus_leagues={len(historical_leagues)} expected={expected_leagues}")
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--registry",required=True)
    ap.add_argument("--expected-leagues",type=int,default=60)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    payload=json.loads(Path(a.registry).read_text(encoding="utf-8"))
    errors=validate_registry(payload,a.expected_leagues)
    result={"status":"PASS" if not errors else "BLOCK","expected_leagues":a.expected_leagues,
            "errors":errors,"production_eligible":False,"betting_eligible":False}
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if not errors else 2)

if __name__=="__main__":
    main()
