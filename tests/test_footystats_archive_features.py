import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_footystats_archive_features.py"
spec = importlib.util.spec_from_file_location("oracle_footystats_features", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class FeatureBuilderUnitTests(unittest.TestCase):
    def test_unix_seconds_parse(self):
        dt = mod.as_date(1790000000)
        self.assertIsNotNone(dt)
        self.assertEqual(dt.tzinfo, mod.timezone.utc)

    def test_iso_date_parse(self):
        dt = mod.as_date("2026-10-21T10:00:00Z")
        self.assertEqual(dt.isoformat(), "2026-10-21T10:00:00+00:00")

    def test_event_arrays_count_goals(self):
        self.assertEqual(mod.score({"homeGoals": ["12", "66"]}, mod.HG_KEYS, "homeGoals"), (2, "counted_goal_event_array"))
        self.assertEqual(mod.score({"awayGoals": []}, mod.AG_KEYS, "awayGoals"), (0, "counted_goal_event_array"))

    def test_explicit_score_wins(self):
        self.assertEqual(mod.score({"homeGoalCount": 0, "homeGoals": ["12"]}, mod.HG_KEYS, "homeGoals"), (0, "explicit_score_field"))

    def test_unknown_status_fails_closed(self):
        self.assertFalse(mod.settled({"status": "unknown"}))
        self.assertFalse(mod.settled({"status": "postponed"}))
        self.assertTrue(mod.settled({"status": "complete"}))

    def test_non_complete_zero_zero_placeholders_are_not_settled_truth(self):
        # Numeric zero scores can parse successfully even when the source status
        # says the match is not complete. Status must therefore gate truth.
        for raw_status in ("incomplete", "suspended", "canceled", "cancelled", "postponed", "abandoned"):
            with self.subTest(status=raw_status):
                row = {"status": raw_status, "homeGoalCount": 0, "awayGoalCount": 0}
                self.assertEqual(mod.score(row, mod.HG_KEYS, "homeGoals"), (0, "explicit_score_field"))
                self.assertEqual(mod.score(row, mod.AG_KEYS, "awayGoals"), (0, "explicit_score_field"))
                self.assertFalse(mod.settled(row))

        # A complete 0-0 can be a research truth candidate, but is not by itself
        # proof of source authenticity, fixture identity, or production settlement.
        self.assertTrue(mod.settled({"status": "complete", "homeGoalCount": 0, "awayGoalCount": 0}))

    def test_missing_score_not_imputed(self):
        self.assertEqual(mod.score({}, mod.HG_KEYS, "homeGoals"), (None, "unavailable"))

if __name__ == "__main__":
    unittest.main()
