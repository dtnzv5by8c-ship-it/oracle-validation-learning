import importlib.util
import unittest
from datetime import datetime, timezone, timedelta

SPEC = importlib.util.spec_from_file_location(
    "goal_engine", "scripts/build_goal_market_research_engine.py"
)
engine = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(engine)

class GoalMarketResearchEngineTests(unittest.TestCase):
    def make_match(self, fid, day, home, away, hg, ag):
        return {
            "fixture_id": str(fid), "provider_season_id": "S1",
            "home_team_id": str(home), "away_team_id": str(away),
            "kickoff_utc": (datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=day)).isoformat(),
            "status_raw": "complete", "home_goals": str(hg), "away_goals": str(ag)
        }

    def test_goal_market_probabilities_are_coherent_and_research_only(self):
        rows=[]
        # Twenty completed league matches establish baseline; both target teams have
        # at least three prior matches and usable venue splits.
        for i in range(20):
            rows.append(self.make_match(i+1, i, 1 if i%2==0 else 2, 2 if i%2==0 else 1, 2, 1))
        teams, leagues = engine.build_indexes(rows)
        target={"provider_season_id":"S1","fixture_id":"999",
                "home_team_provider_id":"1","away_team_provider_id":"2"}
        cutoff=datetime(2026, 2, 1, tzinfo=timezone.utc)
        result=engine.forecast(target, teams, leagues, cutoff)
        self.assertEqual(result["status"], "EXPERIMENTAL_UNCALIBRATED")
        self.assertGreaterEqual(result["over15_probability_pct"], result["over25_probability_pct"])
        self.assertGreaterEqual(result["under45_probability_pct"], result["under15_probability_pct"] if "under15_probability_pct" in result else 0)
        self.assertIn("league_baseline_over15_probability_pct", result)
        self.assertGreaterEqual(result["league_baseline_over15_probability_pct"], 0)
        self.assertEqual(result["production_eligible"], "NO")
        self.assertEqual(result["betting_eligible"], "NO")

    def test_future_matches_do_not_enter_history(self):
        rows=[]
        for i in range(25):
            rows.append(self.make_match(i+1, i, 1 if i%2==0 else 2, 2 if i%2==0 else 1, 3, 0))
        teams, leagues=engine.build_indexes(rows)
        target={"provider_season_id":"S1","fixture_id":"999",
                "home_team_provider_id":"1","away_team_provider_id":"2"}
        cutoff=datetime(2026, 1, 10, tzinfo=timezone.utc)
        result=engine.forecast(target, teams, leagues, cutoff)
        self.assertEqual(result["status"], "BLOCKED_LEAGUE_BASELINE_LT20")
        self.assertEqual(result["league_prior_n"], 9)

    def test_target_fixture_is_excluded_even_if_timestamp_precedes_cutoff(self):
        rows=[]
        for i in range(20):
            rows.append(self.make_match(i+1, i, 1 if i%2==0 else 2, 2 if i%2==0 else 1, 1, 1))
        target_row=self.make_match(999, 5, 1, 2, 8, 0)
        rows.append(target_row)
        teams, leagues=engine.build_indexes(rows)
        target={"provider_season_id":"S1","fixture_id":"999",
                "home_team_provider_id":"1","away_team_provider_id":"2"}
        result=engine.forecast(target, teams, leagues, datetime(2026, 2, 1, tzinfo=timezone.utc))
        self.assertEqual(result["status"], "EXPERIMENTAL_UNCALIBRATED")
        self.assertEqual(result["league_prior_n"], 20)

if __name__ == "__main__":
    unittest.main()
