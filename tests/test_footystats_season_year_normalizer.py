import unittest

from scripts.normalize_footystats_season_year import normalize_season_year


class FootyStatsSeasonYearTests(unittest.TestCase):
    def test_concatenated_consecutive_years(self):
        got = normalize_season_year("20262027")
        self.assertEqual(got.raw_token, "20262027")
        self.assertEqual(got.start_year, 2026)
        self.assertEqual(got.end_year, 2027)
        self.assertEqual(got.status, "CONSECUTIVE_YEAR_RANGE")

    def test_four_digit_year_preserves_unknown_end_year(self):
        got = normalize_season_year("2026")
        self.assertEqual(got.raw_token, "2026")
        self.assertEqual(got.start_year, 2026)
        self.assertIsNone(got.end_year)
        self.assertEqual(got.status, "START_YEAR_ONLY")

    def test_invalid_eight_digit_range_is_quarantined(self):
        got = normalize_season_year("20252027")
        self.assertIsNone(got.start_year)
        self.assertIsNone(got.end_year)
        self.assertEqual(got.status, "INVALID_EIGHT_DIGIT_RANGE")

    def test_unknown_format_is_quarantined(self):
        got = normalize_season_year("2026/27")
        self.assertIsNone(got.start_year)
        self.assertIsNone(got.end_year)
        self.assertEqual(got.status, "UNSUPPORTED_YEAR_TOKEN")

    def test_blank_and_none_are_missing(self):
        self.assertEqual(normalize_season_year("").status, "MISSING_YEAR_TOKEN")
        self.assertEqual(normalize_season_year(None).status, "MISSING_YEAR_TOKEN")


if __name__ == "__main__":
    unittest.main()
