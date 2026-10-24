#!/usr/bin/env python3
"""Fail-closed research gate for Oracle feature point-in-time provenance.

Input CSV contract:
fixture_id,feature_name,kickoff_utc,observed_at_utc,retrieved_at_utc,
source_id,snapshot_hash,value

This validator does not establish source authenticity or season completeness.
It only checks that each row carries auditable provenance fields and that the
feature observation timestamp is strictly earlier than kickoff.
"""
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = (
    "fixture_id", "feature_name", "kickoff_utc", "observed_at_utc",
    "retrieved_at_utc", "source_id", "snapshot_hash", "value",
)


def parse_utc(value):
    value = (value or "").strip()
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(timezone.utc)


def validate(rows):
    errors = []
    checked = 0
    for index, row in enumerate(rows, start=2):
        missing = [key for key in REQUIRED if not str(row.get(key, "")).strip()]
        if missing:
            errors.append({"row": index, "reason": "MISSING_REQUIRED_FIELDS", "fields": missing})
            continue
        kickoff = parse_utc(row["kickoff_utc"])
        observed = parse_utc(row["observed_at_utc"])
        retrieved = parse_utc(row["retrieved_at_utc"])
        if kickoff is None or observed is None or retrieved is None:
            errors.append({"row": index, "reason": "INVALID_OR_TIMEZONE_NAIVE_TIMESTAMP"})
            continue
        if observed >= kickoff:
            errors.append({"row": index, "reason": "FEATURE_NOT_PROVEN_PRE_KICKOFF"})
            continue
        if retrieved < observed:
            errors.append({"row": index, "reason": "RETRIEVAL_PRECEDES_OBSERVATION"})
            continue
        digest = row["snapshot_hash"].strip().lower()
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            errors.append({"row": index, "reason": "INVALID_SNAPSHOT_SHA256"})
            continue
        checked += 1
    return {
        "rows_seen": len(rows),
        "rows_passing_row_level_checks": checked,
        "rows_rejected": len(errors),
        "errors": errors,
        "feature_point_in_time_gate_passed": bool(rows) and not errors and checked == len(rows),
        "source_authenticity_proven": False,
        "season_completeness_proven": False,
        "production_changes": False,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_oracle_feature_provenance.py feature_snapshot.csv", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        rows = list(reader)
    missing_columns = [key for key in REQUIRED if key not in fields]
    if missing_columns:
        report = {
            "rows_seen": len(rows),
            "rows_passing_row_level_checks": 0,
            "rows_rejected": len(rows),
            "missing_columns": missing_columns,
            "feature_point_in_time_gate_passed": False,
            "source_authenticity_proven": False,
            "season_completeness_proven": False,
            "production_changes": False,
        }
        print(json.dumps(report, indent=2))
        return 1
    report = validate(rows)
    print(json.dumps(report, indent=2))
    return 0 if report["feature_point_in_time_gate_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
