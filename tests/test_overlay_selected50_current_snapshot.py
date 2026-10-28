import json, tempfile, unittest, zipfile
from pathlib import Path
from datetime import datetime, timezone
from scripts.overlay_selected50_current_snapshot import parse_utc, valid_id, find_archive_path

class SnapshotOverlayContractTests(unittest.TestCase):
    def test_requires_explicit_timezone(self):
        self.assertIsNone(parse_utc("2026-10-28T16:00:00"))
        self.assertIsNotNone(parse_utc("2026-10-28T16:00:00Z"))
    def test_resolves_nested_archive_paths_by_suffix(self):
        names=["private/archive/seasons/17326/matches.json","private/archive/seasons/17326/teams.json"]
        self.assertEqual(find_archive_path(names,"17326","matches"),names[0])
        self.assertEqual(find_archive_path(names,"17326","teams"),names[1])
        self.assertIsNone(find_archive_path(names,"99999","matches"))

    def test_rejects_ambiguous_archive_paths(self):
        names=["a/seasons/17326/matches.json","b/seasons/17326/matches.json"]
        with self.assertRaises(SystemExit):
            find_archive_path(names,"17326","matches")

    def test_rejects_blank_and_zero_ids(self):
        for v in ("", None, 0, "0", "null", "none"):
            self.assertFalse(valid_id(v))
        self.assertTrue(valid_id("8551579"))

if __name__ == "__main__":
    unittest.main()
