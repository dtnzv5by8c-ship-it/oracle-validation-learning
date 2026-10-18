#!/usr/bin/env python3
"""Rolling chronological validation of goal/result research features.
Research only: never modifies Oracle production logic or canonical ledgers."""
import argparse, csv, json, re
from collections import defaultdict, deque
from datetime import date
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, brier_score_loss, log_loss
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

WINDOWS = [
    ("2025Q4", "2025-10-01", "2025-12-31"),
    ("2026Q1", "2026-01-01", "2026-03-31"),
    ("2026AprOct", "2026-04-01", "2026-10-16"),
]
FEATURE_SETS = ("league_baseline", "recent_form", "recent_plus_h2h", "all_features")

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s or "").lower()).strip()

def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--matches", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    raw = read_rows(args.matches)
    required = {"date","league_code","home_team","away_team","home_goals","away_goals"}
    if not raw or required - set(raw[0]):
        raise SystemExit("DATA_GATED: match archive missing required columns")
    cleaned = []
    for r in raw:
        try:
            d = date.fromisoformat(str(r["date"])[:10])
            hg, ag = int(float(r["home_goals"])), int(float(r["away_goals"]))
            if hg < 0 or ag < 0 or d >= date.today(): continue
        except Exception:
            continue
        lg, h, a = str(r["league_code"]).strip(), norm(r["home_team"]), norm(r["away_team"])
        if lg and h and a and h != a:
            cleaned.append({"date":d.isoformat(),"league":lg,"home":h,"away":a,"hg":hg,"ag":ag})
    cleaned.sort(key=lambda x:(x["date"],x["league"],x["home"],x["away"]))
    unique = {}
    for r in cleaned:
        k=(r["date"],r["league"],r["home"],r["away"])
        if k in unique and unique[k] != (r["hg"],r["ag"]):
            raise SystemExit("DATA_GATED: conflicting scores for exact fixture key")
        unique[k]=(r["hg"],r["ag"])
    clean=[{"date":k[0],"league":k[1],"home":k[2],"away":k[3],"hg":v[0],"ag":v[1]} for k,v in unique.items()]

    teams=defaultdict(lambda:deque(maxlen=10)); league_hist=defaultdict(lambda:deque(maxlen=300)); h2h=defaultdict(lambda:deque(maxlen=10)); built=[]
    def avg(vals): return float(np.mean(vals)) if vals else np.nan
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
    # Batch by date: all fixtures on a date use only strictly earlier-dated results.
    dates=sorted({r["date"] for r in clean})
    for current_date in dates:
        day_rows=[r for r in clean if r["date"]==current_date]
        prepared=[]
        for r in day_rows:
            d,lg,h,a=r["date"],r["league"],r["home"],r["away"]
            th,ta,lh=list(teams[(lg,h)]),list(teams[(lg,a)]),list(league_hist[lg])
            ph=list(h2h[(lg,tuple(sorted((h,a))))])
            f={"date":d,"league":lg,"home":h,"away":a,
               "league_home_avg":avg([x[0] for x in lh]),"league_away_avg":avg([x[1] for x in lh]),
               "league_total_avg":avg([x[0]+x[1] for x in lh]),
               "h2h_n":len(ph),"h2h_total_avg":avg([x[0]+x[1] for x in ph]),
               "h2h_home_goals_avg":avg([x[0] if x[2]==h else x[1] for x in ph]),
               "h2h_away_goals_avg":avg([x[1] if x[2]==h else x[0] for x in ph]),
               "h2h_btts":avg([int(x[0]>0 and x[1]>0) for x in ph]),
               "h2h_o25":avg([int(x[0]+x[1]>2) for x in ph])}
            f.update(team_feats(th,"home")); f.update(team_feats(ta,"away"))
            prepared.append((r,f))
        # Only after every fixture on this date has features, append the day's results.
        for r,f in prepared:
            built.append({**f,"result":"H" if r["hg"]>r["ag"] else "D" if r["hg"]==r["ag"] else "A",
                          "over25":int(r["hg"]+r["ag"]>2)})
            lg,h,a=r["league"],r["home"],r["away"]
            teams[(lg,h)].append((r["hg"],r["ag"])); teams[(lg,a)].append((r["ag"],r["hg"]))
            league_hist[lg].append((r["hg"],r["ag"]))
            h2h[(lg,tuple(sorted((h,a))))].append((r["hg"],r["ag"],h))
    df=pd.DataFrame(built)
    drop={"date","home","away","result","over25"}
    X=pd.get_dummies(df.drop(columns=[c for c in drop if c in df]),columns=["league"],dummy_na=True)
    numeric=list(X.columns)
    groups={
      "league_baseline":[c for c in numeric if c.startswith("league_")],
      "recent_form":[c for c in numeric if c.startswith(("home_n","home_gf","home_ga","home_gd","home_pts","home_btts","home_o25","away_n","away_gf","away_ga","away_gd","away_pts","away_btts","away_o25"))],
      "recent_plus_h2h":[c for c in numeric if c.startswith(("home_n","home_gf","home_ga","home_gd","home_pts","home_btts","home_o25","away_n","away_gf","away_ga","away_gd","away_pts","away_btts","away_o25","h2h_"))],
      "all_features":numeric}
    out=[]; audits=[]
    for win,start,end in WINDOWS:
        train=df[df.date<start]; test=df[(df.date>=start)&(df.date<=end)]
        if len(train)<1000 or len(test)<100:
            audits.append({"window":win,"status":"DATA_GATED","train_n":len(train),"test_n":len(test)})
            continue
        audits.append({"window":win,"status":"SCORED","train_n":len(train),"test_n":len(test),
                       "train_end":str(train.date.max()),"test_start":str(test.date.min()),"test_end":str(test.date.max())})
        for target in ("over25","result"):
            ytr=train[target]; yte=test[target]
            for fs,cols0 in groups.items():
                cols=[c for c in cols0 if c in X.columns]
                xt=X.loc[train.index,cols]; xv=X.loc[test.index,cols]
                models={"baseline":DummyClassifier(strategy="prior")}
                models["logistic"]=make_pipeline(SimpleImputer(strategy="median"),StandardScaler(),LogisticRegression(max_iter=1000))
                models["hist_gradient_boosting"]=make_pipeline(SimpleImputer(strategy="median"),HistGradientBoostingClassifier(max_iter=120,l2_regularization=2,random_state=41))
                for name,model in models.items():
                    try:
                        model.fit(xt,ytr); pred=model.predict(xv); probs=model.predict_proba(xv)
                        classes=list(model.classes_) if hasattr(model,"classes_") else list(model[-1].classes_)
                        row={"window":win,"test_start":start,"test_end":end,"target":target,"feature_set":fs,"model":name,
                             "train_n":len(ytr),"test_n":len(yte),"accuracy_pct":round(100*accuracy_score(yte,pred),3),
                             "balanced_accuracy_pct":round(100*balanced_accuracy_score(yte,pred),3),
                             "log_loss":round(log_loss(yte,probs,labels=classes),6)}
                        if target=="over25" and len(classes)==2:
                            row["brier_score"]=round(brier_score_loss(yte,probs[:,list(classes).index(1)]),6)
                        out.append(row)
                    except Exception as e:
                        out.append({"window":win,"test_start":start,"test_end":end,"target":target,"feature_set":fs,"model":name,
                                    "train_n":len(ytr),"test_n":len(yte),"error":str(e)[:300]})
    outdir=Path(args.out_dir); outdir.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(out).to_csv(outdir/"rolling_goal_result_validation_metrics.csv",index=False)
    audit={"artifact":"ORACLE_ROLLING_GOAL_RESULT_VALIDATION_V1","status":"EXPLORATORY_RESEARCH_ONLY",
           "production_model_changed":False,"canonical_ledgers_written":False,"source_rows":len(raw),
           "valid_unique_matches":len(df),"leagues":int(df.league.nunique()),"windows":audits,
           "features":"league scoring, team rolling form (3/5/10), prior H2H; exact league/team only",
           "notes":["Non-overlapping held-out windows: 2025 Q4, 2026 Q1, 2026-04-01 through 2026-10-16.",
                    "Features use only strictly earlier-dated matches; same-day matches are excluded.",
                    "Research classifiers are not Oracle production predictions and do not establish profitability.",
                    "H2H is tested as a feature set, not promoted; compare per-window deltas against the league baseline.",
                    "No odds or staking strategy evaluated."]}
    (outdir/"rolling_goal_result_validation_audit.json").write_text(json.dumps(audit,indent=2)+"\n")
    print(json.dumps(audit,indent=2)); print(pd.DataFrame(out).to_string(index=False))
if __name__=="__main__": main()
