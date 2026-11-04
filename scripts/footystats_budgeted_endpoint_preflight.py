#!/usr/bin/env python3
"""Budgeted, research-only FootyStats endpoint preflight.

The runner keeps provider payloads in memory only. It writes a sanitized coverage
report and the request timestamp ledger; it never persists match/team payloads.
Only the single central GitHub Actions workflow is allowed to invoke this runner.
"""
from __future__ import annotations

import argparse
import csv
import fcntl
import hashlib
import json
import os
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from footystats_request_budget import (  # noqa: E402
    DEFAULT_GLOBAL_LIMIT,
    DEFAULT_HEADROOM,
    active_usage,
    empty_ledger,
    finalize_reservation,
    reserve_block,
    validate_ledger,
    utc_text,
)
from validate_footystats_endpoint_contracts import (  # noqa: E402
    validate_paged_response,
    validate_single_response,
)

BASE_URL = "https://api.football-data-api.com"
PACE_SECONDS = 1.1
MAX_OPERATIONAL_REQUESTS = DEFAULT_GLOBAL_LIMIT - DEFAULT_HEADROOM
MATCH_ID_FIELDS = ("id", "homeID", "awayID", "date_unix", "status")
MATCH_RESULT_FIELDS = ("homeGoalCount", "awayGoalCount", "totalGoalCount")
TEAM_ID_FIELDS = ("id", "name")
TABLE_FIELDS = (
    "league_table",
    "all_matches_table_overall",
    "all_matches_table_home",
    "all_matches_table_away",
    "specific_tables",
)
XG_FIELDS = (
    "team_a_xg_prematch",
    "team_b_xg_prematch",
    "total_xg_prematch",
)


class PreflightError(RuntimeError):
    def __init__(self, code: str, attempt_timestamp: str | None = None):
        super().__init__(code)
        self.code = code
        self.attempt_timestamp = attempt_timestamp


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temp, path)


@contextmanager
def ledger_lock(path: Path):
    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def read_ledger(path: Path) -> dict[str, Any]:
    if not path.exists():
        return empty_ledger()
    value = json.loads(path.read_text(encoding="utf-8"))
    validate_ledger(value)
    return value


def write_ledger(path: Path, ledger: dict[str, Any]) -> None:
    validate_ledger(ledger)
    atomic_write_json(path, ledger)


