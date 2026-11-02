#!/usr/bin/env python3
"""Selected-50 BTTS goal-environment ablations. Research-only; aggregate outputs only."""
from __future__ import annotations
import argparse, json
from bisect import bisect_left
from collections import defaultdict
from itertools import groupby
from pathlib import Path
import sys
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run8_full_archive_nested_ablations import (
    EXPECTED_ARCHIVE_SHA256, TRAIN_START, PRIMARY_START, PRIMARY_END, FOLDS,
    MAIN_NUMERIC, OVERALL_NUMERIC, read_archive, build_event_time_panel,
    add_eligibility_and_labels, build_model, metric_value, reliability_rows,
    paired_cluster_summary, partial_spearman, adjust_bh_by, write_csv,
)

TEAM_ENV = ["home_score_rate5","home_concede_rate5","home_btts_rate5","home_o25_rate5",
            "away_score_rate5","away_concede_rate5","away_btts_rate5","away_o25_rate5"]
VENUE_ENV = ["home_home_score_rate5","home_home_concede_rate5","home_home_btts_rate5","home_home_o25_rate5",
             "away_away_score_rate5","away_away_concede_rate5","away_away_btts_rate5","away_away_o25_rate5"]
LEAGUE_ENV = ["league_btts_rate50","league_o25_rate50","league_home_score_rate50","league_away_score_rate50"]
H2H_ENV = ["h2h_btts_rate5","h2h_o25_rate5"]
CANDIDATES = TEAM_ENV + VENUE_ENV + LEAGUE_ENV
MODELS = {
    "league_only": [],
    "overall_form_only": OVERALL_NUMERIC,
    "main_effects": MAIN_NUMERIC,
    "main_plus_team_goal_environment": MAIN_NUMERIC + TEAM_ENV,
    "main_plus_venue_goal_environment": MAIN_NUMERIC + VENUE_ENV,
    "main_plus_league_goal_environment": MAIN_NUMERIC + LEAGUE_ENV,
    "main_plus_all_goal_environment": MAIN_NUMERIC + TEAM_ENV + VENUE_ENV + LEAGUE_ENV,
}
COMPARISONS = [
    ("overall_form_vs_league_only","overall_form_only","league_only"),
    ("main_effects_vs_overall_form","main_effects","overall_form_only"),
    ("main_effects_vs_league_only","main_effects","league_only"),
    ("team_goal_environment_incremental","main_plus_team_goal_environment","main_effects"),
    ("venue_goal_environment_incremental","main_plus_venue_goal_environment","main_effects"),
    ("league_goal_environment_incremental","main_plus_league_goal_environment","main_effects"),
    ("all_goal_environment_incremental","main_plus_all_goal_environment","main_effects"),
]
METRICS = ("brier","log_loss","auc","ece10")


def prior_tail(history, cutoff, n):
    stop = bisect_left([r[0] for r in history], cutoff)
    return history[max(0, stop-n):stop]


def rate(rows, fn, minimum=5):
    return float(np.mean([fn(r) for r in rows])) if len(rows) >= minimum else np.nan


