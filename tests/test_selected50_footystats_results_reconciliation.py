import unittest
from scripts.reconcile_selected50_actual_results_footystats import reconcile

class FootyStatsSettlementTests(unittest.TestCase):
    def setUp(self):
        self.runtime = [{
            "provider_season_id": "100", "fixture_id": "200",
            "home_team_provider_id": "10", "away_team_provider_id": "20",
            "date_utc": "2026-11-01T15:00:00Z", "home_team": "Home", "away_team": "Away",
            "league": "Test League"
        }]
        self.match = {"id": 200, "homeID": 10, "awayID": 20, "status": "complete",
                      "homeGoalCount": 2, "awayGoalCount": 1, "date_unix": 1793545200}

    def test_exact_completed_result_settles_markets(self):
        rows = reconcile(self.runtime, {"100": [self.match]}, set(), "2026-11-01T16:00:00Z")
        row = rows[0]
        self.assertEqual(row["settlement_status"], "SETTLED_VERIFIED_PROVIDER_SCORE")
        self.assertEqual((row["actual_home_goals"], row["actual_away_goals"]), (2, 1))
        self.assertEqual(row["actual_btts"], "YES")
        self.assertEqual(row["actual_over_1_5"], "YES")
        self.assertEqual(row["actual_over_2_5"], "YES")
        self.assertEqual(row["actual_under_4_5"], "YES")
        self.assertEqual(row["production_eligible"], "NO")

    def test_wrong_team_orientation_does_not_join(self):
        reversed_match = dict(self.match, homeID=20, awayID=10)
        row = reconcile(self.runtime, {"100": [reversed_match]}, set(), "now")[0]
        self.assertEqual(row["settlement_status"], "PENDING_OR_NOT_FOUND")

    def test_duplicate_identity_is_quarantined(self):
        row = reconcile(self.runtime, {"100": [self.match, dict(self.match)]}, set(), "now")[0]
        self.assertEqual(row["settlement_status"], "QUARANTINED_DUPLICATE_PROVIDER_IDENTITY")

    def test_unfinished_match_is_not_settled(self):
        pending = dict(self.match, status="incomplete")
        row = reconcile(self.runtime, {"100": [pending]}, set(), "now")[0]
        self.assertEqual(row["settlement_status"], "PENDING_NOT_COMPLETED")
        self.assertEqual(row["actual_home_goals"], "")

    def test_failed_season_is_retryable(self):
        row = reconcile(self.runtime, {}, {"100"}, "now")[0]
        self.assertEqual(row["settlement_status"], "API_ERROR_RETRY_REQUIRED")

if __name__ == "__main__":
    unittest.main()
