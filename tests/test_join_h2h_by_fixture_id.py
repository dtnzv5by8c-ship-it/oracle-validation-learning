import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_h2h_report\nimport prepare_oracle_fixture_id_export

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "join_h2h_by_fixture_id.py"

def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

class ExactFixtureJoinTests(unittest.TestCase):
    def test_oracle_export_adapter_uses_canonical_id_format(self):\n        fixture = {"league_code":"E0","date":"2026-10-18","home_team":"Arsenal","away_team":"Chelsea"}\n        self.assertEqual(prepare_oracle_fixture_id_export.canonical_fixture_id(fixture), "E0-2026-10-18-arsenal-chelsea")\n\n    def test_h2h_export_uses_canonical_oracle_fixture_id_format(self):
        fixture = {"league_code":"E0","date":"2026-10-18","home_team":"Arsenal","away_team":"Chelsea"}
        self.assertEqual(build_h2h_report.fixture_id(fixture), "E0-2026-10-18-arsenal-chelsea")


    def run_join(self, oracle_rows, h2h_rows):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        oracle, h2h = root/"oracle.csv", root/"h2h.csv"
        out, audit = root/"joined.csv", root/"audit.json"
        write_csv(oracle, oracle_rows)
        write_csv(h2h, h2h_rows)
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--oracle", str(oracle), "--h2h", str(h2h),
             "--out", str(out), "--audit", str(audit)],
            text=True, capture_output=True
        )
        return proc, out, audit

    def test_exact_match_preserves_oracle_values_and_row_count(self):
        oracle_rows = [
            {"Oracle Fixture ID":"E0-2026-10-18-arsenal-chelsea","League":"E0","BTTS %":"61.2"},
            {"Oracle Fixture ID":"E0-2026-10-19-liverpool-everton","League":"E0","BTTS %":"54.0"},
        ]
        h2h_rows = [
            {"fixture_id":"E0-2026-10-18-arsenal-chelsea","H2H_Meetings":"8","H2H_BTTS_Yes_%":"62.5"}
        ]
        proc, out, audit = self.run_join(oracle_rows, h2h_rows)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        with out.open(newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["BTTS %"], "61.2")
        self.assertEqual(rows[0]["H2H | H2H_Meetings"], "8")
        self.assertEqual(rows[1]["H2H | H2H_Meetings"], "")
        a = json.loads(audit.read_text(encoding="utf-8"))
        self.assertEqual(a["exact_id_matches"], 1)
        self.assertFalse(a["oracle_probability_values_modified"])
        self.assertFalse(a["fuzzy_matching_used"])

    def test_missing_id_column_fails_closed(self):
        proc, _, _ = self.run_join(
            [{"League":"E0","BTTS %":"61.2"}],
            [{"fixture_id":"E0-2026-10-18-arsenal-chelsea","H2H_Meetings":"8"}]
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("Required Oracle ID column", proc.stderr)

    def test_duplicate_oracle_ids_fail_closed(self):
        proc, _, _ = self.run_join(
            [{"Oracle Fixture ID":"x","League":"E0"},{"Oracle Fixture ID":"x","League":"E0"}],
            [{"fixture_id":"x","H2H_Meetings":"8"}]
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("duplicate fixture IDs", proc.stderr)

    def test_blank_id_fails_closed(self):
        proc, _, _ = self.run_join(
            [{"Oracle Fixture ID":"","League":"E0"}],
            [{"fixture_id":"x","H2H_Meetings":"8"}]
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("blank fixture IDs", proc.stderr)

if __name__ == "__main__":
    unittest.main()
