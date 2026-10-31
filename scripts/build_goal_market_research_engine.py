#!/usr/bin/env python3
"""Experimental, walk-forward goal-market research engine. Never writes production Oracle probabilities."""
import argparse, csv, json, math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from bisect import bisect_left

SETTLED={"complete","completed","finished","ft","full time","full_time","played","after extra time","aet","penalties"}
MARKETS=("over15","over25","under45","home_over15","away_over15")

def dt(v):
    try:
        x=datetime.fromisoformat(str(v).replace("Z","+00:00"))
        return x.replace(tzinfo=timezone.utc) if x.tzinfo is None else x.astimezone(timezone.utc)
    except Exception: return None

def num(v):
    try:
        x=float(v)
        return x if math.isfinite(x) and x>=0 else None
    except Exception: return None

def valid(r):
    return (str(r.get("status_raw","")).strip().lower() in SETTLED and
            num(r.get("home_goals")) is not None and num(r.get("away_goals")) is not None and
            num(r.get("home_goals")).is_integer() and num(r.get("away_goals")).is_integer())

def key(r):
    return (str(r.get("provider_season_id","")).strip(),str(r.get("fixture_id","")).strip(),
            str(r.get("home_team_id","")).strip(),str(r.get("away_team_id","")).strip())

def build_indexes(rows):
    teams=defaultdict(list); leagues=defaultdict(list)
    for r in rows:
        d=dt(r.get("kickoff_utc")); s=str(r.get("provider_season_id","")).strip()
        h=str(r.get("home_team_id","")).strip(); a=str(r.get("away_team_id","")).strip()
        if not d or not s or not h or not a or h==a or not valid(r): continue
        x=dict(r); x["_dt"]=d; x["_season"]=s; x["_home"]=h; x["_away"]=a
        x["_hg"]=int(num(r["home_goals"])); x["_ag"]=int(num(r["away_goals"]))
        leagues[s].append(x); teams[(s,h)].append(x); teams[(s,a)].append(x)
    for index in (teams,leagues):
        for k in index: index[k].sort(key=lambda x:(x["_dt"],str(x.get("fixture_id",""))))
    return teams,leagues

def prior(index, cutoff, exclude_fixture_id=""):
    arr=index
    times=[x["_dt"] for x in arr]
    out=arr[:bisect_left(times,cutoff)]
    if exclude_fixture_id: out=[x for x in out if str(x.get("fixture_id",""))!=str(exclude_fixture_id)]
    return out

def avg(xs):
    return sum(xs)/len(xs) if xs else None

def poisson(lam, k):
    return math.exp(-lam)*lam**k/math.factorial(k)

def forecast(target, teams, leagues, cutoff):
    season=str(target.get("provider_season_id","")).strip()
    h=str(target.get("home_team_provider_id") or target.get("home_team_id") or "").strip()
    a=str(target.get("away_team_provider_id") or target.get("away_team_id") or "").strip()
    fid=str(target.get("fixture_id",""))
    if not season or not h or not a or h==a or not cutoff:
        return {"status":"BLOCKED_MISSING_EXACT_IDENTITY_OR_KICKOFF"}
    league=prior(leagues.get(season,[]),cutoff,fid)
    if len(league)<20: return {"status":"BLOCKED_LEAGUE_BASELINE_LT20","league_prior_n":len(league)}
    home=prior(teams.get((season,h),[]),cutoff,fid)
    away=prior(teams.get((season,a),[]),cutoff,fid)
    if len(home)<3 or len(away)<3:
        return {"status":"BLOCKED_TEAM_HISTORY_LT3","home_prior_n":len(home),"away_prior_n":len(away),"league_prior_n":len(league)}
    home5=home[-5:]; away5=away[-5:]
    home_venue=[x for x in home if x["_home"]==h][-5:]
    away_venue=[x for x in away if x["_away"]==a][-5:]
    # Venue split is preferred only with >=3 observations; otherwise use overall last-five.
    hsrc=home_venue if len(home_venue)>=3 else home5
    asrc=away_venue if len(away_venue)>=3 else away5
    league_h=avg([x["_hg"] for x in league]); league_a=avg([x["_ag"] for x in league])
    if not league_h or not league_a: return {"status":"BLOCKED_INVALID_LEAGUE_BASELINE","league_prior_n":len(league)}
    # Empirical-Bayes shrinkage (five pseudo-matches) stabilises small venue samples.
    def shrunk(sample, own, opp, baseline):
        n=len(sample)
        gf=sum(x[own] for x in sample); ga=sum(x[opp] for x in sample)
        return (gf+5*baseline)/(n+5),(ga+5*baseline)/(n+5)
    hgf,hga=shrunk(hsrc,"_hg","_ag",league_h)
    agf,aga=shrunk(asrc,"_ag","_hg",league_a)
    # Independent attack x opposing defensive concession multipliers around league home/away means.
    lam_h=league_h*math.sqrt(max(0.05,hgf/league_h)*max(0.05,aga/league_h))
    lam_a=league_a*math.sqrt(max(0.05,agf/league_a)*max(0.05,hga/league_a))
    lam_h=min(5.0,max(0.05,lam_h)); lam_a=min(5.0,max(0.05,lam_a))
    hp=[poisson(lam_h,k) for k in range(11)]; ap=[poisson(lam_a,k) for k in range(11)]
    # Fold the tiny Poisson tail into the 10+ bucket to preserve total probability.
    hp[-1]+=max(0.0,1-sum(hp)); ap[-1]+=max(0.0,1-sum(ap))
    joint=[(i,j,hp[i]*ap[j]) for i in range(11) for j in range(11)]
    probs={
      "over15":sum(p for i,j,p in joint if i+j>=2),
      "over25":sum(p for i,j,p in joint if i+j>=3),
      "under45":sum(p for i,j,p in joint if i+j<=4),
      "home_over15":sum(p for i,j,p in joint if i>=2),
      "away_over15":sum(p for i,j,p in joint if j>=2),
    }
    return {"status":"EXPERIMENTAL_UNCALIBRATED","home_lambda":round(lam_h,4),"away_lambda":round(lam_a,4),
      "home_overall_n":len(home5),"away_overall_n":len(away5),"home_venue_n":len(home_venue),"away_venue_n":len(away_venue),
      "league_prior_n":len(league),"home_lambda_source":"VENUE" if len(home_venue)>=3 else "OVERALL_FALLBACK",
      "away_lambda_source":"VENUE" if len(away_venue)>=3 else "OVERALL_FALLBACK",
      **{k+"_probability_pct":round(v*100,2) for k,v in probs.items()},
      "model_id":"GOAL_POISSON_SHRUNK_V0.1_RESEARCH_ONLY","production_eligible":"NO","betting_eligible":"NO"}