def load_plan(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise ValueError("historical season plan file is missing")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {
            "provider",
            "provider_league_name",
            "provider_season_label",
            "provider_season_id",
            "catalogue_scope",
            "fixture_filter_start_utc",
            "fixture_filter_end_utc_inclusive",
            "production_eligible",
            "betting_eligible",
        }
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError("historical season plan is missing required columns")
        rows = list(reader)
    if not rows:
        raise ValueError("historical season plan contains no rows")

    seen: set[str] = set()
    for row in rows:
        if row.get("provider") != "FootyStats":
            raise ValueError("historical season plan contains a non-FootyStats row")
        sid = str(row.get("provider_season_id") or "").strip()
        league = str(row.get("provider_league_name") or "").strip()
        if not sid or not league:
            raise ValueError("historical season plan contains a missing provider season ID or league")
        if sid in seen:
            raise ValueError(f"duplicate provider season ID in historical plan: {sid}")
        seen.add(sid)
        if row.get("catalogue_scope") not in {"chosen_leagues_only", "all_available"}:
            raise ValueError("historical season plan has unsupported catalogue scope")
        if str(row.get("production_eligible", "")).lower() not in {"false", "0"}:
            raise ValueError("historical season plan must remain production-ineligible")
        if str(row.get("betting_eligible", "")).lower() not in {"false", "0"}:
            raise ValueError("historical season plan must remain betting-ineligible")
        if not row.get("fixture_filter_start_utc") or not row.get("fixture_filter_end_utc_inclusive"):
            raise ValueError("historical season plan lacks explicit UTC fixture filters")
    return rows


def completed_season_ids(report_dir: Path) -> set[str]:
    completed: set[str] = set()
    if not report_dir.exists():
        return completed
    terminal = {
        "ENDPOINT_PREFLIGHT_COMPLETE",
        "ENDPOINT_PREFLIGHT_COMPLETE_WITH_DATA_GAPS",
        "ENDPOINT_PREFLIGHT_COMPLETE_H2H_NOT_SAMPLEABLE",
    }
    for path in report_dir.glob("footystats-preflight-run-*.json"):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for row in report.get("season_results", []):
            if row.get("season_status") in terminal:
                completed.add(str(row.get("provider_season_id", "")))
    return {value for value in completed if value}


def round_robin_pending(rows: list[dict[str, str]], completed: set[str], limit: int) -> list[dict[str, str]]:
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if row["provider_season_id"] in completed:
            continue
        groups.setdefault(row["provider_league_name"], []).append(row)
    for group in groups.values():
        group.sort(key=lambda r: (
            int(r.get("season_start_year") or 0),
            int(r.get("season_end_year") or 0),
            r["provider_season_id"],
        ))
    ordered: list[dict[str, str]] = []
    league_names = sorted(groups)
    depth = 0
    while len(ordered) < limit:
        added = False
        for league in league_names:
            if depth < len(groups[league]):
                ordered.append(groups[league][depth])
                added = True
                if len(ordered) >= limit:
                    break
        if not added:
            break
        depth += 1
    return ordered


def reserve(args: argparse.Namespace) -> dict[str, Any]:
    if args.max_requests < 1 or args.max_requests > MAX_OPERATIONAL_REQUESTS:
        raise ValueError(f"max_requests must be between 1 and {MAX_OPERATIONAL_REQUESTS}")
    path = Path(args.ledger)
    with ledger_lock(path):
        ledger = read_ledger(path)
        ledger, reserved = reserve_block(
            ledger,
            now_utc(),
            args.max_requests,
            args.reservation_id,
            global_limit=DEFAULT_GLOBAL_LIMIT,
            reserved_headroom=DEFAULT_HEADROOM,
        )
        write_ledger(path, ledger)
    return {
        "reservation_id": args.reservation_id,
        "requested_max_requests": args.max_requests,
        "reserved_requests": reserved,
        "global_rolling_hour_limit": DEFAULT_GLOBAL_LIMIT,
        "operational_ceiling": MAX_OPERATIONAL_REQUESTS,
        "reserved_headroom": DEFAULT_HEADROOM,
        "provider_calls_made": 0,
    }


def parse_optional_int(payload: dict[str, Any], key: str, minimum: int = 0) -> int | None:
    raw = payload.get(key)
    if raw in (None, ""):
        return None
    if isinstance(raw, bool):
        raise ValueError(f"provider {key} must be an integer")
    try:
        value = int(raw)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"provider {key} must be an integer") from exc
    if str(raw).strip() not in {str(value), f"{value}.0"} or value < minimum:
        raise ValueError(f"provider {key} is outside its valid integer range")
    return value


