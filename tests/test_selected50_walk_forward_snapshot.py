#!/usr/bin/env python3
"""Regression tests for the sanitized aggregate walk-forward audit."""
import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import audit_selected50_walk_forward_snapshot as audit

class WalkForwardSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.folds=audit.read_csv(audit.DATA/"aggregate_folds.csv")
        self.metadata=audit.read_json(audit.DATA/"metadata.json")
    def test_pinned_snapshot_passes_research_only(self):
        result=audit.audit_snapshot()
        self.assertEqual(result["status"],"PASS_AGGREGATE_WALK_FORWARD_INTEGRITY_AUDIT_RESEARCH_ONLY")
        self.assertEqual(result["aggregate_market_fold_rows"],15)
        self.assertEqual(result["wilson_intervals_recomputed"],15)
        self.assertEqual(result["brier_skill_formula_checks"],15)
        self.assertFalse(result["production_eligible"])
        self.assertFalse(result["betting_eligible"])
        self.assertEqual(result["combo_probabilities_remaining"],0)
    def test_wilson_interval_is_ordered_around_accuracy(self):
        lo,hi=audit.wilson(3500,6611)
        self.assertLess(lo,3500/6611); self.assertGreater(hi,3500/6611)
    def test_bad_fold_order_is_rejected(self):
        rows=[r.copy() for r in self.folds]
        rows[1]["fold"]="WF2_2025-09-20_to_2025-03-20"
        with self.assertRaises(AssertionError): audit.validate_folds(rows,self.metadata["fold_design"])
    def test_expanding_window_leakage_arithmetic_is_enforced(self):
        rows=[r.copy() for r in self.folds]
        target=next(r for r in rows if r["market"]=="BTTS" and r["fold"].startswith("WF2_"))
        target["train_n"]=str(int(target["train_n"])+1)
        with self.assertRaises(AssertionError): audit.validate_folds(rows,self.metadata["fold_design"])
    def test_brier_skill_corruption_is_rejected(self):
        rows=[r.copy() for r in self.folds]
        rows[0]["brier_skill_vs_prevalence"]="0.99"
        with self.assertRaises(AssertionError): audit.validate_folds(rows,self.metadata["fold_design"])

if __name__=="__main__": unittest.main(verbosity=2)
