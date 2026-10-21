import unittest
from scripts.check_archive_freshness import check_freshness

class ArchiveFreshnessTests(unittest.TestCase):
    def test_recent_release_passes(self):
        result = check_freshness("2026-10-20T00:00:00Z", "2026-10-21T00:00:00Z", 14)
        self.assertEqual(result["status"], "FRESH")
        self.assertEqual(result["release_age_days"], 1.0)

    def test_stale_release_fails(self):
        with self.assertRaisesRegex(ValueError, "STALE_ARCHIVE"):
            check_freshness("2026-09-01T00:00:00Z", "2026-10-21T00:00:00Z", 14)

    def test_future_release_fails(self):
        with self.assertRaisesRegex(ValueError, "future"):
            check_freshness("2026-10-22T00:00:00Z", "2026-10-21T00:00:00Z", 14)

    def test_timezone_required(self):
        with self.assertRaisesRegex(ValueError, "timezone"):
            check_freshness("2026-10-20T00:00:00", "2026-10-21T00:00:00Z", 14)

if __name__ == "__main__":
    unittest.main()
