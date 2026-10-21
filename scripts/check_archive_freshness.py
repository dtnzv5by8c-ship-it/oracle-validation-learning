#!/usr/bin/env python3
"""Fail-closed freshness gate for the research archive release. No provider calls."""
import argparse
from datetime import datetime, timezone

def parse_utc(value):
    value = value.strip().replace("Z", "+00:00")
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return dt.astimezone(timezone.utc)

def check_freshness(published_at, now, max_age_days):
    published = parse_utc(published_at)
    current = parse_utc(now)
    age_seconds = (current - published).total_seconds()
    if age_seconds < 0:
        raise ValueError("archive release timestamp is in the future")
    age_days = age_seconds / 86400
    if age_days > max_age_days:
        raise ValueError(f"STALE_ARCHIVE: release age {age_days:.2f} days exceeds limit {max_age_days}")
    return {"status": "FRESH", "release_age_days": round(age_days, 3), "max_age_days": max_age_days}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--published-at", required=True)
    p.add_argument("--now", required=True, help="UTC ISO timestamp; supplied by workflow for testability")
    p.add_argument("--max-age-days", type=float, default=14)
    a = p.parse_args()
    if a.max_age_days <= 0:
        raise SystemExit("--max-age-days must be positive")
    try:
        print(check_freshness(a.published_at, a.now, a.max_age_days))
    except (ValueError, OverflowError) as e:
        raise SystemExit(str(e))
if __name__ == "__main__":
    main()
