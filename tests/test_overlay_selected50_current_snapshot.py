import csv
import hashlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout

from scripts.overlay_selected50_current_snapshot import (
    TRACE_COLUMNS, find_archive_path, main, no_home_away_flag, future_status_quarantine_reason, parse_utc, valid_id,
)


def iso(value):
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class SnapshotOverlayContractTests(unittest.TestCase):
    def test_requires_explicit_timezone(self):
        self.assertIsNone(parse_utc("2026-10-28T16:00:00"))
        self.assertIsNotNone(parse_utc("2026-10-28T16:00:00Z"))

    def test_resolves_nested_archive_paths_by_suffix(self):
        names = ["private/archive/seasons/17326/matches.json", "private/archive/seasons/17326/teams.json"]
        self.assertEqual(find_archive_path(names, "17326", "matches"), names[0])
        self.assertEqual(find_archive_path(names, "17326", "teams"), names[1])
        self.assertIsNone(find_archive_path(names, "99999", "matches"))

    def test_rejects_ambiguous_archive_paths(self):
        names = ["a/seasons/17326/matches.json", "b/seasons/17326/matches.json"]
        with self.assertRaises(SystemExit):
            find_archive_path(names, "17326", "matches")

    def test_rejects_blank_zero_boolean_and_invalid_numeric_ids(self):
        for value in ("", None, 0, 0.0, "0", "0.0", "null", "none", True, False, float("nan"), float("inf"), -2, "2.5"):
            self.assertFalse(valid_id(value), repr(value))
        self.assertTrue(valid_id("8551579"))
        self.assertTrue(valid_id("provider-fixture-A"))

    def test_no_home_away_flag_is_tristate_and_unknown_is_not_admitted(self):
        self.assertIs(no_home_away_flag(1), True)
        self.assertIs(no_home_away_flag("true"), True)
        self.assertIs(no_home_away_flag(0), False)
        self.assertIs(no_home_away_flag("false"), False)
        self.assertIsNone(no_home_away_flag(None))
        self.assertIsNone(no_home_away_flag("unknown"))

    def test_future_status_gate_is_fail_closed_to_documented_enum(self):
        self.assertIsNone(future_status_quarantine_reason("incomplete"))
        self.assertEqual(future_status_quarantine_reason("complete"), "STATUS_INCONSISTENT_WITH_FUTURE_KICKOFF")
        self.assertEqual(future_status_quarantine_reason("suspended"), "NONSTANDARD_STATUS")
        self.assertEqual(future_status_quarantine_reason("canceled"), "NONSTANDARD_STATUS")
        self.assertEqual(future_status_quarantine_reason("postponed"), "NONSTANDARD_STATUS")
        self.assertEqual(future_status_quarantine_reason("scheduled"), "UNKNOWN_STATUS_VALUE")
        self.assertEqual(future_status_quarantine_reason(None), "MISSING_STATUS")

    def test_runtime_workflow_emits_trace_and_placeholder_when_overlay_disabled(self):
        workflow = (Path(__file__).resolve().parents[1] / ".github/workflows/oracle-selected50-research-runtime.yml").read_text(encoding="utf-8")
        self.assertIn("--out-trace selected50_runtime_output/current_snapshot_candidate_trace.csv", workflow)
        self.assertIn("selected50_runtime_output/current_snapshot_candidate_trace.csv", workflow)
        self.assertIn("from scripts.overlay_selected50_current_snapshot import TRACE_COLUMNS", workflow)
        self.assertIn("name: Upload derived report and sanitized QA only", workflow)

    def test_row_level_trace_hashes_snapshot_and_archive_and_deduplicates_unsupported_leagues(self):
        now = datetime.now(timezone.utc)
        seasons = [
            {"selected_season_id": f"S{i:02d}", "country": f"Country {i:02d}",
             "competition": f"League {i:02d}", "http_status": 200, "provider_success": True}
            for i in range(50)
        ]

        def fixture(fid, sid="S00", kickoff=None, **extra):
            row = {
                "id": fid, "selected_season_id": sid,
                "kickoff_utc": iso(kickoff or (now + timedelta(hours=2))),
                "status": "incomplete", "no_home_away": 0,
                "homeID": 10, "awayID": 20,
                "home_name": "Home FC", "away_name": "Away FC",
            }
            row.update(extra)
            return row

        fixture_rows = [
            fixture("FUTURE-1"),
            fixture("UNSUPPORTED-1", sid="S01"),
            fixture("UNSUPPORTED-2", sid="S01", kickoff=now + timedelta(hours=3)),
            fixture("FLAGGED", no_home_away=1),
            fixture("UNKNOWN-FLAG", no_home_away="unknown"),
            fixture("UNKNOWN-STATUS", status="scheduled"),
            fixture("COMPLETE-FUTURE", status="complete"),
            fixture("SUSPENDED-FUTURE", status="suspended"),
            fixture("MISSING-STATUS", status=""),
            fixture("HISTORICAL", kickoff=now - timedelta(hours=1)),
            fixture("BEYOND", kickoff=now + timedelta(days=8)),
            fixture("BAD-TIME", kickoff_utc="not-a-timestamp"),
        ]
        snapshot = {"retrieved_utc": iso(now - timedelta(minutes=5)), "per_season": seasons, "fixture_rows": fixture_rows}

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            archive_path = root / "archive.zip"
            snapshot_path = root / "snapshot.json"
            out_archive = root / "overlay.zip"
            out_qa = root / "overlay-qa.json"
            out_trace = root / "candidate-trace.csv"
            manifest = [
                {"season_id": f"S{i:02d}", "selected_country": f"Country {i:02d}",
                 "selected_competition_name": f"League {i:02d}", "season": "2026"}
                for i in range(50)
            ]
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("private/archive/ingestion_manifest.json", json.dumps(manifest))
                archive.writestr("private/archive/seasons/S00/matches.json", "[]")
                archive.writestr("private/archive/seasons/S00/teams.json", "[]")
            snapshot_bytes = json.dumps(snapshot, separators=(",", ":")).encode("utf-8")
            snapshot_path.write_bytes(snapshot_bytes)
            argv = [
                "overlay_selected50_current_snapshot.py", "--archive", str(archive_path),
                "--snapshot", str(snapshot_path), "--out-archive", str(out_archive),
                "--out-qa", str(out_qa), "--out-trace", str(out_trace),
            ]
            with patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
                main()
            qa = json.loads(out_qa.read_text(encoding="utf-8"))
            with out_trace.open(encoding="utf-8", newline="") as trace_file:
                trace_rows = list(csv.DictReader(trace_file))
            by_id = {row["fixture_id"]: row for row in trace_rows if row["fixture_id"]}

            self.assertEqual(qa["candidate_rows_added"], 1)
            self.assertEqual(qa["unsupported_archive_rows_not_staged"], 2)
            self.assertIn("DOCUMENTED_FIELD_SEMANTICS", qa["no_home_away_flag_semantics"])
            self.assertIn("no_home_away=1", qa["no_home_away_flag_semantics"])
            self.assertIn("remain quarantined", qa["no_home_away_flag_semantics"])
            by_league = {f'{row["country"]} | {row["competition"]}': row for row in qa["no_home_away_flag_by_league"]}
            self.assertEqual(by_league["Country 00 | League 00"]["future_rows_in_7d"], 7)
            self.assertEqual(by_league["Country 00 | League 00"]["no_home_away_true"], 1)
            self.assertEqual(by_league["Country 00 | League 00"]["no_home_away_false"], 5)
            self.assertEqual(by_league["Country 00 | League 00"]["no_home_away_unknown"], 1)
            self.assertEqual(by_league["Country 01 | League 01"]["future_rows_in_7d"], 2)
            self.assertEqual(by_league["Country 01 | League 01"]["no_home_away_false"], 2)
            self.assertEqual(qa["unsupported_selected_league_count"], 1)
            self.assertEqual(len(qa["unsupported_selected_leagues"]), 1)
            self.assertEqual(qa["candidate_trace_rows"], len(fixture_rows))
            self.assertEqual(qa["snapshot_file_sha256"], hashlib.sha256(snapshot_bytes).hexdigest())
            self.assertEqual(qa["source_archive_sha256"], hashlib.sha256(archive_path.read_bytes()).hexdigest())
            self.assertEqual(qa["overlay_archive_sha256"], hashlib.sha256(out_archive.read_bytes()).hexdigest())
            self.assertEqual(len(trace_rows), len(fixture_rows))
            self.assertEqual(by_id["FUTURE-1"]["trace_outcome"], "STAGED_PROVIDER_NATIVE_ROW_RESEARCH_ONLY")
            self.assertEqual(by_id["UNSUPPORTED-1"]["trace_outcome"], "UNSUPPORTED_ARCHIVE_NO_EXACT_LABEL_SEASON_WITH_MATCHES_AND_TEAMS")
            self.assertEqual(by_id["UNSUPPORTED-2"]["trace_outcome"], "UNSUPPORTED_ARCHIVE_NO_EXACT_LABEL_SEASON_WITH_MATCHES_AND_TEAMS")
            self.assertEqual(by_id["FLAGGED"]["trace_outcome"], "QUARANTINED_INVALID_OR_NONSTANDARD")
            self.assertEqual(by_id["UNKNOWN-FLAG"]["trace_reason"], "NO_HOME_AWAY_FLAG_UNKNOWN")
            self.assertEqual(by_id["UNKNOWN-STATUS"]["trace_reason"], "UNKNOWN_STATUS_VALUE")
            self.assertEqual(by_id["COMPLETE-FUTURE"]["trace_reason"], "STATUS_INCONSISTENT_WITH_FUTURE_KICKOFF")
            self.assertEqual(by_id["SUSPENDED-FUTURE"]["trace_reason"], "NONSTANDARD_STATUS")
            self.assertEqual(by_id["MISSING-STATUS"]["trace_reason"], "MISSING_STATUS")
            self.assertEqual(by_id["HISTORICAL"]["trace_outcome"], "HISTORICAL_NOT_STAGED")
            self.assertEqual(by_id["BEYOND"]["trace_outcome"], "BEYOND_7D_NOT_STAGED")
            self.assertEqual(by_id["BAD-TIME"]["trace_outcome"], "QUARANTINED_INVALID_KICKOFF")
            self.assertEqual(by_id["FUTURE-1"]["production_eligible"], "NO")
            self.assertEqual(by_id["FUTURE-1"]["canonical_fixture_join_status"], "NOT_VERIFIED")
            self.assertIn("selected_country", TRACE_COLUMNS)
            self.assertIn("selected_competition", TRACE_COLUMNS)
            self.assertEqual(by_id["FUTURE-1"]["selected_country"], "Country 00")
            self.assertEqual(by_id["FUTURE-1"]["selected_competition"], "League 00")
            self.assertNotIn("home_name", TRACE_COLUMNS)
            self.assertNotIn("away_name", TRACE_COLUMNS)
            with zipfile.ZipFile(out_archive) as staged_archive:
                staged_rows = json.loads(staged_archive.read("private/archive/seasons/S00/matches.json").decode("utf-8"))
            self.assertEqual([row["id"] for row in staged_rows], ["FUTURE-1"])


if __name__ == "__main__":
    unittest.main()
