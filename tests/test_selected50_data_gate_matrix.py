import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "oracle_selected50_data_gate_matrix_2026-10-25.csv"
MANIFEST = ROOT / "data" / "oracle-footystats-selected-50-season-id-manifest.csv"
CONTRACT = ROOT / "config" / "oracle_selected50_compatibility_contract_v1.json"
EXPECTED_RUN56_GAPS = {
    17326, 16741, 16615, 16789, 16614, 17091, 16714, 16572, 17964,
    17115, 16533, 16905, 16537, 17178, 17119, 16627, 16576, 16708, 16617,
}

class Selected50DataGateMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with MATRIX.open(encoding="utf-8-sig", newline="") as f:
            cls.matrix = list(csv.DictReader(f))
        with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
            cls.manifest = list(csv.DictReader(f))
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def test_exactly_50_unique_season_ids_and_labels(self):
        ids = [int(r["season_id"]) for r in self.matrix]
        self.assertEqual(len(self.matrix), 50)
        self.assertEqual(len(set(ids)), 50)
        expected = {(int(r["selected_id"]), r["country"], r["competition_name"]) for r in self.manifest}
        actual = {(int(r["season_id"]), r["country"], r["competition_name"]) for r in self.matrix}
        self.assertEqual(len(expected), 50)
        self.assertEqual(actual, expected)

    def test_run56_gaps_are_explicit_and_exact(self):
        gaps = {int(r["season_id"]) for r in self.matrix if r["run56_manifest_status"] == "GAP_REQUIRES_RECONCILIATION"}
        self.assertEqual(gaps, EXPECTED_RUN56_GAPS)
        self.assertEqual(len(gaps), 19)

    def test_archive_presence_does_not_promote_data_gates(self):
        for row in self.matrix:
            self.assertEqual(row["archive_package_status"], "PRESENT_VERIFIED_BY_PACKAGE_QA")
            self.assertEqual(row["canonical_fixture_join_status"], "NOT_VERIFIED")
            self.assertEqual(row["settlement_truth_status"], "NOT_VERIFIED")
            self.assertEqual(row["point_in_time_features_status"], "NOT_VERIFIED")
            self.assertEqual(row["production_eligible"], "NO")

    def test_insufficient_recent_form_is_flagged_for_australia_and_india(self):
        for season_id in (17326, 17964):
            row = next(r for r in self.matrix if int(r["season_id"]) == season_id)
            self.assertIn("recent-form coverage insufficient", row["notes"])
            self.assertIn("prior-season continuity unverified", row["notes"])

    def test_production_governance_and_markets_fail_closed(self):
        self.assertEqual(self.contract["status"], "RESEARCH_ONLY_NOT_PRODUCTION_AUTHORIZATION")
        self.assertTrue(self.contract["governance"]["historical_baselines_are_immutable"])
        self.assertFalse(self.contract["governance"]["production_model_logic_may_change"])
        self.assertFalse(self.contract["governance"]["production_probabilities_may_change"])
        self.assertEqual(self.contract["market_readiness_defaults"]["BTTS Yes"], "NOT_VERIFIED")
        self.assertEqual(self.contract["market_readiness_defaults"]["M-1UP"], "BLOCKED")


    def test_presence_of_odds_and_xg_fields_cannot_upgrade_feature_gate(self):
        # Archive QA reports non-empty odds/xG-named fields, but no per-value
        # source, market/bookmaker, scale or as-of-kickoff provenance was certified.
        # This test intentionally keeps every row blocked until evidence is added.
        for row in self.matrix:
            self.assertEqual(row["point_in_time_features_status"], "NOT_VERIFIED")
            self.assertEqual(row["production_eligible"], "NO")

    def test_matrix_never_rewrites_frozen_27_league_historical_counts(self):
        # This matrix is a separate Selected-50 runtime gate artifact. It must not
        # claim that the historical 27-league / 12,836-fixture baseline is 50-league.
        self.assertNotIn("12836", MATRIX.read_text(encoding="utf-8"))
        self.assertNotIn("historical_fixture_count", self.contract)


    def test_form_standings_h2h_xg_and_odds_gates_are_explicit_and_fail_closed(self):
        required = {
            "recent_form_status", "standings_status", "h2h_status",
            "xg_provenance_status", "odds_provenance_status",
        }
        self.assertTrue(required.issubset(set(self.matrix[0].keys())))
        for row in self.matrix:
            self.assertNotEqual(row["recent_form_status"], "VERIFIED")
            self.assertIn("UNVERIFIED", row["standings_status"])
            self.assertIn("UNVERIFIED", row["h2h_status"])
            self.assertIn("UNVERIFIED", row["xg_provenance_status"])
            self.assertIn("UNVERIFIED", row["odds_provenance_status"])
            self.assertEqual(row["production_eligible"], "NO")

if __name__ == "__main__":
    unittest.main()