def outcomes(r):
    h=int(num(r["home_goals"])); a=int(num(r["away_goals"]))
    return {"over15":int(h+a>=2),"over25":int(h+a>=3),"under45":int(h+a<=4),"home_over15":int(h>=2),"away_over15":int(a>=2)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive-audit",required=True); p.add_argument("--runtime-report",required=True); p.add_argument("--out-dir",required=True)
    args=p.parse_args(); out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    with open(args.archive_audit,encoding="utf-8-sig",newline="") as f: archive=list(csv.DictReader(f))
    with open(args.runtime_report,encoding="utf-8-sig",newline="") as f: targets=list(csv.DictReader(f))
    teams,leagues=build_indexes(archive)
    output=[]
    for r in targets:
        cutoff=dt(r.get("date_utc")); pred=forecast(r,teams,leagues,cutoff)
        output.append({"fixture_id":r.get("fixture_id",""),"provider_season_id":r.get("provider_season_id",""),
          "home_team_id":r.get("home_team_provider_id",""),"away_team_id":r.get("away_team_provider_id",""),
          "fixture":f'{r.get("home_team","")} vs {r.get("away_team","")}',"kickoff_utc":r.get("date_utc",""),
          **pred,"forecast_label":"RESEARCH_ESTIMATE_NOT_ORACLE_PRODUCTION_PROBABILITY"})
    fields=list(dict.fromkeys(k for x in output for k in x))
    with open(out/"goal_market_research.csv","w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(output)
    # Chronological walk-forward validation against settled archive scores. Every target is scored
    # using only matches strictly before its kickoff; the target fixture ID is explicitly excluded.
    metrics={m:{"n":0,"brier_sum":0.0,"logloss_sum":0.0,"observed_sum":0,"predicted_sum":0.0} for m in MARKETS}
    for r in archive:
        if not valid(r): continue
        cutoff=dt(r.get("kickoff_utc"))
        if not cutoff: continue
        target={"provider_season_id":r.get("provider_season_id"),"fixture_id":r.get("fixture_id"),
          "home_team_provider_id":r.get("home_team_id"),"away_team_provider_id":r.get("away_team_id")}
        pred=forecast(target,teams,leagues,cutoff)
        if pred.get("status")!="EXPERIMENTAL_UNCALIBRATED": continue
        y=outcomes(r)
        for m in MARKETS:
            q=float(pred[m+"_probability_pct"])/100; obs=y[m]; q=min(1-1e-6,max(1e-6,q))
            z=metrics[m]; z["n"]+=1; z["brier_sum"]+=(q-obs)**2
            z["logloss_sum"]+=-(obs*math.log(q)+(1-obs)*math.log(1-q))
            z["observed_sum"]+=obs; z["predicted_sum"]+=q
    summary={}
    for m,z in metrics.items():
        n=z["n"]
        summary[m]={"n":n,"brier_score":round(z["brier_sum"]/n,5) if n else None,
          "log_loss":round(z["logloss_sum"]/n,5) if n else None,
          "observed_rate_pct":round(100*z["observed_sum"]/n,2) if n else None,
          "mean_predicted_pct":round(100*z["predicted_sum"]/n,2) if n else None,
          "calibration_status":"UNCALIBRATED_RESEARCH_ONLY"}
    blocked=sum(x.get("status")!="EXPERIMENTAL_UNCALIBRATED" for x in output)
    report={"engine":"GOAL_POISSON_SHRUNK_V0.1_RESEARCH_ONLY","forecast_rows":len(output),
      "forecastable_rows":len(output)-blocked,"blocked_rows":blocked,"backtest":summary,
      "method":"Independent Poisson score grid; five-match empirical-Bayes shrinkage; venue sample used when >=3 else overall fallback; exact season/team IDs; strict pre-kickoff; target fixture excluded.",
      "limitations":["No odds/value assessment.","No calibration fitted on a held-out calibration set.","No xG input because prematch xG temporal provenance is not verified.","Not Oracle V1.6; no production or betting eligibility.","No guarantee of accuracy; benchmark against league-rate baseline before any promotion."]}
    (out/"goal_market_research_qa.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"forecast_rows":len(output),"forecastable_rows":len(output)-blocked,"blocked_rows":blocked,"backtest":summary},indent=2))
if __name__=="__main__": main()
