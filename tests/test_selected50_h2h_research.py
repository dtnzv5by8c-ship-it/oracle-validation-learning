import math
import unittest

from scripts.build_selected50_research_runtime import (
    FEATURES,
    make_model_for_features,
    predict_for_features,
)


class H2HResearchFeatureContractTests(unittest.TestCase):
    def rows(self, n=320):
        rows = []
        for i in range(n):
            row = {name: float((i % 7) + (j * 0.1)) for j, name in enumerate(FEATURES)}
            row.update({
                "target_BTTS": int(i % 3 != 0),
                "h2h_prior_n": float(i % 6),
                "h2h_btts_rate_last5": float((i % 5) / 4),
                "h2h_avg_total_goals_last5": float(1 + (i % 4)),
                "h2h_days_since_last": float(30 + i),
            })
            rows.append(row)
        return rows

    def test_candidate_requires_h2h_features_and_fits_separately(self):
        rows = self.rows()
        names = FEATURES + [
            "h2h_prior_n",
            "h2h_btts_rate_last5",
            "h2h_avg_total_goals_last5",
            "h2h_days_since_last",
        ]
        model, n = make_model_for_features(rows, "BTTS", names)
        self.assertIsNotNone(model)
        self.assertEqual(n, len(rows))
        self.assertIsNotNone(predict_for_features(model, rows[0], names))

    def test_candidate_does_not_impute_missing_h2h(self):
        rows = self.rows()
        names = FEATURES + [
            "h2h_prior_n",
            "h2h_btts_rate_last5",
            "h2h_avg_total_goals_last5",
            "h2h_days_since_last",
        ]
        rows[0]["h2h_btts_rate_last5"] = None
        model, n = make_model_for_features(rows, "BTTS", names)
        self.assertEqual(n, len(rows) - 1)
        self.assertIsNone(predict_for_features(model, rows[0], names))

    def test_nonfinite_h2h_values_are_rejected(self):
        rows = self.rows()
        names = FEATURES + [
            "h2h_prior_n",
            "h2h_btts_rate_last5",
            "h2h_avg_total_goals_last5",
            "h2h_days_since_last",
        ]
        rows[0]["h2h_days_since_last"] = math.inf
        model, n = make_model_for_features(rows, "BTTS", names)
        self.assertEqual(n, len(rows) - 1)
        self.assertIsNone(predict_for_features(model, rows[0], names))


if __name__ == "__main__":
    unittest.main()
