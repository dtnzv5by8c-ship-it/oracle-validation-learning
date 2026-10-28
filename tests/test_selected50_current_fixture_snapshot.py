import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from scripts.validate_selected50_current_fixture_snapshot import validate


def epoch(value):
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())


class SnapshotValidatorTests(unittest.TestCase):
    def build(self):
        seasons = [
            {"selected_season_id": str(i), "http_status": 200,
             "provider_success": True, "schedule_status": "ONE_PAGE_RESPONSE"}
            for i in range(1, 51)
        ]
        future_kickoff = "2026-10-30T00:00:00+00:00"
        completed_kickoff = "2026-10-27T00:00:00+00:00"
        rows = [
            {"id": 1, "selected_season_id": "1", "competition_id": "1",
             "homeID": 10, "awayID": 11, "home_name": "Home", "away_name": "Away",
             "date_unix": epoch(future_kickoff), "kickoff_utc": future_kickoff,
             "status": "incomplete", "window_class": "FUTURE_14D", "no_home_away": 0,
             "homeGoalCount": 0, "awayGoalCount": 0, "totalGoalCount": 0},
            {"id": 2, "selected_season_id": "1", "competition_id": "1",
             "homeID": 10, "awayID": 11, "home_name": "Home", "away_name": "Away",
             "date_unix": epoch(completed_kickoff), "kickoff_utc": completed_kickoff,
             "status": "complete", "window_class": "RECENT_30D", "no_home_away": 0,
             "homeGoalCount": 1, "awayGoalCount": 0, "totalGoalCount": 1},
        ]
        return {
            "diagnostic": "BOUNDED_SELECTED50_CURRENT_FIXTURE_SNAPSHOT",
            "retrieved_utc": "2026-10-28T12:00:00+00:00",
            "window_start_utc": "2026-09-28T12:00:00+00:00",
            "window_end_utc": "2026-11-11T12:00:00+00:00",
            "selected_leagues": 50, "requests_planned": 50, "requests_attempted": 50,
            "http_200_success": 50, "request_failures": 0, "seasons_needing_pagination": [],
            "production_eligibility": "NOT_GRANTED", "betting_eligibility": "NOT_GRANTED",
            "raw_provider_payload_persisted": False, "api_key_persisted": False,
            "production_ledger_written": False, "per_season": seasons, "fixture_rows": rows,
            "future_14d_fixture_rows": 1, "recent_completed_30d_rows": 1,
        }

    def run_validation(self, data):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "snapshot.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return validate(path)

    def test_valid_snapshot_passes(self):
        self.assertEqual(self.run_validation(self.build())["status"], "PASS")

    def test_duplicate_match_id_fails(self):
        data = self.build()
        data["fixture_rows"][1]["id"] = data["fixture_rows"][0]["id"]
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_fixture_for_unrequested_season_fails(self):
        data = self.build()
        data["fixture_rows"][0]["selected_season_id"] = "999"
        data["fixture_rows"][0]["competition_id"] = "999"
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_empty_selected_season_id_fails(self):
        data = self.build()
        data["per_season"][0]["selected_season_id"] = ""
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_competition_id_must_match_selected_season_id(self):
        data = self.build()
        data["fixture_rows"][0]["competition_id"] = "999"
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_production_eligibility_must_remain_blocked(self):
        data = self.build()
        data["production_eligibility"] = "APPROVED"
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_retrieval_timestamp_is_required_and_timezone_aware(self):
        data = self.build()
        data.pop("retrieved_utc")
        self.assertEqual(self.run_validation(data)["status"], "FAIL")
        data = self.build()
        data["retrieved_utc"] = "2026-10-28T12:00:00"
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_snapshot_window_must_be_ordered_and_timezone_aware(self):
        data = self.build()
        data["window_start_utc"] = "2026-10-28T12:00:00"
        self.assertEqual(self.run_validation(data)["status"], "FAIL")
        data = self.build()
        data["window_start_utc"] = "2026-11-12T12:00:00+00:00"
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_naive_kickoff_fails_closed(self):
        data = self.build()
        data["fixture_rows"][0]["kickoff_utc"] = "2026-10-30T00:00:00"
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_invalid_kickoff_fails_closed(self):
        data = self.build()
        data["fixture_rows"][0]["kickoff_utc"] = "not-a-time"
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_date_unix_must_match_kickoff(self):
        data = self.build()
        data["fixture_rows"][0]["date_unix"] += 3600
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_kickoff_outside_declared_window_fails(self):
        data = self.build()
        data["fixture_rows"][0]["kickoff_utc"] = "2026-11-12T00:00:00+00:00"
        data["fixture_rows"][0]["date_unix"] = epoch(data["fixture_rows"][0]["kickoff_utc"])
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_window_class_must_match_kickoff(self):
        data = self.build()
        data["fixture_rows"][0]["window_class"] = "RECENT_30D"
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_fractional_boolean_nan_and_negative_scores_fail(self):
        for bad in (1.5, True, "NaN", "-1"):
            with self.subTest(bad=bad):
                data = self.build()
                data["fixture_rows"][0]["homeGoalCount"] = bad
                self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_completed_status_requires_two_valid_scores(self):
        data = self.build()
        data["fixture_rows"][1]["awayGoalCount"] = ""
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_completed_status_with_future_kickoff_fails(self):
        data = self.build()
        row = data["fixture_rows"][0]
        row["status"] = "complete"
        row["homeGoalCount"] = 1
        row["awayGoalCount"] = 0
        row["totalGoalCount"] = 1
        self.assertEqual(self.run_validation(data)["status"], "FAIL")

    def test_completed_zero_zero_score_is_valid(self):
        data = self.build()
        row = data["fixture_rows"][1]
        row["homeGoalCount"] = 0
        row["awayGoalCount"] = 0
        row["totalGoalCount"] = 0
        self.assertEqual(self.run_validation(data)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