def derive_goal_environment_features(records, panel, league_min_n=50):
    """Build all goal rates from actual settled matches strictly before target kickoff."""
    targets = {(str(r.selected_id),str(r.provider_season_id),str(r.fixture_id))
               for r in panel.itertuples(index=False)}
    team, home_role, away_role, h2h, league = (
        defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list),defaultdict(list))
    feature_map = {}
    ordered = sorted(records,key=lambda r:(str(r["selected_id"]),float(r["kickoff_ts"]),str(r["fixture_id"])))
    for _, it in groupby(ordered,key=lambda r:(str(r["selected_id"]),float(r["kickoff_ts"]))):
        group=list(it); cutoff=float(group[0]["kickoff_ts"])
        # Score every target at this kickoff before appending any same-time result.
        for m in group:
            key=(str(m["selected_id"]),str(m["provider_season_id"]),str(m["fixture_id"]))
            if key not in targets: continue
            sid,h,a=str(m["selected_id"]),str(m["home_team_id"]),str(m["away_team_id"])
            ht=prior_tail(team[(sid,h)],cutoff,5); at=prior_tail(team[(sid,a)],cutoff,5)
            hh=prior_tail(home_role[(sid,h)],cutoff,5); aa=prior_tail(away_role[(sid,a)],cutoff,5)
            pair_key=(sid,tuple(sorted((h,a))))
            pair=prior_tail(h2h[pair_key],cutoff,5); lg=prior_tail(league[sid],cutoff,50)
            feature_map[key]={
                "home_score_rate5":rate(ht,lambda x:x[1]>0),
                "home_concede_rate5":rate(ht,lambda x:x[2]>0),
                "home_btts_rate5":rate(ht,lambda x:x[3]==1),
                "home_o25_rate5":rate(ht,lambda x:x[4]==1),
                "away_score_rate5":rate(at,lambda x:x[1]>0),
                "away_concede_rate5":rate(at,lambda x:x[2]>0),
                "away_btts_rate5":rate(at,lambda x:x[3]==1),
                "away_o25_rate5":rate(at,lambda x:x[4]==1),
                "home_home_score_rate5":rate(hh,lambda x:x[1]>0),
                "home_home_concede_rate5":rate(hh,lambda x:x[2]>0),
                "home_home_btts_rate5":rate(hh,lambda x:x[3]==1),
                "home_home_o25_rate5":rate(hh,lambda x:x[4]==1),
                "away_away_score_rate5":rate(aa,lambda x:x[1]>0),
                "away_away_concede_rate5":rate(aa,lambda x:x[2]>0),
                "away_away_btts_rate5":rate(aa,lambda x:x[3]==1),
                "away_away_o25_rate5":rate(aa,lambda x:x[4]==1),
                "league_btts_rate50":rate(lg,lambda x:x[3]==1,league_min_n),
                "league_o25_rate50":rate(lg,lambda x:x[4]==1,league_min_n),
                "league_home_score_rate50":rate(lg,lambda x:x[1]>0,league_min_n),
                "league_away_score_rate50":rate(lg,lambda x:x[2]>0,league_min_n),
                "h2h_btts_rate5":rate(pair,lambda x:x[1]==1),
                "h2h_o25_rate5":rate(pair,lambda x:x[2]==1),
                "home_goal_history_n":len(ht),"away_goal_history_n":len(at),
                "home_home_goal_history_n":len(hh),"away_away_goal_history_n":len(aa),
                "league_goal_history_n":len(lg),"h2h_goal_history_n":len(pair),
            }
        for m in group:
            if not m.get("settled_score"): continue
            hg,ag=int(m["home_goals"]),int(m["away_goals"])
            sid,h,a,ts=str(m["selected_id"]),str(m["home_team_id"]),str(m["away_team_id"]),float(m["kickoff_ts"])
            b,o=int(hg>0 and ag>0),int(hg+ag>2)
            # (kickoff, goals_for, goals_against, BTTS, O2.5)
            team[(sid,h)].append((ts,hg,ag,b,o)); team[(sid,a)].append((ts,ag,hg,b,o))
            pair_key=(sid,tuple(sorted((h,a))))
            h2h[pair_key].append((ts,b,o)); league[sid].append((ts,hg,ag,b,o))
            if m.get("venue_state")=="DISTINGUISHED":
                home_role[(sid,h)].append((ts,hg,ag,b,o))
                away_role[(sid,a)].append((ts,ag,hg,b,o))
    extra=pd.DataFrame(
        [feature_map.get(tuple(map(str,r)),{}) for r in panel[["selected_id","provider_season_id","fixture_id"]].itertuples(index=False,name=None)],
        index=panel.index)
    return pd.concat([panel.copy(),extra],axis=1)


def fit_predict(train,test,features):
    cols=["selected_id"]+list(features); y=train["y_BTTS"].to_numpy(dtype=int)
    if len(np.unique(y))<2: raise ValueError("Training cohort has only one BTTS outcome class")
    model=build_model(features); model.fit(train[cols],y)
    return model.predict_proba(test[cols])[:,1]


