#!/usr/bin/env python3
"""Regression tests for the no-network Selected-50 current-feed identity quarantine."""
import csv
import json
import tempfile
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("identity_quarantine", ROOT / "scripts" / "build_selected50_current_feed_identity_quarantine.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class IdentityQuarantineTests(unittest.TestCase):
    def test_classification_is_fail_closed(self):
        base = {
            "current_feed_display_label_rows": "1",
            "current_feed_distinct_fotmob_league_ids": "1",
            "current_feed_country_field_present": "NO",
            "current_feed_filter_uses_league_id_allowlist": "NO",
            "exact_provider_season_id_to_fotmob_league_id_bridge": "NOT_VERIFIED",
            "identity_collision_status": "SINGLE_ID_STILL_UNVERIFIED",
        }
        self.assertEqual(MODULE.classify({**base, "current_feed_display_label_rows": "0"})["primary_blocker"], "NO_MATCHING_CURRENT_FEED_LABEL")
        self.assertEqual(MODULE.classify({**base, "current_feed_distinct_fotmob_league_ids": "2"})["primary_blocker"], "AMBIGUOUS_DISPLAY_LABEL_MULTIPLE_FEED_IDS")
        self.assertEqual(MODULE.classify(base)["primary_blocker"], "COUNTRY_NOT_RETAINED_IN_CURRENT_FEED")
        self.assertEqual(MODULE.classify({**base, "current_feed_country_field_present": "YES"})["primary_blocker"], "NO_EXACT_LEAGUE_ID_ALLOWLIST")
        self.assertEqual(MODULE.classify({**base, "current_feed_country_field_present": "YES", "current_feed_filter_uses_league_id_allowlist": "YES"})["primary_blocker"], "PROVIDER_SEASON_TO_FEED_BRIDGE_NOT_VERIFIED")
        self.assertEqual(MODULE.classify({**base, "current_feed_country_field_present": "YES", "current_feed_filter_uses_league_id_allowlist": "YES", "exact_provider_season_id_to_fotmob_league_id_bridge": "VERIFIED"})["primary_blocker"], "FEED_BRIDGE_CANDIDATE_ONLY_CANONICAL_APPROVAL_REQUIRED")
        for row in [MODULE.classify(base)]:
            self.assertEqual(row["canonical_fixture_join_verified"], "NO")
            self.assertEqual(row["canonical_team_join_verified"], "NO")
            self.assertEqual(row["official_settlement_truth_verified"], "NO")
            self.assertEqual(row["production_eligibility"], "NOT_GRANTED")

    def test_real_sources_reconcile_50_ids_and_export_no_examples(self):
        with tempfile.TemporaryDirectory() as td:
            summary = MODULE.reconcile(MODULE.DEFAULT_CROSSWALK, MODULE.DEFAULT_COLLISIONS, td)
            out = Path(td)
            rows = list(csv.DictReader((out / "selected50_current_feed_identity_quarantine.csv").open(encoding="utf-8", newline="")))
            loaded = json.loads((out / "selected50_current_feed_identity_quarantine_summary.json").read_text(encoding="utf-8"))
            self.assertEqual(len(rows), 50)
            self.assertEqual(len({r["selected_season_id"] for r in rows}), 50)
            self.assertEqual(summary, loaded)
            self.assertEqual(summary["canonical_fixture_join_verified_rows"], 0)
            self.assertEqual(summary["canonical_team_join_verified_rows"], 0)
            self.assertEqual(summary["official_settlement_truth_verified_rows"], 0)
            self.assertEqual(summary["production_eligible_rows"], 0)
            self.assertEqual(summary["network_calls_made"], 0)
            self.assertEqual(summary["paid_provider_calls_made"], 0)
            self.assertFalse(summary["raw_feed_examples_exported"])
            self.assertNotIn("current_feed_examples", rows[0])
            self.assertNotIn("current_feed_fotmob_league_ids", rows[0])

    def test_id_set_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "collision.csv"
            source_rows = MODULE.read_csv(MODULE.DEFAULT_COLLISIONS)
            source_rows[0]["footystats_selected_season_id"] = "999999"
            with bad.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(source_rows[0].keys()))
                writer.writeheader()
                writer.writerows(source_rows)
            with self.assertRaises(ValueError):
                MODULE.reconcile(MODULE.DEFAULT_CROSSWALK, bad, Path(td) / "out")

if __name__ == "__main__":
    unittest.main()
