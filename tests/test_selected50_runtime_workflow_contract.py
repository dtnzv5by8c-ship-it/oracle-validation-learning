import re
import unittest
from pathlib import Path


WORKFLOW = Path(".github/workflows/oracle-selected50-research-runtime.yml")


class Selected50RuntimeWorkflowContractTests(unittest.TestCase):
    def test_snapshot_disabled_branch_still_emits_declared_metadata_artifact(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        match = re.search(
            r"(?ms)^      - name: Select validated archive input\n.*?^      - name: Install research runtime dependencies",
            text,
        )
        self.assertIsNotNone(match, "archive selection step must remain present")
        step = match.group(0)
        self.assertIn('if [[ "$INCLUDE_CURRENT_SNAPSHOT" == "true" ]]; then', step)
        self.assertIn("else\n", step)
        disabled = step.split("else\n", 1)[1].split("\n          fi", 1)[0]
        metadata_path = "selected50_runtime_output/oracle_selected50_snapshot_artifact_metadata.json"
        self.assertIn(metadata_path, disabled)
        self.assertIn('"status":"NOT_RUN_SNAPSHOT_OVERLAY_DISABLED"', disabled)
        self.assertIn('"artifact_metadata_available":false', disabled)

        upload = text.split("      - name: Upload derived report and sanitized QA only", 1)[1]
        self.assertIn(metadata_path, upload)

    def test_snapshot_disabled_branch_does_not_claim_production_or_betting_eligibility(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        match = re.search(
            r"(?ms)^      - name: Select validated archive input\n.*?^      - name: Install research runtime dependencies",
            text,
        )
        self.assertIsNotNone(match)
        disabled = match.group(0).split("else\n", 1)[1].split("\n          fi", 1)[0]
        self.assertIn('"production_eligible":false', disabled)
        self.assertIn('"betting_eligible":false', disabled)


    def test_stale_snapshot_is_not_the_default_for_historical_validation(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        match = re.search(
            r"(?ms)^      include_current_snapshot:\\n(?P<body>.*?)(?=^      [a-z_]+:|^\\npermissions:)",
            text,
        )
        self.assertIsNotNone(match, "snapshot overlay input must remain declared")
        self.assertIn("default: false", match.group("body"))
        self.assertIn("Opt in only after verifying a fresh successful snapshot run", match.group("body"))

        run_id = re.search(
            r"(?ms)^      snapshot_run_id:\\n(?P<body>.*?)(?=^\\npermissions:)",
            text,
        )
        self.assertIsNotNone(run_id, "snapshot run ID input must remain declared")
        self.assertIn('default: "0"', run_id.group("body"))
        self.assertIn("fail-closed sentinel", run_id.group("body"))


if __name__ == "__main__":
    unittest.main()
