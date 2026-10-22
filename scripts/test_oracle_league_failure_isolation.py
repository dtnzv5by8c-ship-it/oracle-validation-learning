"""Research-only acceptance tests for Oracle league failure isolation.

This contract test does not execute the live workflow or production prediction code.
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
                               "reason": fixture.failure or "PREMATCH_STATE_MISSING"})
            continue
        try:
            results.append({"fixture_id": fixture.fixture_id, "league": fixture.league,
                            "result": predictor(fixture)})
        except Exception as exc:
            exclusions.append({"fixture_id": fixture.fixture_id, "league": fixture.league,
                               "reason": f"FIXTURE_ERROR:{type(exc).__name__}:{exc}"})
    return results, exclusions

class FailureIsolationTests(unittest.TestCase):
    def test_missing_state_does_not_block_other_leagues(self):
        fs = [Fixture("A1","A"), Fixture("B1","B",False,"MISSING_HOME_STATE"), Fixture("C1","C")]
        results, excluded = process_independent_leagues(fs, lambda f: "PREDICTED")
        self.assertEqual([x["fixture_id"] for x in results], ["A1","C1"])
        self.assertEqual(excluded[0]["reason"], "MISSING_HOME_STATE")

    def test_runtime_error_is_quarantined(self):
        fs = [Fixture("A1","A"), Fixture("B1","B"), Fixture("C1","C")]
        def predictor(f):
            if f.league == "B": raise RuntimeError("simulated provider failure")
            return "PREDICTED"
        results, excluded = process_independent_leagues(fs, predictor)
        self.assertEqual([x["league"] for x in results], ["A","C"])
        self.assertTrue(excluded[0]["reason"].startswith("FIXTURE_ERROR:RuntimeError"))

    def test_all_ready_fixtures_continue(self):
        results, excluded = process_independent_leagues(
            [Fixture("A1","A"), Fixture("A2","A"), Fixture("C1","C")], lambda f: "PREDICTED")
        self.assertEqual(len(results), 3)
        self.assertEqual(excluded, [])

    def test_failure_is_visible_not_false_success(self):
        results, excluded = process_independent_leagues(
            [Fixture("B1","B",False,"NO_FIXTURES_IN_WINDOW")], lambda f: "PREDICTED")
        self.assertEqual(results, [])
        self.assertEqual(excluded[0]["reason"], "NO_FIXTURES_IN_WINDOW")

if __name__ == "__main__":
    unittest.main(verbosity=2)
