#!/usr/bin/env python3
"""Audit historical challenger predictions against unique, completed score records.

Reporting/research only: never writes archive/SETTLEMENT_LEDGER.csv, never changes
model code or probabilities, and does not infer first-goal/1UP outcomes from final scores.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from pathlib import Path

import pandas as pd


SUPPORTED_MARKETS = {"BTTS_YES", "HOME_1X", "AWAY_X2", "HOME_1X_U45", "AWAY_X2_U45"}
PREDICTION_REQUIRED = {
    "prediction_id", "run_id", "fixture_id", "competition", "fixture_date",
    "home_team", "away_team", "model", "model_version", "model_status",
    "prediction_timestamp", "raw_probability", "selection",
}
RESULT_REQUIRED = {
    "date_utc", "home_team", "away_team", "home_goals", "away_goals",
    "finished", "cancelled", "status",
}


def norm_team(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(c for c in text if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^a-z0-9]+", "", text)


def truth_for_market(market: str, hg: int, ag: int) -> int | None:
    if market == "BTTS_YES":
        return int(hg > 0 and ag > 0)
    if market == "HOME_1X":
        return int(hg >= ag)
    if market == "AWAY_X2":
        return int(ag >= hg)
    if market == "HOME_1X_U45":
        return int(hg >= ag and hg + ag < 5)
    if market == "AWAY_X2_U45":
        return int(ag >= hg and hg + ag < 5)
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oracle-root", required=True, type=Path)
    ap.add_argument("--output-dir", required=True, type=Path)
    args = ap.parse_args()
    root = args.oracle_root
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    pred_path = root / "archive" / "PREDICTION_LEDGER.csv"
    result_path = root / "database" / "current_matches.csv"
    canonical_settlement_path = root / "archive" / "SETTLEMENT_LEDGER.csv"
    if not pred_path.exists() or not result_path.exists():
        raise SystemExit("BLOCKED: prediction ledger or current results file is missing.")

    pred = pd.read_csv(pred_path, dtype=str).fillna("")
    results = pd.read_csv(result_path, dtype=str).fillna("")
    missing_p = sorted(PREDICTION_REQUIRED - set(pred.columns))
    missing_r = sorted(RESULT_REQUIRED - set(results.columns))
    if missing_p or missing_r:
        raise SystemExit(f"BLOCKED: schema mismatch; prediction missing={missing_p}; results missing={missing_r}")

    pred = pred[pred["selection"].isin(SUPPORTED_MARKETS)].copy()
    pred["fixture_date_key"] = pd.to_datetime(pred["fixture_date"], errors="coerce").dt.strftime("%Y-%m-%d")
    pred["home_key"] = pred["home_team"].map(norm_team)
    pred["away_key"] = pred["away_team"].map(norm_team)
    results["date_key"] = pd.to_datetime(results["date_utc"], utc=True, errors="coerce").dt.strftime("%Y-%m-%d")
    results["home_key"] = results["home_team"].map(norm_team)
    results["away_key"] = results["away_team"].map(norm_team)
    finished = results[
        results["finished"].str.casefold().isin({"true", "1", "yes"})
        & ~results["cancelled"].str.casefold().isin({"true", "1", "yes"})
        & results["home_goals"].str.fullmatch(r"\d+")
        & results["away_goals"].str.fullmatch(r"\d+")
        & results["status"].str.upper().isin({"FT", "AET", "PEN", "FINISHED"})
    ].copy()

    # Strict match key: exact normalized home/away names and calendar date.
    # Do not use fuzzy aliases or infer outcomes for ambiguous candidates.
    groups = {}
    for idx, row in finished.iterrows():
        key = (row["date_key"], row["home_key"], row["away_key"])
        groups.setdefault(key, []).append(idx)

    settlements = []
    audit_rows = []
    for _, p in pred.iterrows():
        key = (p["fixture_date_key"], p["home_key"], p["away_key"])
        hits = groups.get(key, [])
        base = {
            "prediction_id": p["prediction_id"], "run_id": p["run_id"],
            "fixture_id": p["fixture_id"], "competition": p["competition"],
            "fixture_date": p["fixture_date"], "home_team": p["home_team"],
            "away_team": p["away_team"], "market": p["selection"],
            "model": p["model"], "model_version": p["model_version"],
            "model_status": p["model_status"], "prediction_timestamp": p["prediction_timestamp"],
            "raw_probability": p["raw_probability"],
        }
        if len(hits) != 1:
            audit_rows.append({**base, "match_status": "UNMATCHED" if not hits else "AMBIGUOUS",
                               "matching_completed_results": len(hits), "matched_result_date_utc": "",
                               "matched_result_home": "", "matched_result_away": "",
                               "final_home_score": "", "final_away_score": "",
                               "reason": "No exact completed score match" if not hits else "Multiple exact completed score matches"})
            continue

        r = finished.loc[hits[0]]
        hg, ag = int(r["home_goals"]), int(r["away_goals"])
        y = truth_for_market(p["selection"], hg, ag)
        try:
            probability = float(p["raw_probability"])
        except (TypeError, ValueError):
            probability = float("nan")
        if y is None or not math.isfinite(probability) or not 0 <= probability <= 1:
            audit_rows.append({**base, "match_status": "BLOCKED_INVALID_INPUT",
                               "matching_completed_results": 1, "matched_result_date_utc": r["date_utc"],
                               "matched_result_home": r["home_team"], "matched_result_away": r["away_team"],
                               "final_home_score": hg, "final_away_score": ag,
                               "reason": "Unsupported market or invalid raw probability"})
            continue
        eps = 1e-15
        clipped = min(1-eps, max(eps, probability))
        settlements.append({
            "prediction_id": p["prediction_id"], "run_id": p["run_id"], "fixture_id": p["fixture_id"],
            "market": p["selection"],
            "settlement_timestamp": pd.Timestamp.now(tz="UTC").isoformat(),
            "final_home_score": hg, "final_away_score": ag,
            "first_goal_team": "", "first_goal_minute": "", "btts_truth": int(hg > 0 and ag > 0),
            "home_1up_truth": "", "away_1up_truth": "", "selection_truth": y,
            "prediction_hit": int((probability >= 0.5) == bool(y)),
            "probability_error": probability - y, "brier_component": (probability-y)**2,
            "log_loss_component": -(y*math.log(clipped) + (1-y)*math.log(1-clipped)),
            "settlement_source": "FotMob current_matches.csv",
            "event_truth_source": "Unique completed final score; score-derived market truth only",
            "event_truth_cutoff_date": p["fixture_date"], "settlement_status": "SETTLED_SCORE_ONLY_AUDIT",
            "miss_class": "", "root_cause": "",
            "notes": "Research audit candidate only; canonical settlement ledger unchanged; no odds/value or first-goal evidence inferred."
        })
        audit_rows.append({**base, "match_status": "MATCHED_SCORE_ONLY",
                           "matching_completed_results": 1, "matched_result_date_utc": r["date_utc"],
                           "matched_result_home": r["home_team"], "matched_result_away": r["away_team"],
                           "final_home_score": hg, "final_away_score": ag, "selection_truth": y,
                           "reason": "Unique exact normalized team/date match; final-score-settleable market"})

    settlements_df = pd.DataFrame(settlements)
    audit_df = pd.DataFrame(audit_rows)
    settlements_df.to_csv(out / "settlement_candidates_score_only.csv", index=False)
    audit_df.to_csv(out / "prediction_settlement_match_audit.csv", index=False)

    status_counts = audit_df["match_status"].value_counts().to_dict() if len(audit_df) else {}
    settled_by_market = settlements_df.groupby("fixture_id")["market"].count().to_dict() if len(settlements_df) else {}
    market_summary = []
    if len(settlements_df):
        for market, g in settlements_df.groupby("market"):
            y = pd.to_numeric(g["selection_truth"], errors="coerce")
            p = pd.to_numeric(g["raw_probability"], errors="coerce")
            market_summary.append({
                "market": market, "settled_score_only_n": int(len(g)),
                "hit_rate_at_0_50_threshold": float(g["prediction_hit"].mean()),
                "mean_raw_probability": float(p.mean()), "observed_event_rate": float(y.mean()),
                "brier": float(g["brier_component"].mean()), "log_loss": float(g["log_loss_component"].mean()),
                "status": "RESEARCH_ONLY_NO_ODDS_VALUE_OR_PROMOTION"
            })
    canonical_rows = 0
    if canonical_settlement_path.exists():
        try:
            canonical_rows = len(pd.read_csv(canonical_settlement_path))
        except pd.errors.EmptyDataError:
            canonical_rows = 0
    report = {
        "status": "AUDIT_COMPLETE" if len(audit_df) else "NO_CANDIDATES",
        "scope": "archived CHALLENGER predictions for final-score-settleable markets only",
        "prediction_rows_considered": int(len(pred)),
        "unique_completed_result_rows": int(len(finished)),
        "score_only_settlement_candidates": int(len(settlements_df)),
        "match_status_counts": {str(k): int(v) for k, v in status_counts.items()},
        "canonical_settlement_ledger_rows_before": int(canonical_rows),
        "canonical_settlement_ledger_modified": False,
        "first_goal_and_1up_truth_inferred": False,
        "odds_or_value_assessed": False,
        "market_summary": market_summary,
        "guardrails": [
            "No production logic, raw probabilities, calibration, weights, or promotion gates changed.",
            "Only unique exact normalized team/date matches to finished non-cancelled score rows are settled.",
            "No fuzzy matching; ambiguous/unmatched rows remain unresolved.",
            "Final scores cannot establish first-goal timing or 1UP truth.",
            "All metrics are research-only; no profitability claim and no automatic promotion."
        ]
    }
    (out / "settlement_audit_summary.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if len(settlements_df) == 0:
        raise SystemExit("BLOCKED: no unique score-only settlement candidates were verified.")


if __name__ == "__main__":
    main()
