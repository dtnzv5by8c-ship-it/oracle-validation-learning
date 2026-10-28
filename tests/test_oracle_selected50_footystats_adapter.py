import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from oracle_selected50_footystats_adapter import adapt  # noqa: E402


def season_rows():
    return [
        {"selected_season_id": str(i), "http_status": 200, "provider_success": True}
        for i in range(1, 51)
    ]


def snapshot_with(row):
    return {"retrieved_utc": "2026-10-28T06:00:00+00:00", "per_season": season_rows(), "fixture_rows": [row]}


class AdapterTests(unittest.TestCase):
    def test_footystats_season_id_is_source_anchor_not_fotmob_id(self):
        row = {
            "selected_season_id": "1", "id": 123, "homeID": 11, "awayID": 22,
            "manifest_country": "Example", "manifest_competition": "League",
            "home_name": "Home FC", "away_name": "Away FC",
            "kickoff_utc": "2026-10-30T18:00:00+00:00", "status": "scheduled",
            "no_home_away": 0,
        }
        rows, manifest = adapt(snapshot_with(row), datetime(2026, 10, 28, 12, tzinfo=timezone.utc))
        self.assertEqual(rows[0]["research_league_key"], "FS_SEASON_1")
        self.assertEqual(rows[0]["source_match_id"], "123")
        self.assertNotIn("fotmob_match_id", rows[0])
        self.assertEqual(rows[0]["fixture_eligibility"], "RESEARCH_FIXTURE_CANDIDATE")
        self.assertEqual(manifest["fotmob_dependency"], "NONE")
        self.assertEqual(manifest["model_predictions_created"], 0)

    def test_no_home_away_is_quarantined(self):
        row = {
            "selected_season_id": "1", "id": 123, "homeID": 11, "awayID": 22,
            "home_name": "Home", "away_name": "Away", "kickoff_utc": "2026-10-30T18:00:00+00:00",
            "status": "scheduled", "no_home_away": 1,
        }
        rows, _ = adapt(snapshot_with(row), datetime(2026, 10, 28, 12, tzinfo=timezone.utc))
        self.assertEqual(rows[0]["fixture_eligibility"], "QUARANTINE_NO_HOME_AWAY")

    def test_suspended_fixture_is_quarantined(self):
        row = {
            "selected_season_id": "1", "id": 123, "homeID": 11, "awayID": 22,
            "home_name": "Home", "away_name": "Away", "kickoff_utc": "2026-10-30T18:00:00+00:00",
            "status": "suspended", "no_home_away": 0,
        }
        rows, _ = adapt(snapshot_with(row), datetime(2026, 10, 28, 12, tzinfo=timezone.utc))
        self.assertEqual(rows[0]["fixture_eligibility"], "QUARANTINE_SCHEDULE_STATUS")

    def test_missing_season_coverage_fails_closed(self):
        snap = snapshot_with({"selected_season_id": "1", "id": 1})
        snap["per_season"] = snap["per_season"][:-1]
        with self.assertRaises(ValueError):
            adapt(snap)

    def test_snapshot_retrieval_timestamp_is_required(self):
        snap = snapshot_with({
            "selected_season_id": "1", "id": 123, "homeID": 11, "awayID": 22,
            "home_name": "Home", "away_name": "Away",
            "kickoff_utc": "2026-10-30T18:00:00+00:00", "status": "incomplete",
        })
        snap.pop("retrieved_utc")
        with self.assertRaisesRegex(ValueError, "retrieved_utc is required"):
            adapt(snap, datetime(2026, 10, 28, 12, tzinfo=timezone.utc))

    def test_snapshot_retrieval_timestamp_must_be_timezone_aware(self):
        snap = snapshot_with({
            "selected_season_id": "1", "id": 123, "homeID": 11, "awayID": 22,
            "home_name": "Home", "away_name": "Away",
            "kickoff_utc": "2026-10-30T18:00:00+00:00", "status": "incomplete",
        })
        snap["retrieved_utc"] = "2026-10-28T06:00:00"
        with self.assertRaisesRegex(ValueError, "explicit timezone"):
            adapt(snap, datetime(2026, 10, 28, 12, tzinfo=timezone.utc))

    def test_future_snapshot_retrieval_timestamp_fails_closed(self):
        snap = snapshot_with({
            "selected_season_id": "1", "id": 123, "homeID": 11, "awayID": 22,
            "home_name": "Home", "away_name": "Away",
            "kickoff_utc": "2026-10-30T18:00:00+00:00", "status": "incomplete",
        })
        snap["retrieved_utc"] = "2026-10-28T13:00:00Z"
        with self.assertRaisesRegex(ValueError, "cannot be later"):
            adapt(snap, datetime(2026, 10, 28, 12, tzinfo=timezone.utc))

    def test_snapshot_hash_and_retrieval_time_are_exported(self):
        snap = snapshot_with({
            "selected_season_id": "1", "id": 123, "homeID": 11, "awayID": 22,
            "home_name": "Home", "away_name": "Away",
            "kickoff_utc": "2026-10-30T18:00:00+00:00", "status": "incomplete",
        })
        rows, manifest = adapt(snap, datetime(2026, 10, 28, 12, tzinfo=timezone.utc))
        digest = manifest["source_snapshot_sha256"]
        self.assertRegex(digest, r"^[0-9a-f]{64}$")
        self.assertEqual(manifest["source_snapshot_hash_method"], "canonical_json_sha256_sorted_keys_compact_v1")
        self.assertEqual(rows[0]["source_snapshot_sha256"], digest)
        self.assertEqual(rows[0]["source_snapshot_retrieved_utc"], "2026-10-28T06:00:00Z")
        self.assertEqual(manifest["source_snapshot_age_seconds_at_adaptation"], 21600)

    def test_duplicate_match_id_in_season_fails_closed(self):
        row = {"selected_season_id": "1", "id": 123, "homeID": 11, "awayID": 22,
               "home_name": "Home", "away_name": "Away", "kickoff_utc": "2026-10-30T18:00:00+00:00",
               "status": "scheduled"}
        snap = snapshot_with(row)
        snap["fixture_rows"].append(dict(row))
        with self.assertRaises(ValueError):
            adapt(snap)


if __name__ == "__main__":
    unittest.main()
