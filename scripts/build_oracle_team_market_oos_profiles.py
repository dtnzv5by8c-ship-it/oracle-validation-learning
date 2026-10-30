#!/usr/bin/env python3
"""Build research-only team/league DNA from existing chronological OOS outputs.

Reads an existing oracle-football-data checkout. No network/provider calls,
H2H inputs, production writes, probability changes, or governance changes.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np
import pandas as pd

ALLOWED_MARKETS = {"BTTS", "DC_HOME", "DC_AWAY", "COMBO_HOME", "COMBO_AWAY", "M1UP_HOME", "M1UP_AWAY"}


def wilson(hits: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return (float("nan"), float("nan"))
    p = hits / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    w = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return max(0.0, c-w), min(1.0, c+w)


def build_profiles(oos: pd.DataFrame, matches: pd.DataFrame, min_sample: int = 30):
    req_oos = {"match_id", "date", "model", "raw_probability", "target"}
    req_match = {"match_id", "date", "league_code", "home_team", "away_team"}
    if req_oos - set(oos.columns) or req_match - set(matches.columns):
        raise ValueError("Required OOS/match columns are missing")
    oos = oos.copy()
    if "league_code" in oos.columns:
        oos = oos.drop(columns=["league_code"])
    oos["match_id"] = oos.match_id.astype(str)
    matches = matches.copy()
    matches["match_id"] = matches.match_id.astype(str)
    if matches.match_id.duplicated().any():
        raise ValueError("matches.csv has duplicate match_id values")
    if oos.duplicated(["match_id", "model"]).any():
        raise ValueError("OOS predictions have duplicate (match_id, model) keys")
    unknown = sorted(set(oos.model.astype(str)) - ALLOWED_MARKETS)
    if unknown:
        raise ValueError(f"Unexpected market/model labels: {unknown}")
    joined = oos.merge(matches[list(req_match)], on="match_id", how="left", validate="many_to_one", suffixes=("", "_match"))
    joined_rows = len(joined)
    if joined.league_code.isna().any():
        raise ValueError(f"Unmatched OOS fixtures: {int(joined.league_code.isna().sum())}")
    d_oos = pd.to_datetime(joined.date, errors="coerce").dt.date
    d_match = pd.to_datetime(joined.date_match, errors="coerce").dt.date if "date_match" in joined else d_oos
    if (d_oos != d_match).any():
        raise ValueError(f"OOS/match date mismatch rows: {int((d_oos != d_match).sum())}")
    joined["raw_probability"] = pd.to_numeric(joined.raw_probability, errors="coerce")
    joined["target"] = pd.to_numeric(joined.target, errors="coerce")
    joined = joined.dropna(subset=["raw_probability", "target", "date", "home_team", "away_team"])
    joined = joined[joined.target.isin([0, 1]) & joined.raw_probability.between(0, 1)]
    exposures = []
    for r in joined.itertuples(index=False):
        base = {"match_id": r.match_id, "date": pd.Timestamp(r.date), "league_code": r.league_code,
                "market": r.model, "target": int(r.target), "probability": float(r.raw_probability)}
        if r.model == "BTTS":
            exposures += [{**base, "team": r.home_team, "venue": "HOME", "label_unit": "SHARED_FIXTURE"},
                          {**base, "team": r.away_team, "venue": "AWAY", "label_unit": "SHARED_FIXTURE"}]
        elif r.model.endswith("_HOME"):
            exposures.append({**base, "team": r.home_team, "venue": "HOME", "label_unit": "TEAM_TARGET"})
        elif r.model.endswith("_AWAY"):
            exposures.append({**base, "team": r.away_team, "venue": "AWAY", "label_unit": "TEAM_TARGET"})
    e = pd.DataFrame(exposures)
    if e.empty:
        raise ValueError("No supported team-market exposures were generated")
    team_rows, time_rows = [], []
    for (league, team, market, venue), g in e.groupby(["league_code", "team", "market", "venue"]):
        g = g.sort_values(["date", "match_id"])
        n, hits = len(g), int(g.target.sum())
        rate = hits / n
        lo, hi = wilson(hits, n)
        p = np.clip(g.probability.to_numpy(float), 1e-6, 1-1e-6)
        y = g.target.to_numpy(int)
        mean_p = float(p.mean())
        team_rows.append({
            "league_code": league, "team": team, "market": market, "venue": venue,
            "label_unit": g.label_unit.iloc[0], "n": n, "hits": hits, "outcome_rate": rate,
            "wilson_95_low": lo, "wilson_95_high": hi,
            "beta_1_1_shrunk_rate": (hits + 1) / (n + 2),
            "mean_probability": mean_p, "calibration_gap": rate - mean_p,
            "brier": float(np.mean((p-y)**2)),
            "log_loss": float(-np.mean(y*np.log(p)+(1-y)*np.log(1-p))),
            "sample_status": "INSUFFICIENT" if n < 8 else "DEVELOPING" if n < min_sample else "SCREENING_SAMPLE",
            "candidate_discordant_for_review": bool(n >= min_sample and not (lo <= mean_p <= hi)),
        })
        cut = len(g) // 2
        earlier, later = g.iloc[:cut], g.iloc[cut:]
        if len(earlier) >= 8 and len(later) >= 8:
            for period, part in (("EARLIER", earlier), ("LATER", later)):
                pn, ph = len(part), int(part.target.sum())
                plo, phi = wilson(ph, pn)
                pr = float(part.target.mean())
                time_rows.append({"league_code": league, "team": team, "market": market, "venue": venue,
                    "period": period, "n": pn, "date_min": str(part.date.min().date()),
                    "date_max": str(part.date.max().date()), "outcome_rate": pr,
                    "wilson_95_low": plo, "wilson_95_high": phi,
                    "mean_probability": float(part.probability.mean()),
                    "calibration_gap": pr-float(part.probability.mean())})
    team_df, time_df = pd.DataFrame(team_rows), pd.DataFrame(time_rows)
    league_df = team_df.groupby(["league_code", "market", "venue"], as_index=False).agg(
        team_profiles=("team", "nunique"), team_exposure_n=("n", "sum"),
        median_team_n=("n", "median"), candidate_discordant_profiles=("candidate_discordant_for_review", "sum"))
    meta = {"oos_prediction_rows": int(len(oos)), "joined_rows_before_label_filter": int(joined_rows),
        "valid_joined_rows": int(len(joined)), "match_join_coverage": float(joined_rows / len(oos)) if len(oos) else 0.0,
        "team_market_exposure_rows": int(len(e)), "team_market_profiles": int(len(team_df)),
        "chronology_profiles": int(time_df.groupby(["league_code", "team", "market", "venue"]).ngroups) if len(time_df) else 0,
        "candidate_discordant_profiles": int(team_df.candidate_discordant_for_review.sum()),
        "min_sample_for_candidate_flag": min_sample,
        "shrinkage": "Beta(1,1); no evaluation outcomes used to set prior",
        "btts_label_unit": "shared fixture outcome duplicated across home/away team exposures; not independent team trials"}
    return team_df, time_df, league_df, meta


def audit_m1up_export(root: Path) -> dict:
    export = pd.read_csv(root / "research/M1UP_OOS_PREDICTIONS_001.csv", dtype={"match_id": str})
    calibration = pd.read_csv(root / "research/M1UP_CALIBRATION_PREDICTIONS_w250.csv", dtype={"match_id": str})
    keys = export[["match_id", "venue"]].drop_duplicates()
    per_match = export.groupby("match_id").size()
    cal_per_match = calibration.groupby("match_id").size()
    return {"export_rows": len(export), "export_unique_matches": int(export.match_id.nunique()),
        "export_rows_per_match_min": int(per_match.min()), "export_rows_per_match_max": int(per_match.max()),
        "unique_match_venue_keys": len(keys), "duplicate_match_venue_rows": len(export)-len(keys),
        "export_status": "INVALID_FOR_VENUE_ATTRIBUTION" if len(export) > len(keys) else "STRUCTURE_CHECK_PASSED",
        "calibration_rows": len(calibration), "calibration_unique_matches": int(calibration.match_id.nunique()),
        "calibration_rows_per_match_min": int(cal_per_match.min()), "calibration_rows_per_match_max": int(cal_per_match.max()),
        "calibration_has_venue_or_team": any(c in calibration.columns for c in ("venue", "team", "target_team", "team_id")),
        "calibration_status": "AGGREGATE_ONLY_NO_VENUE_OR_TEAM_ATTRIBUTION"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-root", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    root, out = args.source_root, args.output_dir
    oos = pd.read_csv(root / "research/four_model/outputs/four_model_oos_predictions.csv", dtype={"match_id": str})
    matches = pd.read_csv(root / "database/matches.csv", dtype={"match_id": str},
        usecols=["match_id", "date", "league_code", "home_team", "away_team"])
    team, chronology, league, meta = build_profiles(oos, matches)
    out.mkdir(parents=True, exist_ok=True)
    team.to_csv(out / "oracle_team_market_oos_summary.csv", index=False)
    chronology.to_csv(out / "oracle_team_market_oos_chronology.csv", index=False)
    league.to_csv(out / "oracle_league_market_oos_summary.csv", index=False)
    summary = {"status": "COMPLETE_RESEARCH_ONLY", "source_repository": "dtnzv5by8c-ship-it/oracle-football-data",
        "source_commit": "cb89e5bd1c24810fe821a6b2c3c2c1c19272b381", "team_market_oos": meta,
        "m1up_export_integrity": audit_m1up_export(root),
        "governance": {"provider_calls": 0, "provider_credits": 0, "h2h_inputs_read": False,
            "production_logic_changed": False, "frozen_probabilities_changed": False,
            "calibration_changed": False, "governance_changed": False}}
    (out / "oracle_team_market_oos_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps({"status": summary["status"], **meta,
        "m1up_export_status": summary["m1up_export_integrity"]["export_status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
