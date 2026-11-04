import csv
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_footystats_full_ingestion_manifest as manifest


def plan_rows():
    return [
        {
            "provider": "FootyStats",
            "provider_league_name": "League A",
            "provider_season_label": "2024",
            "provider_season_id": "101",
            "production_eligible": "False",
            "betting_eligible": "False",
            "history_end_date": "2026-11-04",
        },
        {
            "provider": "FootyStats",
            "provider_league_name": "League B",
            "provider_season_label": "2024/25",
            "provider_season_id": "202",
            "production_eligible": "False",
            "betting_eligible": "False",
            "history_end_date": "2026-11-04",
        },
    ]


def preflight_row(league="League A", label="2024", sid="101"):
    return {
        "provider_league_name": league,
        "provider_season_label": label,
        "provider_season_id": sid,
        "season_status": "ENDPOINT_PREFLIGHT_COMPLETE",
        "league_matches": {
            "total_results": 1500, "per_page": 1000, "expected_page_count": 2,
            "fetched_pages": 1, "all_pages_retrieved": False,
        },
        "league_teams": {
            "total_results": 18, "per_page": 50, "expected_page_count": 1,
            "fetched_pages": 1, "all_pages_retrieved": True,
        },
        "league_tables": {"response_status": "SUCCESS_SHAPE_VERIFIED"},
        "league_season": {"response_status": "SUCCESS_SHAPE_VERIFIED"},
        "league_matches_response": {"endpoint": "league-matches", "http_status": 200},
        "league_teams_response": {"endpoint": "league-teams", "http_status": 200, "fetched_at_utc": "2026-11-04T15:00:00Z"},
        "league_tables_response": {"endpoint": "league-tables", "http_status": 200, "fetched_at_utc": "2026-11-04T15:00:01Z"},
        "league_season_response": {"endpoint": "league-season", "http_status": 200, "fetched_at_utc": "2026-11-04T15:00:02Z"},
    }


class FootyStatsFullIngestionManifestTests(unittest.TestCase):
    def test_builds_exact_paginated_requests_and_hourly_batches(self):
        tasks, coverage, batches, summary = manifest.build_manifest(
            plan_rows(), {"101": preflight_row()}, 3
        )
        self.assertEqual(len(coverage), 2)
        self.assertEqual(coverage[0]["provider_season_id"], "101")
        self.assertEqual(coverage[0]["planned_ingestion_requests"], 5)
        self.assertEqual(coverage[0]["ingestion_plan_status"], "PLANNED_REQUIRES_PRIVATE_RAW_ARCHIVE")
        self.assertEqual(coverage[1]["ingestion_plan_status"], "BLOCKED_NO_COMPLETE_PREFLIGHT")
        self.assertEqual(len(tasks), 5)
        self.assertEqual(sum(1 for row in tasks if row["endpoint"] == "league-matches"), 2)
        self.assertEqual(sum(1 for row in tasks if row["endpoint"] == "league-teams"), 1)
        self.assertEqual(sum(1 for row in tasks if row["endpoint"] == "league-tables"), 1)
        self.assertEqual(sum(1 for row in tasks if row["endpoint"] == "league-season"), 1)
        self.assertEqual([batch["task_count"] for batch in batches], [3, 2])
        self.assertTrue(all(row["task_id"].startswith("FS:101:") for row in tasks))
        self.assertTrue(all(row["raw_storage_required"] for row in tasks))
        self.assertTrue(all(row["production_eligible"] is False for row in tasks))
        self.assertTrue(all(row["betting_eligible"] is False for row in tasks))
        self.assertEqual(summary["h2h_strategy"], "DERIVE_FROM_COMPLETE_EXACT_CHRONOLOGICAL_MATCH_SPINE_NO_PER_FIXTURE_DETAIL_CALLS")
        self.assertEqual(summary["planned_request_count"], 5)
        self.assertEqual(summary["api_requests_made"], 0)
        self.assertFalse(summary["raw_payloads_written"])

    def test_exact_season_identity_mismatch_is_blocked_not_fuzzy_joined(self):
        wrong = preflight_row(league="Different League")
        tasks, coverage, batches, summary = manifest.build_manifest(
            plan_rows(), {"101": wrong}, 1500
        )
        self.assertEqual(tasks, [])
        self.assertEqual(coverage[0]["ingestion_plan_status"], "BLOCKED_EXACT_SEASON_IDENTITY_MISMATCH")
        self.assertEqual(coverage[1]["ingestion_plan_status"], "BLOCKED_NO_COMPLETE_PREFLIGHT")

    def test_inconsistent_pagination_metadata_blocks_season(self):
        broken = preflight_row()
        broken["league_matches"]["expected_page_count"] = 3
        tasks, coverage, batches, summary = manifest.build_manifest(
            plan_rows(), {"101": broken}, 1500
        )
        self.assertEqual(tasks, [])
        self.assertEqual(coverage[0]["ingestion_plan_status"], "BLOCKED_INCOMPLETE_PREFLIGHT_EVIDENCE")

    def test_maximum_batch_cannot_exceed_operational_limit(self):
        with self.assertRaisesRegex(ValueError, "1..1500"):
            manifest.build_manifest(plan_rows(), {}, 1800)

    def test_h2h_is_derived_without_per_fixture_detail_calls(self):
        tasks, coverage, batches, summary = manifest.build_manifest(
            plan_rows(), {"101": preflight_row()}, 1500
        )
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
