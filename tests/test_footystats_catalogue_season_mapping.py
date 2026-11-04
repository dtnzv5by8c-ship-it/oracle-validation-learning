import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_footystats_catalogue_season_mapping import audit_catalogue, read_csv

DATA = ROOT / "data" / "footystats"
REGISTRY = DATA / "footystats-provider-season-registry-2026-11-04.csv"
PLAN = DATA / "historical-season-plan-2024-2026" / "season-plan.csv"
EXCLUDED = DATA / "historical-season-plan-2024-2026" / "excluded-seasons.csv"
CROSSWALK = DATA / "current-catalogue-reconciliation-2026-11-04" / "current-catalogue-provider-to-oracle-candidate-crosswalk.csv"


def inputs():
    return (
        read_csv(REGISTRY),
        read_csv(PLAN),
        read_csv(EXCLUDED),
        read_csv(CROSSWALK),
    )


class FootyStatsCatalogueSeasonMappingAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry, cls.plan, cls.excluded, cls.crosswalk = inputs()

    def test_live_catalogue_is_exactly_partitioned_into_plan_and_exclusions(self):
        summary, queue = audit_catalogue(self.registry, self.plan, self.excluded, self.crosswalk)
        self.assertEqual(summary["provider_catalogue_rows"], 756)
        self.assertEqual(summary["provider_league_count"], 49)
        self.assertEqual(summary["planned_season_rows"], 182)
        self.assertEqual(summary["planned_league_count"], 49)
        self.assertEqual(summary["excluded_season_rows"], 574)
        self.assertTrue(summary["catalogue_partition_complete"])
        self.assertTrue(summary["planned_and_excluded_ids_exactly_partition_catalogue"])
        self.assertEqual(len(queue), 49)

    def test_crosswalk_history_ids_and_labels_match_exact_plan_for_all_leagues(self):
        summary, _ = audit_catalogue(self.registry, self.plan, self.excluded, self.crosswalk)
        self.assertTrue(summary["crosswalk_league_set_exact"])
        self.assertTrue(summary["crosswalk_history_ids_and_labels_exactly_match_plan"])

    def test_provider_native_competition_identity_is_not_present_in_registry(self):
        summary, queue = audit_catalogue(self.registry, self.plan, self.excluded, self.crosswalk)
        self.assertEqual(summary["provider_country_populated_rows"], 0)
        self.assertEqual(summary["provider_competition_id_populated_rows"], 0)
        self.assertEqual(summary["provider_parent_competition_ids_verified"], 0)
        self.assertEqual(summary["approved_canonical_mapping_count"], 0)
        self.assertTrue(all(row["mapping_approved"] == "False" for row in queue))
        self.assertTrue(all(row["mapping_identity_status"] == "LEAGUE_IDENTITY_INCOMPLETE" for row in queue))

    def test_canonical_candidate_statuses_remain_unapproved_and_separate(self):
        summary, queue = audit_catalogue(self.registry, self.plan, self.excluded, self.crosswalk)
        counts = summary["canonical_mapping_status_counts"]
        self.assertEqual(counts["CANDIDATE_REQUIRES_HUMAN_APPROVAL_NOT_CANONICAL"], 22)
        self.assertEqual(counts["NO_MATCH_IN_CURRENT_PROTECTED_27_LEAGUE_REGISTRY"], 22)
        self.assertEqual(counts["NOT_ASSESSED_AGAINST_CURRENT_PROTECTED_REGISTRY"], 5)
        self.assertEqual(sum(bool(row["candidate_canonical_id"]) for row in queue), 22)
        self.assertTrue(all(row["production_eligible"] == "False" for row in queue))
        self.assertTrue(all(row["betting_eligible"] == "False" for row in queue))

    def test_calendar_2023_season_exclusions_are_explicit_boundary_review_items(self):
        summary, _ = audit_catalogue(self.registry, self.plan, self.excluded, self.crosswalk)
        self.assertEqual(summary["calendar_2023_start_year_only_exclusions_requiring_fixture_date_review"], 14)
        self.assertEqual(summary["cross_year_2023_2024_planned_count"], 35)
        self.assertEqual(summary["cross_year_2026_2027_planned_count"], 36)
        self.assertTrue(summary["fixture_level_start_and_end_filter_required"])
        self.assertTrue(summary["season_membership_is_not_fixture_date_coverage"])

    def test_all_planned_rows_use_exact_inclusive_utc_boundaries(self):
        summary, _ = audit_catalogue(self.registry, self.plan, self.excluded, self.crosswalk)
        self.assertEqual(summary["history_start_utc_inclusive"], "2024-01-01T00:00:00Z")
        self.assertEqual(summary["history_end_utc_inclusive"], "2026-11-04T23:59:59.999999Z")

    def test_crosswalk_history_id_mismatch_fails_closed(self):
        crosswalk = copy.deepcopy(self.crosswalk)
        crosswalk[0]["history_provider_season_ids"] = "999999"
        with self.assertRaisesRegex(ValueError, "history IDs/labels"):
            audit_catalogue(self.registry, self.plan, self.excluded, crosswalk)

    def test_duplicate_registry_season_id_fails_closed(self):
        registry = copy.deepcopy(self.registry)
        registry.append(copy.deepcopy(registry[0]))
        with self.assertRaisesRegex(ValueError, "duplicate provider_season_id"):
            audit_catalogue(registry, self.plan, self.excluded, self.crosswalk)

    def test_changed_inclusive_end_boundary_fails_closed(self):
        plan = copy.deepcopy(self.plan)
        plan[0]["fixture_filter_end_utc_inclusive"] = "2026-11-04T23:59:59Z"
        with self.assertRaisesRegex(ValueError, "inclusive UTC end boundary"):
            audit_catalogue(self.registry, plan, self.excluded, self.crosswalk)

    def test_production_or_betting_eligibility_cannot_be_enabled(self):
        plan = copy.deepcopy(self.plan)
        plan[0]["betting_eligible"] = "True"
        with self.assertRaisesRegex(ValueError, "betting_eligible must remain false"):
            audit_catalogue(self.registry, plan, self.excluded, self.crosswalk)


if __name__ == "__main__":
    unittest.main(verbosity=2)
