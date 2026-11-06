#!/usr/bin/env python3
import csv,subprocess,sys,tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"validate_omi_reporting_extension.py"
FIELDS=["fixture_id","oracle_win_probability","oracle_draw_probability","confidence_score_pct","risk_score_pct",
        "backtest_sample_n","backtest_hit_rate_pct","backtest_brier_score","backtest_log_loss","backtest_scope","backtest_asof_utc"]

def write(path,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)

def base():
    return {"fixture_id":"F1","oracle_win_probability":"61","oracle_draw_probability":"24",
            "confidence_score_pct":"78","risk_score_pct":"22","backtest_sample_n":"100",
            "backtest_hit_rate_pct":"71","backtest_brier_score":"0.18","backtest_log_loss":"0.52",
            "backtest_scope":"league:season:market","backtest_asof_utc":"2026-11-05T21:00:00+00:00"}

def run(rows,ok):
    with tempfile.TemporaryDirectory() as td:
        p=Path(td); inp=p/"x.csv"; out=p/"o.json"; write(inp,rows)
        r=subprocess.run([sys.executable,str(SCRIPT),"--input",str(inp),"--out",str(out)],capture_output=True,text=True)
        assert (r.returncode==0)==ok,(r.stdout,r.stderr)

def main():
    run([base()],True)
    x=base(); x["confidence_score_pct"]="101"; run([x],False)
    x=base(); x["risk_score_pct"]="-1"; run([x],False)
    x=base(); x["oracle_win_probability"]="101"; run([x],False)
    x=base(); x["oracle_win_probability"]="nan"; run([x],False)
    x=base(); x["backtest_brier_score"]="nan"; run([x],False)
    x=base(); x["backtest_sample_n"]="0"; x["backtest_scope"]=""; x["backtest_asof_utc"]=""; run([x],True)
    x=base(); x["backtest_sample_n"]="10"; x["backtest_scope"]=""; run([x],False)
    x=base(); x["backtest_asof_utc"]="2026-11-05T21:00:00"; run([x],False)
    x=base(); x["fixture_id"]=""; run([x],False)
    x=base(); y=base(); y["fixture_id"]="F1"; run([x,y],False)
    print("PASS: OMI reporting extension regression suite")

if __name__=="__main__": main()
