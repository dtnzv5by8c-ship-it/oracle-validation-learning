#!/usr/bin/env python3
"""Research-only OMI readiness validator for the governed multi-league universe.

This validator does not calculate Oracle probabilities and never mutates production
logic. It validates identity joins, chronology, field coverage, settlement truth and
freshness for an OMI input dataset once upstream evidence has been admitted.
"""
from __future__ import annotations
import argparse,csv,json
from datetime import datetime,timezone
from pathlib import Path

REQUIRED = [
    "Fixture Date","League","Fixture","Fixture ID","Provider Season ID",
    "Home Team ID","Away Team ID","History Cutoff UTC",
    "Recent Form (5)","League Position","H2H Last-5",
    "Home Expected Goals Lambda","Away Expected Goals Lambda",
    "Research Over 1,5 %","Research Over 2,5 %",
    "BTTS Yes","actual_home_goals","actual_away_goals",
    "actual_total_goals","actual_match_result","settlement_status",
    "Production Eligible","Betting Eligible","retrieved_utc"
]
PROBABILITY_FIELDS = [
    "BTTS Yes","Home 1X","Away X2","Over 1.5","Over 2.5","Under 4.5",
    "Home over 1.5 goals","Away over 1.5 goals","Home 1X + Over 1.5",
    "Away X2 + Over 1.5","Home 1X + Under 4.5","Away X2 + Under 4.5",
    "M-1UP Home","M-1UP Away","Draw Probability (derived)",
    "Research Over 1,5 %","Research Over 2,5 %","Research Under 4,5 %",
    "Research Home Over 1,5 %","Research Away Over 1,5 %"
]

def dt(v):
    try:
        x=datetime.fromisoformat(str(v).replace("Z","+00:00"))
        return x.astimezone(timezone.utc) if x.tzinfo else None
    except (TypeError,ValueError):
        return None

def num(v):
    try:
        x=float(str(v).strip())
        return x if 0 <= x <= 100 else None
    except (TypeError,ValueError):
        return None

def validate_manifest(rows, expected_universe=60):
    ids=[str(r.get("league_id") or r.get("selected_id") or "").strip() for r in rows]
    errors=[]
    if len(rows)!=expected_universe: errors.append(f"manifest_count={len(rows)} expected={expected_universe}")
    if any(not x for x in ids): errors.append("blank_league_id")
    if len(set(ids))!=len(ids): errors.append("duplicate_league_id")
    for r in rows:
        for k, aliases in {
            "league_id": ("league_id","selected_id"),
            "league_name": ("league_name","league"),
            "provider_league_id": ("provider_league_id","provider_competition_id","provider_id"),
            "provider_league_name": ("provider_league_name","provider_competition_name"),
        }.items():
            if not any(str(r.get(a) or "").strip() for a in aliases):
                errors.append(f"missing_{k}")
        season=str(r.get("season") or r.get("season_start_year") or "")
        try: y=int(season[:4])
        except ValueError: y=0
        if y and y < 2024: errors.append(f"season_before_2024:{season}")
    return errors

def validate_omi(rows, manifest_season_ids):
    errors=[]; stats={"rows":len(rows),"missing_required":0,"duplicate_identity":0,
                     "bad_probability":0,"bad_chronology":0,"missing_feature":0,
                     "stale_or_missing_retrieved":0,"invalid_actuals":0}
    if not rows: return ["omi_empty"],stats
    missing=[x for x in REQUIRED if x not in rows[0]]
    if missing: errors.append("missing_headers:"+",".join(missing)); return errors,stats
    seen=set()
    for i,r in enumerate(rows,1):
        key=tuple(str(r.get(k) or "").strip() for k in
                  ("Provider Season ID","Fixture ID","Home Team ID","Away Team ID"))
        if any(not x for x in key):
            errors.append(f"row{i}:missing_identity"); stats["missing_required"]+=1
        if key in seen: errors.append(f"row{i}:duplicate_identity"); stats["duplicate_identity"]+=1
        seen.add(key)
        if str(r.get("Provider Season ID") or "").strip() not in manifest_season_ids:
            errors.append(f"row{i}:season_not_in_manifest")
        kickoff=dt(r.get("Fixture Date"))
        cutoff=dt(r.get("History Cutoff UTC"))
        if kickoff and cutoff and cutoff >= kickoff:
            errors.append(f"row{i}:history_cutoff_not_pre_kickoff"); stats["bad_chronology"]+=1
        if not kickoff or not cutoff: errors.append(f"row{i}:missing_temporal_evidence")
        for f in PROBABILITY_FIELDS:
            if str(r.get(f) or "").strip() and num(r.get(f)) is None:
                errors.append(f"row{i}:bad_probability:{f}"); stats["bad_probability"]+=1
        for f in ("Recent Form (5)","League Position","H2H Last-5",
                  "Home Expected Goals Lambda","Away Expected Goals Lambda"):
            if not str(r.get(f) or "").strip():
                stats["missing_feature"]+=1
                errors.append(f"row{i}:missing_feature:{f}")
        rt=dt(r.get("retrieved_utc"))
        if not rt: errors.append(f"row{i}:missing_or_invalid_retrieved_utc"); stats["stale_or_missing_retrieved"]+=1
        for f in ("actual_home_goals","actual_away_goals","actual_total_goals"):
            v=str(r.get(f) or "").strip()
            if v:
                try:
                    if int(float(v))<0: raise ValueError
                except ValueError:
                    errors.append(f"row{i}:invalid_actual:{f}"); stats["invalid_actuals"]+=1
        status=str(r.get("settlement_status") or "").strip()
        if status.startswith("SETTLED_VERIFIED_EXACT_ID"):
            if not (str(r.get("actual_home_goals") or "").strip() and str(r.get("actual_away_goals") or "").strip()):
                errors.append(f"row{i}:settled_without_exact_score")
    return errors,stats

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--omi",required=True)
    ap.add_argument("--expected-leagues",type=int,default=60)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    with open(a.manifest,encoding="utf-8-sig",newline="") as f: manifest=list(csv.DictReader(f))
    with open(a.omi,encoding="utf-8-sig",newline="") as f: omi=list(csv.DictReader(f))
    me=validate_manifest(manifest,a.expected_leagues)
    ids={str(r.get("provider_season_id") or r.get("season_id") or "").strip() for r in manifest if str(r.get("provider_season_id") or r.get("season_id") or "").strip()}
    oe,stats=validate_omi(omi,ids)
    result={"status":"PASS" if not me and not oe else "BLOCK","expected_leagues":a.expected_leagues,
            "manifest_errors":me,"omi_errors":oe,"stats":stats,
            "governance":{"oracle_v1_6_probability_recalculation":False,
                          "production_logic_modified":False,
                          "fail_closed":True}}
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result["status"]=="PASS" else 2)

if __name__=="__main__": main()
