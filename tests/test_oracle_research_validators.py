import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_fixture_lifecycle.py"
SPEC = importlib.util.spec_from_file_location("audit_fixture_lifecycle", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class LifecycleClassificationTests(unittest.TestCase):
    def test_completed_candidate(self):
        self.assertEqual(MODULE.classify("complete"), "COMPLETED_CANDIDATE")

    def test_upcoming_candidate(self):
        self.assertEqual(MODULE.classify("scheduled"), "UPCOMING_CANDIDATE")

    def test_postponed(self):
        self.assertEqual(MODULE.classify("postponed"), "POSTPONED")

    def test_abandoned(self):
        self.assertEqual(MODULE.classify("abandoned"), "ABANDONED_OR_CANCELLED")

    def test_in_play(self):
        self.assertEqual(MODULE.classify("in_play"), "IN_PLAY_CANDIDATE")

    def test_suspended_is_not_settled(self):
        self.assertEqual(MODULE.classify("suspended"), "SUSPENDED_REQUIRES_REVIEW")

    def test_incomplete_is_unresolved_not_settled(self):
        self.assertEqual(MODULE.classify("incomplete"), "UNRESOLVED_REQUIRES_REVIEW")

    def test_unknown_status_fails_to_review(self):
        self.assertEqual(MODULE.classify("some-new-provider-state"), "UNRESOLVED_REQUIRES_REVIEW")

if __name__ == "__main__":
    unittest.main()
