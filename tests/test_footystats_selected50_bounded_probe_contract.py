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
        self.assertIn("research-selected50-footystats-history-40320274133", trigger)
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


if __name__ == "__main__":
    unittest.main()
