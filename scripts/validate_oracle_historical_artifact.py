#!/usr/bin/env python3
"""Research-only structural validator for Oracle historical fixture artifacts.

Usage: python scripts/validate_oracle_historical_artifact.py <fixtures.csv> <seasons.csv> <pages.csv> <failures.csv>
Never grants season completeness or prediction readiness.
"""
import csv, json, sys
from datetime import datetime, timezone
from pathlib import Path

START = int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp())
END = int(datetime(2026, 9, 20, 23, 59, 59, tzinfo=timezone.utc).timestamp())
EXPECTED_TARGETS = 49
EXPECTED_CODES = set("""
AR1 AU1 AU2 AU3 AU4 BE1 BR1 CH1 CN1 CO1 DK1 EN1 EN2 EN3 EN4 FI1 FR1 FR2 DE1 DE2 GR1 IN1 IT1 IT2 JP1 MX1 NL1 NO1 PL1 PT2 RO1 RU1 SA1 SC1 SP1 SP2 SE1 TR1 UY1 ZA1
""".split())

def read(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def num(v):
    try: return float(v)
    except (TypeError, ValueError): return None

def main():
    if len(sys.argv) != 5:
        print("Usage: validate_oracle_historical_artifact.py fixtures.csv seasons.csv pages.csv failures.csv", file=sys.stderr)
        return 2
    fixtures, seasons, pages, failures = map(read, sys.argv[1:])
    errors, warnings = [], []
    codes = {r.get("target_code", "").strip() for r in fixtures}
    missing_codes = sorted(EXPECTED_CODES - codes)
    extra_codes = sorted(codes - EXPECTED_CODES)
    if len(codes) != EXPECTED_TARGETS: errors.append(f"Fixture target-code coverage {len(codes)}/{EXPECTED_TARGETS}")
    if missing_codes: warnings.append("Targets without fixture rows: " + ", ".join(missing_codes))
    if extra_codes: errors.append("Unexpected target codes: " + ", ".join(extra_codes))
    ids = [r.get("match_id", "").strip() for r in fixtures]
    blank_ids = sum(not x for x in ids)
    duplicate_ids = len(ids) - len(set(x for x in ids if x))
    if blank_ids: errors.append(f"Blank fixture IDs: {blank_ids}")
    if duplicate_ids: errors.append(f"Duplicate fixture IDs: {duplicate_ids}")
    outside = 0
    bad_timestamps = 0
    missing_scores = 0
    status_counts = {}
    missing_current_xg = 0
    missing_prematch_xg = 0
    negative_xg = 0
    invalid_xg = 0
    score_status_mismatch = 0
    for r in fixtures:
        ts = num(r.get("date_unix"))
        if ts is None: bad_timestamps += 1
        elif not START <= int(ts) <= END: outside += 1
        status = (r.get("status") or "").strip().lower()
        status_counts[status or "(blank)"] = status_counts.get(status or "(blank)", 0) + 1
        hg, ag = num(r.get("homeGoals")), num(r.get("awayGoals"))
        if hg is None or ag is None: missing_scores += 1
        if status == "complete" and (hg is None or ag is None): score_status_mismatch += 1
        cur = [num(r.get("team_a_xg")), num(r.get("team_b_xg"))]
        pre = [num(r.get("team_a_xg_prematch")), num(r.get("team_b_xg_prematch"))]
        if any(v is None for v in cur): missing_current_xg += 1
        if any(v is None for v in pre): missing_prematch_xg += 1
        for raw, value in zip([r.get("team_a_xg"), r.get("team_b_xg"), r.get("team_a_xg_prematch"), r.get("team_b_xg_prematch")], cur+pre):
            if value is None and str(raw or "").strip(): invalid_xg += 1
            if value is not None and value < 0: negative_xg += 1
    if outside: errors.append(f"Rows outside date window: {outside}")
    if bad_timestamps: errors.append(f"Missing/invalid fixture timestamps: {bad_timestamps}")
    if negative_xg: errors.append(f"Negative xG values: {negative_xg}")
    if invalid_xg: errors.append(f"Non-numeric populated xG values: {invalid_xg}")
    if missing_scores: warnings.append(f"Rows missing one or both scores: {missing_scores}")
    if score_status_mismatch: errors.append(f"Complete-status rows missing scores: {score_status_mismatch}")
    season_ids = [r.get("season_id", "").strip() for r in seasons if r.get("season_id", "").strip()]
    unique_season_ids = set(season_ids)
    fixture_season_ids = {r.get("season_id", "").strip() for r in fixtures if r.get("season_id", "").strip()}
    page_keys = {(r.get("target_code","").strip(), r.get("season_id","").strip(), r.get("page","").strip()) for r in pages}
    duplicate_pages = len(page_keys) != len(pages)
    if duplicate_pages: errors.append("Duplicate target/season/page request records")
    if failures: warnings.append(f"Provider/API exceptions recorded: {len(failures)}")
    if any(not (r.get("season_start") or "").strip() or not (r.get("season_end") or "").strip() for r in seasons):
        warnings.append("One or more provider season start/end dates are absent; do not infer from labels")
    if len(fixture_season_ids) < len(unique_season_ids):
        warnings.append(f"Candidate seasons without fixture rows: {len(unique_season_ids - fixture_season_ids)}")
    warnings.append("Pagination termination is not independent proof of season completeness.")
    warnings.append("Presence of prematch xG fields does not prove they were available before historical kickoff.")
    warnings.append("This validator is structural only; it does not grant mapping approval or prediction readiness.")
    report = {
        "window_utc": {"start": "2024-01-01", "end_inclusive": "2026-09-20"},
        "target_universe_expected": EXPECTED_TARGETS,
        "fixture_rows": len(fixtures),
        "target_codes_with_rows": len(codes),
        "missing_target_codes": missing_codes,
        "unexpected_target_codes": extra_codes,
        "distinct_fixture_ids": len(set(x for x in ids if x)),
        "blank_fixture_ids": blank_ids,
        "duplicate_fixture_ids": duplicate_ids,
        "rows_outside_window": outside,
        "invalid_timestamps": bad_timestamps,
        "status_counts": status_counts,
        "rows_missing_scores": missing_scores,
        "complete_status_rows_missing_scores": score_status_mismatch,
        "rows_missing_current_xg": missing_current_xg,
        "rows_missing_prematch_xg": missing_prematch_xg,
        "negative_xg_values": negative_xg,
        "invalid_populated_xg_values": invalid_xg,
        "season_records": len(seasons),
        "distinct_candidate_season_ids": len(unique_season_ids),
        "distinct_season_ids_with_fixture_rows": len(fixture_season_ids),
        "provider_page_records": len(pages),
        "duplicate_page_records": duplicate_pages,
        "provider_failure_records": len(failures),
        "structural_errors": errors,
        "warnings": warnings,
        "season_completeness_proven": False,
        "point_in_time_provenance_established": False,
        "prediction_ready_targets": 0,
        "production_changes": False
    }
    print(json.dumps(report, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
