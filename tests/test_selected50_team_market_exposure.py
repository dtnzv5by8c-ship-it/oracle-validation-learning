import unittest
from datetime import datetime, timezone
from scripts.analyze_selected50_team_market_exposure import analyze

PROVENANCE = {
    "generated_utc": "2026-10-30T00:00:00Z",
    "snapshot_retrieved_utc": "2026-10-29T23:00:00Z",
    "runtime_run_id": "test-run",
    "runtime_run_number": "1",
    "overlay_archive_sha256": "a" * 64,
    "runtime_archive_consumption_verified": True,
}


def fixture(fid="f1", home_id="h1", away_id="a1", home_name="Home", away_name="Away",
            date="2026-10-30T10:00:00Z", status="RAW_RESEARCH_ONLY",
            home_form="WWDLW", away_form="LLDWL", home_n=5, away_n=5,
            btts=61.0, dc_home=72.0, dc_away=48.0):
    return {
        "fixture_id": fid, "date_utc": date, "selected_id": "season-x",
        "country": "Testland", "league": "Test League",
        "home_team_provider_id": home_id, "away_team_provider_id": away_id,
        "home_team": home_name, "away_team": away_name,
        "home_recent5_results": home_form, "away_recent5_results": away_form,
        "home_recent5_n": str(home_n), "away_recent5_n": str(away_n),
        "prediction_status": status,
        "feature_support_status": "PASS_ALL_20_REQUIRED_FEATURES" if status == "RAW_RESEARCH_ONLY" else "BLOCKED_MISSING_REQUIRED_FEATURES",
        "BTTS_probability_pct": str(btts) if btts is not None else "",
        "DC_HOME_probability_pct": str(dc_home) if dc_home is not None else "",
        "DC_AWAY_probability_pct": str(dc_away) if dc_away is not None else "",
        "canonical_fixture_join_status": "NOT_VERIFIED",
        "canonical_team_join_status": "NOT_VERIFIED",
        "settlement_truth_status": "NOT_VERIFIED_AGAINST_PRODUCTION_MARKET_SPEC",
        "production_eligible": "NO",
        "calibration_status": "RAW_ONLY_UNCALIBRATED",
    }


class TeamMarketExposureTests(unittest.TestCase):
    def setUp(self):
        self.as_of = datetime(2026, 10, 30, 1, 0, tzinfo=timezone.utc)

    def test_builds_two_role_profiles_and_exposure_rows(self):
        teams, markets, leagues, summary = analyze([fixture()], PROVENANCE, self.as_of)
        self.assertEqual(len(teams), 2)
        self.assertEqual(len(markets), 4)
        self.assertEqual(len(leagues), 1)
        self.assertEqual(summary["fixture_context"]["distinct_provider_team_ids"], 2)
        home = next(x for x in teams if x["fixture_role"] == "HOME")
        away = next(x for x in teams if x["fixture_role"] == "AWAY")
        self.assertEqual(home["latest_form_win_rate_pct"], 60.0)
        self.assertEqual(home["dc_team_side_mean_probability_pct"], 72.0)
        self.assertEqual(away["dc_team_side_mean_probability_pct"], 48.0)

    def test_btts_is_marked_shared_fixture_probability_not_team_accuracy(self):
        teams, markets, leagues, summary = analyze([fixture()], PROVENANCE, self.as_of)
        btts = [x for x in markets if x["market_exposure"] == "BTTS_FIXTURE_EXPOSURE"]
        self.assertEqual(len(btts), 2)
        self.assertTrue(all("shared by both participating teams" in x["probability_scope"] for x in btts))
        self.assertFalse(summary["interpretation"]["performance_metrics_computed"])

    def test_blocked_fixture_counts_as_exposure_but_not_probability(self):
        row = fixture(status="BLOCKED_MISSING_REQUIRED_FEATURES", btts=None, dc_home=None, dc_away=None)
        teams, markets, leagues, summary = analyze([row], PROVENANCE, self.as_of)
        self.assertTrue(all(x["blocked_appearances"] == 1 for x in teams))
        self.assertTrue(all(x["probability_observations"] == 0 for x in markets))
        self.assertEqual(summary["prediction_and_market_coverage"]["prediction_status_counts"]["BLOCKED_MISSING_REQUIRED_FEATURES"], 1)

    def test_latest_context_selected_chronologically(self):
        rows = [
            fixture(fid="f1", date="2026-10-30T10:00:00Z", home_form="LLDDD"),
            fixture(fid="f2", date="2026-10-31T10:00:00Z", home_form="WWWWW"),
        ]
        teams, _, _, _ = analyze(rows, PROVENANCE, self.as_of)
        home = next(x for x in teams if x["fixture_role"] == "HOME")
        self.assertEqual(home["fixture_appearances"], 2)
        self.assertEqual(home["latest_form_sequence"], "WWWWW")
        self.assertEqual(home["distinct_form_sequences_across_fixture_contexts"], 2)

    def test_duplicate_fixture_ids_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "unique"):
            analyze([fixture(), fixture()], PROVENANCE, self.as_of)

    def test_missing_provider_team_identity_fails_closed(self):
        row = fixture()
        row["home_team_provider_id"] = ""
        with self.assertRaisesRegex(ValueError, "Missing provider team ID"):
            analyze([row], PROVENANCE, self.as_of)

    def test_unverified_provenance_fails_closed(self):
        provenance = dict(PROVENANCE, runtime_archive_consumption_verified=False)
        with self.assertRaisesRegex(ValueError, "provenance"):
            analyze([fixture()], provenance, self.as_of)


if __name__ == "__main__":
    unittest.main(verbosity=2)
