import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
INGESTION = ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml"
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


if __name__ == "__main__":
    unittest.main()
