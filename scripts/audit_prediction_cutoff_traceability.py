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
    a=p.parse_args()
    source=Path(a.predictions); out=Path(a.output)
    result={"scope":"MANDATORY_CUTOFF_TRACEABILITY","source":str(source),
            "status":"BLOCKED","rows":0,"unique_fixtures":0,
            "missing_cutoff_utc_rows":None,"missing_cutoff_date_rows":None,
            "cutoff_after_prediction_rows":None,"cutoff_after_fixture_date_rows":None,
            "production_promotion":"BLOCKED"}
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
    # A data cutoff must be strictly before the fixture date, not merely before prediction time.
    result["cutoff_on_or_after_fixture_date_rows"]=int((cut.notna() & fixture.notna() & (cut.dt.date>=fixture.dt.date)).sum())
    result["latest_cutoff_utc"]=cut.max().isoformat() if cut.notna().any() else None
    result["latest_prediction_timestamp"]=pred.max().isoformat() if pred.notna().any() else None
    ok=(len(df)>0 and result["missing_cutoff_utc_rows"]==0 and result["missing_cutoff_date_rows"]==0
        and result["invalid_cutoff_utc_rows"]==0 and result["invalid_prediction_timestamp_rows"]==0
        and result["invalid_fixture_date_rows"]==0 and result["cutoff_after_prediction_rows"]==0
        and result["cutoff_on_or_after_fixture_date_rows"]==0)
    result["status"]="PASS" if ok else "BLOCKED"
    result["production_promotion"]="BLOCKED"
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    if not ok: raise SystemExit(1)
if __name__=="__main__": main()
