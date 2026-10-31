#!/usr/bin/env python3
"""Offline contract validator for the sanitized Selected-50 FootyStats fixture snapshot."""
import argparse
import datetime as dt
import json
import math
from collections import Counter
from pathlib import Path

FINISHED = {"complete", "completed", "finished", "full time", "full-time", "ft", "ended", "played"}
SCORE_FIELDS = ("homeGoalCount", "awayGoalCount")


def parse_aware(value):
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        parsed = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(dt.timezone.utc)


def integer_value(value):
    """Accept only finite, non-negative integer-valued numbers; reject bools."""
    if isinstance(value, bool) or value is None or str(value).strip() == "":
        return None
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(number) or number < 0 or not number.is_integer():
        return None
    return int(number)


def validate(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = []
    if d.get("diagnostic") != "BOUNDED_SELECTED50_CURRENT_FIXTURE_SNAPSHOT":
        errors.append("wrong diagnostic marker")
    for key, expected in (("selected_leagues", 50), ("requests_planned", 50),
                          ("requests_attempted", 50), ("http_200_success", 50),
                          ("request_failures", 0)):
        if d.get(key) != expected:
            errors.append(f"{key}: expected {expected}, got {d.get(key)!r}")
    if d.get("seasons_needing_pagination") != []:
        errors.append("one or more seasons require pagination")
    if d.get("production_eligibility") != "NOT_GRANTED" or d.get("betting_eligibility") != "NOT_GRANTED":
        errors.append("release eligibility must remain NOT_GRANTED")
    if d.get("rate_limit_detected") is not False:
        errors.append("provider rate limit must not have been detected")
    if d.get("provider_retry_attempts") != 0:
        errors.append("automatic provider retries are not permitted")
    if d.get("requests_skipped_after_stop") != 0:
        errors.append("one or more selected-season requests were skipped after a provider failure")
    if d.get("stop_reason") is not None:
        errors.append(f"snapshot stopped before full coverage: {d.get('stop_reason')}")
    interval = d.get("request_interval_seconds")
    if isinstance(interval, bool) or not isinstance(interval, (int, float)) or interval < 2.1:
        errors.append("request_interval_seconds must be at least 2.1 seconds")
    if d.get("raw_provider_payload_persisted") is not False:
        errors.append("raw provider payload must not be persisted")
    if d.get("api_key_persisted") is not False:
        errors.append("API key must not be persisted")
    if d.get("production_ledger_written") is not False:
        errors.append("production ledger must not be written")

    retrieved = parse_aware(d.get("retrieved_utc"))
    window_start = parse_aware(d.get("window_start_utc"))
    window_end = parse_aware(d.get("window_end_utc"))
    if retrieved is None:
        errors.append("retrieved_utc must be a valid ISO timestamp with an explicit timezone")
    if window_start is None:
        errors.append("window_start_utc must be a valid ISO timestamp with an explicit timezone")
    if window_end is None:
        errors.append("window_end_utc must be a valid ISO timestamp with an explicit timezone")
    if window_start is not None and window_end is not None:
        if window_end <= window_start:
            errors.append("window_end_utc must be later than window_start_utc")
        elif abs((window_end - window_start).total_seconds() - 44 * 86400) > 2:
            errors.append("declared window must span 30 days backward and 14 days forward")
        if retrieved is not None and not (window_start < retrieved < window_end):
            errors.append("retrieved_utc must fall inside the declared snapshot window")

    seasons = d.get("per_season")
    rows = d.get("fixture_rows")
    if not isinstance(seasons, list) or len(seasons) != 50:
        errors.append("per_season must contain exactly 50 rows")
    if not isinstance(rows, list):
        errors.append("fixture_rows must be a list")
        rows = []

    selected_season_id_set = set()
    if isinstance(seasons, list):
        season_ids = [str(x.get("selected_season_id") or "").strip() for x in seasons if isinstance(x, dict)]
        if len(season_ids) != len(seasons):
            errors.append("per_season contains a non-object row")
        if len(season_ids) != 50 or any(not sid for sid in season_ids):
            errors.append("one or more selected season IDs are missing")
        if len(set(season_ids)) != 50:
            errors.append("selected season IDs are not unique")
        selected_season_id_set = {sid for sid in season_ids if sid}
        for item in seasons:
            if not isinstance(item, dict):
                continue
            if item.get("http_status") != 200 or item.get("provider_success") is not True:
                errors.append(f"provider request failed for season {item.get('selected_season_id')}")
            if item.get("schedule_status") != "ONE_PAGE_RESPONSE":
                errors.append(f"unexpected pagination state for season {item.get('selected_season_id')}")

    seen = set()
    classes = Counter()
    statuses = Counter()
    no_home = 0
    missing_fields = Counter()
    window_boundary = window_end - dt.timedelta(days=14) if window_end is not None else None

    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"row {i}: fixture row must be an object")
            continue
        mid = str(row.get("id") or "").strip()
        if not mid:
            errors.append(f"row {i}: missing match id")
        elif mid in seen:
            errors.append(f"duplicate match id {mid}")
        seen.add(mid)

        row_season_id = str(row.get("selected_season_id") or "").strip()
        if not row_season_id:
            errors.append(f"row {i}: missing selected season ID")
        elif row_season_id not in selected_season_id_set:
            errors.append(f"row {i}: selected season ID is not in the requested 50-season set")
        if str(row.get("competition_id") or "").strip() != row_season_id:
            errors.append(f"row {i}: competition_id does not match selected season ID")

        for field in ("homeID", "awayID", "home_name", "away_name", "date_unix", "kickoff_utc", "status"):
            if row.get(field) in (None, ""):
                missing_fields[field] += 1
        cls = row.get("window_class")
        if cls not in ("FUTURE_14D", "RECENT_30D"):
            errors.append(f"row {i}: invalid window_class {cls!r}")
        classes[str(cls)] += 1

        status = str(row.get("status") or "").strip().casefold()
        statuses[status] += 1
        if str(row.get("no_home_away", "0")).strip().casefold() in {"1", "true", "yes"}:
            no_home += 1

        kickoff = parse_aware(row.get("kickoff_utc"))
        if kickoff is None:
            errors.append(f"row {i}: kickoff_utc must be a valid ISO timestamp with an explicit timezone")
        elif window_start is not None and window_end is not None:
            if kickoff < window_start or kickoff > window_end:
                errors.append(f"row {i}: kickoff_utc is outside the declared snapshot window")
            if window_boundary is not None:
                expected_class = "FUTURE_14D" if kickoff >= window_boundary else "RECENT_30D"
                if cls != expected_class:
                    errors.append(f"row {i}: window_class disagrees with kickoff_utc and declared window")

        epoch = integer_value(row.get("date_unix"))
        if epoch is None:
            errors.append(f"row {i}: date_unix must be a finite non-negative integer timestamp")
        elif kickoff is not None:
            try:
                epoch_utc = dt.datetime.fromtimestamp(epoch, tz=dt.timezone.utc)
                if abs((epoch_utc - kickoff).total_seconds()) > 1:
                    errors.append(f"row {i}: date_unix and kickoff_utc disagree")
            except (OverflowError, OSError, ValueError):
                errors.append(f"row {i}: date_unix is outside the supported timestamp range")

        parsed_scores = {}
        for field in SCORE_FIELDS:
            value = row.get(field)
            if value not in (None, ""):
                parsed = integer_value(value)
                if parsed is None:
                    errors.append(f"row {i}: {field} must be a finite non-negative integer when present")
                parsed_scores[field] = parsed
            else:
                parsed_scores[field] = None

        if status in FINISHED:
            if any(parsed_scores[field] is None for field in SCORE_FIELDS):
                errors.append(f"row {i}: completed-status row must have two valid integer scores")
            if kickoff is not None and retrieved is not None and kickoff > retrieved:
                errors.append(f"row {i}: completed status conflicts with a future kickoff")

    future = sum(1 for row in rows if isinstance(row, dict) and row.get("window_class") == "FUTURE_14D")
    recent_complete = sum(
        1 for row in rows
        if isinstance(row, dict)
        and row.get("window_class") == "RECENT_30D"
        and str(row.get("status", "")).lower() == "complete"
    )
    if future != d.get("future_14d_fixture_rows"):
        errors.append("future fixture count does not match summary")
    if recent_complete != d.get("recent_completed_30d_rows"):
        errors.append("recent completed count does not match summary")
    if any(missing_fields.values()):
        errors.append("one or more fixture rows have missing required fields")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "selected_seasons": len(seasons) if isinstance(seasons, list) else 0,
        "fixture_rows": len(rows),
        "future_14d_rows": future,
        "recent_completed_30d_rows": recent_complete,
        "no_home_away_rows": no_home,
        "duplicate_match_ids": len(rows) - len(seen),
        "status_counts": dict(statuses),
        "window_class_counts": dict(classes),
        "missing_required_field_counts": dict(missing_fields),
        "production_eligibility": d.get("production_eligibility"),
        "betting_eligibility": d.get("betting_eligibility"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_json")
    args = parser.parse_args()
    result = validate(args.snapshot_json)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
