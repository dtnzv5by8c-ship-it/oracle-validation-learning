#!/usr/bin/env python3
"""Regression tests for selected-50 dry-run evidence reconciliation."""
import csv, json, subprocess, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class Selected50DryRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = subprocess.run([sys.executable, str(ROOT/"scripts"/"plan_selected50_dry_run.py")],
                           cwd=ROOT, capture_output=True, text=True)
        if p.returncode:
            raise AssertionError(p.stdout + "\n" + p.stderr)
        out=ROOT/"audit-output"
        with (out/"selected50_dry_run_coverage_matrix.csv").open(encoding="utf-8",newline="") as f:
            cls.rows=list(csv.DictReader(f))
        cls.summary=json.loads((out/"selected50_dry_run_summary.json").read_text(encoding="utf-8"))
    def test_exact_manifest_and_evidence_scope(self):
        ids=[r["selected_id"] for r in self.rows]
        self.assertEqual(50,len(ids)); self.assertEqual(50,len(set(ids)))
        self.assertEqual(50,len([r for r in self.rows if r["provider_season_id"] in ids]))
    def test_evidence_counts(self):
        self.assertEqual(31,sum(r["run56_manifest_status"]=="MANIFEST_RECORD_PRESENT" for r in self.rows))
        self.assertEqual(19,sum(r["run56_manifest_status"]=="NO_MANIFEST_RECORD_IN_RUN56" for r in self.rows))
        self.assertTrue(all(r["run56_ingestion_status"]=="INGESTED" for r in self.rows if r["run56_manifest_status"]=="MANIFEST_RECORD_PRESENT"))
    def test_archive_feature_quality_is_exactly_scoped(self):
        matched=[r for r in self.rows if r["run56_manifest_status"]=="MANIFEST_RECORD_PRESENT"]
        self.assertEqual(31,len(matched))
        self.assertTrue(all(r["archive_season_folder"].endswith("_"+r["selected_id"]) for r in matched))
        self.assertTrue(all(r["archive_score_complete"]==r["archive_records"] for r in matched))
        self.assertTrue(all(r["archive_parseable_kickoff"]==r["archive_records"] for r in matched))
        self.assertTrue(all(r["archive_team_ids_complete"]==r["archive_records"] for r in matched))
        self.assertEqual(0,sum(int(r["archive_missing_team_names"] or 0) for r in matched))
        self.assertGreater(self.summary["archive_records_across_exact_matched_selected_seasons"], 0)
        self.assertEqual(sum(int(r["archive_records"]) for r in matched), self.summary["archive_records_across_exact_matched_selected_seasons"])
    def test_no_guessed_parent_ids(self):
        self.assertTrue(all(not r["provider_competition_id"] for r in self.rows))
    def test_dry_run_only(self):
        self.assertEqual("DRY_RUN_ONLY",self.summary["mode"])
        self.assertEqual(0,self.summary["network_calls_made"])
        self.assertEqual(0,self.summary["paid_provider_calls_made"])
        self.assertTrue(all(r["live_ingestion_status"]=="NOT_REQUESTED_DRY_RUN_ONLY" for r in self.rows))
        self.assertTrue(all(r["production_eligible"]=="NO" for r in self.rows))
    def test_minimum_estimate_and_limitation(self):
        self.assertEqual(200,self.summary["minimum_endpoint_calls_if_live_one_pass"])
        self.assertIn("does not prove",self.summary["limitation"])
if __name__=="__main__": unittest.main(verbosity=2)
