import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_selected50_snapshot_runtime_coverage import audit  # noqa: E402

START = "2026-10-28T12:25:49Z"
RETRIEVED = "2026-10-28T06:11:51.985177+00:00"


def snapshot_row(fid, season="S1", kickoff="2026-10-28T14:00:00Z", flag=0, **extra):
    row = {
        "id": fid, "selected_season_id": season, "kickoff_utc": kickoff,
        "status": "incomplete", "no_home_away": flag, "manifest_country": "Serbia",
        "manifest_competition": "SuperLiga", "homeID": 10, "home_name": "Home FC",
        "awayID": 20, "away_name": "Away FC", "homeGoalCount": 0, "awayGoalCount": 0,
    }
    row.update(extra)
    return row


def runtime_row(fid, season="S1", kickoff="2026-10-28T14:00:00Z", **extra):
    row = {
        "fixture_id": fid, "selected_id": season, "date_utc": kickoff,
        "COMBO_HOME_probability_pct": "", "COMBO_AWAY_probability_pct": "",
        "country": "Serbia", "league": "SuperLiga", "home_team": "Home FC",
        "away_team": "Away FC", "prediction_status": "RAW_RESEARCH_ONLY",
    }
    row.update(extra)
    return row


def snapshot(rows, retrieved=RETRIEVED, **extra):
    result = {"retrieved_utc": retrieved, "api_key_persisted": False,
              "raw_provider_payload_persisted": False, "fixture_rows": rows}
    result.update(extra)
    return result


