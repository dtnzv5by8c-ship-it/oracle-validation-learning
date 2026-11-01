import csv
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.audit_run8_pinned_archive_venue_flag_coverage import (
    audit_archive,
    parse_no_home_away,
)


class Run8VenueFlagCoverageTests(unittest.TestCase):
    def test_no_home_away_is_tri_state_and_fail_closed(self):
        self.assertEqual(parse_no_home_away(None), "UNKNOWN")
        self.assertEqual(parse_no_home_away(""), "UNKNOWN")
        self.assertEqual(parse_no_home_away("1"), "NEUTRAL")
        self.assertEqual(parse_no_home_away(True), "NEUTRAL")
        self.assertEqual(parse_no_home_away("0"), "NON_NEUTRAL")
        self.assertEqual(parse_no_home_away(False), "NON_NEUTRAL")
        self.assertEqual(parse_no_home_away("maybe"), "INVALID")

    def test_unknown_flags_are_not_counted_as_non_neutral(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "selected_manifest.csv"
            with manifest.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=["selected_id", "country", "competition_name"]
                )
                writer.writeheader()
                writer.writerow({
                    "selected_id": "SEL-1",
                    "country": "Testland",
                    "competition_name": "Test League",
                })

            records = []
            for i in range(5):
                records.append({
                    "date": "2025-06-01T12:00:00Z",
                    "status": "complete",
                    "homeGoalCount": 1,
                    "awayGoalCount": 0,
                    "homeID": f"H{i}",
                    "awayID": f"A{i}",
                    "no_home_away": 0,
                })
            for i in range(2):
                records.append({
                    "date": "2025-06-01T12:00:00Z",
                    "status": "complete",
                    "homeGoalCount": 1,
                    "awayGoalCount": 1,
                    "homeID": f"NH{i}",
                    "awayID": f"NA{i}",
                    "no_home_away": 1,
                })
            for i in range(3):
                records.append({
                    "date": "2025-06-01T12:00:00Z",
                    "status": "complete",
                    "homeGoalCount": 0,
                    "awayGoalCount": 0,
                    "homeID": f"UH{i}",
                    "awayID": f"UA{i}",
                })
            records.append({
                "date": "2025-06-01T12:00:00Z",
                "status": "complete",
                "homeGoalCount": 2,
                "awayGoalCount": 1,
                "homeID": "IH",
                "awayID": "IA",
                "no_home_away": "unknown-value",
            })

            archive_path = root / "synthetic.zip"
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("ingestion_manifest.json", json.dumps([{
                    "season_id": "S1",
                    "selected_country": "Testland",
                    "selected_competition_name": "Test League",
                }]))
                archive.writestr("league/S1/matches.json", json.dumps(records))

            summary, groups, seasons = audit_archive(archive_path, manifest)
            self.assertEqual(summary["mapping_qa"]["status"], "PASS_EXACT_SELECTED_MANIFEST_LABEL_MAPPING")
            self.assertEqual(summary["primary_window_records"], 11)
            self.assertEqual(summary["primary_window_settled_score_records"], 11)
            flags = summary["primary_window_no_home_away"]
            self.assertEqual(flags["explicit_non_neutral"], 5)
            self.assertEqual(flags["explicit_neutral"], 2)
            self.assertEqual(flags["unknown_or_blank"], 3)
            self.assertEqual(flags["invalid"], 1)
            self.assertEqual(flags["settled_score_non_neutral"], 5)
            self.assertEqual(flags["settled_score_unknown_or_blank"], 3)
            self.assertEqual(len(groups), 1)
            self.assertEqual(len(seasons), 1)
            self.assertEqual(groups[0]["primary_window_non_neutral_records"], 5)
            self.assertEqual(groups[0]["primary_window_unknown_records"], 3)


if __name__ == "__main__":
    unittest.main()
