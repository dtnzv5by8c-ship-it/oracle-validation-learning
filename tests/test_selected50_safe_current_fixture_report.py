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
            snap.write_text(json.dumps({"retrieved_utc":"2026-10-28T00:00:00Z","window_start_utc":"2026-09-28T10:00:00Z","window_end_utc":"2026-11-11T10:00:00Z","per_season":seasons,"fixture_rows":fixtures}), encoding="utf-8")
            report = root / "runtime.csv"
            with report.open("w", newline="", encoding="utf-8") as h:
                w = csv.DictWriter(h, fieldnames=[
                    "provider_season_id", "fixture_id", "date_utc", "home_team_provider_id",
                    "away_team_provider_id", "BTTS_probability_pct",
                    "COMBO_HOME_probability_pct", "COMBO_AWAY_probability_pct",
                    "combo_probability_status"
                ])
                w.writeheader()
                w.writerow({"provider_season_id":"0","fixture_id":"100","date_utc":"2026-10-29T12:00:00Z","home_team_provider_id":"1","away_team_provider_id":"2","BTTS_probability_pct":"61.5"})
                w.writerow({"provider_season_id":"1","fixture_id":"101","date_utc":"2026-10-29T13:00:00Z","home_team_provider_id":"3","away_team_provider_id":"4","BTTS_probability_pct":"70"})
                w.writerow({"provider_season_id":"2","fixture_id":"102","date_utc":"2026-10-29T14:00:00Z","home_team_provider_id":"5","away_team_provider_id":"6","BTTS_probability_pct":"75"})
                w.writerow({"provider_season_id":"3","fixture_id":"103","date_utc":"2026-10-29T15:00:00Z","home_team_provider_id":"WRONG","away_team_provider_id":"8","BTTS_probability_pct":"80"})
            out = root / "out"
            proc = subprocess.run([sys.executable, str(SCRIPT), "--snapshot", str(snap), "--runtime-report", str(report), "--out-dir", str(out), "--as-of-utc", "2026-10-28T10:00:00Z"], text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            qa = json.loads((out / "oracle_selected50_safe_current_fixture_report_qa.json").read_text())
            self.assertEqual(qa["safe_exact_join_rows"], 1)
            self.assertEqual(qa["snapshot_provenance_status"], "PASS_FRESH_TIMEZONE_AWARE")
            self.assertEqual(qa["snapshot_age_seconds"], 36000)
            self.assertEqual(qa["snapshot_file_sha256"], hashlib.sha256(snap.read_bytes()).hexdigest())
            self.assertEqual(qa["combo_probability_columns_checked"], ["COMBO_HOME_probability_pct", "COMBO_AWAY_probability_pct"])
            self.assertEqual(qa["combo_probability_nonblank_cells"], 0)
            self.assertEqual(qa["combo_masking_status"], "PASS_ALL_COMBO_PROBABILITY_VALUES_BLANK")
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
            self.assertEqual(rows[0]["COMBO_HOME_probability_pct"], "")
            self.assertEqual(rows[0]["COMBO_AWAY_probability_pct"], "")

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
                    "provider_season_id", "fixture_id", "date_utc", "home_team_provider_id",
                    "away_team_provider_id", "BTTS_probability_pct"
                ])
                w.writeheader()
                w.writerow({
                    "provider_season_id": "0", "fixture_id": "100", "date_utc": "2026-10-29T12:00:00Z",
                    "home_team_provider_id": "1", "away_team_provider_id": "2",
                    "BTTS_probability_pct": "61.5"
                })
                w.writerow({
                    "provider_season_id": "0", "fixture_id": "100", "date_utc": "2026-10-29T12:00:00Z",
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
                    "provider_season_id", "fixture_id", "date_utc", "home_team_provider_id",
                    "away_team_provider_id", "COMBO_HOME_probability_pct",
                    "COMBO_AWAY_probability_pct", "combo_probability_status"
                ])
                w.writeheader()
                w.writerow({
                    "provider_season_id": "0", "fixture_id": "100", "date_utc": "2026-10-29T12:00:00Z",
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


    def test_14_day_assessment_separates_out_of_runtime_window_from_missing_join_and_quarantine(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seasons = [{"selected_season_id": str(i), "country": "Test", "competition": f"League {i}"} for i in range(50)]
            fixtures = [
                {"selected_season_id":"0","id":"A","kickoff_utc":"2026-10-29T12:00:00Z","status":"scheduled","no_home_away":0,"homeID":"1","awayID":"2"},
                {"selected_season_id":"1","id":"B","kickoff_utc":"2026-11-07T13:00:00Z","status":"scheduled","no_home_away":0,"homeID":"3","awayID":"4"},
                {"selected_season_id":"2","id":"C","kickoff_utc":"2026-11-08T14:00:00Z","status":"scheduled","no_home_away":1,"homeID":"5","awayID":"6"},
                {"selected_season_id":"3","id":"D","kickoff_utc":"2026-11-09T14:00:00Z","status":"suspended","no_home_away":0,"homeID":"7","awayID":"8"},
                {"selected_season_id":"4","id":"E","kickoff_utc":"2026-10-31T12:00:00Z","status":"scheduled","no_home_away":0,"homeID":"9","awayID":"10"},
                {"selected_season_id":"5","id":"F","kickoff_utc":"2026-10-28T10:05:00Z","status":"scheduled","no_home_away":0,"homeID":"11","awayID":"12"},
            ]
            snap = root / "snapshot.json"
            snap.write_text(json.dumps({"retrieved_utc":"2026-10-28T00:00:00Z","window_start_utc":"2026-09-28T10:00:00Z","window_end_utc":"2026-11-11T10:00:00Z","per_season":seasons,"fixture_rows":fixtures}), encoding="utf-8")
            report = root / "runtime.csv"
            with report.open("w", newline="", encoding="utf-8") as h:
                w = csv.DictWriter(h, fieldnames=[
                    "provider_season_id", "fixture_id", "date_utc", "home_team_provider_id",
                    "away_team_provider_id", "BTTS_probability_pct",
                    "COMBO_HOME_probability_pct", "COMBO_AWAY_probability_pct"
                ])
                w.writeheader()
                w.writerow({"provider_season_id":"0","fixture_id":"A","date_utc":"2026-10-29T12:00:00Z","home_team_provider_id":"1","away_team_provider_id":"2","BTTS_probability_pct":"61.5"})
            out = root / "out"
            proc = subprocess.run([
                sys.executable, str(SCRIPT), "--snapshot", str(snap),
                "--runtime-report", str(report), "--out-dir", str(out),
                "--as-of-utc", "2026-10-28T10:00:00Z",
                "--runtime-started-utc", "2026-10-28T10:00:00Z",
                "--report-horizon-days", "14", "--runtime-horizon-days", "7",
                "--minimum-lead-minutes", "15"
            ], text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            qa = json.loads((out / "oracle_selected50_safe_current_fixture_report_qa.json").read_text())
            self.assertEqual(qa["report_horizon_days"], 14)
            self.assertEqual(qa["runtime_generation_horizon_days"], 7)
            self.assertEqual(qa["source_candidates_in_report_horizon"], 3)
            self.assertEqual(qa["source_candidates_outside_runtime_window_not_missing_join"], 1)
            self.assertEqual(qa["source_candidates_outside_minimum_lead_window_not_missing_join"], 1)
            self.assertEqual(qa["source_candidates_blocked_by_missing_runtime_or_team_identity"], 1)
            self.assertEqual(qa["safe_exact_join_rows"], 1)
            self.assertFalse(qa["expanded_prediction_report_approved"])
            self.assertTrue(qa["per_fixture_quarantine_preserved"])
            self.assertTrue(qa["market_gates_preserved"])
            with (out / "oracle_selected50_safe_current_fixture_report.csv").open(newline="", encoding="utf-8") as h:
                joined = list(csv.DictReader(h))
            self.assertEqual([r["fixture_id"] for r in joined], ["A"])
            self.assertEqual(joined[0]["production_eligible"], "NO")
            self.assertEqual(joined[0]["betting_eligible"], "NO")
            self.assertEqual(joined[0]["combo_masked"], "YES")
            with (out / "oracle_selected50_safe_current_fixture_exclusions.csv").open(newline="", encoding="utf-8") as h:
                excluded = list(csv.DictReader(h))
            by_id = {r["fixture_id"]: r for r in excluded}
            self.assertEqual(by_id["B"]["classification"], "OUTSIDE_RUNTIME_GENERATION_WINDOW_NOT_MISSING_JOIN")
            self.assertEqual(by_id["B"]["market_gate_status"], "NOT_EVALUATED_OUTSIDE_RUNTIME_GENERATION_WINDOW")
            self.assertEqual(by_id["C"]["classification"], "QUARANTINE_NO_HOME_AWAY_TRUE")
            self.assertEqual(by_id["C"]["market_gate_status"], "BLOCKED_SOURCE_QUARANTINE")
            self.assertEqual(by_id["D"]["classification"], "QUARANTINE_NONSTANDARD_STATUS")
            self.assertEqual(by_id["E"]["classification"], "BLOCKED_NO_EXACT_RUNTIME_ROW")
            self.assertEqual(by_id["F"]["classification"], "OUTSIDE_MINIMUM_LEAD_WINDOW_NOT_MISSING_JOIN")
            for row in excluded:
                self.assertEqual(row["production_eligible"], "NO")
                self.assertEqual(row["betting_eligible"], "NO")
                self.assertEqual(row["combo_masked"], "YES")
                self.assertEqual(row["combo_probability_emitted"], "0")
                self.assertEqual(row["prediction_created"], "0")

    def test_future_completed_status_is_quarantined_before_horizon_classification(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seasons = [{"selected_season_id": str(i), "country": "Test", "competition": f"League {i}"} for i in range(50)]
            fixtures = [
                {"selected_season_id":"0","id":"A","kickoff_utc":"2026-10-30T12:00:00Z","status":"scheduled","no_home_away":0,"homeID":"1","awayID":"2"},
                {"selected_season_id":"1","id":"B","kickoff_utc":"2026-11-02T12:00:00Z","status":"finished","no_home_away":0,"homeID":"3","awayID":"4"},
                {"selected_season_id":"2","id":"C","kickoff_utc":"2026-11-08T12:00:00Z","status":"complete","no_home_away":0,"homeID":"5","awayID":"6"},
            ]
            snap = root / "snapshot.json"
            snap.write_text(json.dumps({"retrieved_utc":"2026-10-28T00:00:00Z","window_start_utc":"2026-09-28T10:00:00Z","window_end_utc":"2026-11-11T10:00:00Z","per_season":seasons,"fixture_rows":fixtures}), encoding="utf-8")
            report = root / "runtime.csv"
            with report.open("w", newline="", encoding="utf-8") as h:
                w = csv.DictWriter(h, fieldnames=[
                    "provider_season_id", "fixture_id", "date_utc", "home_team_provider_id",
                    "away_team_provider_id", "BTTS_probability_pct",
                    "COMBO_HOME_probability_pct", "COMBO_AWAY_probability_pct"
                ])
                w.writeheader()
                w.writerow({"provider_season_id":"0","fixture_id":"A","date_utc":"2026-10-30T12:00:00Z","home_team_provider_id":"1","away_team_provider_id":"2","BTTS_probability_pct":"61.5"})
            out = root / "out"
            proc = subprocess.run([
                sys.executable, str(SCRIPT), "--snapshot", str(snap),
                "--runtime-report", str(report), "--out-dir", str(out),
                "--as-of-utc", "2026-10-28T10:00:00Z",
                "--runtime-started-utc", "2026-10-28T10:00:00Z",
                "--report-horizon-days", "14", "--runtime-horizon-days", "7",
                "--minimum-lead-minutes", "15"
            ], text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            qa = json.loads((out / "oracle_selected50_safe_current_fixture_report_qa.json").read_text())
            self.assertEqual(qa["source_candidates_in_report_horizon"], 1)
            self.assertEqual(qa["source_candidates_outside_runtime_window_not_missing_join"], 0)
            self.assertEqual(qa["safe_exact_join_rows"], 1)
            self.assertEqual(qa["reason_counts"]["QUARANTINE_STATUS_INCONSISTENT_WITH_FUTURE_KICKOFF"], 2)
            with (out / "oracle_selected50_safe_current_fixture_exclusions.csv").open(newline="", encoding="utf-8") as h:
                excluded = list(csv.DictReader(h))
            by_id = {r["fixture_id"]: r for r in excluded}
            for fixture_id in ("B", "C"):
                self.assertEqual(by_id[fixture_id]["classification"], "QUARANTINE_STATUS_INCONSISTENT_WITH_FUTURE_KICKOFF")
                self.assertEqual(by_id[fixture_id]["market_gate_status"], "BLOCKED_SOURCE_QUARANTINE")
                self.assertEqual(by_id[fixture_id]["combo_masked"], "YES")
                self.assertEqual(by_id[fixture_id]["combo_probability_emitted"], "0")
                self.assertEqual(by_id[fixture_id]["production_eligible"], "NO")
                self.assertEqual(by_id[fixture_id]["betting_eligible"], "NO")

    def test_expanded_report_requires_runtime_start_and_runtime_horizon_stays_at_most_seven_days(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seasons = [{"selected_season_id": str(i), "country": "Test", "competition": f"League {i}"} for i in range(50)]
            snap = root / "snapshot.json"
            snap.write_text(json.dumps({"retrieved_utc":"2026-10-28T00:00:00Z","per_season":seasons,"fixture_rows":[]}), encoding="utf-8")
            report = root / "runtime.csv"
            with report.open("w", newline="", encoding="utf-8") as h:
                w = csv.writer(h)
                w.writerow(["provider_season_id","fixture_id","date_utc","home_team_provider_id","away_team_provider_id"])
                w.writerow(["0","A","2026-10-29T12:00:00Z","1","2"])
            for extra, message in [
                (["--report-horizon-days","14"], "--runtime-started-utc is required"),
                (["--report-horizon-days","14","--runtime-started-utc","2026-10-28T10:00:00Z","--runtime-horizon-days","8"], "--runtime-horizon-days must be between 1 and 7"),
            ]:
                with self.subTest(extra=extra):
                    out = root / ("out-" + str(len(extra)))
                    proc = subprocess.run([
                        sys.executable, str(SCRIPT), "--snapshot", str(snap),
                        "--runtime-report", str(report), "--out-dir", str(out),
                        "--as-of-utc", "2026-10-28T10:00:00Z", *extra
                    ], text=True, capture_output=True)
                    self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                    self.assertIn(message, proc.stderr)



    def test_exact_fixture_key_with_kickoff_mismatch_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seasons = [{"selected_season_id": str(i), "country": "Test", "competition": f"League {i}"} for i in range(50)]
            snap = root / "snapshot.json"
            snap.write_text(json.dumps({
                "retrieved_utc":"2026-10-28T00:00:00Z","per_season":seasons,
                "fixture_rows":[{"selected_season_id":"0","id":"A","kickoff_utc":"2026-10-29T12:00:00Z","status":"scheduled","no_home_away":0,"homeID":"1","awayID":"2"}]
            }), encoding="utf-8")
            report = root / "runtime.csv"
            with report.open("w", newline="", encoding="utf-8") as h:
                w = csv.DictWriter(h, fieldnames=[
                    "provider_season_id","fixture_id","date_utc","home_team_provider_id",
                    "away_team_provider_id","BTTS_probability_pct",
                    "COMBO_HOME_probability_pct","COMBO_AWAY_probability_pct"
                ])
                w.writeheader()
                w.writerow({"provider_season_id":"0","fixture_id":"A","date_utc":"2026-10-29T12:05:00Z","home_team_provider_id":"1","away_team_provider_id":"2","BTTS_probability_pct":"61.5"})
            out = root / "out"
            proc = subprocess.run([
                sys.executable, str(SCRIPT), "--snapshot", str(snap),
                "--runtime-report", str(report), "--out-dir", str(out),
                "--as-of-utc", "2026-10-28T10:00:00Z"
            ], text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            qa = json.loads((out / "oracle_selected50_safe_current_fixture_report_qa.json").read_text())
            self.assertEqual(qa["safe_exact_join_rows"], 0)
            self.assertEqual(qa["source_candidates_blocked_by_missing_runtime_or_team_identity"], 1)
            self.assertEqual(qa["reason_counts"]["BLOCKED_KICKOFF_MISMATCH"], 1)
            with (out / "oracle_selected50_safe_current_fixture_report.csv").open(newline="", encoding="utf-8") as h:
                self.assertEqual(list(csv.DictReader(h)), [])
            with (out / "oracle_selected50_safe_current_fixture_exclusions.csv").open(newline="", encoding="utf-8") as h:
                rows = list(csv.DictReader(h))
            self.assertEqual(rows[0]["classification"], "BLOCKED_KICKOFF_MISMATCH")
            self.assertEqual(rows[0]["market_gate_status"], "BLOCKED_KICKOFF_MISMATCH")
            self.assertEqual(rows[0]["runtime_kickoff_utc"], "2026-10-29T12:05:00Z")
            self.assertEqual(rows[0]["canonical_fixture_join_status"], "NOT_VERIFIED")
            self.assertEqual(rows[0]["official_settlement_truth_status"], "NOT_VERIFIED")
            self.assertEqual(rows[0]["combo_masked"], "YES")
            self.assertEqual(rows[0]["production_eligible"], "NO")
            self.assertEqual(rows[0]["betting_eligible"], "NO")


    def test_expanded_horizon_rejects_snapshot_retrieved_after_runtime_started(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seasons = [
                {"selected_season_id": str(i), "country": "Test", "competition": f"League {i}"}
                for i in range(50)
            ]
            snap = root / "snapshot.json"
            snap.write_text(json.dumps({
                "retrieved_utc": "2026-10-28T10:01:00Z",
                "per_season": seasons,
                "fixture_rows": []
            }), encoding="utf-8")
            report = root / "runtime.csv"
            with report.open("w", newline="", encoding="utf-8") as h:
                w = csv.writer(h)
                w.writerow([
                    "provider_season_id", "fixture_id", "date_utc",
                    "home_team_provider_id", "away_team_provider_id"
                ])
                w.writerow(["0", "A", "2026-10-29T12:00:00Z", "1", "2"])
            out = root / "out"
            proc = subprocess.run([
                sys.executable, str(SCRIPT),
                "--snapshot", str(snap),
                "--runtime-report", str(report),
                "--out-dir", str(out),
                "--as-of-utc", "2026-10-28T10:02:00Z",
                "--runtime-started-utc", "2026-10-28T10:00:00Z",
                "--report-horizon-days", "14",
                "--runtime-horizon-days", "7"
            ], text=True, capture_output=True)
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("post-runtime snapshot cannot establish out-of-window versus missing-join coverage", proc.stderr)
            self.assertFalse((out / "oracle_selected50_safe_current_fixture_report.csv").exists())


    def test_expanded_horizon_requires_declared_snapshot_coverage_end(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            seasons = [
                {"selected_season_id": str(i), "country": "Test", "competition": f"League {i}"}
                for i in range(50)
            ]
            report = root / "runtime.csv"
            with report.open("w", newline="", encoding="utf-8") as h:
                w = csv.writer(h)
                w.writerow([
                    "provider_season_id", "fixture_id", "date_utc",
                    "home_team_provider_id", "away_team_provider_id"
                ])
                w.writerow(["0", "A", "2026-10-29T12:00:00Z", "1", "2"])
            scenarios = [
                (None, "snapshot window_end_utc must be valid timezone-aware ISO-8601"),
                ("2026-11-11T09:00:00Z", "extends 3600 seconds beyond declared snapshot window_end_utc"),
            ]
            for window_end, message in scenarios:
                with self.subTest(window_end=window_end):
                    snap_obj = {
                        "retrieved_utc": "2026-10-28T00:00:00Z",
                        "window_start_utc": "2026-09-28T10:00:00Z",
                        "per_season": seasons,
                        "fixture_rows": [],
                    }
                    if window_end is not None:
                        snap_obj["window_end_utc"] = window_end
                    snap = root / ("snapshot-missing-end.json" if window_end is None else "snapshot-short-window.json")
                    snap.write_text(json.dumps(snap_obj), encoding="utf-8")
                    out = root / ("out-missing-end" if window_end is None else "out-short-window")
                    proc = subprocess.run([
                        sys.executable, str(SCRIPT),
                        "--snapshot", str(snap),
                        "--runtime-report", str(report),
                        "--out-dir", str(out),
                        "--as-of-utc", "2026-10-28T10:00:00Z",
                        "--runtime-started-utc", "2026-10-28T10:00:00Z",
                        "--report-horizon-days", "14",
                        "--runtime-horizon-days", "7",
                    ], text=True, capture_output=True)
                    self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
                    self.assertIn(message, proc.stderr)
                    self.assertFalse((out / "oracle_selected50_safe_current_fixture_report.csv").exists())



if __name__ == "__main__":
    unittest.main()
