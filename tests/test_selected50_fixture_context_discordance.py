#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "analyze_selected50_fixture_context_discordance.py"
spec = importlib.util.spec_from_file_location("fixture_context_discordance", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def row(**overrides):
    base = {
        "fixture_id": "F1", "date_utc": "2026-11-01T12:00:00+00:00",
        "country": "Testland", "league": "Test League", "home_team": "Home FC", "away_team": "Away FC",
        "home_team_provider_id": "1", "away_team_provider_id": "2",
        "home_recent5_results": "WWWWW", "away_recent5_results": "LLLLL",
        "home_recent5_n": "5", "away_recent5_n": "5",
        "h2h_last5_results_home_perspective": "WDL", "h2h_prior_n": "3",
        "h2h_btts_rate_last5": "0.3333333333", "h2h_avg_total_goals_last5": "2.0",
        "h2h_last_date_utc": "2026-08-01T12:00:00+00:00",
        "prediction_status": "RAW_RESEARCH_ONLY", "BTTS_probability_pct": "55",
        "DC_HOME_probability_pct": "75", "DC_AWAY_probability_pct": "50",
        "canonical_fixture_join_status": "NOT_VERIFIED", "canonical_team_join_status": "NOT_VERIFIED",
        "settlement_truth_status": "NOT_VERIFIED", "calibration_status": "RAW_ONLY_UNCALIBRATED",
        "odds_xg_provenance_status": "UNVERIFIED_NOT_USED_IN_MODEL",
    }
    base.update(overrides)
    return base


class FixtureContextDiscordanceTests(unittest.TestCase):
    def test_dc_preference_against_recent_form_is_flagged(self):
        r = row(home_recent5_results="LLLLL", away_recent5_results="WWWWW",
                DC_HOME_probability_pct="75", DC_AWAY_probability_pct="50")
        out, summary = mod.analyze([r])
        self.assertEqual(out[0]["dc_form_disagreement_flag"], 1)
        self.assertEqual(summary["context_flag_counts_nonexclusive"]["dc_preference_vs_recent_form_disagreement"], 1)

    def test_dc_disagreement_not_flagged_below_threshold(self):
        r = row(home_recent5_results="LLLLL", away_recent5_results="WWWWW",
                DC_HOME_probability_pct="58", DC_AWAY_probability_pct="50")
        out, _ = mod.analyze([r])
        self.assertEqual(out[0]["dc_form_disagreement_flag"], 0)

    def test_btts_h2h_gap_requires_minimum_displayed_context(self):
        r = row(BTTS_probability_pct="70", h2h_btts_rate_last5="0.0",
                h2h_last5_results_home_perspective="WDL")
        out, _ = mod.analyze([r])
        self.assertEqual(out[0]["btts_h2h_gap_flag"], 1)
        r2 = row(BTTS_probability_pct="70", h2h_btts_rate_last5="0.0",
                 h2h_last5_results_home_perspective="WD")
        out2, _ = mod.analyze([r2])
        self.assertEqual(out2[0]["btts_h2h_gap_flag"], 0)

    def test_blocked_prediction_does_not_receive_model_discordance_flag(self):
        r = row(prediction_status="BLOCKED_MISSING_REQUIRED_FEATURES",
                BTTS_probability_pct="", DC_HOME_probability_pct="", DC_AWAY_probability_pct="",
                home_recent5_results="LLLLL", away_recent5_results="WWWWW")
        out, summary = mod.analyze([r])
        self.assertEqual(out[0]["dc_form_disagreement_flag"], 0)
        self.assertEqual(summary["blocked_missing_required_feature_rows"], 1)

    def test_h2h_date_must_precede_fixture(self):
        r = row(h2h_last_date_utc="2026-11-01T12:00:00+00:00")
        out, summary = mod.analyze([r])
        self.assertEqual(out[0]["h2h_date_pre_kickoff_check"], "VIOLATION")
        self.assertEqual(summary["h2h_date_at_or_after_fixture_violations"], 1)

    def test_duplicate_fixture_ids_fail_closed(self):
        with self.assertRaises(ValueError):
            mod.analyze([row(), row()])

    def test_internal_provider_team_name_collision_is_counted_not_canonicalized(self):
        a = row(fixture_id="F1", home_team_provider_id="1", home_team="Home FC")
        b = row(fixture_id="F2", home_team_provider_id="1", home_team="Different Home Name")
        _, summary = mod.analyze([a, b])
        self.assertEqual(summary["provider_team_ids_with_multiple_names_in_snapshot"], 1)
        self.assertFalse(summary["production_eligible"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
