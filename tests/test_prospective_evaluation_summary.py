import unittest
from scripts.summarize_prospective_evaluation import summarize

class ProspectiveEvaluationSummaryTests(unittest.TestCase):
    def test_scores_only_verified_win_loss_rows(self):
        rows=[{"probability":.8,"outcome":"WIN","verified_fixture":True,"verified_result_source":True},{"probability":.7,"outcome":"LOSS","verified_fixture":True,"verified_result_source":True},{"probability":.9,"outcome":"VOID","verified_fixture":True,"verified_result_source":True},{"probability":.5,"outcome":"WIN","verified_fixture":False,"verified_result_source":True}]
        r=summarize(rows)
        self.assertEqual(r["counts"]["settled_win_loss"],2); self.assertEqual(r["metrics"]["hit_rate_wins"],1); self.assertEqual(r["metrics"]["hit_rate_denominator"],2); self.assertEqual(r["counts"]["void_push_excluded"],1); self.assertEqual(r["counts"]["invalid_or_unmatched"],1)
    def test_no_valid_rows_has_no_accuracy(self):
        r=summarize([]); self.assertIsNone(r["metrics"]["hit_rate"]); self.assertEqual(r["metrics"]["hit_rate_denominator"],0)
    def test_unsettled_not_scored(self):
        r=summarize([{"probability":.6,"outcome":"UNSETTLED","verified_fixture":True,"verified_result_source":True}]); self.assertEqual(r["counts"]["unsettled"],1); self.assertEqual(r["metrics"]["hit_rate_denominator"],0)

if __name__=="__main__": unittest.main()
