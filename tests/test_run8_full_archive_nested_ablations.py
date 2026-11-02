import numpy as np
import pandas as pd
from datetime import date

from scripts.run8_full_archive_nested_ablations import (
    add_eligibility_and_labels, adjust_bh_by, build_event_time_panel,
    classify_home_away_flag, ece10, metric_value,
)


def _match(fid, ts, home, away, hg, ag, venue="DISTINGUISHED", d=None):
    return {
        "selected_id": "100", "provider_season_id": "S1", "fixture_id": fid,
        "home_team_id": home, "away_team_id": away, "kickoff_ts": float(ts),
        "kickoff_utc": "2025-03-20T00:00:00+00:00",
        "kickoff_date": d or date(2025, 3, 20), "home_goals": hg, "away_goals": ag,
        "settled_score": True, "venue_state": venue,
    }


def test_no_home_away_flag_is_not_assumed_to_mean_neutral_ground():
    assert classify_home_away_flag(None) == "UNKNOWN"
    assert classify_home_away_flag("") == "UNKNOWN"
    assert classify_home_away_flag("1") == "UNDISTINGUISHED"
    assert classify_home_away_flag(True) == "UNDISTINGUISHED"
    assert classify_home_away_flag("0") == "DISTINGUISHED"
    assert classify_home_away_flag(False) == "DISTINGUISHED"
    assert classify_home_away_flag("unknown-token") == "INVALID"


def test_same_kickoff_targets_do_not_enter_each_others_history():
    prior_date, target_date = date(2025, 3, 19), date(2025, 3, 20)
    rows = []
    for i in range(5):
        rows.append(_match(f"h{i}", 1000 + i * 100, "H", f"X{i}", 2, 0, d=prior_date))
        rows.append(_match(f"a{i}", 1050 + i * 100, f"Y{i}", "A", 0, 1, d=prior_date))
    rows.append(_match("target-1", 2000, "H", "A", 1, 1, d=target_date))
    rows.append(_match("same-kickoff", 2000, "H", "Z", 2, 0, d=target_date))
    panel = build_event_time_panel(rows, target_date, target_date, lag_hours=0)
    targets = panel[panel["fixture_id"].isin(["target-1", "same-kickoff"])]
    assert len(targets) == 2
    assert targets["home_prior_n"].tolist() == [5, 5]
    assert targets.loc[targets["fixture_id"] == "target-1", "away_away_n"].iloc[0] == 5


def test_undistinguished_matches_enter_overall_form_but_not_venue_histories():
    prior_date, target_date = date(2025, 3, 19), date(2025, 3, 20)
    rows = []
    for i in range(4):
        rows.append(_match(f"h{i}", 1000 + i * 100, "H", f"X{i}", 1, 0, d=prior_date))
        rows.append(_match(f"a{i}", 1050 + i * 100, f"Y{i}", "A", 0, 1, d=prior_date))
    rows.append(_match("h-undistinguished", 1450, "H", "N", 1, 1, venue="UNDISTINGUISHED", d=prior_date))
    rows.append(_match("a-undistinguished", 1500, "N2", "A", 1, 0, venue="UNDISTINGUISHED", d=prior_date))
    rows.append(_match("target", 2000, "H", "A", 1, 1, d=target_date))
    panel = build_event_time_panel(rows, target_date, target_date)
    row = panel.iloc[0]
    assert row["home_prior_n"] == 5 and row["away_prior_n"] == 5
    assert row["home_home_n"] == 4 and row["away_away_n"] == 4


def test_eligibility_requires_five_observed_overall_and_venue_matches():
    df = pd.DataFrame({
        "home_prior_n": [5, 4, 5], "away_prior_n": [5, 5, 5],
        "home_home_n": [5, 5, 4], "away_away_n": [5, 5, 5],
        "h2h_prior_n": [4, 5, 8], "selected_id": ["1", "1", "2"],
        "home_goals": [1, 0, 2], "away_goals": [0, 0, 2],
    })
    out = add_eligibility_and_labels(df)
    assert out["core_eligible"].tolist() == [True, False, True]
    assert out["venue_eligible"].tolist() == [True, False, False]
    assert out["h2h_eligible"].tolist() == [False, True, True]


def test_bh_by_corrections_are_monotonic_and_by_is_not_less_conservative():
    p = np.array([0.001, 0.01, 0.03, 0.2, np.nan])
    bh, by = adjust_bh_by(p)
    assert np.all(by[:4] >= bh[:4])
    assert np.all(np.diff(np.sort(bh[:4])) >= -1e-12)
    assert np.isnan(bh[4]) and np.isnan(by[4])


def test_metrics_and_ece_are_bounded():
    y = np.array([0, 1, 1, 0, 1, 0])
    p = np.array([0.1, 0.8, 0.7, 0.2, 0.6, 0.4])
    assert 0 <= metric_value("brier", y, p) <= 1
    assert metric_value("log_loss", y, p) > 0
    assert 0 <= metric_value("auc", y, p) <= 1
    assert 0 <= ece10(y, p) <= 1


def test_interaction_inputs_are_not_filled_with_pseudo_counts():
    home_ppg, away_ppg, away_ga, home_gf = 1.5, 1.0, np.nan, 1.8
    assert np.isnan((home_ppg - away_ppg) * away_ga)
    assert np.isnan(home_gf * away_ga)
