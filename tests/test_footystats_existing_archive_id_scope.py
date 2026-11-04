import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_footystats_existing_archive_id_scope import build_audit


def sample_inputs():
    crosswalk = [
        {"provider": "FootyStats", "provider_league_name": "League A", "legacy50_selected_provider_season_id": "101", "canonical_mapping_status": "CANDIDATE_REQUIRES_HUMAN_APPROVAL_NOT_CANONICAL"},
        {"provider": "FootyStats", "provider_league_name": "League B", "legacy50_selected_provider_season_id": "202", "canonical_mapping_status": "NO_MATCH_IN_CURRENT_PROTECTED_27_LEAGUE_REGISTRY"},
        {"provider": "FootyStats", "provider_league_name": "League C", "legacy50_selected_provider_season_id": "", "canonical_mapping_status": ""},
    ]
    archive = [
        {"selected_id": "101", "run56_ingestion_status": "INGESTED", "match_count": "2", "team_count": "4", "matches_pages": "1", "tables_status": "SUCCESS", "season_stats_status": "SUCCESS"},
        {"selected_id": "202", "run56_ingestion_status": "", "match_count": "", "team_count": "", "matches_pages": "", "tables_status": "", "season_stats_status": ""},
    ]
    feature = [
        {"selected_id": "101", "records": "2", "parseable_kickoff": "2", "team_ids_complete": "2", "settled_status_allowed": "1", "score_complete": "2", "explicit_score_pairs": "2", "event_array_score_pairs": "0", "missing_team_names": "0"},
    ]
    settlement = [{
        "footystats_season_id": "101", "footystats_fixture_id": "5001", "fotmob_fixture_id": "9001",
        "join_precision": "EXACT_ORDERED_TEAM_NAMES_AND_UTC_KICKOFF",
        "canonical_bridge_approved": "NO", "settlement_truth_verified": "NO",
        "home_team": "Home FC", "away_team": "Away FC",
    }]
    plan = [
        {"provider_season_id": "101", "provider_league_name": "League A"},
        {"provider_season_id": "202", "provider_league_name": "League B"},
    ]
    return crosswalk, archive, feature, settlement, plan


class ExistingArchiveIdScopeTests(unittest.TestCase):
    def run_audit(self, inputs=None):
        return build_audit(*(inputs or sample_inputs()))

    def test_exact_id_join_and_current_catalogue_scope(self):
        rows, summary = self.run_audit()
        self.assertEqual(len(rows), 3)
        self.assertEqual(summary["current_catalogue"]["legacy_selected_season_id_overlap_count"], 2)
        self.assertEqual(summary["run56_archive"]["current_catalogue_leagues_with_exact_ingested_selected_id"], 1)
        self.assertEqual(summary["run56_archive"]["current_catalogue_leagues_without_run56_archive_evidence"], 2)
        self.assertEqual(summary["run56_archive"]["match_records"], 2)
        self.assertEqual(summary["run56_archive"]["team_count_sum_across_season_folders"], 4)

    def test_new_catalogue_entry_without_legacy_id_is_not_fuzzy_joined(self):
        rows, _ = self.run_audit()
        row = next(r for r in rows if r["provider_league_name"] == "League C")
        self.assertEqual(row["run56_archive_status"], "NO_LEGACY_SELECTED_SEASON_ID_NEW_CATALOGUE_ENTRY")
        self.assertFalse(row["exact_provider_season_id_in_current_plan"])

    def test_exact_plan_league_name_mismatch_fails_closed(self):
        inputs = list(sample_inputs())
        inputs[4] = [dict(inputs[4][0], provider_league_name="Different League"), inputs[4][1]]
        with self.assertRaisesRegex(ValueError, "different provider league"):
            self.run_audit(inputs)

    def test_duplicate_plan_season_id_fails_closed(self):
        inputs = list(sample_inputs())
        inputs[4] = inputs[4] + [dict(inputs[4][0])]
        with self.assertRaisesRegex(ValueError, "duplicate provider_season_id"):
            self.run_audit(inputs)

    def test_duplicate_archive_selected_id_fails_closed(self):
        inputs = list(sample_inputs())
        inputs[1] = inputs[1] + [dict(inputs[1][0])]
        with self.assertRaisesRegex(ValueError, "duplicate selected_id"):
            self.run_audit(inputs)

    def test_missing_feature_row_for_ingested_season_fails_closed(self):
        inputs = list(sample_inputs())
        inputs[2] = []
        with self.assertRaisesRegex(ValueError, "no feature-coverage row"):
            self.run_audit(inputs)

    def test_incomplete_team_id_field_count_fails_closed(self):
        inputs = list(sample_inputs())
        inputs[2] = [dict(inputs[2][0], team_ids_complete="1")]
        with self.assertRaisesRegex(ValueError, "team_ids_complete is incomplete"):
            self.run_audit(inputs)

    def test_score_or_kickoff_completeness_mismatch_fails_closed(self):
        inputs = list(sample_inputs())
        inputs[2] = [dict(inputs[2][0], parseable_kickoff="1")]
        with self.assertRaisesRegex(ValueError, "parseable_kickoff is incomplete"):
            self.run_audit(inputs)

    def test_ingested_archive_id_outside_current_crosswalk_fails_closed(self):
        inputs = list(sample_inputs())
        inputs[1] = inputs[1] + [{
            "selected_id": "999", "run56_ingestion_status": "INGESTED", "match_count": "1",
            "team_count": "2", "matches_pages": "1", "tables_status": "SUCCESS", "season_stats_status": "SUCCESS",
        }]
        inputs[2] = inputs[2] + [{
            "selected_id": "999", "records": "1", "parseable_kickoff": "1", "team_ids_complete": "1",
            "settled_status_allowed": "1", "score_complete": "1", "explicit_score_pairs": "1",
            "event_array_score_pairs": "0", "missing_team_names": "0",
        }]
        with self.assertRaisesRegex(ValueError, "absent from current exact crosswalk"):
            self.run_audit(inputs)

    def test_duplicate_fixture_ids_in_settlement_register_fail_closed(self):
        inputs = list(sample_inputs())
        inputs[3] = inputs[3] + [dict(inputs[3][0], fotmob_fixture_id="9002")]
        with self.assertRaisesRegex(ValueError, "duplicate fixture IDs"):
            self.run_audit(inputs)

    def test_field_completeness_does_not_claim_team_id_stability(self):
        _, summary = self.run_audit()
        self.assertEqual(summary["run56_archive"]["team_id_field_complete_rows"], 2)
        self.assertFalse(summary["identity_assessment"]["exact_team_id_values_available"])
        self.assertFalse(summary["identity_assessment"]["cross_season_team_id_stability_assessed"])
        self.assertTrue(summary["identity_assessment"]["team_id_field_completeness_is_not_team_id_identity_stability"])

    def test_settled_status_allowlist_is_not_official_settlement_truth(self):
        _, summary = self.run_audit()
        self.assertEqual(summary["run56_archive"]["settled_status_allowed_rows"], 1)
        self.assertEqual(summary["settlement_register_sample"]["settlement_truth_verified_rows"], 0)
        self.assertTrue(summary["identity_assessment"]["settled_status_allowed_is_not_official_settlement_truth"])

    def test_all_outputs_remain_ineligible(self):
        rows, summary = self.run_audit()
        self.assertTrue(all(r["production_eligible"] is False for r in rows))
        self.assertTrue(all(r["betting_eligible"] is False for r in rows))
        self.assertFalse(summary["governance"]["production_eligible"])
        self.assertFalse(summary["governance"]["betting_eligible"])


if __name__ == "__main__":
    unittest.main()
