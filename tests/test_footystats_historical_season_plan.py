import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_footystats_historical_season_plan import build_plan, write_outputs


def registry(rows):
    return {
        "source_of_truth": "FootyStats",
        "catalogue_scope": "chosen_leagues_only",
        "catalogue_retrieved_utc": "2026-11-04T14:34:00Z",
        "seasons": rows,
    }


def season(league, label, sid):
    return {
        "provider": "FootyStats",
        "provider_league_name": league,
        "provider_season_label": label,
        "provider_season_id": sid,
        "catalogue_scope": "chosen_leagues_only",
    }


class FootyStatsHistoricalSeasonPlanTests(unittest.TestCase):
    def test_calendar_and_cross_year_seasons_intersect_history_window(self):
        data = registry([
            season("League A", "2023", "1"),
            season("League A", "20232024", "2"),
            season("League A", "2024", "3"),
            season("League A", "20242025", "4"),
            season("League A", "20252026", "5"),
            season("League A", "20262027", "6"),
            season("League A", "2027", "7"),
        ])
        summary, rows = build_plan(data, "2024-01-01", "2026-11-04")
        self.assertEqual([r["provider_season_id"] for r in rows], ["2", "3", "4", "5", "6"])
        self.assertEqual(summary["planned_provider_season_count"], 5)
        self.assertEqual(summary["excluded_provider_season_count"], 2)
        self.assertEqual(summary["excluded_reason_counts"]["SEASON_OUTSIDE_HISTORY_WINDOW"], 2)

    def test_fixture_filter_is_explicit_and_inclusive_utc(self):
        summary, rows = build_plan(
            registry([season("League A", "2024", "1")]),
            "2024-01-01",
            "2026-11-04",
        )
        self.assertEqual(rows[0]["fixture_filter_start_utc"], "2024-01-01T00:00:00Z")
        self.assertEqual(rows[0]["fixture_filter_end_utc_inclusive"], "2026-11-04T23:59:59.999999Z")
        self.assertTrue(rows[0]["fixture_kickoff_filter_required"])
        self.assertTrue(summary["fixture_kickoff_filter"]["required"])

    def test_invalid_season_labels_are_quarantined_not_dropped(self):
        summary, rows = build_plan(
            registry([
                season("League A", "2024/25", "1"),
                season("League A", "20252027", "2"),
                season("League B", "2025", "3"),
            ]),
            "2024-01-01",
            "2026-11-04",
        )
        self.assertEqual([r["provider_season_id"] for r in rows], ["3"])
        self.assertEqual(summary["excluded_provider_season_count"], 2)
        self.assertEqual(
            {r["exclusion_reason"] for r in summary["excluded_seasons"]},
            {"INVALID_OR_UNSUPPORTED_SEASON_LABEL"},
        )

    def test_duplicate_season_ids_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "duplicate provider season ID"):
            build_plan(
                registry([season("League A", "2024", "1"), season("League B", "2025", "1")]),
                "2024-01-01",
                "2026-11-04",
            )

    def test_missing_identity_is_explicitly_accounted_for(self):
        data = registry([
            season("League A", "2024", "1"),
            {"provider_league_name": "League B", "provider_season_label": "2025", "provider_season_id": ""},
        ])
        summary, rows = build_plan(data, "2024-01-01", "2026-11-04")
        self.assertEqual(len(rows), 1)
        self.assertEqual(summary["excluded_seasons"][0]["exclusion_reason"], "MISSING_PROVIDER_SEASON_ID")
        self.assertTrue(summary["all_catalogue_rows_accounted_for"])

    def test_bad_registry_scope_and_dates_fail_closed(self):
        bad_scope = registry([season("League A", "2024", "1")])
        bad_scope["catalogue_scope"] = "unknown"
        with self.assertRaisesRegex(ValueError, "catalogue_scope"):
            build_plan(bad_scope, "2024-01-01", "2026-11-04")
        with self.assertRaisesRegex(ValueError, "not be later"):
            build_plan(registry([season("League A", "2024", "1")]), "2026-11-04", "2024-01-01")

    def test_outputs_preserve_all_plan_and_exclusion_rows(self):
        summary, _ = build_plan(
            registry([season("League A", "2024", "1"), season("League A", "2027", "2")]),
            "2024-01-01",
            "2026-11-04",
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_outputs(
                summary,
                root / "plan.csv",
                root / "excluded.csv",
                root / "summary.json",
            )
            self.assertEqual((root / "plan.csv").read_text().splitlines()[0].count(","), 17)
            self.assertEqual(len((root / "plan.csv").read_text().splitlines()), 2)
            self.assertEqual(len((root / "excluded.csv").read_text().splitlines()), 2)
            saved = json.loads((root / "summary.json").read_text())
            self.assertTrue(saved["all_catalogue_rows_accounted_for"])
            self.assertEqual(saved["api_requests_made"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
