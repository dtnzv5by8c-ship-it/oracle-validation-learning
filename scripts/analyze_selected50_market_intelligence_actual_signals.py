#!/usr/bin/env python3
"""Research-only diagnostics for settled Selected-50 Market Intelligence fixtures.

Uses exact provider identity joins and a five-match minimum. No provider calls,
production writes, calibration fitting, or Oracle V1.6 changes are performed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr, t as student_t

KEYS = ["provider_season_id", "fixture_id", "home_team_provider_id", "away_team_provider_id"]
SETTLED = "SETTLED_VERIFIED_PROVIDER_SCORE"
MIN_HISTORY = 5

BASE_FEATURES = [
    "home_form_gf_avg", "home_form_ga_avg", "home_form_ppg",
    "away_form_gf_avg", "away_form_ga_avg", "away_form_ppg",
    "home_form_btts_rate", "away_form_btts_rate",
    "home_form_over15_rate", "away_form_over15_rate",
    "home_form_over25_rate", "away_form_over25_rate",
    "home_form_under45_rate", "away_form_under45_rate",
    "home_team_over15_rate", "away_team_over15_rate",
    "home_clean_sheet_rate", "away_clean_sheet_rate",
    "home_failed_to_score_rate", "away_failed_to_score_rate",
    "home_at_home_avg_goals_for", "home_at_home_avg_goals_against", "home_at_home_avg_points",
    "away_away_avg_goals_for", "away_away_avg_goals_against", "away_away_avg_points",
    "home_league_position", "away_league_position", "h2h_n", "h2h_avg_total_goals",
]

OUTCOME_COLUMNS = {
    "BTTS": "actual_btts",
    "Over15": "actual_over_1_5",
    "Over25": "actual_over_2_5",
    "Under45": "actual_under_4_5",
}


def _clean_keys(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in keys:
        if col not in out:
            raise ValueError(f"Missing exact identity column: {col}")
        out[col] = out[col].fillna("").astype(str).str.strip()
    if (out[keys] == "").any(axis=None):
        raise ValueError("Blank exact identity value; fail closed")
    return out


def load_and_join(actual_path: Path, mi_path: Path, trace_path: Path, goal_path: Path) -> tuple[pd.DataFrame, dict]:
    actual = pd.read_csv(actual_path, low_memory=False)
    mi = pd.read_csv(mi_path, low_memory=False)
    trace = pd.read_csv(trace_path, low_memory=False)
    goal = pd.read_csv(goal_path, low_memory=False)

    trace = trace.rename(columns={
        "runtime_provider_season_id": "provider_season_id",
        "runtime_home_team_id": "home_team_provider_id",
        "runtime_away_team_id": "away_team_provider_id",
    })
    goal = goal.rename(columns={
        "home_team_id": "home_team_provider_id",
        "away_team_id": "away_team_provider_id",
    })
    actual = _clean_keys(actual, KEYS)
    trace = _clean_keys(trace, KEYS)
    goal = _clean_keys(goal, KEYS)

    for label, frame in (("actual results", actual), ("evidence trace", trace), ("goal research", goal)):
        if frame.duplicated(KEYS).any():
            raise ValueError(f"Duplicate exact identity keys in {label}")

    settled = actual[actual["settlement_status"].eq(SETTLED)].copy()
    joined = settled.merge(trace, on=KEYS, how="left", validate="one_to_one", indicator="_trace_join")
    unmatched = int(joined["_trace_join"].ne("both").sum())
    if unmatched:
        raise ValueError(f"Settled actuals without exact evidence trace: {unmatched}")
    joined = joined.drop(columns="_trace_join")

    mi = mi.rename(columns={"Fixture": "runtime_fixture", "League": "runtime_league", "H2H Avg Total Goals": "h2h_avg_total_goals"})
    display_keys = ["runtime_fixture", "runtime_league"]
    if any(c not in mi for c in display_keys) or any(c not in joined for c in display_keys):
        raise ValueError("Market Intelligence display join columns missing")
    if mi.duplicated(display_keys).any():
        raise ValueError("Duplicate fixture/league display keys in Market Intelligence")
    joined = joined.merge(mi, on=display_keys, how="left", validate="one_to_one", indicator="_mi_join")
    mi_unmatched = int(joined["_mi_join"].ne("both").sum())
    if mi_unmatched:
        raise ValueError(f"Settled exact-identity fixtures without Market Intelligence row: {mi_unmatched}")
    joined = joined.drop(columns="_mi_join")

    joined = joined.merge(goal, on=KEYS, how="left", validate="one_to_one", suffixes=("", "_goal"))
    qa = {
        "settled_actual_rows": int(len(settled)),
        "exact_trace_join_rows": int(len(joined)),
        "market_intelligence_join_rows": int(len(joined)),
        "goal_research_exact_join_rows": int(joined["forecast_status"].notna().sum()),
        "goal_research_missing_rows": int(joined["forecast_status"].isna().sum()),
        "exact_identity_policy": "PROVIDER_SEASON_ID + FIXTURE_ID + ORDERED_HOME_TEAM_ID + ORDERED_AWAY_TEAM_ID",
        "display_join_policy": "EXACT_FIXTURE_LABEL_AND_LEAGUE_ONLY_FOR_MARKET_INTELLIGENCE_TAB_WITHOUT_ID_COLUMNS",
    }
    return joined, qa


def select_strict_sample(joined: pd.DataFrame, min_history: int = MIN_HISTORY) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    settled = joined.copy()
    clean = settled[settled["schedule_reconciliation_status"].eq("MATCH")].copy()
    for col in ("home_form_n", "away_form_n", "home_at_home_form_n", "away_away_form_n"):
        clean[col] = pd.to_numeric(clean[col], errors="coerce")

    cutoff = pd.to_datetime(clean["history_cutoff_utc"], utc=True, errors="coerce")
    kickoff = pd.to_datetime(clean["runtime_kickoff_utc"], utc=True, errors="coerce")
    rule_ok = clean["history_cutoff_rule"].eq("STRICTLY_BEFORE_FIXTURE_KICKOFF")
    cutoff_ok = cutoff.notna() & kickoff.notna() & cutoff.le(kickoff)
    history_ok = clean["home_form_n"].ge(min_history) & clean["away_form_n"].ge(min_history)
    strict = clean[history_ok & rule_ok & cutoff_ok].copy()
    venue = strict[strict["home_at_home_form_n"].ge(min_history) & strict["away_away_form_n"].ge(min_history)].copy()
    qa = {
        "settled_rows": int(len(settled)),
        "schedule_clean_rows": int(len(clean)),
        "schedule_review_rows_excluded": int(len(settled) - len(clean)),
        "five_match_strict_rows": int(len(strict)),
        "both_venue_splits_five_match_rows": int(len(venue)),
        "strict_history_minimum": int(min_history),
        "clean_rows_with_home_history_below_minimum": int((clean["home_form_n"].lt(min_history) | clean["home_form_n"].isna()).sum()),
        "clean_rows_with_away_history_below_minimum": int((clean["away_form_n"].lt(min_history) | clean["away_form_n"].isna()).sum()),
        "strict_history_cutoff_rule_rows": int(rule_ok.sum()),
        "strict_history_cutoff_rule_failures": int((~rule_ok).sum()),
        "strict_history_cutoff_invalid_or_late_rows": int((~cutoff_ok).sum()),
        "league_table_status_counts": clean["league_table_status"].value_counts(dropna=False).to_dict(),
        "active_leagues_in_strict_sample": int(strict["league"].nunique()),
    }
    return clean, strict, venue, qa


def engineer_features(df: pd.DataFrame, min_history: int = MIN_HISTORY) -> pd.DataFrame:
    out = df.copy()
    numeric = list(dict.fromkeys(BASE_FEATURES + [
        "home_form_n", "away_form_n", "home_at_home_form_n", "away_away_form_n",
    ]))
    for col in numeric:
        if col in out:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    out["overall_ppg_diff"] = out["home_form_ppg"] - out["away_form_ppg"]
    out["home_attack_adv"] = out["home_form_gf_avg"] - out["away_form_ga_avg"]
    out["away_attack_adv"] = out["away_form_gf_avg"] - out["home_form_ga_avg"]
    out["home_lambda_proxy"] = (out["home_form_gf_avg"] + out["away_form_ga_avg"]) / 2
    out["away_lambda_proxy"] = (out["away_form_gf_avg"] + out["home_form_ga_avg"]) / 2
    out["lambda_total_proxy"] = out["home_lambda_proxy"] + out["away_lambda_proxy"]
    out["goal_balance_proxy"] = out["home_lambda_proxy"] - out["away_lambda_proxy"]
    out["goal_environment"] = (
        out["home_form_btts_rate"] + out["away_form_btts_rate"] +
        out["home_form_over25_rate"] + out["away_form_over25_rate"]
    ) / 4
    out["team_scoring_support"] = (out["home_team_over15_rate"] + out["away_team_over15_rate"]) / 2
    out["defensive_fragility"] = (out["home_form_ga_avg"] + out["away_form_ga_avg"]) / 2

    venue_ok = out["home_at_home_form_n"].ge(min_history) & out["away_away_form_n"].ge(min_history)
    out["venue_ppg_diff"] = (out["home_at_home_avg_points"] - out["away_away_avg_points"]).where(venue_ok)
    out["venue_gf_adv"] = (out["home_at_home_avg_goals_for"] - out["away_away_avg_goals_for"]).where(venue_ok)
    out["venue_ga_adv"] = (out["away_away_avg_goals_against"] - out["home_at_home_avg_goals_against"]).where(venue_ok)
    # H2H performance features are admissible only with five observed prior meetings.
    h2h_n = pd.to_numeric(out["h2h_n"], errors="coerce")
    out["h2h_goal_environment"] = pd.to_numeric(out["h2h_avg_total_goals"], errors="coerce").where(h2h_n.ge(min_history))

    # Prespecified interactions: exploratory only; no fitted weights or promotion.
    out["home_strength_x_away_weakness"] = out["overall_ppg_diff"] * out["away_form_ga_avg"]
    out["home_attack_x_away_defence"] = out["home_form_gf_avg"] * out["away_form_ga_avg"]
    out["away_attack_x_home_defence"] = out["away_form_gf_avg"] * out["home_form_ga_avg"]
    out["attack_defence_pressure"] = out["home_attack_x_away_defence"] + out["away_attack_x_home_defence"]
    out["form_venue_agreement"] = out["overall_ppg_diff"] * out["venue_ppg_diff"]
    out["btts_form_interaction"] = out["home_form_btts_rate"] * out["away_form_btts_rate"]
    out["goal_scoring_both_interaction"] = out["home_team_over15_rate"] * out["away_team_over15_rate"]
    out["balanced_goal_pressure"] = np.minimum(out["home_form_gf_avg"], out["away_form_gf_avg"])
    out["absolute_form_gap"] = out["overall_ppg_diff"].abs()

    # Outcomes are derived only from independently joined final scores.
    result = out["actual_match_result"].astype(str)
    out["y_home_win"] = result.eq("HOME_WIN").astype(int)
    out["y_draw"] = result.eq("DRAW").astype(int)
    out["y_away_win"] = result.eq("AWAY_WIN").astype(int)
    out["y_home_1x"] = result.isin(["HOME_WIN", "DRAW"]).astype(int)
    out["y_away_x2"] = result.isin(["AWAY_WIN", "DRAW"]).astype(int)
    for name, col in OUTCOME_COLUMNS.items():
        out[f"y_{name.lower()}"] = out[col].astype(str).eq("YES").astype(int)
    out["y_home_over15"] = pd.to_numeric(out["actual_home_goals"], errors="coerce").ge(2).astype(int)
    out["y_away_over15"] = pd.to_numeric(out["actual_away_goals"], errors="coerce").ge(2).astype(int)
    return out


def auc_binary(y: np.ndarray, score: np.ndarray) -> float:
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    n_pos = int(y.sum())
    n_neg = len(y) - n_pos
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    ranks = rankdata(score)
    return float((ranks[y == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def bh_adjust(p_values: np.ndarray) -> np.ndarray:
    p = np.asarray(p_values, dtype=float)
    if p.size == 0:
        return p.copy()
    order = np.argsort(p)
    q = np.empty_like(p)
    running = 1.0
    m = len(p)
    for i in range(m - 1, -1, -1):
        idx = order[i]
        running = min(running, p[idx] * m / (i + 1))
        q[idx] = running
    return np.clip(q, 0, 1)


def by_adjust(p_values: np.ndarray) -> np.ndarray:
    """Benjamini-Yekutieli q-values; valid under arbitrary test dependence."""
    p = np.asarray(p_values, dtype=float)
    if p.size == 0:
        return p.copy()
    harmonic = float(np.sum(1.0 / np.arange(1, len(p) + 1)))
    return np.clip(bh_adjust(p) * harmonic, 0.0, 1.0)


def partial_spearman(x: np.ndarray, y: np.ndarray, controls: np.ndarray) -> tuple[float, float]:
    """Partial Spearman correlation using rank-residualization and a t approximation."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    controls = np.asarray(controls, dtype=float)
    if controls.ndim == 1:
        controls = controls.reshape(-1, 1)
    if len(x) != len(y) or len(x) != len(controls) or len(x) <= controls.shape[1] + 2:
        return float("nan"), float("nan")
    xr, yr = rankdata(x), rankdata(y)
    zr = np.column_stack([np.ones(len(x))] + [rankdata(controls[:, j]) for j in range(controls.shape[1])])
    rx = xr - zr @ np.linalg.lstsq(zr, xr, rcond=None)[0]
    ry = yr - zr @ np.linalg.lstsq(zr, yr, rcond=None)[0]
    sx, sy = float(np.std(rx)), float(np.std(ry))
    if sx == 0 or sy == 0:
        return float("nan"), float("nan")
    rho = float(np.corrcoef(rx, ry)[0, 1])
    dof = len(x) - controls.shape[1] - 2
    if not np.isfinite(rho) or abs(rho) >= 1:
        return rho, float("nan")
    statistic = rho * np.sqrt(dof / (1.0 - rho * rho))
    return rho, float(2.0 * student_t.sf(abs(statistic), dof))


