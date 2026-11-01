import numpy as np
import pandas as pd

from selected50_nested_interaction_contract import (
    add_candidate_interactions,
    core_form_eligible,
    h2h_eligible,
    strict_prior_mask,
    venue_role_eligible,
)


def test_core_requires_five_observed_matches_for_both_teams():
    df = pd.DataFrame({"home_prior_n": [5, 4, 8], "away_prior_n": [5, 9, 4]})
    assert core_form_eligible(df).tolist() == [True, False, False]


def test_venue_requires_five_observed_matches_in_each_role():
    df = pd.DataFrame({
        "home_prior_n": [5, 5, 5],
        "away_prior_n": [5, 5, 5],
        "home_home_n": [5, 4, 7],
        "away_away_n": [5, 8, 4],
    })
    assert venue_role_eligible(df).tolist() == [True, False, False]


def test_h2h_requires_five_prior_meetings():
    df = pd.DataFrame({"h2h_prior_n": [0, 4, 5, 8]})
    assert h2h_eligible(df).tolist() == [False, False, True, True]


def test_interaction_formulas_use_constituent_features_without_imputation():
    df = pd.DataFrame({
        "home_ppg": [2.0, 1.0],
        "away_ppg": [1.0, 1.5],
        "home_gf": [1.8, 1.2],
        "away_ga": [1.4, 1.0],
    })
    out = add_candidate_interactions(df)
    assert np.allclose(out["overall_ppg_diff"], [1.0, -0.5])
    assert np.allclose(out["home_strength_x_away_weakness"], [1.4, -0.5])
    assert np.allclose(out["home_attack_x_away_defence"], [2.52, 1.2])


def test_missing_constituent_is_not_pseudo_counted():
    df = pd.DataFrame({
        "home_ppg": [2.0],
        "away_ppg": [1.0],
        "home_gf": [1.8],
        "away_ga": [np.nan],
    })
    out = add_candidate_interactions(df)
    assert pd.isna(out.loc[0, "home_strength_x_away_weakness"])
    assert pd.isna(out.loc[0, "home_attack_x_away_defence"])


def test_same_kickoff_is_excluded_from_prior_history():
    history = np.array([100, 200, 300, 400])
    assert strict_prior_mask(history, 300).tolist() == [True, True, False, False]
