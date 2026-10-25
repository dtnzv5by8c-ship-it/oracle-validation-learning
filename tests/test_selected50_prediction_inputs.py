#!/usr/bin/env python3
"""Tests for exact-key Oracle prediction/report input validation."""
import csv,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from validate_selected50_prediction_inputs import validate

class PredictionInputTests(unittest.TestCase):
 def write(self,path,fields,rows):
  with path.open("w",encoding="utf-8",newline="") as f:
   w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
 def test_exact_join_and_probability_preserved(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"p.csv"; v=Path(d)/"v.csv"
   self.write(p,["fixture_id","market","oracle_probability_pct"],[
    {"fixture_id":"F1","market":"BTTS Yes","oracle_probability_pct":"67.25"},
    {"fixture_id":"F1","market":"Double Chance","oracle_probability_pct":"81"}])
   self.write(v,["fixture_id","league","kickoff_utc","home_team","away_team","home_recent_form","away_recent_form","h2h_summary","home_attacking_index","home_defensive_index","away_attacking_index","away_defensive_index"],[
    {"fixture_id":"F1","league":"L","kickoff_utc":"2026-10-25T14:00:00Z","home_team":"A","away_team":"B","home_recent_form":"W-D-W","away_recent_form":"L-W-D","h2h_summary":"A 2 wins; B 1 win","home_attacking_index":"72","home_defensive_index":"60","away_attacking_index":"55","away_defensive_index":"63"}])
   result=validate(p,v)
   self.assertEqual("PASS",result["status"])
   self.assertTrue(result["probabilities_changed"] is False)
   self.assertEqual(1,result["matched_fixture_ids"])
 def test_unmatched_and_h2h_gap_block(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"p.csv"; v=Path(d)/"v.csv"
   self.write(p,["fixture_id","market","oracle_probability_pct"],[{"fixture_id":"F1","market":"BTTS Yes","oracle_probability_pct":"67"}])
   self.write(v,["fixture_id","league","kickoff_utc","home_team","away_team","home_recent_form","away_recent_form","h2h_summary","home_attacking_index","home_defensive_index","away_attacking_index","away_defensive_index"],[
    {"fixture_id":"F2","league":"L","kickoff_utc":"x","home_team":"A","away_team":"B","home_recent_form":"W","away_recent_form":"L","h2h_summary":"","home_attacking_index":"1","home_defensive_index":"2","away_attacking_index":"3","away_defensive_index":"4"}])
   result=validate(p,v)
   self.assertEqual("BLOCKED_OR_INCOMPLETE",result["status"])
   self.assertEqual(["F1"],result["unmatched_prediction_fixture_ids"])
 def test_invalid_probability_is_not_silently_fixed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"p.csv"; v=Path(d)/"v.csv"
   self.write(p,["fixture_id","market","oracle_probability_pct"],[{"fixture_id":"F1","market":"BTTS Yes","oracle_probability_pct":"101"}])
   self.write(v,["fixture_id","league","kickoff_utc","home_team","away_team","home_recent_form","away_recent_form","h2h_summary","home_attacking_index","home_defensive_index","away_attacking_index","away_defensive_index"],[
    {"fixture_id":"F1","league":"L","kickoff_utc":"x","home_team":"A","away_team":"B","home_recent_form":"W","away_recent_form":"L","h2h_summary":"h2h","home_attacking_index":"1","home_defensive_index":"2","away_attacking_index":"3","away_defensive_index":"4"}])
   result=validate(p,v)
   self.assertEqual("BLOCKED_OR_INCOMPLETE",result["status"])
   self.assertEqual(1,len(result["invalid_probability_rows"]))
   self.assertFalse(result["probabilities_changed"])
if __name__=="__main__": unittest.main(verbosity=2)
