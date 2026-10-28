#!/usr/bin/env python3
"""Adapt FootyStats selected-50 snapshot into a provider-neutral research feed.

No API calls, no secrets, no FotMob IDs, no production writes, no model changes.
The selected FootyStats season ID is the authoritative competition-season anchor.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUSPENDED_WORDS = {"suspended", "postponed", "cancelled", "canceled", "abandoned", "delayed"}


def truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes"}


def integer_or_blank(value: Any) -> int | str:
    try:
        if value in (None, ""):
            return ""
        return int(float(value))
    except (TypeError, ValueError, OverflowError):
        return ""


def valid_team_id(value: Any) -> bool:
    return value not in (None, "") and str(value).strip().lower() not in {"0", "none", "null"}


def classify(row: dict[str, Any], now: datetime) -> tuple[str, str]:
    status = str(row.get("status") or "").strip().lower()
    kickoff = str(row.get("kickoff_utc") or "")
    if truthy(row.get("no_home_away")):
        return "QUARANTINE_NO_HOME_AWAY", "Provider flags fixture as lacking a standard home/away assignment."
    if any(word in status for word in SUSPENDED_WORDS):
        return "QUARANTINE_SCHEDULE_STATUS", f"Provider status is non-standard: {status or 'unknown'}."
    if not valid_team_id(row.get("homeID")) or not valid_team_id(row.get("awayID")):
        return "QUARANTINE_MISSING_TEAM_ID", "FootyStats home/away provider team ID missing."
    if not str(row.get("home_name") or "").strip() or not str(row.get("away_name") or "").strip():
        return "QUARANTINE_MISSING_TEAM_NAME", "Home/away team name missing."
    try:
        ko = datetime.fromisoformat(kickoff.replace("Z", "+00:00"))
        if ko.tzinfo is None:
            ko = ko.replace(tzinfo=timezone.utc)
        ko = ko.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return "QUARANTINE_INVALID_KICKOFF", "Kickoff timestamp missing or invalid."
    if status in {"complete", "completed", "finished", "ft", "full time"}:
        if integer_or_blank(row.get("homeGoalCount")) == "" or integer_or_blank(row.get("awayGoalCount")) == "":
            return "QUARANTINE_INCOMPLETE_SCORE", "Completed status but one or both scores are missing."
        return "HISTORICAL_COMPLETED_CANDIDATE", "Completed source record; settlement truth remains independently governed."
    if ko <= now:
        return "QUARANTINE_NONFUTURE_UNSETTLED", "Kickoff is not in the future and source status is not explicitly completed."
    return "RESEARCH_FIXTURE_CANDIDATE", "Future FootyStats fixture; prediction readiness still requires feature and market gates."


def adapt(snapshot: dict[str, Any], now: datetime | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    now = now or datetime.now(timezone.utc)
    rows = snapshot.get("fixture_rows")
    seasons = snapshot.get("per_season")
    if not isinstance(rows, list) or not isinstance(seasons, list):
        raise ValueError("snapshot must contain fixture_rows and per_season lists")
    season_ids = {str(x.get("selected_season_id") or "") for x in seasons if isinstance(x, dict)}
    if len(seasons) != 50 or len(season_ids) != 50 or "" in season_ids:
        raise ValueError("selected-50 guard failed: expected 50 per-season records with 50 unique season IDs")
    successful = {
        str(x.get("selected_season_id"))
        for x in seasons
        if isinstance(x, dict) and x.get("http_status") == 200 and x.get("provider_success") is True
    }
    if successful != season_ids:
        raise ValueError(f"source retrieval guard failed: {len(successful)}/50 seasons returned verified HTTP 200 success")
    output = []
    seen_ids = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        season = str(row.get("selected_season_id") or "")
        if season not in season_ids:
            raise ValueError(f"fixture references unselected or missing season ID: {season!r}")
        match_id = str(row.get("id") or "").strip()
        if not match_id:
            raise ValueError(f"fixture in selected season {season} has no FootyStats match ID")
        identity = (season, match_id)
        if identity in seen_ids:
            raise ValueError(f"duplicate FootyStats season/match ID: {identity}")
        seen_ids.add(identity)
        eligibility, reason = classify(row, now)
        output.append({
            "source_provider": "FootyStats",
            "source_season_id": season,
            "research_league_key": f"FS_SEASON_{season}",
            "source_match_id": match_id,
            "source_home_team_id": str(row.get("homeID") or ""),
            "source_away_team_id": str(row.get("awayID") or ""),
            "country": str(row.get("manifest_country") or ""),
            "competition": str(row.get("manifest_competition") or ""),
            "home_team": str(row.get("home_name") or ""),
            "away_team": str(row.get("away_name") or ""),
            "kickoff_utc": str(row.get("kickoff_utc") or ""),
            "source_status": str(row.get("status") or ""),
            "home_goals": integer_or_blank(row.get("homeGoalCount")),
            "away_goals": integer_or_blank(row.get("awayGoalCount")),
            "no_home_away": int(truthy(row.get("no_home_away"))),
            "source_round_id": str(row.get("roundID") or ""),
            "source_game_week": str(row.get("game_week") or ""),
            "btts_potential_source_value": row.get("btts_potential", ""),
            "o25_potential_source_value": row.get("o25_potential", ""),
            "fixture_eligibility": eligibility,
            "eligibility_reason": reason,
            "model_prediction_status": "NOT_RUN",
            "production_eligible": "NO",
        })
    digest = hashlib.sha256(json.dumps(output, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    summary = {
        "diagnostic": "FOOTYSTATS_SELECTED50_PROVIDER_NEUTRAL_ADAPTER",
        "generated_utc": now.isoformat(),
        "source_snapshot_retrieved_utc": snapshot.get("retrieved_utc", "UNKNOWN"),
        "selected_league_seasons": 50,
        "season_retrieval_success": len(successful),
        "source_fixture_rows": len(rows),
        "adapted_fixture_rows": len(output),
        "duplicate_source_match_ids": 0,
        "future_research_fixture_candidates": sum(x["fixture_eligibility"] == "RESEARCH_FIXTURE_CANDIDATE" for x in output),
        "historical_completed_candidates": sum(x["fixture_eligibility"] == "HISTORICAL_COMPLETED_CANDIDATE" for x in output),
        "quarantined_rows": sum(x["fixture_eligibility"].startswith("QUARANTINE_") for x in output),
        "source_provider": "FootyStats",
        "fotmob_dependency": "NONE",
        "provider_ids_preserved_not_crosswalked": True,
        "production_writes": 0,
        "model_predictions_created": 0,
        "production_eligibility": "NOT_GRANTED",
        "output_sha256": digest,
    }
    return output, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--output-manifest", required=True, type=Path)
    args = parser.parse_args()
    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    rows, summary = adapt(snapshot)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else [
        "source_provider", "source_season_id", "research_league_key", "source_match_id",
        "source_home_team_id", "source_away_team_id", "fixture_eligibility",
        "eligibility_reason", "model_prediction_status", "production_eligible"
    ]
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    args.output_manifest.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
