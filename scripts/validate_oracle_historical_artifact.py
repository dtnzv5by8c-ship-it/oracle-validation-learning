#!/usr/bin/env python3
"""Research-only structural checks for Oracle historical fixture artifacts."""
import csv, json, sys
from datetime import datetime, timezone
from pathlib import Path
from oracle_44_catalogue_discovery import TARGETS

START = int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp())
END = int(datetime(2026, 9, 20, 23, 59, 59, tzinfo=timezone.utc).timestamp())
EXPECTED_CODES = {target[0] for target in TARGETS}

def read(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))

def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def main():
    if len(sys.argv) != 5:
        print("Usage: validate_oracle_historical_artifact.py fixtures.csv seasons.csv pages.csv failures.csv", file=sys.stderr)
        return 2
    fixtures, seasons, pages, failures = [read(p) for p in sys.argv[1:]]
    errors, warnings = [], []
    codes = {r.get("target_code", "").strip() for r in fixtures}
    missing_codes, extra_codes = sorted(EXPECTED_CODES - codes), sorted(codes - EXPECTED_CODES)
    if missing_codes:
        warnings.append("Targets with no fixture rows: " + ", ".join(missing_codes))
    if extra_codes:
        errors.append("Unexpected target codes: " + ", ".join(extra_codes))
    if len(codes) != len(EXPECTED_CODES):
        warnings.append(f"Fixture rows cover {len(codes)} of {len(EXPECTED_CODES)} targets")
    ids = [str(r.get("match_id", "")).strip() for r in fixtures]
    blank_ids = sum(not value for value in ids)
    duplicate_ids = len([value for value in ids if value]) - len(set(value for value in ids if value))
    if blank_ids:
        errors.append(f"Blank fixture IDs: {blank_ids}")
    if duplicate_ids:
        errors.append(f"Duplicate fixture IDs: {duplicate_ids}")
    outside, bad_ts, missing_scores, complete_missing_scores = 0, 0, 0, 0
    missing_current_xg, missing_prematch_xg, negative_xg, invalid_xg = 0, 0, 0, 0
    statuses = {}
    for row in fixtures:
        ts = number(row.get("date_unix"))
        if ts is None:
            bad_ts += 1
        elif not START <= int(ts) <= END:
            outside += 1
        status = str(row.get("status", "")).strip().lower()
        statuses[status or "(blank)"] = statuses.get(status or "(blank)", 0) + 1
        home, away = number(row.get("homeGoals")), number(row.get("awayGoals"))
        if home is None or away is None:
            missing_scores += 1
            if status == "complete":
                complete_missing_scores += 1
        current = [number(row.get("team_a_xg")), number(row.get("team_b_xg"))]
        prematch = [number(row.get("team_a_xg_prematch")), number(row.get("team_b_xg_prematch"))]
        if any(value is None for value in current):
            missing_current_xg += 1
        if any(value is None for value in prematch):
            missing_prematch_xg += 1
        for raw, value in zip([row.get("team_a_xg"), row.get("team_b_xg"), row.get("team_a_xg_prematch"), row.get("team_b_xg_prematch")], current + prematch):
            if value is None and str(raw or "").strip():
                invalid_xg += 1
            if value is not None and value < 0:
                negative_xg += 1
    if outside: errors.append(f"Rows outside requested date window: {outside}")
    if bad_ts: errors.append(f"Missing/invalid timestamps: {bad_ts}")
    if negative_xg: errors.append(f"Negative xG values: {negative_xg}")
    if invalid_xg: errors.append(f"Non-numeric populated xG values: {invalid_xg}")
    if complete_missing_scores: errors.append(f"Complete-status rows missing scores: {complete_missing_scores}")
    if missing_scores: warnings.append(f"Rows missing scores: {missing_scores}")
    if len(ids) != len(set(value for value in ids if value)) + blank_ids:
        warnings.append("Review fixture ID accounting")
    season_ids = {str(r.get("season_id", "")).strip() for r in seasons if str(r.get("season_id", "")).strip()}
    fixture_season_ids = {str(r.get("season_id", "")).strip() for r in fixtures if str(r.get("season_id", "")).strip()}
    if any(not str(r.get("season_start", "")).strip() or not str(r.get("season_end", "")).strip() for r in seasons):
        warnings.append("Provider season start/end dates missing; do not infer dates from labels")
    if season_ids - fixture_season_ids:
        warnings.append(f"Candidate seasons with no fixture rows: {len(season_ids - fixture_season_ids)}")
    page_keys = [(r.get("target_code", ""), r.get("season_id", ""), r.get("page", "")) for r in pages]
    duplicate_page_records = len(page_keys) - len(set(page_keys))
    if duplicate_page_records:
        errors.append(f"Duplicate target/season/page records: {duplicate_page_records}")
    if failures:
        warnings.append(f"Provider/API failure records: {len(failures)}")
    warnings.extend([
        "Short-page pagination does not independently prove season completeness.",
        "Prematch xG field presence does not prove the value was available before kickoff.",
        "Structural checks do not approve competition mapping or prediction readiness."
    ])
    report = {
        "window": {"start": "2024-01-01", "end_inclusive": "2026-09-20"},
        "expected_target_count": len(EXPECTED_CODES), "target_codes_with_rows": len(codes),
        "missing_target_codes": missing_codes, "unexpected_target_codes": extra_codes,
        "fixture_rows": len(fixtures), "distinct_fixture_ids": len(set(x for x in ids if x)),
        "blank_fixture_ids": blank_ids, "duplicate_fixture_ids": duplicate_ids,
        "rows_outside_window": outside, "invalid_timestamps": bad_ts, "status_counts": statuses,
        "rows_missing_scores": missing_scores, "complete_rows_missing_scores": complete_missing_scores,
        "rows_missing_current_xg": missing_current_xg, "rows_missing_prematch_xg": missing_prematch_xg,
        "negative_xg_values": negative_xg, "invalid_populated_xg_values": invalid_xg,
        "season_records": len(seasons), "distinct_candidate_season_ids": len(season_ids),
        "season_ids_with_fixture_rows": len(fixture_season_ids), "page_records": len(pages),
        "duplicate_page_records": duplicate_page_records, "provider_failure_records": len(failures),
        "structural_errors": errors, "warnings": warnings,
        "season_completeness_proven": False, "point_in_time_provenance_established": False,
        "prediction_ready_targets": 0, "production_changes": False
    }
    print(json.dumps(report, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
