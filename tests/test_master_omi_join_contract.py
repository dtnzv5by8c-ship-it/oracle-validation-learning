#!/usr/bin/env python3
"""Standard-library regression tests for the Master OMI exact-ID join contract."""
import csv, json, subprocess, sys, tempfile
from pathlib import Path

SCRIPT=Path(__file__).resolve().parents[1]/"scripts"/"validate_master_omi_join_contract.py"

def write(p, fields, rows):
    with p.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

def base():
    oracle=[{"fixture_id":"F1","league_id":"L1","season_id":"S1","kickoff_utc":"2026-11-01T18:00:00+00:00","home_team_id":"H1","away_team_id":"A1","win_probability":"61","draw_probability":"24"}]
    features=[{"fixture_id":"F1","home_team_id":"H1","away_team_id":"A1","recent_form_home":"WWDWL","recent_form_away":"LDWLL","league_position_home":"2","league_position_away":"9","h2h_count":"5","home_xg":"1.72","away_xg":"1.03","btts_probability":"58","feature_asof_utc":"2026-11-01T17:00:00+00:00"}]
    actuals=[{"fixture_id":"F1","actual_home_goals":"2","actual_away_goals":"1","result":"HOME"}]
    return oracle,features,actuals

def run(oracle,features,actuals,expect_ok):
    with tempfile.TemporaryDirectory() as td:
        d=Path(td); op=d/"o.csv"; fp=d/"f.csv"; ap=d/"a.csv"; out=d/"joined.csv"
        write(op,list(oracle[0]),oracle); write(fp,list(features[0]),features); write(ap,list(actuals[0]),actuals)
        r=subprocess.run([sys.executable,str(SCRIPT),"--oracle",str(op),"--features",str(fp),"--actuals",str(ap),"--out",str(out)],text=True,capture_output=True)
        assert (r.returncode==0)==expect_ok, r.stderr or r.stdout

def main():
    o,f,a=base(); run(o,f,a,True)
    bad=[dict(x) for x in f]; bad[0]["feature_asof_utc"]="2026-11-01T19:00:00+00:00"; run(o,bad,a,False)
    bad=[dict(x) for x in f]; bad[0]["fixture_id"]="F2"; run(o,bad,a,False)
    bad=[dict(x) for x in f]; bad.append(dict(bad[0])); run(o,bad,a,False)
    bad=[dict(x) for x in f]; bad[0]["home_team_id"]="H9"; run(o,bad,a,False)
    bad=[dict(x) for x in o]; bad[0]["win_probability"]="101"; run(bad,f,a,False)
    print("PASS: Master OMI exact-ID join contract regression suite")

if __name__=="__main__": main()
