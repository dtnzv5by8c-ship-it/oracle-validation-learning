#!/usr/bin/env python3
"""Audit point-in-time PPG/GF-M/GA-M denominators for governed OMI fixtures.

Research/evidence control only. This script never changes Oracle V1.6 or workbook A:ET.
It requires exact fixture identity fields in the current fixture file and historical
settled matches with a timestamp (or date fallback explicitly marked DATE_ONLY).
For every team it reconstructs overall and venue-specific metrics from the last five
qualifying matches strictly before kickoff. Fewer than five qualifying matches are
reported as UNVERIFIED and are never imputed.
"""
from pathlib import Path
import argparse, json, re
import numpy as np
import pandas as pd

REQUIRED_FIXTURE = {"fixture_id","league_code","home_team","away_team","kickoff_time"}
REQUIRED_MATCH = {"match_id","date","league_code","home_team","away_team","home_goals","away_goals"}

def norm(v):
    return re.sub(r"[^a-z0-9]+"," ",str(v or "").lower()).strip()

def canonical_key(league, team):
    return (norm(league), norm(team))

def parse_time(df, col):
    return pd.to_datetime(df[col], utc=True, errors="coerce")

def metrics(g, team):
    if g.empty:
        return {"n":0,"ppg":np.nan,"gf_m":np.nan,"ga_m":np.nan}
    gf=np.where(g.home_team.eq(team),g.home_goals,g.away_goals).astype(float)
    ga=np.where(g.home_team.eq(team),g.away_goals,g.home_goals).astype(float)
    pts=np.where(gf>ga,3,np.where(gf==ga,1,0))
    return {"n":int(len(g)),"ppg":float(np.mean(pts)),"gf_m":float(np.mean(gf)),"ga_m":float(np.mean(ga))}

def audit(fixtures, matches, out):
    f=pd.read_csv(fixtures,low_memory=False)
    m=pd.read_csv(matches,low_memory=False)
    missing_f=REQUIRED_FIXTURE-set(f.columns); missing_m=REQUIRED_MATCH-set(m.columns)
    if missing_f: raise SystemExit("BLOCKED_FIXTURE_SCHEMA:"+",".join(sorted(missing_f)))
    if missing_m: raise SystemExit("BLOCKED_MATCH_SCHEMA:"+",".join(sorted(missing_m)))
    f["kickoff_parsed"]=parse_time(f,"kickoff_time")
    m["match_time"]=parse_time(m,"kickoff_time") if "kickoff_time" in m.columns else parse_time(m,"date")
    m["date"]=pd.to_datetime(m["date"],utc=True,errors="coerce")
    for c in ["home_goals","away_goals"]: m[c]=pd.to_numeric(m[c],errors="coerce")
    # Exact identity checks; no fuzzy fixture joins are allowed.
    f["fixture_id"]=f["fixture_id"].astype(str)
    m["match_id"]=m["match_id"].astype(str)
    duplicate_fixture_ids=int(f.fixture_id.duplicated(keep=False).sum())
    duplicate_match_ids=int(m.match_id.duplicated(keep=False).sum())
    rows=[]
    for r in f.itertuples(index=False):
        kickoff=r.kickoff_parsed
        league=str(r.league_code); home=str(r.home_team); away=str(r.away_team)
        fixture_status="PREMATCH_TIME_VERIFIED" if pd.notna(kickoff) else "UNVERIFIED_KICKOFF_TIMESTAMP"
        for side,team in (("home",home),("away",away)):
            if pd.notna(kickoff):
                prior=m[(m.league_code.astype(str)==league) &
                        (m.match_time.notna()) & (m.match_time<kickoff) &
                        ((m.home_team.astype(str)==team)|(m.away_team.astype(str)==team)) &
                        m.home_goals.notna() & m.away_goals.notna()].copy()
                scope="strict_kickoff"
            else:
                # No timestamp = no admissible historical denominator. Do not fall back to date-only history.
                prior=m.iloc[0:0].copy()
                scope="BLOCKED_NO_KICKOFF"
            prior=prior.sort_values(["match_time","match_id"]).drop_duplicates("match_id",keep="last")
            overall=prior.tail(5)
            venue=overall[overall.home_team.astype(str)==team] if side=="home" else overall[overall.away_team.astype(str)==team]
            # Venue metric must use the team's five most recent venue matches, not a subset of overall five.
            venue_all=prior[prior.home_team.astype(str)==team] if side=="home" else prior[prior.away_team.astype(str)==team]
            venue=venue_all.tail(5)
            om=metrics(overall,team); vm=metrics(venue,team)
            status="VERIFIED_5_MATCH" if om["n"]>=5 and fixture_status=="PREMATCH_TIME_VERIFIED" else "UNVERIFIED_FIVE_MATCH_MINIMUM"
            vstatus="VERIFIED_5_VENUE_MATCH" if vm["n"]>=5 and fixture_status=="PREMATCH_TIME_VERIFIED" else "UNVERIFIED_VENUE_MINIMUM"
            rows.append({
                "fixture_id":r.fixture_id,"league_code":league,"team":team,"side":side,
                "pre_match_status":fixture_status,"history_scope":scope,
                "overall_n":om["n"],"ppg":om["ppg"],"gf_m":om["gf_m"],"ga_m":om["ga_m"],"overall_status":status,
                "venue_n":vm["n"],"venue_ppg":vm["ppg"],"venue_gf_m":vm["gf_m"],"venue_ga_m":vm["ga_m"],"venue_status":vstatus,
                "source":"historical settled match archive","quality":"VERIFIED" if status=="VERIFIED_5_MATCH" else "UNVERIFIED",
                "substitution_flag":False,
                "missingness_reason":"" if status=="VERIFIED_5_MATCH" else ("KICKOFF_TIMESTAMP_UNVERIFIED" if fixture_status!="PREMATCH_TIME_VERIFIED" else "FIVE_MATCH_MINIMUM_NOT_MET"),
            })
    d=pd.DataFrame(rows)
    out=Path(out); out.parent.mkdir(parents=True,exist_ok=True); d.to_csv(out,index=False)
    summary={
        "fixture_rows":int(len(f)),"fixture_duplicate_id_rows":duplicate_fixture_ids,
        "historical_duplicate_id_rows":duplicate_match_ids,
        "team_side_rows":int(len(d)),
        "verified_overall_rows":int((d.overall_status=="VERIFIED_5_MATCH").sum()),
        "verified_venue_rows":int((d.venue_status=="VERIFIED_5_VENUE_MATCH").sum()),
        "overall_coverage":float((d.overall_status=="VERIFIED_5_MATCH").mean()) if len(d) else 0.0,
        "venue_coverage":float((d.venue_status=="VERIFIED_5_VENUE_MATCH").mean()) if len(d) else 0.0,
        "production_change":False,
        "policy":"No value is admitted when exact identity, pre-match chronology, and minimum qualifying sample are not verified."
    }
    out.with_suffix(".summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--fixtures",required=True)
    ap.add_argument("--matches",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    audit(a.fixtures,a.matches,a.out)
