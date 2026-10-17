#!/usr/bin/env python3
"""Research-only chronological test of incremental H2H signal on August 2026 BTTS OOS cohort.

Does not alter Oracle production predictions, model code, probabilities, or canonical ledgers.
Uses only prior same-league H2H results strictly before each target fixture date.
"""
import argparse, csv, json, math
from bisect import bisect_left
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def norm_team(s):
    return "".join(ch for ch in str(s or "").casefold() if ch.isalnum())

def parse_date(s):
    return pd.to_datetime(str(s)[:10], errors="coerce", utc=True)

def score_metrics(y, p):
    p=np.clip(np.asarray(p, dtype=float), 1e-6, 1-1e-6)
    y=np.asarray(y, dtype=int)
    out={"n":int(len(y)),"classification_accuracy_at_50pct_pct":round(float(accuracy_score(y,p>=0.5))*100,3),
         "brier_score":round(float(brier_score_loss(y,p)),6),
         "log_loss":round(float(log_loss(y,p,labels=[0,1])),6)}
    out["auc"]=round(float(roc_auc_score(y,p)),6) if len(set(y.tolist()))==2 else None
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--matches", required=True)
    ap.add_argument("--predictions", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--test-start", default="2026-08-21")
    args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    matches=pd.read_csv(args.matches)
    preds=pd.read_csv(args.predictions)
    reqm={"date","league_code","home_team","away_team","home_goals","away_goals"}
    reqp={"date","league_code","home_team","away_team","home_goals","away_goals","prob_BTTS"}
    if not reqm.issubset(matches.columns): raise SystemExit(f"Historical match archive missing columns: {sorted(reqm-set(matches.columns))}")
    if not reqp.issubset(preds.columns): raise SystemExit(f"August prediction file missing columns: {sorted(reqp-set(preds.columns))}")
    for df in (matches,preds):
        df["date_key"]=df["date"].map(parse_date)
        df["league_key"]=df["league_code"].astype(str).str.strip().str.upper()
        df["home_key"]=df["home_team"].map(norm_team)
        df["away_key"]=df["away_team"].map(norm_team)
    matches["hg"]=pd.to_numeric(matches["home_goals"],errors="coerce")
    matches["ag"]=pd.to_numeric(matches["away_goals"],errors="coerce")
    matches=matches.dropna(subset=["date_key","hg","ag"])
    matches=matches[(matches["hg"]>=0)&(matches["ag"]>=0)&(matches["home_key"]!="")&(matches["away_key"]!="")]
    matches["btts"]=(matches["hg"]>0)&(matches["ag"]>0)
    # Deduplicate only exact same source key/score representations; conflicting duplicates fail closed.
    matches["fixture_key"]=matches["date_key"].dt.strftime("%Y-%m-%d")+"|"+matches["league_key"]+"|"+matches["home_key"]+"|"+matches["away_key"]
    conflicts=matches.groupby("fixture_key").agg(rows=("btts","size"),scores=("hg",lambda x: len(set(x)))).reset_index()
    bad=conflicts[conflicts["rows"]>1]
    if len(bad):
        raise SystemExit(f"Historical archive contains {len(bad)} duplicate fixture keys; inspect archive before H2H test.")
    # Build exact same-league, unordered pair history; only matches strictly earlier than fixture date count.
    hist=defaultdict(list)
    for r in matches.itertuples(index=False):
        pair=tuple(sorted((r.home_key,r.away_key)))
        hist[(r.league_key,pair)].append((r.date_key, int(bool(r.btts))))
    for k in hist: hist[k].sort(key=lambda x:x[0])
    rows=[]
    preds["prob"]=pd.to_numeric(preds["prob_BTTS"],errors="coerce")
    preds["y"]=((pd.to_numeric(preds["home_goals"],errors="coerce")>0)&(pd.to_numeric(preds["away_goals"],errors="coerce")>0)).astype(int)
    preds=preds.dropna(subset=["date_key","prob","home_goals","away_goals"])
    preds=preds[(preds["date_key"].dt.strftime("%Y-%m")=="2026-08") & preds["prob"].between(0,1) & (preds["home_key"]!="") & (preds["away_key"]!="")]
    for r in preds.itertuples(index=False):
        key=(r.league_key,tuple(sorted((r.home_key,r.away_key))))
        prior=hist.get(key,[])
        cutoff=bisect_left([x[0] for x in prior],r.date_key)
        prior=prior[:cutoff]
        n=len(prior); b=sum(x[1] for x in prior)
        # Fixed Beta(1,1) smoothing; prior outcomes are restricted to earlier fixtures in the same league.
        rate=(b+1)/(n+2)
        rows.append({"match_id":getattr(r,"match_id",""),"date":r.date_key.strftime("%Y-%m-%d"),"league_code":r.league_key,
                     "home_team":r.home_team,"away_team":r.away_team,"prob_BTTS":float(r.prob),"actual_BTTS":int(r.y),
                     "prior_h2h_n":n,"prior_h2h_btts":b,"prior_h2h_btts_rate_smoothed":rate,
                     "h2h_available":int(n>0)})
    df=pd.DataFrame(rows).sort_values(["date","league_code","home_team","away_team"]).reset_index(drop=True)
    if len(df)<150: raise SystemExit(f"Insufficient resolved August rows after validation: {len(df)}")
    split=pd.Timestamp(args.test_start,tz="UTC")
    train=df[pd.to_datetime(df["date"],utc=True)<split].copy()
    test=df[pd.to_datetime(df["date"],utc=True)>=split].copy()
    if len(train)<100 or len(test)<50: raise SystemExit(f"Insufficient chronological cohort: train={len(train)}, test={len(test)}")
    def logit(p):
        p=np.clip(np.asarray(p,dtype=float),1e-5,1-1e-5)
        return np.log(p/(1-p))
    Xtr_base=logit(train["prob"]).reshape(-1,1); Xte_base=logit(test["prob"]).reshape(-1,1)
    Xtr_h2h=np.column_stack([logit(train["prob"]),train["prior_h2h_btts_rate_smoothed"],np.log1p(train["prior_h2h_n"])])
    Xte_h2h=np.column_stack([logit(test["prob"]),test["prior_h2h_btts_rate_smoothed"],np.log1p(test["prior_h2h_n"])])
    ytr=train["actual_BTTS"].to_numpy(); yte=test["actual_BTTS"].to_numpy()
    base=make_pipeline(StandardScaler(),LogisticRegression(C=1.0,max_iter=2000,random_state=41))
    plus=make_pipeline(StandardScaler(),LogisticRegression(C=1.0,max_iter=2000,random_state=41))
    base.fit(Xtr_base,ytr); plus.fit(Xtr_h2h,ytr)
    p_raw=np.clip(test["prob"].to_numpy(),1e-6,1-1e-6)
    p_base=base.predict_proba(Xte_base)[:,1]
    p_plus=plus.predict_proba(Xte_h2h)[:,1]
    df.loc[test.index,"baseline_recalibrated_probability"]=p_base
    df.loc[test.index,"h2h_augmented_probability"]=p_plus
    df.to_csv(out/"h2h_incremental_value_fixture_audit.csv",index=False)
    summaries={
      "artifact":"ORACLE_H2H_INCREMENTAL_VALUE_EXPERIMENT_V0.1",
      "status":"EXPLORATORY_CHRONOLOGICAL_RESEARCH_ONLY",
      "production_model_changed":False,"canonical_ledgers_written":False,
      "source_prediction_file":str(args.predictions),"source_match_archive":str(args.matches),
      "target_market":"BTTS_YES","cohort_month":"2026-08","test_start":args.test_start,
      "archive_rows_used":int(len(matches)),"august_rows_with_valid_probability_and_result":int(len(df)),
      "train_rows":int(len(train)),"test_rows":int(len(test)),
      "test_period":[str(test["date"].min()),str(test["date"].max())],
      "h2h_available_test_rows":int(test["h2h_available"].sum()),
      "h2h_available_test_pct":round(float(test["h2h_available"].mean()*100),2),
      "mean_prior_h2h_count_test":round(float(test["prior_h2h_n"].mean()),3),
      "metrics":{
        "raw_oracle_probability":score_metrics(yte,p_raw),
        "baseline_logistic_recalibration":score_metrics(yte,p_base),
        "baseline_plus_h2h_features":score_metrics(yte,p_plus)},
      "paired_differences":{
        "brier_h2h_minus_baseline":round(float(brier_score_loss(yte,p_plus)-brier_score_loss(yte,p_base)),6),
        "logloss_h2h_minus_baseline":round(float(log_loss(yte,p_plus,labels=[0,1])-log_loss(yte,p_base,labels=[0,1])),6)},
      "bootstrap":{
        "method":"paired bootstrap over test fixtures; seed=41; 2000 resamples",
        "resamples":2000,"seed":41},
      "limitations":[
        "Single August 2026 cohort; research-only, not production promotion evidence.",
        "Team identity matching is strict normalized text and same league only; no aliases or fuzzy matching are inferred.",
        "H2H features use only results with fixture dates strictly earlier than each target date.",
        "The H2H model is a research challenger fit on early-August rows and evaluated on later-August rows; this is not a production Oracle with-H2H/without-H2H controlled run.",
        "No betting profitability claim: odds and a governed staking rule are not evaluated.",
        "Do not interpret missing H2H as proof the teams never met." ]}
    # Paired bootstrap CI for difference in Brier score; negative favors H2H augmented.
    rng=np.random.default_rng(41); diffs=[]
    raw_y=np.asarray(yte,dtype=int); pb=np.asarray(p_base); ph=np.asarray(p_plus)
    for _ in range(2000):
        ix=rng.integers(0,len(raw_y),len(raw_y))
        diffs.append(float(np.mean((ph[ix]-raw_y[ix])**2)-np.mean((pb[ix]-raw_y[ix])**2)))
    summaries["bootstrap"]["brier_difference_95pct_ci"]=[round(float(np.quantile(diffs,.025)),6),round(float(np.quantile(diffs,.975)),6)]
    summaries["interpretation_guardrail"]="Only if H2H improves held-out scores should it be considered a candidate signal; confirm on additional rolling chronological cohorts before any production decision."
    (out/"h2h_incremental_value_audit.json").write_text(json.dumps(summaries,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summaries,indent=2))
if __name__=="__main__": main()
