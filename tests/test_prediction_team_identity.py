import json, tempfile, unittest
from pathlib import Path
from scripts.audit_prediction_team_identity import audit, normalize, resolve

class PredictionTeamIdentityTests(unittest.TestCase):
    def test_normalize_diacritics_and_club_suffix(self):
        self.assertEqual(normalize("FC Zürich"), "zurich")

    def test_normalization_matches_fixture_audit_prefixes(self):
        for name in ("HNK Gorica", "NK Gorica", "FK Gorica", "SK Gorica", "AFC Gorica"):
            with self.subTest(name=name):
                self.assertEqual(normalize(name), "gorica")

    def test_normalization_removes_common_club_suffix(self):
        self.assertEqual(normalize("Alpha FC"), "alpha")

    def test_unique_match_is_candidate_not_fixture_verification(self):
        predictions=[{"adapted_prediction":{"prediction_id":"p1","fixture_id":"f1","competition_id":"CRO"},
                      "source_row":{"home_team":"Alpha FC","away_team":"Beta"}}]
        archive=[{"home_team":"Alpha","home_team_id":"h1","away_team":"Beta","away_team_id":"a1",
                  "league_folder":"league1","season_folder":"2025","fixture_id":"x1","kickoff_utc":"2025-01-01T12:00:00+00:00"}]
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"out.jsonl"; summary=Path(d)/"summary.json"
            result=audit(predictions,archive,out,summary)
            row=json.loads(out.read_text())
        self.assertEqual(result["both_teams_unique_name_match"],1)
        self.assertFalse(row["fixture_identity_verified"])
        self.assertEqual(row["home_team_id_candidate"],"h1")

    def test_ambiguous_team_ids_remain_unresolved(self):
        predictions=[{"adapted_prediction":{"prediction_id":"p1"},"source_row":{"home_team":"Alpha","away_team":"Beta"}}]
        archive=[
            {"home_team":"Alpha","home_team_id":"h1","away_team":"Beta","away_team_id":"a1","league_folder":"l1"},
            {"home_team":"Alpha","home_team_id":"h2","away_team":"Beta","away_team_id":"a2","league_folder":"l2"},
        ]
        with tempfile.TemporaryDirectory() as d:
            result=audit(predictions,archive,Path(d)/"o.jsonl",Path(d)/"s.json")
            row=json.loads((Path(d)/"o.jsonl").read_text())
        self.assertEqual(result["unresolved_prediction_rows"],1)
        self.assertEqual(row["home_identity"]["status"],"AMBIGUOUS")

    def test_unmatched_team_is_not_guessed(self):
        self.assertEqual(resolve("Unknown FC",{} )["status"],"UNMATCHED")

if __name__=="__main__": unittest.main()
