import importlib.util
import unittest
import json
import tempfile
from pathlib import Path
from openpyxl import load_workbook

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_selected50_market_intelligence_report.py"
spec = importlib.util.spec_from_file_location("market_report", SCRIPT)
market_report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(market_report)


def archive_row(fid, date, home_id, away_id, hg, ag, season="S1", league="L1"):
    return {
        "provider_season_id": season, "provider_league_id": "L1", "fixture_id": fid,
        "home_team_id": home_id, "away_team_id": away_id,
        "kickoff_utc": date, "league_folder": league, "season_folder": "2026",
        "status_raw": "complete", "home_goals": str(hg), "away_goals": str(ag),
        "home_team": home_id, "away_team": away_id,
    }


def runtime_row():
    return {
        "fixture_id": "F100", "date_utc": "2026-10-31T18:00:00+00:00",
        "selected_id": "S1", "provider_season_id": "S1",
        "home_team_provider_id": "H", "away_team_provider_id": "A",
        "league": "Test League", "home_team": "Home FC", "away_team": "Away FC",
        "BTTS_probability_pct": "58.21", "DC_HOME_probability_pct": "71.09",
        "DC_AWAY_probability_pct": "49.87",
    }


class Selected50MarketIntelligenceTests(unittest.TestCase):
    def setUp(self):
        self.archive = [
            archive_row("F1", "2026-10-01T12:00:00+00:00", "H", "X", 2, 1),
            archive_row("F2", "2026-10-03T12:00:00+00:00", "Y", "A", 0, 1),
            archive_row("F3", "2026-10-08T12:00:00+00:00", "H", "Z", 1, 1),
            archive_row("F4", "2026-10-10T12:00:00+00:00", "W", "A", 2, 0),
            archive_row("F5", "2026-10-15T12:00:00+00:00", "H", "A", 3, 1),
            archive_row("F6", "2026-10-20T12:00:00+00:00", "A", "Q", 1, 2),
            archive_row("F7", "2026-10-25T12:00:00+00:00", "H", "P", 2, 0),
            archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0),
        ]

    def test_exact_join_requires_season_fixture_and_ordered_team_ids(self):
        rows, missing, duplicates = market_report.exact_join([runtime_row()], self.archive)
        self.assertEqual(len(rows), 1)
        self.assertEqual(missing, [])
        swapped = dict(runtime_row(), home_team_provider_id="A", away_team_provider_id="H")
        rows, missing, _ = market_report.exact_join([swapped], self.archive)
        self.assertEqual(rows, {})
        self.assertEqual(missing[0][1], "NO_EXACT_ARCHIVE_MATCH")

    def test_kickoff_mismatch_is_quarantined(self):
        changed = dict(self.archive[-1], kickoff_utc="2026-10-31T17:59:00+00:00")
        joined, missing, _ = market_report.exact_join([runtime_row()], self.archive[:-1] + [changed])
        self.assertEqual(len(joined), 1)
        self.assertEqual(missing[0][1], "SCHEDULE_KICKOFF_MISMATCH")
        self.assertEqual(missing[0][2]["kickoff_utc"], "2026-10-31T17:59:00+00:00")
        report, trace, summary = market_report.build_report(
            [runtime_row()], self.archive[:-1] + [changed]
        )
        self.assertEqual(len(report), 1)
        self.assertEqual(summary["exact_archive_joins"], 1)
        self.assertEqual(summary["schedule_discordance_rows"], 1)
        self.assertEqual(summary["schedule_reconciliation_gate"], "REVIEW_REQUIRED")
        self.assertEqual(summary["join_failure_reason_counts"], {
            "SCHEDULE_KICKOFF_MISMATCH": 1
        })
        self.assertEqual(trace[0]["runtime_kickoff_utc"], "2026-10-31T18:00:00+00:00")
        self.assertEqual(trace[0]["archive_kickoff_utc"], "2026-10-31T17:59:00+00:00")
        self.assertEqual(trace[0]["join_status"], "PASS_EXACT_SEASON_FIXTURE_ORDERED_TEAM_IDS")
        self.assertEqual(trace[0]["schedule_reconciliation_status"], "MISMATCH_REVIEW_REQUIRED")
        self.assertEqual(summary["report_rows"], 1)

    def test_schedule_discordant_target_is_not_used_as_historical_evidence(self):
        target = dict(self.archive[-1], status_raw="complete", home_goals="9", away_goals="0",
                      kickoff_utc="2026-10-31T17:59:00+00:00")
        other_runtime = dict(runtime_row(), fixture_id="F200",
                             date_utc="2026-11-01T12:00:00+00:00",
                             home_team_provider_id="H", away_team_provider_id="A")
        other_target = archive_row("F200", "2026-11-01T12:00:00+00:00", "H", "A", 0, 0)
        report, trace, summary = market_report.build_report(
            [runtime_row(), other_runtime], self.archive[:-1] + [target, other_target]
        )
        self.assertEqual(summary["schedule_discordance_rows"], 1)
        self.assertNotIn("F100", trace[1].get("home_form_source_fixture_ids", ""))
        self.assertNotIn("F100", trace[1].get("away_form_source_fixture_ids", ""))

    def test_schedule_conflict_exclusion_uses_full_composite_identity(self):
        conflicted = dict(self.archive[-1], kickoff_utc="2026-10-31T17:59:00+00:00")
        same_fixture_id_other_season = archive_row(
            "F100", "2026-10-20T12:00:00+00:00", "H", "B", 4, 0, season="S2"
        )
        other_runtime = dict(runtime_row(), fixture_id="F200", provider_season_id="S2",
                             date_utc="2026-11-01T12:00:00+00:00",
                             home_team_provider_id="B", away_team_provider_id="C")
        other_target = archive_row("F200", "2026-11-01T12:00:00+00:00", "B", "C", 0, 0, season="S2")
        _, trace, summary = market_report.build_report(
            [runtime_row(), other_runtime],
            self.archive[:-1] + [conflicted, same_fixture_id_other_season, other_target]
        )
        self.assertEqual(summary["schedule_discordance_rows"], 1)
        self.assertIn("F100", trace[1]["home_form_source_fixture_ids"])
        self.assertEqual(trace[1]["home_at_home_form_n"], 0)

    def test_h2h_uses_verified_provider_competition_across_seasons(self):
        prior = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                            season="S1", league="L1")
        target_archive = archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0,
                                     season="S2", league="L1")
        target_runtime = dict(runtime_row(), provider_season_id="S2", selected_id="S2")
        report, trace, _ = market_report.build_report(
            [target_runtime], [prior, target_archive]
        )
        self.assertEqual(trace[0]["h2h_n"], 1)
        self.assertEqual(trace[0]["h2h_scope"], "EXPLICIT_PROVIDER_COMPETITION_ID_SCOPE")
        self.assertIn("OLD1", trace[0]["h2h_source_fixture_ids"])
        self.assertEqual(report[0]["H2H Last 5 Summary"], "W")

    def test_same_season_competition_key_is_not_claimed_as_cross_season_coverage(self):
        prior = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                            season="S1", league="L1")
        target_archive = archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0,
                                     season="S2", league="L1")
        target_runtime = dict(runtime_row(), provider_season_id="S2", selected_id="S2")
        report, trace, _ = market_report.build_report([target_runtime], [prior, target_archive])
        self.assertEqual(trace[0]["h2h_scope"], "EXPLICIT_PROVIDER_COMPETITION_ID_SCOPE")
        meetings = json.loads(trace[0]["h2h_meetings_detail"])
        self.assertEqual(meetings[0]["provider_season_id"], "S1")
        self.assertEqual(report[0]["H2H Last 5 Summary"], "W")

    def test_venue_split_form_is_exposed_in_evidence_trace(self):
        _, trace, _ = market_report.build_report([runtime_row()], self.archive)
        self.assertEqual(trace[0]["home_at_home_form_n"], 4)
        self.assertEqual(trace[0]["away_away_form_n"], 3)
        self.assertEqual(trace[0]["home_at_home_form"], "WDWW")
        self.assertEqual(trace[0]["away_away_form"], "WLL")

    def test_same_kickoff_fixture_is_not_used_as_history(self):
        same_time = archive_row("F101", "2026-10-31T18:00:00+00:00", "H", "B", 4, 0)
        report, trace, summary = market_report.build_report([runtime_row()], self.archive + [same_time])
        self.assertEqual(trace[0]["home_form_n"], 4)
        self.assertEqual(trace[0]["away_form_n"], 4)
        self.assertEqual(summary["exact_archive_joins"], 1)

    def test_raw_probabilities_are_copied_and_unsupported_markets_masked(self):
        report, _, _ = market_report.build_report([runtime_row()], self.archive)
        row = report[0]
        self.assertEqual(row["BTTS Yes"], "58.21")
        self.assertEqual(row["Home 1X"], "71.09")
        self.assertEqual(row["Away X2"], "49.87")
        for header in market_report.HEADERS[6:20]:
            self.assertEqual(row[header], market_report.UNAVAILABLE)
        self.assertEqual(len(market_report.HEADERS), 38)
        self.assertFalse(any("COMBO" in h and row[h] not in ("", market_report.UNAVAILABLE)
                             for h in row))

    def test_xlsx_has_exact_locked_38_column_schema_and_research_only_trace(self):
        report, trace, _ = market_report.build_report([runtime_row()], self.archive)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.xlsx"
            market_report.write_xlsx(path, report)
            workbook = load_workbook(path, read_only=True, data_only=True)
            sheet = workbook["Oracle V1.6 Output"]
            self.assertEqual([cell.value for cell in sheet[1]], market_report.HEADERS)
            self.assertEqual(sheet.max_column, 38)
            workbook.close()
        self.assertEqual(trace[0]["production_eligible"], "NO")
        self.assertEqual(trace[0]["betting_eligible"], "NO")
        self.assertEqual(trace[0]["history_cutoff_rule"], "STRICTLY_BEFORE_FIXTURE_KICKOFF")

    def test_workbook_includes_expanded_evidence_tabs_without_changing_main_schema(self):
        prior = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                            season="S1", league="L1")
        report, trace, _ = market_report.build_report(
            [runtime_row()], self.archive + [prior]
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "expanded.xlsx"
            market_report.write_xlsx(path, report, trace, {
                "archive_match_records": 10,
                "field_nonempty_counts": {"homeGoalCount": 8, "awayGoalCount": 7}
            }, goal_market_rows=[{
                "fixture_id": "F100", "provider_season_id": "S1",
                "home_team_id": "H", "away_team_id": "A",
                "forecast_status": "EXPERIMENTAL_UNCALIBRATED",
                "model_id": "GOAL_POISSON_SHRUNK_V0.1_RESEARCH_ONLY",
                "over15_probability_pct": 76.2, "over25_probability_pct": 54.1,
                "under45_probability_pct": 91.0, "home_over15_probability_pct": 48.3,
                "away_over15_probability_pct": 39.2, "home_lambda": 1.6,
                "away_lambda": 1.2, "home_overall_n": 5, "away_overall_n": 4,
                "league_prior_n": 31, "home_lambda_source": "VENUE",
                "away_lambda_source": "OVERALL_FALLBACK", "blocked_reason": "",
                "production_eligible": "NO", "betting_eligible": "NO"
            }])
            workbook = load_workbook(path, read_only=True, data_only=True)
            self.assertEqual(workbook["Oracle V1.6 Output"].max_column, 38)
            self.assertGreater(workbook["Market Intelligence"].max_column, 38)
            decision = workbook["Market Intelligence"]
            decision_headers = [cell.value for cell in decision[1]]
            self.assertIn("Research Over 1.5 %", decision_headers)
            self.assertIn("Home Last-5 Form", decision_headers)
            self.assertIn("Schedule Reconciliation", decision_headers)
            decision_values = dict(zip(decision_headers, [cell.value for cell in decision[2]]))
            self.assertEqual(decision_values["BTTS Yes"], "58.21")
            self.assertEqual(decision_values["Research Over 1.5 %"], 76.2)
            self.assertEqual(decision_values["Goal Research Status"], "EXPERIMENTAL_UNCALIBRATED")
            self.assertEqual(decision_values["Production Eligible"], "NO")
            self.assertEqual(decision_values["Betting Eligible"], "NO")
            self.assertEqual(decision_values["Home Last-5 Form"], "WWDWW")
            for sheet in ("H2H Intelligence", "Team Form Evidence", "Goal Intelligence",
                          "Market Data Coverage", "Archive Field Coverage",
                          "Data Quality & Risk", "Definitions & Governance"):
                self.assertIn(sheet, workbook.sheetnames)
            self.assertGreaterEqual(workbook["H2H Intelligence"].max_row, 2)
            self.assertEqual(workbook["Archive Field Coverage"].max_row, 3)
            goal_sheet = workbook["Goal Intelligence"]
            self.assertIn("HISTORICAL_EMPIRICAL_RATE_NOT_PREDICTION_PROBABILITY",
                          [cell.value for row in goal_sheet.iter_rows(min_row=2, max_row=2) for cell in row])
            goal_headers = [cell.value for cell in goal_sheet[1]]
            self.assertIn("home_last5_goals_scored_avg", goal_headers)
            self.assertIn("home_last5_goals_conceded_avg", goal_headers)
            self.assertIn("home_at_home_goals_scored_avg", goal_headers)
            self.assertIn("away_away_goals_conceded_avg", goal_headers)
            goal_values = dict(zip(goal_headers, [cell.value for cell in goal_sheet[2]]))
            self.assertEqual(goal_values["home_last5_goals_scored_avg"], "2.00")
            self.assertEqual(goal_values["home_last5_goals_conceded_avg"], trace[0]["home_form_ga_avg"])
            self.assertEqual(goal_values["home_at_home_goals_scored_avg"], trace[0]["home_at_home_avg_goals_for"])
            workbook.close()

    def test_duplicate_runtime_keys_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "Duplicate runtime exact key"):
            market_report.build_report([runtime_row(), runtime_row()], self.archive)

    def test_duplicate_archive_key_is_not_silently_joined(self):
        duplicate = dict(self.archive[-1])
        joined, missing, duplicate_keys = market_report.exact_join(
            [runtime_row()], self.archive + [duplicate]
        )
        self.assertEqual(joined, {})
        self.assertEqual(missing[0][1], "DUPLICATE_ARCHIVE_MATCH")
        self.assertTrue(duplicate_keys)

    def test_missing_identity_is_quarantined_not_name_matched(self):
        row = dict(runtime_row(), provider_season_id="")
        joined, missing, _ = market_report.exact_join([row], self.archive)
        self.assertEqual(joined, {})
        self.assertEqual(missing[0][1], "MISSING_COMPOSITE_IDENTITY")


if __name__ == "__main__":
    unittest.main()
