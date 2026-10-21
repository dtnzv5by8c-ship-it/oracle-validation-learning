import csv, json, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_footystats_archive_features.py"

class ChronologyLeakageIntegrationTests(unittest.TestCase):
    def run_builder(self, records):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name)
        source = base / "league" / "2025_2026" / "matches.json"
        source.parent.mkdir(parents=True)
        source.write_text(json.dumps(records), encoding="utf-8")
        archive = base / "synthetic.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(source, "league/2025_2026/matches.json")
        out = base / "out"
        subprocess.run([sys.executable, str(BUILDER), "--archive", str(archive), "--out", str(out)], check=True, capture_output=True, text=True)
        with (out / "chronological_features.csv").open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        return {r["fixture_id"]: r for r in rows}

    @staticmethod
    def match(fid, kickoff, home, away, status="complete", hg=1, ag=0):
        return {"id": fid, "date": kickoff, "homeID": home, "awayID": away,
                "home_name": home, "away_name": away, "status": status,
                "homeGoalCount": hg, "awayGoalCount": ag}

    def test_same_kickoff_fixtures_do_not_inform_each_other(self):
        records = [
            self.match("A", "2026-01-01T12:00:00Z", "T1", "T2"),
            self.match("B", "2026-01-01T12:00:00Z", "T1", "T3"),
            self.match("C", "2026-01-02T12:00:00Z", "T1", "T4"),
        ]
        rows = self.run_builder(records)
        self.assertEqual(int(rows["A"]["home_prior_matches"]), 0)
        self.assertEqual(int(rows["B"]["home_prior_matches"]), 0)
        self.assertEqual(int(rows["C"]["home_prior_matches"]), 2)

    def test_unknown_and_postponed_statuses_do_not_enter_history(self):
        records = [
            self.match("A", "2026-01-01T12:00:00Z", "T1", "T2", status="complete"),
            self.match("B", "2026-01-02T12:00:00Z", "T1", "T3", status="mystery"),
            self.match("C", "2026-01-03T12:00:00Z", "T1", "T4", status="postponed"),
            self.match("D", "2026-01-04T12:00:00Z", "T1", "T5", status="complete"),
        ]
        rows = self.run_builder(records)
        self.assertEqual(int(rows["D"]["home_prior_matches"]), 1)
        self.assertEqual(int(rows["D"]["home_form_n3_available"]), 1)

    def test_future_match_does_not_inform_earlier_target(self):
        records = [
            self.match("A", "2026-01-02T12:00:00Z", "T1", "T2"),
            self.match("B", "2026-01-01T12:00:00Z", "T1", "T3"),
        ]
        rows = self.run_builder(records)
        self.assertEqual(int(rows["B"]["home_prior_matches"]), 0)
        self.assertEqual(int(rows["A"]["home_prior_matches"]), 1)

if __name__ == "__main__":
    unittest.main()
