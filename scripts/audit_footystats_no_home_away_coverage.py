#!/usr/bin/env python3
"""Offline aggregate audit of FootyStats no_home_away flags.

Consumes only the sanitized season-ingestion coverage CSV. It never calls the
provider, reads credentials, infers fixture sides, or certifies venue features.
All outputs are research-only and preserve the raw-row quarantine requirement.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

REQUIRED_COLUMNS = {
    "provider_league_name",
    "provider_season_label",
    "provider_season_id",
    "preflight_status",
    "matches_total_results",
    "matches_page_count",
    "page_1_match_rows_returned",
    "page_1_no_home_away_rows",
}
SEASON_FIELDS = [
    "provider_league_name", "provider_season_label", "provider_season_id",
    "preflight_status", "matches_total_results", "matches_page_count",
    "page_1_match_rows_returned", "page_1_no_home_away_rows",
    "page_1_no_home_away_rate_pct", "flag_coverage_class",
    "fixture_level_ids_available", "root_cause_resolved",
    "venue_split_eligible", "production_eligible", "betting_eligible",
]
LEAGUE_FIELDS = [
    "provider_league_name", "season_count", "seasons_with_flags",
    "fully_flagged_seasons", "page_1_match_rows_returned",
    "page_1_no_home_away_rows", "page_1_no_home_away_rate_pct",
    "flag_burden_tier", "fixture_level_ids_available",
    "root_cause_resolved", "venue_split_eligible",
    "production_eligible", "betting_eligible",
]


def count(value: Any, field: str, minimum: int = 0) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field} must be a non-negative integer")
    try:
        parsed = Decimal(str(value).strip())
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"{field} must be a non-negative integer") from None
    if not parsed.is_finite() or parsed != parsed.to_integral_value() or parsed < minimum:
        raise ValueError(f"{field} must be a non-negative integer")
    return int(parsed)


def read_coverage(path: Path) -> tuple[list[dict[str, str]], str]:
    if not path.is_file():
        raise ValueError("sanitized season-ingestion coverage CSV is missing")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not REQUIRED_COLUMNS.issubset(set(reader.fieldnames)):
            raise ValueError("coverage CSV is missing required fields")
        rows = list(reader)
    if not rows:
        raise ValueError("coverage CSV contains no season rows")
    return rows, digest


def burden_tier(rate: float, season_count: int, fully_flagged: int) -> str:
    if rate == 0:
        return "NONE_REPORTED"
    if fully_flagged == season_count:
        return "ALL_SAMPLED_SEASONS_FULLY_FLAGGED"
    if rate >= 50:
        return "HIGH_GE_50_PERCENT"
    if rate >= 10:
        return "MODERATE_10_TO_50_PERCENT"
    return "LOW_GT_0_TO_10_PERCENT"


def build_audit(
    rows: list[dict[str, str]],
    input_sha256: str,
    generated_utc: str | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    if not rows:
        raise ValueError("coverage rows are required")
    season_ids: set[str] = set()
    season_output: list[dict[str, Any]] = []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    totals = {
        "page_1_match_rows_returned": 0,
        "page_1_no_home_away_rows": 0,
        "seasons_with_any_no_home_away_rows": 0,
        "seasons_with_all_page_1_rows_no_home_away": 0,
    }
    page_counts: set[int] = set()
    pagination_metadata_consistent = True

    for index, source in enumerate(rows, start=1):
        league = str(source.get("provider_league_name") or "").strip()
        label = str(source.get("provider_season_label") or "").strip()
        season_id = str(source.get("provider_season_id") or "").strip()
        if not league or not label or not season_id:
            raise ValueError(f"season row {index} has incomplete provider identity")
        if season_id in season_ids:
            raise ValueError(f"duplicate provider season ID: {season_id}")
        season_ids.add(season_id)
        status = str(source.get("preflight_status") or "").strip()
        if status != "ENDPOINT_PREFLIGHT_COMPLETE":
            raise ValueError(f"season {season_id} is not endpoint-preflight complete")

        total_results = count(source.get("matches_total_results"), "matches_total_results")
        page_count = count(source.get("matches_page_count"), "matches_page_count", 1)
        returned = count(source.get("page_1_match_rows_returned"), "page_1_match_rows_returned")
        flagged = count(source.get("page_1_no_home_away_rows"), "page_1_no_home_away_rows")
        if returned > total_results:
            raise ValueError(f"page-1 returned rows exceed provider total for season {season_id}")
        if flagged > returned:
            raise ValueError(f"no_home_away count exceeds page-1 rows for season {season_id}")
        if page_count == 1 and returned != total_results:
            pagination_metadata_consistent = False
        if page_count > 1:
            pagination_metadata_consistent = False
        page_counts.add(page_count)

        if flagged == 0:
            classification = "NO_FLAG_REPORTED_ON_PAGE_1"
        elif returned > 0 and flagged == returned:
            classification = "ALL_PAGE_1_ROWS_FLAGGED"
            totals["seasons_with_all_page_1_rows_no_home_away"] += 1
        else:
            classification = "PARTIAL_PAGE_1_FLAG"
        if flagged:
            totals["seasons_with_any_no_home_away_rows"] += 1

        rate = (100.0 * flagged / returned) if returned else 0.0
        item = {
            "provider_league_name": league,
            "provider_season_label": label,
            "provider_season_id": season_id,
            "preflight_status": status,
            "matches_total_results": total_results,
            "matches_page_count": page_count,
            "page_1_match_rows_returned": returned,
            "page_1_no_home_away_rows": flagged,
            "page_1_no_home_away_rate_pct": round(rate, 2),
            "flag_coverage_class": classification,
            "fixture_level_ids_available": False,
            "root_cause_resolved": False,
            "venue_split_eligible": False,
            "production_eligible": False,
            "betting_eligible": False,
        }
        season_output.append(item)
        grouped[league].append(item)
        totals["page_1_match_rows_returned"] += returned
        totals["page_1_no_home_away_rows"] += flagged

    league_output: list[dict[str, Any]] = []
    for league in sorted(grouped):
        group = grouped[league]
        season_count = len(group)
        rows_returned = sum(row["page_1_match_rows_returned"] for row in group)
        flagged = sum(row["page_1_no_home_away_rows"] for row in group)
        affected = sum(row["page_1_no_home_away_rows"] > 0 for row in group)
        fully_flagged = sum(row["flag_coverage_class"] == "ALL_PAGE_1_ROWS_FLAGGED" for row in group)
        rate = (100.0 * flagged / rows_returned) if rows_returned else 0.0
        league_output.append({
            "provider_league_name": league,
            "season_count": season_count,
            "seasons_with_flags": affected,
            "fully_flagged_seasons": fully_flagged,
            "page_1_match_rows_returned": rows_returned,
            "page_1_no_home_away_rows": flagged,
            "page_1_no_home_away_rate_pct": round(rate, 2),
            "flag_burden_tier": burden_tier(rate, season_count, fully_flagged),
            "fixture_level_ids_available": False,
            "root_cause_resolved": False,
            "venue_split_eligible": False,
            "production_eligible": False,
            "betting_eligible": False,
        })

    total_rows = totals["page_1_match_rows_returned"]
    total_flagged = totals["page_1_no_home_away_rows"]
    affected_leagues = sum(row["seasons_with_flags"] > 0 for row in league_output)
    full_seasons = totals["seasons_with_all_page_1_rows_no_home_away"]
    generated = generated_utc or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    summary = {
        "schema_version": "1.0",
        "diagnostic": "FOOTYSTATS_NO_HOME_AWAY_AGGREGATE_COVERAGE_AUDIT",
        "generated_utc": generated,
        "source_file": "data/footystats/full-ingestion-manifest/season-ingestion-coverage.csv",
        "source_sha256": input_sha256,
        "provider_season_count": len(season_output),
        "provider_league_count": len(league_output),
        "page_1_match_rows_returned": total_rows,
        "page_1_no_home_away_rows": total_flagged,
        "page_1_no_home_away_rate_pct": round(100.0 * total_flagged / total_rows, 2) if total_rows else 0.0,
        "seasons_with_any_no_home_away_rows": totals["seasons_with_any_no_home_away_rows"],
        "leagues_with_any_no_home_away_rows": affected_leagues,
        "seasons_with_all_page_1_rows_no_home_away": full_seasons,
        "matches_page_counts_observed": sorted(page_counts),
        "single_page_pagination_metadata_consistent_all_seasons": pagination_metadata_consistent,
        "fixture_level_records_inspected": 0,
        "fixture_level_ids_available_in_source": False,
        "root_cause_resolved": False,
        "venue_split_policy": "QUARANTINE_FLAGGED_FIXTURES; DO_NOT_INFER_HOME_AWAY; NONFLAGGED_ROWS_ARE_NOT_AUTOMATICALLY_CERTIFIED",
        "interpretation": "Counts describe provider no_home_away flags in sanitized page-1 season aggregates only. They do not identify fixture-level causes, establish neutral-venue semantics, or certify team-side assignments.",
        "api_requests_made": 0,
        "raw_provider_payloads_read": False,
        "production_logic_changed": False,
        "production_eligible": False,
        "betting_eligible": False,
    }
    return season_output, league_output, summary


def write_outputs(output_dir: Path, seasons: list[dict[str, Any]], leagues: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, rows, fields in (
        ("season-summary.csv", seasons, SEASON_FIELDS),
        ("league-summary.csv", leagues, LEAGUE_FIELDS),
    ):
        with (output_dir / filename).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coverage-csv", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    rows, digest = read_coverage(args.coverage_csv)
    seasons, leagues, summary = build_audit(rows, digest)
    write_outputs(args.output_dir, seasons, leagues, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
