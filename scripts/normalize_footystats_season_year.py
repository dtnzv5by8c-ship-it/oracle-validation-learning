#!/usr/bin/env python3
"""Research-only parser for FootyStats season-year tokens.

Preserves the provider token verbatim and returns a normalized start/end year
only for the two explicitly observed formats. It does not change provider data
or production model behavior.
"""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class SeasonYear:
    raw_token: str
    start_year: int | None
    end_year: int | None
    status: str


def normalize_season_year(value: object) -> SeasonYear:
    raw = "" if value is None else str(value).strip()
    if not raw:
        return SeasonYear(raw, None, None, "MISSING_YEAR_TOKEN")

    if re.fullmatch(r"(?:19|20)\d{2}", raw):
        return SeasonYear(raw, int(raw), None, "START_YEAR_ONLY")

    match = re.fullmatch(r"((?:19|20)\d{2})((?:19|20)\d{2})", raw)
    if match:
        start, end = int(match.group(1)), int(match.group(2))
        if end == start + 1:
            return SeasonYear(raw, start, end, "CONSECUTIVE_YEAR_RANGE")
        return SeasonYear(raw, None, None, "INVALID_EIGHT_DIGIT_RANGE")

    return SeasonYear(raw, None, None, "UNSUPPORTED_YEAR_TOKEN")


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("values", nargs="*", default=["20262027", "2026"])
    args = parser.parse_args()
    print(json.dumps([normalize_season_year(v).__dict__ for v in args.values], indent=2))
