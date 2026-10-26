#!/usr/bin/env python3
"""Audit pinned sanitized Selected-50 aggregate walk-forward metrics only."""
from __future__ import annotations
import csv, json, math, re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"/"selected50_walk_forward_snapshot"
OUT=ROOT/"audit-output"; OUT.mkdir(parents=True,exist_ok=True)
MARKETS={"BTTS","DC_HOME","DC_AWAY","COMBO_HOME","COMBO_AWAY"}
FOLDS=["WF1_2025-03-20_to_2025-09-20","WF2_2025-09-20_to_2026-03-20","WF3_2026-03-20_to_2026-09-20"]
ARTIFACT_SHA="a7d17ff2e058bcf2a8a70f7f280c8ed821f11aa8ca7d8262b45e9f74a25b877d"

def read_json(path):
    if not path.is_file(): raise AssertionError(f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))
def read_csv(path):
    if not path.is_file(): raise AssertionError(f"Missing file: {path}")
    with path.open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f))
def number(row,key,lo=None,hi=None):
    raw=row.get(key)
    if raw in (None,""): raise AssertionError(f"Missing numeric field {key}")
    x=float(raw)
    if not math.isfinite(x): raise AssertionError(f"Non-finite field {key}")
    if lo is not None and x<lo: raise AssertionError(f"{key} below range")
    if hi is not None and x>hi: raise AssertionError(f"{key} above range")
    return x
def wilson(k,n,z=1.959963984540054):
    p=k/n; den=1+z*z/n; center=(p+z*z/(2*n))/den
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return center-half,center+half
def fold_dates(label):
    m=re.fullmatch(r"WF[1-3]_(\d{4}-\d{2}-\d{2})_to_(\d{4}-\d{2}-\d{2})",label)
    if not m: raise AssertionError(f"Invalid fold label: {label}")
    start,end=date.fromisoformat(m.group(1)),date.fromisoformat(m.group(2))
    if start>=end: raise AssertionError(f"Fold start must precede end: {label}")
    return start,end
def validate_folds(rows,design):
    assert len(rows)==15 and {r["market"] for r in rows}==MARKETS
    grouped=defaultdict(list)
    for r in rows: grouped[r["market"]].append(r)
    for market,rs in grouped.items():
        assert [r["fold"] for r in rs]==FOLDS
        ranges=[fold_dates(r["fold"]) for r in rs]
        assert ranges[0][1]==ranges[1][0] and ranges[1][1]==ranges[2][0]
        assert ranges[0][0]<ranges[0][1]<ranges[1][1]<ranges[2][1]
        for i,r in enumerate(rs):
            assert r["status"]=="RAW_WALK_FORWARD_NOT_CALIBRATED"
            train,test=int(r["train_n"]),int(r["test_n"]); assert train>0 and test>0
            acc=number(r,"accuracy_at_0_5",0,1); low=number(r,"accuracy_95ci_low",0,1); high=number(r,"accuracy_95ci_high",0,1)
            assert low<=acc<=high
            k=round(acc*test); assert abs(k/test-acc)<=0.00002
            wl,wh=wilson(k,test); assert abs(wl-low)<=0.00002 and abs(wh-high)<=0.00002
            b=number(r,"brier",0,1); base=number(r,"baseline_brier",0); skill=number(r,"brier_skill_vs_prevalence")
            assert base>0 and abs(skill-(1-b/base))<=0.0001
            number(r,"log_loss",0); number(r,"auc",0,1); number(r,"ece_10_bins",0,1); number(r,"training_prevalence",0,1)
            if i: assert train==int(rs[i-1]["train_n"])+int(rs[i-1]["test_n"]),(market,r["fold"])
    assert "Expanding-window rolling-origin" in design and "strictly before" in design and "no calibration or tuning" in design.lower()
    return grouped
