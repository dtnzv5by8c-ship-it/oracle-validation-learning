import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_footystats_no_home_away_coverage as audit


def row(league="League A", label="2024", sid="101", total=10, returned=10, flagged=2, pages=1):
    return {
        "provider_league_name": league,
        "provider_season_label": label,
        "provider_season_id": sid,
        "preflight_status": "ENDPOINT_PREFLIGHT_COMPLETE",
        "matches_total_results": str(total),
        "matches_page_count": str(pages),
        "page_1_match_rows_returned": str(returned),
        "page_1_no_home_away_rows": str(flagged),
    }


class FootyStatsNoHomeAwayCoverageTests(unittest.TestCase):
    def test_aggregates_season_and_league_flags_without_certifying_venue_data(self):
        rows = [
            row("League A", "2024", "101", 10, 10, 2),
            row("League A", "2025", "102", 10, 10, 10),
            row("League B", "2024", "201", 5, 5, 0),
        ]
        seasons, leagues, summary = audit.build_audit(rows, "a" * 64, "2026-11-04T00:00:00Z")
        self.assertEqual(len(seasons), 3)
        self.assertEqual(len(leagues), 2)
        self.assertEqual(summary["page_1_match_rows_returned"], 25)
        self.assertEqual(summary["page_1_no_home_away_rows"], 12)
        self.assertEqual(summary["seasons_with_any_no_home_away_rows"], 2)
        self.assertEqual(summary["leagues_with_any_no_home_away_rows"], 1)
        self.assertEqual(summary["seasons_with_all_page_1_rows_no_home_away"], 1)
        self.assertEqual(seasons[0]["flag_coverage_class"], "PARTIAL_PAGE_1_FLAG")
        self.assertFalse(seasons[0]["venue_split_eligible"])
        self.assertFalse(seasons[0]["root_cause_resolved"])
        self.assertEqual(leagues[0]["flag_burden_tier"], "HIGH_GE_50_PERCENT")
        self.assertFalse(summary["fixture_level_ids_available_in_source"])
        self.assertFalse(summary["production_eligible"])
        self.assertFalse(summary["betting_eligible"])

    def test_all_flagged_and_no_flagged_season_classes(self):
        seasons, leagues, summary = audit.build_audit([
            row("League A", "2024", "101", 4, 4, 4),
            row("League B", "2024", "201", 4, 4, 0),
        ], "b" * 64)
        by_id = {item["provider_season_id"]: item for item in seasons}
        self.assertEqual(by_id["101"]["flag_coverage_class"], "ALL_PAGE_1_ROWS_FLAGGED")
        self.assertEqual(by_id["201"]["flag_coverage_class"], "NO_FLAG_REPORTED_ON_PAGE_1")
        self.assertEqual(summary["seasons_with_all_page_1_rows_no_home_away"], 1)

    def test_multi_page_source_is_marked_page_one_only(self):
        seasons, _, summary = audit.build_audit([
            row("League A", "2024", "101", total=20, returned=10, flagged=1, pages=2),
        ], "c" * 64)
        self.assertFalse(summary["single_page_pagination_metadata_consistent_all_seasons"])
        self.assertEqual(seasons[0]["page_1_match_rows_returned"], 10)

    def test_duplicate_provider_season_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate provider season ID"):
            audit.build_audit([
                row("League A", "2024", "101"),
                row("League B", "2025", "101"),
            ], "d" * 64)

    def test_flag_count_cannot_exceed_returned_rows(self):
        with self.assertRaisesRegex(ValueError, "exceeds page-1 rows"):
            audit.build_audit([row(flagged=11)], "e" * 64)

    def test_incomplete_provider_identity_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "incomplete provider identity"):
            audit.build_audit([row(league="")], "f" * 64)

    def test_non_complete_preflight_is_rejected(self):
        bad = row()
        bad["preflight_status"] = "BLOCKED"
        with self.assertRaisesRegex(ValueError, "not endpoint-preflight complete"):
            audit.build_audit([bad], "a" * 64)

    def test_output_is_sanitized_and_research_only(self):
        seasons, leagues, summary = audit.build_audit(
            [row()], "a" * 64, "2026-11-04T00:00:00Z"
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            audit.write_outputs(root, seasons, leagues, summary)
            saved = json.loads((root / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["api_requests_made"], 0)
            self.assertFalse(saved["raw_provider_payloads_read"])
            self.assertFalse(saved["production_eligible"])
            self.assertFalse(saved["betting_eligible"])
            season_text = (root / "season-summary.csv").read_text(encoding="utf-8")
            self.assertNotIn("raw_payload", season_text)
            self.assertNotIn("homeGoalCount", season_text)
            self.assertTrue((root / "league-summary.csv").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
