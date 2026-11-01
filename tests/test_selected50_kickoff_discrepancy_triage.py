import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_selected50_kickoff_discrepancy_triage.py"


def row(fixture_id, runtime, archive, delta, season="S1"):
    return {
        "status": "REVIEW_REQUIRED",
        "schedule_reconciliation_status": "REVIEW_REQUIRED",
        "reason": "KICKOFF_MISMATCH",
        "fixture_date": runtime,
        "league": "Test League",
        "fixture": f"Home {fixture_id} vs Away {fixture_id}",
        "fixture_id": fixture_id,
        "selected_id": season,
        "provider_season_id": season,
        "home_team_id": f"H-{fixture_id}",
        "away_team_id": f"A-{fixture_id}",
        "fixture_identity": f"{season}|{fixture_id}|H-{fixture_id}|A-{fixture_id}",
        "runtime_kickoff_utc": runtime,
        "archive_kickoff_utc": archive,
        "delta_minutes_archive_minus_runtime": str(delta),
        "archive_source_file": f"private-package/seasons/{season}/matches.json",
        "archive_source_row": "12",
        "exact_join_status": "PASS_EXACT_SEASON_FIXTURE_ORDERED_TEAM_IDS",
        "resolution_action": "MANUAL_AUTHORITATIVE_EVENT_TIME_REVIEW_ONLY_NO_AUTO_CORRECTION",
    }


class Selected50KickoffTriageTests(unittest.TestCase):
    def run_triage(self, rows):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        queue = root / "queue.csv"
        out = root / "out"
        fields = list(rows[0].keys())
        with queue.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--queue", str(queue), "--out-dir", str(out)],
            capture_output=True, text=True,
        )
        return result, out

    def test_builds_disjoint_review_buckets_and_preserves_overlapping_indicators(self):
        rows = [
            row("F1", "2026-01-01T10:00:00+00:00", "2026-01-03T00:00:00+00:00", 2280),
            row("F2", "2026-01-01T10:00:00+00:00", "2026-01-02T11:00:00+00:00", 1500),
            row("F3", "2026-01-01T10:00:00+00:00", "2026-01-01T11:30:00+00:00", 90),
            row("F4", "2026-01-01T10:00:00+00:00", "2026-01-01T20:00:00+00:00", 600),
        ]
        result, out = self.run_triage(rows)
        self.assertEqual(result.returncode, 0, result.stderr)
        qa = json.loads((out / "oracle_selected50_kickoff_discrepancy_triage_qa.json").read_text())
        self.assertEqual(qa["status"], "PASS_REPORT_ONLY_KICKOFF_TRIAGE")
        self.assertEqual(qa["triage_bucket_counts"], {
            "ARCHIVE_KICKOFF_AT_UTC_MIDNIGHT_REVIEW_INDICATOR": 1,
            "NON_MIDNIGHT_ABS_DELTA_150M_TO_24H": 1,
            "NON_MIDNIGHT_ABS_DELTA_GT_24H": 1,
            "NON_MIDNIGHT_ABS_DELTA_LE_150M": 1,
        })
        self.assertEqual(qa["archive_kickoff_at_utc_midnight_indicator_count"], 1)
        self.assertEqual(qa["absolute_delta_gt_24h_indicator_count"], 2)
        self.assertEqual(qa["absolute_delta_le_150m_indicator_count"], 1)
        with (out / "oracle_selected50_kickoff_discrepancy_triage.csv").open(encoding="utf-8", newline="") as handle:
            emitted = list(csv.DictReader(handle))
        self.assertEqual(len(emitted), 4)
        self.assertTrue(all(r["schedule_auto_correction"] == "NO" for r in emitted))
        self.assertTrue(all(r["authoritative_event_time_verified"] == "NO" for r in emitted))
        self.assertTrue(all(r["production_eligible"] == "NO" and r["betting_eligible"] == "NO" for r in emitted))

    def test_rejects_signed_delta_that_does_not_match_timestamps(self):
        result, _ = self.run_triage([
            row("F1", "2026-01-01T10:00:00+00:00", "2026-01-01T11:00:00+00:00", 120)
        ])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not match recomputed", result.stderr)

    def test_rejects_duplicate_exact_fixture_identity(self):
        duplicate = row("F1", "2026-01-01T10:00:00+00:00", "2026-01-01T11:00:00+00:00", 60)
        result, _ = self.run_triage([duplicate, dict(duplicate)])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate exact fixture identity", result.stderr)

    def test_rejects_non_manual_or_non_review_rows(self):
        invalid = row("F1", "2026-01-01T10:00:00+00:00", "2026-01-01T11:00:00+00:00", 60)
        invalid["resolution_action"] = "AUTO_CORRECT"
        result, _ = self.run_triage([invalid])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("non-manual resolution action", result.stderr)


if __name__ == "__main__":
    unittest.main()
