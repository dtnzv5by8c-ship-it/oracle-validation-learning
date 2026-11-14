#!/usr/bin/env python3
"""Research-only weekly chronological backtest and calibration challenger."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import roc_auc_score

ROOT=Path(__file__).resolve().parents[1]
PRED=ROOT/"oracle/research/four_model/outputs/four_model_oos_predictions.csv"
MATCHES=ROOT/"oracle/database/matches.csv"
OUT=ROOT/"outputs/weekly_recalibration"
OUT.mkdir(parents=True,exist_ok=True)
MIN_TRAIN=500
MIN_TEST=50
EPS=1e-6

def metrics(y,p):
    y=np.asarray(y,float); p=np.clip(np.asarray(p,float),EPS,1-EPS)
    if not len(y): return {"n":0,"brier":None,"log_loss":None,"auc":None,"actual_rate":None,"mean_probability":None,"calibration_gap":None}
    auc=None
    if len(np.unique(y))==2: auc=float(roc_auc_score(y,p))
    return {"n":int(len(y)),"brier":float(np.mean((p-y)**2)),
            "log_loss":float(-np.mean(y*np.log(p)+(1-y)*np.log(1-p))),
            "auc":auc,"actual_rate":float(np.mean(y)),
            "mean_probability":float(np.mean(p)),
            "calibration_gap":float(np.mean(p)-np.mean(y))}

def ece(y,p,bins=10):
    y=np.asarray(y,float); p=np.asarray(p,float)
    if not len(y): return None
    edges=np.linspace(0,1,bins+1); v=0.0
    for i in range(bins):
        mask=(p>=edges[i]) & ((p<edges[i+1]) if i<bins-1 else (p<=edges[i+1]))
        if mask.any(): v += mask.mean()*abs(y[mask].mean()-p[mask].mean())
    return float(v)

def main():
    if not PRED.exists() or not MATCHES.exists(): raise SystemExit("MISSING_INPUT")
    p=pd.read_csv(PRED,low_memory=False); m=pd.read_csv(MATCHES,low_memory=False)
    req={"match_id","date","model","target"}
    if not req.issubset(p.columns): raise SystemExit(f"PRED_SCHEMA_FAILURE missing={sorted(req-set(p.columns))}")
    prob="raw_probability" if "raw_probability" in p.columns else ("probability" if "probability" in p.columns else None)
    if not prob: raise SystemExit("PRED_SCHEMA_FAILURE probability missing")
    reqm={"match_id","date","league_code"}
    if not reqm.issubset(m.columns): raise SystemExit(f"MATCH_SCHEMA_FAILURE missing={sorted(reqm-set(m.columns))}")

    # The OOS ledger already contains prediction date and event truth. Global performance
    # and calibration must not depend on a secondary identity join. Match metadata is
    # enrichment only; no fuzzy matching is permitted.
    p["date"]=pd.to_datetime(p["date"],errors="coerce")
    p["p"]=pd.to_numeric(p[prob],errors="coerce")
    p["target"]=pd.to_numeric(p["target"],errors="coerce")
    p=p.dropna(subset=["date","p","target","match_id"]).copy()
    before=len(p)

    m["date"]=pd.to_datetime(m["date"],errors="coerce")
    p["_match_key"]=p["match_id"].astype(str).str.strip()
    m["_match_key"]=m["match_id"].astype(str).str.strip()
    meta=m[["_match_key","league_code"]].drop_duplicates("_match_key")
    p=p.merge(meta,on="_match_key",how="left",validate="many_to_one",suffixes=("","_match"))
    matched=int(p["league_code"].notna().sum())
    join_rate=(matched/before) if before else 0.0
    p["league_code"]=p["league_code"].fillna("UNMATCHED_IDENTITY").astype(str).str.strip()

    p["week"]=p["date"].dt.to_period("W-MON").apply(lambda x:str(x.start_time.date()))
    p["market"]=p["model"].astype(str).str.replace("_R2","",regex=False)
    p=p.sort_values(["date","match_id","model"]).reset_index(drop=True)

    weekly=[]; reliability_rows=[]; band_rows=[]
    for (week,model),g in p.groupby(["week","model"],sort=True):
        z=metrics(g.target,g.p); z["ece"]=ece(g.target,g.p)
        weekly.append({"week":week,"model":model,**z})
        for i in range(10):
            lo=i/10; hi=(i+1)/10
            mask=(g.p>=lo)&((g.p<hi) if i<9 else (g.p<=hi))
            if mask.any():
                reliability_rows.append({"week":week,"model":model,"bin":i,"n":int(mask.sum()),
                    "predicted_mean":float(g.loc[mask,"p"].mean()),"actual_rate":float(g.loc[mask,"target"].mean()),
                    "abs_gap":float(abs(g.loc[mask,"p"].mean()-g.loc[mask,"target"].mean()))})
        edges=[0,.5,.6,.7,.8,1.0]
        labels=["<0.50","0.50-0.59","0.60-0.69","0.70-0.79","0.80-1.00"]
        for lo,hi,label in zip(edges[:-1],edges[1:],labels):
            mask=(g.p>=lo)&((g.p<hi) if hi<1 else (g.p<=hi))
            if mask.any():
                bm=metrics(g.loc[mask,"target"],g.loc[mask,"p"])
                band_rows.append({"week":week,"model":model,"probability_band":label,**bm})
    pd.DataFrame(weekly).to_csv(OUT/"weekly_raw_performance.csv",index=False)
    pd.DataFrame(reliability_rows).to_csv(OUT/"weekly_reliability.csv",index=False)
    pd.DataFrame(band_rows).to_csv(OUT/"weekly_probability_bands.csv",index=False)

    league_week=[]
    for (week,league,model),g in p.groupby(["week","league_code","model"],sort=True):
        if len(g)<10 or league=="UNMATCHED_IDENTITY": continue
        z=metrics(g.target,g.p); z["ece"]=ece(g.target,g.p)
        league_week.append({"week":week,"league_code":league,"model":model,**z})
    pd.DataFrame(league_week).to_csv(OUT/"weekly_league_performance.csv",index=False)

    cal_rows=[]
    for model in sorted(p["model"].unique()):
        q=p[p.model.eq(model)].sort_values(["date","match_id"]).copy()
        for week in sorted(q.week.unique()):
            test=q[q.week.eq(week)]
            train=q[q.date < test.date.min()]
            if len(train)<MIN_TRAIN or len(test)<MIN_TEST: continue
            raw=metrics(test.target,test.p); raw["ece"]=ece(test.target,test.p)
            for method in ["platt","isotonic"]:
                try:
                    if len(train.target.unique())<2: continue
                    if method=="platt":
                        fit=LogisticRegression(solver="lbfgs").fit(train.p.to_numpy().reshape(-1,1),train.target.astype(int))
                        cp=fit.predict_proba(test.p.to_numpy().reshape(-1,1))[:,1]
                    else:
                        fit=IsotonicRegression(y_min=EPS,y_max=1-EPS,out_of_bounds="clip").fit(train.p,train.target)
                        cp=fit.predict(test.p)
                    cm=metrics(test.target,cp); cm["ece"]=ece(test.target,cp)
                    cal_rows.append({"week":week,"model":model,"method":method,"train_n":len(train),"test_n":len(test),
                        "raw_brier":raw["brier"],"candidate_brier":cm["brier"],"brier_improvement":raw["brier"]-cm["brier"],
                        "raw_log_loss":raw["log_loss"],"candidate_log_loss":cm["log_loss"],"log_loss_improvement":raw["log_loss"]-cm["log_loss"],
                        "raw_ece":raw["ece"],"candidate_ece":cm["ece"],"ece_improvement":raw["ece"]-cm["ece"]})
                except Exception as e:
                    cal_rows.append({"week":week,"model":model,"method":method,"train_n":len(train),"test_n":len(test),"error":type(e).__name__})
    cal=pd.DataFrame(cal_rows); cal.to_csv(OUT/"weekly_recalibration_candidates.csv",index=False)

    rec=[]
    if len(cal):
        valid=cal[~cal.get("error",pd.Series(index=cal.index,dtype=object)).notna()] if "error" in cal else cal
        for (model,method),g in valid.groupby(["model","method"]):
            rec.append({"model":model,"method":method,"weeks_tested":len(g),
                "mean_brier_improvement":float(g.brier_improvement.mean()),"median_brier_improvement":float(g.brier_improvement.median()),
                "mean_log_loss_improvement":float(g.log_loss_improvement.mean()),"median_log_loss_improvement":float(g.log_loss_improvement.median()),
                "mean_ece_improvement":float(g.ece_improvement.mean()),"weeks_brier_better":int((g.brier_improvement>0).sum()),
                "weeks_log_loss_better":int((g.log_loss_improvement>0).sum()),
                "recommendation":"RESEARCH_CANDIDATE" if len(g)>=8 and g.brier_improvement.mean()>0 and g.log_loss_improvement.mean()>0 and (g.brier_improvement>0).mean()>=0.60 else "HOLD"})
    pd.DataFrame(rec).to_csv(OUT/"recalibration_recommendations.csv",index=False)

    manifest={"status":"COMPLETE_RESEARCH_ONLY" if len(p) else "BLOCKED_NO_OOS","generated_utc":pd.Timestamp.now(tz="UTC").isoformat(),
              "prediction_rows":int(len(p)),"models":sorted(p.model.unique().tolist()) if len(p) else [],
              "weeks":int(p.week.nunique()) if len(p) else 0,"source_prediction_rows":int(before),
              "prediction_match_metadata_join_rate":float(join_rate),"unmatched_prediction_rows":int(before-matched),
              "minimum_training_rows":MIN_TRAIN,"minimum_test_rows":MIN_TEST,"production_change":False,
              "chronology":"prediction-ledger date; training strictly before test week",
              "identity_rule":"exact canonical match_id for metadata enrichment only; unmatched metadata retained; no fuzzy matching"}
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"
"); print(json.dumps(manifest,indent=2))

if __name__=="__main__": main()
