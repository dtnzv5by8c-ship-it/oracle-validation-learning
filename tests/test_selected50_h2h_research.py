import math
import unittest

from scripts.build_selected50_research_runtime import (
    FEATURES,
    make_model_for_features,
    predict_for_features,
    h2h_prior_meetings,
    h2h_result_from_target_home_perspective,
    h2h_duplicate_signature_diagnostics,
    valid_completed_score,
    completed_fixture_signature_key,
    market_targets_for_match,
    team_ids,
    provider_fixture_id_collision_diagnostics,
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

    def test_h2h_prior_meetings_excludes_same_kickoff_and_future(self):
        history = [
            (100, {"fixture_id": "old"}),
            (200, {"fixture_id": "same-time"}),
            (300, {"fixture_id": "future"}),
        ]
        prior = h2h_prior_meetings(history, 200)
        self.assertEqual([row["fixture_id"] for _, row in prior], ["old"])

    def test_h2h_prior_meetings_allows_all_strictly_earlier_rows(self):
        history = [(100, {"fixture_id": "a"}), (150, {"fixture_id": "b"})]
        self.assertEqual(len(h2h_prior_meetings(history, 151)), 2)

    def test_h2h_result_is_from_target_home_team_perspective(self):
        target_home_id = "A"
        old_when_target_home_was_home = {"home_id": "A", "away_id": "B", "home_goals": 2, "away_goals": 1}
        old_when_target_home_was_away = {"home_id": "B", "away_id": "A", "home_goals": 0, "away_goals": 1}
        old_draw = {"home_id": "B", "away_id": "A", "home_goals": 2, "away_goals": 2}
        self.assertEqual(h2h_result_from_target_home_perspective(old_when_target_home_was_home, target_home_id), "W")
        self.assertEqual(h2h_result_from_target_home_perspective(old_when_target_home_was_away, target_home_id), "W")
        self.assertEqual(h2h_result_from_target_home_perspective(old_draw, target_home_id), "D")

    def test_h2h_result_rejects_unrelated_team(self):
        unrelated = {"home_id": "X", "away_id": "Y", "home_goals": 1, "away_goals": 0}
        with self.assertRaises(ValueError):
            h2h_result_from_target_home_perspective(unrelated, "A")

    def test_valid_completed_score_requires_finite_nonnegative_integer_goals(self):
        self.assertTrue(valid_completed_score(2, 1))
        self.assertTrue(valid_completed_score(0, 0))
        self.assertFalse(valid_completed_score(2.5, 1))
        self.assertFalse(valid_completed_score(-1, 0))
        self.assertFalse(valid_completed_score(float("nan"), 1))
        self.assertFalse(valid_completed_score(None, 1))

    def test_duplicate_signature_detects_different_fixture_ids(self):
        matches = [
            {"competition_id": "C", "kickoff_unix": 1000, "home_id": "A", "away_id": "B",
             "home_goals": 2, "away_goals": 1, "finished": True, "fixture_id": "f1"},
            {"competition_id": "C", "kickoff_unix": 1000, "home_id": "A", "away_id": "B",
             "home_goals": 2, "away_goals": 1, "finished": True, "fixture_id": "f2"},
        ]
        qa = h2h_duplicate_signature_diagnostics(matches)
        self.assertEqual(qa["duplicate_signature_groups"], 1)
        self.assertEqual(qa["duplicate_extra_rows"], 1)
        self.assertEqual(qa["conflicting_score_groups"], 0)

    def test_duplicate_signature_normalizes_reversed_home_away_score(self):
        matches = [
            {"competition_id": "C", "kickoff_unix": 1000, "home_id": "A", "away_id": "B",
             "home_goals": 2, "away_goals": 1, "finished": True, "fixture_id": "f1"},
            {"competition_id": "C", "kickoff_unix": 1000, "home_id": "B", "away_id": "A",
             "home_goals": 1, "away_goals": 2, "finished": True, "fixture_id": "f2"},
        ]
        qa = h2h_duplicate_signature_diagnostics(matches)
        self.assertEqual(qa["duplicate_signature_groups"], 1)
        self.assertEqual(qa["conflicting_score_groups"], 0)

    def test_duplicate_signature_flags_conflicting_score(self):
        matches = [
            {"competition_id": "C", "kickoff_unix": 1000, "home_id": "A", "away_id": "B",
             "home_goals": 2, "away_goals": 1, "finished": True, "fixture_id": "f1"},
            {"competition_id": "C", "kickoff_unix": 1000, "home_id": "B", "away_id": "A",
             "home_goals": 0, "away_goals": 2, "finished": True, "fixture_id": "f2"},
        ]
        qa = h2h_duplicate_signature_diagnostics(matches)
        self.assertEqual(qa["duplicate_signature_groups"], 1)
        self.assertEqual(qa["conflicting_score_groups"], 1)

    def test_duplicate_signatures_are_quarantined_from_market_labels(self):
        matches = [
            {"competition_id": "C", "kickoff_unix": 1000, "home_id": "A", "away_id": "B",
             "home_goals": 2, "away_goals": 1, "finished": True, "fixture_id": "f1"},
            {"competition_id": "C", "kickoff_unix": 1000, "home_id": "B", "away_id": "A",
             "home_goals": 1, "away_goals": 2, "finished": True, "fixture_id": "f2"},
        ]
        qa = h2h_duplicate_signature_diagnostics(matches)
        excluded = set(qa["duplicate_signature_keys"])
        self.assertEqual(len(excluded), 1)
        for match in matches:
            with self.subTest(fixture=match["fixture_id"]):
                self.assertTrue(all(value is None for value in market_targets_for_match(match, excluded).values()))

    def test_duplicate_signatures_are_excluded_from_historical_signature_key(self):
        valid = {"competition_id": "C", "kickoff_unix": 1000, "home_id": "A", "away_id": "B",
                 "home_goals": 2, "away_goals": 1, "finished": True}
        self.assertEqual(completed_fixture_signature_key(valid), ("C", 1000.0, ("A", "B")))
        self.assertIsNone(completed_fixture_signature_key({**valid, "finished": False}))
        self.assertIsNone(completed_fixture_signature_key({**valid, "home_id": "A", "away_id": "A"}))

    def test_boolean_values_are_not_accepted_as_goal_counts(self):
        self.assertFalse(valid_completed_score(True, 1))
        self.assertFalse(valid_completed_score(0, False))

    def test_provider_team_ids_are_trimmed_before_identity_checks(self):
        home_id, away_id = team_ids({"homeID": " 123 ", "awayID": "123"})
        self.assertEqual(home_id, "123")
        self.assertEqual(away_id, "123")
        # After normalization, a whitespace-variant self-fixture cannot form a signature.
        self.assertIsNone(completed_fixture_signature_key({
            "finished": True,
            "home_goals": 1,
            "away_goals": 0,
            "home_id": home_id,
            "away_id": away_id,
            "kickoff_unix": 1000,
            "competition_id": "C",
        }))


    def test_same_fixture_id_exact_duplicate_is_reported_for_safe_deduplication(self):
        rows = [
            {"competition_id": "C", "fixture_id": "same", "kickoff_unix": 1000,
             "home_id": "A", "away_id": "B", "home_goals": 2, "away_goals": 1, "finished": True},
            {"competition_id": "C", "fixture_id": "same", "kickoff_unix": 1000,
             "home_id": "B", "away_id": "A", "home_goals": 1, "away_goals": 2, "finished": True},
        ]
        qa = provider_fixture_id_collision_diagnostics(rows)
        self.assertEqual(qa["duplicate_fixture_id_groups"], 1)
        self.assertEqual(qa["exact_duplicate_fixture_id_groups"], 1)
        self.assertEqual(qa["exact_duplicate_fixture_id_extra_rows_deduplicated"], 1)
        self.assertEqual(qa["conflicting_fixture_id_groups"], 0)

    def test_same_fixture_id_with_conflicting_score_is_quarantined(self):
        rows = [
            {"competition_id": "C", "fixture_id": "same", "kickoff_unix": 1000,
             "home_id": "A", "away_id": "B", "home_goals": 2, "away_goals": 1, "finished": True},
            {"competition_id": "C", "fixture_id": "same", "kickoff_unix": 1000,
             "home_id": "B", "away_id": "A", "home_goals": 1, "away_goals": 0, "finished": True},
        ]
        qa = provider_fixture_id_collision_diagnostics(rows)
        self.assertEqual(qa["conflicting_fixture_id_groups"], 1)
        self.assertEqual(qa["conflicting_fixture_id_rows_quarantined"], 2)
        self.assertEqual(qa["conflicting_fixture_id_keys"], [("C", "same")])

    def test_same_fixture_id_with_different_kickoff_is_quarantined(self):
        base = {"competition_id": "C", "fixture_id": "same", "home_id": "A", "away_id": "B",
                "home_goals": 2, "away_goals": 1, "finished": True}
        rows = [{**base, "kickoff_unix": 1000}, {**base, "kickoff_unix": 2000}]
        qa = provider_fixture_id_collision_diagnostics(rows)
        self.assertEqual(qa["conflicting_fixture_id_groups"], 1)
        self.assertEqual(qa["conflicting_fixture_id_rows_quarantined"], 2)


if __name__ == "__main__":
    unittest.main()
