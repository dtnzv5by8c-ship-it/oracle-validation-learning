import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_oracle_season_crosswalk.py"
SPEC = importlib.util.spec_from_file_location("validate_oracle_season_crosswalk", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SeasonCrosswalkTests(unittest.TestCase):
    def test_iso_date_parsing(self):
        self.assertEqual(str(MODULE.parse_date("2025-07-01")), "2025-07-01")
        self.assertIsNone(MODULE.parse_date(""))
        self.assertIsNone(MODULE.parse_date("not-a-date"))

    def test_end_before_start_is_error(self):
        header = "target_code,catalogue_status,provider_league_id,provider_name,candidate_season_ids,candidate_season_labels,candidate_season_dates,decision\n"
        row = "E0,EXACT_ALIAS_CANDIDATE,10,England Premier League,100,2025/26,2026-06-01/2025-08-01,REVIEW_REQUIRED_NOT_AUTO_MAPPED\n"
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "crosswalk.csv"
            p.write_text(header + row, encoding="utf-8")
            errors, warnings, metrics = MODULE.validate(p)
        self.assertTrue(any("season end precedes season start" in e for e in errors))
        self.assertEqual(metrics["mapping_approval"], "NOT_GRANTED")

    def test_missing_dates_warn_and_do_not_auto_approve(self):
        header = "target_code,catalogue_status,provider_league_id,provider_name,candidate_season_ids,candidate_season_labels,candidate_season_dates,decision\n"
        row = "E0,EXACT_ALIAS_CANDIDATE,10,England Premier League,100,2025/26,/,REVIEW_REQUIRED_NOT_AUTO_MAPPED\n"
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "crosswalk.csv"
            p.write_text(header + row, encoding="utf-8")
            errors, warnings, metrics = MODULE.validate(p)
        self.assertFalse(errors)
        self.assertFalse(any("malformed season date pair" in w or "missing or invalid ISO season dates" in w for w in warnings))
        self.assertEqual(metrics["mapping_approval"], "NOT_GRANTED")


if __name__ == "__main__":
    unittest.main()
