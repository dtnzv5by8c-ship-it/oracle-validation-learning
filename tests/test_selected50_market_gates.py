#!/usr/bin/env python3
"""Regression checks for conservative selected-50 market gates."""
import csv,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class MarketGateTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  p=subprocess.run([sys.executable,str(ROOT/"scripts"/"plan_selected50_dry_run.py")],cwd=ROOT,capture_output=True,text=True)
  if p.returncode: raise AssertionError(p.stdout+"\n"+p.stderr)
  p=subprocess.run([sys.executable,str(ROOT/"scripts"/"build_selected50_market_gates.py")],cwd=ROOT,capture_output=True,text=True)
  if p.returncode: raise AssertionError(p.stdout+"\n"+p.stderr)
  out=ROOT/"audit-output"
  with (out/"selected50_market_readiness_gates.csv").open(encoding="utf-8",newline="") as f: cls.rows=list(csv.DictReader(f))
  cls.summary=json.loads((out/"selected50_market_readiness_summary.json").read_text(encoding="utf-8"))
 def test_exact_50_and_no_promotion(self):
  self.assertEqual(50,len(self.rows)); self.assertEqual(50,len({r["selected_id"] for r in self.rows}))
  self.assertTrue(all(r["production_eligible"]=="NO" for r in self.rows))
 def test_all_required_gates_blocked_or_unverified(self):
  self.assertTrue(all(r["fixture_join_gate"]=="BLOCKED_NOT_VERIFIED" for r in self.rows))
  self.assertTrue(all(r["point_in_time_xg_gate"]=="BLOCKED_NO_VERIFIED_AS_OF_PROVENANCE" for r in self.rows))
  self.assertTrue(all(r["point_in_time_odds_gate"]=="BLOCKED_NO_VERIFIED_AS_OF_PROVENANCE" for r in self.rows))
  self.assertTrue(all(r["btts_yes_gate"]=="NOT_VERIFIED" for r in self.rows))
  self.assertTrue(all(r["double_chance_gate"]=="NOT_VERIFIED" for r in self.rows))
  self.assertTrue(all(r["dc_under_4_5_gate"]=="NOT_VERIFIED" for r in self.rows))
  self.assertTrue(all(r["m1up_gate"].startswith("BLOCKED_") for r in self.rows))
 def test_no_live_calls_and_summary_matches(self):
  self.assertEqual(0,self.summary["live_api_calls_made"])
  self.assertFalse(self.summary["all_production_eligible"])
if __name__=="__main__": unittest.main(verbosity=2)
