"""Tests for the research-only team alias candidate audit."""
import unittest

from scripts.oracle_team_alias_audit import audit_team_aliases


class TeamAliasAuditTests(unittest.TestCase):
    def setUp(self):
        self.history = [
            {"league_code": "NED2", "date": "2026-09-18", "home_team": "Almere City FC", "away_team": "Roda JC Kerkrade"},
            {"league_code": "NED2", "date": "2026-09-17", "home_team": "Jong AZ Alkmaar", "away_team": "Helmond Sport"},
            {"league_code": "CZE", "date": "2026-09-19", "home_team": "FC Zbrojovka Brno", "away_team": "Bohemians 1905"},
            {"league_code": "CZE", "date": "2026-09-18", "home_team": "Artis Brno", "away_team": "Bohemians 1905"},
            {"league_code": "POL", "date": "2026-09-19", "home_team": "Wisła Płock", "away_team": "Raków Częstochowa"},
            {"league_code": "POL", "date": "2026-09-18", "home_team": "Wisła Kraków", "away_team": "Raków Częstochowa"},
        ]

    def test_single_same_league_candidate_is_review_only(self):
        report = audit_team_aliases([
            {"league_code": "NED2", "date": "2026-10-23", "home_team": "Almere City", "away_team": "Roda"}
        ], self.history)
        home = next(row for row in report if row["role"] == "home_team")
        away = next(row for row in report if row["role"] == "away_team")
        self.assertEqual(home["status"], "REVIEW_SINGLE_CANDIDATE")
        self.assertEqual(home["candidates"][0]["label"], "Almere City FC")
        self.assertEqual(away["status"], "REVIEW_SINGLE_CANDIDATE")
        self.assertEqual(away["candidates"][0]["label"], "Roda JC Kerkrade")
        self.assertNotIn("approved_alias", home)

    def test_ambiguous_candidate_is_never_auto_selected(self):
        report = audit_team_aliases([
            {"league_code": "CZE", "date": "2026-10-24", "home_team": "Brno", "away_team": "Bohemians"}
        ], self.history)
        home = next(row for row in report if row["role"] == "home_team")
        away = next(row for row in report if row["role"] == "away_team")
        self.assertEqual(home["status"], "NEEDS_REVIEW")
        self.assertEqual({x["label"] for x in home["candidates"]}, {"FC Zbrojovka Brno", "Artis Brno"})
        self.assertEqual(away["status"], "REVIEW_SINGLE_CANDIDATE")
        self.assertEqual(away["candidates"][0]["label"], "Bohemians 1905")

    def test_candidates_are_competition_scoped(self):
        report = audit_team_aliases([
            {"league_code": "OTHER", "date": "2026-10-24", "home_team": "Almere City", "away_team": "Roda"}
        ], self.history)
        self.assertEqual({row["status"] for row in report}, {"NO_CANDIDATE"})

    def test_exact_label_is_distinguished(self):
        report = audit_team_aliases([
            {"league_code": "NED2", "date": "2026-10-23", "home_team": "Almere City FC", "away_team": "Roda JC Kerkrade"}
        ], self.history)
        self.assertTrue(all(row["status"] == "EXACT_LABEL" for row in report))


if __name__ == "__main__":
    unittest.main(verbosity=2)
