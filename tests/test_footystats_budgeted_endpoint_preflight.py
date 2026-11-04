import csv
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import footystats_budgeted_endpoint_preflight as preflight
from footystats_request_budget import empty_ledger, reserve_block, utc_text


def write_plan(path: Path, rows=None):
    rows = rows or [{
        "provider": "FootyStats",
        "provider_country": "Testland",
        "provider_league_name": "Test League",
        "provider_season_label": "2024",
        "provider_season_id": "12345",
        "provider_competition_id": "",
        "catalogue_scope": "chosen_leagues_only",
        "catalogue_retrieved_utc": "2026-11-04T14:34:00Z",
        "season_start_year": "2024",
        "season_end_year": "2024",
        "history_start_date": "2024-01-01",
        "history_end_date": "2026-11-04",
        "fixture_filter_start_utc": "2024-01-01T00:00:00Z",
        "fixture_filter_end_utc_inclusive": "2026-11-04T23:59:59.999999Z",
        "fixture_kickoff_filter_required": "True",
        "plan_status": "PLANNED_NOT_RETRIEVED",
        "production_eligible": "False",
        "betting_eligible": "False",
    }]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def payloads():
    kickoff = int(datetime(2026, 1, 1, tzinfo=timezone.utc).timestamp())
    return [
        {
            "success": True,
            "pager": {"current_page": 1, "max_page": 1, "results_per_page": 1000, "total_results": 1},
            "data": [{
                "id": 100, "homeID": 10, "awayID": 20, "date_unix": kickoff,
                "status": "complete", "homeGoalCount": 1, "awayGoalCount": 0, "totalGoalCount": 1,
                "homeTeam": "HOME_TEST_PRIVATE_NAME", "awayTeam": "AWAY_TEST_PRIVATE_NAME",
            }],
            "request_limit": 1800,
            "request_remaining": 1799,
        },
        {
            "success": True,
            "pager": {"page": 1, "per_page": 50, "total_results": 2},
            "data": [
                {"id": 10, "name": "HOME_TEST_PRIVATE_NAME", "stats": {"xg_for_avg_overall": 1.2}},
                {"id": 20, "full_name": "AWAY_TEST_PRIVATE_NAME", "stats": [{"name": "xg_against_avg_overall", "value": 0.9}]},
            ],
            "request_limit": 1800,
            "request_remaining": 1798,
        },
        {
            "success": True,
            "data": {
                "league_table": [{"position": 1}],
                "all_matches_table_overall": [],
                "all_matches_table_home": [],
                "all_matches_table_away": [],
                "specific_tables": [],
            },
            "request_limit": 1800,
            "request_remaining": 1797,
        },
        {
            "success": True,
            "data": [{"id": 12345, "name": "Test League", "season": "2024", "totalMatches": 1}],
            "request_limit": 1800,
            "request_remaining": 1796,
        },
        {
            "success": True,
            "data": {
                "id": 100, "homeID": 10, "awayID": 20,
                "h2h": {"matches": []},
                "team_a_xg_prematch": 1.1,
                "team_b_xg_prematch": 0.9,
                "total_xg_prematch": 2.0,
            },
            "request_limit": 1800,
            "request_remaining": 1795,
        },
    ]


class FootyStatsBudgetedEndpointPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.ledger = self.root / "rolling-request-ledger.json"
        self.plan = self.root / "season-plan.csv"
        self.report = self.root / "endpoint-preflight" / "footystats-preflight-run-test.json"
        write_plan(self.plan)
        ledger, count = reserve_block(
            empty_ledger(), datetime.now(timezone.utc), 10, "run-test",
        )
        self.assertEqual(count, 10)
        self.ledger.write_text(json.dumps(ledger), encoding="utf-8")
        self.args = SimpleNamespace(
            ledger=str(self.ledger),
            reservation_id="run-test",
            plan=str(self.plan),
            report=str(self.report),
            run_id="test",
            max_seasons=182,
            max_requests=10,
            history_end_date="2026-11-04",
            api_key_env="FOOTYSTATS_API_KEY",
            base_url="https://api.football-data-api.com",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def make_fetch(self, values):
        cursor = {"i": 0}

        def fake(endpoint, params, api_key, attempts, base_url):
            index = cursor["i"]
            cursor["i"] += 1
            timestamp = utc_text(datetime.now(timezone.utc))
            attempts.append(timestamp)
            payload = values[index]
            meta = {
                "endpoint": endpoint,
                "http_status": 200,
                "fetched_at_utc": timestamp,
                "payload_sha256": "a" * 64,
                "provider_request_limit_observed": payload.get("request_limit"),
                "provider_request_remaining_observed": payload.get("request_remaining"),
                "request_remaining_interpretation": "REQUEST_WINDOW_OBSERVATION_ONLY_NOT_MONTHLY_CREDIT_EVIDENCE",
            }
            return payload, meta

        return fake

    def test_provider_request_limit_never_reduces_required_300_headroom(self):
        with self.assertRaises(preflight.PreflightError) as low:
            preflight.check_provider_limit(
                {"provider_request_limit_observed": 250}, self.ledger
            )
        self.assertEqual(low.exception.code, "PROVIDER_REQUEST_LIMIT_CANNOT_PRESERVE_300_HEADROOM")
        with self.assertRaises(preflight.PreflightError) as insufficient:
            preflight.check_provider_limit(
                {"provider_request_limit_observed": 309}, self.ledger
            )
        self.assertEqual(insufficient.exception.code, "PROVIDER_REQUEST_LIMIT_BELOW_ACTIVE_RESERVATION")
        preflight.check_provider_limit(
            {"provider_request_limit_observed": 310}, self.ledger
        )

    @patch.dict(os.environ, {"FOOTYSTATS_API_KEY": "test-key"})
    def test_successful_preflight_is_sanitized_and_counts_all_requests(self):
        values = payloads()
        with patch.object(preflight, "fetch_json", side_effect=self.make_fetch(values)):
            report, code = preflight.execute(self.args)
        self.assertEqual(code, 0)
        self.assertEqual(report["run_status"], "ENDPOINT_PREFLIGHT_BATCH_COMPLETE")
        self.assertEqual(report["request_budget"]["requests_attempted_this_run"], 5)
        self.assertEqual(report["seasons_completed_this_run"], 1)
        self.assertFalse(report["raw_payloads_persisted"])
        self.assertFalse(report["production_eligible"])
        self.assertFalse(report["betting_eligible"])
        self.assertEqual(report["season_results"][0]["season_status"], "ENDPOINT_PREFLIGHT_COMPLETE")
        self.assertEqual(report["season_results"][0]["league_matches"]["page_1_rows_in_window"], 1)
        self.assertTrue(report["season_results"][0]["match_detail"]["h2h_field_present"])
        self.assertIn("xg_against_avg_overall", report["season_results"][0]["league_teams"]["team_stats_field_names"])
        self.assertEqual(report["season_results"][0]["league_teams"]["team_identity_fields"]["name_or_alias"], 2)
        self.assertEqual(
            report["season_results"][0]["xg_usage_status"],
            "QUARANTINED_NO_FIXTURE_LEVEL_CAPTURE_AND_REVISION_PROVENANCE",
        )
        report_text = self.report.read_text(encoding="utf-8")
        self.assertNotIn("HOME_TEST_PRIVATE_NAME", report_text)
        self.assertNotIn("AWAY_TEST_PRIVATE_NAME", report_text)
        ledger = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertEqual(len(ledger["actual_requests"]), 5)
        self.assertEqual(ledger["reservations"], [])

    @patch.dict(os.environ, {"FOOTYSTATS_API_KEY": "test-key"})
    def test_lower_provider_request_limit_binds_and_stops_after_first_call(self):
        values = payloads()
        values[0]["request_limit"] = 300
        with patch.object(preflight, "fetch_json", side_effect=self.make_fetch(values)):
            report, code = preflight.execute(self.args)
        self.assertEqual(code, 1)
        self.assertEqual(report["run_status"], "STOPPED_FAIL_CLOSED")
        self.assertEqual(report["failure_code"], "PROVIDER_REQUEST_LIMIT_CANNOT_PRESERVE_300_HEADROOM")
        self.assertEqual(report["request_budget"]["requests_attempted_this_run"], 1)
        self.assertEqual(report["request_budget"]["provider_request_limit_observed"], 300)
        self.assertEqual(len(json.loads(self.ledger.read_text(encoding="utf-8"))["actual_requests"]), 1)

    @patch.dict(os.environ, {"FOOTYSTATS_API_KEY": "test-key"})
    def test_http_429_is_counted_once_and_stops_without_retry(self):
        def fail_once(endpoint, params, api_key, attempts, base_url):
            attempts.append(utc_text(datetime.now(timezone.utc)))
            raise preflight.PreflightError("HTTP_429", attempts[-1])

        with patch.object(preflight, "fetch_json", side_effect=fail_once):
            report, code = preflight.execute(self.args)
        self.assertEqual(code, 1)
        self.assertEqual(report["failure_code"], "HTTP_429")
        self.assertEqual(report["request_budget"]["requests_attempted_this_run"], 1)
        self.assertEqual(len(json.loads(self.ledger.read_text(encoding="utf-8"))["actual_requests"]), 1)

    def test_missing_api_key_releases_reservation_without_a_request(self):
        with patch.dict(os.environ, {}, clear=True):
            report, code = preflight.execute(self.args)
        self.assertEqual(code, 1)
        self.assertEqual(report["failure_code"], "FOOTYSTATS_API_KEY_SECRET_MISSING")
        ledger = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertEqual(ledger["actual_requests"], [])
        self.assertEqual(ledger["reservations"], [])

    def test_match_detail_requires_exact_ordered_provider_ids(self):
        data = {
            "success": True,
            "data": {"id": 100, "homeID": 20, "awayID": 10, "h2h": {}},
        }
        expected = {"id": 100, "homeID": 10, "awayID": 20}
        with self.assertRaisesRegex(preflight.PreflightError, "MATCH_DETAIL_ORDERED_IDENTITY_MISMATCH"):
            preflight.match_detail_summary(data, expected)

    def test_round_robin_selection_covers_distinct_leagues_first(self):
        rows = []
        for league in ("League A", "League B"):
            for season, sid in (("2024", f"{league}-1"), ("2025", f"{league}-2")):
                rows.append({
                    "provider_league_name": league,
                    "provider_season_label": season,
                    "provider_season_id": sid,
                    "season_start_year": season,
                    "season_end_year": season,
                })
        selected = preflight.round_robin_pending(rows, set(), 2)
        self.assertEqual({row["provider_league_name"] for row in selected}, {"League A", "League B"})

    def test_history_window_filter_keeps_out_of_window_rows_visible(self):
        rows = [
            {"date_unix": int(datetime(2023, 12, 31, tzinfo=timezone.utc).timestamp())},
            {"date_unix": int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp())},
        ]
        summary = {}
        preflight.add_history_window_summary(summary, rows, {
            "fixture_filter_start_utc": "2024-01-01T00:00:00Z",
            "fixture_filter_end_utc_inclusive": "2026-11-04T23:59:59.999999Z",
        })
        self.assertEqual(summary["page_1_rows_in_window"], 1)
        self.assertEqual(summary["page_1_rows_outside_window"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
