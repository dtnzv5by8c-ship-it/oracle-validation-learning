#!/usr/bin/env python3
"""Offline, fail-closed contract for Master OMI joins.

Reporting-only: validates exact Fixture ID joins and chronology/field completeness.
It never recalculates Oracle probabilities and never calls a provider.
"""
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_ORACLE = [
    "fixture_id","league_id","season_id","kickoff_utc","home_team_id","away_team_id",
    "win_probability","draw_probability"
]
REQUIRED_FEATURES = [
    "fixture_id","home_team_id","away_team_id","recent_form_home","recent_form_away","league_position_home",
    "league_position_away","h2h_count","home_xg","away_xg","btts_probability"
]
REQUIRED_ACTUALS = ["fixture_id","actual_home_goals","actual_away_goals","result"]

def rows(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def present(v):
    return v is not None and str(v).strip() != ""

def parse_ts(v):
    s = str(v or "").strip().replace("Z","+00:00")
    dt = datetime.fromisoformat(s)
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)

def unique_ids(rs, label):
    ids = [str(r.get("fixture_id","")).strip() for r in rs]
    if any(not x for x in ids):
        raise ValueError(f"{label}: blank fixture_id")
    if len(ids) != len(set(ids)):
        raise ValueError(f"{label}: duplicate fixture_id")
    return set(ids)

def require_fields(rs, fields, label):
    missing = sorted({f for f in fields if any(not present(r.get(f)) for r in rs)})
    if missing:
        raise ValueError(f"{label}: missing required fields: {','.join(missing)}")

def pct(v, label):
    x=float(v)
    if not 0 <= x <= 100:
        raise ValueError(f"{label}: probability outside 0..100: {x}")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--oracle", required=True)
    ap.add_argument("--features", required=True)
    ap.add_argument("--actuals", required=True)
    ap.add_argument("--out", required=True)
    a=ap.parse_args()
    oracle=rows(a.oracle); features=rows(a.features); actuals=rows(a.actuals)
    if not oracle: raise ValueError("oracle: empty")
    if not features: raise ValueError("features: empty")
    if not actuals: raise ValueError("actuals: empty")

    oid=unique_ids(oracle,"oracle")
    fid=unique_ids(features,"features")
    aid=unique_ids(actuals,"actuals")
    require_fields(oracle,REQUIRED_ORACLE,"oracle")
    require_fields(features,REQUIRED_FEATURES,"features")
    require_fields(actuals,REQUIRED_ACTUALS,"actuals")

    for r in oracle:
        pct(r["win_probability"],"win_probability")
        pct(r["draw_probability"],"draw_probability")
    for r in features:
        pct(r["btts_probability"],"btts_probability")
        try:
            parse_ts(r.get("feature_asof_utc", r.get("kickoff_utc")))
        except Exception as e:
            raise ValueError(f"features: invalid feature_asof_utc for {r['fixture_id']}: {e}")
    for r in oracle:
        k=parse_ts(r["kickoff_utc"])
        for key in ("feature_asof_utc","h2h_asof_utc","league_position_asof_utc"):
            if present(r.get(key)) and parse_ts(r[key]) > k:
                raise ValueError(f"oracle: {key} after kickoff for {r['fixture_id']}")

    overlap_oracle_features=oid & fid
    overlap_oracle_actuals=oid & aid
    if overlap_oracle_features != oid:
        raise ValueError(f"oracle/features: {len(oid-overlap_oracle_features)} fixtures missing exact feature join")
    if overlap_oracle_actuals != oid:
        raise ValueError(f"oracle/actuals: {len(oid-overlap_oracle_actuals)} fixtures missing exact actual join")

    fby={r["fixture_id"]:r for r in features}
    aby={r["fixture_id"]:r for r in actuals}
    joined=[]
    for r in oracle:
        fid=r["fixture_id"]
        fr=fby[fid]; ar=aby[fid]
        if str(r["home_team_id"]) != str(fr.get("home_team_id", r["home_team_id"])) or str(r["away_team_id"]) != str(fr.get("away_team_id", r["away_team_id"])):
            raise ValueError(f"oracle/features: team identity mismatch for {fid}")
        joined.append({
            "fixture_id":fid,
            "league_id":r["league_id"],
            "season_id":r["season_id"],
            "kickoff_utc":r["kickoff_utc"],
            "home_team_id":r["home_team_id"],
            "away_team_id":r["away_team_id"],
            "win_probability":r["win_probability"],
            "draw_probability":r["draw_probability"],
            "recent_form_home":fr["recent_form_home"],
            "recent_form_away":fr["recent_form_away"],
            "league_position_home":fr["league_position_home"],
            "league_position_away":fr["league_position_away"],
            "h2h_count":fr["h2h_count"],
            "home_xg":fr["home_xg"],
            "away_xg":fr["away_xg"],
            "btts_probability":fr["btts_probability"],
            "actual_home_goals":ar["actual_home_goals"],
            "actual_away_goals":ar["actual_away_goals"],
            "result":ar["result"],
        })
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    fields=list(joined[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(joined)
    summary={
        "status":"PASS_MASTER_OMI_EXACT_ID_JOIN",
        "oracle_rows":len(oracle),
        "feature_rows":len(features),
        "actual_rows":len(actuals),
        "joined_rows":len(joined),
        "oracle_probabilities_recalculated":False,
        "provider_api_calls":0,
        "production_model_logic_changed":False,
        "production_eligibility":"NOT_GRANTED",
        "join_key":"fixture_id",
        "fail_closed":True
    }
    (out.with_suffix(".summary.json")).write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
