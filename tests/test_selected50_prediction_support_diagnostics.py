import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "selected50_runtime_support", ROOT / "scripts" / "build_selected50_research_runtime.py"
)
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


class Selected50PredictionSupportDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        self.features = {name: 0.25 for name in runtime.FEATURES}
        self.fits = {market: (object(), 1200) for market in runtime.MARKETS}

    def test_complete_features_and_models_are_reported_as_supported(self):
        result = runtime.prediction_support_diagnostics(self.features, self.fits, True)
        self.assertEqual(result["feature_support_status"], "PASS_ALL_20_REQUIRED_FEATURES")
        self.assertEqual(result["training_support_status"], "PASS_ALL_MARKET_MODELS")
        self.assertEqual(result["prediction_block_reason"], "RESEARCH_PREDICTION_AVAILABLE")
        self.assertEqual(result["prediction_status"], "RAW_RESEARCH_ONLY")
        self.assertEqual(result["missing_required_features"], "")
        self.assertEqual(result["unavailable_training_markets"], "")

    def test_missing_features_are_named_without_imputation(self):
        feature = dict(self.features)
        feature["home_gf5"] = None
        result = runtime.prediction_support_diagnostics(feature, self.fits, False)
        self.assertEqual(result["feature_support_status"], "BLOCKED_MISSING_REQUIRED_FEATURES")
        self.assertEqual(result["missing_required_features"], "home_gf5")
        self.assertEqual(result["training_support_status"], "PASS_ALL_MARKET_MODELS")
        self.assertEqual(result["prediction_block_reason"], "BLOCKED_MISSING_REQUIRED_FEATURES")
        self.assertEqual(result["prediction_status"], "BLOCKED_MISSING_REQUIRED_FEATURES")

    def test_training_gate_is_distinguished_from_feature_gate(self):
        fits = {market: (None, 299) for market in runtime.MARKETS}
        result = runtime.prediction_support_diagnostics(self.features, fits, False)
        self.assertEqual(result["feature_support_status"], "PASS_ALL_20_REQUIRED_FEATURES")
        self.assertEqual(result["training_support_status"], "BLOCKED_ALL_MARKET_MODELS_UNAVAILABLE")
        self.assertEqual(result["unavailable_training_markets"], ";".join(runtime.MARKETS))
        self.assertEqual(
            result["training_eligible_rows_by_market"],
            ";".join(f"{market}:299" for market in runtime.MARKETS),
        )
        self.assertEqual(result["prediction_block_reason"], "BLOCKED_MODEL_TRAINING_GATE")
        self.assertEqual(result["prediction_status"], "BLOCKED_MODEL_TRAINING_GATE")

    def test_unclassified_no_prediction_fails_closed_with_explicit_status(self):
        result = runtime.prediction_support_diagnostics(self.features, self.fits, False)
        self.assertEqual(result["prediction_block_reason"], "BLOCKED_UNCLASSIFIED_NO_PREDICTION")
        self.assertEqual(result["prediction_status"], "BLOCKED_UNCLASSIFIED_NO_PREDICTION")

    def test_combined_gate_failure_is_explicit(self):
        feature = dict(self.features)
        feature["away_sot5"] = None
        fits = dict(self.fits)
        fits["COMBO_AWAY"] = (None, 0)
        result = runtime.prediction_support_diagnostics(feature, fits, False)
        self.assertEqual(result["prediction_block_reason"], "BLOCKED_MISSING_FEATURES_AND_TRAINING_GATE")
        self.assertEqual(result["prediction_status"], "BLOCKED_MISSING_FEATURES_AND_TRAINING_GATE")
        self.assertEqual(result["unavailable_training_markets"], "COMBO_AWAY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
