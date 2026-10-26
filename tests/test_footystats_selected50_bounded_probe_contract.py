import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "footystats-selected50-bounded-endpoint-probe.yml"


class Selected50BoundedProbeContractTests(unittest.TestCase):
    def setUp(self):
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_probe_is_manual_dispatch_only(self):
        trigger = self.text.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)

    def test_probe_is_hard_capped_and_never_retries(self):
        self.assertIn("MAX_CALLS = 201", self.text)
        self.assertIn("if calls >= MAX_CALLS", self.text)
        self.assertIn("no retries", self.text.lower())

    def test_checkpoint_does_not_overwrite_final_status(self):
        self.assertIn('summary.setdefault("status", "IN_PROGRESS_OR_STOPPED_FAIL_CLOSED")', self.text)
        self.assertIn('"status": "SELECTED50_BOUNDED_ENDPOINT_PROBE_COMPLETED_RESEARCH_ONLY"', self.text)

    def test_no_private_transfer_or_raw_payload_persistence(self):
        self.assertIn('"raw_provider_payloads_saved": False', self.text)
        self.assertIn('"private_repo_transfer_attempted": False', self.text)
        self.assertNotIn("ORACLE_PRIVATE_REPO_TOKEN", self.text)


    def test_historical_ingestion_has_a_hard_request_cap_and_budget_preflight(self):
        ingestion = (ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml").read_text(encoding="utf-8")
        self.assertIn("MAX_API_REQUESTS = 250", ingestion)
        self.assertIn("if api_calls >= MAX_API_REQUESTS", ingestion)
        self.assertIn("request_hard_cap_reached", ingestion)
        self.assertIn("request_remaining < MAX_API_REQUESTS", ingestion)
        self.assertIn("provider_request_window_is_not_monthly_credit_proof", ingestion)

    def test_historical_ingestion_uses_unique_private_archive_tag_and_keeps_production_blocked(self):
        ingestion = (ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml").read_text(encoding="utf-8")
        self.assertIn('TAG="research-selected50-footystats-history-${GITHUB_RUN_ID}"', ingestion)
        self.assertIn('"production_readiness": "NOT_GRANTED"', ingestion)
        self.assertIn("Transfer raw archive to private Oracle release only", ingestion)
        self.assertIn("Upload sanitized ledger only to public research run", ingestion)


    def test_research_runtime_uses_verified_archive_and_guarded_triggers(self):
        runtime = (ROOT / ".github" / "workflows" / "oracle-selected50-research-runtime.yml").read_text(encoding="utf-8")
        trigger = runtime.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertIn("\n  push:", trigger)
        self.assertIn("research-selected50-footystats-history-40375285207", trigger)
        self.assertIn("paths-ignore:", trigger)
        self.assertIn('"reports/**"', trigger)
        self.assertIn('"tests/**"', trigger)
        self.assertIn('"**/*.md"', trigger)
        self.assertIn('".github/workflows/**"', trigger)
        self.assertIn('gh release download "${PRIVATE_ARCHIVE_RELEASE_TAG}"', runtime)
        self.assertIn("Invalid private archive release tag format.", runtime)
        self.assertIn("Explicit private archive read confirmation required.", runtime)
        self.assertIn("if [[ \"${GITHUB_EVENT_NAME}\" == \"workflow_dispatch\" ]]; then", runtime)


    def test_private_transfer_uses_the_same_unique_run_tag(self):
        ingestion = (ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml").read_text(encoding="utf-8")
        self.assertIn('TAG="research-selected50-footystats-history-${GITHUB_RUN_ID}"', ingestion)
        self.assertNotIn("TAG=research-selected50-footystats-history-20261025", ingestion)


    def test_ingestion_supports_explicit_resume_and_skips_completed_seasons(self):
        ingestion = (ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml").read_text(encoding="utf-8")
        self.assertIn("resume_from_archive_tag:", ingestion)
        self.assertIn('gh release download "${RESUME_FROM_ARCHIVE_TAG}"', ingestion)
        self.assertIn('existing.get("status") == "INGESTED"', ingestion)
        self.assertIn('prior_manifest = out / "ingestion_manifest.json"', ingestion)
        self.assertIn("if not isinstance(prior_ledger, list)", ingestion)


    def test_identity_market_gate_matrix_is_exactly_50_rows_and_fail_closed(self):
        import csv

        matrix_path = ROOT / "reports" / "oracle-selected50-identity-and-market-gate-matrix-2026-10-26.csv"
        with matrix_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        self.assertEqual(len(rows), 50)
        self.assertEqual(len({row["selected_season_id"] for row in rows}), 50)
        required = {
            "selected_season_id", "country", "provider_competition_name",
            "candidate_canonical_code", "identity_gap_status",
            "provider_parent_competition_id_status", "provider_to_canonical_bridge",
            "fixture_identity", "team_identity", "official_settlement_truth",
            "BTTS_readiness", "DC_HOME_readiness", "DC_AWAY_readiness",
            "COMBO_HOME_readiness", "COMBO_AWAY_readiness", "production_eligible",
        }
        self.assertTrue(required.issubset(set(rows[0].keys())))
        self.assertTrue(all(row["production_eligible"] == "NO" for row in rows))
        self.assertTrue(all(row["provider_parent_competition_id_status"] == "VERIFIED_IN_MATCH_RECORDS" for row in rows))
        self.assertTrue(all(row["provider_parent_competition_id_value"] == row["selected_season_id"] for row in rows))
        self.assertTrue(all(row["provider_parent_id_evidence_run"] == "40382835076" for row in rows))
        self.assertTrue(all(row["provider_to_canonical_bridge"] == "UNVERIFIED" for row in rows))
        self.assertTrue(all(row["fixture_identity"] == "PROVIDER_FIXTURE_ID_OBSERVED_CANONICAL_JOIN_UNVERIFIED" for row in rows))
        self.assertTrue(all(row["team_identity"] == "PROVIDER_TEAM_IDS_OBSERVED_CANONICAL_JOIN_UNVERIFIED" for row in rows))
        self.assertTrue(all(row["provider_sample_fixture_id"] for row in rows))
        self.assertTrue(all(row["provider_sample_home_team_id"] and row["provider_sample_away_team_id"] for row in rows))
        self.assertTrue(all(row["provider_sample_scope"] == "SAMPLE_ONLY; SCORES_NOT_SETTLEMENT_TRUTH" for row in rows))
        self.assertTrue(all(row["official_settlement_truth"] == "UNVERIFIED" for row in rows))
        self.assertTrue(all(row["COMBO_HOME_readiness"] == "BLOCKED_TARGET_VS_LEDGER_MISMATCH" for row in rows))
        self.assertTrue(all(row["COMBO_AWAY_readiness"] == "BLOCKED_TARGET_VS_LEDGER_MISMATCH" for row in rows))
        self.assertTrue(all(row["registry_readiness"] != "APPROVED" for row in rows))

        probe_path = ROOT / "reports" / "oracle-selected50-parent-id-probe-2026-10-26.csv"
        with probe_path.open(encoding="utf-8", newline="") as handle:
            probe_rows = list(csv.DictReader(handle))
        self.assertEqual(len(probe_rows), 50)
        self.assertEqual(len({row["selected_id"] for row in probe_rows}), 50)
        self.assertEqual(len({row["provider_match_id"] for row in probe_rows}), 50)
        self.assertTrue(all(row["provider_competition_id"] == row["selected_id"] for row in probe_rows))
        self.assertTrue(all(row["home_team_id"] and row["away_team_id"] for row in probe_rows))
        self.assertTrue(all(row["evidence_scope"] == "ONE_SAMPLE_MATCH_PER_SELECTED_ID; NOT_SETTLEMENT_TRUTH" for row in probe_rows))


    def test_parent_id_probe_is_bounded_rate_limited_and_sanitized(self):
        workflow = (ROOT / ".github" / "workflows" / "oracle-selected50-parent-id-reconciliation.yml").read_text(encoding="utf-8")
        self.assertIn("if calls >= 50", workflow)
        self.assertIn('"max_per_page": 1', workflow)
        self.assertIn("time.sleep(2.1)", workflow)
        self.assertIn("planned_calls_after_this + 25", workflow)
        self.assertIn('"monthly_credit_budget_verified": False', workflow)
        self.assertIn('"raw_provider_payloads_saved": False', workflow)
        self.assertIn('"api_key_logged_or_saved": False', workflow)
        self.assertIn("sample_home_team_id_fields", workflow)
        self.assertIn("sample_away_team_id_fields", workflow)
        self.assertIn("sample_status_fields", workflow)
        self.assertIn("sample_home_score_fields", workflow)
        self.assertIn("sample_away_score_fields", workflow)
        self.assertNotIn("print(payload", workflow)

        runtime = (ROOT / "scripts" / "build_selected50_research_runtime.py").read_text(encoding="utf-8")
        validator = (ROOT / "scripts" / "validate_selected50_runtime_outputs.py").read_text(encoding="utf-8")
        self.assertIn('PARENT_ID_PROBE = Path("reports/oracle-selected50-parent-id-probe-2026-10-26.csv")', runtime)
        self.assertIn("MATCH_RECORD_PROBE_VERIFIED_50_OF_50", runtime)
        self.assertIn('"provider_parent_competition_ids_verified_from_match_probe"', runtime)
        self.assertIn('"provider_sample_scores_are_settlement_truth":False', runtime)
        self.assertIn('provider_parent_competition_ids_verified_from_match_probe") == 50', validator)
        self.assertIn('provider_to_canonical_bridges_verified") == 0', validator)


    def test_parent_id_audit_is_bounded_and_summarizes_first_page_coverage(self):
        audit = (ROOT / ".github" / "workflows" / "oracle-selected50-parent-id-reconciliation.yml").read_text(encoding="utf-8")
        self.assertIn('MAX_API_REQUESTS = 50', audit) if 'MAX_API_REQUESTS = 50' in audit else self.assertIn('if calls >= 50:', audit)
        self.assertIn('"max_per_page": 1000', audit)
        self.assertIn('"pager_max_page"', audit)
        self.assertIn('"unique_fixture_ids_on_page"', audit)
        self.assertIn('"duplicate_fixture_id_rows_on_page"', audit)
        self.assertIn('"status_counts_json"', audit)
        self.assertIn('"rows_with_both_team_ids"', audit)
        self.assertIn('"rows_with_both_score_fields"', audit)
        self.assertIn('"first_page_only": True', audit)
        self.assertIn('"raw_provider_payloads_saved": False', audit)
        self.assertIn('"monthly_credit_budget_verified": False', audit)
        self.assertIn("if not ok:", audit)
        self.assertIn("no retries", audit.lower())


if __name__ == "__main__":
    unittest.main()
