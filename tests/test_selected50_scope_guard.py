import csv
import tempfile
import unittest
from pathlib import Path

from scripts.validate_selected50_scope import audit


class Selected50ScopeGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.ids = [str(16000 + i) for i in range(50)]
        self.manifest = self.root / "manifest.md"
        self.crosswalk = self.root / "crosswalk.csv"
        self.catalogue = self.root / "catalogue.csv"
        self.archive = self.root / "archive_manifest.csv"
        self.write_manifest(self.ids)
        self.write_csv(self.crosswalk, [
            {"footystats_provider_id": x, "crosswalk_status": "UNRESOLVED", "production_eligibility": "NOT_GRANTED"}
            for x in self.ids
        ])
        self.write_csv(self.catalogue, [{"provider_league_id": x, "provider_league_name": f"League {x}"} for x in self.ids])
        # Archive may have multiple season rows per league; set equality is over IDs,
        # but every row must preserve provider_league_id.
        self.write_csv(self.archive, [
            {"provider_league_id": x, "provider_season_id": f"S{x}-2025"} for x in self.ids
        ])

    def tearDown(self):
        self.tmp.cleanup()

    def write_manifest(self, ids):
        lines = ["# Selected 50"]
        lines += [f"| {i} | {pid} | Country {i} | League {i} |" for i, pid in enumerate(ids, start=1)]
        self.manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_csv(self, path, rows):
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    def run_audit(self):
        return audit(self.manifest, self.crosswalk, self.catalogue, self.archive)

    def test_exact_selected_50_scope_passes_only_scope_gate(self):
        result = self.run_audit()
        self.assertEqual(result["status"], "PASS_SCOPE_MATCH")
        self.assertEqual(result["selected_unique_provider_ids"], 50)
        self.assertEqual(result["production_eligibility"], "NOT_GRANTED")

    def test_missing_archive_provider_id_fails_closed(self):
        rows = [{"provider_league_id": x, "provider_season_id": f"S{x}"} for x in self.ids]
        rows[7]["provider_league_id"] = ""
        self.write_csv(self.archive, rows)
        result = self.run_audit()
        self.assertEqual(result["status"], "BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE")
        self.assertEqual(result["archive_blank_provider_id_rows"], 1)

    def test_catalogue_missing_selected_id_fails_closed(self):
        self.write_csv(self.catalogue, [{"provider_league_id": x} for x in self.ids[:-1]])
        result = self.run_audit()
        self.assertEqual(result["status"], "BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE")
        self.assertFalse(result["provider_catalogue_id_check"]["exact_set_match"])

    def test_crosswalk_id_set_mismatch_fails_closed(self):
        rows = [{"footystats_provider_id": x, "crosswalk_status": "UNRESOLVED", "production_eligibility": "NOT_GRANTED"} for x in self.ids]
        rows[-1]["footystats_provider_id"] = "99999"
        self.write_csv(self.crosswalk, rows)
        result = self.run_audit()
        self.assertEqual(result["status"], "BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE")
        self.assertFalse(result["crosswalk_id_check"]["exact_set_match"])

    def test_duplicate_manifest_id_fails_closed(self):
        ids = list(self.ids)
        ids[-1] = ids[0]
        self.write_manifest(ids)
        result = self.run_audit()
        self.assertEqual(result["status"], "BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE")
        self.assertIn("selected manifest contains duplicate provider IDs", result["blockers"])

    def test_ambiguous_catalogue_id_columns_fails_closed(self):
        rows = [{"provider_league_id": x, "league_id": ("99999" if i == 0 else x)}
                for i, x in enumerate(self.ids)]
        self.write_csv(self.catalogue, rows)
        result = self.run_audit()
        self.assertEqual(result["status"], "BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE")
        self.assertEqual(result["provider_catalogue_id_column_check"]["status"], "AMBIGUOUS_ID_COLUMNS")

    def test_catalogue_provider_id_column_present_but_blank(self):
        self.write_csv(self.catalogue, [{"provider_league_id": "", "provider_league_name": f"League {i}"}
                                        for i in range(43)])
        result = self.run_audit()
        self.assertEqual(result["status"], "BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE")
        self.assertEqual(result["provider_catalogue_id_column_check"]["status"], "ID_COLUMN_PRESENT_BUT_BLANK")
        self.assertIn("every provider ID value is blank", " ".join(result["blockers"]))


    def test_approval_state_is_rejected_by_scope_audit(self):
        rows = [{"footystats_provider_id": x, "crosswalk_status": "UNRESOLVED", "production_eligibility": "NOT_GRANTED"} for x in self.ids]
        rows[0]["production_eligibility"] = "PRODUCTION"
        self.write_csv(self.crosswalk, rows)
        result = self.run_audit()
        self.assertEqual(result["status"], "BLOCKED_EXACT_SCOPE_OR_ID_PROVENANCE")


if __name__ == "__main__":
    unittest.main()
