#!/usr/bin/env python3
"""Research-only validation of catalogue candidate mappings and season date metadata.

Does not auto-approve mappings, fetch fixtures, or modify Oracle's governed registry.
Usage: python scripts/validate_oracle_season_crosswalk.py <crosswalk.csv>
"""
import csv
import json
import sys
from datetime import date
from pathlib import Path

EXPECTED_TARGETS = 44
REQUIRED = {
    "target_code", "catalogue_status", "provider_name",
    "candidate_season_ids", "candidate_season_labels", "candidate_season_dates",
    "decision",
}


def parse_date(value):
    value = (value or "").strip()
    if not value:
        return None
    # Accept ISO date or ISO datetime; never infer a date from a season label.
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def validate(path):
    errors, warnings = [], []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        return ["Crosswalk has no rows"], [], {}
    missing = REQUIRED - set(rows[0])
    if missing:
        return ["Missing columns: " + ", ".join(sorted(missing))], [], {}

    codes = [r["target_code"].strip() for r in rows]
    unique_codes = set(codes)
    if len(unique_codes) != EXPECTED_TARGETS:
        errors.append(f"Expected {EXPECTED_TARGETS} unique target codes; found {len(unique_codes)}")
    if len(rows) != EXPECTED_TARGETS:
        warnings.append(f"Crosswalk has {len(rows)} rows for {len(unique_codes)} targets; duplicate candidate rows require manual review")

    per_target = {}
    for row in rows:
        code = row["target_code"].strip()
        per_target.setdefault(code, []).append(row)
        status = (row.get("catalogue_status") or "").strip()
        season_ids = [x.strip() for x in (row.get("candidate_season_ids") or "").split(";") if x.strip()]
        labels = [x.strip() for x in (row.get("candidate_season_labels") or "").split(";") if x.strip()]
        date_pairs = [x.strip() for x in (row.get("candidate_season_dates") or "").split(";") if x.strip()]
        if status != "EXACT_ALIAS_CANDIDATE":
            warnings.append(f"{code}: catalogue status is {status or 'blank'}; mapping remains unresolved")
        if not season_ids:
            warnings.append(f"{code}: no candidate season ID")
        if len(set(season_ids)) != len(season_ids):
            errors.append(f"{code}: duplicate season IDs in candidate metadata")
        if len(labels) != len(season_ids):
            warnings.append(f"{code}: season IDs and labels have mismatched counts")
        # The provider catalogue can omit season dates. Treat these as unavailable
        # evidence, not malformed data; do not infer dates from season labels.
        if date_pairs and len(date_pairs) != len(season_ids):
            warnings.append(f"{code}: season IDs and date pairs have mismatched counts")
        for pair in date_pairs:
            parts = pair.split("/", 1)
            if len(parts) != 2:
                warnings.append(f"{code}: malformed season date pair {pair!r}")
                continue
            start, end = parse_date(parts[0]), parse_date(parts[1])
            if start is None or end is None:
                warnings.append(f"{code}: missing or invalid ISO season dates {pair!r}")
            elif end < start:
                errors.append(f"{code}: season end precedes season start ({pair})")
        if (row.get("decision") or "").strip() != "REVIEW_REQUIRED_NOT_AUTO_MAPPED":
            warnings.append(f"{code}: candidate decision is not marked for independent review")

    for code, candidates in per_target.items():
        if len(candidates) > 1:
            warnings.append(f"{code}: multiple crosswalk rows; exact mapping must be resolved manually")
    metrics = {
        "crosswalk_rows": len(rows),
        "unique_target_codes": len(unique_codes),
        "targets_with_provider_season_ids": sum(any((r.get("candidate_season_ids") or "").strip() for r in per_target[c]) for c in per_target),
        "targets_with_season_labels": sum(any((r.get("candidate_season_labels") or "").strip() for r in per_target[c]) for c in per_target),
        "targets_with_season_dates": sum(any((r.get("candidate_season_dates") or "").strip().strip("/; ") for r in per_target[c]) for c in per_target),
        "targets_with_exact_alias_candidate": sum(any((r.get("catalogue_status") or "").strip() == "EXACT_ALIAS_CANDIDATE" for r in per_target[c]) for c in per_target),
        "validation_errors": len(errors),
        "warnings": len(warnings),
        "mapping_approval": "NOT_GRANTED",
        "note": "Valid date syntax and coherent ranges do not independently prove that a provider season matches the intended competition or requested historical window.",
    }
    return errors, warnings, metrics


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_oracle_season_crosswalk.py <crosswalk.csv>", file=sys.stderr)
        return 2
    errors, warnings, metrics = validate(Path(sys.argv[1]))
    print(json.dumps({"metrics": metrics, "errors": errors, "warnings": warnings}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
