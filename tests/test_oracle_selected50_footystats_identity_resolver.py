import sys
import unittest
from datetime import timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from oracle_selected50_footystats_identity_resolver import parse_kickoff, resolve_candidates


def fs_row(**overrides):
    row = {
        "selected_season_id": "16741", "id": 11, "homeID": 1, "awayID": 2,
        "home_name": "Forge FC", "away_name": "Pacific FC",
        "date_unix": 1790895600, "status": "complete",
        "homeGoalCount": 3, "awayGoalCount": 0,
    }
    row.update(overrides)
    return row


def ref_row(**overrides):
    row = {
        "match_id": "ref-1", "league_code": "CAN", "home_team": "Forge",
        "away_team": "Pacific", "kickoff_utc": "2026-10-01T23:00:00+00:00",
        "status": "complete", "home_goals": 3, "away_goals": 0,
    }
    row.update(overrides)
    return row


class ResolverHardeningTests(unittest.TestCase):
    def test_unix_kickoff_is_utc(self):
        dt = parse_kickoff({"date_unix": 1790895600})
        self.assertIsNotNone(dt)
        self.assertEqual(dt.tzinfo, timezone.utc)

    def test_timezone_aware_iso_is_accepted(self):
        dt = parse_kickoff({"kickoff_utc": "2026-10-01T23:00:00+00:00"})
        self.assertIsNotNone(dt)
        self.assertEqual(dt.tzinfo, timezone.utc)

    def test_timezone_naive_iso_is_rejected(self):
        self.assertIsNone(parse_kickoff({"kickoff_utc": "2026-10-01T23:00:00"}))

    def test_no_approved_competition_bridge_is_quarantined(self):
        rows = resolve_candidates([fs_row()], [ref_row()])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["settlement_status"], "QUARANTINE_COMPETITION_BRIDGE_UNVERIFIED")
        self.assertEqual(rows[0]["competition_bridge_status"], "UNVERIFIED_NO_APPROVED_BRIDGE")
        self.assertEqual(rows[0]["decision"], "NOT_APPROVED")

    def test_approved_competition_bridge_allows_candidate_review_only(self):
        rows = resolve_candidates([fs_row()], [ref_row()], approved_competition_bridges={"16741": ["CAN"]})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["settlement_status"], "CANDIDATE_REVIEW_REQUIRED")
        self.assertEqual(rows[0]["competition_bridge_status"], "VERIFIED_APPROVED")
        self.assertEqual(rows[0]["decision"], "NOT_APPROVED")

    def test_wrong_competition_code_is_not_accepted_by_bridge(self):
        rows = resolve_candidates(
            [fs_row()], [ref_row(league_code="CUP")],
            approved_competition_bridges={"16741": ["CAN"]}
        )
        self.assertEqual(rows[0]["settlement_status"], "QUARANTINE_COMPETITION_BRIDGE_UNVERIFIED")

    def test_multiple_reference_candidates_are_quarantined(self):
        refs = [ref_row(match_id="ref-1"), ref_row(match_id="ref-2")]
        rows = resolve_candidates(
            [fs_row()], refs, approved_competition_bridges={"16741": ["CAN"]}
        )
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r["settlement_status"] == "QUARANTINE_AMBIGUOUS_MULTIPLE_REFERENCE_CANDIDATES" for r in rows))
        self.assertTrue(all(r["reference_candidate_count"] == 2 for r in rows))
        self.assertTrue(all(r["decision"] == "NOT_APPROVED" for r in rows))

    def test_timezone_naive_reference_is_quarantined_not_joined(self):
        rows = resolve_candidates(
            [fs_row()], [ref_row(kickoff_utc="2026-10-01T23:00:00")],
            approved_competition_bridges={"16741": ["CAN"]}
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["settlement_status"], "QUARANTINE_KICKOFF_UNVERIFIED")
        self.assertEqual(rows[0]["match_strength"], "EXACT_TEAMS_KICKOFF_UNVERIFIED")

    def test_completed_score_conflict_is_quarantined(self):
        rows = resolve_candidates(
            [fs_row()], [ref_row(home_goals=0, away_goals=0)],
            approved_competition_bridges={"16741": ["CAN"]}
        )
        self.assertEqual(rows[0]["settlement_status"], "QUARANTINE_SCORE_CONFLICT")

    def test_no_home_away_flag_is_quarantined(self):
        rows = resolve_candidates(
            [fs_row(no_home_away=1)], [ref_row()],
            approved_competition_bridges={"16741": ["CAN"]}
        )
        self.assertEqual(rows[0]["settlement_status"], "QUARANTINE_NO_HOME_AWAY")

    def test_fuzzy_names_never_become_approved(self):
        fs = [fs_row(home_name="Manchester United", away_name="Liverpool")]
        ref = [ref_row(home_team="Manchester Utd", away_team="Liverpool FC")]
        rows = resolve_candidates(fs, ref, approved_competition_bridges={"16741": ["CAN"]})
        self.assertTrue(rows)
        self.assertTrue(all(r["match_strength"] == "FUZZY_NAME_LEAD_ONLY" for r in rows))
        self.assertTrue(all(r["decision"] == "NOT_APPROVED" for r in rows))


if __name__ == "__main__":
    unittest.main()
