import unittest
from scripts.verify_prospective_evaluation_provenance import verify

class ProvenanceGateTests(unittest.TestCase):
    def setUp(self):
        self.pred = {"prediction_id":"p1","fixture_id":"f1","competition_id":"c1",
            "scheduled_kickoff_utc":"2026-10-01T12:00:00Z","home_team_id":"h1","away_team_id":"a1",
            "market":"BTTS","selection":"YES","probability":0.72}
        self.result = {k:self.pred[k] for k in ("fixture_id","competition_id","scheduled_kickoff_utc",
            "home_team_id","away_team_id","market","selection")}
        self.result.update({"outcome":"WIN","result_source":"official-results"})
        self.settlement = {"prediction_id":"p1","fixture_id":"f1","outcome":"WIN","result_source":"official-results"}
        self.allow = {"official-results"}

    def test_exact_match_accepted(self):
        r=verify([self.pred],[self.settlement],[self.result],self.allow)
        self.assertEqual(r["accepted_count"],1)
        self.assertTrue(r["accepted"][0]["verified_fixture"])

    def test_untrusted_source_rejected(self):
        s=dict(self.settlement, result_source="unknown")
        r=verify([self.pred],[s],[self.result],self.allow)
        self.assertEqual(r["accepted_count"],0)
        self.assertEqual(r["rejected"][0]["reason"],"RESULT_SOURCE_NOT_ALLOWLISTED")

    def test_kickoff_mismatch_rejected(self):
        bad=dict(self.result, scheduled_kickoff_utc="2026-10-01T13:00:00Z")
        r=verify([self.pred],[self.settlement],[bad],self.allow)
        self.assertEqual(r["rejected"][0]["reason"],"NO_EXACT_TRUSTED_RESULT_MATCH")

    def test_outcome_conflict_rejected(self):
        s=dict(self.settlement, outcome="LOSS")
        r=verify([self.pred],[s],[self.result],self.allow)
        self.assertEqual(r["rejected"][0]["reason"],"SETTLEMENT_OUTCOME_CONFLICTS_WITH_TRUSTED_RESULT")

    def test_duplicate_settlement_rejected(self):
        with self.assertRaisesRegex(ValueError,"DUPLICATE_SETTLEMENT"):
            verify([self.pred],[self.settlement,self.settlement],[self.result],self.allow)

    def test_duplicate_prediction_id_rejected(self):
        with self.assertRaisesRegex(ValueError,"DUPLICATE_OR_MISSING"):
            verify([self.pred,self.pred],[self.settlement],[self.result],self.allow)

if __name__ == "__main__":
    unittest.main()
