import unittest
from scripts.oracle_prematch_state_replay import replay


class PrematchStateReplayTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = [{"league_code":"L1","date":"2026-10-23","home_team":"Pau FC","away_team":"Grenoble"}]
        self.history = [
            {"league_code":"L1","date":"2026-10-01","home_team":"Pau","away_team":"Other","home_n":"4","away_n":"0"},
            {"league_code":"L1","date":"2026-10-02","home_team":"Other","away_team":"Grenoble","home_n":"0","away_n":"5"},
            {"league_code":"L1","date":"2026-10-23","home_team":"Pau","away_team":"Other","home_n":"6","away_n":"0"},
        ]

    def test_explicit_scoped_alias_uses_only_pre_fixture_state(self):
        aliases = [{"league_code":"L1","fixture_label":"Pau FC","role":"home_team",
                    "canonical_label":"Pau","identity_evidence":"reviewed stable source ID: test-only"}]
        out = replay(self.fixtures, self.history, aliases)[0]
        self.assertEqual(out["counterfactual_status"], "ELIGIBLE_FOR_REVIEW_ONLY")
        self.assertEqual(out["role_state_audit"]["home_team"]["usable_pre_fixture_role_rows"], 1)
        self.assertEqual(out["role_state_audit"]["home_team"]["latest_pre_fixture_state_date"], "2026-10-01")

    def test_no_alias_does_not_fuzzy_match(self):
        out = replay(self.fixtures, self.history, [])[0]
        self.assertEqual(out["counterfactual_status"], "BLOCKED")
        self.assertIn("MISSING_HOME_TEAM_ROLE_STATE", out["blockers"])

    def test_alias_requires_identity_evidence(self):
        aliases = [{"league_code":"L1","fixture_label":"Pau FC","role":"home_team",
                    "canonical_label":"Pau","identity_evidence":""}]
        with self.assertRaises(ValueError):
            replay(self.fixtures, self.history, aliases)

    def test_ambiguous_alias_is_rejected(self):
        aliases = [
            {"league_code":"L1","fixture_label":"Pau FC","role":"home_team","canonical_label":"Pau","identity_evidence":"id A"},
            {"league_code":"L1","fixture_label":"Pau FC","role":"home_team","canonical_label":"Pau FC","identity_evidence":"id B"},
        ]
        with self.assertRaises(ValueError):
            replay(self.fixtures, self.history, aliases)


if __name__ == "__main__":
    unittest.main(verbosity=2)
