#!/usr/bin/env python3
"""Validate prediction and Visual Intelligence CSVs for exact-key reporting.

Research-only: does not create predictions, recalculate probabilities, call APIs, or
change Oracle production logic. Missing evidence is reported as blocked, not filled.
"""
import argparse, csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT_DEFAULT=ROOT/"audit-output"/"selected50_fixture_report_input_validation.json"
PRED_REQUIRED={"fixture_id","market","oracle_probability_pct"}
VI_REQUIRED={"fixture_id","league","kickoff_utc","home_team","away_team",
             "home_recent_form","away_recent_form","h2h_summary",
             "home_attacking_index","home_defensive_index",
             "away_attacking_index","away_defensive_index"}

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"{path}: missing header")
        return reader.fieldnames,list(reader)

def nonblank(row,key):
    return str(row.get(key,"")).strip() != ""

def validate(prediction_path, visual_path):
    pheaders, preds=read_csv(prediction_path)
    vheaders, vis=read_csv(visual_path)
    missing_p=sorted(PRED_REQUIRED-set(pheaders))
    missing_v=sorted(VI_REQUIRED-set(vheaders))
    if missing_p or missing_v:
        return {"status":"BLOCKED_SCHEMA_MISMATCH","missing_prediction_columns":missing_p,
                "missing_visual_columns":missing_v,"prediction_rows":len(preds),
                "visual_rows":len(vis),"exact_fixture_join_performed":False,
                "probabilities_changed":False}
    pred_keys=[str(r["fixture_id"]).strip() for r in preds]
    vis_keys=[str(r["fixture_id"]).strip() for r in vis]
    duplicate_vi=sorted({k for k in vis_keys if k and vis_keys.count(k)>1})
    blank_pred=sum(not k for k in pred_keys)
    blank_vi=sum(not k for k in vis_keys)
    pred_fixture_ids=set(k for k in pred_keys if k)
    vis_fixture_ids=set(k for k in vis_keys if k)
    unmatched_pred=sorted(pred_fixture_ids-vis_fixture_ids)
    visual_without_pred=sorted(vis_fixture_ids-pred_fixture_ids)
    duplicate_market_keys=[]
    seen=set()
    for r in preds:
        fid=str(r.get("fixture_id","")).strip()
        market=str(r.get("market","")).strip()
        key=(fid,market)
        if fid and market and key in seen:
            duplicate_market_keys.append(f"{fid}|{market}")
        seen.add(key)
    bad_probs=[]
    for i,r in enumerate(preds, start=2):
        raw=str(r.get("oracle_probability_pct","")).strip()
        try:
            val=float(raw)
            if not (0.0 <= val <= 100.0):
                raise ValueError()
        except (TypeError,ValueError):
            bad_probs.append({"csv_row":i,"fixture_id":str(r.get("fixture_id","")),
                              "market":str(r.get("market","")),"reason":"MISSING_OR_OUT_OF_RANGE"})
    vi_by_id={str(r.get("fixture_id","")).strip():r for r in vis if str(r.get("fixture_id","")).strip()}
    matched=[fid for fid in pred_fixture_ids & vis_fixture_ids if fid not in duplicate_vi]
    form_missing=sum(not nonblank(vi_by_id[fid],"home_recent_form") or
                     not nonblank(vi_by_id[fid],"away_recent_form") for fid in matched)
    h2h_missing=sum(not nonblank(vi_by_id[fid],"h2h_summary") for fid in matched)
    index_fields=["home_attacking_index","home_defensive_index","away_attacking_index","away_defensive_index"]
    indices_missing=sum(any(not nonblank(vi_by_id[fid],k) for k in index_fields) for fid in matched)
    status="PASS" if not (blank_pred or blank_vi or duplicate_vi or unmatched_pred or visual_without_pred or duplicate_market_keys or bad_probs or form_missing or h2h_missing or indices_missing) else "BLOCKED_OR_INCOMPLETE"
    return {
      "status":status,"prediction_rows":len(preds),"visual_rows":len(vis),
      "prediction_unique_fixture_ids":len(pred_fixture_ids),"visual_unique_fixture_ids":len(vis_fixture_ids),
      "exact_fixture_join_performed":True,"matched_fixture_ids":len(matched),
      "unmatched_prediction_fixture_ids":unmatched_pred,
      "visual_fixture_ids_without_predictions":visual_without_pred,
      "blank_prediction_fixture_ids":blank_pred,"blank_visual_fixture_ids":blank_vi,
      "duplicate_visual_fixture_ids":duplicate_vi,"duplicate_fixture_market_keys":sorted(set(duplicate_market_keys)),
      "invalid_probability_rows":bad_probs,"probability_unit":"percentage, 0–100",
      "probabilities_changed":False,"recent_form_missing_fixture_count":form_missing,
      "h2h_missing_fixture_count":h2h_missing,"visual_index_missing_fixture_count":indices_missing,
      "notes":["Exact fixture_id join only; no fuzzy team-name matching.",
               "Probability values are validated, never recalculated or modified.",
               "H2H/recent-form/index gaps remain visible and block full reporting readiness."]
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--predictions",required=True,help="Prediction export CSV with fixture_id, market, oracle_probability_pct")
    ap.add_argument("--visual-intelligence",required=True,help="Visual Intelligence CSV keyed by exact fixture_id")
    ap.add_argument("--out",default=str(OUT_DEFAULT))
    a=ap.parse_args()
    result=validate(a.predictions,a.visual_intelligence)
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    if result["status"]!="PASS":
        raise SystemExit(2)

if __name__=="__main__": main()
