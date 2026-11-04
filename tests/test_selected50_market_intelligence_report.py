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


def archive_row(fid, date, home_id, away_id, hg, ag, season="S1", league="L1", selected_id="S1", provider_competition_id="L1"):
    return {
        "provider_season_id": season, "provider_league_id": provider_competition_id, "selected_id": selected_id,
        "selected_country": ("Testland" if selected_id else "") if selected_id != "OTHER" else "Elsewhere",
        "selected_competition_name": ("Test League" if selected_id else "") if selected_id != "OTHER" else "Foreign League",
        "fixture_id": fid,
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


def snapshot_row(no_home_away="1"):
    return {
        "snapshot_row_number": "7", "snapshot_file_sha256": "snapshot-sha",
        "source_archive_sha256": "archive-sha",
        "snapshot_retrieved_utc": "2026-10-31T06:02:13.776050+00:00",
        "selected_season_id": "S1", "fixture_id": "F100",
        "home_team_provider_id": "H", "away_team_provider_id": "A",
        "no_home_away": no_home_away,
    }


def snapshot_provenance():
    return {
        "snapshot_file_sha256": "snapshot-sha",
        "snapshot_retrieved_utc": "2026-10-31T06:02:13.776050+00:00",
        "snapshot_artifact_id": "SNAP-1", "snapshot_run_id": "RUN-1",
        "snapshot_fixture_rows": 1,
    }


class Selected50MarketIntelligenceTests(unittest.TestCase):
    def test_parse_dt_requires_explicit_timezone(self):
        self.assertIsNone(market_report.parse_dt("2026-10-31T18:00:00"))
        self.assertIsNotNone(market_report.parse_dt("2026-10-31T18:00:00Z"))

    def test_archive_actual_fields_require_settlement_and_respect_no_home_away(self):
        neutral = archive_row("NEUTRAL", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1)
        neutral["no_home_away"] = "1"
        actuals = market_report.archive_actual_fields(neutral)
        self.assertEqual(actuals["settlement_status"], "SETTLED_VERIFIED_NO_HOME_AWAY")
        self.assertEqual(actuals["actual_home_goals"], "")
        self.assertEqual(actuals["actual_away_goals"], "")
        self.assertEqual(actuals["actual_total_goals"], 3)
        self.assertEqual(actuals["actual_match_result"], "NOT_AVAILABLE_NO_HOME_AWAY")
        scheduled = archive_row("SCHEDULED", "2025-08-02T12:00:00+00:00", "H", "A", "", "")
        scheduled["status_raw"] = "scheduled"
        scheduled_actuals = market_report.archive_actual_fields(scheduled)
        self.assertEqual(scheduled_actuals["settlement_status"], "NOT_SETTLED")
        self.assertEqual(scheduled_actuals["actual_total_goals"], "")

    def test_archive_history_ignores_naive_kickoff_timestamps(self):
        naive = archive_row("NAIVE", "2025-08-01T12:00:00", "H", "A", 2, 1)
        by_team, by_season, by_pair, _, _, qa = market_report.build_indexes([naive])
        self.assertEqual(sum(len(rows) for rows in by_team.values()), 0)
        self.assertEqual(sum(len(rows) for rows in by_season.values()), 0)
        self.assertEqual(sum(len(rows) for rows in by_pair.values()), 0)

    def test_archive_index_qa_accounts_for_invalid_and_missing_exact_identity_fields(self):
        naive = archive_row("NAIVE", "2025-08-01T12:00:00", "H", "A", 2, 1)
        no_fixture = archive_row("", "2025-08-02T12:00:00+00:00", "H", "A", 1, 0)
        no_home_id = archive_row("NO-HOME", "2025-08-03T12:00:00+00:00", "", "A", 1, 0)
        same_team = archive_row("SAME", "2025-08-04T12:00:00+00:00", "H", "H", 1, 0)
        by_team, by_season, by_pair, _, _, qa = market_report.build_indexes(
            [naive, no_fixture, no_home_id, same_team]
        )
        self.assertEqual(qa["candidate_rows"], 4)
        self.assertEqual(qa["invalid_or_naive_kickoff_rows"], 1)
        self.assertEqual(qa["missing_fixture_id_rows"], 1)
        self.assertEqual(qa["missing_home_team_id_rows"], 1)
        self.assertEqual(qa["same_home_away_team_id_rows"], 1)
        self.assertEqual(qa["rows_indexed"], 0)
        self.assertEqual(qa["rows_quarantined"], 4)
        self.assertEqual(sum(len(rows) for rows in by_team.values()), 0)
        self.assertEqual(sum(len(rows) for rows in by_season.values()), 0)
        self.assertEqual(sum(len(rows) for rows in by_pair.values()), 0)

    def test_archive_index_deduplicates_exact_rows_and_quarantines_conflicting_fixture_ids(self):
        exact = archive_row("DUP", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1)
        exact_duplicate = dict(exact)
        conflict_a = archive_row("CONFLICT", "2025-08-02T12:00:00+00:00", "H", "B", 2, 0)
        conflict_b = archive_row("CONFLICT", "2025-08-02T12:00:00+00:00", "H", "B", 1, 0)
        by_team, by_season, by_pair, duplicates, h2h_qa, qa = market_report.build_indexes(
            [exact, exact_duplicate, conflict_a, conflict_b]
        )
        self.assertEqual(qa["exact_duplicate_rows_deduplicated"], 1)
        self.assertEqual(qa["conflicting_fixture_identity_groups"], 1)
        self.assertEqual(qa["conflicting_fixture_identity_rows_quarantined"], 2)
        self.assertEqual(qa["rows_indexed"], 1)
        self.assertEqual(duplicates, 2)
        self.assertEqual(sum(len(rows) for rows in by_season.values()), 1)

    def test_snapshot_orientation_uses_exact_ordered_identity_and_quarantines_unknowns(self):
        runtime = runtime_row()
        archive_summary = {"archive_sha256": "archive-sha"}
        orientation, qa = market_report.build_snapshot_orientation_map(
            [runtime], [snapshot_row("1")], snapshot_provenance(), archive_summary
        )
        item = orientation[("S1", "F100", "H", "A")]
        self.assertEqual(item["snapshot_evidence_status"], "EXACT_SNAPSHOT_MATCH")
        self.assertEqual(item["snapshot_no_home_away_flag"], "1")
        self.assertEqual(item["fixture_orientation_status"], "NO_HOME_AWAY_DISTINCTION")
        self.assertEqual(item["home_away_market_review_status"],
                         "REVIEW_REQUIRED_NO_HOME_AWAY_DISTINCTION")
        self.assertEqual(qa["exact_snapshot_matches"], 1)
        self.assertEqual(qa["no_home_away_flagged"], 1)
        self.assertEqual(qa["orientation_unknown_rows"], 0)

        unknown, unknown_qa = market_report.build_snapshot_orientation_map(
            [runtime], [snapshot_row("unknown")], snapshot_provenance(), archive_summary
        )
        self.assertEqual(unknown[("S1", "F100", "H", "A")]["fixture_orientation_status"],
                         "ORIENTATION_UNKNOWN")
        self.assertEqual(unknown_qa["orientation_unknown_rows"], 1)

        swapped = dict(runtime, home_team_provider_id="A", away_team_provider_id="H")
        swapped_map, swapped_qa = market_report.build_snapshot_orientation_map(
            [swapped], [snapshot_row("1")], snapshot_provenance(), archive_summary
        )
        self.assertEqual(swapped_map[("S1", "F100", "A", "H")]["fixture_orientation_status"],
                         "ORIENTATION_UNKNOWN")
        self.assertEqual(swapped_qa["exact_snapshot_matches"], 0)

    def test_snapshot_orientation_release_gate_requires_accounting_and_allows_explicit_review_exceptions(self):
        runtime = runtime_row()
        archive_summary = {"archive_sha256": "archive-sha"}
        _, qa = market_report.build_snapshot_orientation_map(
            [runtime], [snapshot_row("1")], snapshot_provenance(), archive_summary
        )
        self.assertTrue(market_report.require_snapshot_orientation_qa(qa))

        _, unknown_flag_qa = market_report.build_snapshot_orientation_map(
            [runtime], [snapshot_row("unknown")], snapshot_provenance(), archive_summary
        )
        self.assertEqual(unknown_flag_qa["status"], "REVIEW_REQUIRED_SNAPSHOT_EVIDENCE_GAPS")
        self.assertEqual(unknown_flag_qa["unknown_snapshot_flag_rows"], 1)
        self.assertTrue(market_report.require_snapshot_orientation_qa(unknown_flag_qa))

        missing_row = dict(snapshot_row("0"), fixture_id="NOT-THE-RUNTIME-FIXTURE")
        missing, missing_qa = market_report.build_snapshot_orientation_map(
            [runtime], [missing_row], snapshot_provenance(), archive_summary
        )
        item = missing[("S1", "F100", "H", "A")]
        self.assertEqual(item["snapshot_evidence_status"], "MISSING_FROM_FRESH_SNAPSHOT")
        self.assertEqual(item["home_away_market_review_status"], "REVIEW_REQUIRED_MISSING_FROM_FRESH_SNAPSHOT")
        self.assertEqual(missing_qa["missing_snapshot_rows"], 1)
        self.assertEqual(missing_qa["rows_accounted_for"], 1)
        self.assertTrue(market_report.require_snapshot_orientation_qa(missing_qa))

        duplicated, duplicate_qa = market_report.build_snapshot_orientation_map(
            [runtime], [snapshot_row("0"), snapshot_row("1")],
            dict(snapshot_provenance(), snapshot_fixture_rows=2), archive_summary
        )
        self.assertEqual(duplicated[("S1", "F100", "H", "A")]["snapshot_evidence_status"],
                         "DUPLICATE_SNAPSHOT_MATCH")
        self.assertEqual(duplicate_qa["duplicate_snapshot_match_rows"], 1)
        self.assertTrue(market_report.require_snapshot_orientation_qa(duplicate_qa))

        inconsistent = dict(qa, no_home_away_flagged=0)
        with self.assertRaisesRegex(ValueError, "SNAPSHOT_ORIENTATION_QA_BLOCKED"):
            market_report.require_snapshot_orientation_qa(inconsistent)
        unaccounted = dict(qa, rows_accounted_for=0, all_runtime_rows_accounted_for=False)
        with self.assertRaisesRegex(ValueError, "SNAPSHOT_ORIENTATION_QA_BLOCKED"):
            market_report.require_snapshot_orientation_qa(unaccounted)

    def test_runtime_feature_block_audit_counts_sides_without_relaxing_gate(self):
        rows = [
            dict(runtime_row(), feature_support_status="BLOCKED_MISSING_REQUIRED_FEATURES",
                 prediction_block_reason="BLOCKED_MISSING_REQUIRED_FEATURES",
                 missing_required_features="home_gf5;pair_btts_mean",
                 home_recent5_n="4", away_recent5_n="5"),
            dict(runtime_row(), fixture_id="F200", feature_support_status="BLOCKED_MISSING_REQUIRED_FEATURES",
                 prediction_block_reason="BLOCKED_MISSING_REQUIRED_FEATURES",
                 missing_required_features="home_gf5;away_gf5",
                 home_recent5_n="3", away_recent5_n="4"),
            dict(runtime_row(), fixture_id="F300", feature_support_status="PASS_ALL_20_REQUIRED_FEATURES",
                 home_recent5_n="5", away_recent5_n="5"),
        ]
        audit, qa = market_report.build_runtime_feature_block_audit(rows)
        self.assertEqual(len(audit), 3)
        self.assertEqual(qa["blocked_fixture_rows"], 2)
        self.assertEqual(qa["blocked_team_side_histories"], 3)
        self.assertEqual(qa["home_side_histories_below_5"], 2)
        self.assertEqual(qa["away_side_histories_below_5"], 1)
        self.assertEqual(qa["side_history_sample_n_counts"], {"3": 1, "4": 2})
        self.assertTrue(all(row["production_eligible"] == "NO" for row in audit))
        self.assertTrue(all(row["betting_eligible"] == "NO" for row in audit))
        self.assertTrue(market_report.require_runtime_feature_block_audit(audit, qa))
        with self.assertRaisesRegex(ValueError, "RUNTIME_FEATURE_BLOCK_AUDIT_RECONCILIATION_FAILED"):
            market_report.require_runtime_feature_block_audit(audit[:-1], qa)

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

    def test_xg_audit_exact_identity_and_quarantine(self):
        target = dict(self.archive[-1],
            home_xg_prematch_source_field="team_a_xg_prematch",
            home_xg_prematch_raw="1.23", home_xg_prematch_value=1.23,
            away_xg_prematch_source_field="team_b_xg_prematch",
            away_xg_prematch_raw="0.87", away_xg_prematch_value=0.87,
            total_xg_prematch_source_field="total_xg_prematch",
            total_xg_prematch_raw="2.10", total_xg_prematch_value=2.10,
            xg_capture_time_utc="",
            xg_temporal_provenance_status="UNVERIFIED_NO_CAPTURE_TIMESTAMP")
        rows = market_report.build_xg_audit([runtime_row()], self.archive[:-1] + [target])
        self.assertEqual(rows[0]["join_status"], "PASS_EXACT_COMPOSITE_IDENTITY")
        self.assertEqual(rows[0]["home_xg_numeric"], 1.23)
        self.assertEqual(rows[0]["capture_time_utc"], "")
        self.assertEqual(rows[0]["prediction_use_status"], "QUARANTINED_RESEARCH_AUDIT_ONLY")
        self.assertEqual(rows[0]["prediction_eligible"], "NO")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "xg.xlsx"
            market_report.write_xlsx(path, [], [], {}, [], rows)
            workbook = load_workbook(path, read_only=True, data_only=True)
            sheet = workbook["xG Evidence Audit"]
            self.assertEqual(sheet.max_row, 2)
            self.assertIn("QUARANTINED_RESEARCH_AUDIT_ONLY",
                          [cell.value for cell in sheet[2]])
            self.assertEqual(workbook["Oracle V1.6 Output"].max_column, 38)
            workbook.close()
        swapped = dict(runtime_row(), home_team_provider_id="A", away_team_provider_id="H")
        self.assertEqual(market_report.build_xg_audit([swapped], self.archive)[0]["join_status"],
                         "BLOCKED_NO_EXACT_ARCHIVE_MATCH")

    def test_xg_audit_blocks_missing_and_duplicate_identity(self):
        missing = dict(runtime_row(), provider_season_id="")
        self.assertEqual(market_report.build_xg_audit([missing], self.archive)[0]["join_status"],
                         "BLOCKED_MISSING_RUNTIME_COMPOSITE_IDENTITY")
        duplicate = dict(self.archive[-1])
        self.assertEqual(market_report.build_xg_audit([runtime_row()], self.archive + [duplicate])[0]["join_status"],
                         "QUARANTINED_DUPLICATE_ARCHIVE_IDENTITY")

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
        self.assertEqual(trace[0]["schedule_reconciliation_status"], "REVIEW_REQUIRED")
        self.assertEqual(trace[0]["schedule_delta_minutes_archive_minus_runtime"], -1)
        queue = summary["schedule_reconciliation_queue"]
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0]["status"], "REVIEW_REQUIRED")
        self.assertEqual(queue[0]["fixture_identity"], "S1|F100|H|A")
        self.assertEqual(queue[0]["league"], "Test League")
        self.assertEqual(queue[0]["delta_minutes_archive_minus_runtime"], -1)
        self.assertEqual(summary["schedule_reconciliation_queue_rows"], 1)
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

    def test_h2h_average_uses_only_verified_pre_cutoff_meetings(self):
        _, trace, _ = market_report.build_report([runtime_row()], self.archive)
        self.assertEqual(market_report.h2h_average_total_goals(trace[0]), 4.0)

    def test_h2h_average_is_explicit_when_no_verified_meetings_exist(self):
        self.assertEqual(market_report.h2h_average_total_goals({"h2h_meetings_detail": "[]"}),
                         "NO_VERIFIED_PRIOR_H2H")

    def test_h2h_does_not_bridge_changed_provider_team_ids_by_matching_names(self):
        prior = archive_row("OLD-ID-MEETING", "2025-08-01T12:00:00+00:00",
                            "OLD-HOME-ID", "OLD-AWAY-ID", 2, 1,
                            season="S0", selected_id="S1")
        prior["home_team"] = "Home FC"
        prior["away_team"] = "Away FC"
        target = archive_row("F100", "2026-10-31T18:00:00+00:00",
                             "H", "A", 0, 0, season="S1", selected_id="S1")
        report, trace, summary = market_report.build_report([runtime_row()], [prior, target])
        self.assertEqual(trace[0]["h2h_n"], 0)
        self.assertEqual(trace[0]["h2h_match_basis"], "NO_VERIFIED_PAIR_MATCH")
        self.assertNotIn("OLD-ID-MEETING", trace[0]["h2h_source_fixture_ids"])
        self.assertEqual(report[0]["H2H Last 5 Summary"], "NO_VERIFIED_PRIOR_H2H")
        self.assertEqual(summary["h2h_identity_policy"], "EXACT_UNORDERED_PROVIDER_TEAM_ID_PAIR_ONLY")
        self.assertIn("NAIVE_KICKOFFS_REJECTED", summary["archive_timestamp_policy"])

    def test_h2h_does_not_bridge_changed_ids_across_selected_divisions_by_name(self):
        prior = archive_row("OLD-DIVISION-ID", "2025-08-01T12:00:00+00:00",
                            "OLD-HOME-ID", "OLD-AWAY-ID", 2, 1,
                            season="S2", league="Lower Division", selected_id="S2")
        prior["home_team"] = "Home FC"
        prior["away_team"] = "Away FC"
        target = archive_row("F100", "2026-10-31T18:00:00+00:00",
                             "H", "A", 0, 0, season="S1", selected_id="S1")
        report, trace, _ = market_report.build_report([runtime_row()], [prior, target])
        self.assertEqual(trace[0]["h2h_n"], 0)
        self.assertEqual(trace[0]["h2h_match_basis"], "NO_VERIFIED_PAIR_MATCH")
        self.assertEqual(report[0]["H2H Last 5 Summary"], "NO_VERIFIED_PRIOR_H2H")

    def test_h2h_uses_prior_exact_ids_even_when_names_differ_and_a_future_name_pair_exists(self):
        future_name_match = archive_row("FUTURE-NAME", "2026-11-02T12:00:00+00:00",
                                        "OLD-H", "OLD-A", 1, 0,
                                        season="S0", selected_id="S1")
        future_name_match["home_team"] = "Home FC"
        future_name_match["away_team"] = "Away FC"
        prior_id_match = archive_row("PRIOR-ID", "2025-08-01T12:00:00+00:00",
                                     "H", "A", 2, 1,
                                     season="S0", selected_id="S1")
        prior_id_match["home_team"] = "Home Club Historic"
        prior_id_match["away_team"] = "Away Club Historic"
        target = archive_row("F100", "2026-10-31T18:00:00+00:00",
                             "H", "A", 0, 0, season="S1", selected_id="S1")
        report, trace, _ = market_report.build_report([runtime_row()], [
            future_name_match, prior_id_match, target
        ])
        self.assertEqual(trace[0]["h2h_n"], 1)
        self.assertEqual(trace[0]["h2h_match_basis"], "EXACT_PROVIDER_TEAM_IDS")
        self.assertIn("PRIOR-ID", trace[0]["h2h_source_fixture_ids"])
        self.assertEqual(report[0]["H2H Last 5 Summary"], "W")

    def test_h2h_name_matching_is_not_fuzzy(self):
        prior = archive_row("OLD-ID-MEETING", "2025-08-01T12:00:00+00:00",
                            "OLD-HOME-ID", "OLD-AWAY-ID", 2, 1,
                            season="S0", selected_id="S1")
        prior["home_team"] = "Home FC Reserves"
        prior["away_team"] = "Away FC"
        target = archive_row("F100", "2026-10-31T18:00:00+00:00",
                             "H", "A", 0, 0, season="S1", selected_id="S1")
        report, trace, _ = market_report.build_report([runtime_row()], [prior, target])
        self.assertEqual(trace[0]["h2h_n"], 0)
        self.assertEqual(trace[0]["h2h_match_basis"], "NO_VERIFIED_PAIR_MATCH")

    def test_h2h_uses_exact_selected_manifest_scope_across_season_scoped_provider_ids(self):
        prior = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                            season="S1", league="L1", selected_id="S2",
                            provider_competition_id="S1")
        target_archive = archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0,
                                     season="S2", league="L1", selected_id="S2",
                                     provider_competition_id="S2")
        target_runtime = dict(runtime_row(), provider_season_id="S2", selected_id="S2")
        report, trace, _ = market_report.build_report(
            [target_runtime], [prior, target_archive]
        )
        self.assertEqual(trace[0]["h2h_n"], 1)
        self.assertEqual(trace[0]["h2h_scope"], "EXACT_SELECTED50_COUNTRY_SCOPE")
        self.assertIn("OLD1", trace[0]["h2h_source_fixture_ids"])
        self.assertEqual(report[0]["H2H Last 5 Summary"], "W")


    def test_h2h_deduplicates_repeated_fixture_ids_across_season_folders(self):
        prior = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                            season="S1", selected_id="S1", provider_competition_id="S1")
        duplicate = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                                season="S2", selected_id="S1", provider_competition_id="S2")
        target = archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0,
                             season="S1", selected_id="S1")
        report, trace, summary = market_report.build_report([runtime_row()], [prior, duplicate, target])
        self.assertEqual(trace[0]["h2h_n"], 1)
        self.assertEqual(summary["h2h_history_deduplication"]["exact_duplicate_rows_removed"], 1)

    def test_h2h_quarantines_conflicting_fixture_id_duplicates(self):
        first = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                            season="S1", selected_id="S1")
        conflicting = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 4, 0,
                                  season="S2", selected_id="S1")
        target = archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0,
                             season="S1", selected_id="S1")
        report, trace, summary = market_report.build_report([runtime_row()], [first, conflicting, target])
        self.assertEqual(trace[0]["h2h_n"], 0)
        self.assertEqual(summary["h2h_history_deduplication"]["conflicting_fixture_id_groups_quarantined"], 1)

    def test_h2h_marks_unoriented_history_without_inventing_home_away_result(self):
        prior = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                            season="S1", selected_id="S1")
        prior["no_home_away"] = 1
        target = archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0,
                             season="S1", selected_id="S1")
        report, trace, _ = market_report.build_report([runtime_row()], [prior, target])
        meetings = json.loads(trace[0]["h2h_meetings_detail"])
        self.assertEqual(meetings[0]["no_home_away"], 1)
        self.assertEqual(meetings[0]["result_current_home_perspective"], "N/A")
        self.assertEqual(report[0]["H2H Last 5 Summary"], "N/A")

    def test_h2h_includes_prior_meetings_from_another_selected_division_in_same_country(self):
        prior = archive_row("OLD-DIVISION", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                            season="S2", league="Lower Division", selected_id="S2",
                            provider_competition_id="S2")
        target = archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0,
                             season="S1", league="Top Division", selected_id="S1")
        report, trace, _ = market_report.build_report([runtime_row()], [prior, target])
        self.assertEqual(trace[0]["h2h_n"], 1)
        self.assertEqual(trace[0]["h2h_scope"], "EXACT_SELECTED50_COUNTRY_SCOPE")
        self.assertEqual(trace[0]["h2h_scope_id"], "Testland")
        meetings = json.loads(trace[0]["h2h_meetings_detail"])
        self.assertEqual(meetings[0]["meeting_selected_id"], "S2")
        self.assertEqual(meetings[0]["selected_competition_name"], "Test League")
        self.assertEqual(report[0]["H2H Last 5 Summary"], "W")

    def test_h2h_does_not_mix_same_team_pair_from_another_country(self):
        foreign = archive_row("FOREIGN", "2025-08-01T12:00:00+00:00", "H", "A", 5, 0,
                              season="FOREIGN-S", league="Foreign", selected_id="OTHER",
                              provider_competition_id="OTHER")
        target_archive = archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0,
                                     season="S1", selected_id="S1", provider_competition_id="S1")
        report, trace, _ = market_report.build_report([runtime_row()], [foreign, target_archive])
        self.assertEqual(trace[0]["h2h_n"], 0)
        self.assertEqual(report[0]["H2H Last 5 Summary"], "NO_VERIFIED_PRIOR_H2H")

    def test_h2h_requires_selected_manifest_scope_and_does_not_fallback_to_season_id(self):
        unmapped_prior = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                                     season="S1", selected_id="")
        target_archive = archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0,
                                     season="S1", selected_id="S1")
        report, trace, _ = market_report.build_report([runtime_row()], [unmapped_prior, target_archive])
        self.assertEqual(trace[0]["h2h_n"], 0)
        self.assertEqual(trace[0]["h2h_scope"], "EXACT_SELECTED50_COUNTRY_SCOPE")
        self.assertEqual(report[0]["H2H Last 5 Summary"], "NO_VERIFIED_PRIOR_H2H")

    def test_h2h_meeting_retains_source_season_under_selected_competition_scope(self):
        prior = archive_row("OLD1", "2025-08-01T12:00:00+00:00", "H", "A", 2, 1,
                            season="S1", league="L1", selected_id="S2",
                            provider_competition_id="S1")
        target_archive = archive_row("F100", "2026-10-31T18:00:00+00:00", "H", "A", 0, 0,
                                     season="S2", league="L1", selected_id="S2",
                                     provider_competition_id="S2")
        target_runtime = dict(runtime_row(), provider_season_id="S2", selected_id="S2")
        report, trace, _ = market_report.build_report([target_runtime], [prior, target_archive])
        self.assertEqual(trace[0]["h2h_scope"], "EXACT_SELECTED50_COUNTRY_SCOPE")
        meetings = json.loads(trace[0]["h2h_meetings_detail"])
        self.assertEqual(meetings[0]["provider_season_id"], "S1")
        self.assertEqual(report[0]["H2H Last 5 Summary"], "W")

    def test_venue_split_form_is_exposed_in_evidence_trace(self):
        _, trace, _ = market_report.build_report([runtime_row()], self.archive)
        self.assertEqual(trace[0]["home_at_home_form_n"], 4)
        self.assertEqual(trace[0]["away_away_form_n"], 3)
        self.assertEqual(trace[0]["home_at_home_form"], "WDWW")
        self.assertEqual(trace[0]["away_away_form"], "WLL")

    def test_no_home_away_history_is_excluded_from_venue_splits_but_retained_for_overall_form(self):
        neutral = archive_row("F8", "2026-10-27T12:00:00+00:00", "H", "R", 1, 0)
        neutral["no_home_away"] = "1"
        _, trace, summary = market_report.build_report([runtime_row()], self.archive + [neutral])
        self.assertEqual(trace[0]["home_form_n"], 5)
        self.assertEqual(trace[0]["home_at_home_form_n"], 4)
        self.assertEqual(trace[0]["home_at_home_no_home_away_excluded_n"], 1)
        self.assertEqual(summary["archive_index_gate"], "PASS")

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
            }], xg_audit_rows=market_report.build_xg_audit(
                [runtime_row()], self.archive + [prior], trace
            ))
            workbook = load_workbook(path, read_only=True, data_only=True)
            self.assertEqual(workbook["Oracle V1.6 Output"].max_column, 38)
            schema = json.loads((SCRIPT.parents[1] / "config" / "omi_market_intelligence_schema_v1.json").read_text(encoding="utf-8"))
            self.assertEqual(workbook["Market Intelligence"].max_column, 95)
            decision = workbook["Market Intelligence"]
            decision_headers = [cell.value for cell in decision[1]]
            self.assertEqual(decision_headers, schema["headers"])
            self.assertIn("Research Over 1,5 %", decision_headers)
            self.assertIn("Home Last-5 Form", decision_headers)
            self.assertIn("Schedule Reconciliation", decision_headers)
            decision_values = dict(zip(decision_headers, [cell.value for cell in decision[2]]))
            self.assertEqual(decision_values["BTTS Yes"], "58.21")
            self.assertEqual(decision_values["Research Over 1,5 %"], 76.2)
            self.assertEqual(decision_values["Goal Research Status"], "EXPERIMENTAL_UNCALIBRATED")
            self.assertEqual(decision_values["Production Eligible"], "NO")
            self.assertEqual(decision_values["Betting Eligible"], "NO")
            self.assertEqual(decision_values["Home Last-5 Form"], "WWDWW")
            self.assertEqual(decision_values["H2H Avg Total Goals"], 3.5)
            self.assertEqual(decision_values["H2H Avg Total Goals2"], 3.5)
            self.assertEqual(decision_values["actual_home_goals"], 0)
            self.assertEqual(decision_values["actual_away_goals"], 0)
            self.assertEqual(decision_values["actual_total_goals"], 0)
            self.assertEqual(decision_values["actual_match_result"], "DRAW")
            self.assertEqual(decision_values["actual_btts"], "NO")
            self.assertEqual(decision_values["actual_over_1_5"], "NO")
            self.assertEqual(decision_values["actual_over_2_5"], "NO")
            self.assertEqual(decision_values["actual_under_4_5"], "YES")
            self.assertEqual(decision_values["settlement_status"], "SETTLED_VERIFIED_EXACT_ID")
            self.assertEqual(decision_values["provider_match_status"], "complete")
            self.assertEqual(workbook["OMI Report"].cell(row=2, column=2).value, "Oracle Market Intelligence (OMI) Report")
            for sheet in ("OMI Report", "Visual Intelligence", "H2H Intelligence",
                          "Team Form Evidence", "Goal Intelligence", "Goal Market Research",
                          "xG Evidence Audit", "Schedule Reconciliation", "Market Data Coverage",
                          "Archive Field Coverage", "Data Quality & Risk", "Definitions & Governance"):
                self.assertIn(sheet, workbook.sheetnames)
            expected_context = ["Fixture Date", "League", "Fixture"]
            for sheet in ("H2H Intelligence", "Team Form Evidence", "Data Quality & Risk",
                          "Goal Intelligence", "Goal Market Research", "xG Evidence Audit"):
                self.assertEqual([cell.value for cell in workbook[sheet][1][:3]], expected_context)
                self.assertGreaterEqual(workbook[sheet].max_row, 2)
                context_values = [cell.value for cell in workbook[sheet][2][:3]]
                self.assertEqual(context_values, [
                    "2026-10-31T18:00:00+00:00", "Test League", "Home FC vs Away FC"
                ])
            self.assertEqual(workbook["Market Data Coverage"][1][0].value, "field")
            self.assertEqual(workbook["Archive Field Coverage"][1][0].value, "raw_source_field")
            self.assertEqual(workbook["Schedule Reconciliation"].max_row, 1)
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

    def test_schedule_reconciliation_queue_exposes_full_conflict_evidence(self):
        changed = dict(self.archive[-1],
            kickoff_utc="2026-10-31T17:59:00+00:00",
            source_file="england/2026/matches.json", source_row="88")
        report, trace, summary = market_report.build_report(
            [runtime_row()], self.archive[:-1] + [changed]
        )
        queue = market_report.build_schedule_reconciliation_queue(trace)
        self.assertEqual(len(queue), 1)
        item = queue[0]
        self.assertEqual(item["status"], "REVIEW_REQUIRED")
        self.assertEqual(item["fixture_identity"], "S1|F100|H|A")
        self.assertEqual(item["league"], "Test League")
        self.assertEqual(item["fixture"], "Home FC vs Away FC")
        self.assertEqual(item["runtime_kickoff_utc"], "2026-10-31T18:00:00+00:00")
        self.assertEqual(item["archive_kickoff_utc"], "2026-10-31T17:59:00+00:00")
        self.assertEqual(item["delta_minutes_archive_minus_runtime"], -1)
        self.assertEqual(item["archive_source_file"], "england/2026/matches.json")
        self.assertEqual(item["archive_source_row"], "88")
        self.assertIn("NO_AUTO_CORRECTION", item["resolution_action"])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schedule.xlsx"
            xg = market_report.build_xg_audit([runtime_row()], self.archive[:-1] + [changed], trace)
            market_report.write_xlsx(path, report, trace, {}, xg_audit_rows=xg)
            workbook = load_workbook(path, read_only=True, data_only=True)
            goal_headers = [cell.value for cell in workbook["Goal Market Research"][1]]
            self.assertEqual(goal_headers[:3], ["Fixture Date", "League", "Fixture"])
            self.assertIn("fixture_id", goal_headers)
            self.assertIn("forecast_status", goal_headers)
            sheet = workbook["Schedule Reconciliation"]
            headers = [cell.value for cell in sheet[1]]
            values = dict(zip(headers, [cell.value for cell in sheet[2]]))
            self.assertEqual(values["status"], "REVIEW_REQUIRED")
            self.assertEqual(values["fixture_identity"], "S1|F100|H|A")
            self.assertEqual(values["delta_minutes_archive_minus_runtime"], -1)
            self.assertEqual(values["archive_source_file"], "england/2026/matches.json")
            self.assertEqual(values["archive_source_row"], "88")
            quality = workbook["Data Quality & Risk"]
            quality_headers = [cell.value for cell in quality[1]]
            quality_values = dict(zip(quality_headers, [cell.value for cell in quality[2]]))
            self.assertEqual(quality_values["schedule_reconciliation_status"], "REVIEW_REQUIRED")
            self.assertEqual(quality_values["runtime_kickoff_utc"], item["runtime_kickoff_utc"])
            self.assertEqual(quality_values["archive_kickoff_utc"], item["archive_kickoff_utc"])
            self.assertEqual(quality_values["schedule_delta_minutes_archive_minus_runtime"], -1)
            workbook.close()

    def test_goal_market_context_requires_exact_composite_identity(self):
        report, trace, _ = market_report.build_report([runtime_row()], self.archive)
        mismatched_goal = {
            "provider_season_id": "S2", "fixture_id": "F100",
            "home_team_id": "H", "away_team_id": "A",
            "forecast_status": "EXPERIMENTAL_UNCALIBRATED",
            "production_eligible": "NO", "betting_eligible": "NO"
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "goal-market.xlsx"
            market_report.write_xlsx(path, report, trace, {}, goal_market_rows=[mismatched_goal])
            workbook = load_workbook(path, read_only=True, data_only=True)
            sheet = workbook["Goal Market Research"]
            headers = [cell.value for cell in sheet[1]]
            values = dict(zip(headers, [cell.value for cell in sheet[2]]))
            self.assertEqual(values["Fixture Date"], "NOT_AVAILABLE_EXACT_IDENTITY_CONTEXT_JOIN")
            self.assertEqual(values["League"], "NOT_AVAILABLE_EXACT_IDENTITY_CONTEXT_JOIN")
            self.assertEqual(values["Fixture"], "NOT_AVAILABLE_EXACT_IDENTITY_CONTEXT_JOIN")
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


    def test_50_league_coverage_sheet_includes_no_fixture_groups_and_quarantine(self):
        target = dict(
            self.archive[-1],
            home_xg_prematch_source_field="team_a_xg_prematch",
            home_xg_prematch_raw="1.23",
            home_xg_prematch_value=1.23,
            away_xg_prematch_source_field="team_b_xg_prematch",
            away_xg_prematch_raw="0.87",
            away_xg_prematch_value=0.87,
            total_xg_prematch_source_field="total_xg_prematch",
            total_xg_prematch_raw="2.10",
            total_xg_prematch_value=2.10,
            xg_capture_time_utc="",
            xg_temporal_provenance_status="UNVERIFIED_NO_CAPTURE_TIMESTAMP",
        )
        runtime = dict(runtime_row(), feature_support_status="PASS_ALL_20_REQUIRED_FEATURES",
                       home_recent5_n="5", away_recent5_n="5")
        report, trace, _ = market_report.build_report([runtime], self.archive[:-1] + [target])
        xg = market_report.build_xg_audit([runtime], self.archive[:-1] + [target], trace)
        goals = [{
            "provider_season_id": "S1", "fixture_id": "F100",
            "home_team_id": "H", "away_team_id": "A",
            "forecast_status": "EXPERIMENTAL_UNCALIBRATED",
            "blocked_reason": "", "production_eligible": "NO", "betting_eligible": "NO",
        }]
        schedule = [
            {"selected_id": "S1", "country": "Testland", "competition_name": "Test League",
             "schedule_coverage_status": "FIXTURES_FOUND"},
            {"selected_id": "S2", "country": "Elsewhere", "competition_name": "No Fixtures League",
             "schedule_coverage_status": "NO_FIXTURES_IN_REPORT_WINDOW"},
        ]
        coverage = market_report.build_50_league_coverage_rows(
            schedule, [runtime], report, trace, xg, goals
        )
        self.assertEqual(len(coverage), 2)
        self.assertEqual(len({row["Selected Season ID"] for row in coverage}), 2)
        populated = coverage[0]
        empty = coverage[1]
        self.assertEqual(populated["Selected Season ID"], "S1")
        self.assertEqual(populated["Upcoming Fixtures (Report Window)"], 1)
        self.assertEqual(populated["Exact Archive Joins"], 1)
        self.assertEqual(populated["BTTS Raw Research Predictions"], 1)
        self.assertEqual(populated["Experimental Goal Forecasts"], 1)
        self.assertEqual(populated["Pre-match-labelled xG Rows"], 1)
        self.assertEqual(populated["Verified xG Capture Timestamps"], 0)
        self.assertEqual(populated["Production Eligible YES"], 0)
        self.assertEqual(populated["Betting Eligible YES"], 0)
        self.assertEqual(empty["Selected Season ID"], "S2")
        self.assertEqual(empty["Upcoming Fixtures (Report Window)"], 0)
        self.assertEqual(empty["Fixture Coverage Status"], "NO_FIXTURE_IN_REPORT_WINDOW")
        self.assertEqual(empty["Raw Oracle Prediction Status"], "NO_FIXTURES_TO_SCORE")
        summary_rows = market_report.build_coverage_summary_rows(
            coverage,
            report_summary={
                "report_start_date_utc": "2026-11-06",
                "report_end_date_utc_inclusive": "2026-11-24",
                "report_horizon_days": 19,
            },
        )
        self.assertTrue(any(row["Metric"] == "Report horizon (inclusive calendar days)"
                            and row["Value"] == 19 for row in summary_rows))
        xg_rows = market_report.build_xg_provenance_rows(coverage)
        self.assertTrue(any(row["Metric"] == "Groups with no fixtures in report window"
                            and row["Value"] == 1 for row in summary_rows))
        self.assertTrue(any(row["Control"] == "Point-in-time capture timestamps"
                            and row["Finding"] == "0/1 rows have a verified capture timestamp."
                            for row in xg_rows))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "coverage.xlsx"
            runtime["feature_support_status"] = "PASS_ALL_20_REQUIRED_FEATURES"
            runtime["home_recent5_n"] = "5"
            runtime["away_recent5_n"] = "5"
            orientation, orientation_qa = market_report.build_snapshot_orientation_map(
                [runtime], [snapshot_row("1")], snapshot_provenance(),
                {"archive_sha256": "archive-sha"}
            )
            market_report.write_xlsx(
                path, report, trace, {}, goal_market_rows=goals, xg_audit_rows=xg,
                league_coverage_rows=coverage, coverage_summary_rows=summary_rows,
                xg_provenance_rows=xg_rows, runtime_rows=[runtime],
                snapshot_orientation_by_key=orientation,
            )
            workbook = load_workbook(path, read_only=True, data_only=True)
            self.assertEqual(workbook["Oracle V1.6 Output"].max_column, 38)
            self.assertEqual(workbook["Market Intelligence"].max_column, 95)
            self.assertEqual(workbook.sheetnames, [
                "Oracle V1.6 Output", "Market Intelligence", "xG Evidence Audit",
                "H2H Intelligence", "Team Form Evidence", "Data Quality & Risk",
                "Schedule Reconciliation", "Goal Intelligence", "Goal Market Research",
                "Market Data Coverage", "Archive Field Coverage", "Definitions & Governance",
                "50-League Coverage", "Coverage Audit Summary", "xG Provenance Decision",
            ])
            quality = workbook["Data Quality & Risk"]
            quality_headers = [cell.value for cell in quality[1]]
            quality_values = dict(zip(quality_headers, [cell.value for cell in quality[2]]))
            self.assertEqual(quality_values["snapshot_no_home_away_flag"], "1")
            self.assertEqual(quality_values["fixture_orientation_status"], "NO_HOME_AWAY_DISTINCTION")
            self.assertEqual(quality_values["home_away_market_review_status"],
                             "REVIEW_REQUIRED_NO_HOME_AWAY_DISTINCTION")
            self.assertEqual(quality_values["runtime_feature_support_status"],
                             "PASS_ALL_20_REQUIRED_FEATURES")
            self.assertEqual(quality_values["runtime_home_history_gate"], "PASS_5_OR_MORE")
            sheet = workbook["50-League Coverage"]
            self.assertEqual(sheet.max_row, 3)
            self.assertEqual(sheet.max_column, len(market_report.COVERAGE_HEADERS))
            self.assertEqual(sheet["A3"].value, "S2")
            self.assertEqual(workbook["Coverage Audit Summary"].max_row, len(summary_rows) + 1)
            self.assertEqual(workbook["xG Provenance Decision"].max_row, len(xg_rows) + 1)
            workbook.close()


if __name__ == "__main__":
    unittest.main()
