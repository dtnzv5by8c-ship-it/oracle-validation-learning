#!/usr/bin/env python3
"""Bounded research-only current fixture snapshot from FootyStats selected-50 seasons.

Makes at most one sequential league-matches request per selected season (50 total),
uses conservative pacing for the lowest plan that supports 50 leagues, stops after
the first failed provider request, never retries, persists no raw provider payload,
and writes no production ledger. Output remains provider-native.
"""
import csv
import json
import os
import re
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OUT = Path("oracle-selected50-current-fixture-snapshot")
OUT.mkdir(exist_ok=True)
MAX_REQUESTS = 50
REQUEST_INTERVAL_SECONDS = 2.1

manifest = Path("reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md")
crosswalk = Path("reports/oracle-selected50-provider-identity-reconciliation-2026-10-27.csv")
if not manifest.is_file() or not crosswalk.is_file():
    raise SystemExit("Required selected-50 manifest/crosswalk missing; zero requests made.")

selected = []
for line in manifest.read_text(encoding="utf-8").splitlines():
    match = re.match(r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", line)
    if match:
        selected.append({
            "row": int(match.group(1)),
            "selected_season_id": match.group(2).strip(),
            "country": match.group(3).strip(),
            "competition": match.group(4).strip(),
        })

if len(selected) != 50 or len({item["selected_season_id"] for item in selected}) != 50:
    raise SystemExit("Manifest guard failed: expected 50 unique selected season IDs; zero requests made.")

with crosswalk.open(encoding="utf-8", newline="") as handle:
    cross = {row["selected_manifest_id"]: row for row in csv.DictReader(handle)}

for item in selected:
    row = cross.get(item["selected_season_id"], {})
    item["provider_comp_master_id_observed"] = row.get("provider_comp_master_id_observed", "")
    item["provider_master_id_semantic_status"] = row.get(
        "provider_master_id_semantic_status", "REVIEW_REQUIRED_NOT_CANONICAL"
    )

key = os.environ.get("FOOTYSTATS_API_KEY", "").strip()
if not key:
    raise SystemExit("FOOTYSTATS_API_KEY missing; zero requests made.")

now = datetime.now(timezone.utc)
now_ts = int(now.timestamp())
past_cutoff = now_ts - int(timedelta(days=30).total_seconds())
future_cutoff = now_ts + int(timedelta(days=14).total_seconds())

fields = (
    "id", "homeID", "awayID", "home_name", "away_name", "season", "status",
    "roundID", "game_week", "homeGoalCount", "awayGoalCount", "totalGoalCount",
    "date_unix", "competition_id", "no_home_away", "home_ppg", "away_ppg",
    "pre_match_home_ppg", "pre_match_away_ppg", "btts_potential", "o25_potential",
)

results = []
all_window_matches = []
request_failures = []
pagination_gaps = []
requests_started = 0
stop_reason = None
retry_after_header = None


def not_attempted_row(item):
    """Retain the exact selected-season row without implying a provider request."""
    return {
        **item,
        "http_status": None,
        "provider_success": False,
        "returned_match_count": 0,
        "max_page": None,
        "current_page": None,
        "error_class": "NOT_ATTEMPTED_AFTER_STOP",
        "request_attempted": False,
        "retry_after_header": None,
        "rate_limit_detected": False,
        "matches_in_window": 0,
        "future_14d_count": 0,
        "recent_completed_30d_count": 0,
        "schedule_status": "NOT_ATTEMPTED_AFTER_STOP",
    }


for index, item in enumerate(selected):
    if requests_started >= MAX_REQUESTS:
        stop_reason = "MAX_REQUESTS_HARD_CAP_REACHED"
        results.extend(not_attempted_row(skipped) for skipped in selected[index:])
        break

    season_id = str(item["selected_season_id"])
    query = {"key": key, "season_id": season_id, "max_per_page": 1000}
    url = "https://api.football-data-api.com/league-matches?" + urlencode(query)
    result = {
        **item,
        "http_status": None,
        "provider_success": False,
        "returned_match_count": 0,
        "max_page": None,
        "current_page": None,
        "error_class": None,
        "request_attempted": False,
        "retry_after_header": None,
        "rate_limit_detected": False,
        "matches_in_window": 0,
        "future_14d_count": 0,
        "recent_completed_30d_count": 0,
        "schedule_status": "UNVERIFIED",
    }
    payload = None
    result["request_attempted"] = True
    requests_started += 1

    try:
        request = Request(
            url,
            headers={"User-Agent": "Oracle-Selected50-Current-Fixture-Snapshot/1.0"},
        )
        with urlopen(request, timeout=35) as response:
            result["http_status"] = response.status
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        result["http_status"] = exc.code
        result["error_class"] = "HTTPError"
        result["retry_after_header"] = exc.headers.get("Retry-After") if exc.headers else None
        result["rate_limit_detected"] = exc.code == 429
    except URLError as exc:
        result["error_class"] = type(exc).__name__
    except Exception as exc:
        result["error_class"] = type(exc).__name__

    data = None
    if isinstance(payload, dict):
        result["provider_success"] = payload.get("success") is True
        pager = payload.get("pager") if isinstance(payload.get("pager"), dict) else {}
        result["max_page"] = pager.get("max_page")
        result["current_page"] = pager.get("current_page")
        data = payload.get("data")
        if isinstance(data, list):
            result["returned_match_count"] = len(data)
            try:
                max_page = int(result["max_page"] or 1)
            except (TypeError, ValueError):
                max_page = 1
            if max_page > 1:
                pagination_gaps.append(season_id)

            for match in data:
                if not isinstance(match, dict):
                    continue
                try:
                    kickoff_epoch = int(match.get("date_unix") or 0)
                except (TypeError, ValueError):
                    kickoff_epoch = 0
                if not kickoff_epoch or kickoff_epoch < past_cutoff or kickoff_epoch > future_cutoff:
                    continue

                clean = {
                    field: match.get(field)
                    for field in fields
                    if field in match and isinstance(match.get(field), (str, int, float, bool, type(None)))
                }
                clean.update({
                    "selected_season_id": season_id,
                    "provider_comp_master_id_observed": item["provider_comp_master_id_observed"],
                    "manifest_country": item["country"],
                    "manifest_competition": item["competition"],
                    "kickoff_utc": datetime.fromtimestamp(
                        kickoff_epoch, tz=timezone.utc
                    ).isoformat(),
                    "window_class": "FUTURE_14D" if kickoff_epoch >= now_ts else "RECENT_30D",
                })
                all_window_matches.append(clean)
                result["matches_in_window"] += 1
                if kickoff_epoch >= now_ts:
                    result["future_14d_count"] += 1
                elif str(match.get("status", "")).lower() == "complete":
                    result["recent_completed_30d_count"] += 1

        if result["http_status"] == 200 and result["provider_success"] and isinstance(data, list):
            result["schedule_status"] = (
                "REQUIRES_PAGINATION" if season_id in pagination_gaps else "ONE_PAGE_RESPONSE"
            )
        elif result["provider_success"] and not isinstance(data, list):
            result["error_class"] = "INVALID_PROVIDER_DATA_SHAPE"

    request_succeeded = (
        result["http_status"] == 200
        and result["provider_success"] is True
        and isinstance(data, list)
    )
    if not request_succeeded:
        request_failures.append(season_id)

    results.append(result)

    if not request_succeeded:
        if result["http_status"] == 429:
            stop_reason = "HTTP_429_RATE_LIMITED"
        elif result["http_status"] in (401, 403):
            stop_reason = "HTTP_401_403_AUTH_OR_PLAN_REJECTED"
        elif result["http_status"] is not None:
            stop_reason = "HTTP_ERROR_OR_PROVIDER_RESPONSE_FAILURE"
        else:
            stop_reason = "TRANSPORT_OR_PAYLOAD_FAILURE"
        retry_after_header = result.get("retry_after_header")
        results.extend(not_attempted_row(skipped) for skipped in selected[index + 1:])
        break

    if index < len(selected) - 1:
        time.sleep(REQUEST_INTERVAL_SECONDS)

unattempted_season_ids = [
    str(row.get("selected_season_id") or "")
    for row in results
    if row.get("request_attempted") is False
]

summary = {
    "diagnostic": "BOUNDED_SELECTED50_CURRENT_FIXTURE_SNAPSHOT",
    "retrieved_utc": datetime.now(timezone.utc).isoformat(),
    "window_start_utc": datetime.fromtimestamp(past_cutoff, tz=timezone.utc).isoformat(),
    "window_end_utc": datetime.fromtimestamp(future_cutoff, tz=timezone.utc).isoformat(),
    "endpoint": "league-matches",
    "selected_leagues": len(selected),
    "requests_planned": len(selected),
    "requests_attempted": requests_started,
    "http_200_success": sum(
        1 for row in results
        if row.get("request_attempted") is True
        and row.get("http_status") == 200
        and row.get("provider_success") is True
    ),
    "request_failures": len(request_failures),
    "request_failure_season_ids": request_failures,
    "requests_skipped_after_stop": len(unattempted_season_ids),
    "unattempted_season_ids": unattempted_season_ids,
    "stop_reason": stop_reason,
    "rate_limit_detected": stop_reason == "HTTP_429_RATE_LIMITED",
    "retry_after_header": retry_after_header,
    "provider_retry_attempts": 0,
    "request_interval_seconds": REQUEST_INTERVAL_SECONDS,
    "seasons_needing_pagination": pagination_gaps,
    "complete_one_page_responses": sum(
        1 for row in results if row["schedule_status"] == "ONE_PAGE_RESPONSE"
    ),
    "seasons_with_future_14d_fixtures": sum(
        1 for row in results if row["future_14d_count"] > 0
    ),
    "future_14d_fixture_rows": sum(
        1 for row in all_window_matches if row["window_class"] == "FUTURE_14D"
    ),
    "recent_completed_30d_rows": sum(
        1 for row in all_window_matches
        if row["window_class"] == "RECENT_30D" and str(row.get("status", "")).lower() == "complete"
    ),
    "raw_provider_payload_persisted": False,
    "api_key_persisted": False,
    "production_ledger_written": False,
    "production_eligibility": "NOT_GRANTED",
    "betting_eligibility": "NOT_GRANTED",
    "identity_warning": (
        "FootyStats-native season/team/match IDs only; comp_master_id semantics "
        "and FotMob/Oracle canonical bridge are not approved."
    ),
    "fixture_rows": all_window_matches,
    "per_season": results,
}

(OUT / "current-fixture-snapshot.json").write_text(
    json.dumps(summary, indent=2, sort_keys=True),
    encoding="utf-8",
)
print(json.dumps(
    {key: value for key, value in summary.items() if key not in ("fixture_rows", "per_season")},
    indent=2,
    sort_keys=True,
))
print("PER_SEASON_SUMMARY")
print(json.dumps([
    {
        key: row.get(key)
        for key in (
            "country", "competition", "selected_season_id",
            "provider_comp_master_id_observed", "request_attempted",
            "http_status", "provider_success", "returned_match_count",
            "max_page", "future_14d_count", "recent_completed_30d_count",
            "schedule_status", "error_class", "retry_after_header",
        )
    }
    for row in results
], indent=2, sort_keys=True))
