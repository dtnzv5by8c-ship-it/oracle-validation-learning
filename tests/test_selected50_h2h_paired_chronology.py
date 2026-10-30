import json
import tempfile
import unittest
from pathlib import Path

from scripts.audit_selected50_h2h_paired_chronology import (
    audit_h2h_paired_predictions,
    write_h2h_paired_chronology_qa,
)


class Selected50H2HPairedChronologyTests(unittest.TestCase):
    def row(self, market="BTTS", **overrides):
        row = {
            "fixture_id": "F1",
            "date_utc": "2025-03-22T18:30:00+00:00",
            "h2h_last_date_utc": "2024-09-01T18:30:00+00:00",
            "competition_id": "C1",
            "league": "League A",
            "home_team": "Home",
            "away_team": "Away",
            "market": market,
            "actual": "1",
            "baseline_probability": "0.54",
            "h2h_candidate_probability": "0.56",
            "h2h_prior_n": "3",
            "h2h_btts_rate_last5": "0.6666667",
            "h2h_avg_total_goals_last5": "2.3333333",
            "h2h_days_since_last": str((__import__("datetime").datetime.fromisoformat("2025-03-22T18:30:00+00:00") - __import__("datetime").datetime.fromisoformat("2024-09-01T18:30:00+00:00")).total_seconds() / 86400),
        }
        row.update(overrides)
        return row

    def test_valid_paired_rows_pass_with_complete_market_coverage(self):
        rows = [self.row("BTTS"), self.row("DC_HOME")]
        qa = audit_h2h_paired_predictions(rows, {"BTTS", "DC_HOME"})
        self.assertEqual(qa["status"], "PASS_H2H_PAIRED_OUTPUT_CHRONOLOGY")
        self.assertEqual(qa["row_count"], 2)
        self.assertEqual(qa["unique_fixture_count"], 1)

    def test_same_kickoff_and_future_h2h_dates_are_rejected(self):
        rows = [
            self.row("BTTS", h2h_last_date_utc="2025-03-22T18:30:00+00:00", h2h_days_since_last="0"),
            self.row("DC_HOME", h2h_last_date_utc="2025-03-23T18:30:00+00:00", h2h_days_since_last="-1"),
        ]
        qa = audit_h2h_paired_predictions(rows, {"BTTS", "DC_HOME"})
        self.assertEqual(qa["non_strict_prior_rows"], 2)
        self.assertEqual(qa["status"], "BLOCKED_H2H_PAIRED_OUTPUT_INTEGRITY")

    def test_timezone_naive_utc_fields_are_rejected(self):
        rows = [
            self.row("BTTS", date_utc="2025-03-22T18:30:00"),
            self.row("DC_HOME", h2h_last_date_utc="2024-09-01T18:30:00"),
        ]
        qa = audit_h2h_paired_predictions(rows, {"BTTS", "DC_HOME"})
        self.assertEqual(qa["invalid_kickoff_rows"], 1)
        self.assertEqual(qa["invalid_h2h_date_rows"], 1)
        self.assertEqual(qa["status"], "BLOCKED_H2H_PAIRED_OUTPUT_INTEGRITY")

    def test_elapsed_days_must_match_published_prior_date(self):
        qa = audit_h2h_paired_predictions(
            [self.row("BTTS", h2h_days_since_last="1")],
            {"BTTS"},
        )
        self.assertEqual(qa["days_since_last_mismatch_rows"], 1)
        self.assertEqual(qa["status"], "BLOCKED_H2H_PAIRED_OUTPUT_INTEGRITY")

    def test_duplicate_fixture_market_and_incomplete_market_set_are_rejected(self):
        rows = [self.row("BTTS"), self.row("BTTS")]
        qa = audit_h2h_paired_predictions(rows, {"BTTS", "DC_HOME"})
        self.assertEqual(qa["duplicate_fixture_market_rows"], 1)
        self.assertEqual(qa["incomplete_fixture_market_sets"], 1)

    def test_invalid_probability_and_h2h_feature_values_are_rejected(self):
        row = self.row("BTTS", h2h_btts_rate_last5="1.2", baseline_probability="nan")
        qa = audit_h2h_paired_predictions([row], {"BTTS"})
        self.assertEqual(qa["invalid_h2h_rate_rows"], 1)
        self.assertEqual(qa["invalid_probability_rows"], 1)

    def test_empty_output_is_blocked_not_reported_as_pass(self):
        qa = audit_h2h_paired_predictions([], {"BTTS"})
        self.assertEqual(qa["status"], "BLOCKED_NO_PAIRED_ROWS")

    def test_chronology_qa_writer_emits_one_parseable_json_document(self):
        qa = audit_h2h_paired_predictions(
            [self.row("BTTS"), self.row("DC_HOME")],
            {"BTTS", "DC_HOME"},
        )
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "nested" / "chronology.json"
            write_h2h_paired_chronology_qa(target, qa)
            raw = target.read_text(encoding="utf-8")
            self.assertTrue(raw.endswith("\n"))
            self.assertEqual(json.loads(raw), qa)


if __name__ == "__main__":
    unittest.main()
