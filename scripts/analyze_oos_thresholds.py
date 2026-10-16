#!/usr/bin/env python3
"""Research-only, chronological OOS selection-threshold audit for Oracle.

Does not change production probabilities, model logic, or promotion gates.
No odds are available here, so this cannot establish ROI or betting value.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, log_loss

THRESHOLDS = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85]
MIN_N = 100


def wilson(successes: int, n: int, z: float = 1.96):
    if n <= 0:
        return (None, None)
    p = successes / n
    den = 1 + z*z/n
    centre = (p + z*z/(2*n))/den
    margin = z*math.sqrt((p*(1-p)/n)+(z*z/(4*n*n)))/den
    return (centre-margin, centre+margin)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: analyze_oos_thresholds.py <oos_predictions.csv> <output.csv>")
    source = Path(sys.argv[1])
    out = Path(sys.argv[2])
    df = pd.read_csv(source)
    required = {"market", "target", "raw_probability", "fold", "date"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")
    df = df.dropna(subset=["market", "target", "raw_probability", "fold", "date"]).copy()
    df["target"] = pd.to_numeric(df["target"], errors="coerce")
    df["raw_probability"] = pd.to_numeric(df["raw_probability"], errors="coerce")
    df = df.dropna(subset=["target", "raw_probability"])
    if not df["target"].isin([0, 1]).all():
        raise SystemExit("Targets must be binary 0/1.")
    if not df["raw_probability"].between(0, 1).all():
        raise SystemExit("Raw probabilities outside [0,1].")
    rows = []
    for market, g in df.groupby("market", sort=True):
        prevalence = float(g.target.mean())
        overall_brier = float(brier_score_loss(g.target, g.raw_probability))
        overall_logloss = float(log_loss(g.target, g.raw_probability, labels=[0, 1]))
        for threshold in THRESHOLDS:
            s = g[g.raw_probability >= threshold]
            n = len(s)
            wins = int(s.target.sum()) if n else 0
            lo, hi = wilson(wins, n)
            rows.append({
                "market": market,
                "threshold": threshold,
                "sample_n": n,
                "minimum_sample_n": MIN_N,
                "sample_gate": "PASS" if n >= MIN_N else "INSUFFICIENT_SAMPLE",
                "hits": wins,
                "hit_rate": float(s.target.mean()) if n else None,
                "hit_rate_wilson95_low": lo,
                "hit_rate_wilson95_high": hi,
                "overall_market_base_rate": prevalence,
                "hit_rate_minus_base_rate": float(s.target.mean()-prevalence) if n else None,
                "mean_selected_probability": float(s.raw_probability.mean()) if n else None,
                "selected_brier": float(brier_score_loss(s.target, s.raw_probability)) if n else None,
                "selected_log_loss": float(log_loss(s.target, s.raw_probability, labels=[0, 1])) if n else None,
                "overall_raw_brier": overall_brier,
                "overall_raw_log_loss": overall_logloss,
                "fold_count": int(s.fold.nunique()) if n else 0,
                "odds_available": False,
                "roi_or_value_status": "NOT_EVALUATED_NO_VERIFIED_ODDS",
                "decision_status": "RESEARCH_ONLY_NOT_APPROVED"
            })
    result = pd.DataFrame(rows)
    out.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(out, index=False)
    summary = {
        "status": "COMPLETE_RESEARCH_ONLY",
        "source_file": str(source),
        "source_rows": int(len(df)),
        "markets": int(df.market.nunique()),
        "thresholds": THRESHOLDS,
        "minimum_sample_n": MIN_N,
        "rows": int(len(result)),
        "markets_with_any_threshold_meeting_sample_gate": int(result.loc[result.sample_gate.eq("PASS"), "market"].nunique()),
        "odds_available": False,
        "roi_or_value_evaluated": False,
        "production_changed": False,
        "promotion": "BLOCKED",
        "caveat": "Thresholds are descriptive on the OOS cohort. Do not select/promote a threshold from this same cohort without a separate nested or later chronological holdout."
    }
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
