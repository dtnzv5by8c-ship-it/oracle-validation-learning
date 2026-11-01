"""Research-only feature eligibility and interaction contracts for Project Oracle Run 3.

This module is intentionally isolated from Oracle V1.6 production code.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def core_form_eligible(frame: pd.DataFrame) -> pd.Series:
    """Both teams must have at least five observed prior matches."""
    return pd.to_numeric(frame["home_prior_n"], errors="coerce").ge(5) & pd.to_numeric(
        frame["away_prior_n"], errors="coerce"
    ).ge(5)


def venue_role_eligible(frame: pd.DataFrame) -> pd.Series:
    """Core form plus at least five observed home-role and away-role matches."""
    return (
        core_form_eligible(frame)
        & pd.to_numeric(frame["home_home_n"], errors="coerce").ge(5)
        & pd.to_numeric(frame["away_away_n"], errors="coerce").ge(5)
    )


def h2h_eligible(frame: pd.DataFrame) -> pd.Series:
    """H2H features are eligible only with at least five prior meetings."""
    return pd.to_numeric(frame["h2h_prior_n"], errors="coerce").ge(5)


def add_candidate_interactions(frame: pd.DataFrame) -> pd.DataFrame:
    """Add the two prespecified candidate interactions without imputing inputs."""
    required = ["home_ppg", "away_ppg", "home_gf", "away_ga"]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")
    out = frame.copy()
    out["overall_ppg_diff"] = out["home_ppg"] - out["away_ppg"]
    out["home_strength_x_away_weakness"] = out["overall_ppg_diff"] * out["away_ga"]
    out["home_attack_x_away_defence"] = out["home_gf"] * out["away_ga"]
    return out


def strict_prior_mask(history_kickoffs, target_kickoff) -> np.ndarray:
    """Only observations strictly earlier than kickoff are eligible."""
    return np.asarray(history_kickoffs) < target_kickoff
