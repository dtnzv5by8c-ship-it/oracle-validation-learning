import csv
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_footystats_full_ingestion_manifest as manifest


def plan_rows():
    return [
        {"provider": "FootyStats", "provider_league_name": "League A", "provider_season_label": "2024", "provider_season_id": "101", "production_eligible": "False", "betting_eligible": "False", "history_end_date": "2026-11-04"},
        {"provider": "FootyStats", "provider_league_name": "League B", "provider_season_label": "2024/25", "provider_season_id": "202", "production_eligible": "False", "betting_eligible": "False", "history_end_date": "2026-11-04"},
    ]


def preflight_row(league="League A", label="2024", sid="101"):
    return {
        "provider_league_name": league,
        "provider_season_label": label,
        "provider_season_id": sid,
        "season_status": "ENDPOINT_PREFLIGHT_COMPLETE",
        "league_matches": {
            "total_results": 1200, "per_page": 600, "expected_page_count": 2,
            "fetched_pages": 1, "all_pages_retrieved": False, "page_complete": True,
            "returned_rows": 600, "unique_match_ids_on_page": 600,
            "match_identity_fields": {"id": 600, "homeID": 600, "awayID": 600, "date_unix": 600, "status": 600},
            "completed_match_rows": 580, "completed_rows_missing_any_goal_field": 0,
            "completed_goal_field_presence": {"homeGoalCount": 580, "awayGoalCount": 580, "totalGoalCount": 580},
            "no_home_away_rows": 10, "page_1_rows_in_window": 400, "page_1_rows_outside_window": 200,
        },
        "league_teams": {
            "total_results": 18, "per_page": 50, "expected_page_count": 1,
            "fetched_pages": 1, "all_pages_retrieved": True, "page_complete": True,
            "returned_rows": 18, "unique_team_ids_on_page": 18,
            "team_identity_fields": {"id": 18, "name_or_alias": 18},
            "team_stats_field_names": ["xg_for_avg_home", "xg_for_avg_away", "xg_against_avg_home", "xg_against_avg_away"],
        },
        "league_tables": {"response_status": "SUCCESS_SHAPE_VERIFIED"},
        "league_season": {"response_status": "SUCCESS_SHAPE_VERIFIED", "data_field_names": ["total_goals", "home_teams_goals", "away_teams_goals", "xg_avg"]},
        "table_field_presence": {"all_matches_table_away": True, "all_matches_table_home": True, "all_matches_table_overall": True, "league_table": True, "specific_tables": True},
        "match_detail": {"h2h_field_present": True, "h2h_temporal_status": "PRESENT_NOT_CHRONOLOGY_VALIDATED", "xg_field_presence": {"team_a_xg_prematch": True, "team_b_xg_prematch": True, "total_xg_prematch": True}},
        "h2h_temporal_status": "PRESENT_NOT_CHRONOLOGY_VALIDATED",
        "recent_form_status": "NOT_ASSESSED_FULL_MATCH_PAGINATION_REQUIRED",
        "home_away_form_status": "NOT_ASSESSED_FULL_MATCH_PAGINATION_REQUIRED",
        "standings_temporal_status": "CURRENT_AS_OF_PREFLIGHT_ONLY_NOT_FIXTURE_TIME",
        "xg_usage_status": "QUARANTINED_NO_FIXTURE_LEVEL_CAPTURE_AND_REVISION_PROVENANCE",
        "league_matches_response": {"endpoint": "league-matches", "http_status": 200},
        "league_teams_response": {"endpoint": "league-teams", "http_status": 200, "fetched_at_utc": "2026-11-04T15:00:00Z"},
        "league_tables_response": {"endpoint": "league-tables", "http_status": 200, "fetched_at_utc": "2026-11-04T15:00:01Z"},
        "league_season_response": {"endpoint": "league-season", "http_status": 200, "fetched_at_utc": "2026-11-04T15:00:02Z"},
    }


