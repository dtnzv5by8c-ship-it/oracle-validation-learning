"""Research-only acceptance tests for Oracle crosswalk and failure isolation.

These contract tests do not execute the production prediction model or live workflow.
"""
from dataclasses import dataclass
import unittest

from scripts.oracle_isolated_batch_runner import BatchItem, run_isolated_batches, run_isolated_leagues

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


    def test_multiple_failures_in_one_league_do_not_block_other_leagues(self):
        fs = [
            Fixture("A1", "A"),
            Fixture("B1", "B", False, "MISSING_HOME_STATE"),
            Fixture("B2", "B"),
            Fixture("B3", "B"),
            Fixture("C1", "C"),
        ]
        def predictor(f):
            if f.fixture_id in {"B2", "B3"}:
                raise RuntimeError("simulated failure")
            return "test-only"
        results, excluded = process_independent_leagues(fs, predictor)
        self.assertEqual([x["fixture_id"] for x in results], ["A1", "C1"])
        self.assertEqual(
            [(x["fixture_id"], x["status"]) for x in excluded],
            [
                ("B1", "SKIPPED_DATA_GAP"),
                ("B2", "FAILED_PROCESSING"),
                ("B3", "FAILED_PROCESSING"),
            ],
        )

    def test_empty_league_window_is_explicitly_reported(self):
        results, excluded = process_independent_leagues(
            [Fixture("B1", "B", False, "NO_FIXTURES_IN_WINDOW")],
            lambda f: "test-only",
        )
        self.assertEqual(results, [])
        self.assertEqual(excluded[0]["status"], "SKIPPED_DATA_GAP")
        self.assertEqual(excluded[0]["reason"], "NO_FIXTURES_IN_WINDOW")

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


class IsolatedBatchRunnerTests(unittest.TestCase):
    def test_fixture_failures_are_isolated_and_reported(self):
        items = [
            BatchItem("A1", "A"),
            BatchItem("B1", "B", False, "MISSING_STATE"),
            BatchItem("B2", "B"),
            BatchItem("C1", "C"),
        ]
        def processor(item):
            if item.fixture_id == "B2":
                raise RuntimeError("simulated failure")
            return "test-only"
        report = run_isolated_batches(items, processor, global_preflight=lambda: None)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual([x["fixture_id"] for x in report["results"]], ["A1", "C1"])
        self.assertEqual(
            [x["status"] for x in report["fixture_outcomes"]],
            ["PREDICTED", "SKIPPED_DATA_GAP", "FAILED_PROCESSING", "PREDICTED"],
        )
        self.assertEqual(report["league_summary"]["B"]["FAILED_PROCESSING"], 1)
        self.assertTrue(report["global_preflight_passed"])

    def test_global_preflight_failure_aborts_before_processing(self):
        called = []
        def preflight():
            raise RuntimeError("stale source")
        def processor(item):
            called.append(item.fixture_id)
            return "must-not-run"
        with self.assertRaisesRegex(RuntimeError, "stale source"):
            run_isolated_batches([BatchItem("A1", "A")], processor, global_preflight=preflight)
        self.assertEqual(called, [])

    def test_all_success_reports_success(self):
        report = run_isolated_batches(
            [BatchItem("A1", "A"), BatchItem("A2", "A")],
            lambda item: "test-only",
            global_preflight=lambda: None,
        )
        self.assertEqual(report["status"], "SUCCESS")
        self.assertEqual(report["league_summary"]["A"]["PREDICTED"], 2)



class LeagueBatchIsolationTests(unittest.TestCase):
    def test_one_failed_league_does_not_block_other_league_batches(self):
        items = [
            BatchItem("A1", "A"), BatchItem("A2", "A"),
            BatchItem("B1", "B"), BatchItem("B2", "B", False, "MISSING_STATE"),
            BatchItem("C1", "C"),
        ]
        def processor(league, ready_items):
            if league == "B":
                raise RuntimeError("simulated league source failure")
            return {item.fixture_id: "test-only" for item in ready_items}
        report = run_isolated_leagues(items, processor, global_preflight=lambda: None)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertEqual({r["fixture_id"] for r in report["results"]}, {"A1", "A2", "C1"})
        self.assertEqual(report["league_summary"]["B"]["FAILED_PROCESSING"], 1)
        self.assertEqual(report["league_summary"]["B"]["SKIPPED_DATA_GAP"], 1)
        self.assertEqual(report["execution_scope"], "RESEARCH_ONLY_LEAGUE_BATCHES")

    def test_duplicate_fixture_ids_fail_only_the_affected_league(self):
        items = [BatchItem("A1", "A"), BatchItem("A1", "A"), BatchItem("B1", "B")]
        called = []
        def processor(league, ready_items):
            called.append(league)
            return {item.fixture_id: "test-only" for item in ready_items}
        report = run_isolated_leagues(items, processor, global_preflight=lambda: None)
        self.assertEqual(called, ["B"])
        self.assertEqual(report["league_summary"]["A"]["FAILED_PROCESSING"], 2)
        self.assertEqual(report["league_summary"]["B"]["PREDICTED"], 1)
        self.assertTrue(all(
            o["reason"] == "DUPLICATE_FIXTURE_ID_WITHIN_LEAGUE_BATCH"
            for o in report["fixture_outcomes"] if o["league"] == "A"
        ))

    def test_missing_output_is_explicit_and_other_leagues_continue(self):
        items = [BatchItem("A1", "A"), BatchItem("A2", "A"), BatchItem("B1", "B")]
        def processor(league, ready_items):
            if league == "A":
                return {"A1": "test-only"}  # A2 deliberately omitted
            return {"B1": "test-only"}
        report = run_isolated_leagues(items, processor, global_preflight=lambda: None)
        by_id = {row["fixture_id"]: row for row in report["fixture_outcomes"]}
        self.assertEqual(by_id["A2"]["status"], "FAILED_PROCESSING")
        self.assertEqual(by_id["A2"]["reason"], "MISSING_RESULT_FROM_LEAGUE_BATCH")
        self.assertEqual(by_id["B1"]["status"], "PREDICTED")

    def test_empty_batch_is_not_reported_as_success(self):
        report = run_isolated_leagues([], lambda league, items: {}, global_preflight=lambda: None)
        self.assertEqual(report["status"], "NO_FIXTURES")
        self.assertEqual(report["results"], [])
        self.assertEqual(report["league_summary"], {})

    def test_global_preflight_stops_all_league_batches(self):
        called = []
        def processor(league, ready_items):
            called.append(league)
            return {item.fixture_id: "test-only" for item in ready_items}
        def preflight():
            raise RuntimeError("stale global source")
        with self.assertRaisesRegex(RuntimeError, "stale global source"):
            run_isolated_leagues([BatchItem("A1", "A"), BatchItem("B1", "B")],
                                 processor, global_preflight=preflight)
        self.assertEqual(called, [])

if __name__ == "__main__":
    unittest.main(verbosity=2)
