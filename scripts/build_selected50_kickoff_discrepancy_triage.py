#!/usr/bin/env python3
"""Build a report-only triage view of exact-identity kickoff discrepancies.

This does not resolve schedules, select an authoritative time, or modify any
Oracle probability. Midnight and delta bands are review indicators only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = (
    "status", "schedule_reconciliation_status", "fixture_id", "selected_id",
    "provider_season_id", "home_team_id", "away_team_id", "fixture_identity",
    "runtime_kickoff_utc", "archive_kickoff_utc",
    "delta_minutes_archive_minus_runtime", "archive_source_file",
    "archive_source_row", "resolution_action",
)
MANUAL_ACTION = "MANUAL_AUTHORITATIVE_EVENT_TIME_REVIEW_ONLY_NO_AUTO_CORRECTION"
EXTRA = (
    "archive_kickoff_at_utc_midnight_indicator",
    "absolute_delta_gt_24h_indicator",
    "absolute_delta_le_150m_indicator",
    "triage_bucket",
    "root_cause_status",
    "authoritative_event_time_verified",
    "schedule_auto_correction",
    "production_eligible",
    "betting_eligible",
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_utc(value: str, field: str) -> datetime:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError(f"{field} is empty")
    parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include a UTC offset")
    return parsed.astimezone(timezone.utc)


def classify(row: dict[str, str]) -> dict[str, str]:
    runtime = parse_utc(row["runtime_kickoff_utc"], "runtime_kickoff_utc")
    archive = parse_utc(row["archive_kickoff_utc"], "archive_kickoff_utc")
    supplied_delta = float(row["delta_minutes_archive_minus_runtime"])
    computed_delta = (archive - runtime).total_seconds() / 60.0
    if not math.isfinite(supplied_delta) or not math.isclose(
        supplied_delta, computed_delta, rel_tol=0.0, abs_tol=0.01
    ):
        raise ValueError(
            f"fixture {row.get('fixture_id', '')}: supplied signed delta "
            f"{supplied_delta} does not match recomputed {computed_delta}"
        )

    midnight = archive.hour == 0 and archive.minute == 0 and archive.second == 0
    abs_delta = abs(computed_delta)
    if midnight:
        bucket = "ARCHIVE_KICKOFF_AT_UTC_MIDNIGHT_REVIEW_INDICATOR"
    elif abs_delta > 1440:
        bucket = "NON_MIDNIGHT_ABS_DELTA_GT_24H"
    elif abs_delta <= 150:
        bucket = "NON_MIDNIGHT_ABS_DELTA_LE_150M"
    else:
        bucket = "NON_MIDNIGHT_ABS_DELTA_150M_TO_24H"

    return {
        "archive_kickoff_at_utc_midnight_indicator": "YES" if midnight else "NO",
        "absolute_delta_gt_24h_indicator": "YES" if abs_delta > 1440 else "NO",
        "absolute_delta_le_150m_indicator": "YES" if abs_delta <= 150 else "NO",
        "triage_bucket": bucket,
        "root_cause_status": "NOT_ESTABLISHED_NO_AUTHORITATIVE_EVENT_TIME_SOURCE",
        "authoritative_event_time_verified": "NO",
        "schedule_auto_correction": "NO",
        "production_eligible": "NO",
        "betting_eligible": "NO",
    }


def build(queue_path: Path, out_dir: Path) -> dict:
    rows = read_rows(queue_path)
    if rows:
        missing = [field for field in REQUIRED if field not in rows[0]]
        if missing:
            raise ValueError(f"schedule queue missing required fields: {missing}")
    else:
        with queue_path.open(encoding="utf-8-sig", newline="") as handle:
            headers = next(csv.reader(handle), [])
        missing = [field for field in REQUIRED if field not in headers]
        if missing:
            raise ValueError(f"schedule queue missing required fields: {missing}")

    identities = []
    output = []
    for row in rows:
        if row.get("status") != "REVIEW_REQUIRED" or row.get("schedule_reconciliation_status") != "REVIEW_REQUIRED":
            raise ValueError(f"fixture {row.get('fixture_id', '')}: queue row is not review-required")
        if row.get("resolution_action") != MANUAL_ACTION:
            raise ValueError(f"fixture {row.get('fixture_id', '')}: non-manual resolution action found")
        key = tuple(str(row.get(k) or "").strip() for k in (
            "provider_season_id", "fixture_id", "home_team_id", "away_team_id"
        ))
        if not all(key):
            raise ValueError(f"fixture {row.get('fixture_id', '')}: incomplete exact fixture identity")
        identities.append(key)
        output.append({**row, **classify(row)})

    if len(identities) != len(set(identities)):
        raise ValueError("duplicate exact fixture identity in schedule reconciliation queue")

    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "oracle_selected50_kickoff_discrepancy_triage.csv"
    fieldnames = list(rows[0].keys()) + list(EXTRA) if rows else list(headers) + list(EXTRA)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output)

    source_sha = hashlib.sha256(queue_path.read_bytes()).hexdigest()
    output_sha = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    buckets = Counter(row["triage_bucket"] for row in output)
    midnight_count = sum(row["archive_kickoff_at_utc_midnight_indicator"] == "YES" for row in output)
    over_24h_count = sum(row["absolute_delta_gt_24h_indicator"] == "YES" for row in output)
    within_150m_count = sum(row["absolute_delta_le_150m_indicator"] == "YES" for row in output)
    qa = {
        "status": "PASS_REPORT_ONLY_KICKOFF_TRIAGE",
        "source_rows": len(rows),
        "output_rows": len(output),
        "exact_fixture_identity_keys_unique": True,
        "signed_delta_recomputed_and_verified": True,
        "triage_bucket_counts": dict(sorted(buckets.items())),
        "archive_kickoff_at_utc_midnight_indicator_count": midnight_count,
        "absolute_delta_gt_24h_indicator_count": over_24h_count,
        "absolute_delta_le_150m_indicator_count": within_150m_count,
        "indicators_may_overlap": True,
        "root_cause_status": "NOT_ESTABLISHED_NO_AUTHORITATIVE_EVENT_TIME_SOURCE",
        "authoritative_event_time_verified_rows": 0,
        "schedule_auto_corrections": 0,
        "all_rows_manual_review_only": all(row.get("resolution_action") == MANUAL_ACTION for row in rows),
        "production_eligible": False,
        "betting_eligible": False,
        "source_file": str(queue_path),
        "source_sha256": source_sha,
        "output_file": str(csv_path),
        "output_sha256": output_sha,
    }
    qa_path = out_dir / "oracle_selected50_kickoff_discrepancy_triage_qa.json"
    qa_path.write_text(json.dumps(qa, indent=2) + "\n", encoding="utf-8")
    return qa


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", required=True, help="Workflow-generated schedule reconciliation queue CSV")
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    qa = build(Path(args.queue), Path(args.out_dir))
    print(json.dumps(qa, indent=2))


if __name__ == "__main__":
    main()