class FootyStatsFullIngestionManifestTests(unittest.TestCase):
    def test_builds_exact_paginated_requests_and_hourly_batches(self):
        tasks, coverage, batches, summary = manifest.build_manifest(plan_rows(), {"101": preflight_row()}, 3)
        self.assertEqual(len(coverage), 2)
        self.assertEqual(coverage[0]["provider_season_id"], "101")
        self.assertEqual(coverage[0]["planned_ingestion_requests"], 5)
        self.assertEqual(coverage[0]["ingestion_plan_status"], "PLANNED_REQUIRES_PRIVATE_RAW_ARCHIVE")
        self.assertEqual(coverage[1]["ingestion_plan_status"], "BLOCKED_NO_COMPLETE_PREFLIGHT")
        self.assertEqual(len(tasks), 5)
        self.assertEqual(sum(1 for row in tasks if row["endpoint"] == "league-matches"), 2)
        self.assertTrue(all(row["max_per_page"] == 600 for row in tasks if row["endpoint"] == "league-matches"))
        self.assertEqual(sum(1 for row in tasks if row["endpoint"] == "league-teams"), 1)
        self.assertEqual([row["max_per_page"] for row in tasks if row["endpoint"] == "league-teams"], [50])
        self.assertEqual(sum(1 for row in tasks if row["endpoint"] == "league-tables"), 1)
        self.assertEqual(sum(1 for row in tasks if row["endpoint"] == "league-season"), 1)
        self.assertEqual([batch["task_count"] for batch in batches], [3, 2])
        self.assertTrue(all(row["task_id"].startswith("FS:101:") for row in tasks))
        self.assertTrue(all(row["raw_storage_required"] for row in tasks))
        self.assertTrue(all(row["production_eligible"] is False for row in tasks))
        self.assertTrue(all(row["betting_eligible"] is False for row in tasks))
        self.assertEqual(coverage[0]["page_1_match_rows_returned"], 600)
        self.assertEqual(coverage[0]["page_1_match_rows_in_history_window"], 400)
        self.assertEqual(coverage[0]["page_1_match_rows_outside_history_window"], 200)
        self.assertEqual(coverage[0]["page_1_completed_match_goal_field_gaps"], 0)
        self.assertEqual(coverage[0]["page_1_no_home_away_rows"], 10)
        self.assertTrue(coverage[0]["match_ids_unique"])
        self.assertTrue(coverage[0]["team_ids_unique"])
        self.assertTrue(coverage[0]["table_required_fields_complete"])
        self.assertTrue(coverage[0]["season_goal_fields_complete"])
        self.assertTrue(coverage[0]["team_xg_aggregate_fields_complete"])
        self.assertTrue(coverage[0]["h2h_field_present"])
        self.assertEqual(coverage[0]["h2h_temporal_status"], "PRESENT_NOT_CHRONOLOGY_VALIDATED")
        self.assertEqual(coverage[0]["xg_usage_status"], "QUARANTINED_NO_FIXTURE_LEVEL_CAPTURE_AND_REVISION_PROVENANCE")
        self.assertEqual(summary["planned_request_count"], 5)
        self.assertEqual(summary["page_1_match_rows_returned"], 600)
        self.assertEqual(summary["page_1_match_rows_in_history_window"], 400)
        self.assertEqual(summary["page_1_match_rows_outside_history_window"], 200)
        self.assertEqual(summary["page_1_no_home_away_rows"], 10)
        self.assertEqual(summary["seasons_with_any_no_home_away_rows"], 1)
        self.assertEqual(summary["seasons_with_h2h_temporal_order_unverified"], 1)
        self.assertEqual(summary["seasons_with_fixture_level_xg_quarantined"], 1)
        self.assertEqual(summary["api_requests_made"], 0)
        self.assertFalse(summary["raw_payloads_written"])

    def test_exact_season_identity_mismatch_is_blocked_not_fuzzy_joined(self):
        wrong = preflight_row(league="Different League")
        tasks, coverage, batches, summary = manifest.build_manifest(plan_rows(), {"101": wrong}, 1500)
        self.assertEqual(tasks, [])
        self.assertEqual(coverage[0]["ingestion_plan_status"], "BLOCKED_EXACT_SEASON_IDENTITY_MISMATCH")
        self.assertEqual(coverage[1]["ingestion_plan_status"], "BLOCKED_NO_COMPLETE_PREFLIGHT")

    def test_inconsistent_pagination_metadata_blocks_season(self):
        broken = preflight_row()
        broken["league_matches"]["expected_page_count"] = 3
        tasks, coverage, batches, summary = manifest.build_manifest(plan_rows(), {"101": broken}, 1500)
        self.assertEqual(tasks, [])
        self.assertEqual(coverage[0]["ingestion_plan_status"], "BLOCKED_INCOMPLETE_PREFLIGHT_EVIDENCE")

    def test_short_preflight_page_is_blocked_even_when_page_complete_flag_is_true(self):
        broken = preflight_row()
        broken["league_matches"]["returned_rows"] = 599
        broken["league_matches"]["match_identity_fields"] = {
            key: 599 for key in ("id", "homeID", "awayID", "date_unix", "status")
        }
        broken["league_matches"]["unique_match_ids_on_page"] = 599
        tasks, coverage, batches, summary = manifest.build_manifest(
            plan_rows(), {"101": broken}, 1500
        )
        self.assertEqual(tasks, [])
        self.assertEqual(coverage[0]["ingestion_plan_status"], "BLOCKED_INCOMPLETE_PREFLIGHT_EVIDENCE")

    def test_single_page_must_be_marked_all_pages_retrieved(self):
        broken = preflight_row()
        broken["league_matches"]["expected_page_count"] = 1
        broken["league_matches"]["total_results"] = 600
        broken["league_matches"]["all_pages_retrieved"] = False
        tasks, coverage, batches, summary = manifest.build_manifest(
            plan_rows(), {"101": broken}, 1500
        )
        self.assertEqual(tasks, [])
        self.assertEqual(coverage[0]["ingestion_plan_status"], "BLOCKED_INCOMPLETE_PREFLIGHT_EVIDENCE")

    def test_duplicate_match_ids_block_season(self):
        broken = preflight_row()
        broken["league_matches"]["unique_match_ids_on_page"] = 599
        tasks, coverage, batches, summary = manifest.build_manifest(plan_rows(), {"101": broken}, 1500)
        self.assertEqual(tasks, [])
        self.assertEqual(coverage[0]["ingestion_plan_status"], "BLOCKED_INCOMPLETE_PREFLIGHT_EVIDENCE")

    def test_required_goal_field_gap_is_explicitly_quarantined(self):
        broken = preflight_row()
        broken["league_matches"]["completed_rows_missing_any_goal_field"] = 1
        broken["league_matches"]["completed_goal_field_presence"]["awayGoalCount"] = 579
        tasks, coverage, batches, summary = manifest.build_manifest(plan_rows(), {"101": broken}, 1500)
        self.assertEqual(len(tasks), 5)
        self.assertEqual(coverage[0]["ingestion_plan_status"], "PLANNED_WITH_REQUIRED_FIELD_GAPS_QUARANTINED")
        self.assertIn("COMPLETED_MATCH_GOAL_FIELDS", coverage[0]["required_field_gap_reasons"])
        self.assertEqual(summary["seasons_with_required_field_gaps"], 1)

    def test_maximum_batch_cannot_exceed_operational_limit(self):
        with self.assertRaisesRegex(ValueError, "1..1500"):
            manifest.build_manifest(plan_rows(), {}, 1800)

    def test_h2h_is_derived_without_per_fixture_detail_calls(self):
        tasks, coverage, batches, summary = manifest.build_manifest(plan_rows(), {"101": preflight_row()}, 1500)
        self.assertFalse(any(row["endpoint"] == "match" for row in tasks))
        self.assertIn("DERIVE_FROM_COMPLETE", summary["h2h_strategy"])
        self.assertEqual(summary["fixture_time_standings_status"], "NOT_VERIFIED_REQUIRES_AS_OF_RECONSTRUCTION_OR_SEPARATE_VALIDATION")
        self.assertTrue(summary["xg_status"].startswith("QUARANTINED"))

    def test_read_plan_rejects_production_eligible_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.csv"
            rows = plan_rows()
            rows[0]["production_eligible"] = "True"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "production-ineligible"):
                manifest.read_plan(path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
