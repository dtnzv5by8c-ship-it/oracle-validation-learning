import unittest
from scripts.validate_prospective_settlement import validate_settlement

class ProspectiveSettlementTests(unittest.TestCase):
    def setUp(self):
        self.event = {"prediction_id":"p-1", "fixture_id":"f-1", "outcome":"WIN", "settled_at_utc":"2026-10-23T12:00:00Z", "result_source":"verified-source", "settlement_rule_version":"1"}
        self.predictions = {"p-1"}; self.fixtures = {"f-1"}
    def test_verified_win_is_scorable(self):
        self.assertTrue(validate_settlement(self.event,self.predictions,self.fixtures)["scorable"])
    def test_unknown_prediction_rejected(self):
        self.event["prediction_id"]="unknown"
        with self.assertRaisesRegex(ValueError,"UNKNOWN_PREDICTION_ID"): validate_settlement(self.event,self.predictions,self.fixtures)
    def test_unverified_fixture_rejected(self):
        self.event["fixture_id"]="unknown"
        with self.assertRaisesRegex(ValueError,"UNVERIFIED_FIXTURE_ID"): validate_settlement(self.event,self.predictions,self.fixtures)
    def test_unsettled_remains_pending(self):
        self.event["outcome"]="UNSETTLED"
        result=validate_settlement(self.event,self.predictions,self.fixtures)
        self.assertEqual(result["status"],"PENDING"); self.assertFalse(result["scorable"])
    def test_void_not_scorable_as_loss(self):
        self.event["outcome"]="VOID"
        result=validate_settlement(self.event,self.predictions,self.fixtures)
        self.assertFalse(result["scorable"])
    def test_unknown_outcome_rejected(self):
        self.event["outcome"]="MAYBE"
        with self.assertRaisesRegex(ValueError,"INVALID_SETTLEMENT_OUTCOME"): validate_settlement(self.event,self.predictions,self.fixtures)

if __name__ == "__main__": unittest.main()
