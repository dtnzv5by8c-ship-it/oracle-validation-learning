#!/usr/bin/env python3
"""Regression checks for the selected-50 dry-run planner."""
import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class Selected50DryRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "plan_selected50_dry_run.py")],
            cwd=ROOT, capture_output=True, text=True, check=False
        )
        if result.returncode:
            raise AssertionError(f"Planner failed: {result.stdout}\n{result.stderr}")
        cls.out = ROOT / "audit-output"
        with (cls.out / "selected50_dry_run_coverage_matrix.csv").open(
            encoding="utf-8", newline=""
        ) as f:
            cls.rows = list(csv.DictReader(f))
        cls.summary = json.loads(
            (cls.out / "selected50_dry_run_summary.json").read_text(encoding="utf-8")
        )

    def test_exactly_50_unique_ids(self):
        ids = [r["selected_id"] for r in self.rows]
        self.assertEqual(50, len(ids))
        self.assertEqual(50, len(set(ids)))
        self.assertTrue(all(ids))

    def test_scope_is_dry_run_only(self):
        self.assertEqual("DRY_RUN_ONLY", self.summary["mode"])
        self.assertEqual(0, self.summary["network_calls_made"])
        self.assertEqual(0, self.summary["paid_provider_calls_made"])
        self.assertTrue(all(r["live_ingestion_status"] == "NOT_REQUESTED_DRY_RUN_ONLY" for r in self.rows))

    def test_competition_ids_are_not_guessed(self):
        self.assertTrue(all(not r["provider_competition_id"] for r in self.rows))
        self.assertTrue(all(r["provider_season_id"] == r["selected_id"] for r in self.rows))

    def test_unknown_archive_is_not_called_unavailable(self):
        statuses = {r["archive_exact_id_status"] for r in self.rows}
        self.assertEqual({"ARCHIVE_MATCHED", "ARCHIVE_ABSENT_UNVERIFIED"}, statuses)
        self.assertTrue(all(r["production_eligible"] == "NO" for r in self.rows))

    def test_minimum_request_estimate_is_explicit(self):
        self.assertEqual(200, self.summary["minimum_endpoint_calls_if_live_one_pass"])
        self.assertIn("pagination", self.summary["additional_calls"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
