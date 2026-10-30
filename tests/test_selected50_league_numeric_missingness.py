import unittest
from scripts.analyze_selected50_league_numeric_missingness import zero_rate, build_outlier_lists, zero_count_parity, build_scope_rows

class LeagueNumericMissingnessTests(unittest.TestCase):
    def test_zero_rate_keeps_denominator(self):
        self.assertEqual(zero_rate(5, 20), 25.0)
        self.assertIsNone(zero_rate(0, 0))

    def test_outlier_rows_keep_sample_size(self):
        rows = [
            {"scope_id":"A","country":"X","competition_name":"L1","field_name":"odds_btts_yes","sample_rows":40,"zero_rows":20,"zero_pct":50.0},
            {"scope_id":"B","country":"Y","competition_name":"L2","field_name":"odds_btts_yes","sample_rows":10,"zero_rows":10,"zero_pct":100.0},
        ]
        result = build_outlier_lists(rows, min_sample=30)
        self.assertEqual(len(result["full_time_btts_odds"]), 1)
        self.assertEqual(result["full_time_btts_odds"][0]["sample_rows"], 40)

    def test_absent_field_is_explicitly_flagged(self):
        rows = [{
            "subset":"primary_window_provider_complete","scope_id":"L1","country":"X","competition_name":"L1",
            "selected_current_season":False,"field_name":"team_a_xg_prematch","total_rows":"40",
            "numeric_rows":"40","zero_rows":"2","non_numeric_rows":"0","negative_rows":"0",
        }]
        result = build_scope_rows(rows, "LEAGUE_GROUP")
        absent = [r for r in result if r["field_name"] == "odds_btts_yes"][0]
        self.assertEqual(absent["quality_flag"], "FIELD_ABSENT_OR_UNOBSERVED")
        self.assertEqual(absent["scope_rows"], 40)

    def test_zero_count_parity_is_counted_by_scope(self):
        rows = []
        for scope, a, b in [("L1",5,5),("L2",2,3)]:
            rows.extend([
                {"scope_type":"LEAGUE_GROUP","scope_id":scope,"field_name":"odds_btts_yes","zero_rows":a},
                {"scope_type":"LEAGUE_GROUP","scope_id":scope,"field_name":"odds_btts_no","zero_rows":b},
            ])
        result = zero_count_parity(rows)
        self.assertEqual(result["odds_btts_yes/odds_btts_no"]["scopes_compared"], 2)
        self.assertEqual(result["odds_btts_yes/odds_btts_no"]["scopes_with_equal_zero_counts"], 1)

if __name__ == "__main__":
    unittest.main()
