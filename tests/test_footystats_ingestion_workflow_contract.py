import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
INGESTION = ROOT / ".github" / "workflows" / "oracle-selected50-footystats-live-ingestion.yml"


class FootyStatsIngestionWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = INGESTION.read_text(encoding="utf-8")

    def test_provider_credit_confirmation_and_secrets_are_guarded(self):
        self.assertIn("confirm_provider_credit_usage", self.workflow)
        self.assertIn('CONFIRM_PROVIDER_CREDIT_USAGE:-false', self.workflow)
        self.assertIn('FOOTYSTATS_API_KEY missing; no provider calls made.', self.workflow)
        self.assertIn('ORACLE_PRIVATE_REPO_TOKEN missing; no provider calls made.', self.workflow)

    def test_private_destination_write_permission_is_preflighted_before_provider_calls(self):
        # A missing destination write grant must fail before any paid-provider request.
        permission_check = self.workflow.index("ORACLE_PRIVATE_REPO_TOKEN lacks private destination write permission; no provider calls made.")
        first_provider_call = self.workflow.index('api("league-list"')
        self.assertLess(permission_check, first_provider_call)
        self.assertIn("gh api \"repos/$TARGET\" --jq '.permissions.push // false' | grep -qx true", self.workflow)
        self.assertIn("Validate credentials and private destination", self.workflow)

    def test_exact_50_selected_leagues_expand_to_historical_seasons(self):
        self.assertIn("len(selected) != 50", self.workflow)
        self.assertIn("len({str(r.get(\"selected_id\",\"\")).strip() for r in selected}) != 50", self.workflow)
        self.assertIn("historical_targets", self.workflow)
        self.assertIn("int(year_text) < 2023", self.workflow)
        self.assertIn('"selected_leagues": 50', self.workflow)
        self.assertIn('"season_year_floor": 2023', self.workflow)

    def test_hobby_rate_is_conservatively_throttled_and_attempts_counted(self):
        self.assertIn("api_calls += 1", self.workflow)
        self.assertIn("time.sleep(2.1)", self.workflow)
        self.assertIn("1,800 requests/hour", self.workflow)

    def test_raw_provider_payload_is_not_uploaded_to_public_artifacts(self):
        self.assertIn("raw_provider_payload_saved_publicly", self.workflow)
        self.assertIn("Upload sanitized ledger only to public research run", self.workflow)
        self.assertIn("Raw provider payloads remain only in this job's temporary workspace until private transfer", self.workflow)


    def test_parent_competition_id_and_season_id_are_never_conflated(self):
        # Contract-only check: does not call FootyStats or consume provider credits.
        self.assertIn('"season_id": sid,', self.workflow)
        self.assertIn('"provider_league_id": str(league.get("id")) if league.get("id") is not None else "NOT_EXPOSED_BY_CATALOGUE",', self.workflow)
        self.assertIn('sid = safe_id(season.get("id"))', self.workflow)
        self.assertNotIn('"provider_league_id": sid', self.workflow)

    def test_embedded_ingestion_python_compiles_without_running_api_calls(self):
        lines = self.workflow.splitlines()
        start = next(i for i, line in enumerate(lines) if "python - <<'PY'" in line)
        end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "PY")
        script_lines = lines[start + 1:end]
        # Strip the YAML block's common indentation; preserve Python's relative indentation.
        script = "\n".join(line[10:] if line.startswith("          ") else line for line in script_lines)
        compile(script, str(INGESTION), "exec")


if __name__ == "__main__":
    unittest.main()
