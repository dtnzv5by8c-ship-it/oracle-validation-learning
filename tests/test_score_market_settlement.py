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
    def test_home_1x_under_45_wins_on_0_0(self):
        self.p.update({"market":"COMPOSITE","selection":"HOME_1X_U45"})
        self.r.update({"home_score":0,"away_score":0})
        self.assertEqual(settle(self.p,self.r)["outcome"],"WIN")

    def test_home_1x_under_45_wins_on_four_total_goals_and_draw(self):
        self.p.update({"market":"COMPOSITE","selection":"HOME_1X_U45"})
        self.r.update({"home_score":2,"away_score":2})
        self.assertEqual(settle(self.p,self.r)["outcome"],"WIN")

    def test_home_1x_under_45_loses_when_away_wins(self):
        self.p.update({"market":"COMPOSITE","selection":"HOME_1X_U45"})
        self.r.update({"home_score":0,"away_score":1})
        self.assertEqual(settle(self.p,self.r)["outcome"],"LOSS")

    def test_home_1x_under_45_loses_at_five_goals(self):
        self.p.update({"market":"COMPOSITE","selection":"HOME_1X_U45"})
        self.r.update({"home_score":3,"away_score":2})
        self.assertEqual(settle(self.p,self.r)["outcome"],"LOSS")

    def test_away_x2_under_45_wins_on_draw(self):
        self.p.update({"market":"COMPOSITE","selection":"AWAY_X2_U45"})
        self.r.update({"home_score":1,"away_score":1})
        self.assertEqual(settle(self.p,self.r)["outcome"],"WIN")

    def test_away_x2_under_45_loses_when_home_wins(self):
        self.p.update({"market":"COMPOSITE","selection":"AWAY_X2_U45"})
        self.r.update({"home_score":1,"away_score":0})
        self.assertEqual(settle(self.p,self.r)["outcome"],"LOSS")

    def test_away_x2_under_45_loses_at_five_goals(self):
        self.p.update({"market":"COMPOSITE","selection":"AWAY_X2_U45"})
        self.r.update({"home_score":1,"away_score":4})
        self.assertEqual(settle(self.p,self.r)["outcome"],"LOSS")

    def test_fixture_identity_mismatch_fails_closed(self):
        self.r["away_team_id"]="other"
        with self.assertRaisesRegex(ValueError,"FIXTURE_IDENTITY_MISMATCH"): settle(self.p,self.r)
    def test_unsupported_market_fails_closed(self):
        self.p.update({"market":"ASIAN_HANDICAP","selection":"HOME_-0.5"})
        with self.assertRaisesRegex(ValueError,"UNSUPPORTED_MARKET"): settle(self.p,self.r)
    def test_postponed_pending(self):
        self.r["match_status"]="POSTPONED"
        self.assertEqual(settle(self.p,self.r)["outcome"],"UNSETTLED")

    def test_fractional_final_score_is_rejected_not_truncated(self):
        self.r["home_score"] = 1.5
        with self.assertRaisesRegex(ValueError, "INVALID_FINAL_SCORE"):
            settle(self.p, self.r)

    def test_nonfinite_negative_and_boolean_final_scores_are_rejected(self):
        for invalid in (float("nan"), float("inf"), -1, True, "not-a-score"):
            with self.subTest(invalid=repr(invalid)):
                self.r["home_score"] = invalid
                with self.assertRaisesRegex(ValueError, "INVALID_FINAL_SCORE"):
                    settle(self.p, self.r)

if __name__=="__main__": unittest.main()
