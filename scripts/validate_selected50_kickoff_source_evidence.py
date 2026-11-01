#!/usr/bin/env python3
"""Fail-closed QA for the Selected-50 report-only kickoff evidence register.

No network calls, source edits, schedule corrections, or production writes.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CORROBORATED = {
    "AUTHORITATIVE_TIME_CORROBORATES_RUNTIME",
    "AUTHORITATIVE_BODY_MATCH_TITLE_SLUG_MISMATCH",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def utc(value: str) -> datetime:
    if not value:
        raise ValueError("missing UTC timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp has no timezone: {value}")
    return parsed.astimezone(timezone.utc)


def source_timezone(value: str):
    try:
        return ZoneInfo(value)
    except ZoneInfoNotFoundError:
        match = re.search(r"UTC([+-])(\d{2}):?(\d{2})", value)
        if not match:
            raise ValueError(f"unsupported source timezone: {value}")
        sign = 1 if match.group(1) == "+" else -1
        offset = sign * (int(match.group(2)) * 60 + int(match.group(3)))
        return timezone(timedelta(minutes=offset))


def validate(queue_rows: list[dict[str, str]], evidence_rows: list[dict[str, str]]) -> dict:
    if not queue_rows or not evidence_rows:
        raise ValueError("queue and evidence register must both contain rows")

    def keyed(rows, label):
        result = {}
        for row in rows:
            fixture_id = (row.get("fixture_id") or "").strip()
            if not fixture_id or fixture_id in result:
                raise ValueError(f"{label}: missing or duplicate fixture_id {fixture_id!r}")
            result[fixture_id] = row
        return result

    queue = keyed(queue_rows, "queue")
    evidence = keyed(evidence_rows, "evidence")
    if set(queue) != set(evidence):
        missing = sorted(set(queue) - set(evidence))
        extra = sorted(set(evidence) - set(queue))
        raise ValueError(f"fixture identity set mismatch; missing={missing}, extra={extra}")

    statuses = Counter()
    corroborated = unresolved = 0
    for fixture_id, ev in evidence.items():
        q = queue[fixture_id]
        if (ev.get("fixture") or "").strip() != (q.get("fixture") or "").strip():
            raise ValueError(f"{fixture_id}: fixture label differs from exact queue row")
        for field in ("runtime_kickoff_utc", "archive_kickoff_utc"):
            if utc(ev.get(field, "")) != utc(q.get(field, "")):
                raise ValueError(f"{fixture_id}: {field} differs from source queue")

        status = (ev.get("external_source_status") or "").strip()
        decision = (ev.get("decision") or "").strip().upper()
        statuses[status] += 1
        if not (ev.get("source_url") or "").strip().startswith("https://"):
            raise ValueError(f"{fixture_id}: missing HTTPS source reference")
        action = (q.get("resolution_action") or "").upper()
        if "MANUAL" not in action or "NO_AUTO_CORRECTION" not in action:
            raise ValueError(f"{fixture_id}: source queue does not enforce manual review/no auto-correction")
        if "schedule_auto_correction" in q and q.get("schedule_auto_correction") != "NO":
            raise ValueError(f"{fixture_id}: source queue permits a schedule auto-correction")
        for eligibility_field in ("production_eligible", "betting_eligible"):
            if eligibility_field in q and q.get(eligibility_field) != "NO":
                raise ValueError(f"{fixture_id}: queue row is not explicitly ineligible")

        converted = (ev.get("source_converted_utc") or "").strip()
        local_text = (ev.get("source_local_kickoff") or "").strip()
        zone_text = (ev.get("source_timezone") or "").strip()
        if status in CORROBORATED:
            if not converted or not local_text or not zone_text:
                raise ValueError(f"{fixture_id}: corroborated source lacks local time, zone or UTC conversion")
            local = datetime.fromisoformat(local_text)
            if local.tzinfo is not None:
                raise ValueError(f"{fixture_id}: source local time must be timezone-naive")
            calculated = local.replace(tzinfo=source_timezone(zone_text)).astimezone(timezone.utc)
            if calculated != utc(converted):
                raise ValueError(f"{fixture_id}: source local-to-UTC conversion mismatch")
            if utc(converted) != utc(ev.get("runtime_kickoff_utc", "")):
                raise ValueError(f"{fixture_id}: authoritative source does not corroborate runtime kickoff")
            if "NO_AUTO_CORRECTION" not in decision and "NO_CORRECTION" not in decision:
                raise ValueError(f"{fixture_id}: corroboration decision must prohibit automatic correction")
            corroborated += 1
        else:
            if converted:
                raise ValueError(f"{fixture_id}: unresolved/conflicted source must not carry accepted UTC")
            if "REVIEW_REQUIRED" not in decision:
                raise ValueError(f"{fixture_id}: unresolved source must remain review-required")
            unresolved += 1

    for fixture_id, q in queue.items():
        if q.get("schedule_reconciliation_status") != "REVIEW_REQUIRED":
            raise ValueError(f"{fixture_id}: original schedule queue must remain review-required")

    return {
        "status": "PASS_REPORT_ONLY_KICKOFF_EVIDENCE_REGISTER",
        "queue_rows": len(queue),
        "evidence_rows": len(evidence),
        "exact_fixture_id_set_match": True,
        "unique_fixture_ids": True,
        "source_status_counts": dict(sorted(statuses.items())),
        "authoritative_runtime_corroborations": corroborated,
        "unresolved_or_conflicted_sources": unresolved,
        "schedule_auto_corrections": 0,
        "original_queue_rows_still_review_required": len(queue),
        "production_eligible": False,
        "betting_eligible": False,
        "network_calls_made": 0,
        "interpretation": "Evidence overlay only; does not edit the canonical schedule queue or certify a schedule correction."
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", required=True, type=Path)
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    result = validate(read_csv(args.queue), read_csv(args.evidence))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
