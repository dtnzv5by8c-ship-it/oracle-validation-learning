import sys, unittest
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_footystats_provider_registry import build_registry

class ProviderRegistryTests(unittest.TestCase):
    def test_provider_catalogue_controls_any_league_count(self):
        rows = [
            {"league_name":"League A","season_year":"2025","season_id":"101"},
            {"league_name":"League B","season_year":"2025/26","season_id":"202"},
            {"league_name":"League B","season_year":"2026/27","season_id":"203"},
        ]
        result = build_registry(rows, "2026-11-04T14:34:00Z")
        self.assertEqual(result["source_of_truth"], "FootyStats")
        self.assertEqual(result["provider_league_count"], 2)
        self.assertEqual(result["provider_season_count"], 3)
        self.assertFalse(result["legacy_fixed_50_manifest_used"])
        self.assertEqual([x["provider_season_id"] for x in result["seasons"]], ["101","202","203"])
        self.assertTrue(all(x["provider"] == "FootyStats" for x in result["seasons"]))
        self.assertFalse(result["production_eligible"])

    def test_duplicate_provider_season_id_fails_closed(self):
        rows = [{"league_name":"A","season_id":"1"},{"league_name":"B","season_id":"1"}]
        with self.assertRaisesRegex(ValueError, "duplicate FootyStats season ID"):
            build_registry(rows, "2026-11-04T14:34:00Z")

    def test_empty_catalogue_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "catalogue is empty"):
            build_registry([], "2026-11-04T14:34:00Z")

    def test_timestamp_requires_timezone(self):
        with self.assertRaisesRegex(ValueError, "include timezone"):
            build_registry([{"league_name":"A","season_id":"1"}], "2026-11-04T14:34:00")

    def test_scope_is_explicit(self):
        with self.assertRaisesRegex(ValueError, "catalogue scope"):
            build_registry([{"league_name":"A","season_id":"1"}], "2026-11-04T14:34:00Z", "unknown")

if __name__ == "__main__":
    unittest.main(verbosity=2)
