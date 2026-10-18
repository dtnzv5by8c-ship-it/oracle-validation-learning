#!/usr/bin/env python3
"""Reporting-only league/market and team-context audit of settled shadow predictions.
Never writes to the governed Oracle prediction or settlement ledgers."""
import argparse, csv, json
from pathlib import Path
import numpy as np
import pandas as pd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--settlements",required=True)
    ap.add_argument("--out-dir",required=True)
    ap.add_argument("--min-team-fixtures",type=int,default=8)
    ap.add_argument("--min-league-market",type=int,default=20)
    a=ap.parse_args()
    d=pd.read_csv(a.settlements)
    required={"fixture_id","competition","home_team","away_team","market","raw_probability","actual_truth","prediction_hit","settlement_status","model_status","decision","final_home_score","final_away_score"}
    if required-set(d.columns): raise SystemExit("DATA_GATED: shadow settlement file missing required columns")
    d=d[d.settlement_status.eq("SETTLED")].copy()
    if d.empty: raise SystemExit("DATA_GATED: no settled shadow prediction rows")
    for c in ("raw_probability","actual_truth","prediction_hit","final_home_score","final_away_score"):
        d[c]=pd.to_numeric(d[c],errors="coerce")
    d=d.dropna(subset=["raw_probability","actual_truth","prediction_hit"])
    # Explicitly retain the challenger/shadow identity. Never label this production Oracle accuracy.
    d["source_class"]="CHALLENGER_SHADOW_NOT_PRODUCTION"
    d["brier"]=(d.raw_probability-d.actual_truth)**2
    eps=1e-15
    p=d.raw_probability.clip(eps,1-eps)
    d["logloss"]=-(d.actual_truth*np.log(p)+(1-d.actual_truth)*np.log(1-p))
    outdir=Path(a.out_dir); outdir.mkdir(parents=True,exist_ok=True)

    def summarize(g, keys, fixture_col="fixture_id"):
        rows=[]
        for key, x in g.groupby(keys,dropna=False):
            if not isinstance(key,tuple): key=(key,)
            r=dict(zip(keys,key))
            r.update({"source_class":"CHALLENGER_SHADOW_NOT_PRODUCTION",
              "fixture_count":int(x[fixture_col].nunique()),
              "prediction_rows":int(len(x)),
              "accuracy_pct":round(100*x.prediction_hit.mean(),2),
              "mean_predicted_probability_pct":round(100*x.raw_probability.mean(),2),
              "observed_market_truth_pct":round(100*x.actual_truth.mean(),2),
              "brier_score":round(x.brier.mean(),5),"log_loss":round(x.logloss.mean(),5),
              "non_no_bet_rows":int((~x.decision.astype(str).str.upper().eq("NO_BET")).sum()),
              "non_no_bet_hit_rate_pct":round(100*x.loc[~x.decision.astype(str).str.upper().eq("NO_BET"),"prediction_hit"].mean(),2) if (~x.decision.astype(str).str.upper().eq("NO_BET")).any() else np.nan})
            rows.append(r)
        return pd.DataFrame(rows)

    lm=summarize(d,["competition","market"])
    lm["evidence_status"]=np.where(lm.fixture_count>=a.min_league_market,"SAMPLE_GATE_MET_FOR_REVIEW","LOW_SAMPLE_NOT_RANKABLE")
    lm.sort_values(["competition","market"]).to_csv(outdir/"league_market_shadow_scorecard.csv",index=False)

    # Team-context audit attributes each match-market row to the named team in its home/away role.
    # This is association with match-level market forecasts, not a team-specific model probability.
    team_rows=[]
    for role, team_col in (("HOME","home_team"),("AWAY","away_team")):
        z=d.copy()
        z["team_role"]=role
        z["team"]=z[team_col].astype(str)
        team_rows.append(z)
    td=pd.concat(team_rows,ignore_index=True)
    tm=summarize(td,["competition","team","team_role","market"])
    tm["alignment_status"]=np.where(tm.fixture_count>=a.min_team_fixtures,
        np.where(tm.accuracy_pct>=60,"PROVISIONAL_ALIGNED",np.where(tm.accuracy_pct<45,"PROVISIONAL_DIVERGENT","MIXED_OR_UNCLEAR")),
        "INSUFFICIENT_SAMPLE")
    tm["interpretation_limit"]="Match-market forecast outcome for fixtures involving this team in this role; not an individual team-goal prediction."
    tm.sort_values(["competition","market","fixture_count","accuracy_pct"],ascending=[True,True,False,False]).to_csv(outdir/"team_market_shadow_alignment.csv",index=False)

    # Actual score context only; no goal forecast exists in the shadow ledger, so no goal prediction residual is claimed.
    scores=d.drop_duplicates(["fixture_id"])[["fixture_id","competition","home_team","away_team","final_home_score","final_away_score"]].copy()
    scores["final_home_score"]=pd.to_numeric(scores.final_home_score,errors="coerce")
    scores["final_away_score"]=pd.to_numeric(scores.final_away_score,errors="coerce")
    home=scores.rename(columns={"home_team":"team","final_home_score":"goals_for","final_away_score":"goals_against"})[["competition","team","goals_for","goals_against"]]
    away=scores.rename(columns={"away_team":"team","final_away_score":"goals_for","final_home_score":"goals_against"})[["competition","team","goals_for","goals_against"]]
    goals=pd.concat([home,away]).groupby(["competition","team"],as_index=False).agg(fixtures=("team","size"),actual_goals_for_avg=("goals_for","mean"),actual_goals_against_avg=("goals_against","mean"))
    goals["status"]=np.where(goals.fixtures>=a.min_team_fixtures,"DESCRIPTIVE_ONLY_REVIEW","LOW_SAMPLE")
    goals.to_csv(outdir/"team_actual_goals_context.csv",index=False,float_format="%.3f")
    counts=d.groupby("model_status").size().to_dict()
    audit={"artifact":"ORACLE_SHADOW_LEAGUE_TEAM_ALIGNMENT_AUDIT_V1","status":"DESCRIPTIVE_SHADOW_AUDIT",
      "source_class":"CHALLENGER_SHADOW_NOT_PRODUCTION","production_model_changed":False,"canonical_ledgers_written":False,
      "settled_prediction_rows":int(len(d)),"unique_fixtures":int(d.fixture_id.nunique()),
      "competitions":int(d.competition.nunique()),"markets":sorted(d.market.dropna().unique().tolist()),
      "model_status_counts":{str(k):int(v) for k,v in counts.items()},
      "league_market_groups":int(len(lm)),"league_market_groups_low_sample":int((lm.fixture_count<a.min_league_market).sum()),
      "team_market_groups":int(len(tm)),"team_market_groups_insufficient_sample":int((tm.fixture_count<a.min_team_fixtures).sum()),
      "min_team_fixtures":a.min_team_fixtures,"min_league_market_fixtures":a.min_league_market,
      "limitations":["The governed canonical settlement ledger is empty; this audit uses the isolated shadow-settlement artifact.",
       "Shadow predictions are challenger records, not production Oracle prediction accuracy.",
       "The current cohort is only 42 fixtures across 9 competitions; league-market and team samples are too small for durable rankings.",
       "Team-level rows describe match-market predictions in fixtures involving the team, not a team-specific probability forecast.",
       "The shadow ledger has no predicted home/away goal counts; team goal residuals cannot be calculated.",
       "No odds/staking strategy or profitability was evaluated."]}
    (outdir/"shadow_league_team_alignment_audit.json").write_text(json.dumps(audit,indent=2)+"\n")
    print(json.dumps(audit,indent=2))
if __name__=="__main__": main()
