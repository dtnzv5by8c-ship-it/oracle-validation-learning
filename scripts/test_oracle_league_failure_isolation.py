"""Research-only acceptance tests for Oracle crosswalk and failure isolation.

These contract tests do not execute the production prediction model or live workflow.
"""
from dataclasses import dataclass
import unittest

@dataclass(frozen=True)
class Fixture:
    fixture_id: str
    league: str
    ready: bool = True
    failure: str = ""

def process_independent_leagues(fixtures, predictor):
    results, exclusions = [], []
    for fixture in fixtures:
        if not fixture.ready:
            exclusions.append({"fixture_id": fixture.fixture_id, "league": fixture.league,
                               "status": "SKIPPED_DATA_GAP",
                               "reason": fixture.failure or "PREMATCH_STATE_MISSING"})
            continue
        try:
            results.append({"fixture_id": fixture.fixture_id, "league": fixture.league,
                            "status": "PREDICTED", "result": predictor(fixture)})
        except Exception as exc:
            exclusions.append({"fixture_id": fixture.fixture_id, "league": fixture.league,
                               "status": "FAILED_PROCESSING",
                               "reason": f"{type(exc).__name__}:{exc}"})
    return results, exclusions

def date_gate(*, competition_match, fixture_date_match, home_team_id, away_team_id,
              identities_unique, kickoff_verified, feature_requires_ordering):
    """Return whether a date-only base join is safe for the requested feature."""
    base_identity_ok = bool(competition_match and fixture_date_match and home_team_id
                            and away_team_id and identities_unique)
    if not base_identity_ok:
        return False, "HOLD_UNVERIFIED_IDENTITY"
    if feature_requires_ordering and not kickoff_verified:
        return False, "HOLD_KICKOFF_REQUIRED_FOR_ORDERING_FEATURE"
    return True, "PASS_BASE_IDENTITY_ONLY" if not kickoff_verified else "PASS_IDENTITY_AND_TIME"

class FailureIsolationTests(unittest.TestCase):
    def test_missing_state_does_not_block_other_leagues(self):
        fs = [Fixture("A1", "A"), Fixture("B1", "B", False, "MISSING_HOME_STATE"), Fixture("C1", "C")]
        results, excluded = process_independent_leagues(fs, lambda f: "test-only")
        self.assertEqual([x["fixture_id"] for x in results], ["A1", "C1"])
        self.assertEqual(excluded[0]["status"], "SKIPPED_DATA_GAP")
        self.assertEqual(excluded[0]["reason"], "MISSING_HOME_STATE")

    def test_runtime_error_is_quarantined(self):
        fs = [Fixture("A1", "A"), Fixture("B1", "B"), Fixture("C1", "C")]
        def predictor(f):
            if f.league == "B":
                raise RuntimeError("simulated provider failure")
            return "test-only"
        results, excluded = process_independent_leagues(fs, predictor)
        self.assertEqual([x["league"] for x in results], ["A", "C"])
        self.assertEqual(excluded[0]["status"], "FAILED_PROCESSING")
        self.assertTrue(excluded[0]["reason"].startswith("RuntimeError"))

    def test_all_ready_fixtures_continue(self):
        results, excluded = process_independent_leagues(
            [Fixture("A1", "A"), Fixture("A2", "A"), Fixture("C1", "C")], lambda f: "test-only")
        self.assertEqual(len(results), 3)
        self.assertEqual(excluded, [])

    def test_failure_is_visible_not_false_success(self):
        results, excluded = process_independent_leagues(
            [Fixture("B1", "B", False, "NO_FIXTURES_IN_WINDOW")], lambda f: "test-only")
        self.assertEqual(results, [])
        self.assertEqual(excluded[0]["status"], "SKIPPED_DATA_GAP")
        self.assertEqual(excluded[0]["reason"], "NO_FIXTURES_IN_WINDOW")

class DateGateTests(unittest.TestCase):
    def test_date_only_allowed_for_base_identity_join(self):
        ok, reason = date_gate(competition_match=True, fixture_date_match=True,
            home_team_id="h1", away_team_id="a1", identities_unique=True,
            kickoff_verified=False, feature_requires_ordering=False)
        self.assertTrue(ok)
        self.assertEqual(reason, "PASS_BASE_IDENTITY_ONLY")

    def test_missing_kickoff_blocks_ordering_feature(self):
        ok, reason = date_gate(competition_match=True, fixture_date_match=True,
            home_team_id="h1", away_team_id="a1", identities_unique=True,
            kickoff_verified=False, feature_requires_ordering=True)
        self.assertFalse(ok)
        self.assertEqual(reason, "HOLD_KICKOFF_REQUIRED_FOR_ORDERING_FEATURE")

    def test_ambiguous_team_identity_blocks_even_date_only_join(self):
        ok, reason = date_gate(competition_match=True, fixture_date_match=True,
            home_team_id="h1", away_team_id="a1", identities_unique=False,
            kickoff_verified=False, feature_requires_ordering=False)
        self.assertFalse(ok)
        self.assertEqual(reason, "HOLD_UNVERIFIED_IDENTITY")

if __name__ == "__main__":
    unittest.main(verbosity=2)