def fetch_json(
    endpoint: str,
    params: dict[str, Any],
    api_key: str,
    attempts: list[str],
    base_url: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if attempts:
        time.sleep(PACE_SECONDS)
    timestamp = utc_text(now_utc())
    attempts.append(timestamp)
    query = dict(params)
    query["key"] = api_key
    url = f"{base_url.rstrip('/')}/{endpoint}?{urlencode(query)}"
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "Project-Oracle-Research/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            status = int(getattr(response, "status", 200))
            body = response.read()
    except HTTPError as exc:
        raise PreflightError(f"HTTP_{exc.code}", timestamp) from None
    except URLError:
        raise PreflightError("TRANSPORT_ERROR", timestamp) from None
    except TimeoutError:
        raise PreflightError("TRANSPORT_TIMEOUT", timestamp) from None
    except OSError:
        raise PreflightError("TRANSPORT_ERROR", timestamp) from None

    if status != 200:
        raise PreflightError(f"HTTP_{status}", timestamp)
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise PreflightError("MALFORMED_JSON", timestamp) from None
    if not isinstance(payload, dict):
        raise PreflightError("MALFORMED_TOP_LEVEL", timestamp)
    if payload.get("success") is not True:
        raise PreflightError("PROVIDER_SUCCESS_FALSE", timestamp)

    try:
        request_limit = parse_optional_int(payload, "request_limit", 1)
        request_remaining = parse_optional_int(payload, "request_remaining", 0)
    except ValueError:
        raise PreflightError("MALFORMED_PROVIDER_LIMIT_METADATA", timestamp) from None

    return payload, {
        "endpoint": endpoint,
        "http_status": status,
        "fetched_at_utc": timestamp,
        "payload_sha256": hashlib.sha256(body).hexdigest(),
        "provider_request_limit_observed": request_limit,
        "provider_request_remaining_observed": request_remaining,
        "request_remaining_interpretation": "REQUEST_WINDOW_OBSERVATION_ONLY_NOT_MONTHLY_CREDIT_EVIDENCE",
    }



def check_provider_limit(meta: dict[str, Any], ledger_path: Path) -> None:
    """A lower provider request_limit returned mid-run immediately binds."""
    observed = meta.get("provider_request_limit_observed")
    if observed is None:
        return
    effective = min(DEFAULT_GLOBAL_LIMIT, int(observed))
    headroom = min(DEFAULT_HEADROOM, max(0, effective - 1))
    usage = active_usage(read_ledger(ledger_path), now_utc())["active_total"]
    if usage + headroom > effective:
        raise PreflightError("PROVIDER_REQUEST_LIMIT_BELOW_ACTIVE_RESERVATION")


def add_history_window_summary(summary: dict[str, Any], rows: list[dict[str, Any]], season: dict[str, str]) -> None:
    try:
        start = datetime.fromisoformat(season["fixture_filter_start_utc"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(season["fixture_filter_end_utc_inclusive"].replace("Z", "+00:00"))
        if start.tzinfo is None or end.tzinfo is None or start > end:
            raise ValueError
        start_unix = int(start.timestamp())
        end_unix = int(end.timestamp())
    except (KeyError, ValueError, TypeError):
        raise PreflightError("INVALID_EXPLICIT_FIXTURE_DATE_FILTER") from None
    in_window = 0
    out_of_window = 0
    for row in rows:
        kickoff = int(row["date_unix"])
        if start_unix <= kickoff <= end_unix:
            in_window += 1
        else:
            out_of_window += 1
    summary["requested_history_window_utc"] = {
        "start_inclusive": season["fixture_filter_start_utc"],
        "end_inclusive": season["fixture_filter_end_utc_inclusive"],
    }
    summary["page_1_rows_in_window"] = in_window
    summary["page_1_rows_outside_window"] = out_of_window
    summary["fixture_date_filter_applied_to_future_ingestion"] = True

def validate_match_page(payload: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    try:
        pager = validate_paged_response("league-matches", payload, 1)
    except ValueError:
        raise PreflightError("MATCH_PAGINATION_CONTRACT_FAILURE") from None
    rows = payload["data"]
    missing_identity = {
        field: sum(1 for row in rows if not isinstance(row, dict) or row.get(field) in (None, ""))
        for field in MATCH_ID_FIELDS
    }
    invalid_identity = 0
    seen: set[str] = set()
    duplicate_ids = 0
    complete_rows = 0
    complete_goal_gaps = 0
    goal_presence = {field: 0 for field in MATCH_RESULT_FIELDS}
    no_home_away_count = 0
    kickoff_values: list[int] = []
    for row in rows:
        if not isinstance(row, dict):
            invalid_identity += 1
            continue
        try:
            match_id = int(row.get("id"))
            home_id = int(row.get("homeID"))
            away_id = int(row.get("awayID"))
            kickoff = int(row.get("date_unix"))
            if min(match_id, home_id, away_id, kickoff) < 1 or not str(row.get("status") or "").strip():
                raise ValueError
        except (TypeError, ValueError, OverflowError):
            invalid_identity += 1
            continue
        if str(match_id) in seen:
            duplicate_ids += 1
        seen.add(str(match_id))
        kickoff_values.append(kickoff)
        if str(row.get("no_home_away", "")).strip() in {"1", "true", "True"}:
            no_home_away_count += 1
        if str(row.get("status", "")).lower() == "complete":
            complete_rows += 1
            for field in MATCH_RESULT_FIELDS:
                if row.get(field) not in (None, ""):
                    goal_presence[field] += 1
            if any(row.get(field) in (None, "") for field in MATCH_RESULT_FIELDS):
                complete_goal_gaps += 1

    if any(missing_identity.values()) or invalid_identity or duplicate_ids:
        raise PreflightError("MATCH_IDENTITY_FIELD_GAP_OR_DUPLICATE")
    summary = {
        **pager,
        "fetched_pages": 1,
        "all_pages_retrieved": pager["expected_page_count"] == 1,
        "match_identity_fields": {field: len(rows) for field in MATCH_ID_FIELDS},
        "unique_match_ids_on_page": len(seen),
        "completed_match_rows": complete_rows,
        "completed_rows_missing_any_goal_field": complete_goal_gaps,
        "completed_goal_field_presence": goal_presence,
        "no_home_away_rows": no_home_away_count,
        "kickoff_unix_min": min(kickoff_values) if kickoff_values else None,
        "kickoff_unix_max": max(kickoff_values) if kickoff_values else None,
    }
    return summary, rows


def validate_team_page(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        pager = validate_paged_response("league-teams", payload, 1)
    except ValueError:
        raise PreflightError("TEAM_PAGINATION_CONTRACT_FAILURE") from None
    rows = payload["data"]
    missing = {
        field: sum(1 for row in rows if not isinstance(row, dict) or row.get(field) in (None, ""))
        for field in TEAM_ID_FIELDS
    }
    ids: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            raise PreflightError("TEAM_IDENTITY_FIELD_GAP")
        try:
            team_id = int(row.get("id"))
            if team_id < 1 or not str(row.get("name") or "").strip():
                raise ValueError
        except (TypeError, ValueError, OverflowError):
            raise PreflightError("TEAM_IDENTITY_FIELD_GAP") from None
        ids.append(str(team_id))
    if any(missing.values()) or len(ids) != len(set(ids)):
        raise PreflightError("TEAM_IDENTITY_FIELD_GAP_OR_DUPLICATE")
    return {
        **pager,
        "fetched_pages": 1,
        "all_pages_retrieved": pager["expected_page_count"] == 1,
        "team_identity_fields": {field: len(rows) for field in TEAM_ID_FIELDS},
        "unique_team_ids_on_page": len(set(ids)),
        "team_stats_field_names": sorted({
            key for row in rows if isinstance(row.get("stats"), dict) for key in row["stats"]
        }),
    }


def summarize_single(endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        shape = validate_single_response(endpoint, payload)
    except ValueError:
        raise PreflightError(f"{endpoint.upper().replace('-', '_')}_RESPONSE_SHAPE_FAILURE") from None
    data = payload["data"]
    if isinstance(data, dict):
        fields = sorted(data.keys())
        arrays = {
            key: len(value) for key, value in data.items()
            if isinstance(value, list)
        }
        return {**shape, "data_field_names": fields, "array_row_counts": arrays}
    if isinstance(data, list):
        field_names = sorted(data[0].keys()) if data and isinstance(data[0], dict) else []
        return {
            **shape,
            "data_row_count": len(data),
            "first_row_field_names": field_names,
        }
    raise PreflightError(f"{endpoint.upper().replace('-', '_')}_RESPONSE_SHAPE_FAILURE")


def match_detail_summary(payload: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    try:
        shape = validate_single_response("match", payload)
    except ValueError:
        raise PreflightError("MATCH_DETAIL_RESPONSE_SHAPE_FAILURE") from None
    data = payload["data"]
    identity = {
        "id": str(data.get("id", "")),
        "homeID": str(data.get("homeID", "")),
        "awayID": str(data.get("awayID", "")),
    }
    expected_identity = {
        "id": str(expected.get("id", "")),
        "homeID": str(expected.get("homeID", "")),
        "awayID": str(expected.get("awayID", "")),
    }
    if identity != expected_identity:
        raise PreflightError("MATCH_DETAIL_ORDERED_IDENTITY_MISMATCH")
    return {
        **shape,
        "exact_ordered_fixture_identity_verified": True,
        "h2h_field_present": "h2h" in data,
        "h2h_field_shape": type(data.get("h2h")).__name__ if "h2h" in data else "MISSING",
        "xg_field_presence": {field: field in data and data.get(field) not in (None, "") for field in XG_FIELDS},
        "xg_usage_status": "QUARANTINED_NO_FIXTURE_LEVEL_CAPTURE_AND_REVISION_PROVENANCE",
        "h2h_temporal_status": "PRESENT_NOT_CHRONOLOGY_VALIDATED" if "h2h" in data else "H2H_FIELD_MISSING",
    }


def execute(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    ledger_path = Path(args.ledger)
    report_path = Path(args.report)
    report_dir = report_path.parent
    attempts: list[str] = []
    season_results: list[dict[str, Any]] = []
    failure_code: str | None = None
    provider_limit_seen: int | None = None
    reservation_count = 0
    rest_reservation_id = args.reservation_id + "-rest"
    rest_reservation_created = False
    first_reservation_finalized = False
    first_match_payload: dict[str, Any] | None = None
    first_match_meta: dict[str, Any] | None = None
    first_match_summary: dict[str, Any] | None = None
    request_meta_observations: list[dict[str, Any]] = []
    pending: list[dict[str, str]] = []
    report: dict[str, Any] = {
        "schema_version": "1.0",
        "diagnostic": "FOOTYSTATS_BUDGETED_ENDPOINT_PREFLIGHT",
        "run_id": args.run_id,
        "started_at_utc": utc_text(now_utc()),
        "history_start_date": "2024-01-01",
        "history_end_date_inclusive": args.history_end_date,
        "catalogue_scope": "selected_catalogue_provider_registry",
        "provider": "FootyStats",
        "request_budget": {
            "global_limit_per_rolling_hour": DEFAULT_GLOBAL_LIMIT,
            "reserved_headroom": DEFAULT_HEADROOM,
            "operational_ceiling": MAX_OPERATIONAL_REQUESTS,
            "max_requests_requested": args.max_requests,
            "provider_request_limit_observed": None,
            "provider_request_remaining_observed": None,
            "request_remaining_is_monthly_credit_evidence": False,
        },
        "raw_payloads_persisted": False,
        "production_eligible": False,
        "betting_eligible": False,
        "xg_usage_status": "QUARANTINED_NO_FIXTURE_LEVEL_CAPTURE_AND_REVISION_PROVENANCE",
        "fixture_time_standings_verified": False,
        "recent_form_verified": False,
        "home_away_form_verified": False,
        "h2h_temporal_order_verified": False,
        "full_pagination_completed": False,
        "season_results": [],
    }

    try:
        api_key = os.environ.get(args.api_key_env, "").strip()
        with ledger_lock(ledger_path):
            ledger = read_ledger(ledger_path)
            matches = [
                item for item in ledger["reservations"]
                if item["reservation_id"] == args.reservation_id
            ]
            if len(matches) != 1:
                raise PreflightError("ACTIVE_INITIAL_RESERVATION_NOT_FOUND")
            reservation_count = int(matches[0]["reserved_count"])
            if reservation_count > args.max_requests:
                raise PreflightError("RESERVATION_EXCEEDS_REQUESTED_MAXIMUM")
            report["request_budget"]["reserved_requests_this_run"] = reservation_count

        if not api_key:
            raise PreflightError("FOOTYSTATS_API_KEY_SECRET_MISSING")

        plan_rows = load_plan(Path(args.plan))
        completed = completed_season_ids(report_dir)
        pending = round_robin_pending(plan_rows, completed, args.max_seasons)
        report["catalogue"] = {
            "planned_season_rows": len(plan_rows),
            "unique_provider_leagues": len({row["provider_league_name"] for row in plan_rows}),
            "previously_preflighted_seasons": len(completed),
            "pending_seasons_before_this_run": len(pending),
        }
        if not pending:
            report["run_status"] = "NO_PENDING_SEASONS"
        else:
            first = pending[0]
            first_match_payload, first_match_meta = fetch_json(
                "league-matches",
                {"season_id": first["provider_season_id"], "page": 1, "max_per_page": 1000},
                api_key,
                attempts,
                args.base_url,
            )
            with ledger_lock(ledger_path):
                ledger = read_ledger(ledger_path)
                ledger = finalize_reservation(
                    ledger, args.reservation_id, attempts[:1], now_utc()
                )
                write_ledger(ledger_path, ledger)
            first_reservation_finalized = True

            first_match_summary, first_rows = validate_match_page(first_match_payload)
            add_history_window_summary(first_match_summary, first_rows, first)
            request_meta_observations.append(first_match_meta)
            provider_limit_seen = first_match_meta["provider_request_limit_observed"]
            report["request_budget"]["provider_request_limit_observed"] = provider_limit_seen
            report["request_budget"]["provider_request_remaining_observed"] = first_match_meta[
                "provider_request_remaining_observed"
            ]

            desired_rest = min(
                max(0, reservation_count - 1),
                max(0, 5 * len(pending) - 1),
            )
            rest_reserved = 0
            if desired_rest:
                with ledger_lock(ledger_path):
                    ledger = read_ledger(ledger_path)
                    try:
                        ledger, rest_reserved = reserve_block(
                            ledger,
                            now_utc(),
                            desired_rest,
                            rest_reservation_id,
                            request_limit=provider_limit_seen,
                            global_limit=DEFAULT_GLOBAL_LIMIT,
                            reserved_headroom=DEFAULT_HEADROOM,
                        )
                        write_ledger(ledger_path, ledger)
                        rest_reservation_created = True
                    except ValueError as exc:
                        if "budget exhausted or reserved" not in str(exc):
                            raise
                        write_ledger(ledger_path, ledger)

            effective_season_count = min(len(pending), (rest_reserved + 1) // 5)
            if effective_season_count < 1:
                first_result = {
                    "provider_league_name": first["provider_league_name"],
                    "provider_season_label": first["provider_season_label"],
                    "provider_season_id": first["provider_season_id"],
                    "season_status": "PARTIAL_PROVIDER_BUDGET_AFTER_MATCHES_PAGE_1",
                    "league_matches": first_match_summary,
                    "league_matches_response": first_match_meta,
                    "team_endpoint_status": "NOT_REQUESTED",
                    "tables_endpoint_status": "NOT_REQUESTED",
                    "league_season_endpoint_status": "NOT_REQUESTED",
                    "h2h_endpoint_status": "NOT_REQUESTED",
                }
                season_results.append(first_result)
                report["run_status"] = "PARTIAL_PROVIDER_BUDGET"
            else:
                seasons_to_process = pending[:effective_season_count]
                for index, season in enumerate(seasons_to_process):
                    result: dict[str, Any] = {
                        "provider_league_name": season["provider_league_name"],
                        "provider_season_label": season["provider_season_label"],
                        "provider_season_id": season["provider_season_id"],
                    }
                    if index == 0:
                        match_payload = first_match_payload
                        match_meta = first_match_meta
                        match_summary = first_match_summary
                        match_rows = first_rows
                    else:
                        match_payload, match_meta = fetch_json(
                            "league-matches",
                            {"season_id": season["provider_season_id"], "page": 1, "max_per_page": 1000},
                            api_key,
                            attempts,
                            args.base_url,
                        )
                        match_summary, match_rows = validate_match_page(match_payload)
                        check_provider_limit(match_meta, ledger_path)
                        request_meta_observations.append(match_meta)
                        add_history_window_summary(match_summary, match_rows, season)
                    result["league_matches"] = match_summary
                    result["league_matches_response"] = match_meta
                    result["completed_goal_field_gap_rows"] = match_summary["completed_rows_missing_any_goal_field"]

                    as_of_unix = int(now_utc().timestamp())
                    teams_payload, teams_meta = fetch_json(
                        "league-teams",
                        {"season_id": season["provider_season_id"], "page": 1, "include": "stats", "max_time": as_of_unix},
                        api_key,
                        attempts,
                        args.base_url,
                    )
                    check_provider_limit(teams_meta, ledger_path)
                    request_meta_observations.append(teams_meta)
                    result["league_teams"] = validate_team_page(teams_payload)
                    result["league_teams_response"] = teams_meta

                    tables_payload, tables_meta = fetch_json(
                        "league-tables",
                        {"season_id": season["provider_season_id"], "max_time": as_of_unix},
                        api_key,
                        attempts,
                        args.base_url,
                    )
                    check_provider_limit(tables_meta, ledger_path)
                    request_meta_observations.append(tables_meta)
                    result["league_tables"] = summarize_single("league-tables", tables_payload)
                    result["league_tables_response"] = tables_meta
                    table_data = tables_payload["data"]
                    result["table_field_presence"] = {
                        field: field in table_data for field in TABLE_FIELDS
                    }
                    result["standings_temporal_status"] = "CURRENT_AS_OF_PREFLIGHT_ONLY_NOT_FIXTURE_TIME"

                    season_payload, season_meta = fetch_json(
                        "league-season",
                        {"season_id": season["provider_season_id"], "max_time": as_of_unix},
                        api_key,
                        attempts,
                        args.base_url,
                    )
                    check_provider_limit(season_meta, ledger_path)
                    request_meta_observations.append(season_meta)
                    result["league_season"] = summarize_single("league-season", season_payload)
                    result["league_season_response"] = season_meta

                    sample_match = next(
                        (row for row in match_rows if isinstance(row, dict) and row.get("id") not in (None, "")),
                        None,
                    )
                    if sample_match is None:
                        result["h2h_endpoint_status"] = "NOT_SAMPLEABLE_NO_MATCH_ON_PAGE_1"
                        result["h2h_temporal_status"] = "NOT_VERIFIED"
                        result["xg_field_presence"] = {field: False for field in XG_FIELDS}
                        season_status = "ENDPOINT_PREFLIGHT_COMPLETE_H2H_NOT_SAMPLEABLE"
                    else:
                        detail_payload, detail_meta = fetch_json(
                            "match",
                            {"match_id": sample_match["id"]},
                            api_key,
                            attempts,
                            args.base_url,
                        )
                        check_provider_limit(detail_meta, ledger_path)
                        request_meta_observations.append(detail_meta)
                        result["match_detail"] = match_detail_summary(detail_payload, sample_match)
                        result["match_detail_response"] = detail_meta
                        result["h2h_endpoint_status"] = "RESPONSE_VERIFIED"
                        result["h2h_temporal_status"] = result["match_detail"]["h2h_temporal_status"]
                        result["xg_field_presence"] = result["match_detail"]["xg_field_presence"]
                        season_status = "ENDPOINT_PREFLIGHT_COMPLETE"

                    data_gaps = (
                        result["completed_goal_field_gap_rows"] > 0
                        or result["h2h_endpoint_status"] == "NOT_SAMPLEABLE_NO_MATCH_ON_PAGE_1"
                        or (result.get("match_detail") and not result["match_detail"]["h2h_field_present"])
                    )
                    if data_gaps and season_status == "ENDPOINT_PREFLIGHT_COMPLETE":
                        season_status = "ENDPOINT_PREFLIGHT_COMPLETE_WITH_DATA_GAPS"
                    result["recent_form_status"] = "NOT_ASSESSED_FULL_MATCH_PAGINATION_REQUIRED"
                    result["home_away_form_status"] = "NOT_ASSESSED_FULL_MATCH_PAGINATION_REQUIRED"
                    result["xg_usage_status"] = "QUARANTINED_NO_FIXTURE_LEVEL_CAPTURE_AND_REVISION_PROVENANCE"
                    result["season_status"] = season_status
                    season_results.append(result)

                if effective_season_count < len(pending):
                    report["run_status"] = "PARTIAL_PROVIDER_OR_REQUEST_BUDGET"
                else:
                    report["run_status"] = "ENDPOINT_PREFLIGHT_BATCH_COMPLETE"

    except PreflightError as exc:
        failure_code = exc.code
        report["run_status"] = "STOPPED_FAIL_CLOSED"
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        failure_code = "LOCAL_PLAN_OR_LEDGER_VALIDATION_FAILURE"
        report["run_status"] = "STOPPED_FAIL_CLOSED"
        report["local_error_type"] = type(exc).__name__
    finally:
        with ledger_lock(ledger_path):
            ledger = read_ledger(ledger_path)
            initial_active = any(
                item["reservation_id"] == args.reservation_id for item in ledger["reservations"]
            )
            rest_active = any(
                item["reservation_id"] == rest_reservation_id for item in ledger["reservations"]
            )
            if initial_active:
                ledger = finalize_reservation(
                    ledger,
                    args.reservation_id,
                    attempts[:1],
                    now_utc(),
                )
            if rest_active:
                ledger = finalize_reservation(
                    ledger,
                    rest_reservation_id,
                    attempts[1:],
                    now_utc(),
                )
            write_ledger(ledger_path, ledger)

        report["finished_at_utc"] = utc_text(now_utc())
        report["request_budget"]["requests_attempted_this_run"] = len(attempts)
        observed_limits = [item["provider_request_limit_observed"] for item in request_meta_observations if item.get("provider_request_limit_observed") is not None]
        observed_remaining = [item["provider_request_remaining_observed"] for item in request_meta_observations if item.get("provider_request_remaining_observed") is not None]
        report["request_budget"]["provider_request_limit_observed_min"] = min(observed_limits) if observed_limits else None
        report["request_budget"]["provider_request_remaining_observed_min"] = min(observed_remaining) if observed_remaining else None
        report["request_budget"]["actual_requests_in_rolling_hour_after_run"] = active_usage(
            read_ledger(ledger_path), now_utc()
        )["actual_requests_in_rolling_hour"]
        report["season_results"] = season_results
        report["seasons_completed_this_run"] = sum(
            1 for row in season_results
            if str(row.get("season_status", "")).startswith("ENDPOINT_PREFLIGHT_COMPLETE")
        )
        report["seasons_not_completed_this_run"] = max(
            0, len(pending) - report["seasons_completed_this_run"]
        )
        report["failure_code"] = failure_code
        report["pagination_note"] = (
            "Only page 1 was preflighted for paged endpoints. expected_page_count and "
            "all_pages_retrieved are recorded; full pagination is not claimed."
        )
        report["h2h_note"] = (
            "The match endpoint's H2H field is presence-checked only; previous-match chronology "
            "and exact historical H2H reconstruction remain separate validation work."
        )
        report["xg_note"] = (
            "Pre-match-labelled xG field presence does not establish point-in-time capture or "
            "revision provenance. All xG remains quarantined."
        )
        report["request_remaining_note"] = (
            "request_remaining is recorded only as a provider request-window observation; "
            "it is never interpreted as monthly credit balance."
        )
        report["season_results"] = season_results
        atomic_write_json(report_path, report)

    exit_code = 1 if failure_code else 0
    return report, exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    reserve_parser = sub.add_parser("reserve")
    reserve_parser.add_argument("--ledger", required=True)
    reserve_parser.add_argument("--reservation-id", required=True)
    reserve_parser.add_argument("--max-requests", required=True, type=int)

    execute_parser = sub.add_parser("execute")
    execute_parser.add_argument("--ledger", required=True)
    execute_parser.add_argument("--reservation-id", required=True)
    execute_parser.add_argument("--plan", required=True)
    execute_parser.add_argument("--report", required=True)
    execute_parser.add_argument("--run-id", required=True)
    execute_parser.add_argument("--max-seasons", required=True, type=int)
    execute_parser.add_argument("--max-requests", required=True, type=int)
    execute_parser.add_argument("--history-end-date", required=True)
    execute_parser.add_argument("--api-key-env", default="FOOTYSTATS_API_KEY")
    execute_parser.add_argument("--base-url", default=BASE_URL)

    args = parser.parse_args()
    try:
        if args.command == "reserve":
            result = reserve(args)
            print(json.dumps(result, indent=2))
            return 0
        if args.max_seasons < 1 or args.max_requests < 1 or args.max_requests > MAX_OPERATIONAL_REQUESTS:
            raise ValueError("max_seasons/max_requests is outside the approved operational bounds")
        report, code = execute(args)
        print(json.dumps({
            "run_status": report.get("run_status"),
            "failure_code": report.get("failure_code"),
            "requests_attempted": report.get("request_budget", {}).get("requests_attempted_this_run", 0),
            "seasons_completed": report.get("seasons_completed_this_run", 0),
            "report_path": args.report,
            "raw_payloads_persisted": False,
        }, indent=2))
        return code
    except Exception as exc:
        print(json.dumps({"status": "FAILED_CLOSED", "error_type": type(exc).__name__}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
