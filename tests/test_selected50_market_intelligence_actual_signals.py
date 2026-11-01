import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import analyze_selected50_market_intelligence_actual_signals as signal


class TestSelected50MarketIntelligenceActualSignals(unittest.TestCase):
    def test_bh_adjust_is_monotone_and_restores_input_order(self):
        q = signal.bh_adjust(np.array([0.01, 0.04, 0.03]))
        np.testing.assert_allclose(q, np.array([0.03, 0.04, 0.04]))

    def test_auc_binary_direction(self):
        y = np.array([0, 0, 1, 1])
        self.assertAlmostEqual(signal.auc_binary(y, np.array([0.1, 0.2, 0.8, 0.9])), 1.0)
        self.assertAlmostEqual(signal.auc_binary(y, np.array([0.9, 0.8, 0.2, 0.1])), 0.0)

    def test_bootstrap_spearman_ci_captures_strong_positive_signal(self):
        x = np.arange(1, 31, dtype=float)
        y = x + np.random.default_rng(12).normal(0, 4, size=len(x))
        lo, hi = signal.bootstrap_spearman(x, y, 200, np.random.default_rng(4))
        self.assertGreater(lo, 0.5)
        self.assertGreaterEqual(hi, lo)

    def test_strict_sample_excludes_schedule_history_and_cutoff_failures(self):
        base = {
            "schedule_reconciliation_status": "MATCH",
            "home_form_n": 5,
            "away_form_n": 5,
            "home_at_home_form_n": 5,
            "away_away_form_n": 5,
            "history_cutoff_utc": "2026-10-31T12:00:00Z",
            "runtime_kickoff_utc": "2026-10-31T13:00:00Z",
            "history_cutoff_rule": "STRICTLY_BEFORE_FIXTURE_KICKOFF",
            "league_table_status": "PROVISIONAL_CONVENTIONAL_TABLE",
            "league": "Test League",
        }
        rows = [
            dict(base, fixture_id="1"),
            dict(base, fixture_id="2", home_form_n=4),
            dict(base, fixture_id="3", schedule_reconciliation_status="REVIEW_REQUIRED"),
            dict(base, fixture_id="4", history_cutoff_utc="2026-10-31T14:00:00Z"),
        ]
        clean, strict, venue, qa = signal.select_strict_sample(pd.DataFrame(rows), 5)
        self.assertEqual(len(clean), 3)
        self.assertEqual(len(strict), 1)
        self.assertEqual(len(venue), 1)
        self.assertEqual(qa["schedule_review_rows_excluded"], 1)
        self.assertEqual(qa["clean_rows_with_home_history_below_minimum"], 1)
        self.assertEqual(qa["strict_history_cutoff_invalid_or_late_rows"], 1)

    def test_engineered_venue_signals_require_five_venue_matches(self):
        row = {c: 1.0 for c in signal.BASE_FEATURES}
        row.update({
            "home_form_n": 5, "away_form_n": 5,
            "home_at_home_form_n": 4, "away_away_form_n": 5,
            "home_form_ppg": 2.0, "away_form_ppg": 1.0,
            "home_form_gf_avg": 2.0, "away_form_ga_avg": 1.5,
            "away_form_gf_avg": 1.0, "home_form_ga_avg": 1.2,
            "home_at_home_avg_points": 2.2, "away_away_avg_points": 1.1,
            "home_at_home_avg_goals_for": 2.0, "away_away_avg_goals_for": 1.0,
            "home_at_home_avg_goals_against": 0.8, "away_away_avg_goals_against": 1.4,
            "home_form_btts_rate": 0.6, "away_form_btts_rate": 0.5,
            "home_form_over25_rate": 0.7, "away_form_over25_rate": 0.4,
            "home_team_over15_rate": 0.6, "away_team_over15_rate": 0.5,
            "actual_match_result": "HOME_WIN", "actual_btts": "YES",
            "actual_over_1_5": "YES", "actual_over_2_5": "YES", "actual_under_4_5": "YES",
            "actual_home_goals": 2, "actual_away_goals": 1,
        })
        out = signal.engineer_features(pd.DataFrame([row]))
        self.assertTrue(pd.isna(out.loc[0, "venue_ppg_diff"]))
        self.assertAlmostEqual(out.loc[0, "overall_ppg_diff"], 1.0)
        self.assertAlmostEqual(out.loc[0, "home_strength_x_away_weakness"], 1.5)

    def test_fixture_diagnostics_preserves_rows_and_marks_research_only(self):
        df = pd.DataFrame({
            "fixture_date_utc": ["2026-10-31T10:00:00Z", "2026-10-31T11:00:00Z"],
            "league": ["L1", "L2"], "runtime_fixture": ["A v B", "C v D"],
            "fixture_id": ["F1", "F2"], "overall_ppg_diff": [-1.0, 1.0],
            "home_strength_x_away_weakness": [-0.5, 1.5],
        })
        out = signal.fixture_diagnostics_table(df)
        self.assertEqual(len(out), 2)
        self.assertEqual(out["production_eligible"].tolist(), [False, False])
        self.assertEqual(out["betting_eligible"].tolist(), [False, False])
        self.assertEqual(out["home_strength_x_away_weakness_quartile"].notna().sum(), 2)

    def test_probability_table_reports_paired_intervals_and_auc_interval(self):
        n = 40
        y = np.array([0, 1] * 20)
        df = pd.DataFrame({
            "BTTS Yes": np.where(y == 1, 70, 30),
            "Home 1X": np.where(y == 1, 75, 25),
            "Away X2": np.where(y == 1, 65, 35),
            "over15_probability_pct": np.where(y == 1, 80, 20),
            "over25_probability_pct": np.where(y == 1, 70, 30),
            "under45_probability_pct": np.where(y == 1, 75, 25),
            "home_over15_probability_pct": np.where(y == 1, 70, 30),
            "away_over15_probability_pct": np.where(y == 1, 65, 35),
            "y_btts": y, "y_home_1x": y, "y_away_x2": y,
            "y_over15": y, "y_over25": y, "y_under45": y,
            "y_home_over15": y, "y_away_over15": y,
        })
        out = signal.probability_table(df, 100, 3)
        self.assertEqual(len(out), 8)
        self.assertIn("brier_improvement_ci95_low", out.columns)
        self.assertIn("logloss_improvement_ci95_high", out.columns)
        self.assertIn("auc_ci95_low", out.columns)
        self.assertIn("ece10", out.columns)

    def test_exact_identity_join_fails_closed_on_duplicate_actuals(self):
        keys = {
            "provider_season_id": "S1", "fixture_id": "F1",
            "home_team_provider_id": "H1", "away_team_provider_id": "A1",
        }
        actual = pd.DataFrame([dict(keys, settlement_status=signal.SETTLED)])
        trace = pd.DataFrame([{
            "runtime_provider_season_id": "S1", "fixture_id": "F1",
            "runtime_home_team_id": "H1", "runtime_away_team_id": "A1",
            "runtime_fixture": "Home v Away", "runtime_league": "Test League",
        }])
        mi = pd.DataFrame([{"Fixture": "Home v Away", "League": "Test League", "BTTS Yes": 50, "Home 1X": 50, "Away X2": 50}])
        goal = pd.DataFrame([{
            "provider_season_id": "S1", "fixture_id": "F1", "home_team_id": "H1", "away_team_id": "A1",
            "forecast_status": "EXPERIMENTAL_UNCALIBRATED",
        }])
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            actual.to_csv(td / "actual.csv", index=False)
            trace.to_csv(td / "trace.csv", index=False)
            mi.to_csv(td / "mi.csv", index=False)
            goal.to_csv(td / "goal.csv", index=False)
            joined, qa = signal.load_and_join(td / "actual.csv", td / "mi.csv", td / "trace.csv", td / "goal.csv")
            self.assertEqual(len(joined), 1)
            self.assertEqual(qa["goal_research_exact_join_rows"], 1)
            pd.concat([actual, actual]).to_csv(td / "actual.csv", index=False)
            with self.assertRaises(ValueError):
                signal.load_and_join(td / "actual.csv", td / "mi.csv", td / "trace.csv", td / "goal.csv")


if __name__ == "__main__":
    unittest.main()