def audit_snapshot():
    meta=read_json(DATA/"metadata.json"); rows=read_csv(DATA/"aggregate_folds.csv"); src=meta["source"]
    assert src["repository"]=="dtnzv5by8c-ship-it/oracle-validation-learning"
    assert src["branch"]=="research/oracle-50-league-readiness-audit"
    assert src["runtime_run_id"]==40238357851 and src["artifact_id"]==12615034595
    assert src["artifact_sha256"]==ARTIFACT_SHA==src["artifact_expected_sha256"]
    assert meta["runtime_validation"]["status"]=="PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT"
    assert meta["runtime_validation"]["production_eligible"] is False and meta["runtime_validation"]["betting_eligible"] is False
    grouped=validate_folds(rows,meta["fold_design"]); gqa=meta["governed_fixture_qa"]
    assert gqa["all_rows_production_ineligible"] is True and gqa["all_combo_probabilities_blocked"] is True
    assert int(gqa["combo_home_probabilities_remaining"])==int(gqa["combo_away_probabilities_remaining"])==0
    markets=[]
    for market,rs in sorted(grouped.items()):
        n=sum(int(r["test_n"]) for r in rs)
        markets.append({"market":market,"folds":3,"total_test_n":n,
          "mean_fold_accuracy":round(sum(float(r["accuracy_at_0_5"]) for r in rs)/3,6),
          "weighted_accuracy":round(sum(float(r["accuracy_at_0_5"])*int(r["test_n"]) for r in rs)/n,6),
          "accuracy_min":min(float(r["accuracy_at_0_5"]) for r in rs),"accuracy_max":max(float(r["accuracy_at_0_5"]) for r in rs),
          "accuracy_ci_low_min":min(float(r["accuracy_95ci_low"]) for r in rs),"accuracy_ci_high_max":max(float(r["accuracy_95ci_high"]) for r in rs),
          "mean_brier":round(sum(float(r["brier"]) for r in rs)/3,6),
          "brier_skill_min":min(float(r["brier_skill_vs_prevalence"]) for r in rs),"brier_skill_max":max(float(r["brier_skill_vs_prevalence"]) for r in rs),
          "mean_log_loss":round(sum(float(r["log_loss"]) for r in rs)/3,6),
          "auc_min":min(float(r["auc"]) for r in rs),"auc_max":max(float(r["auc"]) for r in rs),
          "mean_ece":round(sum(float(r["ece_10_bins"]) for r in rs)/3,6),
          "calibration":"RAW_UNCALIBRATED_ECE_ONLY","odds_benchmark":"NOT_RUN_PROVENANCE_UNVERIFIED","production_eligible":"NO"})
    reported=meta["source_artifact_reported_counts"]
    result={"status":"PASS_AGGREGATE_WALK_FORWARD_INTEGRITY_AUDIT_RESEARCH_ONLY","source":src,
      "aggregate_market_fold_rows":len(rows),"markets":len(MARKETS),"fold_order_and_expanding_window_arithmetic":"PASS",
      "wilson_intervals_recomputed":15,"brier_skill_formula_checks":15,
      "source_artifact_reported_league_market_rows":reported["league_market_rows"],
      "source_artifact_reported_league_market_fold_rows":reported["league_market_fold_rows"],
      "source_artifact_reported_readiness_status_counts":reported["readiness_status_counts"],
      "source_artifact_reported_primary_sample_gate_failures":reported["primary_sample_gate_failures"],
      "per_league_counts_independently_rebuilt":False,"combo_probabilities_remaining":0,"production_eligible":False,"betting_eligible":False,
      "calibration":"NOT_PERFORMED_RAW_PROBABILITIES_ONLY","odds_roi_benchmark":"NOT_RUN_PROVENANCE_UNVERIFIED",
      "limitations":["This compact public audit independently checks the 15 aggregate fold records; the 250/750 per-league counts are reported from the source artifact, not rebuilt here.",
      "Metric integrity does not verify canonical fixture/team joins, official settlement truth, or point-in-time provenance.",
      "Only ECE is available in the snapshot; reliability bins/calibration curves cannot be reconstructed. No calibration was performed.",
      "Wilson intervals use rounded accuracy and test_n and do not quantify model stability or betting returns.",
      "Odds/ROI benchmarking is blocked by unverified provenance. Combo and M-1UP remain blocked."],"market_summaries":markets}
    (OUT/"selected50_walk_forward_integrity_audit.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    with (OUT/"selected50_walk_forward_market_summary.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(markets[0]));w.writeheader();w.writerows(markets)
    lines=["# Selected-50 Walk-Forward Integrity Audit — 2026-10-26","","Result: PASS_AGGREGATE_WALK_FORWARD_INTEGRITY_AUDIT_RESEARCH_ONLY.",
      "Scope: pinned sanitized aggregate metrics from runtime run 40238357851, artifact 12615034595. No model execution, calibration, API call or production change occurred.","",
      "## Integrity checks","",f"- Aggregate rows: {len(rows)} (five markets × three adjacent chronological test windows).",
      "- Recomputed Wilson accuracy intervals: 15; all match within tolerance.","- Recomputed Brier-skill formulas: 15; all match within rounding tolerance.",
      "- Expanding-window arithmetic passes: next fold training count equals prior training plus prior test count.",
      f"- Source artifact reports {reported['league_market_rows']} league-market rows and {reported['league_market_fold_rows']} league/fold rows; this compact audit does not independently rebuild them.",
      "- All governed rows remain production-ineligible; Combo probabilities remain masked.","","## Market diagnostics (raw, uncalibrated)","",
      "| Market | Mean fold accuracy | Weighted accuracy | Brier skill range | AUC range | Mean ECE |","|---|---:|---:|---:|---:|---:|"]
    for m in markets: lines.append(f"| {m['market']} | {m['mean_fold_accuracy']:.3%} | {m['weighted_accuracy']:.3%} | {m['brier_skill_min']:+.4f} to {m['brier_skill_max']:+.4f} | {m['auc_min']:.4f}–{m['auc_max']:.4f} | {m['mean_ece']:.4f} |")
    lines += ["","## Limitations and gates","","- This validates metric arithmetic, not fixture/team identity, official settlement truth, or point-in-time feature provenance.",
      "- ECE is the only calibration diagnostic in this snapshot; reliability bins and calibration curves are unavailable. Calibration was not performed.",
      "- Odds/ROI benchmarking was not run because bookmaker/market/timestamp provenance remains unverified.",
      "- Combo remains blocked by the predictor/settlement mismatch. M-1UP remains blocked by its independent gate.","- Production remains NOT_GRANTED; this audit is research-only.","",
      "## Provenance","",f"- Runtime run: https://github.com/{src['repository']}/actions/runs/{src['runtime_run_id']}",
      f"- Runtime commit: {src['runtime_commit']}",f"- Artifact ID: {src['artifact_id']}",f"- Artifact SHA-256: {src['artifact_sha256']}",f"- Branch: {src['branch']}"]
    (OUT/"selected50_walk_forward_integrity_audit.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ["status","aggregate_market_fold_rows","fold_order_and_expanding_window_arithmetic","wilson_intervals_recomputed","brier_skill_formula_checks","production_eligible","betting_eligible"]},sort_keys=True))
    return result
if __name__=="__main__": audit_snapshot()
