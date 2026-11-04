import datetime as dt
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_selected50_research_runtime import resolve_report_window


class Selected50ReportWindowTests(unittest.TestCase):
    def tearDown(self):
        os.environ.pop("ORACLE_REPORT_START_DATE", None)
        os.environ.pop("ORACLE_REPORT_END_DATE", None)

    def test_requested_6_to_24_november_window_is_inclusive(self):
        os.environ["ORACLE_REPORT_START_DATE"] = "2026-11-06"
        os.environ["ORACLE_REPORT_END_DATE"] = "2026-11-24"
        now = dt.datetime(2026, 11, 4, 6, 0, tzinfo=dt.timezone.utc).timestamp()
        start, end_exclusive, start_text, end_text = resolve_report_window(now)
        self.assertEqual(start_text, "2026-11-06")
        self.assertEqual(end_text, "2026-11-24")
        self.assertEqual(dt.datetime.fromtimestamp(start, dt.timezone.utc), dt.datetime(2026, 11, 6, 0, 0, tzinfo=dt.timezone.utc))
        self.assertEqual(dt.datetime.fromtimestamp(end_exclusive, dt.timezone.utc), dt.datetime(2026, 11, 25, 0, 0, tzinfo=dt.timezone.utc))

    def test_inclusive_report_horizon_days_reflects_declared_date_span(self):
        from build_selected50_research_runtime import inclusive_report_horizon_days
        self.assertEqual(inclusive_report_horizon_days("2026-11-06", "2026-11-24"), 19)
        self.assertEqual(inclusive_report_horizon_days("2026-11-24", "2026-11-24"), 1)
        with self.assertRaises(ValueError):
            inclusive_report_horizon_days("2026-11-25", "2026-11-24")

    def test_started_window_excludes_less_than_fifteen_minutes_lead(self):
        os.environ["ORACLE_REPORT_START_DATE"] = "2026-11-04"
        os.environ["ORACLE_REPORT_END_DATE"] = "2026-11-24"
        now = dt.datetime(2026, 11, 4, 6, 0, tzinfo=dt.timezone.utc).timestamp()
        start, end_exclusive, _, _ = resolve_report_window(now)
        self.assertEqual(start, now + 15 * 60)
        self.assertGreater(end_exclusive, start)

    def test_reversed_dates_fail_closed(self):
        os.environ["ORACLE_REPORT_START_DATE"] = "2026-11-25"
        os.environ["ORACLE_REPORT_END_DATE"] = "2026-11-24"
        with self.assertRaises(SystemExit):
            resolve_report_window()


if __name__ == "__main__":
    unittest.main()