class SnapshotRuntimeCoverageTests(unittest.TestCase):
    def test_exact_season_and_fixture_ids_join_not_display_names(self):
        diffs, summary = audit(snapshot([snapshot_row("A"), snapshot_row("B")]), [runtime_row("B")], START)
        self.assertEqual(summary["exact_season_id_and_fixture_id_matches"], 1)
        self.assertEqual(summary["snapshot_only_rows"], 1)
        self.assertEqual(diffs[0]["fixture_id"], "A")
        self.assertEqual(diffs[0]["classification"], "SNAPSHOT_ONLY_FLAG_FALSE_NOT_IN_RUNTIME_OUTPUT")

    def test_flagged_no_home_away_rows_are_reviewed_not_silently_discarded(self):
        diffs, summary = audit(snapshot([snapshot_row("A", flag=1)]), [runtime_row("B")], START)
        self.assertEqual(summary["snapshot_only_no_home_away_flag_true"], 1)
        self.assertEqual(diffs[0]["classification"], "SNAPSHOT_ONLY_NO_HOME_AWAY_FLAGGED_REVIEW")

    def test_runtime_only_rows_are_separate_from_snapshot_only_rows(self):
        diffs, summary = audit(snapshot([snapshot_row("A")]), [runtime_row("B")], START)
        self.assertEqual(summary["runtime_only_rows"], 1)
        self.assertEqual(diffs[1]["side"], "RUNTIME_ONLY")
        self.assertEqual(diffs[1]["classification"], "RUNTIME_ONLY_NOT_IN_SNAPSHOT_REVIEW")

    def test_same_names_different_ids_do_not_join(self):
        s = snapshot_row("A", home_name="Same FC", away_name="Other FC")
        r = runtime_row("B", home_team="Same FC", away_team="Other FC")
        diffs, summary = audit(snapshot([s]), [r], START)
        self.assertEqual(summary["exact_season_id_and_fixture_id_matches"], 0)
        self.assertEqual(len(diffs), 2)

    def test_combo_mask_violation_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Combo probability mask"):
            audit(snapshot([snapshot_row("A")]), [runtime_row("A", COMBO_HOME_probability_pct="61.2")], START)

    def test_naive_snapshot_timestamp_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "explicit timezone"):
            audit(snapshot([snapshot_row("A")], retrieved="2026-10-28T06:11:51"), [runtime_row("A")], START)

    def test_snapshot_retrieved_after_runtime_start_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "later than runtime start"):
            audit(snapshot([snapshot_row("A")], retrieved="2026-10-28T13:00:00Z"), [runtime_row("A")], START)

    def test_duplicate_snapshot_key_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "duplicate snapshot fixture key"):
            audit(snapshot([snapshot_row("A"), snapshot_row("A")]), [runtime_row("A")], START)

    def test_runtime_fixture_outside_declared_window_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "outside the declared runtime window"):
            audit(snapshot([snapshot_row("A", kickoff="2026-11-10T14:00:00Z")]),
                  [runtime_row("A", kickoff="2026-11-10T14:00:00Z")], START)

    def test_finished_status_with_valid_scores_is_excluded_from_snapshot_candidates(self):
        finished = snapshot_row("A", status="complete", homeGoalCount=1, awayGoalCount=0)
        _, summary = audit(snapshot([finished]), [runtime_row("B")], START)
        self.assertEqual(summary["snapshot_rows_in_runtime_window"], 0)
        self.assertEqual(summary["snapshot_only_rows"], 0)
        self.assertEqual(summary["runtime_only_rows"], 1)

    def test_cancelled_or_postponed_statuses_are_excluded_like_runtime(self):
        postponed = snapshot_row("A", status="postponed")
        _, summary = audit(snapshot([postponed]), [runtime_row("B")], START)
        self.assertEqual(summary["snapshot_rows_in_runtime_window"], 0)
        self.assertEqual(summary["snapshot_only_rows"], 0)

    def test_unknown_no_home_away_flag_is_not_inferred(self):
        diffs, summary = audit(snapshot([snapshot_row("A", flag="unknown")]), [runtime_row("B")], START)
        self.assertEqual(summary["snapshot_only_no_home_away_flag_unknown"], 1)
        self.assertEqual(diffs[0]["classification"], "SNAPSHOT_ONLY_NO_HOME_AWAY_FLAG_UNKNOWN_REVIEW")

    def test_snapshot_sanitization_guard(self):
        with self.assertRaisesRegex(ValueError, "sanitized-artifact guard"):
            audit(snapshot([snapshot_row("A")], api_key_persisted=True), [runtime_row("A")], START)


    def _assert_invalid_completed_score_is_quarantined(self, row):
        diffs, summary = audit(snapshot([row]), [runtime_row("B")], START)
        self.assertEqual(summary["snapshot_finished_invalid_score_rows"], 1)
        self.assertEqual(summary["snapshot_finished_invalid_score_keys"], [["S1", "A"]])
        self.assertEqual(summary["snapshot_rows_in_runtime_window"], 0)
        self.assertEqual(summary["snapshot_only_rows"], 0)
        quarantined = [d for d in diffs if d["side"] == "SNAPSHOT_QUARANTINED"]
        self.assertEqual(len(quarantined), 1)
        self.assertEqual(quarantined[0]["classification"], "QUARANTINE_FINISHED_STATUS_INVALID_SCORE")
        self.assertEqual(quarantined[0]["production_eligible"], "NO")
        self.assertEqual(quarantined[0]["prediction_created"], 0)

    def test_fractional_score_cannot_make_completed_status_settlement_truth(self):
        row = snapshot_row("A", status="complete", homeGoalCount=1.5, awayGoalCount=0)
        self._assert_invalid_completed_score_is_quarantined(row)

    def test_boolean_score_cannot_make_completed_status_settlement_truth(self):
        row = snapshot_row("A", status="complete", homeGoalCount=True, awayGoalCount=0)
        self._assert_invalid_completed_score_is_quarantined(row)

    def test_negative_score_cannot_make_completed_status_settlement_truth(self):
        row = snapshot_row("A", status="complete", homeGoalCount=-1, awayGoalCount=0)
        self._assert_invalid_completed_score_is_quarantined(row)

    def test_missing_score_on_completed_status_is_quarantined(self):
        row = snapshot_row("A", status="complete", homeGoalCount="", awayGoalCount=0)
        self._assert_invalid_completed_score_is_quarantined(row)

    def test_integer_valued_decimal_score_remains_valid_completed_result(self):
        row = snapshot_row("A", status="complete", homeGoalCount="1.0", awayGoalCount="0.0")
        _, summary = audit(snapshot([row]), [runtime_row("B")], START)
        self.assertEqual(summary["snapshot_finished_invalid_score_rows"], 0)
        self.assertEqual(summary["snapshot_rows_in_runtime_window"], 0)
        self.assertEqual(summary["snapshot_only_rows"], 0)

if __name__ == "__main__":
    unittest.main()
