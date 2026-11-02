import unittest
from datetime import date, timedelta

import numpy as np

from scripts.calibrate_run8_selected50_venue_models import (
    temporal_windows, fit_calibrator, apply_calibrator, calibration_slope_intercept,
    COMPARISONS, MODEL_FEATURES,
)


class TestRun8ChronologicalCalibration(unittest.TestCase):
    def test_calibration_window_is_disjoint_and_immediately_precedes_test(self):
        test_start = date(2025, 10, 1)
        test_end = date(2026, 4, 1)
        windows = temporal_windows(test_start, test_end, calibration_days=90)
        self.assertEqual(windows["calibration_end_exclusive"], test_start)
        self.assertEqual(windows["calibration_start"], test_start - timedelta(days=90))
        self.assertEqual(windows["train_end_exclusive"], windows["calibration_start"])
        self.assertLess(windows["train_end_exclusive"], windows["calibration_start"])
        self.assertLess(windows["calibration_end_exclusive"], windows["test_end_exclusive"])

    def test_platt_calibrator_fits_only_supplied_calibration_sample(self):
        p = np.linspace(0.03, 0.97, 800)
        y = (p > 0.48).astype(int)
        model, status = fit_calibrator("platt", p, y, min_calibration_n=500)
        self.assertEqual(status, "FITTED")
        calibrated = apply_calibrator("platt", model, p)
        self.assertEqual(len(calibrated), len(p))
        self.assertTrue(np.all((calibrated >= 0) & (calibrated <= 1)))

    def test_isotonic_calibrator_is_bounded_and_monotone(self):
        rng = np.random.default_rng(7)
        p = rng.uniform(0.02, 0.98, 1000)
        y = (rng.uniform(size=1000) < p).astype(int)
        model, status = fit_calibrator("isotonic", p, y, min_calibration_n=500)
        self.assertEqual(status, "FITTED")
        grid = np.linspace(0.01, 0.99, 100)
        calibrated = apply_calibrator("isotonic", model, grid)
        self.assertTrue(np.all((calibrated >= 0) & (calibrated <= 1)))
        self.assertTrue(np.all(np.diff(calibrated) >= -1e-12))

    def test_calibration_is_blocked_below_minimum_or_with_one_class(self):
        p = np.linspace(0.1, 0.9, 100)
        y = np.array([0, 1] * 50)
        model, status = fit_calibrator("platt", p, y, min_calibration_n=500)
        self.assertIsNone(model)
        self.assertTrue(status.startswith("CALIBRATION_N_BELOW_MINIMUM"))
        p = np.linspace(0.1, 0.9, 600)
        y = np.ones(600, dtype=int)
        model, status = fit_calibrator("isotonic", p, y, min_calibration_n=500)
        self.assertIsNone(model)
        self.assertEqual(status, "CALIBRATION_WINDOW_HAS_ONE_OUTCOME_CLASS")

    def test_calibration_diagnostic_is_finite_for_two_class_sample(self):
        p = np.linspace(0.05, 0.95, 600)
        y = (np.sin(np.arange(600) / 10) > 0).astype(int)
        intercept, slope = calibration_slope_intercept(y, p)
        self.assertTrue(np.isfinite(intercept))
        self.assertTrue(np.isfinite(slope))

    def test_models_use_same_venue_eligible_cohort_and_only_allowed_features(self):
        self.assertEqual(set(MODEL_FEATURES), {"league_only", "overall_form_only", "main_effects"})
        self.assertNotIn("xg", str(MODEL_FEATURES).lower())
        self.assertNotIn("league_position", str(MODEL_FEATURES).lower())

    def test_comparisons_include_calibration_and_nested_venue_tests(self):
        names = {row[0] for row in COMPARISONS}
        self.assertIn("main_effects_platt_vs_raw", names)
        self.assertIn("main_effects_isotonic_vs_raw", names)
        self.assertIn("main_effects_platt_vs_overall_form_platt", names)
        self.assertIn("main_effects_platt_vs_league_only_platt", names)
        self.assertNotIn("oracle_v16", str(COMPARISONS).lower())

    def test_calibrator_refuses_unknown_method(self):
        with self.assertRaises(ValueError):
            fit_calibrator("temperature", [0.2, 0.8], [0, 1], min_calibration_n=2)


if __name__ == "__main__":
    unittest.main()
