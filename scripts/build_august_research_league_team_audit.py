#!/usr/bin/env python3
"""Descriptive audit of the August 2026 fixture-level research prediction export.
This file lacks immutable prediction timestamps/feature hashes, so outputs are not a production-grade Oracle backtest."""
import argparse, csv, json
from pathlib import Path
import numpy as np
import pandas as pd

MARKETS=[
 ("BTTS","BTTS_y","prob_BTTS","pred_BTTS"),
 ("DC_HOME","DC_HOME_y","prob_DC_HOME","pred_DC_HOME"),
 ("DC_AWAY","DC_AWAY_y","prob_DC_AWAY","pred_DC_AWAY"),
 ("OVER15","OVER15_y","prob_OVER15","pred_OVER15"),
 ("OVER25","OVER25_y","prob_OVER25","pred_OVER25"),
 ("UNDER15","UNDER15_y","prob_UNDER15","pred_UNDER15"),
 ("UNDER25","UNDER25_y","prob_UNDER25","pred_UNDER25"),
 ("UNDER35","UNDER35_y","prob_UNDER35","pred_UNDER35"),
 ("UNDER45","UNDER45_y","prob_UNDER45","pred_UNDER45"),
 ("UNDER55","UNDER55_y","prob_UNDER55","pred_UNDER55"),
 ("COMBO_HOME","COMBO_HOME_y","prob_COMBO_HOME","pred_COMBO_HOME"),
 ("COMBO_AWAY","COMBO_AWAY_y","prob_COMBO_AWAY","pred_COMBO_AWAY"),
]

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--predictions",required=True)
 ap.add_argument("--out-dir",required=True)
 ap.add_argument("--min-team-fixtures",type=int,default=8)
 ap.add_argument("--min-league-market",type=int,default=15)
 a=ap.parse_args()
 d=pd.read_csv(a.predictions)
 required={"match_id","date","league_code","home_team","away_team","status"}
 for _,y,predp,pred in MARKETS: required|={y,predp,pred}
 if required-set(d.columns): raise SystemExit("DATA_GATED: August research export missing required columns")
 raw_rows=len(d)
 d=d[d.status.eq("PREDICTED")].copy()
 for _,y,predp,pred in MARKETS:
  for c in (y,predp,pred): d[c]=pd.to_numeric(d[c],errors="coerce")
 out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True)
 rows=[]
 for market,ycol,pcol,prcol in MARKETS:
  z=d.dropna(subset=[ycol,pcol,prcol]).copy()
  if z.empty: continue
  p=z[pcol].clip(1e-15,1-1e-15); truth=z[ycol]
  z["_hit"]=(z[prcol]==truth).astype(int); z["_brier"]=(z[p]-truth)**2
  z["_logloss"]=-(truth*np.log(p)+(1-truth)*np.log(1-p))
  rows.append({"market":market,"fixtures":int(z.match_id.nunique()),"prediction_rows":len(z),
   "accuracy_pct":round(100*z["_hit"].mean(),2),"brier_score":round(z["_brier"].mean(),5),"log_loss":round(z["_logloss"].mean(),5),
   "mean_predicted_probability_pct":round(100*z[pcol].mean(),2),"observed_truth_pct":round(100*truth.mean(),2),
   "source_class":"AUGUST_RESEARCH_EXPORT_PROVENANCE_INCOMPLETE"})
 overall=pd.DataFrame(rows); overall.to_csv(out/"august_research_market_scorecard.csv",index=False)
 lm=[]; tm=[]
 for market,ycol,pcol,prcol in MARKETS:
  z=d.dropna(subset=[ycol,pcol,prcol]).copy()
  p=z[pcol].clip(1e-15,1-1e-15); truth=z[ycol]
  z["_hit"]=(z[prcol]==truth).astype(int); z["_brier"]=(p-truth)**2
  z["_logloss"]=-(truth*np.log(p)+(1-truth)*np.log(1-p))
  for league,g in z.groupby("league_code"):
   lm.append({"league_code":league,"market":market,"fixtures":int(g.match_id.nunique()),"accuracy_pct":round(100*g["_hit"].mean(),2),
    "brier_score":round(g["_brier"].mean(),5),"log_loss":round(g["_logloss"].mean(),5),
    "evidence_status":"DESCRIPTIVE_ONLY" if g.match_id.nunique()>=a.min_league_market else "LOW_SAMPLE"})
  for role,teamcol in (("HOME","home_team"),("AWAY","away_team")):
   for (league,team),g in z.groupby(["league_code",teamcol]):
    n=int(g.match_id.nunique())
    tm.append({"league_code":league,"team":team,"team_role":role,"market":market,"fixtures":n,
     "accuracy_pct":round(100*g["_hit"].mean(),2),"brier_score":round(g["_brier"].mean(),5),"log_loss":round(g["_logloss"].mean(),5),
     "mean_predicted_probability_pct":round(100*g[pcol].mean(),2),"observed_truth_pct":round(100*g[ycol].mean(),2),
     "alignment_status":"INSUFFICIENT_SAMPLE" if n<a.min_team_fixtures else ("PROVISIONAL_ALIGNED" if g["_hit"].mean()>=.60 else "PROVISIONAL_DIVERGENT" if g["_hit"].mean()<.45 else "MIXED_OR_UNCLEAR")})
 pd.DataFrame(lm).sort_values(["league_code","market"]).to_csv(out/"august_research_league_market_scorecard.csv",index=False)
 pd.DataFrame(tm).sort_values(["league_code","market","fixtures","accuracy_pct"],ascending=[True,True,False,False]).to_csv(out/"august_research_team_alignment.csv",index=False)
 audit={"artifact":"ORACLE_AUGUST_RESEARCH_LEAGUE_TEAM_AUDIT_V1","status":"DESCRIPTIVE_RESEARCH_ONLY",
  "source_file":"research/august_2026_backtest/august_2026_predictions.csv","raw_rows":raw_rows,
  "predicted_rows":int(len(d)),"excluded_data_gated_rows":int(raw_rows-len(d)),
  "unique_fixtures":int(d.match_id.nunique()),"leagues":int(d.league_code.nunique()),"markets":len(MARKETS),
  "min_team_fixtures":a.min_team_fixtures,"min_league_market_fixtures":a.min_league_market,
  "production_model_changed":False,"canonical_ledgers_written":False,
  "limitations":["This August export has no immutable per-row prediction timestamp, feature snapshot hash, or fully paired production ledger provenance.",
   "Scores are descriptive research-file metrics and must not be called production Oracle accuracy or profitability.",
   "Team labels below the sample threshold remain INSUFFICIENT_SAMPLE; one month is not enough for durable team DNA.",
   "The export has market probabilities but no predicted home/away goal counts, so exact goal-count residuals cannot be computed.",
   "No odds or staking rule were evaluated."]}
 (out/"august_research_league_team_audit.json").write_text(json.dumps(audit,indent=2)+"\n")
 print(json.dumps(audit,indent=2)); print(overall.to_string(index=False))
if __name__=="__main__": main()
