#!/usr/bin/env python3
"""Research-only uncertainty audit for aggregate Selected-50 league walk-forward metrics.

Reads only aggregate chronological league folds and the readiness table. It does not
load the locked H2H paired holdout, rank teams, or grant betting eligibility.
"""
import argparse, csv, json, statistics
from collections import defaultdict
from pathlib import Path

MARKETS={"BTTS","DC_HOME","DC_AWAY"}

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def number(value):
    try:
        x=float(value)
        return x if x==x and abs(x)!=float("inf") else None
    except (TypeError,ValueError):
        return None

def write_csv(path, rows):
    fields=list(rows[0]) if rows else []
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir",required=True,type=Path)
    ap.add_argument("--output-dir",required=True,type=Path)
    args=ap.parse_args(); args.output_dir.mkdir(parents=True,exist_ok=True)
    folds=[r for r in read_csv(args.input_dir/"oracle_selected50_league_walk_forward_metrics.csv") if r.get("market") in MARKETS]
    readiness=[r for r in read_csv(args.input_dir/"oracle_selected50_league_market_readiness.csv") if r.get("market") in MARKETS]
    rmap={(r.get("selected_id"),r.get("market")):r for r in readiness}
    groups=defaultdict(list)
    for r in folds: groups[(r.get("selected_id"),r.get("market"))].append(r)
    output=[]
    for key,rows in groups.items():
        rows=sorted(rows,key=lambda r:r.get("fold","")); first=rows[0]
        skill=[number(r.get("brier_skill_vs_league_prevalence")) for r in rows]
        skill=[x for x in skill if x is not None]
        ece=[number(r.get("ece_10_bins")) for r in rows]; ece=[x for x in ece if x is not None]
        widths=[]
        for r in rows:
            lo,hi=number(r.get("accuracy_95ci_low")),number(r.get("accuracy_95ci_high"))
            if lo is not None and hi is not None: widths.append(hi-lo)
        train=[int(number(r.get("train_n")) or 0) for r in rows]
        test=[int(number(r.get("test_n")) or 0) for r in rows]
        gates=sum(r.get("sample_gate")=="SAMPLE_GATE_MET_DIAGNOSTIC_ONLY" for r in rows)
        positive=sum(x>0 for x in skill)
        max_ece=max(ece) if ece else None
        if len(rows)==3 and gates==3 and positive==3: disposition="RETEST_CANDIDATE_NOT_APPROVED"
        elif len(rows)<3 or gates<3: disposition="INSUFFICIENT_CHRONOLOGICAL_SUPPORT"
        else: disposition="MIXED_OR_NONPOSITIVE_SKILL"
        if disposition!="RETEST_CANDIDATE_NOT_APPROVED": cal_note="NOT_A_CANDIDATE_UNDER_CURRENT_RULE"
        elif max_ece is not None and max_ece>=.10: cal_note="AT_LEAST_ONE_FOLD_ECE_GE_0.10_REVIEW_CALIBRATION"
        elif max_ece is not None and max_ece>=.05: cal_note="FOLD_ECE_RANGE_REQUIRES_REVIEW"
        else: cal_note="LOWER_OBSERVED_ECE_BUT_STILL_UNCALIBRATED"
        rr=rmap.get(key,{})
        output.append({
          "selected_id":key[0],"country":first.get("country",""),"league":first.get("league",""),"market":key[1],
          "folds_observed":len(rows),"sample_gate_pass_folds":gates,"train_n_min":min(train) if train else 0,
          "test_n_min":min(test) if test else 0,"test_n_total_across_folds":sum(test),
          "positive_brier_skill_folds":positive,"brier_skill_min":round(min(skill),6) if skill else "",
          "brier_skill_median":round(statistics.median(skill),6) if skill else "",
          "brier_skill_max":round(max(skill),6) if skill else "",
          "ece_median":round(statistics.median(ece),6) if ece else "",
          "ece_max":round(max_ece,6) if max_ece is not None else "",
          "accuracy_95ci_width_median":round(statistics.median(widths),6) if widths else "",
          "accuracy_95ci_width_max":round(max(widths),6) if widths else "",
          "readiness_status":rr.get("fold_stability_status",""),"research_disposition":disposition,
          "calibration_diagnostic":cal_note,
          "selection_bias_note":"150 league-market hypotheses screened; no multiplicity-adjusted inference",
          "production_eligible":"NO","betting_eligibility":"NOT_ASSESSED"})
    output.sort(key=lambda r:(r["market"],r["research_disposition"],-(number(r["brier_skill_min"]) or -999),r["country"],r["league"]))
    write_csv(args.output_dir/"oracle_selected50_market_screen_uncertainty_audit.csv",output)
    summary={"status":"RESEARCH_ONLY_MARKET_SCREEN_UNCERTAINTY_AUDIT","source":"Run #168 aggregate league walk-forward metrics and readiness table",
      "locked_h2h_paired_holdout_loaded":False,"total_league_market_pairs":len(output),
      "selection_bias":"150 hypotheses (50 league groups x 3 markets); no Brier-skill confidence intervals or multiplicity-adjusted inference in source artifact.",
      "interpretation":"Candidate means positive Brier skill versus league prevalence in all three folds with the existing sample gate. It does not mean calibrated, profitable, canonical-identity verified or approved for betting.","markets":{}}
    for market in sorted(MARKETS):
        rows=[r for r in output if r["market"]==market]
        cand=[r for r in rows if r["research_disposition"]=="RETEST_CANDIDATE_NOT_APPROVED"]
        summary["markets"][market]={
          "league_market_pairs":len(rows),
          "three_fold_sample_gate_pass":sum(r["folds_observed"]==3 and r["sample_gate_pass_folds"]==3 for r in rows),
          "positive_brier_skill_all_three_folds":len(cand),
          "candidate_max_ece_ge_0_10":sum((number(r["ece_max"]) or 0)>=.10 for r in cand),
          "candidate_max_ece_0_05_to_below_0_10":sum(.05<=(number(r["ece_max"]) or 0)<.10 for r in cand),
          "candidate_max_ece_below_0_05":sum((number(r["ece_max"]) or 0)<.05 for r in cand),
          "median_candidate_min_fold_brier_skill":round(statistics.median([number(r["brier_skill_min"]) for r in cand]),6) if cand else None,
          "median_candidate_accuracy_ci_width":round(statistics.median([number(r["accuracy_95ci_width_median"]) for r in cand]),6) if cand else None,
          "top_three_by_worst_fold_brier_skill":[
            {"league":r["country"]+" — "+r["league"],"min_fold_brier_skill":r["brier_skill_min"],
             "median_fold_ece":r["ece_median"],"max_fold_ece":r["ece_max"],"minimum_test_n":r["test_n_min"],
             "calibration_diagnostic":r["calibration_diagnostic"]}
            for r in sorted(cand,key=lambda z:(-(number(z["brier_skill_min"]) or -999),number(z["ece_max"]) or 999))[:3]]}
    (args.output_dir/"oracle_selected50_market_screen_uncertainty_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
