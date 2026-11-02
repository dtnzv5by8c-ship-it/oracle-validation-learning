import unittest
import numpy as np
import pandas as pd

from scripts.run8_selected50_btts_goal_environment import derive_goal_environment_features


def make_record(ts, fixture, home, away, hg, ag, venue="DISTINGUISHED"):
    return {
        "selected_id": "league-1", "provider_season_id": "season-1",
        "fixture_id": fixture, "home_team_id": home, "away_team_id": away,
        "kickoff_ts": float(ts), "kickoff_utc": f"2026-01-{int(ts):02d}T12:00:00",
        "kickoff_date": pd.Timestamp("2026-01-01") + pd.Timedelta(days=int(ts)-1),
        "home_goals": int(hg), "away_goals": int(ag), "settled_score": True,
        "venue_state": venue,
    }


def target_panel():
    return pd.DataFrame([{
        "selected_id": "league-1", "provider_season_id": "season-1",
        "fixture_id": "target", "kickoff_ts": 100.0,
        "kickoff_date": pd.Timestamp("2026-04-10").date(),
    }])


class GoalEnvironmentFeatureTests(unittest.TestCase):
    def test_five_prior_h2h_and_venue_rates_and_same_kickoff_exclusion(self):
        records = [make_record(i, f"prior-{i}", "H", "A", 1, 1) for i in range(1, 6)]
        records.extend(make_record(i + 5, f"other-{i}", f"X{i}", f"Y{i}", 2, 0) for i in range(45))
        records.append(make_record(100, "target", "H", "A", 1, 0))
        records.append(make_record(100, "same-time", "H", "Z", 0, 0))
        row = derive_goal_environment_features(records, target_panel()).iloc[0]
        self.assertEqual(row["home_goal_history_n"], 5)
        self.assertEqual(row["away_goal_history_n"], 5)
        self.assertEqual(row["home_home_goal_history_n"], 5)
        self.assertEqual(row["away_away_goal_history_n"], 5)
        self.assertEqual(row["h2h_goal_history_n"], 5)
        self.assertEqual(row["league_goal_history_n"], 50)
        self.assertAlmostEqual(row["home_btts_rate5"], 1.0)
        self.assertAlmostEqual(row["away_btts_rate5"], 1.0)
        self.assertAlmostEqual(row["home_home_btts_rate5"], 1.0)
        self.assertAlmostEqual(row["away_away_btts_rate5"], 1.0)
        self.assertAlmostEqual(row["h2h_btts_rate5"], 1.0)
        self.assertAlmostEqual(row["league_btts_rate50"], 5 / 50)
        self.assertAlmostEqual(row["home_score_rate5"], 1.0)

    def test_four_observed_matches_do_not_create_five_match_features(self):
        records = [make_record(i, f"prior-{i}", "H", "A", 1, 1) for i in range(1, 5)]
        records.append(make_record(100, "target", "H", "A", 1, 0))
        row = derive_goal_environment_features(records, target_panel()).iloc[0]
        self.assertEqual(row["home_goal_history_n"], 4)
        self.assertEqual(row["away_goal_history_n"], 4)
        self.assertEqual(row["home_home_goal_history_n"], 4)
        self.assertEqual(row["away_away_goal_history_n"], 4)
        self.assertEqual(row["h2h_goal_history_n"], 4)
        self.assertTrue(np.isnan(row["home_btts_rate5"]))
        self.assertTrue(np.isnan(row["home_home_btts_rate5"]))
        self.assertTrue(np.isnan(row["h2h_btts_rate5"]))

    def test_league_environment_missing_below_50_observed_matches(self):
        records = [make_record(i, f"prior-{i}", "H", "A", 1, 1) for i in range(1, 6)]
        records.extend(make_record(i + 5, f"other-{i}", f"X{i}", f"Y{i}", 2, 0) for i in range(44))
        records.append(make_record(100, "target", "H", "A", 1, 0))
        row = derive_goal_environment_features(records, target_panel()).iloc[0]
        self.assertEqual(row["league_goal_history_n"], 49)
        self.assertTrue(np.isnan(row["league_btts_rate50"]))


if __name__ == "__main__":
    unittest.main()
