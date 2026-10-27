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

    def test_probe_requires_explicit_provider_and_monthly_credit_confirmation(self):
        trigger = self.text.split("permissions:", 1)[0]
        self.assertIn("confirm_provider_credit_usage:", trigger)
        self.assertIn("confirm_monthly_credit_budget_checked:", trigger)
        self.assertIn("CONFIRM_PROVIDER_CREDIT_USAGE", self.text)
        self.assertIn("CONFIRM_MONTHLY_CREDIT_BUDGET_CHECKED", self.text)
        self.assertIn("Explicit provider-credit confirmation is required; zero requests made.", self.text)
        self.assertIn("Current monthly FootyStats credit balance has not been explicitly confirmed; zero requests made.", self.text)
        self.assertIn('"monthly_credit_budget_verified_by_provider": False', self.text)
        self.assertIn("Monthly credit budget is not verified by provider metadata", self.text)

    def test_probe_is_hard_capped_and_never_retries(self):
        self.assertIn("MAX_CALLS = 201", self.text)
        self.assertIn("if calls >= MAX_CALLS", self.text)
        self.assertIn("no retries", self.text.lower())

    def test_checkpoint_does_not_overwrite_final_status(self):
        self.assertIn('summary.setdefault("status", "IN_PROGRESS_OR_STOPPED_FAIL_CLOSED")', self.text)
        self.assertIn('"status": "SELECTED50_BOUNDED_ENDPOINT_PROBE_COMPLETED_RESEARCH_ONLY"', self.text)

    def test_per_league_failure_context_is_checkpointed_before_network_call(self):
        # A provider error must leave both the endpoint result and the selected
        # season row in the sanitized artifact; CSV columns must stay stable.
        self.assertEqual(self.text.count("per_league.append(base_row)"), 1)
        self.assertIn('"last_endpoint_attempted": ""', self.text)
        self.assertIn('"matches_sample_field_names": ""', self.text)
        self.assertIn('"identity_note": ""', self.text)
        row_append = self.text.index("per_league.append(base_row)")
        endpoint_call = self.text.index("payload = api(endpoint, params)")
        attempt_marker = self.text.index('base_row["last_endpoint_attempted"] = endpoint')
        self.assertLess(row_append, attempt_marker)
        self.assertLess(attempt_marker, endpoint_call)
        self.assertNotEqual(self.text.rfind("save_checkpoint()", attempt_marker, endpoint_call), -1)
        self.assertIn("except SystemExit:", self.text)
        self.assertIn('base_row[field] = "FAILED_OR_STOPPED"', self.text)
        self.assertNotIn("per_league[-1:] = [base_row]", self.text)

    def test_no_private_transfer_or_raw_payload_persistence(self):
        self.assertIn('"raw_provider_payloads_saved": False', self.text)
        self.assertIn('"private_repo_transfer_attempted": False', self.text)
        self.assertNotIn("ORACLE_PRIVATE_REPO_TOKEN", self.text)


    def test_legacy_historical_ingestion_is_disabled_and_fail_closed(self):
        ingestion = (ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml").read_text(encoding="utf-8")
        trigger = ingestion.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertIn("DISABLED", ingestion)
        self.assertIn("exit 1", ingestion)
        self.assertNotIn("secrets.FOOTYSTATS_API_KEY", ingestion)
        self.assertNotIn("secrets.ORACLE_PRIVATE_REPO_TOKEN", ingestion)
        self.assertNotIn("api.football-data-api.com", ingestion)
        self.assertNotIn("gh release create", ingestion)
        self.assertNotIn("gh release download", ingestion)

    def test_legacy_full_ingestion_and_catalogue_transfer_workflows_are_fail_closed(self):
        paths = (
            ".github/workflows/footystats-full-selected-league-historical-ingestion.yml",
            ".github/workflows/footystats-full-universe-catalogue-transfer.yml",
        )
        for relative in paths:
            workflow = (ROOT / relative).read_text(encoding="utf-8")
            trigger = workflow.split("permissions:", 1)[0]
            with self.subTest(workflow=relative):
                self.assertIn("workflow_dispatch:", trigger)
                self.assertNotIn("\n  push:", trigger)
                self.assertIn("Disabled", workflow)
                self.assertIn("exit 1", workflow)
                self.assertIn("contents: read", workflow)
                self.assertNotIn("contents: write", workflow)
                self.assertNotIn("secrets.FOOTYSTATS_API_KEY", workflow)
                self.assertNotIn("secrets.ORACLE_PRIVATE_REPO_TOKEN", workflow)
                self.assertNotIn("api.football-data-api.com", workflow)
                self.assertNotIn("gh release create", workflow)
                self.assertNotIn("gh release upload", workflow)
                self.assertNotIn("oracle-football-data", workflow)


    def test_research_runtime_uses_verified_archive_and_guarded_triggers(self):
        runtime = (ROOT / ".github" / "workflows" / "oracle-selected50-research-runtime.yml").read_text(encoding="utf-8")
        trigger = runtime.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertIn("\n  push:", trigger)
        self.assertIn("research-selected50-footystats-history-40447419806", trigger)
        self.assertIn("paths:", trigger)
        self.assertIn('"!reports/**"', trigger)
        self.assertIn('"!tests/**"', trigger)
        self.assertIn('"!**/*.md"', trigger)
        self.assertIn('"!.github/workflows/**"', trigger)
        self.assertIn('".github/workflows/oracle-selected50-research-runtime.yml"', trigger)
        self.assertIn('gh release download "${PRIVATE_ARCHIVE_RELEASE_TAG}"', runtime)
        self.assertIn("Invalid private archive release tag format.", runtime)
        self.assertIn("Explicit private archive read confirmation required.", runtime)
        self.assertIn("if [[ \"${GITHUB_EVENT_NAME}\" == \"workflow_dispatch\" ]]; then", runtime)


    def test_private_archive_qa_reports_status_score_and_date_exceptions_without_settlement_claims(self):
        import datetime as dt
        import importlib.util

        script_path = ROOT / "scripts" / "qa_selected50_private_archive.py"
        spec = importlib.util.spec_from_file_location("selected50_private_archive_qa", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        def unix_day(year, month, day):
            return int(dt.datetime(year, month, day, tzinfo=dt.timezone.utc).timestamp())

        matches = [
            {"id": "a", "status": "complete", "date_unix": unix_day(2026, 10, 26), "homeGoalCount": 1, "awayGoalCount": 0},
            {"id": "b", "status": "incomplete", "date_unix": unix_day(2026, 10, 26), "homeGoalCount": 2, "awayGoalCount": 1},
            {"id": "c", "status": "complete", "date_unix": unix_day(2026, 10, 28)},
            {"id": "d", "status": "suspended", "date_unix": unix_day(2026, 10, 26), "homeGoalCount": 0, "awayGoalCount": 0},
            {"id": "e", "status": "incomplete", "date_unix": unix_day(2026, 10, 28)},
            {"id": "f"},
        ]
        audit = module.audit_matches(matches, dt.date(2026, 10, 27))
        metrics = audit["metrics"]
        self.assertEqual(audit["status_counts"], {"MISSING": 1, "complete": 2, "incomplete": 2, "suspended": 1})
        self.assertEqual(metrics["records_with_both_parseable_scores"], 3)
        self.assertEqual(metrics["noncomplete_status_records_with_parseable_score_pair"], 2)
        self.assertEqual(metrics["noncomplete_status_records_with_zero_zero_score_pair"], 1)
        self.assertEqual(metrics["noncomplete_status_records_with_nonzero_score_pair"], 1)
        self.assertEqual(metrics.get("complete_status_records_with_zero_zero_score_pair", 0), 0)
        self.assertEqual(metrics.get("complete_status_records_with_nonzero_score_pair", 0), 1)
        self.assertEqual(audit["status_score_pattern_counts"], {
            "complete:nonzero": 1,
            "incomplete:nonzero": 1,
            "suspended:zero_zero": 1,
        })
        self.assertEqual(metrics["complete_status_records_missing_or_invalid_score_pair"], 1)
        self.assertEqual(metrics["incomplete_status_records_with_past_kickoff"], 1)
        self.assertEqual(metrics["complete_status_records_with_future_kickoff"], 1)
        self.assertEqual(metrics["suspended_status_records_with_parseable_score_pair"], 1)
        self.assertEqual(metrics["records_without_kickoff_date"], 1)
        self.assertEqual(metrics["records_with_missing_status"], 1)
        self.assertEqual(audit["kickoff_date_min"], "2026-10-26")
        self.assertEqual(audit["kickoff_date_max"], "2026-10-28")
        self.assertNotIn("settlement_truth", audit)

    def test_private_archive_qa_uses_the_same_current_archive_as_runtime(self):
        qa = (ROOT / ".github" / "workflows" / "oracle-selected50-private-archive-qa.yml").read_text(encoding="utf-8")
        runtime = (ROOT / ".github" / "workflows" / "oracle-selected50-research-runtime.yml").read_text(encoding="utf-8")
        current_tag = "research-selected50-footystats-history-40447419806"
        self.assertIn(f"gh release download {current_tag}", qa)
        self.assertIn(current_tag, runtime)
        self.assertNotIn("research-selected50-footystats-history-20261025", qa)
        self.assertIn("sha256sum -c private-package.sha256", qa)
        self.assertIn("Upload sanitized QA only", qa)
        self.assertIn("ref: ${{ github.sha }}", qa)
        self.assertNotIn("FOOTYSTATS_API_KEY", qa)

        contracts = (ROOT / ".github" / "workflows" / "oracle-selected50-contract-tests.yml").read_text(encoding="utf-8")
        self.assertIn("ref: ${{ github.sha }}", contracts)
        self.assertNotIn("ref: research/oracle-50-league-readiness-audit", contracts)

    def test_legacy_ingestion_has_no_resume_or_private_transfer_path(self):
        ingestion = (ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml").read_text(encoding="utf-8")
        self.assertNotIn("resume_from_archive_tag:", ingestion)
        self.assertNotIn("gh release download", ingestion)
        self.assertNotIn("gh release create", ingestion)
        self.assertNotIn("Transfer raw archive to private Oracle release only", ingestion)
        self.assertNotIn("Upload sanitized ledger only to public research run", ingestion)
        self.assertIn("This legacy ingestion workflow is disabled", ingestion)

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
            "provider_competition_id_observation_status", "provider_competition_id_observed_value",
            "provider_competition_id_evidence_run", "provider_to_canonical_bridge",
            "fixture_identity", "team_identity", "official_settlement_truth",
            "provider_match_coverage_rows_first_page", "provider_match_coverage_unique_fixture_ids_first_page",
            "provider_match_coverage_duplicate_fixture_rows_first_page", "provider_match_coverage_status_counts_json",
            "provider_match_coverage_rows_with_both_team_ids", "provider_match_coverage_rows_with_both_score_fields",
            "provider_match_coverage_nonempty_season_id_field_rows",
            "BTTS_readiness", "DC_HOME_readiness", "DC_AWAY_readiness",
            "COMBO_HOME_readiness", "COMBO_AWAY_readiness", "production_eligible",
        }
        self.assertTrue(required.issubset(set(rows[0].keys())))
        self.assertTrue(all(row["production_eligible"] == "NO" for row in rows))
        self.assertTrue(all(row["provider_competition_id_observation_status"] == "PROVIDER_DOCS_DEFINE_COMPETITION_ID_AS_SEASON_ID_NOT_PARENT_ID" for row in rows))
        self.assertTrue(all("Official FootyStats docs define league-matches competition_id as the league season ID" in row["provider_competition_id_evidence_scope"] for row in rows))
        self.assertTrue(all(row["provider_competition_id_observed_value"] == row["selected_season_id"] for row in rows))
        self.assertTrue(all(row["provider_competition_id_evidence_run"] == "40382835076;40391540391" for row in rows))
        self.assertTrue(all(int(row["provider_match_coverage_rows_first_page"]) > 0 for row in rows))
        self.assertTrue(all(row["provider_match_coverage_rows_first_page"] == row["provider_match_coverage_unique_fixture_ids_first_page"] for row in rows))
        self.assertTrue(all(row["provider_match_coverage_duplicate_fixture_rows_first_page"] == "0" for row in rows))
        self.assertTrue(all(row["provider_match_coverage_pager_max_page"] == "1" for row in rows))
        self.assertTrue(all(row["provider_match_coverage_rows_with_both_team_ids"] == row["provider_match_coverage_rows_first_page"] for row in rows))
        self.assertTrue(all(row["provider_match_coverage_rows_with_both_score_fields"] == row["provider_match_coverage_rows_first_page"] for row in rows))
        self.assertTrue(all(row["provider_match_coverage_nonempty_season_id_field_rows"] == "0" for row in rows))
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


    def test_parent_id_probe_is_disabled_and_historical_evidence_stays_quarantined(self):
        workflow = (ROOT / ".github" / "workflows" / "oracle-selected50-parent-id-reconciliation.yml").read_text(encoding="utf-8")
        trigger = workflow.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertIn("DISABLED", workflow.upper())
        self.assertIn("exit 1", workflow)
        self.assertNotIn("FOOTYSTATS_API_KEY", workflow)
        self.assertNotIn("api.football-data-api.com", workflow)

        runtime = (ROOT / "scripts" / "build_selected50_research_runtime.py").read_text(encoding="utf-8")
        validator = (ROOT / "scripts" / "validate_selected50_runtime_outputs.py").read_text(encoding="utf-8")
        self.assertIn('PARENT_ID_PROBE = Path("reports/oracle-selected50-parent-id-probe-2026-10-26.csv")', runtime)
        self.assertIn("MATCH_RECORD_COMPETITION_ID_DOCUMENTED_AS_SEASON_ID_50_OF_50_PARENT_ID_NOT_PROVIDED", runtime)
        self.assertIn('"provider_competition_id_field_semantics_documented_as_season_id":True', runtime)
        self.assertIn('"provider_sample_scores_are_settlement_truth":False', runtime)
        self.assertIn('provider_competition_id_field_matches_selected_id_in_match_probe") == 50', validator)
        self.assertIn('provider_match_coverage_first_page_total_rows") == 14051', validator)
        self.assertIn('provider_to_canonical_bridges_verified") == 0', validator)


    def test_parent_id_audit_workflow_is_disabled(self):
        audit = (ROOT / ".github" / "workflows" / "oracle-selected50-parent-id-reconciliation.yml").read_text(encoding="utf-8")
        audit_trigger = audit.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", audit_trigger)
        self.assertNotIn("\n  push:", audit_trigger)
        self.assertIn("DISABLED", audit.upper())
        self.assertIn("exit 1", audit)
        self.assertNotIn("secrets.FOOTYSTATS_API_KEY", audit)
        self.assertNotIn("api.football-data-api.com", audit)
        self.assertNotIn("urlopen(", audit)


    def test_provider_schema_diagnostic_requires_explicit_single_call_confirmation(self):
        workflow = (ROOT / ".github" / "workflows" / "oracle-selected50-provider-schema-diagnostic.yml").read_text(encoding="utf-8")
        trigger = workflow.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertIn("confirm_provider_credit_usage:", trigger)
        self.assertIn("confirm_monthly_credit_budget_checked:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertIn("Explicit provider-credit confirmation is required; no request made.", workflow)
        self.assertIn("CONFIRM_MONTHLY_CREDIT_BUDGET_CHECKED", workflow)
        self.assertIn("Current monthly FootyStats credit balance has not been explicitly confirmed; no request made.", workflow)
        self.assertIn('"operator_confirmed_monthly_credit_budget_checked": os.environ.get("CONFIRM_MONTHLY_CREDIT_BUDGET_CHECKED", "false").lower() == "true"', workflow)
        self.assertLess(workflow.index("CONFIRM_MONTHLY_CREDIT_BUDGET_CHECKED:-false"), workflow.index('url = "https://api.football-data-api.com/league-list?'))
        self.assertIn('"planned_api_requests": 1', workflow)
        self.assertIn('"hard_request_cap": 1', workflow)
        self.assertIn('"monthly_credit_budget_verified": False', workflow)
        self.assertIn('"raw_provider_payload_saved": False', workflow)
        self.assertIn('"api_key_saved_or_printed": False', workflow)
        self.assertNotIn("print(payload", workflow)


    def test_runtime_quarantines_noncomplete_scores_from_targets_and_training(self):
        import ast
        import math

        runtime_path = ROOT / "scripts" / "build_selected50_research_runtime.py"
        source = runtime_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(runtime_path))
        selected = []
        wanted = {"num", "get_first", "match_score", "finished"}
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "FINISHED"
                for target in node.targets
            ):
                selected.append(node)
            elif isinstance(node, ast.FunctionDef) and node.name in wanted:
                selected.append(node)
        self.assertEqual(
            {node.name for node in selected if isinstance(node, ast.FunctionDef)},
            wanted,
        )
        namespace = {"math": math}
        exec(compile(ast.Module(body=selected, type_ignores=[]), str(runtime_path), "exec"), namespace)
        is_finished = namespace["finished"]

        self.assertTrue(is_finished({"status": "complete", "homeGoalCount": 0, "awayGoalCount": 0}))
        self.assertTrue(is_finished({"status": "COMPLETE", "homeGoalCount": 2, "awayGoalCount": 1}))
        self.assertFalse(is_finished({"status": "incomplete", "homeGoalCount": 0, "awayGoalCount": 0}))
        self.assertFalse(is_finished({"status": "suspended", "homeGoalCount": 0, "awayGoalCount": 0}))
        self.assertFalse(is_finished({"status": "canceled", "homeGoalCount": 0, "awayGoalCount": 0}))
        self.assertFalse(is_finished({"status": "abandoned", "homeGoalCount": 2, "awayGoalCount": 1}))
        self.assertFalse(is_finished({"status": "complete", "homeGoalCount": None, "awayGoalCount": 0}))
        self.assertFalse(is_finished({"status": "complete", "homeGoalCount": -1, "awayGoalCount": 0}))

        self.assertIn(
            'if r["finished"] and r["home_goals"] is not None and r["away_goals"] is not None:',
            source,
        )
        self.assertIn(
            'train_rows=[r for r in feature_rows if r.get("finished") and r.get("kickoff_unix",NOW)>=0]',
            source,
        )
        self.assertIn(
            'and not r["finished"] and str(r["status"]).strip().lower() not in CANCELLED',
            source,
        )


    def test_safety_contract_workflow_skips_markdown_only_checkpoint_edits(self):
        workflow = (ROOT / ".github" / "workflows" / "oracle-selected50-contract-tests.yml").read_text(encoding="utf-8")
        trigger = workflow.split("permissions:", 1)[0]
        self.assertIn("paths-ignore:", trigger)
        self.assertIn('"**/*.md"', trigger)
        self.assertIn("ref: ${{ github.sha }}", workflow)


    def test_private_archive_qa_primary_window_and_manifest_integrity(self):
        import ast
        import datetime as dt
        import math
        from collections import Counter

        qa_path = ROOT / "scripts" / "qa_selected50_private_archive.py"
        source = qa_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(qa_path))
        wanted_functions = {"date_value", "within_date_range", "index_season_rows", "parse_score", "audit_matches"}
        wanted_constants = {
            "PRIMARY_WINDOW_START", "PRIMARY_WINDOW_END",
            "PRIMARY_2025_START", "PRIMARY_2025_END",
            "PRIMARY_2026_START", "PRIMARY_2026_END",
        }
        selected_nodes = []
        found_functions = set()
        found_constants = set()
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in wanted_functions:
                selected_nodes.append(node)
                found_functions.add(node.name)
            elif isinstance(node, ast.Assign):
                names = {t.id for t in node.targets if isinstance(t, ast.Name)}
                if names & wanted_constants:
                    selected_nodes.append(node)
                    found_constants.update(names & wanted_constants)

        self.assertEqual(found_functions, wanted_functions)
        self.assertEqual(found_constants, wanted_constants)
        namespace = {"dt": dt, "math": math, "Counter": Counter}
        exec(compile(ast.Module(body=selected_nodes, type_ignores=[]), str(qa_path), "exec"), namespace)

        index_rows = namespace["index_season_rows"]
        self.assertEqual(set(index_rows([{"season_id": "1"}, {"season_id": "2"}])), {"1", "2"})
        with self.assertRaisesRegex(ValueError, "duplicate season IDs"):
            index_rows([{"season_id": "1"}, {"season_id": "1"}])
        with self.assertRaisesRegex(ValueError, "missing season ID"):
            index_rows([{"season_id": "1"}, {"season_id": ""}])
        with self.assertRaisesRegex(ValueError, "missing season ID"):
            index_rows([{"season_id": "1"}, {"season_id": None}])

        in_range = namespace["within_date_range"]
        start = dt.date(2025, 3, 20)
        end = dt.date(2026, 9, 20)
        self.assertTrue(in_range({"date": "2025-03-20"}, start, end))
        self.assertTrue(in_range({"date": "2026-09-20"}, start, end))
        self.assertFalse(in_range({"date": "2025-03-19"}, start, end))
        self.assertFalse(in_range({"date": "2026-09-21"}, start, end))
        self.assertFalse(in_range({"status": "complete"}, start, end))

        rows = [
            {"date": "2025-03-20", "status": "complete", "homeGoalCount": 1, "awayGoalCount": 0},
            {"date": "2026-09-20", "status": "incomplete", "homeGoalCount": 0, "awayGoalCount": 0},
            {"date": "2025-03-19", "status": "complete", "homeGoalCount": 3, "awayGoalCount": 1},
            {"date": "2026-09-21", "status": "complete", "homeGoalCount": 1, "awayGoalCount": 1},
            {"status": "incomplete", "homeGoalCount": 0, "awayGoalCount": 0},
        ]
        window_rows = [row for row in rows if in_range(row, start, end)]
        self.assertEqual(len(window_rows), 2)
        audit = namespace["audit_matches"](window_rows, dt.date(2026, 10, 27))
        self.assertEqual(audit["status_counts"], {"complete": 1, "incomplete": 1})
        self.assertEqual(audit["metrics"]["noncomplete_status_records_with_zero_zero_score_pair"], 1)
        self.assertEqual(audit["kickoff_date_min"], "2025-03-20")
        self.assertEqual(audit["kickoff_date_max"], "2026-09-20")

        self.assertIn('"primary_window_start": PRIMARY_WINDOW_START.isoformat()', source)
        self.assertIn('"primary_window_calendar_year_coverage"', source)
        self.assertIn('"selected_group_primary_window_coverage_rows": len(group_coverage_rows)', source)
        self.assertIn('"group_label_basis": "INHERITED_FROM_EXACT_SELECTED_SEASON_CATALOGUE_RELATION_RESEARCH_GROUPING_ONLY"', source)
        self.assertIn('"primary_window_coverage_is_canonical_fixture_count": False', source)
        self.assertIn('"official_settlement_truth_verified": False', source)
        qa_workflow = (ROOT / ".github" / "workflows" / "oracle-selected50-private-archive-qa.yml").read_text(encoding="utf-8")
        self.assertIn("selected50_primary_window_coverage.csv", qa_workflow)
        self.assertIn('assert len(groups) == 50', qa_workflow)
        self.assertIn('assert all(row["production_eligible"] == "NO" for row in groups)', qa_workflow)


    def test_unbudgeted_legacy_provider_workflows_are_disabled(self):
        paths = (
            ".github/workflows/footystats-api-catalogue-audit.yml",
            ".github/workflows/footystats-api-endpoint-coverage-audit.yml",
            ".github/workflows/footystats-bounded-selected50-smoke-probe.yml",
            ".github/workflows/footystats-historical-season-coverage-audit.yml",
            ".github/workflows/oracle-selected50-parent-id-reconciliation.yml",
            ".github/workflows/oracle-selected50-catalogue-schema-audit.yml",
        )
        for relative in paths:
            workflow = (ROOT / relative).read_text(encoding="utf-8")
            trigger = workflow.split("permissions:", 1)[0]
            with self.subTest(workflow=relative):
                self.assertIn("workflow_dispatch:", trigger)
                self.assertNotIn("\n  push:", trigger)
                self.assertIn("DISABLED", workflow.upper())
                self.assertIn("exit 1", workflow)
                self.assertIn("contents: read", workflow)
                self.assertNotIn("secrets.FOOTYSTATS_API_KEY", workflow)
                self.assertNotIn("api.football-data-api.com", workflow)
                self.assertNotIn("secrets.ORACLE_PRIVATE_REPO_TOKEN", workflow)
                self.assertNotIn("gh release create", workflow)
                self.assertNotIn("gh release upload", workflow)

    def test_private_transfer_write_validator_is_disabled(self):
        workflow = (ROOT / ".github" / "workflows" / "validate-private-oracle-transfer-write.yml").read_text(encoding="utf-8")
        trigger = workflow.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertIn("DISABLED", workflow.upper())
        self.assertIn("exit 1", workflow)
        self.assertIn("contents: read", workflow)
        self.assertNotIn("secrets.ORACLE_PRIVATE_REPO_TOKEN", workflow)
        self.assertNotIn("gh api", workflow)
        self.assertNotIn("git/refs", workflow)
        self.assertNotIn("oracle-football-data", workflow)

    def test_canonical_provider_schema_diagnostic_requires_monthly_budget_confirmation(self):
        workflow = (ROOT / ".github" / "workflows" / "oracle-selected50-provider-schema-diagnostic.yml").read_text(encoding="utf-8")
        trigger = workflow.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertIn("confirm_provider_credit_usage:", trigger)
        self.assertIn("confirm_monthly_credit_budget_checked:", trigger)
        self.assertIn("default: false", trigger)
        self.assertIn("planned_api_requests", workflow)
        self.assertIn('"monthly_credit_budget_verified": False', workflow)


if __name__ == "__main__":
    unittest.main()
