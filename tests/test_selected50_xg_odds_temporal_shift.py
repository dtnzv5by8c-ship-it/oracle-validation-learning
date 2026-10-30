import unittest

from scripts.audit_selected50_xg_odds_temporal_shift import (
    aggregate_period, build_xg_shift_rows, select_current_xg_outliers,
    wilson_interval, build_summary,
)


class Selected50XgOddsTemporalShiftTests(unittest.TestCase):
    def test_wilson_interval_known_values(self):
        self.assertEqual(wilson_interval(20, 50), (27.61, 53.82))
        self.assertEqual(wilson_interval(0, 0), (None, None))

    def test_current_outlier_gate_requires_sample_and_rate(self):
        rows = [
            {"subset": "primary_window_provider_complete", "selected_current_season": "True",
             "field_name": "team_a_xg_prematch", "country": "A", "competition_name": "L",
             "numeric_rows": "30", "zero_rows": "9"},
            {"subset": "primary_window_provider_complete", "selected_current_season": "True",
             "field_name": "team_b_xg_prematch", "country": "B", "competition_name": "L",
             "numeric_rows": "29", "zero_rows": "20"},
            {"subset": "primary_window", "selected_current_season": "True",
             "field_name": "team_a_xg_prematch", "country": "C", "competition_name": "L",
             "numeric_rows": "50", "zero_rows": "40"},
        ]
        self.assertEqual(select_current_xg_outliers(rows), {("A", "L")})

    def test_period_aggregation_keeps_current_and_historical_separate(self):
        rows = [
            {"subset": "primary_window_provider_complete", "selected_current_season": "True",
             "scope_id": "C1", "country": "A", "competition_name": "L",
             "field_name": "team_a_xg_prematch", "numeric_rows": "50", "zero_rows": "20"},
            {"subset": "primary_window_provider_complete", "selected_current_season": "False",
             "scope_id": "H1", "country": "A", "competition_name": "L",
             "field_name": "team_a_xg_prematch", "numeric_rows": "100", "zero_rows": "5"},
            {"subset": "primary_window_provider_complete", "selected_current_season": "False",
             "scope_id": "H2", "country": "A", "competition_name": "L",
             "field_name": "team_a_xg_prematch", "numeric_rows": "100", "zero_rows": "5"},
        ]
        current = aggregate_period(rows, "A", "L", "team_a_xg_prematch", True)
        historical = aggregate_period(rows, "A", "L", "team_a_xg_prematch", False)
        self.assertEqual((current["numeric_rows"], current["zero_rows"], current["zero_pct"]),
                         (50, 20, 40.0))
        self.assertEqual((historical["numeric_rows"], historical["zero_rows"],
                          historical["zero_pct"], historical["season_count"]),
                         (200, 10, 5.0, 2))

    def test_shift_rows_are_field_specific_and_include_uncertainty(self):
        rows = []
        for field, zeros in (("team_a_xg_prematch", 20),
                             ("team_b_xg_prematch", 20),
                             ("total_xg_prematch", 18)):
            rows.extend([
                {"subset": "primary_window_provider_complete", "selected_current_season": "True",
                 "scope_id": "C", "country": "A", "competition_name": "L",
                 "field_name": field, "numeric_rows": "50", "zero_rows": str(zeros)},
                {"subset": "primary_window_provider_complete", "selected_current_season": "False",
                 "scope_id": "H1", "country": "A", "competition_name": "L",
                 "field_name": field, "numeric_rows": "200", "zero_rows": "10"},
            ])
        result = build_xg_shift_rows(rows)
        self.assertEqual(len(result), 3)
        self.assertTrue(all(row["current_wilson95_low_pct"] is not None for row in result))
        self.assertEqual(result[0]["absolute_zero_rate_change_pp"], 35.0)

    def test_summary_does_not_claim_event_lag_is_provider_freshness(self):
        qa = {"audit_date_utc": "2026-10-30", "primary_window_end": "2026-09-20"}
        result = build_summary(qa, [], {})
        self.assertEqual(result["archive_audit_to_event_window_end_lag_days"], 40)
        self.assertIn("not a source retrieval timestamp", result["lag_interpretation"])
        self.assertFalse(result["production_eligible"])
        self.assertFalse(result["betting_eligible"])


if __name__ == "__main__":
    unittest.main()
