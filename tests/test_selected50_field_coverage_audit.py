import csv, json, subprocess, sys, tempfile, unittest
from pathlib import Path
from openpyxl import Workbook, load_workbook

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_selected50_field_coverage_audit.py"

class FieldCoverageAuditTests(unittest.TestCase):
    def test_builds_50_group_matrix_normalizes_report_statuses_and_preserves_oracle_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            book = root / "source.xlsx"
            out = root / "out"
            wb = Workbook()
            oracle = wb.active
            oracle.title = "Oracle V1.6 Output"
            oracle.append(["Fixture", "BTTS"])
            oracle.append(["A vs B", 57.3])
            cov = wb.create_sheet("50-League Coverage")
            cov.append(["Selected Season ID", "Country", "League"])
            for i in range(50):
                cov.append([f"S{i+1:02d}", "Testland", f"League {i+1}"])
            mi = wb.create_sheet("Market Intelligence")
            mi.append(["Provider Season ID", "League", "BTTS Yes"])
            for i in range(50):
                mi.append([f"S{i+1:02d}", f"League {i+1}", 55.0 if i else "NOT_AVAILABLE_FROM_ORACLE_OUTPUT"])
            xg = wb.create_sheet("xG Evidence Audit")
            xg.append(["selected_id", "League", "capture_time_utc", "prediction_use_status"])
            for i in range(50):
                xg.append([f"S{i+1:02d}", f"League {i+1}", None, "QUARANTINED_RESEARCH_AUDIT_ONLY"])
            sched = wb.create_sheet("Schedule Reconciliation")
            sched.append(["selected_id", "League", "reason"])
            sched.append(["S01", "League 1", "KICKOFF_MISMATCH"])
            goal = wb.create_sheet("Goal Market Research")
            goal.append(["provider_season_id", "League", "forecast_status", "blocked_reason"])
            for i in range(50):
                goal.append([f"S{i+1:02d}", f"League {i+1}", "EXPERIMENTAL_UNCALIBRATED", None])
            quality = wb.create_sheet("Data Quality & Risk")
            quality.append(["selected_id", "League", "schedule_reconciliation_status", "schedule_reconciliation_reason", "runtime_kickoff_utc", "archive_kickoff_utc", "schedule_delta_minutes_archive_minus_runtime"])
            for i in range(49):
                quality.append([f"S{i+1:02d}", f"League {i+1}", "MATCH", None, "2026-10-31T12:00:00Z", "2026-10-31T12:00:00Z", None])
            quality.append(["S50", "League 50", "REVIEW_REQUIRED", "KICKOFF_MISMATCH", "2026-10-31T12:00:00Z", "2026-10-31T12:05:00Z", 5])
            wb.save(book)

            subprocess.run([sys.executable, str(SCRIPT), "--workbook", str(book), "--out-dir", str(out)], check=True, capture_output=True, text=True)

            qa = json.loads((out / "oracle_selected50_field_coverage_qa.json").read_text())
            self.assertEqual(qa["selected_league_groups"], 50)
            self.assertEqual(qa["status"], "PASS_FIELD_BY_FIELD_SELECTED50_REPORT_AUDIT")
            self.assertEqual(qa["unmapped_rows_by_sheet"], {})
            self.assertEqual(qa["report_only_status_normalizations"]["goal_market_nonblocked_reason_filled"], 50)
            self.assertEqual(qa["report_only_status_normalizations"]["schedule_no_mismatch_reason_filled"], 49)
            self.assertEqual(qa["report_only_status_normalizations"]["schedule_exact_match_zero_delta_filled"], 49)
            with (out / "oracle_selected50_field_coverage_by_league.csv").open(encoding="utf-8-sig", newline="") as f:
                matrix = list(csv.DictReader(f))
            self.assertEqual(len(matrix), 50 * (3 + 3 + 4 + 3 + 4 + 7))
            xg_capture = [r for r in matrix if r["Source Sheet"] == "xG Evidence Audit" and r["Field"] == "capture_time_utc"]
            self.assertEqual(len(xg_capture), 50)
            self.assertTrue(all(r["Coverage State"] == "NO_USABLE_VALUES" for r in xg_capture))
            xg_status = [r for r in matrix if r["Source Sheet"] == "xG Evidence Audit" and r["Field"] == "prediction_use_status"]
            self.assertTrue(all(r["Coverage State"] == "STATUS_PRESENT_ALL_RECORDS" for r in xg_status))
            blocked_reason = [r for r in matrix if r["Source Sheet"] == "Goal Market Research" and r["Field"] == "blocked_reason"]
            self.assertTrue(all(r["Coverage State"] == "STATUS_PRESENT_ALL_RECORDS" for r in blocked_reason))
            schedule_reason = [r for r in matrix if r["Source Sheet"] == "Data Quality & Risk" and r["Field"] == "schedule_reconciliation_reason"]
            self.assertTrue(all(r["Coverage State"] == "STATUS_PRESENT_ALL_RECORDS" for r in schedule_reason))

            result = load_workbook(book, read_only=True, data_only=True)
            self.assertEqual(result["Oracle V1.6 Output"].max_column, 2)
            self.assertEqual(result["Oracle V1.6 Output"].cell(2,2).value, 57.3)
            self.assertIn("50-League Field Coverage", result.sheetnames)
            self.assertIn("Field Coverage Summary", result.sheetnames)
            self.assertIn("Field Coverage Exceptions", result.sheetnames)
            self.assertEqual(result["Goal Market Research"].cell(2,4).value, "NONE_FORECASTABLE_RESEARCH_ONLY")
            self.assertEqual(result["Data Quality & Risk"].cell(2,4).value, "NOT_REQUIRED_NO_KICKOFF_MISMATCH")
            self.assertEqual(result["Data Quality & Risk"].cell(2,7).value, 0)
            result.close()

if __name__ == "__main__":
    unittest.main()
