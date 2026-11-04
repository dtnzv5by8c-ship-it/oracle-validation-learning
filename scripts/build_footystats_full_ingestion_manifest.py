#!/usr/bin/env python3
"""Build an offline, exact-ID full-ingestion request manifest from preflight evidence.

This planner makes no provider calls and stores no raw payloads. It plans full
match/team pagination only for seasons with a successful sanitized endpoint
preflight. H2H, recent form and venue splits are derived from the completed
match spine; fixture-time standings and xG remain separately gated.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TASK_FIELDS = [
    "task_id", "batch_id", "provider", "provider_league_name",
    "provider_season_label", "provider_season_id", "endpoint",
    "page", "max_per_page", "include", "max_time_unix",
    "expected_total_results", "expected_page_count",
    "request_status", "raw_storage_required",
    "production_eligible", "betting_eligible",
]
COVERAGE_FIELDS = [
    "provider_league_name", "provider_season_label", "provider_season_id",
    "preflight_status", "matches_total_results", "matches_per_page",
    "matches_page_count", "teams_total_results", "teams_per_page",
    "teams_page_count", "tables_endpoint_verified", "season_endpoint_verified",
    "planned_ingestion_requests", "ingestion_plan_status",
    "production_eligible", "betting_eligible",
]
BATCH_FIELDS = ["batch_id", "task_count", "first_task_id", "last_task_id", "status"]


def parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("preflight timestamp must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def read_plan(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "provider", "provider_league_name", "provider_season_label",
            "provider_season_id", "production_eligible", "betting_eligible",
        }
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError("season plan is missing required fields")
        rows = list(reader)
    if not rows:
        raise ValueError("season plan is empty")
    ids = [str(row["provider_season_id"]).strip() for row in rows]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("season plan has missing or duplicate provider season IDs")
    for row in rows:
        if row["provider"] != "FootyStats":
            raise ValueError("non-FootyStats season in plan")
        if str(row["production_eligible"]).lower() not in {"false", "0"}:
            raise ValueError("season plan must remain production-ineligible")
        if str(row["betting_eligible"]).lower() not in {"false", "0"}:
            raise ValueError("season plan must remain betting-ineligible")
    return rows


def latest_preflight_by_season(report_dir: Path) -> dict[str, dict[str, Any]]:
    latest: dict[str, tuple[str, dict[str, Any]]] = {}
    if not report_dir.exists():
        return {}
    terminal_prefixes = ("ENDPOINT_PREFLIGHT_COMPLETE",)
    for path in report_dir.glob("footystats-preflight-run-*.json"):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        stamp = str(report.get("finished_at_utc") or report.get("started_at_utc") or "")
        for season in report.get("season_results", []):
            sid = str(season.get("provider_season_id") or "")
            status = str(season.get("season_status") or "")
            if not sid or not status.startswith(terminal_prefixes):
                continue
            previous = latest.get(sid)
            if previous is None or stamp > previous[0]:
                latest[sid] = (stamp, season)
    return {sid: value[1] for sid, value in latest.items()}


def page_contract(season: dict[str, Any], key: str) -> tuple[int, int]:
    item = season.get(key)
    if not isinstance(item, dict):
        raise ValueError(f"missing {key} pagination evidence")
    total = item.get("total_results")
    per_page = item.get("per_page")
    pages = item.get("expected_page_count")
    if any(isinstance(value, bool) for value in (total, per_page, pages)):
        raise ValueError(f"invalid {key} pagination evidence")
    try:
        total_i, per_page_i, pages_i = int(total), int(per_page), int(pages)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(f"invalid {key} pagination evidence") from None
    if total_i < 0 or per_page_i < 1 or pages_i < 1:
        raise ValueError(f"invalid {key} pagination evidence")
    expected_pages = max(1, (total_i + per_page_i - 1) // per_page_i)
    if pages_i != expected_pages:
        raise ValueError(f"{key} expected_page_count conflicts with total/per_page")
    if item.get("fetched_pages") != 1:
        raise ValueError(f"{key} page-1 preflight evidence is missing")
    return total_i, pages_i


def response_max_time(season: dict[str, Any], key: str) -> int:
    meta = season.get(key)
    if not isinstance(meta, dict) or not meta.get("fetched_at_utc"):
        raise ValueError(f"missing timestamp provenance for {key}")
    return int(parse_utc(str(meta["fetched_at_utc"])).timestamp())


def build_manifest(
    plan_rows: list[dict[str, str]],
    preflight_by_season: dict[str, dict[str, Any]],
    max_requests_per_batch: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    if max_requests_per_batch < 1 or max_requests_per_batch > 1500:
        raise ValueError("max_requests_per_batch must be 1..1500")

    tasks: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    blocked_count = 0
    completed_count = 0

    for row in plan_rows:
        sid = str(row["provider_season_id"])
        league = row["provider_league_name"]
        label = row["provider_season_label"]
        preflight = preflight_by_season.get(sid)
        base = {
            "provider_league_name": league,
            "provider_season_label": label,
            "provider_season_id": sid,
            "preflight_status": "NOT_PREFLIGHTED",
            "matches_total_results": "",
            "matches_per_page": "",
            "matches_page_count": "",
            "teams_total_results": "",
            "teams_per_page": "",
            "teams_page_count": "",
            "tables_endpoint_verified": False,
            "season_endpoint_verified": False,
            "planned_ingestion_requests": 0,
            "ingestion_plan_status": "BLOCKED_NO_COMPLETE_PREFLIGHT",
            "production_eligible": False,
            "betting_eligible": False,
        }
        if not preflight:
            blocked_count += 1
            coverage.append(base)
            continue

        status = str(preflight.get("season_status") or "")
        base["preflight_status"] = status
        if (
            preflight.get("provider_league_name") != league
            or preflight.get("provider_season_label") != label
        ):
            base["ingestion_plan_status"] = "BLOCKED_EXACT_SEASON_IDENTITY_MISMATCH"
            blocked_count += 1
            coverage.append(base)
            continue
        try:
            matches_total, match_pages = page_contract(preflight, "league_matches")
            teams_total, team_pages = page_contract(preflight, "league_teams")
            if not isinstance(preflight.get("league_tables"), dict):
                raise ValueError("league-tables response not verified")
            if preflight["league_tables"].get("response_status") != "SUCCESS_SHAPE_VERIFIED":
                raise ValueError("league-tables response shape is not verified")
            if not isinstance(preflight.get("league_season"), dict):
                raise ValueError("league-season response not verified")
            if preflight["league_season"].get("response_status") != "SUCCESS_SHAPE_VERIFIED":
                raise ValueError("league-season response shape is not verified")
            match_meta = preflight.get("league_matches_response")
            team_meta = preflight.get("league_teams_response")
            table_meta = preflight.get("league_tables_response")
            season_meta = preflight.get("league_season_response")
            expected_endpoints = ("league-matches", "league-teams", "league-tables", "league-season")
            if not all(
                isinstance(meta, dict) and meta.get("http_status") == 200 and meta.get("endpoint") == endpoint
                for meta, endpoint in zip((match_meta, team_meta, table_meta, season_meta), expected_endpoints)
            ):
                raise ValueError("one or more endpoint response metadata records are not successful or exact")
            team_max_time = response_max_time(preflight, "league_teams_response")
            table_max_time = response_max_time(preflight, "league_tables_response")
            season_max_time = response_max_time(preflight, "league_season_response")
        except (ValueError, TypeError):
            base["ingestion_plan_status"] = "BLOCKED_INCOMPLETE_PREFLIGHT_EVIDENCE"
            blocked_count += 1
            coverage.append(base)
            continue

        base.update({
            "matches_total_results": matches_total,
            "matches_per_page": preflight["league_matches"]["per_page"],
            "matches_page_count": match_pages,
            "teams_total_results": teams_total,
            "teams_per_page": preflight["league_teams"]["per_page"],
            "teams_page_count": team_pages,
            "tables_endpoint_verified": True,
            "season_endpoint_verified": True,
        })

        season_tasks: list[dict[str, Any]] = []
        for page in range(1, match_pages + 1):
            season_tasks.append({
                "provider": "FootyStats",
                "provider_league_name": league,
                "provider_season_label": label,
                "provider_season_id": sid,
                "endpoint": "league-matches",
                "page": page,
                "max_per_page": 1000,
                "include": "",
                "max_time_unix": "",
                "expected_total_results": matches_total,
                "expected_page_count": match_pages,
                "request_status": "PLANNED_NOT_EXECUTED",
                "raw_storage_required": True,
                "production_eligible": False,
                "betting_eligible": False,
            })
        for page in range(1, team_pages + 1):
            season_tasks.append({
                "provider": "FootyStats",
                "provider_league_name": league,
                "provider_season_label": label,
                "provider_season_id": sid,
                "endpoint": "league-teams",
                "page": page,
                "max_per_page": "",
                "include": "stats",
                "max_time_unix": team_max_time,
                "expected_total_results": teams_total,
                "expected_page_count": team_pages,
                "request_status": "PLANNED_NOT_EXECUTED",
                "raw_storage_required": True,
                "production_eligible": False,
                "betting_eligible": False,
            })
        for endpoint, max_time in (("league-tables", table_max_time), ("league-season", season_max_time)):
            season_tasks.append({
                "provider": "FootyStats",
                "provider_league_name": league,
                "provider_season_label": label,
                "provider_season_id": sid,
                "endpoint": endpoint,
                "page": 1,
                "max_per_page": "",
                "include": "",
                "max_time_unix": max_time,
                "expected_total_results": "",
                "expected_page_count": 1,
                "request_status": "PLANNED_NOT_EXECUTED",
                "raw_storage_required": True,
                "production_eligible": False,
                "betting_eligible": False,
            })

        base["planned_ingestion_requests"] = len(season_tasks)
        base["ingestion_plan_status"] = "PLANNED_REQUIRES_PRIVATE_RAW_ARCHIVE"
        coverage.append(base)
        completed_count += 1
        for task in season_tasks:
            tasks.append(task)

    # Deterministic stable task IDs and hourly batches. The executor must still
    # reserve against the live rolling ledger immediately before each batch.
    for index, task in enumerate(tasks, start=1):
        task["task_id"] = f"FS:{task['provider_season_id']}:{task['endpoint']}:p{task['page']}"
        task["batch_id"] = f"batch-{((index - 1) // max_requests_per_batch) + 1:04d}"

    batches: list[dict[str, Any]] = []
    for batch_id in sorted({task["batch_id"] for task in tasks}):
        group = [task for task in tasks if task["batch_id"] == batch_id]
        batches.append({
            "batch_id": batch_id,
            "task_count": len(group),
            "first_task_id": group[0]["task_id"],
            "last_task_id": group[-1]["task_id"],
            "status": "PLANNED_NOT_EXECUTED",
        })

    summary = {
        "schema_version": "1.0",
        "diagnostic": "FOOTYSTATS_FULL_HISTORICAL_INGESTION_MANIFEST",
        "source_of_truth": "FootyStats selected provider catalogue",
        "history_start_date": "2024-01-01",
        "history_end_date": max((row.get("history_end_date") or "" for row in plan_rows), default=""),
        "planned_provider_league_count": len({row["provider_league_name"] for row in plan_rows}),
        "planned_provider_season_count": len(plan_rows),
        "seasons_with_complete_endpoint_preflight": completed_count,
        "seasons_blocked_or_not_preflighted": blocked_count,
        "planned_request_count": len(tasks),
        "planned_batches": len(batches),
        "max_requests_per_batch": max_requests_per_batch,
        "absolute_requests_per_rolling_hour": 1800,
        "operational_requests_per_rolling_hour": 1500,
        "reserved_headroom": 300,
        "h2h_strategy": "DERIVE_FROM_COMPLETE_EXACT_CHRONOLOGICAL_MATCH_SPINE_NO_PER_FIXTURE_DETAIL_CALLS",
        "recent_form_strategy": "DERIVE_FROM_COMPLETE_MATCH_SPINE_WITH_STRICT_PRE_KICKOFF_CUTOFF",
        "home_away_form_strategy": "DERIVE_FROM_EXACT_ORDERED_HOME_AWAY_TEAM_IDS",
        "fixture_time_standings_status": "NOT_VERIFIED_REQUIRES_AS_OF_RECONSTRUCTION_OR_SEPARATE_VALIDATION",
        "xg_status": "QUARANTINED_NO_FIXTURE_LEVEL_CAPTURE_AND_REVISION_PROVENANCE",
        "private_raw_archive_write_required": True,
        "raw_payloads_written": False,
        "api_requests_made": 0,
        "production_logic_changed": False,
        "production_eligible": False,
        "betting_eligible": False,
    }
    return tasks, coverage, batches, summary


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-csv", required=True, type=Path)
    parser.add_argument("--preflight-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-requests-per-batch", type=int, default=1500)
    args = parser.parse_args()

    plan = read_plan(args.plan_csv)
    preflight = latest_preflight_by_season(args.preflight_dir)
    tasks, coverage, batches, summary = build_manifest(
        plan, preflight, args.max_requests_per_batch
    )
    write_csv(args.output_dir / "ingestion-request-manifest.csv", TASK_FIELDS, tasks)
    write_csv(args.output_dir / "season-ingestion-coverage.csv", COVERAGE_FIELDS, coverage)
    write_csv(args.output_dir / "ingestion-batches.csv", BATCH_FIELDS, batches)
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "planned_seasons": summary["planned_provider_season_count"],
        "preflighted_seasons": summary["seasons_with_complete_endpoint_preflight"],
        "blocked_seasons": summary["seasons_blocked_or_not_preflighted"],
        "planned_requests": summary["planned_request_count"],
        "planned_batches": summary["planned_batches"],
        "api_requests_made": 0,
        "raw_payloads_written": False,
        "production_eligible": False,
        "betting_eligible": False,
    }, indent=2))


if __name__ == "__main__":
    main()
