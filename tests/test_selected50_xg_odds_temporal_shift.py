import unittest

from scripts.audit_selected50_xg_odds_temporal_shift import (
    aggregate_period, build_xg_shift_rows, select_current_xg_outliers,
    wilson_interval, build_summary, as_int, validate_numeric_quality_rows,
    EXPECTED_ARCHIVE_SHA256,
)


class Selected50XgOddsTemporalShiftTests(unittest.TestCase):
    def test_archive_checksum_pin_matches_current_verified_archive(self):
        self.assertEqual(EXPECTED_ARCHIVE_SHA256, "7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f")

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



    def test_count_parser_rejects_silent_truncation_and_invalid_values(self):
        self.assertEqual(as_int("3.0"), 3)
        for value in (True, False, "", "NaN", "inf", "-1", "2.5", "not-a-count"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    as_int(value)

    def test_zero_count_cannot_exceed_numeric_population(self):
        row = {
            "subset": "primary_window_provider_complete", "selected_current_season": "True",
            "scope_id": "C1", "country": "A", "competition_name": "L",
            "field_name": "team_a_xg_prematch", "numeric_rows": "5", "zero_rows": "6",
        }
        with self.assertRaises(ValueError):
            select_current_xg_outliers([row])

    def test_duplicate_scope_field_rows_fail_closed(self):
        row = {
            "subset": "primary_window_provider_complete", "selected_current_season": "True",
            "scope_id": "C1", "country": "A", "competition_name": "L",
            "field_name": "team_a_xg_prematch", "numeric_rows": "50", "zero_rows": "10",
        }
        with self.assertRaises(ValueError):
            validate_numeric_quality_rows([row, dict(row)])

    def test_all_group_pool_is_separate_from_outlier_selected_pool(self):
        rows = []
        for field in ("team_a_xg_prematch", "team_b_xg_prematch", "total_xg_prematch"):
            for country, current_zeros, historical_zeros in (("A", 20, 5), ("B", 5, 2)):
                rows.extend([
                    {"subset": "primary_window_provider_complete", "selected_current_season": "True",
                     "scope_id": f"{country}C", "country": country, "competition_name": "L",
                     "field_name": field, "numeric_rows": "50", "zero_rows": str(current_zeros)},
                    {"subset": "primary_window_provider_complete", "selected_current_season": "False",
                     "scope_id": f"{country}H", "country": country, "competition_name": "L",
                     "field_name": field, "numeric_rows": "100", "zero_rows": str(historical_zeros)},
                ])
        validate_numeric_quality_rows(rows)
        shift_rows = build_xg_shift_rows(rows)
        self.assertEqual(len(shift_rows), 6)
        summary = build_summary({"selected_leagues_in_manifest": 3}, shift_rows, {})
        all_groups = summary["pooled_xg_current_vs_historical"]["team_a_xg_prematch"]
        flagged = summary["pooled_xg_current_vs_historical_flagged_leagues"]["team_a_xg_prematch"]
        self.assertEqual((all_groups["current_n"], all_groups["current_zero"]), (100, 25))
        self.assertEqual((all_groups["historical_n"], all_groups["historical_zero"]), (200, 7))
        self.assertEqual((flagged["current_n"], flagged["current_zero"]), (50, 20))
        self.assertEqual((flagged["historical_n"], flagged["historical_zero"]), (100, 5))
        self.assertEqual(summary["xg_outlier_screen"]["current_selected_groups_with_xg_qa_rows"], 2)
        self.assertEqual(summary["xg_outlier_screen"]["selected_groups_without_current_xg_qa_rows"], 1)
        self.assertEqual(summary["xg_outlier_screen"]["flagged_league_count"], 1)
        self.assertFalse(summary["production_eligible"])
        self.assertFalse(summary["betting_eligible"])

if __name__ == "__main__":
    unittest.main()
