#!/usr/bin/env python3
"""Regression tests: Combo stays blocked while predictor and ledger targets differ."""
import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Selected50ComboSettlementGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_combo_settlement_mismatch_audit.py")],
            cwd=ROOT, capture_output=True, text=True
        )
        if p.returncode:
            raise AssertionError(p.stdout + "\n" + p.stderr)
        out = ROOT / "audit-output"
        with (out / "selected50_combo_settlement_mismatch_matrix.csv").open(
            encoding="utf-8", newline=""
        ) as f:
            cls.rows = list(csv.DictReader(f))
        cls.summary = json.loads(
            (out / "selected50_combo_settlement_mismatch_summary.json").read_text(encoding="utf-8")
        )
        with (ROOT / "reports" / "oracle-selected50-research-market-settlement-crosswalk-2026-10-25.csv").open(
            encoding="utf-8", newline=""
        ) as f:
            cls.crosswalk = {r["market"]: r for r in csv.DictReader(f)}

    def test_score_grid_is_complete_and_diagnostic_only(self):
        self.assertEqual(121, len(self.rows))
        self.assertEqual("DIAGNOSTIC_ONLY_NOT_A_MARKET_DEFINITION_APPROVAL", self.summary["status"])
        self.assertFalse(self.summary["production_eligible"])
        self.assertTrue(all(r["production_eligible"] == "NO" for r in self.rows))
        self.assertTrue(all(r["decision_status"] == "BLOCKED_PENDING_GOVERNED_DEFINITION" for r in self.rows))

    def test_disagreements_are_exactly_the_low_goal_scorelines(self):
        home = [r for r in self.rows if r["combo_home_disagreement"] == "True"]
        away = [r for r in self.rows if r["combo_away_disagreement"] == "True"]
        self.assertEqual({"0-0", "1-0"}, {f'{r["home_score"]}-{r["away_score"]}' for r in home})
        self.assertEqual({"0-0", "0-1"}, {f'{r["home_score"]}-{r["away_score"]}' for r in away})
        self.assertEqual(2, self.summary["combo_home_disagreement_scorelines"])
        self.assertEqual(2, self.summary["combo_away_disagreement_scorelines"])

    def test_repository_crosswalk_keeps_both_combo_markets_blocked(self):
        for market in ("COMBO_HOME", "COMBO_AWAY"):
            row = self.crosswalk[market]
            self.assertEqual("NO", row["production_eligible"])
            self.assertIn("PREDICTION_VS_SETTLEMENT_LEDGER_COMBO_MISMATCH", row["source_settlement_crosswalk_status"])
            self.assertIn("between 2 and 4 inclusive", row["implemented_research_target"])
            self.assertIn("Confirm authoritative target", row["required_verification"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
