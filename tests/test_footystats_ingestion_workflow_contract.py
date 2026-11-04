import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
INGESTION = ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml"
OMI_REPAIR = ROOT / ".github" / "workflows" / "oracle-selected50-market-intelligence-repair.yml"
PROTECTED_WRITE_WORKFLOWS = (
    ROOT / ".github" / "workflows" / "audit-private-footystats-history-h2h.yml",
    ROOT / ".github" / "workflows" / "build-oracle-league-acquisition-tracker.yml",
)


class FootyStatsIngestionWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = INGESTION.read_text(encoding="utf-8")

    def test_legacy_ingestion_is_manual_only_and_fail_closed(self):
        trigger = self.workflow.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertIn("DISABLED", self.workflow)
        self.assertIn("Refuse legacy ingestion path", self.workflow)
        self.assertIn("exit 1", self.workflow)

    def test_legacy_workflow_cannot_read_provider_or_private_destination_secrets(self):
        self.assertNotIn("secrets.FOOTYSTATS_API_KEY", self.workflow)
        self.assertNotIn("secrets.ORACLE_PRIVATE_REPO_TOKEN", self.workflow)
        self.assertNotIn("FOOTYSTATS_API_KEY", self.workflow)
        self.assertNotIn("ORACLE_PRIVATE_REPO_TOKEN", self.workflow)

    def test_legacy_workflow_cannot_call_provider_or_write_protected_repository(self):
        self.assertNotIn("api.football-data-api.com", self.workflow)
        self.assertNotIn("gh release create", self.workflow)
        self.assertNotIn("gh release upload", self.workflow)
        self.assertNotIn("gh release download", self.workflow)
        self.assertNotIn("oracle-football-data", self.workflow.split("run: |", 1)[-1].split("exit 1", 1)[0].replace("This legacy ingestion workflow is disabled. It must not call FootyStats or write to oracle-football-data.", ""))

    def test_disabled_workflow_uses_read_only_permissions(self):
        self.assertIn("permissions:", self.workflow)
        self.assertIn("contents: read", self.workflow)
        self.assertNotIn("contents: write", self.workflow)


class ProtectedRepositoryWriteWorkflowContractTests(unittest.TestCase):
    def test_private_archive_audit_and_tracker_are_manual_only_fail_closed_stubs(self):
        for path in PROTECTED_WRITE_WORKFLOWS:
            with self.subTest(workflow=path.name):
                content = path.read_text(encoding="utf-8")
                trigger = content.split("permissions:", 1)[0]
                self.assertIn("workflow_dispatch:", trigger)
                self.assertNotIn("\n  push:", trigger)
                self.assertNotIn("\n  schedule:", trigger)
                self.assertIn("exit 1", content)
                self.assertIn("contents: read", content)
                self.assertNotIn("contents: write", content)

    def test_protected_repository_workflows_cannot_read_secrets_or_write_releases(self):
        forbidden = (
            "secrets.ORACLE_PRIVATE_REPO_TOKEN",
            "secrets.FOOTYSTATS_API_KEY",
            "ORACLE_PRIVATE_REPO_TOKEN",
            "FOOTYSTATS_API_KEY",
            "gh release download",
            "gh release create",
            "gh release upload",
            "api.football-data-api.com",
            "git push",
            "contents: write",
        )
        for path in PROTECTED_WRITE_WORKFLOWS:
            with self.subTest(workflow=path.name):
                content = path.read_text(encoding="utf-8")
                for marker in forbidden:
                    self.assertNotIn(marker, content)


class CentralFootyStatsBudgetWorkflowContractTests(unittest.TestCase):
    def test_omi_report_repair_cannot_make_direct_provider_requests(self):
        content = OMI_REPAIR.read_text(encoding="utf-8")
        self.assertNotIn("secrets.FOOTYSTATS_API_KEY", content)
        self.assertNotIn("FOOTYSTATS_API_KEY", content)
        self.assertNotIn("api.football-data-api.com", content)
        self.assertNotIn("python scripts/reconcile_selected50_actual_results_footystats.py", content)
        self.assertIn("all FootyStats requests must use the governed global rolling-hour budget workflow", content)
        self.assertIn("write_selected50_unqueried_actual_results.py", content)



