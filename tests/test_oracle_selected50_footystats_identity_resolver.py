import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from oracle_selected50_footystats_identity_resolver import (  # noqa: E402
    norm_name, parse_kickoff, resolve_candidates
)


class ResolverTests(unittest.TestCase):
    def test_name_normalization_is_accent_and_suffix_tolerant(self):
        self.assertEqual(norm_name("Atlético Ottawa FC"), norm_name("Atletico Ottawa"))

    def test_unix_kickoff_is_utc(self):
        dt = parse_kickoff({"date_unix": 1790895600})
        self.assertIsNotNone(dt)
        self.assertEqual(dt.tzinfo, __import__("datetime").timezone.utc)

    def test_exact_join_is_candidate_not_approved(self):
        fs = [{
            "selected_season_id": "16741", "id": 11, "homeID": 1, "awayID": 2,
            "home_name": "Forge FC", "away_name": "Pacific FC",
            "date_unix": 1790895600, "status": "complete",
            "homeGoalCount": 3, "awayGoalCount": 0,
        }]
        ref = [{
            "match_id": "x", "league_code": "CAN", "home_team": "Forge",
            "away_team": "Pacific", "kickoff_utc": "2026-10-01T23:00:00+00:00",
            "status": "complete", "home_goals": 3, "away_goals": 0,
        }]
        rows = resolve_candidates(fs, ref, kickoff_tolerance_minutes=10)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["match_strength"], "EXACT_TEAMS_KICKOFF")
        self.assertEqual(rows[0]["decision"], "NOT_APPROVED")
        self.assertEqual(rows[0]["research_league_key"], "FS_SEASON_16741")

    def test_completed_score_conflict_is_quarantined(self):
        fs = [{
            "selected_season_id": "16741", "id": 11, "home_name": "Forge FC",
            "away_name": "Pacific FC", "date_unix": 1790895600,
            "status": "complete", "homeGoalCount": 3, "awayGoalCount": 0,
        }]
        ref = [{
            "match_id": "x", "home_team": "Forge", "away_team": "Pacific",
            "kickoff_utc": "2026-10-01T23:00:00+00:00", "status": "complete",
            "home_goals": 0, "away_goals": 0,
        }]
        rows = resolve_candidates(fs, ref)
        self.assertEqual(rows[0]["settlement_status"], "QUARANTINE_SCORE_CONFLICT")

    def test_fuzzy_names_never_become_approved_join(self):
        fs = [{
            "selected_season_id": "17146", "id": 1, "home_name": "Manchester United",
            "away_name": "Liverpool", "date_unix": 1790895600,
        }]
        ref = [{
            "match_id": "z", "home_team": "Manchester Utd", "away_team": "Liverpool FC",
            "kickoff_utc": "2026-10-01T23:00:00+00:00",
        }]
        rows = resolve_candidates(fs, ref)
        self.assertTrue(all(r["decision"] == "NOT_APPROVED" for r in rows))
        self.assertTrue(all(r["match_strength"] == "FUZZY_NAME_LEAD_ONLY" for r in rows))

    def test_no_home_away_fields_do_not_invent_team_join(self):
        fs = [{"selected_season_id": "16741", "id": 2, "home_name": "", "away_name": ""}]
        self.assertEqual(resolve_candidates(fs, [{"home_team": "A", "away_team": "B"}]), [])

    def test_no_home_away_flag_is_quarantined(self):
        fs = [{
            "selected_season_id": "16741", "id": 12, "home_name": "Forge FC",
            "away_name": "Pacific FC", "date_unix": 1790895600,
            "status": "complete", "homeGoalCount": 3, "awayGoalCount": 0,
            "no_home_away": 1,
        }]
        ref = [{
            "match_id": "x", "home_team": "Forge", "away_team": "Pacific",
            "kickoff_utc": "2026-10-01T23:00:00+00:00", "status": "complete",
            "home_goals": 3, "away_goals": 0,
        }]
        rows = resolve_candidates(fs, ref)
        self.assertEqual(rows[0]["settlement_status"], "QUARANTINE_NO_HOME_AWAY")
        self.assertEqual(rows[0]["decision"], "NOT_APPROVED")


if __name__ == "__main__":
    unittest.main()
