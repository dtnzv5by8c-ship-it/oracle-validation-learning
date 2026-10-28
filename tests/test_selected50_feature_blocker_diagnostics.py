import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from diagnose_selected50_feature_blockers import diagnose, normalize_label  # noqa: E402


def row(fid="1", **overrides):
    base = {
        "fixture_id": fid, "date_utc": "2026-10-31T12:00:00Z", "selected_id": "17404",
        "provider_season_id": "17404", "country": "Italy", "league": "Serie B",
        "home_team": "Arezzo", "away_team": "Ascoli",
        "home_team_provider_id": "2335", "away_team_provider_id": "509",
        "home_recent5_n": "4", "away_recent5_n": "5",
        "feature_support_status": "BLOCKED_MISSING_REQUIRED_FEATURES",
        "missing_required_features": "home_gf5;home_ga5;pair_btts_mean;score_environment",
        "training_support_status": "PASS_ALL_MARKET_MODELS", "unavailable_training_markets": "",
        "COMBO_HOME_probability_pct": "", "COMBO_AWAY_probability_pct": "",
        "production_eligible": "NO",
    }
    base.update(overrides)
    return base


class FeatureBlockerDiagnosticsTests(unittest.TestCase):
    def test_reports_missing_side_features_and_history_shortfall(self):
        sides, _, summary = diagnose([row()])
        self.assertEqual(len(sides), 1)
        self.assertEqual(sides[0]["side"], "home")
        self.assertEqual(sides[0]["oriented_history_count_from_runtime"], 4)
        self.assertEqual(sides[0]["history_count_shortfall"], 1)
        self.assertEqual(sides[0]["missing_side_features"], "home_gf5;home_ga5")
        self.assertEqual(sides[0]["history_support_diagnosis"], "INSUFFICIENT_ORIENTED_HISTORY")
        self.assertEqual(summary["blocked_fixture_rows"], 1)

    def test_both_sides_emit_two_rows_without_imputation(self):
        sides, _, summary = diagnose([row(missing_required_features="home_gf5;away_gf5;pair_btts_mean",
                                           away_recent5_n="3")])
        self.assertEqual({x["side"] for x in sides}, {"home", "away"})
        self.assertEqual(summary["blocked_fixture_side_rows"], 2)
        self.assertTrue(all(x["features_imputed"] == 0 and x["prediction_created"] == 0 for x in sides))

    def test_count_at_minimum_but_feature_missing_is_flagged_not_repaired(self):
        sides, _, summary = diagnose([row(home_recent5_n="5")])
        self.assertEqual(sides[0]["history_support_diagnosis"], "COUNT_MEETS_MINIMUM_BUT_FEATURES_MISSING")
        self.assertEqual(summary["count_meets_minimum_but_features_missing_rows"], 1)
        self.assertEqual(summary["count_contradiction_fixture_ids"], ["1"])

    def test_unknown_history_count_is_not_inferred(self):
        sides, _, summary = diagnose([row(home_recent5_n="")])
        self.assertEqual(sides[0]["history_support_diagnosis"], "HISTORY_COUNT_UNKNOWN")
        self.assertEqual(sides[0]["history_count_shortfall"], "")
        self.assertEqual(summary["unknown_history_count_rows"], 1)

    def test_same_display_name_different_provider_ids_are_not_merged(self):
        _, teams, _ = diagnose([row("1", home_team_provider_id="111"), row("2", home_team_provider_id="222")])
        self.assertEqual(len(teams), 2)
        self.assertNotEqual(teams[0]["source_team_key_not_canonical"], teams[1]["source_team_key_not_canonical"])
        self.assertTrue(all(x["identity_approved"] == "NO" for x in teams))

    def test_same_provider_key_groups_home_and_away_gaps(self):
        a = row("1", home_team_provider_id="2335", missing_required_features="home_gf5", home_recent5_n="4")
        b = row("2", away_team="Arezzo", away_team_provider_id="2335",
                missing_required_features="away_gf5", away_recent5_n="4")
        _, teams, summary = diagnose([a, b])
        team = next(x for x in teams if x["source_team_key_not_canonical"].endswith("provider-team:2335"))
        self.assertEqual(team["blocked_fixture_side_rows"], 2)
        self.assertEqual(team["home_side_gaps"], 1)
        self.assertEqual(team["away_side_gaps"], 1)
        self.assertEqual(summary["blocked_fixture_rows"], 2)

    def test_duplicate_fixture_ids_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "blank or duplicate"):
            diagnose([row("1"), row("1")])

    def test_visible_combo_probability_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Combo probability mask"):
            diagnose([row(COMBO_HOME_probability_pct="67.1")])

    def test_pair_only_block_is_explicitly_unclassified(self):
        sides, _, summary = diagnose([row(missing_required_features="pair_btts_mean;score_environment")])
        self.assertEqual(sides[0]["side"], "PAIR_OR_ENVIRONMENT_ONLY")
        self.assertEqual(summary["unclassified_blocked_fixture_ids"], ["1"])

    def test_nonblocked_rows_are_not_emitted(self):
        sides, teams, summary = diagnose([row(feature_support_status="PASS_ALL_REQUIRED_FEATURES",
                                               prediction_status="RESEARCH_PREDICTION_AVAILABLE")])
        self.assertEqual(sides, [])
        self.assertEqual(teams, [])
        self.assertEqual(summary["blocked_fixture_rows"], 0)

    def test_empty_report_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "contains no fixture rows"):
            diagnose([])

    def test_missing_combo_columns_fails_closed(self):
        r = row()
        r.pop("COMBO_HOME_probability_pct")
        with self.assertRaisesRegex(ValueError, "missing required columns"):
            diagnose([r])

    def test_malformed_history_count_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "must be a non-negative integer"):
            diagnose([row(home_recent5_n="four")])

    def test_runtime_workflow_requires_manual_dispatch_for_private_archive_read(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github/workflows/oracle-selected50-research-runtime.yml").read_text(encoding="utf-8")
        triggers = workflow.split("\npermissions:", 1)[0]
        self.assertIn("workflow_dispatch:", triggers)
        self.assertNotRegex(triggers, r"(?m)^\s{2}push:")

    def test_unicode_normalization_is_grouping_only(self):
        self.assertEqual(normalize_label("Çorum Belediyespor"), "corum belediyespor")
        self.assertEqual(normalize_label("  FC Vizela  "), "fc vizela")


if __name__ == "__main__":
    unittest.main()
