#!/usr/bin/env python3
"""Regression tests for the sanitized Selected-50 governed readiness matrix."""
import sys, unittest
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import build_selected50_governed_readiness_matrix as matrix

class GovernedReadinessMatrixTests(unittest.TestCase):
    def synthetic(self):
        coverage=[]; quarantine=[]; crosswalk=[]
        for i in range(50):
            sid=str(16000+i)
            status="CANDIDATE_REQUIRES_HUMAN_REVIEW_NOT_APPROVED" if i<22 else "UNRESOLVED_NO_EXACT_OR_EXPLICIT_ALIAS"
            sem="YES" if i<31 else "NO"
            coverage.append({"selected_id":sid,"country":f"C{i}","competition":f"League {i}","crosswalk_status":status,
                "crosswalk_candidate_code":"CANDIDATE" if i<22 else "UNRESOLVED","selected_id_semantics_status":"RESEARCH_ALIAS_ONLY",
                "provider_parent_competition_id_status":"NOT_EXPOSED_BY_CATALOGUE","provider_season_fixture_records":"10",
                "provider_season_team_records":"20","current_feed_identity_join_status":"BLOCKED",
                "canonical_fixture_join_status":"NOT_VERIFIED","canonical_team_join_status":"NOT_VERIFIED","official_settlement_truth_status":"NOT_VERIFIED",
                "provider_recent_form5_both_teams_prior_count":"5","provider_standings_payload_status":"NOT_VERIFIED",
                "provider_xg_point_in_time_provenance":"NOT_VERIFIED","provider_odds_point_in_time_provenance":"NOT_VERIFIED",
                "BTTS_YES_readiness":"NOT_PRODUCTION_READY","DOUBLE_CHANCE_readiness":"NOT_PRODUCTION_READY","DC_UNDER_4_5_readiness":"BLOCKED","M1UP_readiness":"BLOCKED","production_eligible":"NO"})
            quarantine.append({"selected_season_id":sid,"source_crosswalk_status":status,"current_feed_display_label_rows":"0" if i>=12 else "1",
                "current_feed_distinct_league_id_count":"0" if i>=12 else ("2" if i<5 else "1"),"current_feed_country_field_present":"NO",
                "current_feed_exact_league_id_allowlist":"NO","provider_season_to_feed_bridge_status":"NOT_VERIFIED",
                "source_collision_status":"NO_MATCHING_CURRENT_FEED_LABEL","primary_blocker":"BLOCKED","all_blockers":"BLOCKED"})
            crosswalk.append({"footystats_provider_id":sid,"crosswalk_status":status,"candidate_basis":"REVIEW" if i<22 else "UNRESOLVED",
                "selected_id_semantics_status":"ARCHIVE_EXACT_SEASON_ID_MATCH" if i<31 else "UNRESOLVED_NO_ARCHIVE_SEASON_ID_MATCH",
                "selected_id_exact_archive_season_id_match":sem,"archive_provider_league_id_status":"BLANK",
                "provider_parent_competition_id_status":"NOT_EXPOSED_BY_CATALOGUE","provider_parent_competition_id_schema_evidence":"NO PARENT ID",
                "current_fixture_coverage_status":"STALE","freshness_status":"STALE","current_upcoming_fixture_schedule_rows":"80",
                "current_upcoming_fixture_schedule_last_date":"2026-10-17","upcoming_fixture_manifest_rows":"80","upcoming_fixture_window_end":"2026-10-22",
                "current_data_snapshot_consistency_status":"INCONSISTENT","current_source_manifest_generated_utc":"2026-10-08","current_reconciliation_generated_utc":"2026-10-07",
                "current_team_state_manifest_generated_utc":"2026-10-07","immutable_feature_snapshot_manifest_row_count":"0",
                "immutable_feature_snapshot_manifest_status":"HEADER_ONLY","latest_private_archive_selected_id_set_match":"PASS_50_OF_50",
                "latest_private_archive_seasons_audited":"50","latest_private_archive_fixture_rows":"14051",
                "latest_private_archive_unique_season_fixture_pairs":"14051","latest_private_archive_duplicate_pairs":"0",
                "latest_private_archive_parent_competition_id_rows":"0","latest_private_archive_odds_timestamp_rows":"0",
                "latest_private_archive_xg_pit_provenance":"UNVERIFIED","latest_private_archive_odds_pit_provenance":"UNVERIFIED"})
        return coverage,quarantine,crosswalk
    def test_exact_50_row_join_and_fail_closed_gates(self):
        c,q,x=self.synthetic(); rows=matrix.build_matrix(c,q,x,audit_date=date(2026,10,26))
        self.assertEqual(len(rows),50)
        self.assertEqual(len({r['selected_season_id'] for r in rows}),50)
        self.assertTrue(all(r['production_eligible']=='NO' for r in rows))
        self.assertTrue(all(r['parent_competition_id_status']=='NOT_EXPOSED_BY_CATALOGUE' for r in rows))
        self.assertTrue(all(r['raw_feed_examples_exported']=='NO' for r in rows))
        self.assertEqual(rows[0]['audit_date'],'2026-10-26')
        self.assertEqual(rows[0]['days_since_last_fixture_date'],9)
        self.assertEqual(rows[0]['days_since_schedule_window_end'],4)
    def test_duplicate_or_missing_selected_ids_fail(self):
        c,q,x=self.synthetic(); q[1]['selected_season_id']=q[0]['selected_season_id']
        with self.assertRaises(AssertionError): matrix.build_matrix(c,q,x)
    def test_crosswalk_status_mismatch_fails(self):
        c,q,x=self.synthetic(); x[0]['crosswalk_status']='APPROVED'
        with self.assertRaises(AssertionError): matrix.build_matrix(c,q,x)
    def test_parent_competition_id_is_never_inferred(self):
        c,q,x=self.synthetic(); x[0]['provider_parent_competition_id_status']='VERIFIED'
        with self.assertRaises(AssertionError): matrix.build_matrix(c,q,x)
    def test_fixture_gate_emits_no_unsupported_rows(self):
        gate=matrix.build_fixture_gate({'audit_date':'2026-10-26','schedule_rows_global':'80','schedule_last_fixture_date':'2026-10-17','schedule_manifest_window_end':'2026-10-22','days_since_last_fixture_date':9,'days_since_schedule_window_end':4})
        self.assertEqual(gate['status'],'BLOCKED_NO_CURRENT_GOVERNED_FIXTURE_SLATE')
        self.assertEqual(gate['current_fixture_rows_emitted'],0)
        self.assertEqual(gate['prediction_rows_emitted'],0)
        self.assertEqual(gate['unsupported_predictions_emitted'],0)
        self.assertFalse(gate['production_eligible'])
        self.assertTrue(gate['research_only'])

if __name__=='__main__': unittest.main(verbosity=2)
