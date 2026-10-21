import unittest
from scripts.build_score_verified_evaluation import build_rows
import hashlib, json

class ScoreVerifiedEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.p={"prediction_id":"p1","fixture_id":"f1","competition_id":"c1",
          "scheduled_kickoff_utc":"2026-10-20T18:00:00Z","prediction_timestamp_utc":"2026-10-20T10:00:00Z",
          "home_team_id":"h","away_team_id":"a","market":"BTTS","selection":"YES","probability":0.72}
        self.r={"fixture_id":"f1","competition_id":"c1","scheduled_kickoff_utc":"2026-10-20T18:00:00Z",
          "home_team_id":"h","away_team_id":"a","home_score":2,"away_score":1,"match_status":"FINISHED",
          "result_source":"official-results","result_observed_at_utc":"2026-10-20T20:00:00Z"}
        self.raw=(json.dumps(self.r)+"\n").encode()
        self.sha=hashlib.sha256(self.raw).hexdigest()
        self.manifest={"results_sha256":self.sha,"sources":{"official-results":{
          "source_uri":"https://example.invalid/results","approved_for_evaluation":True}}}

    def test_score_derived_win_and_metrics(self):
        out=build_rows([self.p],[self.r],self.manifest,self.sha)
        self.assertEqual(out["accepted_count"],1)
        self.assertEqual(out["rows"][0]["outcome"],"WIN")
        self.assertEqual(out["metrics"]["metrics"]["hit_rate"],1.0)

    def test_result_snapshot_hash_mismatch_fails(self):
        with self.assertRaisesRegex(ValueError,"HASH_MISMATCH"):
            build_rows([self.p],[self.r],self.manifest,"bad")

    def test_unapproved_source_excluded(self):
        m={"results_sha256":self.sha,"sources":{"official-results":{"source_uri":"x","approved_for_evaluation":False}}}
        out=build_rows([self.p],[self.r],m,self.sha)
        self.assertEqual(out["accepted_count"],0)

    def test_prediction_at_kickoff_rejected(self):
        p=dict(self.p,prediction_timestamp_utc=self.p["scheduled_kickoff_utc"])
        out=build_rows([p],[self.r],self.manifest,self.sha)
        self.assertEqual(out["rejected"][0]["reason"],"PREDICTION_NOT_STRICTLY_PRE_KICKOFF")

    def test_fixture_identity_mismatch_rejected(self):
        r=dict(self.r,home_team_id="other")
        out=build_rows([self.p],[r],self.manifest,self.sha)
        self.assertEqual(out["accepted_count"],0)

    def test_duplicate_prediction_id_fails(self):
        with self.assertRaisesRegex(ValueError,"DUPLICATE_OR_MISSING"):
            build_rows([self.p,self.p],[self.r],self.manifest,self.sha)

if __name__=="__main__": unittest.main()