def metric_row(window,name,train,test,p):
    y=test["y_BTTS"].to_numpy(dtype=int)
    return {"window":window,"model":name,"n_train":len(train),"n_test":len(test),
            "n_leagues":int(test.selected_id.nunique()),"brier":metric_value("brier",y,p),
            "log_loss":metric_value("log_loss",y,p),"auc":metric_value("auc",y,p),
            "ece10":metric_value("ece10",y,p)}


def run_diagnostics(frame,selected_ids,archive_meta,out_dir,league_min_n=50):
    frame=add_eligibility_and_labels(frame)
    metrics,reliability,paired,tests,partial,coverage,missing=[],[],[],[],[],[],[]
    preds,h2h_preds,h2h_status={},{},{}
    for fold,start,end in FOLDS:
        raw_train=frame[(frame.kickoff_date>=TRAIN_START)&(frame.kickoff_date<start)].copy()
        raw_test=frame[(frame.kickoff_date>=start)&(frame.kickoff_date<end)].copy()
        train=raw_train[raw_train.venue_eligible].copy()
        test=raw_test[raw_test.venue_eligible].copy()
        if len(train)<100 or len(test)<30: raise ValueError(f"{fold} insufficient N train={len(train)} test={len(test)}")
        coverage.append({"window":fold,"train_raw_n":len(raw_train),"train_venue_n":len(train),
                         "test_raw_n":len(raw_test),"test_core_n":int(raw_test.core_eligible.sum()),
                         "test_venue_n":len(test),"test_h2h_n":int(raw_test.h2h_eligible.sum()),
                         "test_leagues_n":int(test.selected_id.nunique()),"test_btts_rate":float(test.y_BTTS.mean())})
        for sid in selected_ids:
            coverage.append({"window":fold+"|LEAGUE","selected_id":sid,
                             "train_venue_n":int((train.selected_id==sid).sum()),
                             "test_venue_n":int((test.selected_id==sid).sum()),
                             "test_h2h_n":int(((raw_test.selected_id==sid)&raw_test.h2h_eligible).sum())})
        for period,raw,eligible in (("TRAIN",raw_train,train),("TEST",raw_test,test)):
            for f in CANDIDATES+H2H_ENV:
                missing.append({"window":fold,"period":period,"feature":f,"raw_n":len(raw),
                                "missing_n_raw":int(raw[f].isna().sum()),
                                "missing_pct_raw":float(raw[f].isna().mean()*100) if len(raw) else np.nan,
                                "eligible_n":len(eligible),"missing_n_eligible":int(eligible[f].isna().sum()),
                                "missing_pct_eligible":float(eligible[f].isna().mean()*100) if len(eligible) else np.nan})
        for name,features in MODELS.items():
            p=fit_predict(train,test,features)
            pred=pd.DataFrame({"selected_id":test.selected_id.to_numpy(),"y":test.y_BTTS.to_numpy(dtype=int),"p":p},index=test.index)
            for f in CANDIDATES+H2H_ENV: pred[f]=test[f].to_numpy()
            preds[(fold,name)]=pred; metrics.append(metric_row(fold,name,train,test,p))
            reliability.extend(reliability_rows(pred.y,pred.p,"BTTS",name,fold))
        # H2H only on the >=5 actual prior meetings cohort.
        trh,teh=train[train.h2h_eligible].copy(),test[test.h2h_eligible].copy()
        available=len(trh)>=100 and len(teh)>=30 and trh.y_BTTS.nunique()==2
        h2h_status[fold]={"train_n":len(trh),"test_n":len(teh),"leagues_n":int(teh.selected_id.nunique()),
                          "status":"AVAILABLE" if available else "BLOCKED"}
        coverage.append({"window":fold+"|H2H_N5",**h2h_status[fold]})
        if available:
            for name,features in {"h2h_cohort_league_only":[],"h2h_cohort_main_effects":MAIN_NUMERIC,
                                  "h2h_cohort_main_plus_h2h":MAIN_NUMERIC+H2H_ENV}.items():
                p=fit_predict(trh,teh,features)
                pred=pd.DataFrame({"selected_id":teh.selected_id.to_numpy(),"y":teh.y_BTTS.to_numpy(dtype=int),"p":p},index=teh.index)
                for f in H2H_ENV: pred[f]=teh[f].to_numpy()
                h2h_preds[(fold,name)]=pred; metrics.append(metric_row(fold,name,trh,teh,p))
                reliability.extend(reliability_rows(pred.y,pred.p,"BTTS_H2H_N5",name,fold))

    for name in MODELS:
        p=pd.concat([preds[(f,name)] for f,_,_ in FOLDS]).sort_index()
        preds[("POOLED_OOS",name)]=p
        metrics.append({"window":"POOLED_OOS","model":name,"n_train":np.nan,"n_test":len(p),
                        "n_leagues":int(p.selected_id.nunique()),"brier":metric_value("brier",p.y,p.p),
                        "log_loss":metric_value("log_loss",p.y,p.p),"auc":metric_value("auc",p.y,p.p),
                        "ece10":metric_value("ece10",p.y,p.p)})
        reliability.extend(reliability_rows(p.y,p.p,"BTTS",name,"POOLED_OOS"))

    windows=[f[0] for f in FOLDS]+["POOLED_OOS"]
    for window in windows:
        for cmp,challenger,baseline in COMPARISONS:
            a,b=preds[(window,challenger)],preds[(window,baseline)]
            if not a.index.equals(b.index): raise ValueError(f"Paired cohort mismatch {window}/{cmp}")
            for metric in METRICS:
                r=paired_cluster_summary(a.y,a.p,b.p,a.selected_id,metric)
                tid=f"{window}|BTTS|{cmp}|{metric}"
                paired.append({"test_id":tid,"window":window,"market":"BTTS","comparison":cmp,
                               "challenger":challenger,"baseline":baseline,"metric":metric,"n_test":len(a),**r})
                tests.append({"test_id":tid,"test_type":"PAIRED_LEAGUE_CLUSTER","window":window,
                              "market":"BTTS","comparison":cmp,"metric":metric,"n":len(a),
                              "p_value":r["p_value_one_sided"]})

    h2h_all=all(h2h_status[f]["status"]=="AVAILABLE" for f,_,_ in FOLDS)
    if h2h_all:
        for name in ("h2h_cohort_league_only","h2h_cohort_main_effects","h2h_cohort_main_plus_h2h"):
            p=pd.concat([h2h_preds[(f,name)] for f,_,_ in FOLDS]).sort_index()
            h2h_preds[("POOLED_OOS",name)]=p
            metrics.append({"window":"POOLED_OOS","model":name,"n_train":np.nan,"n_test":len(p),
                            "n_leagues":int(p.selected_id.nunique()),"brier":metric_value("brier",p.y,p.p),
                            "log_loss":metric_value("log_loss",p.y,p.p),"auc":metric_value("auc",p.y,p.p),
                            "ece10":metric_value("ece10",p.y,p.p)})
            reliability.extend(reliability_rows(p.y,p.p,"BTTS_H2H_N5",name,"POOLED_OOS"))
        for window in windows:
            for cmp,challenger,baseline in [
                ("h2h_main_vs_league","h2h_cohort_main_effects","h2h_cohort_league_only"),
                ("h2h_incremental_vs_main","h2h_cohort_main_plus_h2h","h2h_cohort_main_effects")]:
                a,b=h2h_preds[(window,challenger)],h2h_preds[(window,baseline)]
                for metric in METRICS:
                    r=paired_cluster_summary(a.y,a.p,b.p,a.selected_id,metric)
                    tid=f"{window}|BTTS_H2H_N5|{cmp}|{metric}"
                    paired.append({"test_id":tid,"window":window,"market":"BTTS_H2H_N5","comparison":cmp,
                                   "challenger":challenger,"baseline":baseline,"metric":metric,"n_test":len(a),**r})
                    tests.append({"test_id":tid,"test_type":"PAIRED_LEAGUE_CLUSTER","window":window,
                                  "market":"BTTS_H2H_N5","comparison":cmp,"metric":metric,"n":len(a),
                                  "p_value":r["p_value_one_sided"]})

    pm=preds[("POOLED_OOS","main_effects")]; mp=frame.loc[pm.index]
    for feature in CANDIDATES:
        r=partial_spearman(pm.y.to_numpy(float),mp[feature].to_numpy(float),
                           {c:mp[c].to_numpy(float) for c in MAIN_NUMERIC},pm.selected_id.to_numpy(str))
        tid=f"POOLED_OOS|BTTS|PARTIAL_SPEARMAN|{feature}"
        partial.append({"test_id":tid,"feature":feature,**r})
        tests.append({"test_id":tid,"test_type":"PARTIAL_SPEARMAN_CONTROL_MAIN_EFFECTS_AND_LEAGUE",
                      "window":"POOLED_OOS","market":"BTTS","comparison":feature,
                      "metric":"partial_spearman","n":r["n"],"p_value":r["p_value_two_sided"]})
    if h2h_all:
        ph=h2h_preds[("POOLED_OOS","h2h_cohort_main_effects")]; hp=frame.loc[ph.index]
        for feature in H2H_ENV:
            r=partial_spearman(ph.y.to_numpy(float),hp[feature].to_numpy(float),
                               {c:hp[c].to_numpy(float) for c in MAIN_NUMERIC},ph.selected_id.to_numpy(str))
            tid=f"POOLED_OOS|BTTS_H2H_N5|PARTIAL_SPEARMAN|{feature}"
            partial.append({"test_id":tid,"feature":feature,**r})
            tests.append({"test_id":tid,"test_type":"PARTIAL_SPEARMAN_CONTROL_MAIN_EFFECTS_AND_LEAGUE",
                          "window":"POOLED_OOS","market":"BTTS_H2H_N5","comparison":feature,
                          "metric":"partial_spearman","n":r["n"],"p_value":r["p_value_two_sided"]})

    bh,by=adjust_bh_by([r["p_value"] for r in tests])
    for i,r in enumerate(tests):
        r["q_value_bh"]=float(bh[i]) if np.isfinite(bh[i]) else np.nan
        r["q_value_by"]=float(by[i]) if np.isfinite(by[i]) else np.nan

    primary=frame[(frame.kickoff_date>=PRIMARY_START)&(frame.kickoff_date<=PRIMARY_END)]
    core,venue=primary[primary.core_eligible],primary[primary.venue_eligible]
    h2h=venue[venue.h2h_eligible]
    for sid in selected_ids:
        coverage.append({"window":"POOLED_OOS|LEAGUE","selected_id":sid,
                         "raw_primary_n":int((primary.selected_id==sid).sum()),
                         "core_5plus_n":int((core.selected_id==sid).sum()),
                         "venue_5plus_n":int((venue.selected_id==sid).sum()),
                         "h2h_5plus_n":int((h2h.selected_id==sid).sum())})
    coverage.append({"window":"POOLED_OOS","raw_primary_n":len(primary),"core_5plus_n":len(core),
                     "venue_5plus_n":len(venue),"h2h_5plus_n":len(h2h),
                     "venue_leagues_n":int(venue.selected_id.nunique()),
                     "h2h_leagues_n":int(h2h.selected_id.nunique()),
                     "btts_rate_venue_eligible":float(venue.y_BTTS.mean()) if len(venue) else np.nan})

    out=Path(out_dir); out.mkdir(parents=True,exist_ok=True)
    write_csv(out/"fold_metrics.csv",metrics); write_csv(out/"paired_confidence_intervals.csv",paired)
    write_csv(out/"multiplicity_bh_by.csv",tests); write_csv(out/"partial_spearman.csv",partial)
    write_csv(out/"reliability_bins.csv",reliability); write_csv(out/"fold_and_league_coverage.csv",coverage)
    write_csv(out/"feature_missingness.csv",missing)
    summary={
        "run":"ORACLE_SELECTED50_BTTS_GOAL_ENVIRONMENT_ABLATIONS_RUN10","archive":archive_meta,
        "population":{"panel_rows":len(frame),"primary_raw_n":len(primary),"core_5plus_n":len(core),
                      "venue_5plus_n":len(venue),"h2h_5plus_n":len(h2h),
                      "venue_leagues_n":int(venue.selected_id.nunique()),"h2h_leagues_n":int(h2h.selected_id.nunique())},
        "folds":[{"name":f,"train_start":TRAIN_START.isoformat(),"test_start":s.isoformat(),
                  "test_end_exclusive":e.isoformat()} for f,s,e in FOLDS],
        "method":{"event_time":"strict earlier kickoff; same-kickoff results appended after all targets",
                  "overall_minimum":"five actual settled score-complete prior matches per team",
                  "venue_minimum":"five explicit home-role and away-role matches",
                  "h2h_minimum":"five actual prior pair meetings; H2H cohort only",
                  "league_environment_minimum":league_min_n,"pseudo_counts":False,"calibration":"none",
                  "estimator":"LogisticRegression(C=0.1, LBFGS, max_iter=2500); train-only median imputation/standardisation",
                  "hyperparameter_tuning":"none"},
        "models":MODELS,"h2h_fold_status":h2h_status,
        "multiplicity":{"joint_test_family_n":len(tests),
                        "bh_q_lt_0_05":sum(np.isfinite(r["q_value_bh"]) and r["q_value_bh"]<0.05 for r in tests),
                        "by_q_lt_0_05":sum(np.isfinite(r["q_value_by"]) and r["q_value_by"]<0.05 for r in tests)},
        "oracle_v16_baseline":{"status":"BLOCKED_NO_MATCHING_HISTORICAL_FIXTURE_LEVEL_V1_6_LEDGER",
                               "reason":"No matching frozen V1.6 BTTS probabilities, prediction timestamps and settlement truth; no challenger substituted."},
        "original_run8_assets":{"workbook_recovered":False,
            "workbook_sha256":"66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7",
            "companion_bundle_recovered":False,
            "companion_bundle_sha256":"b44e99c3ee9b1e1e4515739d810ec10b0bab1c8c718ef2918ec3f1bf78a08e2f",
            "rebuild_archive_sha256":EXPECTED_ARCHIVE_SHA256},
        "provenance_limits":{"provider_publication_timestamps_verified":False,
                             "official_settlement_verified":False,"xg_used":False,"provisional_standings_used":False},
        "governance":{"provider_api_credits_used":0,"raw_provider_rows_exported":False,
                      "fixture_predictions_exported":False,"feature_panel_exported":False,
                      "production_logic_changed":False,"production_probabilities_changed":False,
                      "canonical_ledgers_changed":False,"production_workflows_changed":False,
                      "production_eligible":False,"betting_eligible":False}}
    (out/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True,default=str)+"\n",encoding="utf-8")
    return summary


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True); p.add_argument("--selected-manifest",required=True)
    p.add_argument("--out",required=True); p.add_argument("--league-min-n",type=int,default=50)
    a=p.parse_args()
    records,selected_ids,meta=read_archive(a.archive,a.selected_manifest,EXPECTED_ARCHIVE_SHA256)
    panel=build_event_time_panel(records,PRIMARY_START,PRIMARY_END,lag_hours=0.0)
    panel=derive_goal_environment_features(records,panel,a.league_min_n)
    summary=run_diagnostics(panel,selected_ids,meta,a.out,a.league_min_n)
    print(json.dumps({"status":"COMPLETED_RESEARCH_ONLY","population":summary["population"],
                      "multiplicity":summary["multiplicity"],"archive_sha256":meta["archive_sha256"]},indent=2))


if __name__=="__main__":
    main()
