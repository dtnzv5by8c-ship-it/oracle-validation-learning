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
    "page_1_match_rows_returned", "page_1_match_rows_in_history_window",
    "page_1_match_rows_outside_history_window", "page_1_completed_match_rows",
    "page_1_completed_match_goal_field_gaps", "page_1_no_home_away_rows",
    "match_ids_unique", "team_ids_unique", "table_required_fields_complete",
    "season_goal_fields_complete", "team_xg_aggregate_fields_complete",
    "h2h_field_present", "h2h_temporal_status", "recent_form_status",
    "home_away_form_status", "standings_temporal_status", "xg_usage_status",
    "required_field_gap_reasons", "planned_ingestion_requests",
    "ingestion_plan_status", "production_eligible", "betting_eligible",
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
    if item.get("fetched_pages") != 1 or item.get("page_complete") is not True:
        raise ValueError(f"{key} page-1 preflight evidence is incomplete")
    returned = item.get("returned_rows")
    if isinstance(returned, bool):
        raise ValueError(f"{key} returned_rows is invalid")
    try:
        returned_i = int(returned)
    except (TypeError, ValueError, OverflowError):
        raise ValueError(f"{key} returned_rows is invalid") from None
    if returned_i < 0 or returned_i > per_page_i or returned_i > total_i:
        raise ValueError(f"{key} returned_rows conflicts with total/per_page")
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
            "page_1_match_rows_returned": 0,
            "page_1_match_rows_in_history_window": 0,
            "page_1_match_rows_outside_history_window": 0,
            "page_1_completed_match_rows": 0,
            "page_1_completed_match_goal_field_gaps": 0,
            "page_1_no_home_away_rows": 0,
            "match_ids_unique": False,
            "team_ids_unique": False,
            "table_required_fields_complete": False,
            "season_goal_fields_complete": False,
            "team_xg_aggregate_fields_complete": False,
            "h2h_field_present": False,
            "h2h_temporal_status": "NOT_VERIFIED",
            "recent_form_status": "NOT_ASSESSED",
            "home_away_form_status": "NOT_ASSESSED",
            "standings_temporal_status": "NOT_VERIFIED",
            "xg_usage_status": "QUARANTINED",
            "required_field_gap_reasons": "",
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
            match_page = preflight["league_matches"]
            team_page = preflight["league_teams"]
            match_rows = int(match_page["returned_rows"])
            team_rows = int(team_page["returned_rows"])
            required_match_identity = {"id", "homeID", "awayID", "date_unix", "status"}
            match_identity = match_page.get("match_identity_fields", {})
            if not required_match_identity.issubset(match_identity) or any(
                int(match_identity.get(field, -1)) != match_rows for field in required_match_identity
            ):
                raise ValueError("match identity fields are incomplete")
            if int(match_page.get("unique_match_ids_on_page", -1)) != match_rows:
                raise ValueError("match IDs are not unique on the preflight page")
            required_team_identity = {"id", "name_or_alias"}
            team_identity = team_page.get("team_identity_fields", {})
            if not required_team_identity.issubset(team_identity) or any(
                int(team_identity.get(field, -1)) != team_rows for field in required_team_identity
            ):
                raise ValueError("team identity fields are incomplete")
            if int(team_page.get("unique_team_ids_on_page", -1)) != team_rows:
                raise ValueError("team IDs are not unique on the preflight page")
            no_home_away_rows = int(match_page.get("no_home_away_rows", -1))
            completed_rows = int(match_page.get("completed_match_rows", -1))
            goal_gaps = int(match_page.get("completed_rows_missing_any_goal_field", -1))
            in_window = int(match_page.get("page_1_rows_in_window", -1))
            out_window = int(match_page.get("page_1_rows_outside_window", -1))
            if not (0 <= no_home_away_rows <= match_rows and 0 <= completed_rows <= match_rows
                    and 0 <= goal_gaps <= completed_rows and in_window >= 0
                    and out_window >= 0 and in_window + out_window == match_rows):
                raise ValueError("match field/temporal coverage counts are invalid")
            goal_presence = match_page.get("completed_goal_field_presence", {})
            required_goal_fields = {"homeGoalCount", "awayGoalCount", "totalGoalCount"}
            goal_fields_complete = required_goal_fields.issubset(goal_presence) and all(
                int(goal_presence.get(field, -1)) == completed_rows for field in required_goal_fields
            ) and goal_gaps == 0
            table_presence = preflight.get("table_field_presence", {})
            required_table_fields = {
                "all_matches_table_away", "all_matches_table_home",
                "all_matches_table_overall", "league_table", "specific_tables",
            }
            table_fields_complete = required_table_fields.issubset(table_presence) and all(
                table_presence.get(field) is True for field in required_table_fields
            )
            season_fields = set(preflight.get("league_season", {}).get("data_field_names", []))
            required_season_fields = {"total_goals", "home_teams_goals", "away_teams_goals", "xg_avg"}
            season_goal_fields_complete = required_season_fields.issubset(season_fields)
            team_stats_fields = set(team_page.get("team_stats_field_names", []))
            required_team_xg_fields = {
                "xg_for_avg_home", "xg_for_avg_away",
                "xg_against_avg_home", "xg_against_avg_away",
            }
            team_xg_fields_complete = required_team_xg_fields.issubset(team_stats_fields)
            match_detail = preflight.get("match_detail", {})
            h2h_field_present = match_detail.get("h2h_field_present") is True
            sample_xg_fields = match_detail.get("xg_field_presence", {})
            sample_xg_fields_complete = all(
                sample_xg_fields.get(field) is True
                for field in ("team_a_xg_prematch", "team_b_xg_prematch", "total_xg_prematch")
            )
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
            "page_1_match_rows_returned": match_rows,
            "page_1_match_rows_in_history_window": in_window,
            "page_1_match_rows_outside_history_window": out_window,
            "page_1_completed_match_rows": completed_rows,
            "page_1_completed_match_goal_field_gaps": goal_gaps,
            "page_1_no_home_away_rows": no_home_away_rows,
            "match_ids_unique": True,
            "team_ids_unique": True,
            "table_required_fields_complete": table_fields_complete,
            "season_goal_fields_complete": season_goal_fields_complete,
            "team_xg_aggregate_fields_complete": team_xg_fields_complete,
            "h2h_field_present": h2h_field_present,
            "h2h_temporal_status": preflight.get("h2h_temporal_status", "NOT_VERIFIED"),
            "recent_form_status": preflight.get("recent_form_status", "NOT_ASSESSED"),
            "home_away_form_status": preflight.get("home_away_form_status", "NOT_ASSESSED"),
            "standings_temporal_status": preflight.get("standings_temporal_status", "NOT_VERIFIED"),
            "xg_usage_status": preflight.get("xg_usage_status", "QUARANTINED"),
        })
        field_gaps = []
        if not goal_fields_complete:
            field_gaps.append("COMPLETED_MATCH_GOAL_FIELDS")
        if not table_fields_complete:
            field_gaps.append("REQUIRED_TABLE_FIELDS")
        if not season_goal_fields_complete:
            field_gaps.append("SEASON_GOAL_OR_XG_AGGREGATE_FIELDS")
        if not team_xg_fields_complete:
            field_gaps.append("TEAM_XG_AGGREGATE_FIELDS")
        if not h2h_field_present:
            field_gaps.append("SAMPLE_H2H_FIELD")
        if not sample_xg_fields_complete:
            field_gaps.append("SAMPLE_FIXTURE_XG_FIELDS")
        base["required_field_gap_reasons"] = ";".join(field_gaps)

        season_tasks: list[dict[str, Any]] = []
        for page in range(1, match_pages + 1):
            season_tasks.append({
                "provider": "FootyStats",
                "provider_league_name": league,
                "provider_season_label": label,
                "provider_season_id": sid,
                "endpoint": "league-matches",
                "page": page,
                "max_per_page": int(match_page["per_page"]),
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
        base["ingestion_plan_status"] = (
            "PLANNED_WITH_REQUIRED_FIELD_GAPS_QUARANTINED"
            if field_gaps else "PLANNED_REQUIRES_PRIVATE_RAW_ARCHIVE"
        )
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
        "page_1_match_rows_returned": sum(int(row["page_1_match_rows_returned"] or 0) for row in coverage),
        "page_1_match_rows_in_history_window": sum(int(row["page_1_match_rows_in_history_window"] or 0) for row in coverage),
        "page_1_match_rows_outside_history_window": sum(int(row["page_1_match_rows_outside_history_window"] or 0) for row in coverage),
        "page_1_completed_match_rows": sum(int(row["page_1_completed_match_rows"] or 0) for row in coverage),
        "page_1_completed_match_goal_field_gaps": sum(int(row["page_1_completed_match_goal_field_gaps"] or 0) for row in coverage),
        "page_1_no_home_away_rows": sum(int(row["page_1_no_home_away_rows"] or 0) for row in coverage),
        "seasons_with_any_no_home_away_rows": sum(1 for row in coverage if int(row["page_1_no_home_away_rows"] or 0) > 0),
        "seasons_with_all_page_1_rows_no_home_away": sum(1 for row in coverage if int(row["page_1_match_rows_returned"] or 0) > 0 and int(row["page_1_no_home_away_rows"] or 0) == int(row["page_1_match_rows_returned"] or 0)),
        "seasons_with_required_field_gaps": sum(1 for row in coverage if row["required_field_gap_reasons"]),
        "seasons_with_h2h_field_present": sum(1 for row in coverage if row["h2h_field_present"] is True),
        "seasons_with_h2h_temporal_order_unverified": sum(1 for row in coverage if not str(row["ingestion_plan_status"]).startswith("BLOCKED") and row["h2h_temporal_status"] != "VERIFIED"),
        "seasons_with_recent_form_unverified": sum(1 for row in coverage if not str(row["ingestion_plan_status"]).startswith("BLOCKED") and row["recent_form_status"] != "VERIFIED"),
        "seasons_with_home_away_form_unverified": sum(1 for row in coverage if not str(row["ingestion_plan_status"]).startswith("BLOCKED") and row["home_away_form_status"] != "VERIFIED"),
        "seasons_with_fixture_time_standings_unverified": sum(1 for row in coverage if not str(row["ingestion_plan_status"]).startswith("BLOCKED") and row["standings_temporal_status"] != "VERIFIED"),
        "seasons_with_fixture_level_xg_quarantined": sum(1 for row in coverage if not str(row["ingestion_plan_status"]).startswith("BLOCKED") and str(row["xg_usage_status"]).startswith("QUARANTINED")),
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
