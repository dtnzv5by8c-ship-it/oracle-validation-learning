import sys
import unittest
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_oracle_team_market_oos_profiles import build_profiles, wilson


class TeamMarketOosProfileTests(unittest.TestCase):
    def test_wilson_small_sample(self):
        lo, hi = wilson(5, 5)
        self.assertAlmostEqual(lo, .5655, places=3)
        self.assertEqual(hi, 1.0)

    def test_exact_join_role_assignment_and_low_sample_safeguard(self):
        matches = pd.DataFrame([
            {"match_id":"m1","date":"2025-01-01","league_code":"L","home_team":"A","away_team":"B"},
            {"match_id":"m2","date":"2025-02-01","league_code":"L","home_team":"A","away_team":"C"},
        ])
        oos = pd.DataFrame([
            {"match_id":"m1","date":"2025-01-01","model":"DC_HOME","raw_probability":.7,"target":1},
            {"match_id":"m2","date":"2025-02-01","model":"DC_HOME","raw_probability":.6,"target":0},
            {"match_id":"m1","date":"2025-01-01","model":"DC_AWAY","raw_probability":.4,"target":0},
            {"match_id":"m2","date":"2025-02-01","model":"DC_AWAY","raw_probability":.5,"target":1},
        ])
        team, chrono, league, meta = build_profiles(oos, matches)
        self.assertEqual(meta["match_join_coverage"], 1.0)
        self.assertEqual(set(team.team), {"A","B","C"})
        self.assertFalse(team.candidate_discordant_for_review.any())
        self.assertEqual(len(chrono), 0)

    def test_discordance_flag_requires_minimum_sample_and_wilson_exclusion(self):
        matches, oos = [], []
        for i in range(40):
            mid = f"m{i:03d}"
            date = f"2025-{1+i//28:02d}-{1+i%28:02d}"
            matches.append({"match_id":mid,"date":date,"league_code":"L","home_team":"A","away_team":f"B{i}"})
            oos.append({"match_id":mid,"date":date,"model":"DC_HOME","raw_probability":.1,"target":1})
        team, chrono, league, meta = build_profiles(pd.DataFrame(oos), pd.DataFrame(matches))
        row = team[team.team == "A"].iloc[0]
        self.assertTrue(row.candidate_discordant_for_review)
        self.assertEqual(row.n, 40)
        self.assertEqual(len(chrono[chrono.team == "A"]), 2)
        self.assertGreater(row.beta_1_1_shrunk_rate, .9)

    def test_duplicate_prediction_key_fails_closed(self):
        matches = pd.DataFrame([{"match_id":"m1","date":"2025-01-01","league_code":"L","home_team":"A","away_team":"B"}])
        row = {"match_id":"m1","date":"2025-01-01","model":"DC_HOME","raw_probability":.5,"target":1}
        with self.assertRaises(ValueError):
            build_profiles(pd.DataFrame([row,row]), matches)

    def test_date_mismatch_fails_closed(self):
        matches = pd.DataFrame([{"match_id":"m1","date":"2025-01-02","league_code":"L","home_team":"A","away_team":"B"}])
        oos = pd.DataFrame([{"match_id":"m1","date":"2025-01-01","model":"DC_HOME","raw_probability":.5,"target":1}])
        with self.assertRaises(ValueError):
            build_profiles(oos, matches)


if __name__ == "__main__":
    unittest.main()