class CentralFootyStatsBudgetWorkflowContractTests(unittest.TestCase):
    def setUp(self):
        self.central = ROOT / ".github" / "workflows" / "footystats-global-budgeted-endpoint-preflight.yml"
        self.content = self.central.read_text(encoding="utf-8")

    def test_single_central_gateway_is_manual_and_serialized(self):
        trigger = self.content.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertNotIn("\n  schedule:", trigger)
        self.assertIn("group: footystats-global-api-gateway", self.content)
        self.assertIn("cancel-in-progress: false", self.content)
        self.assertIn("confirm_provider_api_usage:", self.content)
        self.assertIn("default: true", self.content)
        self.assertIn("max_requests:", self.content)
        self.assertIn("default: 1000", self.content)
        self.assertIn("<= 1500", self.content)

    def test_reservation_is_committed_before_the_only_api_executor(self):
        reserve_step = self.content.index("Reserve global rolling-hour request budget before any provider call")
        commit_step = self.content.index("Commit durable reservation before provider access")
        execute_step = self.content.index("Run sanitized endpoint and field preflight")
        self.assertLess(reserve_step, commit_step)
        self.assertLess(commit_step, execute_step)
        self.assertIn("footystats_budgeted_endpoint_preflight.py reserve", self.content)
        self.assertIn("footystats_budgeted_endpoint_preflight.py execute", self.content)

    def test_gateway_uses_bounded_safe_push_retries_without_force(self):
        self.assertEqual(self.content.count("for attempt in 1 2 3 4 5"), 2)
        self.assertIn("git rebase --abort", self.content)
        self.assertIn("stopping before provider access", self.content)
        self.assertIn("artifact upload remains available", self.content)
        self.assertNotIn("git push --force", self.content)
        self.assertNotIn("git push -f", self.content)

    def test_gateway_writes_only_sanitized_ledger_and_preflight_outputs(self):
        self.assertIn("contents: write", self.content)
        self.assertIn("rolling-request-ledger.json", self.content)
        self.assertIn("endpoint-preflight", self.content)
        self.assertIn("Upload sanitized preflight report and ingestion manifest", self.content)
        self.assertNotIn("ORACLE_PRIVATE_REPO_TOKEN", self.content)
        self.assertNotIn("gh release create", self.content)
        self.assertNotIn("gh release upload", self.content)
        self.assertNotIn("oracle-football-data", self.content)

    def test_only_the_central_workflow_may_reference_footystats_api_secret_or_host(self):
        workflow_dir = ROOT / ".github" / "workflows"
        allowed = self.central.resolve()
        for path in workflow_dir.glob("*.yml"):
            content = path.read_text(encoding="utf-8")
            if path.resolve() == allowed:
                continue
            with self.subTest(workflow=path.name):
                self.assertNotIn("secrets.FOOTYSTATS_API_KEY", content)
                self.assertNotIn("api.football-data-api.com", content)

    def test_preflight_and_checkpoint_scripts_are_offline_safe_with_respect_to_raw_storage(self):
        script = (ROOT / "scripts" / "footystats_budgeted_endpoint_preflight.py").read_text(encoding="utf-8")
        self.assertIn('"raw_payloads_persisted": False', script)
        self.assertIn('"production_eligible": False', script)
        self.assertIn('"betting_eligible": False', script)
        self.assertIn("QUARANTINED_NO_FIXTURE_LEVEL_CAPTURE_AND_REVISION_PROVENANCE", script)
        self.assertNotIn("write_text(json.dumps(payload", script)
        checkpoint_script = (ROOT / "scripts" / "footystats_ingestion_checkpoint.py").read_text(encoding="utf-8")
        self.assertNotIn("api.football-data-api.com", checkpoint_script)
        self.assertNotIn("urlopen(", checkpoint_script)
        self.assertIn('"dispatch_allowed": False', checkpoint_script)
        self.assertIn("private_archive_write_verified", checkpoint_script)

    def test_gateway_builds_resumable_checkpoint_after_manifest_and_before_commit(self):
        manifest_step = self.content.index("Build offline full historical ingestion manifest")
        resume_step = self.content.index("Build offline resumable ingestion checkpoint plan")
        commit_step = self.content.index("Commit sanitized report and finalized request ledger")
        self.assertLess(manifest_step, resume_step)
        self.assertLess(resume_step, commit_step)
        self.assertIn("footystats_ingestion_checkpoint.py", self.content)
        self.assertIn("--receipts-jsonl", self.content)
        self.assertIn("--max-batch-requests 1500", self.content)

    def test_gateway_builds_offline_manifest_after_preflight(self):
        self.assertIn("Build offline full historical ingestion manifest", self.content)
        self.assertIn("build_footystats_full_ingestion_manifest.py", self.content)
        self.assertIn("full-ingestion-manifest", self.content)
        planner = (ROOT / "scripts" / "build_footystats_full_ingestion_manifest.py").read_text(encoding="utf-8")
        self.assertIn('"api_requests_made": 0', planner)
        self.assertIn('"raw_payloads_written": False', planner)
        self.assertIn('"private_raw_archive_write_required": True', planner)


if __name__ == "__main__":
    unittest.main()
