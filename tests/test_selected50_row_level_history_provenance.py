import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_selected50_row_level_history_provenance import audit  # noqa: E402


def archive_row(fid, kickoff, home="H", away="X", status="complete",
                hg=1, ag=0, source_row=0, competition="L", season="S"):
    raw = {
        "team_a_shots": 10, "team_b_shots": 7,
        "team_a_shotsOnTarget": 4, "team_b_shotsOnTarget": 2,
    }
    return {
        "competition_id": competition, "season_id": season, "country": "Test",
        "league": "League", "source_file": f"seasons/{season}/matches.json",
        "source_row": source_row, "fixture_id": fid, "kickoff_unix": kickoff,
        "home_id": home, "away_id": away, "home_goals": hg, "away_goals": ag,
        "finished": status.lower() in {"complete", "completed", "finished", "full time", "full-time", "ft", "ended", "played"} and hg is not None and ag is not None,
        "status_raw": status, "raw": raw, "raw_record_sha256": f"hash-{source_row}",
    }


def runtime_row(**overrides):
    row = {
        "fixture_id": "TARGET", "selected_id": "L", "country": "Test",
        "league": "League", "date_utc": "1970-01-01T00:16:40Z",
        "home_team": "Home Team", "away_team": "Away Team",
        "home_team_provider_id": "H", "away_team_provider_id": "A",
        "home_recent5_n": "2", "away_recent5_n": "5",
        "feature_support_status": "BLOCKED_MISSING_REQUIRED_FEATURES",
        "missing_required_features": "home_gf5",
    }
    row.update(overrides)
    return row


class RowLevelHistoryProvenanceTests(unittest.TestCase):
    def test_reconstructs_oriented_history_and_strict_cutoff(self):
        rows = [
            archive_row("H1", 100, home="H", away="X", source_row=1),
            archive_row("H2", 200, home="H", away="Y", source_row=2),
            archive_row("H3", 300, home="Z", away="H", source_row=3),
            archive_row("H4", 1000, home="H", away="Q", source_row=4),
            archive_row("H5", 400, home="H", away="R", status="incomplete", source_row=5),
        ]
        sides, details, qa = audit([runtime_row()], rows, {"L"})
        side = sides[0]
        self.assertEqual(side["reconstructed_history_count"], 2)
        self.assertEqual(side["runtime_history_count"], "2")
        self.assertEqual(side["history_count_reconciles"], "YES")
        self.assertEqual(side["included_history_match_ids"], "H1;H2")
        decisions = {d["historical_fixture_id"]: d["history_decision"] for d in details}
        self.assertEqual(decisions["H3"], "OTHER_EVIDENCED_REASON")
        self.assertEqual(decisions["H4"], "AFTER_CUTOFF")
        self.assertEqual(decisions["H5"], "REQUIRED_FEATURE_MISSING")
        self.assertTrue(qa["all_side_history_counts_reconcile"])

    def test_exact_duplicate_fixture_id_extra_row_is_excluded(self):
        rows = [
            archive_row("DUP", 100, source_row=1),
            archive_row("DUP", 100, source_row=2),
        ]
        sides, details, _ = audit([runtime_row(home_recent5_n="1")], rows, {"L"})
        self.assertEqual(sides[0]["reconstructed_history_count"], 1)
        duplicate = [d for d in details if d["source_record_index"] == 2][0]
        self.assertEqual(duplicate["history_decision"], "DUPLICATE_RECORD")
        self.assertEqual(duplicate["exclusion_detail"], "EXACT_DUPLICATE_FIXTURE_ID_EXTRA_ROW")

    def test_duplicate_completed_signature_quarantines_all_matching_rows(self):
        rows = [
            archive_row("SIG1", 100, home="H", away="X", source_row=1),
            archive_row("SIG2", 100, home="H", away="X", source_row=2),
        ]
        sides, details, qa = audit([runtime_row(home_recent5_n="0")], rows, {"L"})
        self.assertEqual(sides[0]["reconstructed_history_count"], 0)
        self.assertTrue(all(d["history_decision"] == "DUPLICATE_RECORD" for d in details))
        self.assertEqual(qa["history_decision_counts"]["DUPLICATE_RECORD"], 2)

    def test_runtime_count_mismatch_is_review_required(self):
        rows = [archive_row("ONE", 100, source_row=1)]
        sides, _, qa = audit([runtime_row(home_recent5_n="4")], rows, {"L"})
        self.assertEqual(sides[0]["audit_status"], "REVIEW_REQUIRED_COUNT_MISMATCH")
        self.assertFalse(qa["all_side_history_counts_reconcile"])
        self.assertEqual(len(qa["runtime_archive_history_count_mismatches"]), 1)

    def test_feature_completeness_does_not_claim_five_match_sample(self):
        rows = [archive_row(f"M{i}", 100 + i, source_row=i) for i in range(1, 4)]
        sides, _, _ = audit([runtime_row(home_recent5_n="3")], rows, {"L"})
        for feature in ("home_gf5", "home_ga5", "home_shots5", "home_sot5"):
            self.assertEqual(sides[0][feature], "NO_FIVE_MATCH_SAMPLE")

    def test_unknown_selected_id_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unknown selected_id"):
            audit([runtime_row(selected_id="UNKNOWN")], [], {"L"})


if __name__ == "__main__":
    unittest.main()