def bootstrap_partial_spearman_ci(x: np.ndarray, y: np.ndarray, controls: np.ndarray, reps: int, rng: np.random.Generator) -> tuple[float, float]:
    """Percentile bootstrap interval for partial Spearman correlation."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    controls = np.asarray(controls, dtype=float)
    n = len(x)
    idx = rng.integers(0, n, size=(reps, n))
    values = []
    for sample in idx:
        rho, _ = partial_spearman(x[sample], y[sample], controls[sample])
        if np.isfinite(rho):
            values.append(rho)
    if not values:
        return float("nan"), float("nan")
    lo, hi = np.quantile(values, [0.025, 0.975])
    return float(lo), float(hi)


def partial_interaction_table(df: pd.DataFrame, outcome: str, reps: int, seed: int) -> pd.DataFrame:
    """Test whether the two lead interactions add rank-association beyond their main effects."""
    rng = np.random.default_rng(seed)
    controls_by_feature = {
        "home_strength_x_away_weakness": ["overall_ppg_diff", "away_form_ga_avg"],
        "home_attack_x_away_defence": ["home_form_gf_avg", "away_form_ga_avg"],
    }
    rows = []
    y_all = pd.to_numeric(df[outcome], errors="coerce")
    for feature, controls in controls_by_feature.items():
        cols = [feature] + controls
        numeric = df[cols].apply(pd.to_numeric, errors="coerce")
        mask = numeric.notna().all(axis=1) & y_all.notna()
        if int(mask.sum()) < 30:
            continue
        x = numeric.loc[mask, feature].to_numpy(float)
        y = y_all.loc[mask].to_numpy(float)
        z = numeric.loc[mask, controls].to_numpy(float)
        rho, p = partial_spearman(x, y, z)
        lo, hi = bootstrap_partial_spearman_ci(x, y, z, reps, rng)
        rows.append({
            "outcome": "HomeWin", "feature": feature, "n": int(mask.sum()),
            "controls": ";".join(controls), "partial_spearman_rho": rho,
            "partial_rho_ci95_low": lo, "partial_rho_ci95_high": hi,
            "partial_p_value": p,
        })
    return pd.DataFrame(rows)


def adjust_joint_multiple_testing(base: pd.DataFrame, interactions: pd.DataFrame, partial: pd.DataFrame | None = None):
    """Adjust base, raw-interaction and partial-interaction tests as one family."""
    partial = partial if partial is not None else pd.DataFrame()
    parts = []
    for family, frame, p_col in (("base", base, "p_value_raw"),
                                 ("interaction", interactions, "p_value_raw"),
                                 ("partial_interaction", partial, "partial_p_value")):
        if not frame.empty:
            part = frame.copy()
            part["_p_for_adjustment"] = pd.to_numeric(part[p_col], errors="coerce")
            part["test_family"] = family
            parts.append(part)
    if not parts:
        return base.copy(), interactions.copy(), partial.copy()
    combined = pd.concat(parts, ignore_index=True)
    p = combined["_p_for_adjustment"].to_numpy(float)
    combined["q_value_bh_global"] = bh_adjust(p)
    combined["q_value_by_global"] = by_adjust(p)
    def extract(family):
        return combined[combined["test_family"].eq(family)].drop(columns=["test_family", "_p_for_adjustment"]).reset_index(drop=True)
    return extract("base"), extract("interaction"), extract("partial_interaction")


def bootstrap_spearman(x: np.ndarray, y: np.ndarray, reps: int, rng: np.random.Generator) -> tuple[float, float]:
    n = len(x)
    idx = rng.integers(0, n, size=(reps, n))
    # Re-rank within each resample so bootstrap ties/duplicate draws are handled correctly.
    bx, by = rankdata(x[idx], axis=1), rankdata(y[idx], axis=1)
    bx = bx - bx.mean(axis=1, keepdims=True)
    by = by - by.mean(axis=1, keepdims=True)
    den = np.sqrt((bx * bx).sum(axis=1) * (by * by).sum(axis=1))
    corr = np.divide((bx * by).sum(axis=1), den, out=np.full(reps, np.nan), where=den > 0)
    lo, hi = np.nanquantile(corr, [0.025, 0.975])
    return float(lo), float(hi)


def association_table(df: pd.DataFrame, features: list[str], outcomes: dict[str, str], reps: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for outcome, y_col in outcomes.items():
        y_all = pd.to_numeric(df[y_col], errors="coerce")
        for feature in features:
            x_all = pd.to_numeric(df[feature], errors="coerce")
            mask = x_all.notna() & y_all.notna()
            x, y = x_all[mask].to_numpy(float), y_all[mask].to_numpy(int)
            if len(x) < 30 or len(np.unique(x)) < 3 or len(np.unique(y)) < 2:
                continue
            rho, p = spearmanr(x, y)
            lo, hi = bootstrap_spearman(x, y, reps, rng)
            rows.append({
                "outcome": outcome, "feature": feature, "n": int(len(x)),
                "spearman_rho": float(rho), "rho_ci95_low": lo, "rho_ci95_high": hi,
                "p_value_raw": float(p), "auc_signed": auc_binary(y, x),
                "auc_oriented": max(auc_binary(y, x), 1 - auc_binary(y, x)),
            })
    result = pd.DataFrame(rows)
    if not result.empty:
        result["q_value_bh_within_table"] = bh_adjust(result["p_value_raw"].to_numpy())
        result = result.sort_values(["outcome", "q_value_bh_within_table", "p_value_raw"], kind="stable")
    return result


def ece10(y: np.ndarray, p: np.ndarray) -> float:
    """Ten-bin expected calibration error; empty bins are ignored."""
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    edges = np.linspace(0.0, 1.0, 11)
    total = len(y)
    error = 0.0
    for i in range(10):
        mask = (p >= edges[i]) & (p < edges[i + 1] if i < 9 else p <= edges[i + 1])
        if mask.any():
            error += mask.sum() / total * abs(float(p[mask].mean()) - float(y[mask].mean()))
    return float(error)


def bootstrap_auc_ci(y: np.ndarray, p: np.ndarray, reps: int, rng: np.random.Generator) -> tuple[float, float]:
    n = len(y)
    idx = rng.integers(0, n, size=(reps, n))
    by, bp = y[idx], p[idx]
    ranks = rankdata(bp, axis=1)
    n_pos = by.sum(axis=1).astype(float)
    n_neg = n - n_pos
    numerator = (ranks * by).sum(axis=1) - n_pos * (n_pos + 1) / 2
    aucs = np.divide(numerator, n_pos * n_neg, out=np.full(reps, np.nan), where=(n_pos > 0) & (n_neg > 0))
    lo, hi = np.nanquantile(aucs, [0.025, 0.975])
    return float(lo), float(hi)


def probability_table(df: pd.DataFrame, reps: int, seed: int) -> pd.DataFrame:
    specs = [
        ("Oracle_BTTS", "BTTS Yes", "y_btts"),
        ("Oracle_Home1X", "Home 1X", "y_home_1x"),
        ("Oracle_AwayX2", "Away X2", "y_away_x2"),
        ("Research_Over15", "over15_probability_pct", "y_over15"),
        ("Research_Over25", "over25_probability_pct", "y_over25"),
        ("Research_Under45", "under45_probability_pct", "y_under45"),
        ("Research_HomeOver15", "home_over15_probability_pct", "y_home_over15"),
        ("Research_AwayOver15", "away_over15_probability_pct", "y_away_over15"),
    ]
    rng = np.random.default_rng(seed)
    rows = []
    for label, p_col, y_col in specs:
        p = pd.to_numeric(df[p_col], errors="coerce") / 100.0
        y = pd.to_numeric(df[y_col], errors="coerce")
        mask = p.notna() & y.notna()
        p = p[mask].clip(1e-6, 1 - 1e-6).to_numpy(float)
        y = y[mask].to_numpy(int)
        n = len(y)
        if n < 30 or len(np.unique(y)) < 2:
            continue
        prevalence = float(y.mean())
        base_p = np.full(n, prevalence)
        brier = (p - y) ** 2
        base_brier = (base_p - y) ** 2
        logloss = -(y * np.log(p) + (1 - y) * np.log(1 - p))
        base_logloss = -(y * np.log(base_p) + (1 - y) * np.log(1 - base_p))
        brier_diff = base_brier - brier
        logloss_diff = base_logloss - logloss
        idx = rng.integers(0, n, size=(reps, n))
        brier_ci = np.quantile(brier_diff[idx].mean(axis=1), [0.025, 0.975])
        logloss_ci = np.quantile(logloss_diff[idx].mean(axis=1), [0.025, 0.975])
        auc_ci = bootstrap_auc_ci(y, p, reps, rng)
        rows.append({
            "market": label, "n": n, "observed_rate": prevalence,
            "mean_prediction": float(p.mean()), "brier_score": float(brier.mean()),
            "constant_prevalence_brier": float(base_brier.mean()),
            "brier_improvement_vs_constant": float(brier_diff.mean()),
            "brier_improvement_ci95_low": float(brier_ci[0]),
            "brier_improvement_ci95_high": float(brier_ci[1]),
            "log_loss": float(logloss.mean()),
            "constant_prevalence_log_loss": float(base_logloss.mean()),
            "logloss_improvement_vs_constant": float(logloss_diff.mean()),
            "logloss_improvement_ci95_low": float(logloss_ci[0]),
            "logloss_improvement_ci95_high": float(logloss_ci[1]),
            "auc": auc_binary(y, p),
            "auc_ci95_low": auc_ci[0],
            "auc_ci95_high": auc_ci[1],
            "ece10": ece10(y, p),
            "calibration_in_the_large": float(p.mean() - prevalence),
            "baseline_method": "CONSTANT_PREVALENCE_ESTIMATED_ON_THIS_DIAGNOSTIC_COHORT_NOT_A_DEPLOYABLE_PRIOR",
        })
    return pd.DataFrame(rows)


def fixture_diagnostics_table(df: pd.DataFrame) -> pd.DataFrame:
    """Row-level signal audit; preserves actual fixture identity and raw feature values."""
    columns = [
        "fixture_date_utc", "league", "runtime_fixture", "fixture_id",
        "schedule_reconciliation_status", "history_cutoff_utc", "history_cutoff_rule",
        "home_form_n", "away_form_n", "home_at_home_form_n", "away_away_form_n",
        "home_form_ppg", "away_form_ppg", "overall_ppg_diff",
        "home_form_gf_avg", "away_form_ga_avg", "home_strength_x_away_weakness",
        "home_attack_x_away_defence", "away_attack_x_home_defence",
        "venue_ppg_diff", "venue_gf_adv", "venue_ga_adv",
        "home_form_btts_rate", "away_form_btts_rate",
        "home_team_over15_rate", "away_team_over15_rate",
        "home_league_position", "away_league_position", "league_table_status",
        "actual_home_goals", "actual_away_goals", "actual_match_result",
        "actual_btts", "actual_over_1_5", "actual_over_2_5", "actual_under_4_5",
        "BTTS Yes", "Home 1X", "Away X2",
        "forecast_status", "over15_probability_pct", "over25_probability_pct",
        "under45_probability_pct", "home_over15_probability_pct", "away_over15_probability_pct",
    ]
    available = [c for c in columns if c in df.columns]
    out = df[available].copy()
    rank_features = [
        "overall_ppg_diff", "home_strength_x_away_weakness",
        "home_attack_x_away_defence", "venue_ppg_diff", "venue_gf_adv",
    ]
    for feature in rank_features:
        if feature not in out:
            continue
        values = pd.to_numeric(out[feature], errors="coerce")
        out[feature + "_rank_pct"] = values.rank(method="average", pct=True)
        out[feature + "_quartile"] = pd.Series(pd.NA, index=out.index, dtype="Int64")
        mask = values.notna()
        if mask.any():
            ranks = values[mask].rank(method="first", pct=True)
            out.loc[mask, feature + "_quartile"] = np.ceil(ranks * 4).clip(1, 4).astype(int)
    out["production_eligible"] = False
    out["betting_eligible"] = False
    sort_cols = [c for c in ("fixture_date_utc", "league", "runtime_fixture") if c in out.columns]
    return out.sort_values(sort_cols, kind="stable") if sort_cols else out


def run(args: argparse.Namespace) -> dict:
    joined, join_qa = load_and_join(args.actual_results, args.market_intelligence, args.evidence_trace, args.goal_market_research)
    clean, strict, venue, sample_qa = select_strict_sample(joined, args.min_history)
    strict = engineer_features(strict, args.min_history)

    core_features = [
        "home_form_gf_avg", "home_form_ga_avg", "home_form_ppg",
        "away_form_gf_avg", "away_form_ga_avg", "away_form_ppg",
        "overall_ppg_diff", "home_attack_adv", "away_attack_adv",
        "home_lambda_proxy", "away_lambda_proxy", "lambda_total_proxy", "goal_balance_proxy",
        "goal_environment", "team_scoring_support", "defensive_fragility",
        "home_form_btts_rate", "away_form_btts_rate",
        "home_form_over25_rate", "away_form_over25_rate",
        "home_team_over15_rate", "away_team_over15_rate",
        "home_clean_sheet_rate", "away_clean_sheet_rate",
        "home_failed_to_score_rate", "away_failed_to_score_rate",
        # Provisional standings and raw H2H sample count are deliberately not predictors.
        # H2H goal environment is masked unless at least five observed meetings exist.
        "h2h_goal_environment",
        "venue_ppg_diff", "venue_gf_adv", "venue_ga_adv",
    ]
    outcomes = {
        "BTTS": "y_btts", "Over15": "y_over15", "Over25": "y_over25", "Under45": "y_under45",
        "HomeWin": "y_home_win", "Draw": "y_draw", "AwayWin": "y_away_win",
        "Home1X": "y_home_1x", "AwayX2": "y_away_x2",
    }
    associations = association_table(strict, core_features, outcomes, args.bootstrap_reps, args.seed)
    interactions = [
        "home_strength_x_away_weakness", "home_attack_x_away_defence", "away_attack_x_home_defence",
        "attack_defence_pressure", "form_venue_agreement", "btts_form_interaction",
        "goal_scoring_both_interaction", "balanced_goal_pressure", "absolute_form_gap",
    ]
    interaction_outcomes = {k: outcomes[k] for k in ("HomeWin", "Home1X", "AwayX2", "BTTS", "Over25")}
    interaction_table = association_table(strict, interactions, interaction_outcomes, args.bootstrap_reps, args.seed + 1)
    partial_interactions = partial_interaction_table(strict, "y_home_win", args.bootstrap_reps, args.seed + 3)
    associations, interaction_table, partial_interactions = adjust_joint_multiple_testing(associations, interaction_table, partial_interactions)
    scores = probability_table(strict, args.bootstrap_reps, args.seed + 2)
    fixture_rows = fixture_diagnostics_table(strict)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    associations.to_csv(args.output_dir / "market_intelligence_signal_associations.csv", index=False)
    interaction_table.to_csv(args.output_dir / "market_intelligence_interaction_associations.csv", index=False)
    partial_columns = ["outcome", "feature", "n", "controls", "partial_spearman_rho", "partial_rho_ci95_low", "partial_rho_ci95_high", "partial_p_value", "q_value_bh_global", "q_value_by_global"]
    partial_interactions[partial_columns].to_csv(args.output_dir / "market_intelligence_interaction_incremental_tests.csv", index=False)
    scores.to_csv(args.output_dir / "market_intelligence_probability_scores.csv", index=False)
    fixture_rows.to_csv(args.output_dir / "market_intelligence_fixture_signal_diagnostics.csv", index=False)

    # League position is deliberately not treated as an admissible feature while the table is provisional.
    provisional_table = clean["league_table_status"].astype(str).str.contains("PROVISIONAL", case=False).all()
    qa = {
        **join_qa, **sample_qa,
        "strict_sample_rows": int(len(strict)),
        "joint_feature_outcome_test_count": int(len(associations) + len(interaction_table) + len(partial_interactions)),
        "partial_interaction_tests": int(len(partial_interactions)),
        "h2h_five_meeting_rows": int(pd.to_numeric(strict["h2h_n"], errors="coerce").ge(args.min_history).sum()),
        "venue_five_match_sample_rows": int(len(venue)),
        "fixture_row_diagnostics_rows": int(len(fixture_rows)),
        "league_table_positions_quarantined": bool(provisional_table),
        "league_position_provenance": "PROVISIONAL_CONVENTIONAL_TABLE_NOT_ADMISSIBLE_FOR_SIGNAL_PROMOTION" if provisional_table else "REVIEW_REQUIRED",
        "xg_policy": "EXCLUDED_UNTIL_POINT_IN_TIME_CAPTURE_TIMESTAMP_AND_SOURCE_PROVENANCE_ARE_VERIFIED",
        "multiple_testing": "JOINT_BASE_PLUS_RAW_INTERACTION_PLUS_PARTIAL_INTERACTION_BH_AND_BENJAMINI_YEKUTIELI_ADJUSTMENTS; WITHIN_TABLE_Q_VALUES_RETAINED_FOR_DIAGNOSTIC_ONLY",
        "feature_test_quarantine": {
            "league_positions": "EXCLUDED_FROM_ASSOCIATION_TESTS_WHILE_ALL_CURRENT_TABLES_ARE_PROVISIONAL",
            "h2h_sample_count": "NOT_USED_AS_A_PREDICTIVE_FEATURE",
            "h2h_goal_environment": "MASKED_UNLESS_H2H_N_AT_LEAST_FIVE_OBSERVED_PRIOR_MEETINGS",
            "venue_features": "MASKED_UNLESS_HOME_AT_HOME_AND_AWAY_AWAY_N_AT_LEAST_FIVE",
        },
        "bootstrap_repetitions": int(args.bootstrap_reps),
        "random_seed": int(args.seed),
        "production_eligible": False,
        "betting_eligible": False,
        "oracle_v1_6_logic_changed": False,
        "oracle_v1_6_probabilities_changed": False,
        "interpretation": "RESEARCH_ONLY_EXPLORATORY_ASSOCIATIONS_NOT_CHRONOLOGICAL_OUT_OF_SAMPLE_MODEL_VALIDATION",
    }
    (args.output_dir / "market_intelligence_signal_qa.json").write_text(json.dumps(qa, indent=2) + "\n", encoding="utf-8")
    return qa


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--actual-results", type=Path, required=True)
    parser.add_argument("--market-intelligence", type=Path, required=True)
    parser.add_argument("--evidence-trace", type=Path, required=True)
    parser.add_argument("--goal-market-research", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--min-history", type=int, default=MIN_HISTORY)
    parser.add_argument("--bootstrap-reps", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=20261101)
    args = parser.parse_args()
    if args.min_history < MIN_HISTORY:
        parser.error(f"--min-history cannot be below the governed {MIN_HISTORY}-match minimum")
    qa = run(args)
    print(json.dumps(qa, indent=2))


if __name__ == "__main__":
    main()
