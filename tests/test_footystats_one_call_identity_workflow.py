import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "footystats-selected50-one-season-identity-probe.yml"
SCRIPT = ROOT / "scripts" / "oracle_selected50_one_season_identity_probe.py"


class OneCallIdentityWorkflowSafetyTests(unittest.TestCase):
    def setUp(self):
        self.workflow = WORKFLOW.read_text(encoding="utf-8")
        self.script = SCRIPT.read_text(encoding="utf-8")

    def test_workflow_is_manual_dispatch_only(self):
        trigger = self.workflow.split("permissions:", 1)[0]
        self.assertIn("workflow_dispatch:", trigger)
        self.assertNotIn("\n  push:", trigger)
        self.assertNotIn("\n  schedule:", trigger)

    def test_workflow_fails_closed_without_provider_credentials_or_script_call(self):
        self.assertIn("intentionally fail-closed", self.workflow)
        self.assertIn("iterates over 50 selected seasons", self.workflow)
        self.assertIn("No provider requests were made", self.workflow)
        self.assertNotIn("FOOTYSTATS_API_KEY", self.workflow)
        self.assertNotIn("api.football-data-api.com", self.workflow)
        self.assertNotIn("python scripts/oracle_selected50_one_season_identity_probe.py", self.workflow)

    def test_current_entrypoint_is_batch_scope_not_one_call(self):
        self.assertIn("for item in selected:", self.script)
        self.assertIn('"requests_planned":len(selected)', self.script)
        self.assertIn('"selected_leagues":len(selected)', self.script)


if __name__ == "__main__":
    unittest.main()
