import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from footystats_request_budget import (
    active_usage, empty_ledger, finalize_reservation, parse_utc,
    prune_ledger, reserve_block, validate_ledger,
)


class FootyStatsRollingRequestBudgetTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 11, 4, 15, 0, tzinfo=timezone.utc)

    def test_default_ledger_has_1800_global_cap(self):
        ledger = empty_ledger()
        self.assertEqual(ledger["global_limit_per_rolling_hour"], 1800)
        self.assertEqual(ledger["reserved_headroom"], 300)
        validate_ledger(ledger)

    def test_reservation_obeys_1500_operational_cap_and_headroom(self):
        ledger, count = reserve_block(empty_ledger(), self.now, 1800, "batch-1")
        self.assertEqual(count, 1500)
        usage = active_usage(ledger, self.now)
        self.assertEqual(usage["active_reserved_requests"], 1500)
        with self.assertRaisesRegex(ValueError, "budget exhausted"):
            reserve_block(ledger, self.now, 1, "batch-2")

    def test_lower_provider_limit_is_binding(self):
        ledger, count = reserve_block(empty_ledger(), self.now, 1500, "batch-low", request_limit=1000)
        self.assertEqual(count, 700)

    def test_actual_requests_count_only_inside_rolling_hour(self):
        ledger = empty_ledger()
        ledger["actual_requests"] = [
            {"timestamp_utc": (self.now - timedelta(minutes=30)).isoformat().replace("+00:00", "Z")},
            {"timestamp_utc": (self.now - timedelta(minutes=61)).isoformat().replace("+00:00", "Z")},
        ]
        got = active_usage(ledger, self.now)
        self.assertEqual(got["actual_requests_in_rolling_hour"], 1)
        self.assertEqual(len(ledger["actual_requests"]), 1)

    def test_reservation_is_conservatively_counted_until_expiry(self):
        ledger, count = reserve_block(empty_ledger(), self.now, 100, "batch-1")
        self.assertEqual(count, 100)
        got = active_usage(ledger, self.now + timedelta(minutes=70))
        self.assertEqual(got["active_reserved_requests"], 100)
        got = active_usage(ledger, self.now + timedelta(minutes=121))
        self.assertEqual(got["active_reserved_requests"], 0)

    def test_finalize_replaces_reservation_with_actual_request_times(self):
        ledger, count = reserve_block(empty_ledger(), self.now, 10, "batch-1")
        self.assertEqual(count, 10)
        actual = [
            (self.now + timedelta(seconds=i)).isoformat().replace("+00:00", "Z")
            for i in range(4)
        ]
        ledger = finalize_reservation(ledger, "batch-1", actual, self.now + timedelta(seconds=5))
        usage = active_usage(ledger, self.now + timedelta(seconds=5))
        self.assertEqual(usage["active_reserved_requests"], 0)
        self.assertEqual(usage["actual_requests_in_rolling_hour"], 4)

    def test_finalize_cannot_exceed_reserved_count_or_time_window(self):
        ledger, _ = reserve_block(empty_ledger(), self.now, 2, "batch-1")
        with self.assertRaisesRegex(ValueError, "exceeds reserved block"):
            finalize_reservation(
                ledger, "batch-1",
                [(self.now + timedelta(seconds=i)).isoformat().replace("+00:00", "Z") for i in range(3)],
                self.now + timedelta(seconds=4),
            )
        with self.assertRaisesRegex(ValueError, "outside its reservation"):
            finalize_reservation(
                ledger, "batch-1",
                [(self.now - timedelta(seconds=1)).isoformat().replace("+00:00", "Z")],
                self.now + timedelta(seconds=4),
            )

    def test_malformed_or_naive_timestamps_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "explicit timezone"):
            parse_utc("2026-11-04T15:00:00")
        ledger = empty_ledger()
        ledger["actual_requests"] = [{"timestamp_utc": "2026-11-04T15:00:00"}]
        with self.assertRaisesRegex(ValueError, "explicit timezone"):
            validate_ledger(ledger)


if __name__ == "__main__":
    unittest.main(verbosity=2)
