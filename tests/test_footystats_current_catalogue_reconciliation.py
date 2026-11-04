import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from reconcile_footystats_current_catalogue_to_legacy50 import build_reconciliation, parse_legacy_manifest


class FootyStatsCurrentCatalogueReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.catalogue = [
            {"provider": "FootyStats", "provider_country": "", "provider_league_name": "Alpha Premier",
             "provider_season_label": "2024", "provider_season_id": "101", "provider_competition_id": "",
             "catalogue_scope": "chosen_leagues_only"},
            {"provider": "FootyStats", "provider_country": "", "provider_league_name": "Alpha Premier",
             "provider_season_label": "2025", "provider_season_id": "102", "provider_competition_id": "",
             "catalogue_scope": "chosen_leagues_only"},
            {"provider": "FootyStats", "provider_country": "", "provider_league_name": "Beta League",
             "provider_season_label": "2024/2025", "provider_season_id": "201", "provider_competition_id": "",
             "catalogue_scope": "chosen_leagues_only"},
            {"provider": "FootyStats", "provider_country": "", "provider_league_name": "Gamma Cup",
             "provider_season_label": "2026", "provider_season_id": "301", "provider_competition_id": "",
             "catalogue_scope": "chosen_leagues_only"},
        ]
        self.plan = [
            {"provider_league_name": "Alpha Premier", "provider_season_label": "2024", "provider_season_id": "101",
             "history_start_date": "2024-01-01", "history_end_date": "2026-11-04",
             "plan_status": "PLANNED_NOT_RETRIEVED", "production_eligible": "False", "betting_eligible": "False"},
            {"provider_league_name": "Alpha Premier", "provider_season_label": "2025", "provider_season_id": "102",
             "history_start_date": "2024-01-01", "history_end_date": "2026-11-04",
             "plan_status": "PLANNED_NOT_RETRIEVED", "production_eligible": "False", "betting_eligible": "False"},
            {"provider_league_name": "Beta League", "provider_season_label": "2024/2025", "provider_season_id": "201",
             "history_start_date": "2024-01-01", "history_end_date": "2026-11-04",
             "plan_status": "PLANNED_NOT_RETRIEVED", "production_eligible": "False", "betting_eligible": "False"},
            {"provider_league_name": "Gamma Cup", "provider_season_label": "2026", "provider_season_id": "301",
             "history_start_date": "2024-01-01", "history_end_date": "2026-11-04",
             "plan_status": "PLANNED_NOT_RETRIEVED", "production_eligible": "False", "betting_eligible": "False"},
        ]
        self.legacy = [
            {"manifest_row": "1", "selected_provider_season_id": "102", "country": "Alpha", "competition": "Premier",
             "provider_league_name": "Alpha Premier"},
            {"manifest_row": "2", "selected_provider_season_id": "999", "country": "Old", "competition": "League",
             "provider_league_name": "Old League"},
        ]
        self.prior = [
            {"provider_catalogue_name": "Alpha Premier", "canonical_candidate_id": "ALP_1",
             "canonical_candidate_competition": "Alpha Premier", "match_state": "CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW",
             "provider_comp_master_id_observed": "44", "historical_ledger_code_candidate": "AP",
             "historical_ledger_team_date_join_count": "5",
             "historical_ledger_join_precision": "TEAM_PAIR_AND_DATE_ONLY_NO_KICKOFF_PROOF",
             "historical_ledger_candidate_status": "STRONG_CANDIDATE_HUMAN_REVIEW_REQUIRED"},
            {"provider_catalogue_name": "Beta League", "canonical_candidate_id": "",
             "canonical_candidate_competition": "", "match_state": "NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY"},
        ]

    def test_exact_mapping_and_candidate_only_statuses(self):
        rows, summary = build_reconciliation(
            self.catalogue, self.plan, self.legacy, self.prior, "2024-01-01", "2026-11-04"
        )
        by_name = {row["provider_league_name"]: row for row in rows}
        self.assertEqual(len(rows), 3)
        self.assertEqual(by_name["Alpha Premier"]["history_provider_season_ids"], "101;102")
        self.assertEqual(by_name["Alpha Premier"]["legacy50_reconciliation_status"],
                         "EXACT_LEGACY_NAME_AND_SELECTED_SEASON_ID_PRESENT")
        self.assertEqual(by_name["Alpha Premier"]["canonical_mapping_status"],
                         "CANDIDATE_REQUIRES_HUMAN_APPROVAL_NOT_CANONICAL")
        self.assertEqual(by_name["Alpha Premier"]["provider_parent_competition_id"], "")
        self.assertEqual(by_name["Alpha Premier"]["provider_comp_master_id_semantics"],
                         "OBSERVED_PROVIDER_FIELD_NOT_APPROVED_AS_PARENT_OR_CANONICAL_ID")
        self.assertEqual(by_name["Beta League"]["canonical_mapping_status"],
                         "NO_MATCH_IN_CURRENT_PROTECTED_27_LEAGUE_REGISTRY")
        self.assertEqual(by_name["Gamma Cup"]["legacy50_reconciliation_status"],
                         "NEW_IN_CURRENT_SELECTED_CATALOGUE_NOT_IN_LEGACY50")
        self.assertFalse(summary["production_eligible"])
        self.assertFalse(summary["betting_eligible"])
        self.assertEqual(summary["api_requests_made"], 0)
        self.assertEqual(summary["approved_oracle_canonical_mappings"], 0)

    def test_legacy_id_must_be_present_under_exact_provider_name(self):
        legacy = [dict(self.legacy[0], selected_provider_season_id="999")]
        rows, _ = build_reconciliation(
            self.catalogue, self.plan, legacy, self.prior, "2024-01-01", "2026-11-04"
        )
        alpha = next(row for row in rows if row["provider_league_name"] == "Alpha Premier")
        self.assertEqual(alpha["legacy50_selected_id_present_under_same_provider_name"], "FALSE")
        self.assertEqual(alpha["legacy50_reconciliation_status"],
                         "LEGACY_NAME_MATCH_BUT_SELECTED_SEASON_ID_NOT_IN_CURRENT_CATALOGUE")

    def test_no_fuzzy_country_or_competition_matching(self):
        legacy = [dict(self.legacy[0], provider_league_name="Premier")]
        rows, _ = build_reconciliation(
            self.catalogue, self.plan, legacy, [], "2024-01-01", "2026-11-04"
        )
        alpha = next(row for row in rows if row["provider_league_name"] == "Alpha Premier")
        self.assertEqual(alpha["legacy50_exact_country_competition_match"], "FALSE")
        self.assertEqual(alpha["legacy50_reconciliation_status"],
                         "NEW_IN_CURRENT_SELECTED_CATALOGUE_NOT_IN_LEGACY50")

    def test_duplicate_provider_season_ids_fail_closed(self):
        duplicate = self.catalogue + [dict(self.catalogue[0], provider_league_name="Other League")]
        with self.assertRaisesRegex(ValueError, "duplicate provider season ID"):
            build_reconciliation(duplicate, self.plan, self.legacy, self.prior,
                                 "2024-01-01", "2026-11-04")

    def test_history_window_must_match_requested_window(self):
        wrong = [dict(row, history_end_date="2026-11-03") for row in self.plan]
        with self.assertRaisesRegex(ValueError, "historical plan window does not equal"):
            build_reconciliation(self.catalogue, wrong, self.legacy, self.prior,
                                 "2024-01-01", "2026-11-04")

    def test_legacy_manifest_parser_uses_exact_table_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.md"
            path.write_text(
                "# manifest\n| # | Provider league ID | Country | Provider competition name |\n"
                "|---:|---:|---|---|\n| 1 | 16571 | Argentina | Primera División |\n",
                encoding="utf-8",
            )
            rows = parse_legacy_manifest(path)
            self.assertEqual(rows[0]["selected_provider_season_id"], "16571")
            self.assertEqual(rows[0]["provider_league_name"], "Argentina Primera División")


if __name__ == "__main__":
    unittest.main(verbosity=2)
