import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from reconcile_footystats_prior_probe_identity_to_current_catalogue import read_csv, reconcile

DATA = ROOT / "data" / "footystats"
CROSSWALK = DATA / "current-catalogue-reconciliation-2026-11-04" / "current-catalogue-provider-to-oracle-candidate-crosswalk.csv"
PLAN = DATA / "historical-season-plan-2024-2026" / "season-plan.csv"
PRIOR_PROBE = ROOT / "reports" / "oracle-selected50-footystats-first-identity-registry-2026-10-29.csv"


class FootyStatsPriorProbeIdentityReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.crosswalk = read_csv(CROSSWALK)
        cls.plan = read_csv(PLAN)
        cls.probe = read_csv(PRIOR_PROBE)

    def test_exact_id_reconciliation_covers_44_current_leagues(self):
        summary, current, absent = reconcile(self.crosswalk, self.probe, self.plan)
        self.assertEqual(summary["prior_identity_probe_rows"], 50)
        self.assertEqual(summary["current_catalogue_crosswalk_rows"], 49)
        self.assertEqual(summary["current_leagues_with_exact_prior_selected_season_id_probe"], 44)
        self.assertEqual(summary["exact_country_matches"], 44)
        self.assertEqual(summary["exact_competition_name_matches"], 44)
        self.assertEqual(summary["exact_country_plus_competition_composite_matches_current_provider_league_name"], 44)
        self.assertEqual(summary["exact_comp_master_value_matches"], 44)
        self.assertEqual(len(current), 49)
        self.assertEqual(len(absent), 6)

    def test_five_new_current_leagues_are_explicitly_unprobed(self):
        summary, current, _ = reconcile(self.crosswalk, self.probe, self.plan)
        expected = {
            "Bulgaria First League",
            "Egypt Egyptian Premier League",
            "Portugal Liga NOS",
            "Qatar Stars League",
            "Wales Welsh Premier League",
        }
        got = {r["provider_league_name"] for r in current if r["provider_identity_evidence_status"] == "NEW_CURRENT_CATALOGUE_NO_PRIOR_PROBE_EVIDENCE"}
        self.assertEqual(got, expected)
        self.assertEqual(summary["new_current_catalogue_leagues_without_prior_probe"], 5)

    def test_six_legacy_probe_ids_are_not_silently_reintroduced(self):
        _, _, absent = reconcile(self.crosswalk, self.probe, self.plan)
        got = {(r["prior_probe_country"], r["prior_probe_competition_name"]) for r in absent}
        self.assertEqual(got, {
            ("Finland", "Veikkausliiga"),
            ("India", "Indian Super League"),
            ("Republic of Ireland", "Premier Division"),
            ("Russia", "Russian Premier League"),
            ("South Korea", "K League 1"),
            ("Venezuela", "Primera División"),
        })
        self.assertTrue(all(r["current_catalogue_presence"] == "NOT_PRESENT_IN_CURRENT_49_SELECTED_CATALOGUE" for r in absent))

    def test_comp_master_is_evidence_only_and_never_approved(self):
        summary, current, _ = reconcile(self.crosswalk, self.probe, self.plan)
        self.assertFalse(summary["comp_master_parent_semantics_verified"])
        self.assertFalse(summary["comp_master_cross_season_stability_verified"])
        self.assertEqual(summary["provider_parent_competition_ids_verified"], 0)
        self.assertEqual(summary["approved_canonical_mappings"], 0)
        self.assertTrue(all(r["mapping_approved"] == "False" for r in current))
        self.assertTrue(all(r["production_eligible"] == "False" for r in current))
        self.assertTrue(all(r["betting_eligible"] == "False" for r in current))

    def test_duplicate_prior_probe_season_id_fails_closed(self):
        probe = copy.deepcopy(self.probe)
        probe.append(copy.deepcopy(probe[0]))
        with self.assertRaisesRegex(ValueError, "duplicate footystats_season_id"):
            reconcile(self.crosswalk, probe, self.plan)

    def test_country_mismatch_fails_closed(self):
        probe = copy.deepcopy(self.probe)
        probe[0]["provider_country_observed"] = "Different Country"
        with self.assertRaisesRegex(ValueError, "country does not match"):
            reconcile(self.crosswalk, probe, self.plan)

    def test_competition_name_mismatch_fails_closed(self):
        probe = copy.deepcopy(self.probe)
        probe[0]["provider_competition_name_observed"] = "Different Competition"
        with self.assertRaisesRegex(ValueError, "competition does not match"):
            reconcile(self.crosswalk, probe, self.plan)

    def test_comp_master_mismatch_fails_closed(self):
        crosswalk = copy.deepcopy(self.crosswalk)
        crosswalk[0]["provider_comp_master_id_observed_2026_10_27"] = "999999"
        with self.assertRaisesRegex(ValueError, "comp_master values conflict"):
            reconcile(crosswalk, self.probe, self.plan)

    def test_selected_season_id_must_exist_in_current_plan(self):
        plan = copy.deepcopy(self.plan)
        plan = [r for r in plan if r["provider_season_id"] != "16571"]
        with self.assertRaisesRegex(ValueError, "missing from current history plan"):
            reconcile(self.crosswalk, self.probe, plan)


if __name__ == "__main__":
    unittest.main(verbosity=2)
