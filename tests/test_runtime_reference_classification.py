import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION = ROOT / "data" / "oracle_runtime_27_reference_classification_2026-10-25.csv"

EXPECTED_COUNTS = {
    "scripts/ingest_upcoming_fixtures.py": 16,
    "scripts/validate_four_model_production.py": 6,
    "scripts/build_four_model_report.py": 2,
    "scripts/oracle_final_assessment.py": 5,
    "config/oracle_major_league_registry_v1.json": 3,
    "scripts/build_oracle_team_dna_v2.py": 1,
    "scripts/build_oracle_historical_intelligence.py": 1,
    ".github/workflows/oracle_v4_router.yml": 2,
    ".github/workflows/oracle_final_assessment.yml": 7,
    ".github/workflows/oracle_27_league_dna_lab.yml": 10,
    ".github/workflows/oracle_27_league_market_vetting.yml": 12,
    ".github/workflows/oracle_27_league_prediction_readiness.yml": 12,
    ".github/workflows/openfoot-27-league-coverage.yml": 5,
}

class RuntimeReferenceClassificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with CLASSIFICATION.open(encoding="utf-8-sig", newline="") as f:
            cls.rows = list(csv.DictReader(f))

    def test_inventory_covers_all_13_expected_files_and_82_matches(self):
        counts = {r["path"]: int(r["pattern_matches"]) for r in self.rows}
        self.assertEqual(counts, EXPECTED_COUNTS)
        self.assertEqual(len(self.rows), 13)
        self.assertEqual(sum(counts.values()), 82)

    def test_historical_baselines_are_not_migrated_as_runtime_universe(self):
        rows = {r["path"]: r for r in self.rows}
        hist = rows["scripts/build_oracle_historical_intelligence.py"]
        router = rows[".github/workflows/oracle_v4_router.yml"]
        self.assertEqual(hist["classification"], "FROZEN_HISTORICAL_BASELINE")
        self.assertEqual(router["classification"], "FROZEN_HISTORICAL_BASELINE_GATE")
        self.assertIn("keep", hist["required_action"].lower())
        self.assertIn("historical", router["required_action"].lower())

    def test_runtime_consumers_are_explicitly_blocked_until_reviewed_migration(self):
        rows = {r["path"]: r for r in self.rows}
        for path in (
            "scripts/ingest_upcoming_fixtures.py",
            "scripts/validate_four_model_production.py",
            "scripts/build_four_model_report.py",
            "scripts/oracle_final_assessment.py",
            "config/oracle_major_league_registry_v1.json",
        ):
            self.assertIn("ACTIVE_RUNTIME", rows[path]["classification"])
            self.assertTrue(rows[path]["required_action"].strip())

    def test_no_row_authorizes_production_migration(self):
        for row in self.rows:
            self.assertNotIn("production approved", row["required_action"].lower())
            self.assertNotIn("change model logic", row["required_action"].lower())

if __name__ == "__main__":
    unittest.main()
