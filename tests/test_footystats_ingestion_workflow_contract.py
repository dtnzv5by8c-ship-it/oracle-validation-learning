import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
INGESTION = ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml"


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


if __name__ == "__main__":
    unittest.main()
