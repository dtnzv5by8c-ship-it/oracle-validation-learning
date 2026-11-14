#!/usr/bin/env python3
"""Leakage-safe FootyStats team-intelligence feature challenger.

Research only. Uses FootyStats-derived historical results already persisted in the
private Oracle repository. Reconstructs point-in-time team/venue/league statistics
strictly before each OOS fixture, then evaluates incremental predictive value
against the locked Oracle OOS probabilities. Never changes Oracle V1.6.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

ROOT=Path(__file__).resolve().parents[1]
ORACLE=ROOT/"oracle"
PRED=ORACLE/"research/four_model/outputs/four_model_oos_predictions.csv"
MATCHES=ORACLE/"database/matches.csv"
FS=ORACLE/"database/major_footystats_results.csv"
OUT=ROOT/"outputs/footystats_feature_evaluation"
OUT.mkdir(parents=True,exist_ok=True)
MIN_TRAIN=500
MIN_TEST=50
EPS=1e-6

def metric(y,p):
    y=np.asarray(y,float); p=np.clip(np.asarray(p,float),EPS,1-EPS)
    auc=float(roc_auc_score(y,p)) if len(y) and len(np.unique(y))==2 else None
    return {"n":int(len(y)),"brier":float(np.mean((p-y)**2)) if len(y) else None,
            "log_loss":float(-np.mean(y*np.log(p)+(1-y)*np.log(1-p))) if len(y) else None,
            "auc":auc,"actual_rate":float(np.mean(y)) if len(y) else None,
            "mean_probability":float(np.mean(p)) if len(y) else None}

def ece(y,p,bins=10):
    y=np.asarray(y,float); p=np.asarray(p,float)
    if not len(y): return None
    edges=np.linspace(0,1,bins+1); v=0.0
    for i in range(bins):
        mask=(p>=edges[i]) & ((p<edges[i+1]) if i<bins-1 else (p<=edges[i+1]))
        if mask.any(): v += mask.mean()*abs(y[mask].mean()-p[mask].mean())
    return float(v)

def pct(values,v,higher=True):
    a=np.asarray([x for x in values if pd.notna(x)],float)
    if len(a)<2 or pd.isna(v): return np.nan
    return 100.0*float(np.sum(a<v if higher else a>v))/(len(a)-1)

def build_features(matches, fs):
    fs=fs.copy(); matches=matches.copy()
    for d in (fs,matches):
        d["date"]=pd.to_datetime(d["date"],errors="coerce")
    fs=fs.dropna(subset=["date"]).copy()
    fs["home_goals"]=pd.to_numeric(fs["home_goals"],errors="coerce")
    fs["away_goals"]=pd.to_numeric(fs["away_goals"],errors="coerce")
    fs=fs.dropna(subset=["home_goals","away_goals","league_code","home_team","away_team"])
    rows=[]
    # FootyStats result rows are treated as settled historical observations.
    for r in matches.sort_values(["date","match_id"]).itertuples(index=False):
        cutoff=pd.Timestamp(r.date)
        lg=str(r.league_code); home=str(r.home_team); away=str(r.away_team)
        prior=fs[(fs.league_code.astype(str)==lg)&(fs.date<cutoff)].copy()
        if prior.empty: continue
        team_records={}
        for team,venue in ((home,"home"),(away,"away")):
            allg=prior[(prior.home_team==team)|(prior.away_team==team)].copy()
            vg=prior[prior.home_team.eq(team) if venue=="home" else prior.away_team.eq(team)].copy()
            def agg(g):
                if g.empty: return (np.nan,np.nan,np.nan,np.nan,0)
                gf=np.where(g.home_team.eq(team),g.home_goals,g.away_goals)
                ga=np.where(g.home_team.eq(team),g.away_goals,g.home_goals)
                pts=np.where(gf>ga,3,np.where(gf==ga,1,0))
                return (float(np.mean(pts)),float(np.mean(gf)),float(np.mean(ga)),float(np.mean(gf+ga)),len(g))
            team_records[venue+"_overall"]=agg(allg); team_records[venue+"_venue"]=agg(vg)
        # League-relative comparison pool uses every team with prior FootyStats results.
        team_stats=[]
        for team in pd.unique(pd.concat([prior.home_team,prior.away_team],ignore_index=True)):
            g=prior[(prior.home_team==team)|(prior.away_team==team)]
            gf=np.where(g.home_team.eq(team),g.home_goals,g.away_goals)
            ga=np.where(g.home_team.eq(team),g.away_goals,g.home_goals)
            pts=np.where(gf>ga,3,np.where(gf==ga,1,0))
            team_stats.append({"team":team,"ppg":np.mean(pts),"gfpm":np.mean(gf),"gapm":np.mean(ga),"tgpm":np.mean(gf+ga)})
        def rel(team,scope):
            x=team_records[scope+"_overall"] if scope in ("home","away") else None
            if x is None: return {}
            ppg,gf,ga,tg,n=x
            return {
                "ppg":pct([z["ppg"] for z in team_stats],ppg,True),
                "gfpm":pct([z["gfpm"] for z in team_stats],gf,True),
                "gapm_inv":pct([z["gapm"] for z in team_stats],ga,False),
                "tgpm":pct([z["tgpm"] for z in team_stats],tg,True)
            }
        def venue_rel(team,venue):
            ppg,gf,ga,tg,n=team_records[venue+"_venue"]
            pool=[]
            for tm in pd.unique(pd.concat([prior.home_team,prior.away_team],ignore_index=True)):
                g=prior[prior.home_team.eq(tm) if venue=="home" else prior.away_team.eq(tm)]
                if g.empty: continue
                gf2=np.where(g.home_team.eq(tm),g.home_goals,g.away_goals); ga2=np.where(g.home_team.eq(tm),g.away_goals,g.home_goals)
                pts=np.where(gf2>ga2,3,np.where(gf2==ga2,1,0))
                pool.append({"ppg":np.mean(pts),"gfpm":np.mean(gf2),"gapm":np.mean(ga2),"tgpm":np.mean(gf2+ga2)})
            return {"ppg":pct([z["ppg"] for z in pool],ppg,True),"gfpm":pct([z["gfpm"] for z in pool],gf,True),"gapm_inv":pct([z["gapm"] for z in pool],ga,False),"tgpm":pct([z["tgpm"] for z in pool],tg,True)}
        f={"match_id":r.match_id,"date":cutoff,"league_code":lg}
        for side,team,venue in (("home",home,"home"),("away",away,"away")):
            o=team_records[side+"_overall"]; v=team_records[side+"_venue"]
            f[f"fs_{side}_ppg"]=o[0]; f[f"fs_{side}_gfpm"]=o[1]; f[f"fs_{side}_gapm"]=o[2]; f[f"fs_{side}_tgpm"]=o[3]; f[f"fs_{side}_n"]=o[4]
            f[f"fs_{side}_venue_ppg"]=v[0]; f[f"fs_{side}_venue_gfpm"]=v[1]; f[f"fs_{side}_venue_gapm"]=v[2]; f[f"fs_{side}_venue_tgpm"]=v[3]; f[f"fs_{side}_venue_n"]=v[4]
            ro=rel(team,side); rv=venue_rel(team,venue)
            for k,val in ro.items(): f[f"fs_{side}_rel_{k}"]=val
            for k,val in rv.items(): f[f"fs_{side}_venue_rel_{k}"]=val
        f["fs_goal_environment_score"]=np.nanmean([f["fs_home_rel_tgpm"],f["fs_away_rel_tgpm"],f["fs_home_rel_gfpm"],f["fs_away_rel_gfpm"],f["fs_home_rel_gapm_inv"],f["fs_away_rel_gapm_inv"]])
        f["fs_feature_cutoff_rule"]="strictly_before_fixture_date"
        rows.append(f)
    return pd.DataFrame(rows)

def main():
    if not PRED.exists() or not MATCHES.exists() or not FS.exists():
        raise SystemExit("BLOCKED_MISSING_FOOTYSTATS_HISTORICAL_INPUT")
    p=pd.read_csv(PRED,low_memory=False); m=pd.read_csv(MATCHES,low_memory=False); fs=pd.read_csv(FS,low_memory=False)
    req={"match_id","date","model","target"}; prob="raw_probability" if "raw_probability" in p.columns else ("probability" if "probability" in p.columns else None)
    if not req.issubset(p.columns) or not prob: raise SystemExit("BLOCKED_PRED_SCHEMA")
    m["match_id"]=m["match_id"].astype(str); p["match_id"]=p["match_id"].astype(str)
    m["date"]=pd.to_datetime(m["date"],errors="coerce"); p["date"]=pd.to_datetime(p["date"],errors="coerce")
    p["target"]=pd.to_numeric(p["target"],errors="coerce"); p["raw_p"]=pd.to_numeric(p[prob],errors="coerce")
    base=p.dropna(subset=["match_id","date","target","raw_p"]).merge(m[["match_id","league_code","home_team","away_team"]],on="match_id",how="inner",validate="many_to_one")
    feat=build_features(m[["match_id","date","league_code","home_team","away_team"]],fs)
    d=base.merge(feat,on=["match_id","date","league_code"],how="left",validate="one_to_one")
    feature_cols=[c for c in d.columns if c.startswith("fs_") and c not in {"fs_feature_cutoff_rule"} and pd.api.types.is_numeric_dtype(d[c])]
    d["feature_complete"]=d[feature_cols].notna().mean(axis=1)>=0.75
    d.to_csv(OUT/"oos_footystats_feature_join.csv",index=False)
    rows=[]; challenger_rows=[]
    for model,g in d.groupby("model",sort=True):
        g=g.sort_values(["date","match_id"]).copy()
        usable=g[g["feature_complete"]].copy()
        for c in feature_cols:
            usable[c]=pd.to_numeric(usable[c],errors="coerce")
        # Individual feature association on the full OOS sample is diagnostic only;
        # no model-selection decision is based on it.
        for c in feature_cols:
            q=usable.dropna(subset=[c])
            if len(q)>=100 and q.target.nunique()==2:
                rows.append({"model":model,"feature":c,"n":len(q),"auc":float(roc_auc_score(q.target,q[c])),"mean":float(q[c].mean())})
        for week in sorted(g.date.dt.to_period("W-MON").astype(str).unique()):
            test=g[g.date.dt.to_period("W-MON").astype(str).eq(week)].copy()
            train=g[g.date<test.date.min()].copy()
            train=train[train.feature_complete]; test=test[test.feature_complete]
            if len(train)<MIN_TRAIN or len(test)<MIN_TEST: continue
            Xtr=train[feature_cols]; Xte=test[feature_cols]
            model_pipe=Pipeline([("imp",SimpleImputer(strategy="median")),("scale",StandardScaler()),("lr",LogisticRegression(max_iter=2000,C=0.25))])
            model_pipe.fit(Xtr,train.target.astype(int))
            cp=model_pipe.predict_proba(Xte)[:,1]
            raw=metric(test.target,test.raw_p); cand=metric(test.target,cp)
            challenger_rows.append({"week":week,"model":model,"train_n":len(train),"test_n":len(test),
                "raw_brier":raw["brier"],"candidate_brier":cand["brier"],"brier_improvement":raw["brier"]-cand["brier"],
                "raw_log_loss":raw["log_loss"],"candidate_log_loss":cand["log_loss"],"log_loss_improvement":raw["log_loss"]-cand["log_loss"],
                "raw_auc":raw["auc"],"candidate_auc":cand["auc"],"auc_improvement":(cand["auc"]-raw["auc"]) if raw["auc"] is not None and cand["auc"] is not None else None,
                "raw_ece":ece(test.target,test.raw_p),"candidate_ece":ece(test.target,cp)})
    pd.DataFrame(rows).to_csv(OUT/"feature_association_diagnostics.csv",index=False)
    ch=pd.DataFrame(challenger_rows); ch.to_csv(OUT/"weekly_footystats_feature_challenger.csv",index=False)
    summary=[]
    if len(ch):
        for (model,),g in ch.groupby(["model"]):
            summary.append({"model":model,"weeks_tested":len(g),"rows_tested":int(g.test_n.sum()),
                "mean_brier_improvement":float(g.brier_improvement.mean()),"mean_log_loss_improvement":float(g.log_loss_improvement.mean()),
                "mean_auc_improvement":float(g.auc_improvement.mean()),"mean_ece_improvement":float((g.raw_ece-g.candidate_ece).mean()),
                "weeks_brier_better":int((g.brier_improvement>0).sum()),"weeks_log_loss_better":int((g.log_loss_improvement>0).sum()),
                "recommendation":"HOLD_RESEARCH_ONLY"})
    pd.DataFrame(summary).to_csv(OUT/"footystats_feature_challenger_summary.csv",index=False)
    manifest={"status":"COMPLETE_RESEARCH_ONLY","production_change":False,"feature_source":"FootyStats historical result archive",
              "pit_rule":"all FootyStats source matches have date strictly before target fixture date; same-date rows excluded",
              "feature_set":"PPG, GF/M, GA/M, total goals/match, home/away venue context, league-relative percentile scores, goal-environment score",
              "oos_rows":int(len(base)),"feature_rows":int(len(feat)),"joined_rows":int(len(d)),"complete_feature_rows":int(d.feature_complete.sum()),
              "coverage_rate":float(d.feature_complete.mean()) if len(d) else 0.0,"models":sorted(d.model.unique().tolist()) if len(d) else [],
              "no_production_promotion":True}
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps(manifest,indent=2))
if __name__=="__main__": main()
