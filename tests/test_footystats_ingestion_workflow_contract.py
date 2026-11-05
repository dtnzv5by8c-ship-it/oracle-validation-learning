import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEGACY_INGESTION = ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml"
OMI_REPAIR = ROOT / ".github" / "workflows" / "oracle-selected50-market-intelligence-repair.yml"
RESOLVER = ROOT / ".github" / "workflows" / "footystats-selected50-catalogue-resolver.yml"
RETIRED_GATEWAY = ROOT / ".github" / "workflows" / "footystats-global-budgeted-endpoint-preflight.yml"
PROTECTED_WRITE_WORKFLOWS = (
    ROOT / ".github" / "workflows" / "audit-private-footystats-history-h2h.yml",
    ROOT / ".github" / "workflows" / "build-oracle-league-acquisition-tracker.yml",
)


class FootyStatsIngestionWorkflowContractTests(unittest.TestCase):
    def test_legacy_ingestion_is_manual_only_and_fail_closed(self):
        workflow = LEGACY_INGESTION.read_text(encoding="utf-8")
        trigger = workflow.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertIn("DISABLED", workflow)
        self.assertIn("Refuse legacy ingestion path", workflow)
        self.assertIn("exit 1", workflow)

    def test_legacy_workflow_cannot_read_provider_or_private_destination_secrets(self):
        workflow = LEGACY_INGESTION.read_text(encoding="utf-8")
        for marker in ("secrets.FOOTYSTATS_API_KEY", "secrets.ORACLE_PRIVATE_REPO_TOKEN",
                       "FOOTYSTATS_API_KEY", "ORACLE_PRIVATE_REPO_TOKEN"):
            self.assertNotIn(marker, workflow)

    def test_legacy_workflow_cannot_call_provider_or_write_protected_repository(self):
        workflow = LEGACY_INGESTION.read_text(encoding="utf-8")
        self.assertNotIn("api.football-data-api.com", workflow)
        self.assertNotIn("gh release create", workflow)
        self.assertNotIn("gh release upload", workflow)
        self.assertNotIn("gh release download", workflow)
        self.assertNotIn("oracle-football-data", workflow)

    def test_disabled_workflow_uses_read_only_permissions(self):
        workflow = LEGACY_INGESTION.read_text(encoding="utf-8")
        self.assertIn("permissions:", workflow)
        self.assertIn("contents: read", workflow)
        self.assertNotIn("contents: write", workflow)


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
            "secrets.ORACLE_PRIVATE_REPO_TOKEN", "secrets.FOOTYSTATS_API_KEY",
            "ORACLE_PRIVATE_REPO_TOKEN", "FOOTYSTATS_API_KEY",
            "gh release download", "gh release create", "gh release upload",
            "api.football-data-api.com", "git push", "contents: write",
        )
        for path in PROTECTED_WRITE_WORKFLOWS:
            content = path.read_text(encoding="utf-8")
            for marker in forbidden:
                with self.subTest(workflow=path.name, marker=marker):
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

    def test_retired_global_gateway_is_fail_closed(self):
        content = RETIRED_GATEWAY.read_text(encoding="utf-8")
        trigger = content.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertNotIn("api.football-data-api.com", content)
        self.assertNotIn("secrets.FOOTYSTATS_API_KEY", content)
        self.assertIn("exit 1", content)

    def test_selected50_resolver_is_the_single_public_provider_caller(self):
        content = RESOLVER.read_text(encoding="utf-8")
        trigger = content.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertIn("group: footystats-selected50-catalogue-resolver", content)
        self.assertIn("cancel-in-progress: false", content)
        self.assertIn("secrets.FOOTYSTATS_API_KEY", content)
        self.assertIn("chosen_leagues_only", content)
        self.assertIn("'false'", content)
        self.assertIn("'api_calls_this_run':1", content)
        self.assertIn("raw_provider_payload_persisted", content)
        self.assertIn("production_eligible", content)
        self.assertIn("betting_eligible", content)

    def test_resolver_requires_exact_50_and_uses_correct_year_parser(self):
        content = RESOLVER.read_text(encoding="utf-8")
        self.assertIn("len(set(x['selected_id'] for x in resolved))!=50", content)
        self.assertIn("re.findall(r'20\\d{2}',label)", content)
        self.assertIn("len({x['provider_season_id'] for x in resolved})!=len(resolved)", content)
        self.assertIn("PLANNED_NOT_EXECUTED", content)
        self.assertIn("raw_storage_required", content)

    def test_only_resolver_references_public_footystats_api_secret_or_host(self):
        workflow_dir = ROOT / ".github" / "workflows"
        allowed = RESOLVER.resolve()
        private_patterns = ("secrets.FOOTYSTATS_API_KEY", "api.football-data-api.com")
        for path in workflow_dir.glob("*.yml"):
            if path.resolve() == allowed:
                continue
            content = path.read_text(encoding="utf-8")
            for marker in private_patterns:
                with self.subTest(workflow=path.name, marker=marker):
                    self.assertNotIn(marker, content)


if __name__ == "__main__":
    unittest.main()
