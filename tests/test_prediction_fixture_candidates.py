import json,tempfile,unittest
from pathlib import Path
from scripts.audit_prediction_fixture_candidates import audit,norm
class FixtureCandidateTests(unittest.TestCase):
 def test_normalization_prefix_and_diacritic(self): self.assertEqual(norm("HNK Gorica"),"gorica")
 def test_exact_kickoff_and_team_pair_only_candidate_not_verified(self):
  p=[{"adapted_prediction":{"prediction_id":"p","fixture_id":"f","competition_id":"CRO","scheduled_kickoff_utc":"2026-10-09T16:00:00Z"},"source_row":{"home_team":"HNK Gorica","away_team":"Rudeš"}}]
  a=[{"fixture_id":"123","league_folder":"Croatia_Prva_HNL","season_folder":"2026_x","kickoff_utc":"2026-10-09T16:00:00+00:00","home_team":"Gorica","away_team":"Rudeš"}]
  with tempfile.TemporaryDirectory() as d:
   o=Path(d)/"o.jsonl";s=Path(d)/"s.json"; r=audit(p,a,o,s); row=json.loads(o.read_text())
  self.assertEqual(r["match_status_counts"]["UNIQUE_FIXTURE_CANDIDATE_COMPETITION_ALIGNED"],1)
  self.assertFalse(row["fixture_identity_verified"]); self.assertFalse(row["eligible_for_scoring"])
 def test_kickoff_mismatch_does_not_match(self):
  p=[{"adapted_prediction":{"prediction_id":"p","competition_id":"CRO","scheduled_kickoff_utc":"2026-10-09T16:00:00Z"},"source_row":{"home_team":"Gorica","away_team":"Rudeš"}}]
  a=[{"fixture_id":"123","league_folder":"Croatia_Prva_HNL","kickoff_utc":"2026-10-09T17:00:00Z","home_team":"Gorica","away_team":"Rudeš"}]
  with tempfile.TemporaryDirectory() as d:
   r=audit(p,a,Path(d)/"o",Path(d)/"s")
  self.assertEqual(r["match_status_counts"]["NO_EXACT_KICKOFF_TEAM_CANDIDATE"],1)
 def test_ambiguous_candidates_not_accepted(self):
  p=[{"adapted_prediction":{"prediction_id":"p","competition_id":"CRO","scheduled_kickoff_utc":"2026-10-09T16:00:00Z"},"source_row":{"home_team":"Gorica","away_team":"Rudeš"}}]
  a=[{"fixture_id":"1","league_folder":"Croatia_Prva_HNL","kickoff_utc":"2026-10-09T16:00:00Z","home_team":"Gorica","away_team":"Rudeš"},{"fixture_id":"2","league_folder":"Croatia_Prva_HNL","kickoff_utc":"2026-10-09T16:00:00Z","home_team":"Gorica","away_team":"Rudeš"}]
  with tempfile.TemporaryDirectory() as d:
   r=audit(p,a,Path(d)/"o",Path(d)/"s")
  self.assertEqual(r["match_status_counts"]["AMBIGUOUS_COMPETITION_ALIGNED_FIXTURE"],1)
if __name__=="__main__":unittest.main()
