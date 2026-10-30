import unittest
from scripts.analyze_selected50_xg_odds_mask_audit import (
    wilson_interval, get_pair, identify_xg_outlier_seasons, pair_row,
    ZERO_CO_OCCURRENCE_FIELDS,
)

class Selected50XgOddsMaskAuditTests(unittest.TestCase):
    def test_zero_mask_field_contract_is_twenty_fields(self):
        self.assertEqual(len(ZERO_CO_OCCURRENCE_FIELDS), 20)
        self.assertIn("team_a_xg", ZERO_CO_OCCURRENCE_FIELDS)
        self.assertIn("team_b_xg", ZERO_CO_OCCURRENCE_FIELDS)
        self.assertIn("total_xg", ZERO_CO_OCCURRENCE_FIELDS)
        self.assertIn("odds_doublechance_12", ZERO_CO_OCCURRENCE_FIELDS)

    def test_wilson_interval_handles_zero_and_high_missingness_samples(self):
        self.assertEqual(wilson_interval(0, 72), (0.0, 5.1))
        self.assertEqual(wilson_interval(54, 63), (75.0, 92.3))

    def test_wilson_interval_rejects_invalid_counts(self):
        with self.assertRaises(ValueError):
            wilson_interval(4, 3)
        self.assertEqual(wilson_interval(0, 0), (None, None))

    def test_xg_outlier_gate_keeps_minimum_sample_and_rate_threshold(self):
        rows = [
            {"season_id":"A","numeric_rows":36,"zero_pct":50.0},
            {"season_id":"B","numeric_rows":29,"zero_pct":80.0},
            {"season_id":"C","numeric_rows":50,"zero_pct":29.9},
        ]
        self.assertEqual(identify_xg_outlier_seasons(rows), {"A"})

    def test_pair_lookup_normalizes_reversed_pair(self):
        row = {
            "scope_id":"S1", "field_a":"odds_btts_yes", "field_b":"team_a_xg_prematch",
            "field_a_zero_rows_on_pair_complete_rows":"5",
            "field_b_zero_rows_on_pair_complete_rows":"2",
            "field_a_zero_field_b_nonzero_rows":"4",
            "field_a_nonzero_field_b_zero_rows":"1",
        }
        normalized = get_pair({("S1","odds_btts_yes","team_a_xg_prematch"):row},
                              "S1", "team_a_xg_prematch", "odds_btts_yes")
        self.assertEqual(normalized["field_a_zero_rows_on_pair_complete_rows"], "2")
        self.assertEqual(normalized["field_b_zero_rows_on_pair_complete_rows"], "5")
        self.assertEqual(normalized["field_a_zero_field_b_nonzero_rows"], "1")
        self.assertEqual(normalized["field_a_nonzero_field_b_zero_rows"], "4")

    def test_missing_pair_is_explicit_not_silently_zero(self):
        result = pair_row(None, {"country":"X","competition_name":"League"},
                          "S1","team_a_xg_prematch","team_a_xg","PREMATCH_XG_ZERO_MASK")
        self.assertEqual(result["pair_status"], "PAIR_NOT_PRESENT_IN_SOURCE_ARTIFACT")

if __name__ == "__main__":
    unittest.main()
