#!/usr/bin/env python3
"""Research-only chronological feature experiments for goal counts and 1X2.
Never changes Oracle production logic or writes canonical ledgers."""
import argparse, csv, json, math, re
from collections import defaultdict, deque
from datetime import date
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor, ExtraTreesClassifier, ExtraTreesRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, PoissonRegressor
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss, mean_absolute_error, mean_squared_error, r2_score, brier_score_loss
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def norm(s):
    return re.sub(r"[^a-z0-9]+"," ",str(s or "").lower()).strip()

def read_rows(path):
    with open(path,newline="",encoding="utf-8-sig") as f: return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--matches",required=True)
    ap.add_argument("--out-dir",required=True)
    ap.add_argument("--test-start",default="2026-04-01")
    a=ap.parse_args()
    rows=read_rows(a.matches)
    required={"date","league_code","home_team","away_team","home_goals","away_goals"}
    if not rows or required-set(rows[0]): raise SystemExit("DATA_GATED: match archive missing required columns")
    clean=[]
    for r in rows:
        try:
            d=date.fromisoformat(str(r["date"])[:10]); hg=int(float(r["home_goals"])); ag=int(float(r["away_goals"]))
            if hg<0 or ag<0 or d>=date.today(): continue
        except Exception: continue
        lc=str(r["league_code"]).strip(); ht=norm(r["home_team"]); at=norm(r["away_team"])
        if not lc or not ht or not at or ht==at: continue
        clean.append({"date":d.isoformat(),"league":lc,"home":ht,"away":at,"hg":hg,"ag":ag})
    # Exact league/team strings only; no fuzzy or alias inference.
    clean.sort(key=lambda x:(x["date"],x["league"],x["home"],x["away"]))
    seen={}
    for r in clean:
        k=(r["date"],r["league"],r["home"],r["away"])
        if k in seen and seen[k]!=(r["hg"],r["ag"]): raise SystemExit("DATA_GATED: conflicting scores for exact fixture key")
        seen[k]=(r["hg"],r["ag"])
    clean=[dict(date=k[0],league=k[1],home=k[2],away=k[3],hg=v[0],ag=v[1]) for k,v in seen.items()]
    # Sequential feature construction. Each fixture only sees strictly earlier dated results.
    teams=defaultdict(lambda:deque(maxlen=10)); league_hist=defaultdict(lambda:deque(maxlen=300))
    h2h=defaultdict(lambda:deque(maxlen=10)); rows_x=[]
    for r in clean:
        d=r["date"]; lg=r["league"]; h=r["home"]; aw=r["away"]
        th=list(teams[(lg,h)]); ta=list(teams[(lg,aw)]); lh=list(league_hist[lg])
        pair=tuple(sorted((h,aw))); ph=list(h2h[(lg,pair)])
        def avg(v,default=np.nan): return float(np.mean(v)) if v else default
        def team_feats(hist,prefix):
            out={}
            for n in (3,5,10):
                z=hist[-n:]
                out[f"{prefix}_n{n}"]=len(z)
                out[f"{prefix}_gf{n}"]=avg([x[0] for x in z])
                out[f"{prefix}_ga{n}"]=avg([x[1] for x in z])
                out[f"{prefix}_gd{n}"]=avg([x[0]-x[1] for x in z])
                out[f"{prefix}_pts{n}"]=avg([3 if x[0]>x[1] else 1 if x[0]==x[1] else 0 for x in z])
                out[f"{prefix}_btts{n}"]=avg([int(x[0]>0 and x[1]>0) for x in z])
                out[f"{prefix}_o25{n}"]=avg([int(x[0]+x[1]>2) for x in z])
            return out
        feat={"league":lg,"date":d,"home":h,"away":aw,
              "league_home_avg":avg([x[0] for x in lh]),"league_away_avg":avg([x[1] for x in lh]),
              "league_total_avg":avg([x[0]+x[1] for x in lh]),
              "h2h_n":len(ph),"h2h_total_avg":avg([x[0]+x[1] for x in ph]),
              "h2h_home_goals_avg":avg([x[0] if x[2]==h else x[1] for x in ph]),
              "h2h_away_goals_avg":avg([x[1] if x[2]==h else x[0] for x in ph]),
              "h2h_btts":avg([int(x[0]>0 and x[1]>0) for x in ph]),
              "h2h_o25":avg([int(x[0]+x[1]>2) for x in ph])}
        feat.update(team_feats(th,"home")); feat.update(team_feats(ta,"away"))
        # Store match outcomes after feature creation to avoid leakage.
        rows_x.append({**feat,"home_goals":r["hg"],"away_goals":r["ag"],"total_goals":r["hg"]+r["ag"],
                       "result":"H" if r["hg"]>r["ag"] else "D" if r["hg"]==r["ag"] else "A",
                       "btts":int(r["hg"]>0 and r["ag"]>0),"over15":int(r["hg"]+r["ag"]>1),"over25":int(r["hg"]+r["ag"]>2),"under35":int(r["hg"]+r["ag"]<4)})
        teams[(lg,h)].append((r["hg"],r["ag"])); teams[(lg,aw)].append((r["ag"],r["hg"]))
        league_hist[lg].append((r["hg"],r["ag"])); h2h[(lg,pair)].append((r["hg"],r["ag"],h))
    df=pd.DataFrame(rows_x)
    test_start=a.test_start
    train=df[df.date<test_start].copy(); test=df[df.date>=test_start].copy()
    if len(train)<1000 or len(test)<200: raise SystemExit(f"DATA_GATED: insufficient chronological sample train={len(train)} test={len(test)}")
    # Categorical league one-hot, all numeric features are strictly pre-match.
    drop={"date","home","away","home_goals","away_goals","total_goals","result","btts","over15","over25","under35"}
    X=pd.get_dummies(df.drop(columns=[c for c in drop if c in df]),columns=["league"],dummy_na=True)
    X_train=X.loc[train.index]; X_test=X.loc[test.index]
    targetsets={
      "home_goals":["league_baseline","recent_form","recent_plus_h2h","all_features"],
      "away_goals":["league_baseline","recent_form","recent_plus_h2h","all_features"],
      "total_goals":["league_baseline","recent_form","recent_plus_h2h","all_features"],
      "result":["league_baseline","recent_form","recent_plus_h2h","all_features"],
      "btts":["league_baseline","recent_form","recent_plus_h2h","all_features"],
      "over25":["league_baseline","recent_form","recent_plus_h2h","all_features"]}
    numeric=[c for c in X.columns if c!="league"]
    groups={
      "league_baseline":[c for c in numeric if c.startswith("league_")],
      "recent_form":[c for c in numeric if c.startswith(("home_n","home_gf","home_ga","home_gd","home_pts","home_btts","home_o25","away_n","away_gf","away_ga","away_gd","away_pts","away_btts","away_o25"))],
      "recent_plus_h2h":[c for c in numeric if c.startswith(("home_n","home_gf","home_ga","home_gd","home_pts","home_btts","home_o25","away_n","away_gf","away_ga","away_gd","away_pts","away_btts","away_o25","h2h_"))],
      "all_features":numeric}
    outdir=Path(a.out_dir); outdir.mkdir(parents=True,exist_ok=True)
    metrics=[]; importances=[]
    def fit_eval(target,group,task):
      cols=[c for c in groups[group] if c in X.columns]
      xt=X_train[cols]; xv=X_test[cols]; ytr=train[target]; yv=test[target]
      if task=="reg":
        models={
          "mean_baseline":DummyRegressor(strategy="mean"),
          "poisson":make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),PoissonRegressor(alpha=1.0,max_iter=500)),
          "random_forest":make_pipeline(SimpleImputer(strategy="median"),RandomForestRegressor(n_estimators=180,min_samples_leaf=5,max_features=0.8,n_jobs=-1,random_state=41)),
          "extra_trees":make_pipeline(SimpleImputer(strategy="median"),ExtraTreesRegressor(n_estimators=180,min_samples_leaf=5,max_features=0.8,n_jobs=-1,random_state=41)),
          "hist_gradient_boosting":make_pipeline(SimpleImputer(strategy="median"),HistGradientBoostingRegressor(max_iter=150,l2_regularization=2,random_state=41))}
      else:
        models={
          "most_common_baseline":DummyClassifier(strategy="prior"),
          "logistic":make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),LogisticRegression(max_iter=1000,class_weight=None)),
          "random_forest":make_pipeline(SimpleImputer(strategy="median"),RandomForestClassifier(n_estimators=180,min_samples_leaf=5,max_features=0.8,n_jobs=-1,random_state=41,class_weight="balanced_subsample")),
          "extra_trees":make_pipeline(SimpleImputer(strategy="median"),ExtraTreesClassifier(n_estimators=180,min_samples_leaf=5,max_features=0.8,n_jobs=-1,random_state=41,class_weight="balanced")),
          "hist_gradient_boosting":make_pipeline(SimpleImputer(strategy="median"),HistGradientBoostingClassifier(max_iter=150,l2_regularization=2,random_state=41))}
      for name,m in models.items():
        try:
          m.fit(xt,ytr); pred=m.predict(xv)
          row={"target":target,"feature_set":group,"model":name,"train_n":len(ytr),"test_n":len(yv),"test_start":test_start}
          if task=="reg":
            row.update({"mae":round(mean_absolute_error(yv,pred),4),"rmse":round(mean_squared_error(yv,pred)**0.5,4),"r2":round(r2_score(yv,pred),4),"exact_goal_count_pct":round(100*np.mean(np.rint(np.maximum(pred,0))==yv),2)})
          else:
            row.update({"accuracy_pct":round(100*accuracy_score(yv,pred),2),"balanced_accuracy_pct":round(100*balanced_accuracy_score(yv,pred),2)})
            if hasattr(m,"predict_proba"):
              probs=m.predict_proba(xv); classes=list(m.classes_) if hasattr(m,"classes_") else list(m[-1].classes_)
              if len(classes)==2:
                row["brier_score"]=round(brier_score_loss(yv,probs[:,1]),5)
              try: row["log_loss"]=round(log_loss(yv,probs,labels=classes),5)
              except Exception: pass
          metrics.append(row)
          # Tree importance averaged by impurity, exported as diagnostic only.
          est=m[-1] if hasattr(m,"steps") else m
          if hasattr(est,"feature_importances_"):
            for c,v in sorted(zip(cols,est.feature_importances_),key=lambda z:-z[1])[:20]:
              importances.append({"target":target,"feature_set":group,"model":name,"feature":c,"importance":round(float(v),6)})
        except Exception as e:
          metrics.append({"target":target,"feature_set":group,"model":name,"train_n":len(ytr),"test_n":len(yv),"error":str(e)[:300]})
    for target in ("home_goals","away_goals","total_goals"):
      for group in groups: fit_eval(target,group,"reg")
    for target in ("result","btts","over25"):
      for group in groups: fit_eval(target,group,"class")
    pd.DataFrame(metrics).to_csv(outdir/"goal_result_feature_experiment_metrics.csv",index=False)
    pd.DataFrame(importances).to_csv(outdir/"goal_result_feature_importance.csv",index=False)
    # Save prediction rows for the best-performing models by primary metric, not as betting advice.
    summary={"artifact":"ORACLE_GOAL_RESULT_FEATURE_EXPERIMENT_V1","status":"EXPLORATORY_CHRONOLOGICAL_RESEARCH_ONLY",
      "production_model_changed":False,"canonical_ledgers_written":False,"source_rows":len(rows),"valid_unique_matches":len(df),
      "train_rows":len(train),"test_rows":len(test),"train_start":str(train.date.min()),"train_end":str(train.date.max()),
      "test_start":str(test.date.min()),"test_end":str(test.date.max()),"leagues":int(df.league.nunique()),
      "feature_sets":list(groups),"targets":list(targetsets),"notes":[
       "Only features from strictly earlier-dated matches are used; same-day matches are not included in pre-match form.",
       "Exact normalized team names and exact league codes only; no fuzzy aliases or league reassignment.",
       "Chronological holdout is one broad cohort and metrics are exploratory, not production Oracle performance.",
       "Goal-count exact-match percentage rounds regression predictions and is only a secondary diagnostic.",
       "No odds or profitability claims; do not promote any result into production without additional rolling holdouts."]}
    (outdir/"goal_result_feature_experiment_audit.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
    print(pd.DataFrame(metrics).to_string(index=False))
if __name__=="__main__": main()
