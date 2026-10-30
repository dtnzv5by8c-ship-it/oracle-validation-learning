import unittest
from datetime import date
from scripts.build_selected50_calendar_year_coverage import summarize, FIELDS

class Selected50CalendarYearCoverageTests(unittest.TestCase):
    def test_exact_year_summary_preserves_status_and_numeric_zero(self):
        rows = [
            {"id": "1", "status": "complete", "date": "2024-01-01", "team_a_xg_prematch": 0, "odds_btts_yes": "1.85"},
            {"id": "2", "status": "incomplete", "date": "2024-12-31", "team_a_xg_prematch": "1.2", "odds_btts_yes": 0},
            {"id": "3", "status": "suspended", "date": "2024-06-15", "team_a_xg_prematch": None, "odds_btts_yes": "N/A"},
            {"id": "4", "status": "incomplete", "date": "2027-01-01", "team_a_xg_prematch": 0.9, "odds_btts_yes": 2.1},
        ]
        result = summarize(rows, date(2026, 10, 30))
        self.assertEqual(result["match_rows"], 4)
        self.assertEqual(result["unique_provider_match_ids"], 4)
        self.assertEqual(result["status_counts"], {"complete": 1, "incomplete": 2, "suspended": 1})
        self.assertEqual(result["field_quality"]["team_a_xg_prematch"]["zero_rows"], 1)
        self.assertEqual(result["kickoff_on_or_before_audit_date_rows"], 3)
        self.assertEqual(result["kickoff_after_audit_date_rows"], 1)
        self.assertEqual(result["field_quality"]["team_a_xg_prematch"]["positive_rows"], 2)
        self.assertEqual(result["field_quality"]["odds_btts_yes"]["zero_rows"], 1)
        self.assertEqual(result["field_quality"]["odds_btts_yes"]["missing_or_nonnumeric_rows"], 1)

    def test_duplicate_provider_ids_are_reported_not_collapsed(self):
        rows = [
            {"id": "same", "status": "complete", "date": "2024-01-01"},
            {"id": "same", "status": "complete", "date": "2024-02-01"},
            {"status": "complete", "date": "2024-03-01"},
        ]
        result = summarize(rows, date(2026, 10, 30))
        self.assertEqual(result["match_rows"], 3)
        self.assertEqual(result["unique_provider_match_ids"], 1)
        self.assertEqual(result["duplicate_provider_match_id_rows"], 1)

    def test_missing_features_are_not_imputed(self):
        result = summarize([{"id": "1", "status": "complete", "date": "2024-01-01"}], date(2026, 10, 30))
        self.assertEqual(set(result["field_quality"]), set(FIELDS))
        for field in FIELDS:
            self.assertEqual(result["field_quality"][field]["numeric_rows"], 0)
            self.assertEqual(result["field_quality"][field]["missing_or_nonnumeric_rows"], 1)
            self.assertEqual(result["field_quality"][field]["zero_rows"], 0)

if __name__ == "__main__":
    unittest.main()
