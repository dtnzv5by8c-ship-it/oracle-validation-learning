import csv
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_identity_settlement_evidence_register.py"
SPEC = importlib.util.spec_from_file_location("identity_settlement_register", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
REGISTER = ROOT / "data" / "oracle-identity-settlement-evidence-register-2026-10-28.csv"


class IdentitySettlementEvidenceRegisterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = MODULE.read_rows(REGISTER)

    def test_register_passes_with_fail_closed_release_flags(self):
        summary = MODULE.validate_rows(self.rows)
        self.assertEqual(summary["evidence_rows"], 10)
        self.assertEqual(summary["canada_material_conflicts_quarantined"], 1)
        self.assertEqual(summary["england_postponed_or_suspended_zero_zero_rows_excluded"], 3)
        self.assertEqual(summary["completed_cross_provider_score_agreements"], 6)
        self.assertEqual(summary["official_settlement_truth_verified_rows"], 0)
        self.assertEqual(summary["canonical_bridges_approved"], 0)
        self.assertEqual(summary["combo_probability_unmasked_rows"], 0)
        self.assertEqual(summary["production_eligible_rows"], 0)
        self.assertEqual(summary["betting_eligible_rows"], 0)
        self.assertEqual(summary["provider_api_calls_made"], 0)

    def test_canada_source_conflict_cannot_be_promoted(self):
        rows = [dict(r) for r in self.rows]
        target = next(r for r in rows if r["footystats_fixture_id"] == "8465167")
        target["settlement_disposition"] = "CROSS_PROVIDER_AGREEMENT_ONLY_NOT_OFFICIAL_SETTLEMENT"
        with self.assertRaisesRegex(ValueError, "CANADA_SOURCE_CONFLICT_NOT_QUARANTINED"):
            MODULE.validate_rows(rows)

    def test_postponed_zero_zero_placeholder_cannot_be_market_label(self):
        rows = [dict(r) for r in self.rows]
        target = next(r for r in rows if r["footystats_fixture_id"] == "8565639")
        target["market_label_eligible"] = "YES"
        with self.assertRaisesRegex(ValueError, "NONFINAL_MARKET_LABEL_ELIGIBLE"):
            MODULE.validate_rows(rows)

    def test_join_must_use_ordered_teams_and_exact_utc_kickoff(self):
        rows = [dict(r) for r in self.rows]
        rows[0]["join_precision"] = "DATE_ONLY"
        with self.assertRaisesRegex(ValueError, "JOIN_PRECISION_NOT_EXACT"):
            MODULE.validate_rows(rows)

    def test_comp_master_id_semantics_must_remain_unresolved(self):
        rows = [dict(r) for r in self.rows]
        rows[0]["provider_comp_master_id_semantics"] = "CANONICAL_ORACLE_ID"
        with self.assertRaisesRegex(ValueError, "COMP_MASTER_ID_SEMANTICS_OVERCLAIMED"):
            MODULE.validate_rows(rows)

    def test_kickoff_must_be_explicit_utc(self):
        rows = [dict(r) for r in self.rows]
        rows[0]["kickoff_utc"] = "2026-09-30T23:00:00"
        with self.assertRaisesRegex(ValueError, "KICKOFF_NOT_EXPLICIT_UTC"):
            MODULE.validate_rows(rows)

    def test_source_capture_gaps_cannot_be_filled_without_revalidation(self):
        rows = [dict(r) for r in self.rows]
        rows[0]["source_snapshot_sha256"] = "a" * 64
        with self.assertRaisesRegex(ValueError, "UNSUPPORTED_SOURCE_SNAPSHOT_HASH_ADDED"):
            MODULE.validate_rows(rows)

    def test_production_combo_and_betting_gates_fail_closed(self):
        rows = [dict(r) for r in self.rows]
        rows[0]["combo_probability_masked"] = "NO"
        with self.assertRaisesRegex(ValueError, "COMBO_NOT_MASKED"):
            MODULE.validate_rows(rows)
        rows = [dict(r) for r in self.rows]
        rows[0]["production_eligible"] = "YES"
        with self.assertRaisesRegex(ValueError, "PRODUCTION_ELIGIBILITY_PROMOTED"):
            MODULE.validate_rows(rows)

    def test_validator_has_no_network_client_calls(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("requests.get(", source)
        self.assertNotIn("urlopen(", source)
        self.assertNotIn("httpx.", source)


if __name__ == "__main__":
    unittest.main()
