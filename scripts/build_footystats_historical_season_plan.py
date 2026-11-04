#!/usr/bin/env python3
"""Build an exact-ID historical season plan from the FootyStats provider registry.

Offline only. This plans season partitions intersecting an inclusive history window;
it does not call FootyStats or infer fixture-level coverage. Every catalogue row is
accounted for as planned or explicitly excluded/quarantined.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any, Iterable

from normalize_footystats_season_year import normalize_season_year

PLAN_FIELDS = (
    "provider",
    "provider_country",
    "provider_league_name",
    "provider_season_label",
    "provider_season_id",
    "provider_competition_id",
    "catalogue_scope",
    "catalogue_retrieved_utc",
    "season_start_year",
    "season_end_year",
    "history_start_date",
    "history_end_date",
    "fixture_filter_start_utc",
    "fixture_filter_end_utc_inclusive",
    "fixture_kickoff_filter_required",
    "plan_status",
    "production_eligible",
    "betting_eligible",
)
EXCLUDED_FIELDS = (
    "provider_league_name",
    "provider_season_label",
    "provider_season_id",
    "exclusion_reason",
    "season_year_parse_status",
)


def _parse_date(value: str | date, label: str) -> date:
    if isinstance(value, date):
        return value
    try:
        parsed = date.fromisoformat(str(value))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be an ISO YYYY-MM-DD date") from exc
    if parsed.isoformat() != str(value):
        raise ValueError(f"{label} must be an ISO YYYY-MM-DD date")
    return parsed


def build_plan(
    registry: dict[str, Any],
    start_date: str | date,
    end_date: str | date,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    start = _parse_date(start_date, "start_date")
    end = _parse_date(end_date, "end_date")
    if start > end:
        raise ValueError("history start_date must not be later than end_date")
    if registry.get("source_of_truth") != "FootyStats":
        raise ValueError("registry source_of_truth must be FootyStats")
    scope = registry.get("catalogue_scope")
    if scope not in {"chosen_leagues_only", "all_available"}:
        raise ValueError("registry catalogue_scope is missing or unsupported")
    retrieved = registry.get("catalogue_retrieved_utc")
    if not isinstance(retrieved, str) or not retrieved.strip():
        raise ValueError("registry catalogue_retrieved_utc is required")
    try:
        stamp = datetime.fromisoformat(retrieved.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("registry catalogue_retrieved_utc must be ISO-8601") from exc
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError("registry catalogue_retrieved_utc must include timezone")
    seasons = registry.get("seasons")
    if not isinstance(seasons, list) or not seasons:
        raise ValueError("registry seasons must be a non-empty list")

    seen_ids: set[str] = set()
    planned: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    league_names: set[str] = set()
    for index, raw in enumerate(seasons, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"registry season row {index} is not an object")
        sid = str(raw.get("provider_season_id") or "").strip()
        league = str(raw.get("provider_league_name") or "").strip()
        label = str(raw.get("provider_season_label") or "").strip()
        if not sid:
            excluded.append({
                "provider_league_name": league,
                "provider_season_label": label,
                "provider_season_id": "",
                "exclusion_reason": "MISSING_PROVIDER_SEASON_ID",
                "season_year_parse_status": "NOT_PARSED",
            })
            continue
        if sid in seen_ids:
            raise ValueError(f"duplicate provider season ID in registry: {sid}")
        seen_ids.add(sid)
        if not league:
            excluded.append({
                "provider_league_name": "",
                "provider_season_label": label,
                "provider_season_id": sid,
                "exclusion_reason": "MISSING_PROVIDER_LEAGUE_NAME",
                "season_year_parse_status": "NOT_PARSED",
            })
            continue
        if not label:
            excluded.append({
                "provider_league_name": league,
                "provider_season_label": "",
                "provider_season_id": sid,
                "exclusion_reason": "MISSING_PROVIDER_SEASON_LABEL",
                "season_year_parse_status": "MISSING_YEAR_TOKEN",
            })
            continue

        parsed = normalize_season_year(label)
        if parsed.start_year is None:
            excluded.append({
                "provider_league_name": league,
                "provider_season_label": label,
                "provider_season_id": sid,
                "exclusion_reason": "INVALID_OR_UNSUPPORTED_SEASON_LABEL",
                "season_year_parse_status": parsed.status,
            })
            continue
        season_start = parsed.start_year
        season_end = parsed.end_year if parsed.end_year is not None else parsed.start_year
        if season_start > season_end:
            excluded.append({
                "provider_league_name": league,
                "provider_season_label": label,
                "provider_season_id": sid,
                "exclusion_reason": "INVALID_SEASON_YEAR_ORDER",
                "season_year_parse_status": parsed.status,
            })
            continue
        if season_start > end.year or season_end < start.year:
            excluded.append({
                "provider_league_name": league,
                "provider_season_label": label,
                "provider_season_id": sid,
                "exclusion_reason": "SEASON_OUTSIDE_HISTORY_WINDOW",
                "season_year_parse_status": parsed.status,
            })
            continue

        league_names.add(league)
        planned.append({
            "provider": "FootyStats",
            "provider_country": str(raw.get("provider_country") or ""),
            "provider_league_name": league,
            "provider_season_label": label,
            "provider_season_id": sid,
            "provider_competition_id": str(raw.get("provider_competition_id") or ""),
            "catalogue_scope": scope,
            "catalogue_retrieved_utc": stamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "season_start_year": season_start,
            "season_end_year": season_end,
            "history_start_date": start.isoformat(),
            "history_end_date": end.isoformat(),
            "fixture_filter_start_utc": datetime.combine(start, time.min, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
            "fixture_filter_end_utc_inclusive": datetime.combine(end, time.max, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
            "fixture_kickoff_filter_required": True,
            "plan_status": "PLANNED_NOT_RETRIEVED",
            "production_eligible": False,
            "betting_eligible": False,
        })

    if not planned:
        raise ValueError("no valid provider seasons intersect the requested history window")
    planned.sort(key=lambda row: (row["provider_league_name"], row["season_start_year"], row["provider_season_id"]))
    excluded.sort(key=lambda row: (row["provider_league_name"], row["provider_season_label"], row["provider_season_id"]))
    summary = {
        "schema_version": "1.0",
        "diagnostic": "FOOTYSTATS_PROVIDER_HISTORICAL_SEASON_PLAN",
        "source_of_truth": "FootyStats",
        "catalogue_scope": scope,
        "catalogue_retrieved_utc": stamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "history_start_date": start.isoformat(),
        "history_end_date_inclusive": end.isoformat(),
        "fixture_kickoff_filter": {
            "start_utc_inclusive": datetime.combine(start, time.min, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
            "end_utc_inclusive": datetime.combine(end, time.max, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z"),
            "required": True,
            "rule": "Filter every returned fixture by its explicit-offset kickoff timestamp; season membership alone is not fixture-date coverage.",
        },
        "catalogue_provider_season_count": len(seasons),
        "catalogue_unique_provider_season_ids": len(seen_ids),
        "planned_provider_season_count": len(planned),
        "planned_provider_league_count": len(league_names),
        "excluded_provider_season_count": len(excluded),
        "excluded_reason_counts": {
            reason: sum(1 for row in excluded if row["exclusion_reason"] == reason)
            for reason in sorted({row["exclusion_reason"] for row in excluded})
        },
        "planned_provider_season_ids": [row["provider_season_id"] for row in planned],
        "all_catalogue_rows_accounted_for": len(planned) + len(excluded) == len(seasons),
        "api_requests_made": 0,
        "production_logic_changed": False,
        "production_eligible": False,
        "betting_eligible": False,
        "plan_status": "OFFLINE_PLAN_ONLY",
        "seasons": planned,
        "excluded_seasons": excluded,
    }
    return summary, planned


def write_outputs(summary: dict[str, Any], plan_csv: Path, excluded_csv: Path, summary_json: Path) -> None:
    plan_csv.parent.mkdir(parents=True, exist_ok=True)
    excluded_csv.parent.mkdir(parents=True, exist_ok=True)
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    with plan_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PLAN_FIELDS)
        writer.writeheader()
        writer.writerows(summary["seasons"])
    with excluded_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXCLUDED_FIELDS)
        writer.writeheader()
        writer.writerows(summary["excluded_seasons"])
    summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry-json", required=True, type=Path)
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--plan-csv", required=True, type=Path)
    parser.add_argument("--excluded-csv", required=True, type=Path)
    parser.add_argument("--summary-json", required=True, type=Path)
    args = parser.parse_args()
    registry = json.loads(args.registry_json.read_text(encoding="utf-8"))
    summary, _ = build_plan(registry, args.start_date, args.end_date)
    write_outputs(summary, args.plan_csv, args.excluded_csv, args.summary_json)
    print(json.dumps({
        "history_window": [summary["history_start_date"], summary["history_end_date_inclusive"]],
        "catalogue_seasons": summary["catalogue_provider_season_count"],
        "planned_seasons": summary["planned_provider_season_count"],
        "planned_leagues": summary["planned_provider_league_count"],
        "excluded_seasons": summary["excluded_provider_season_count"],
        "api_requests_made": summary["api_requests_made"],
        "production_eligible": summary["production_eligible"],
        "betting_eligible": summary["betting_eligible"],
    }, indent=2))


if __name__ == "__main__":
    main()
