#!/usr/bin/env python3
"""Research-only Selected-50 scoreline model; aggregate outputs only."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.special import gammaln
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import PoissonRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from scripts.run8_full_archive_nested_ablations import (
    EXPECTED_ARCHIVE_SHA256, TRAIN_START, PRIMARY_END, FOLDS,
    read_archive, build_event_time_panel, add_eligibility_and_labels,
    build_model, metric_value, ece10, write_csv,
)

FEATURE_SETS = {
    "league_only": [],
    "overall_attack_defence": ["home_gf5", "away_ga5", "away_gf5", "home_ga5"],
    "overall_plus_venue_attack_defence": [
        "home_gf5", "away_ga5", "away_gf5", "home_ga5",
        "home_home_gf5", "home_home_ga5", "away_away_gf5", "away_away_ga5",
    ],
}
MAX_GOALS = 10

def poisson_pipeline(features):
    transformers = []
    if features:
        numeric = Pipeline([
            ("imputer", SimpleImputer(strategy="median", keep_empty_features=True)),
            ("scale", StandardScaler()),
        ])
        transformers.append(("numeric", numeric, list(features)))
    transformers.append(("league", OneHotEncoder(handle_unknown="ignore"), ["selected_id"]))
    return Pipeline([
        ("preprocess", ColumnTransformer(transformers, remainder="drop")),
        ("poisson", PoissonRegressor(alpha=0.5, max_iter=1000, tol=1e-8)),
    ])

def fit_goal_models(train, test, features):
    h_features = [x for x in features if x in {
        "home_gf5", "away_ga5", "home_home_gf5", "away_away_ga5"
    }]
    a_features = [x for x in features if x in {
        "away_gf5", "home_ga5", "away_away_gf5", "home_home_ga5"
    }]
    # The same four overall/venue indicators can inform both scoring intensities.
    h_features = list(dict.fromkeys(h_features))
    a_features = list(dict.fromkeys(a_features))
    h_model, a_model = poisson_pipeline(h_features), poisson_pipeline(a_features)
    h_model.fit(train[["selected_id"] + h_features], train["home_goals"].astype(float))
    a_model.fit(train[["selected_id"] + a_features], train["away_goals"].astype(float))
    train_h = np.clip(h_model.predict(train[["selected_id"] + h_features]), 0.03, 6.0)
    train_a = np.clip(a_model.predict(train[["selected_id"] + a_features]), 0.03, 6.0)
    test_h = np.clip(h_model.predict(test[["selected_id"] + h_features]), 0.03, 6.0)
    test_a = np.clip(a_model.predict(test[["selected_id"] + a_features]), 0.03, 6.0)
    return train_h, train_a, test_h, test_a

def log_pois(k, lam):
    k = np.asarray(k, dtype=float)
    lam = np.asarray(lam, dtype=float)
    return k * np.log(lam) - lam - gammaln(k + 1.0)

def dc_tau(hg, ag, lh, la, rho):
    tau = np.ones(np.broadcast(hg, ag, lh, la).shape, dtype=float)
    both = (hg == 0) & (ag == 0)
    h0a1 = (hg == 0) & (ag == 1)
    h1a0 = (hg == 1) & (ag == 0)
    h1a1 = (hg == 1) & (ag == 1)
    tau[both] = 1.0 - lh[both] * la[both] * rho
    tau[h0a1] = 1.0 + lh[h0a1] * rho
    tau[h1a0] = 1.0 + la[h1a0] * rho
    tau[h1a1] = 1.0 - rho
    return tau

def fit_dc_rho(train, lh, la):
    hg = train["home_goals"].to_numpy(dtype=int)
    ag = train["away_goals"].to_numpy(dtype=int)
    base = log_pois(hg, lh) + log_pois(ag, la)
    def objective(rho):
        tau = dc_tau(hg, ag, lh, la, rho)
        if np.any(tau <= 1e-8):
            return 1e12
        return float(-np.mean(base + np.log(tau)))
    result = minimize_scalar(objective, bounds=(-0.15, 0.15), method="bounded",
                             options={"xatol": 1e-5, "maxiter": 300})
    return float(result.x) if result.success else 0.0

def poisson_pmf_grid(lam, max_goals=MAX_GOALS):
    ks = np.arange(max_goals + 1, dtype=float)
    logs = ks[None, :] * np.log(lam[:, None]) - lam[:, None] - gammaln(ks[None, :] + 1)
    return np.exp(logs)

def scoreline_matrices(lh, la, rho):
    ph, pa = poisson_pmf_grid(lh), poisson_pmf_grid(la)
    joint = ph[:, :, None] * pa[:, None, :]
    if rho != 0:
        n = len(lh)
        for h, a, factor in [
            (0, 0, 1.0 - lh * la * rho),
            (0, 1, 1.0 + lh * rho),
            (1, 0, 1.0 + la * rho),
            (1, 1, 1.0 - rho),
        ]:
            joint[:, h, a] *= np.clip(factor, 1e-8, None)
    mass = joint.sum(axis=(1, 2))
    joint = joint / mass[:, None, None]
    return joint, mass

def derive_markets(joint):
    n, g, _ = joint.shape
    hs = np.arange(g)[:, None]
    aw = np.arange(g)[None, :]
    total = hs + aw
    p_home = joint[:, hs > aw].sum(axis=1)
    p_draw = joint[:, hs == aw].sum(axis=1)
    p_away = joint[:, hs < aw].sum(axis=1)
    p_btts = joint[:, 1:, 1:].sum(axis=(1, 2))
    p_o15 = joint[:, total >= 2].sum(axis=1)
    p_o25 = joint[:, total >= 3].sum(axis=1)
    p_u45 = joint[:, total <= 4].sum(axis=1)
    return {
        "home_win": p_home, "draw": p_draw, "away_win": p_away,
        "btts": p_btts, "over15": p_o15, "over25": p_o25, "under45": p_u45,
    }

def score_metrics(yh, ya, markets, joint, tail_mass):
    yb = ((yh > 0) & (ya > 0)).astype(int)
    yo15 = ((yh + ya) >= 2).astype(int)
    yo25 = ((yh + ya) >= 3).astype(int)
    yu45 = ((yh + ya) <= 4).astype(int)
    result = np.where(yh > ya, 0, np.where(yh == ya, 1, 2))
    probs = np.column_stack([markets["home_win"], markets["draw"], markets["away_win"]])
    onehot = np.eye(3)[result]
    in_grid = (yh <= MAX_GOALS) & (ya <= MAX_GOALS)
    score_prob = np.zeros(len(yh), dtype=float)
    score_prob[in_grid] = joint[np.where(in_grid)[0], yh[in_grid], ya[in_grid]]
    return {
        "btts_brier": float(np.mean((markets["btts"] - yb) ** 2)),
        "btts_log_loss": metric_value("log_loss", yb, markets["btts"]),
        "btts_auc": metric_value("auc", yb, markets["btts"]),
        "btts_ece10": ece10(yb, markets["btts"]),
        "over15_brier": float(np.mean((markets["over15"] - yo15) ** 2)),
        "over25_brier": float(np.mean((markets["over25"] - yo25) ** 2)),
        "under45_brier": float(np.mean((markets["under45"] - yu45) ** 2)),
        "1x2_multiclass_brier": float(np.mean(np.sum((probs - onehot) ** 2, axis=1))),
        "1x2_log_loss": float(-np.mean(np.log(np.clip(probs[np.arange(len(result)), result], 1e-8, 1.0)))),
        "scoreline_log_loss": float(-np.mean(np.log(np.clip(score_prob, 1e-12, 1.0)))),
        "mean_truncated_mass_before_renormalisation": float(np.mean(tail_mass)),
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True)
    parser.add_argument("--selected-manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    records, selected_ids, archive_meta = read_archive(
        args.archive, args.selected_manifest, EXPECTED_ARCHIVE_SHA256
    )
    # Archive source contains calendar dates, not verified intraday kickoff times.
    # Same-date results are therefore excluded from one another's pre-match histories.
    panel = build_event_time_panel(records, TRAIN_START, PRIMARY_END, lag_hours=0.0)
    frame = add_eligibility_and_labels(panel)
    metrics, coverage, reliability, missing = [], [], [], []
    pooled = {}
    for fold, start, end in FOLDS:
        raw_train = frame[(frame.kickoff_date >= TRAIN_START) & (frame.kickoff_date < start)]
        raw_test = frame[(frame.kickoff_date >= start) & (frame.kickoff_date < end)]
        train = raw_train[raw_train.venue_eligible].copy()
        test = raw_test[raw_test.venue_eligible].copy()
        if len(train) < 100 or len(test) < 30:
            raise ValueError(f"{fold} insufficient eligible sample: train={len(train)} test={len(test)}")
        coverage.append({
            "fold": fold, "train_n": len(train), "test_n": len(test),
            "test_leagues_n": int(test.selected_id.nunique()),
            "train_start": str(train.kickoff_date.min()), "train_end": str(train.kickoff_date.max()),
            "test_start": str(test.kickoff_date.min()), "test_end": str(test.kickoff_date.max()),
        })
        for model_name, features in FEATURE_SETS.items():
            tr_h, tr_a, te_h, te_a = fit_goal_models(train, test, features)
            rho = fit_dc_rho(train, tr_h, tr_a)
            for variant, r in [("independent_poisson", 0.0), ("dixon_coles", rho)]:
                joint, mass = scoreline_matrices(te_h, te_a, r)
                markets = derive_markets(joint)
                values = score_metrics(test.home_goals.to_numpy(dtype=int),
                                       test.away_goals.to_numpy(dtype=int), markets, joint, mass)
                metrics.append({
                    "fold": fold, "model": model_name, "variant": variant,
                    "rho": float(r), "n_train": len(train), "n_test": len(test),
                    "n_leagues": int(test.selected_id.nunique()), **values,
                })
                if fold not in pooled:
                    pooled[fold] = {}
                pooled[fold][(model_name, variant)] = (test, markets, joint)
            # Aggregate reliability only; no fixture-level predictions leave the job.
            y = ((test.home_goals.to_numpy() > 0) & (test.away_goals.to_numpy() > 0)).astype(int)
            reliability.append({
                "fold": fold, "model": model_name,
                "observed_btts_rate": float(y.mean()),
                "mean_predicted_btts_independent": float(derive_markets(scoreline_matrices(te_h, te_a, 0.0)[0])["btts"].mean()),
                "mean_predicted_btts_dc": float(derive_markets(scoreline_matrices(te_h, te_a, rho)[0])["btts"].mean()),
                "rho_train_estimate": float(rho),
            })
        # Logistic BTTS benchmark on the exact same test fixtures.
        logistic_features = ["home_ppg5", "away_ppg5", "home_gf5", "away_gf5", "home_ga5", "away_ga5"]
        logit = build_model(logistic_features)
        logit.fit(train[["selected_id"] + logistic_features], train.y_BTTS.astype(int))
        p = logit.predict_proba(test[["selected_id"] + logistic_features])[:, 1]
        y = test.y_BTTS.to_numpy(dtype=int)
        metrics.append({
            "fold": fold, "model": "existing_overall_form_logistic", "variant": "binary_btts_only",
            "rho": np.nan, "n_train": len(train), "n_test": len(test),
            "n_leagues": int(test.selected_id.nunique()),
            "btts_brier": float(np.mean((p-y)**2)),
            "btts_log_loss": metric_value("log_loss", y, p),
            "btts_auc": metric_value("auc", y, p),
            "btts_ece10": ece10(y,p),
        })
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "scoreline_fold_metrics.csv", metrics)
    write_csv(out / "scoreline_fold_coverage.csv", coverage)
    write_csv(out / "scoreline_reliability_summary.csv", reliability)
    summary = {
        "status": "COMPLETED_RESEARCH_ONLY",
        "archive_sha256": archive_meta["archive_sha256"],
        "archive_records": archive_meta["archive_raw_rows"],
        "season_files": archive_meta["archive_match_files"],
        "selected_groups_mapped": archive_meta["selected_groups_mapped"],
        "calendar_date_precision_only": True,
        "same_calendar_date_results_excluded": True,
        "venue_eligibility_minimum": "five prior overall matches and five prior home/away-role matches",
        "models": list(FEATURE_SETS),
        "variants": ["independent_poisson", "dixon_coles"],
        "max_score_grid": MAX_GOALS,
        "metrics": metrics,
        "coverage": coverage,
        "reliability": reliability,
        "governance": {
            "provider_api_credits_used": 0, "raw_provider_rows_exported": False,
            "fixture_level_predictions_exported": False, "feature_panel_exported": False,
            "oracle_v16_production_logic_changed": False,
            "oracle_v16_production_probabilities_changed": False,
            "canonical_ledgers_changed": False, "production_eligible": False,
            "betting_eligible": False,
        },
    }
    (out / "scoreline_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status": summary["status"], "archive_records": summary["archive_records"],
                      "metrics_rows": len(metrics), "folds": len(coverage),
                      "production_eligible": False, "betting_eligible": False}, indent=2))

if __name__ == "__main__":
    main()
