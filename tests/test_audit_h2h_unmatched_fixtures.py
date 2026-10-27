import unittest

from scripts.build_h2h_report import team
from scripts.audit_h2h_unmatched_fixtures import diagnose


class H2HUnmatchedDiagnosticsTests(unittest.TestCase):
    def test_same_team_name_in_expected_league_is_reported(self):
        rows = diagnose(
            [{"league_code": "D1", "home_team": "Borussia Dortmund", "away_team": "Mainz 05"}],
            [{"date": "2026-10-24", "league": "D1", "home_team": "Borussia Dortmund", "away_team": "Frankfurt"}],
        )
        home = next(row for row in rows if row["unresolved_team_side"] == "home")
        self.assertEqual(home["diagnosis"], "FOUND_IN_EXPECTED_LEAGUE")

    def test_other_league_presence_is_not_auto_approved(self):
        rows = diagnose(
            [{"league_code": "D2", "home_team": "Schalke 04", "away_team": "Paderborn"}],
            [{"date": "2026-10-24", "league": "D1", "home_team": "Schalke 04", "away_team": "Paderborn"}],
        )
        home = next(row for row in rows if row["unresolved_team_side"] == "home")
        self.assertEqual(home["diagnosis"], "FOUND_ONLY_IN_OTHER_LEAGUE_CODES")
        self.assertFalse(home["mapping_approved"])
        self.assertFalse(home["scoring_eligible_from_this_diagnostic"])

    def test_diacritics_are_normalized_without_fuzzy_approval(self):
        rows = diagnose(
            [{"league_code": "ROU", "home_team": "Oțelul", "away_team": "UTA Arad"}],
            [{"date": "2026-10-24", "league": "ROU", "home_team": "Otelul", "away_team": "Missing FC"}],
        )
        home = next(row for row in rows if row["unresolved_team_side"] == "home")
        self.assertEqual(home["diagnosis"], "FOUND_IN_EXPECTED_LEAGUE")

    def test_name_similarity_is_candidate_only(self):
        rows = diagnose(
            [{"league_code": "D1", "home_team": "FC Koln", "away_team": "Mainz"}],
            [{"date": "2026-10-24", "league": "D1", "home_team": "1. FC Koln", "away_team": "Missing Club"}],
        )
        home = next(row for row in rows if row["unresolved_team_side"] == "home")
        self.assertIn(home["diagnosis"], {"POSSIBLE_NAME_ALIAS_REQUIRES_REVIEW", "NOT_FOUND_IN_ARCHIVE"})
        self.assertFalse(home["mapping_approved"])
        self.assertFalse(home["scoring_eligible_from_this_diagnostic"])

    def test_report_canonical_aliases_are_shared_with_diagnostic(self):
        rows = diagnose(
            [{"league_code": "D2", "home_team": "1. FC Nürnberg", "away_team": "Kaiserslautern"}],
            [{"date": "2026-10-24", "league": "D2", "home_team": "Nurnberg", "away_team": "Kaiserslautern"}],
        )
        home = next(row for row in rows if row["unresolved_team_side"] == "home")
        self.assertEqual(home["diagnosis"], "FOUND_IN_EXPECTED_LEAGUE")

    def test_heerenveen_short_name_matches_full_archive_name(self):
        rows = diagnose(
            [{"league_code": "N1", "home_team": "Den Haag", "away_team": "Heerenveen"}],
            [{"date": "2026-10-24", "league": "N1", "home_team": "Den Haag", "away_team": "SC Heerenveen"}],
        )
        away = next(row for row in rows if row["unresolved_team_side"] == "away")
        self.assertEqual(away["diagnosis"], "FOUND_IN_EXPECTED_LEAGUE")

    def test_polish_l_stroke_name_variant_matches_archive(self):
        rows = diagnose(
            [{"league_code": "POL", "home_team": "Wisła Płock", "away_team": "Raków"}],
            [{"date": "2026-10-24", "league": "POL", "home_team": "Wisla Plock", "away_team": "Rakow"}],
        )
        home = next(row for row in rows if row["unresolved_team_side"] == "home")
        self.assertEqual(home["diagnosis"], "FOUND_IN_EXPECTED_LEAGUE")

    def test_official_variant_alias_is_not_auto_approved_as_new_mapping(self):
        rows = diagnose(
            [{"league_code": "B1", "home_team": "SK Beveren", "away_team": "Westerlo"}],
            [{"date": "2026-10-24", "league": "B1", "home_team": "Beveren", "away_team": "Westerlo"}],
        )
        home = next(row for row in rows if row["unresolved_team_side"] == "home")
        self.assertEqual(home["diagnosis"], "FOUND_IN_EXPECTED_LEAGUE")
        self.assertFalse(home["mapping_approved"])

    def test_empty_archive_fails_closed_as_not_found(self):
        rows = diagnose(
            [],
            [{"date": "2026-10-24", "league": "D1", "home_team": "Unknown A", "away_team": "Unknown B"}],
        )
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(row["diagnosis"] == "NOT_FOUND_IN_ARCHIVE" for row in rows))
        self.assertTrue(all(not row["mapping_approved"] for row in rows))



    def test_manchester_united_fc_variant_uses_explicit_alias(self):
        self.assertEqual(team("Manchester United FC"), "manutd")
        self.assertEqual(team("Manchester Utd"), "manutd")
        self.assertEqual(team("Manchester City"), "mancity")

    def test_lusitania_short_name_is_scoped_to_portuguese_second_tier(self):
        self.assertEqual(team("Lusitânia", "POR2"), "lusitanialourosa")
        self.assertEqual(team("Lusitânia Lourosa", "POR2"), "lusitanialourosa")
        # Do not conflate SC Lusitânia dos Açores with Lusitânia Lourosa.
        self.assertEqual(team("Lusitânia", "POR"), "lusitania")
        self.assertEqual(team("SC Lusitânia dos Açores", "POR"), "sclusitaniadosacores")

    def test_archive_aliases_for_verified_short_names(self):
        cases = [
            ("B1", "Waregem", "Zulte Waregem"),
            ("POL", "Rakow", "Raków Częstochowa"),
            ("I2", "Entella", "Virtus Entella"),
            ("ROU", "Sepsi Sf. Gheorghe", "Sepsi OSK"),
        ]
        for league, short, canonical in cases:
            with self.subTest(short=short):
                rows = diagnose(
                    [{"league_code": league, "home_team": short, "away_team": "Opponent"}],
                    [{"date": "2026-10-24", "league": league, "home_team": canonical, "away_team": "Opponent"}],
                )
                home = next(row for row in rows if row["unresolved_team_side"] == "home")
                self.assertEqual(home["diagnosis"], "FOUND_IN_EXPECTED_LEAGUE")

if __name__ == "__main__":
    unittest.main()
