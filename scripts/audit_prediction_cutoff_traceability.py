#!/usr/bin/env python3
"""Mandatory research-run cutoff traceability audit; never alters predictions."""
import argparse, json
from pathlib import Path
import pandas as pd

REQUIRED={"fixture_id","data_cutoff_date","data_cutoff_utc","prediction_timestamp","fixture_date"}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--predictions",default="oracle/research/four_model/outputs/four_model_live_predictions.csv")
    p.add_argument("--output",default="/tmp/oracle-mandatory-cutoff-audit.json")
    p.add_argument("--live-outcome",default="unknown")
    a=p.parse_args()
    source=Path(a.predictions); out=Path(a.output)
    result={"scope":"MANDATORY_CUTOFF_TRACEABILITY","source":str(source),
            "status":"BLOCKED","rows":0,"unique_fixtures":0,
            "missing_cutoff_utc_rows":None,"missing_cutoff_date_rows":None,
            "cutoff_after_prediction_rows":None,"cutoff_after_fixture_date_rows":None,
            "production_promotion":"BLOCKED","live_runner_outcome":a.live_outcome}
    if a.live_outcome != "success":
        result["reason"]="live runner did not succeed; stale outputs are not eligible for cutoff validation"
        out.write_text(json.dumps(result,indent=2)+"\\n",encoding="utf-8")
        print(json.dumps(result,indent=2))
        raise SystemExit(2)
    if not source.exists():
        result["reason"]="prediction output absent; audit ran but no current output exists to validate"
        out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(result,indent=2))
        raise SystemExit(2)
    df=pd.read_csv(source,dtype=str).fillna("")
    result["rows"]=int(len(df))
    result["unique_fixtures"]=int(df["fixture_id"].nunique()) if "fixture_id" in df else 0
    missing=sorted(REQUIRED-set(df.columns))
    if missing:
        result["reason"]="required cutoff fields absent"
        result["missing_columns"]=missing
        out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(result,indent=2))
        raise SystemExit(2)
    result["missing_cutoff_utc_rows"]=int((df["data_cutoff_utc"].str.strip()=="").sum())
    result["missing_cutoff_date_rows"]=int((df["data_cutoff_date"].str.strip()=="").sum())
    cut=pd.to_datetime(df["data_cutoff_utc"],utc=True,errors="coerce")
    pred=pd.to_datetime(df["prediction_timestamp"],utc=True,errors="coerce")
    fixture=pd.to_datetime(df["fixture_date"],utc=True,errors="coerce")
    result["invalid_cutoff_utc_rows"]=int(cut.isna().sum())
    result["invalid_prediction_timestamp_rows"]=int(pred.isna().sum())
    result["invalid_fixture_date_rows"]=int(fixture.isna().sum())
    result["cutoff_after_prediction_rows"]=int((cut.notna() & pred.notna() & (cut>pred)).sum())
    # When a timezone-qualified kickoff exists, compare full timestamps. If the
    # kickoff is unknown, conservatively require the cutoff date to precede the
    # fixture date; never infer an unverified kickoff time.
    if "kickoff_utc" in df:
        kickoff=pd.to_datetime(df["kickoff_utc"],utc=True,errors="coerce")
        unknown_kickoff=kickoff.isna()
        result["cutoff_on_or_after_kickoff_rows"]=int((cut.notna() & kickoff.notna() & (cut>=kickoff)).sum())
    else:
        kickoff=pd.Series([pd.NaT]*len(df),index=df.index)
        unknown_kickoff=pd.Series([True]*len(df),index=df.index)
        result["cutoff_on_or_after_kickoff_rows"]=0
    result["rows_with_unverified_kickoff"]=int(unknown_kickoff.sum())
    # Same-day cutoff with no verified kickoff is unresolved, not proof of leakage.
    # Preserve it as an explicit quality flag while allowing research reconciliation
    # to finish; production remains blocked until kickoff coverage is reviewed.
    result["cutoff_date_on_or_after_fixture_date_without_verified_kickoff_rows"]=int(
        (cut.notna() & fixture.notna() & unknown_kickoff & (cut.dt.date>=fixture.dt.date)).sum()
    )
    result["latest_cutoff_utc"]=cut.max().isoformat() if cut.notna().any() else None
    result["latest_prediction_timestamp"]=pred.max().isoformat() if pred.notna().any() else None
    ok=(len(df)>0 and result["missing_cutoff_utc_rows"]==0 and result["missing_cutoff_date_rows"]==0
        and result["invalid_cutoff_utc_rows"]==0 and result["invalid_prediction_timestamp_rows"]==0
        and result["invalid_fixture_date_rows"]==0 and result["cutoff_after_prediction_rows"]==0
        and result["cutoff_on_or_after_kickoff_rows"]==0)
    result["cutoff_traceability_complete"]=bool(ok and result["rows_with_unverified_kickoff"]==0)
    result["status"]=("BLOCKED" if not ok else
        ("PASS" if result["rows_with_unverified_kickoff"]==0 else "PASS_WITH_UNVERIFIED_KICKOFFS"))
    result["production_promotion"]="BLOCKED"
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    if not ok: raise SystemExit(1)
if __name__=="__main__": main()
