import unittest
from scripts.settle_market_from_final_score import settle

class ScoreSettlementTests(unittest.TestCase):
    def setUp(self):
        self.p={"prediction_id":"p1","fixture_id":"f1","competition_id":"c1",
            "scheduled_kickoff_utc":"2026-10-20T18:00:00Z","home_team_id":"h","away_team_id":"a",
            "market":"BTTS","selection":"YES"}
        self.r={"fixture_id":"f1","competition_id":"c1","scheduled_kickoff_utc":"2026-10-20T18:00:00Z",
            "home_team_id":"h","away_team_id":"a","home_score":2,"away_score":1,
            "match_status":"FINISHED","result_source":"official-results"}

    def test_btts_yes_win(self):
        self.assertEqual(settle(self.p,self.r)["outcome"],"WIN")
    def test_btts_yes_loss(self):
        self.r["away_score"]=0
        self.assertEqual(settle(self.p,self.r)["outcome"],"LOSS")
    def test_over_under_push(self):
        self.p.update({"market":"TOTAL_GOALS","selection":"OVER_3.0"})
        self.assertEqual(settle(self.p,self.r)["outcome"],"PUSH")
    def test_1x2(self):
        self.p.update({"market":"1X2","selection":"HOME"})
        self.assertEqual(settle(self.p,self.r)["outcome"],"WIN")
    def test_dnb_draw_push(self):
        self.p.update({"market":"DNB","selection":"HOME"}); self.r.update({"home_score":1,"away_score":1})
        self.assertEqual(settle(self.p,self.r)["outcome"],"PUSH")
    def test_fixture_identity_mismatch_fails_closed(self):
        self.r["away_team_id"]="other"
        with self.assertRaisesRegex(ValueError,"FIXTURE_IDENTITY_MISMATCH"): settle(self.p,self.r)
    def test_unsupported_market_fails_closed(self):
        self.p.update({"market":"ASIAN_HANDICAP","selection":"HOME_-0.5"})
        with self.assertRaisesRegex(ValueError,"UNSUPPORTED_MARKET"): settle(self.p,self.r)
    def test_postponed_pending(self):
        self.r["match_status"]="POSTPONED"
        self.assertEqual(settle(self.p,self.r)["outcome"],"UNSETTLED")

if __name__=="__main__": unittest.main()
