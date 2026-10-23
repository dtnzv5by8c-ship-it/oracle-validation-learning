#!/usr/bin/env python3
"""Fail-closed structural validator for Oracle's sanitized 44-league audit CSVs.

This validates the audit artifact's internal consistency only. It does not prove
provider completeness, correct season selection, or historical as-of provenance.
Usage: python scripts/validate_oracle_44_audit.py <audit-directory>
"""
import csv
import json
import sys
from pathlib import Path

EXPECTED_TARGETS = 44
REQUIRED_COVERAGE = {
    "target_code", "catalogue_status", "match_fetch_status", "fixture_rows",
    "unique_match_ids", "duplicate_match_ids", "missing_match_ids",
    "missing_kickoff", "cutoff_provenance",
}
REQUIRED_FIXTURES = {"target_code", "season_id", "match_id", "date_unix"}
REQUIRED_CROSSWALK = {"target_code", "catalogue_status"}


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def integer(row, key):
    try:
        return int(row.get(key) or 0)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid integer in {key}: {row.get(key)!r}")


def validate(root: Path):
    errors, warnings = [], []
    paths = {
        "summary": root / "oracle_44_league_full_season_summary.json",
        "coverage": root / "oracle_44_league_full_season_coverage.csv",
        "crosswalk": root / "oracle_44_league_candidate_crosswalk.csv",
        "fixtures": root / "oracle_44_league_sanitized_fixture_audit.csv",
        "pages": root / "oracle_44_league_page_provenance.csv",
    }
    for name, path in paths.items():
        if not path.is_file():
            errors.append(f"Missing required file: {path.name}")
    if errors:
        return errors, warnings, {}

    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    coverage = read_csv(paths["coverage"])
    crosswalk = read_csv(paths["crosswalk"])
    fixtures = read_csv(paths["fixtures"])
    pages = read_csv(paths["pages"])

    for label, rows, required in [
        ("coverage", coverage, REQUIRED_COVERAGE),
        ("crosswalk", crosswalk, REQUIRED_CROSSWALK),
        ("fixtures", fixtures, REQUIRED_FIXTURES),
    ]:
        if not rows:
            errors.append(f"{label} CSV has no data rows")
        elif not required.issubset(rows[0].keys()):
            errors.append(f"{label} missing columns: {sorted(required - set(rows[0].keys()))}")

    if errors:
        return errors, warnings, {}

    codes = [r["target_code"] for r in coverage]
    if len(codes) != EXPECTED_TARGETS:
        errors.append(f"Expected {EXPECTED_TARGETS} coverage rows; found {len(codes)}")
    if len(set(codes)) != len(codes):
        errors.append("Duplicate target_code rows in coverage CSV")
    if len(crosswalk) != EXPECTED_TARGETS:
        errors.append(f"Expected {EXPECTED_TARGETS} crosswalk rows; found {len(crosswalk)}")
    if set(codes) != {r["target_code"] for r in crosswalk}:
        errors.append("Coverage and crosswalk target_code sets differ")

    fixture_keys = []
    for row in fixtures:
        if not row.get("match_id"):
            errors.append("Fixture row missing match_id")
        if not row.get("season_id"):
            errors.append("Fixture row missing season_id")
        if not row.get("date_unix"):
            errors.append("Fixture row missing date_unix")
        fixture_keys.append((row["target_code"], row["season_id"], row["match_id"]))
    if len(fixture_keys) != len(set(fixture_keys)):
        errors.append("Duplicate target-season-match keys in fixture audit")

    by_code = {}
    for row in coverage:
        code = row["target_code"]
        by_code[code] = row
        count = integer(row, "fixture_rows")
        if row["match_fetch_status"] == "PAGINATION_COMPLETE_SHORT_PAGE" and count == 0:
            errors.append(f"{code}: short-page status with zero fixtures")
        if integer(row, "duplicate_match_ids") > 0:
            errors.append(f"{code}: duplicate match IDs reported")
        if integer(row, "missing_match_ids") > 0 or integer(row, "missing_kickoff") > 0:
            errors.append(f"{code}: missing fixture identity or kickoff")
        if row["match_fetch_status"] == "PAGINATION_COMPLETE_SHORT_PAGE":
            warnings.append(f"{code}: short-page termination is not independent proof of season completeness")
        if row["cutoff_provenance"] != "VERIFIED":
            warnings.append(f"{code}: historical/pre-kickoff provenance is not verified")
        if row["catalogue_status"] == "NO_EXACT_ALIAS_MATCH":
            warnings.append(f"{code}: selected-catalogue alias miss; not proof provider lacks league")
        actual_count = sum(1 for f in fixtures if f["target_code"] == code)
        if actual_count != count:
            errors.append(f"{code}: coverage fixture_rows={count}, fixture CSV rows={actual_count}")

    if integer(summary, "target_leagues") != EXPECTED_TARGETS:
        errors.append("Summary target_leagues is not 44")
    if integer(summary, "fixture_rows") != len(fixtures):
        errors.append("Summary fixture_rows does not match fixture CSV")
    if summary.get("model_logic_changed") is not False:
        errors.append("Summary does not affirm model_logic_changed=false")
    if summary.get("production_registry_changed") is not False:
        errors.append("Summary does not affirm production_registry_changed=false")
    if summary.get("production_predictions_created") is not False:
        errors.append("Summary does not affirm production_predictions_created=false")

    metrics = {
        "target_leagues": len(coverage),
        "fixture_rows": len(fixtures),
        "targets_with_short_page": sum(r["match_fetch_status"] == "PAGINATION_COMPLETE_SHORT_PAGE" for r in coverage),
        "targets_not_retrieved": sum(r["match_fetch_status"] != "PAGINATION_COMPLETE_SHORT_PAGE" for r in coverage),
        "targets_without_verified_cutoff_provenance": sum(r["cutoff_provenance"] != "VERIFIED" for r in coverage),
        "page_provenance_rows": len(pages),
        "validation_errors": len(errors),
        "warnings": len(warnings),
    }
    return errors, warnings, metrics


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_oracle_44_audit.py <audit-directory>", file=sys.stderr)
        return 2
    errors, warnings, metrics = validate(Path(sys.argv[1]))
    print(json.dumps({"metrics": metrics, "errors": errors, "warnings": warnings}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
