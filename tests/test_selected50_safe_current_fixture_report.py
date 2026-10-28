import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_selected50_safe_current_fixture_report.py"

class SafeCurrentReportContractTests(unittest.TestCase):
    def test_exact_identity_and_fail_closed_flag_handling(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seasons = [{"selected_season_id": str(i), "country": "Test", "competition": f"League {i}"} for i in range(50)]
            fixtures = [
                {"selected_season_id":"0","id":"100","kickoff_utc":"2026-10-29T12:00:00Z","status":"scheduled","no_home_away":0,"homeID":"1","awayID":"2","home_name":"Home A","away_name":"Away A"},
                {"selected_season_id":"1","id":"101","kickoff_utc":"2026-10-29T13:00:00Z","status":"scheduled","no_home_away":1,"homeID":"3","awayID":"4","home_name":"Home B","away_name":"Away B"},
                {"selected_season_id":"2","id":"102","kickoff_utc":"2026-10-29T14:00:00Z","status":"scheduled","no_home_away":None,"homeID":"5","awayID":"6","home_name":"Home C","away_name":"Away C"},
                {"selected_season_id":"3","id":"103","kickoff_utc":"2026-10-29T15:00:00Z","status":"scheduled","no_home_away":0,"homeID":"7","awayID":"8","home_name":"Home D","away_name":"Away D"},
            ]
            snap = root / "snapshot.json"
            snap.write_text(json.dumps({"retrieved_utc":"2026-10-28T00:00:00Z","per_season":seasons,"fixture_rows":fixtures}), encoding="utf-8")
            report = root / "runtime.csv"
            with report.open("w", newline="", encoding="utf-8") as h:
                w = csv.DictWriter(h, fieldnames=["provider_season_id","fixture_id","home_team_provider_id","away_team_provider_id","BTTS_probability_pct"])
                w.writeheader()
                w.writerow({"provider_season_id":"0","fixture_id":"100","home_team_provider_id":"1","away_team_provider_id":"2","BTTS_probability_pct":"61.5"})
                w.writerow({"provider_season_id":"1","fixture_id":"101","home_team_provider_id":"3","away_team_provider_id":"4","BTTS_probability_pct":"70"})
                w.writerow({"provider_season_id":"2","fixture_id":"102","home_team_provider_id":"5","away_team_provider_id":"6","BTTS_probability_pct":"75"})
                w.writerow({"provider_season_id":"3","fixture_id":"103","home_team_provider_id":"WRONG","away_team_provider_id":"8","BTTS_probability_pct":"80"})
            out = root / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), "--snapshot", str(snap), "--runtime-report", str(report), "--out-dir", str(out), "--as-of-utc", "2026-10-28T10:00:00Z"], text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            qa = json.loads((out / "oracle_selected50_safe_current_fixture_report_qa.json").read_text())
            self.assertEqual(qa["safe_exact_join_rows"], 1)
            self.assertEqual(qa["snapshot_provenance_status"], "PASS_FRESH_TIMEZONE_AWARE")
            self.assertEqual(qa["snapshot_age_seconds"], 36000)
            self.assertEqual(qa["snapshot_file_sha256"], hashlib.sha256(snap.read_bytes()).hexdigest())
            self.assertEqual(qa["reason_counts"]["QUARANTINE_NO_HOME_AWAY_TRUE"], 1)
            self.assertEqual(qa["reason_counts"]["QUARANTINE_NO_HOME_AWAY_UNKNOWN"], 1)
            self.assertEqual(qa["reason_counts"]["BLOCKED_ORDERED_TEAM_ID_MISMATCH"], 1)
            with (out / "oracle_selected50_safe_current_fixture_report.csv").open(newline="", encoding="utf-8") as h:
                rows = list(csv.DictReader(h))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["fixture_id"], "100")
            self.assertEqual(rows[0]["BTTS_probability_pct"], "61.5")
            self.assertEqual(rows[0]["production_eligible"], "NO")
            self.assertEqual(rows[0]["betting_eligible"], "NO")
            self.assertEqual(rows[0]["snapshot_provenance_status"], "PASS_FRESH_TIMEZONE_AWARE")
            self.assertEqual(rows[0]["snapshot_age_seconds"], "36000")
            self.assertEqual(rows[0]["snapshot_file_sha256"], hashlib.sha256(snap.read_bytes()).hexdigest())

    def test_missing_naive_future_and_stale_snapshot_timestamps_fail_closed(self):
        cases = [
            ("missing", None),
            ("timezone_naive", "2026-10-28T00:00:00"),
            ("future", "2026-10-28T10:01:00Z"),
            ("stale", "2026-10-26T09:59:00Z"),
        ]
        for label, retrieved in cases:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                seasons = [{"selected_season_id": str(i), "country": "Test", "competition": f"League {i}"} for i in range(50)]
                snap_obj = {"per_season": seasons, "fixture_rows": []}
                if retrieved is not None:
                    snap_obj["retrieved_utc"] = retrieved
                snap = root / "snapshot.json"
                snap.write_text(json.dumps(snap_obj), encoding="utf-8")
                report = root / "runtime.csv"
                with report.open("w", newline="", encoding="utf-8") as h:
                    w = csv.writer(h)
                    w.writerow(["provider_season_id", "fixture_id", "home_team_provider_id", "away_team_provider_id"])
                    w.writerow(["0", "100", "1", "2"])
                out = root / "out"
                proc = subprocess.run(
                    [sys.executable, str(SCRIPT), "--snapshot", str(snap), "--runtime-report", str(report),
                     "--out-dir", str(out), "--as-of-utc", "2026-10-28T10:00:00Z"],
                    text=True, capture_output=True
                )
                self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                self.assertIn("FAIL:", proc.stderr)

    def test_duplicate_runtime_exact_key_is_blocked_instead_of_first_row_winning(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seasons = [{"selected_season_id": str(i), "country": "Test", "competition": f"League {i}"} for i in range(50)]
            fixtures = [{
                "selected_season_id": "0", "id": "100",
                "kickoff_utc": "2026-10-29T12:00:00Z", "status": "scheduled",
                "no_home_away": 0, "homeID": "1", "awayID": "2",
                "home_name": "Home A", "away_name": "Away A"
            }]
            snap = root / "snapshot.json"
            snap.write_text(json.dumps({
                "retrieved_utc": "2026-10-28T19:00:00Z",
                "per_season": seasons, "fixture_rows": fixtures
            }), encoding="utf-8")
            report = root / "runtime.csv"
            with report.open("w", newline="", encoding="utf-8") as h:
                w = csv.DictWriter(h, fieldnames=[
                    "provider_season_id", "fixture_id", "home_team_provider_id",
                    "away_team_provider_id", "BTTS_probability_pct"
                ])
                w.writeheader()
                w.writerow({
                    "provider_season_id": "0", "fixture_id": "100",
                    "home_team_provider_id": "1", "away_team_provider_id": "2",
                    "BTTS_probability_pct": "61.5"
                })
                w.writerow({
                    "provider_season_id": "0", "fixture_id": "100",
                    "home_team_provider_id": "1", "away_team_provider_id": "2",
                    "BTTS_probability_pct": "77.0"
                })
            out = root / "out"
            proc = subprocess.run([
                sys.executable, str(SCRIPT), "--snapshot", str(snap),
                "--runtime-report", str(report), "--out-dir", str(out),
                "--as-of-utc", "2026-10-28T20:00:00Z"
            ], text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            qa = json.loads((out / "oracle_selected50_safe_current_fixture_report_qa.json").read_text())
            self.assertEqual(qa["runtime_report_rows"], 2)
            self.assertEqual(qa["duplicate_runtime_exact_keys"], 1)
            self.assertEqual(qa["ambiguous_runtime_exact_key_count"], 1)
            self.assertEqual(qa["source_candidates_blocked_by_duplicate_runtime_exact_key"], 1)
            self.assertEqual(qa["reason_counts"]["BLOCKED_DUPLICATE_RUNTIME_EXACT_KEY"], 1)
            self.assertEqual(qa["safe_exact_join_rows"], 0)
            with (out / "oracle_selected50_safe_current_fixture_report.csv").open(newline="", encoding="utf-8") as h:
                rows = list(csv.DictReader(h))
            self.assertEqual(rows, [])

    def test_nonblank_combo_probability_input_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seasons = [{"selected_season_id": str(i), "country": "Test", "competition": f"League {i}"} for i in range(50)]
            snap = root / "snapshot.json"
            snap.write_text(json.dumps({
                "retrieved_utc": "2026-10-28T19:00:00Z",
                "per_season": seasons, "fixture_rows": []
            }), encoding="utf-8")
            report = root / "runtime.csv"
            with report.open("w", newline="", encoding="utf-8") as h:
                w = csv.DictWriter(h, fieldnames=[
                    "provider_season_id", "fixture_id", "home_team_provider_id",
                    "away_team_provider_id", "COMBO_HOME_probability_pct",
                    "COMBO_AWAY_probability_pct", "combo_probability_status"
                ])
                w.writeheader()
                w.writerow({
                    "provider_season_id": "0", "fixture_id": "100",
                    "home_team_provider_id": "1", "away_team_provider_id": "2",
                    "COMBO_HOME_probability_pct": "55.0",
                    "COMBO_AWAY_probability_pct": "",
                    "combo_probability_status": "BLOCKED_SETTLEMENT_SPEC_MISMATCH"
                })
            out = root / "out"
            proc = subprocess.run([
                sys.executable, str(SCRIPT), "--snapshot", str(snap),
                "--runtime-report", str(report), "--out-dir", str(out),
                "--as-of-utc", "2026-10-28T20:00:00Z"
            ], text=True, capture_output=True)
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("Combo probability values must remain masked", proc.stderr)
            self.assertFalse((out / "oracle_selected50_safe_current_fixture_report.csv").exists())

if __name__ == "__main__":
    unittest.main()
