#!/usr/bin/env python3
"""Offline audit of FootyStats season partitions and provider-to-Oracle mapping evidence.

This audit is intentionally conservative. Provider season IDs are treated as exact
season keys; league/canonical identity is not promoted from names, comp_master_id,
or historical date-only joins. No API calls or raw provider payloads are used.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from normalize_footystats_season_year import normalize_season_year

EXPECTED_START = date(2024, 1, 1)
EXPECTED_END = date(2026, 11, 4)
EXPECTED_START_UTC = "2024-01-01T00:00:00Z"
EXPECTED_END_UTC = "2026-11-04T23:59:59.999999Z"

QUEUE_FIELDS = [
    "provider", "provider_league_name", "catalogue_season_count",
    "history_season_count", "history_provider_season_ids", "history_season_labels",
    "provider_country_populated_rows", "provider_competition_id_populated_rows",
    "provider_competition_id_from_crosswalk", "provider_comp_master_id_observed",
    "provider_comp_master_id_semantics", "provider_parent_competition_id",
    "legacy50_reconciliation_status", "candidate_canonical_id",
    "candidate_canonical_competition", "prior_protected_registry_match_state",
    "canonical_mapping_status", "mapping_identity_status", "decision_required",
    "mapping_approved", "production_eligible", "betting_eligible",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path}: missing CSV header")
        return [dict(row) for row in reader]


def _required(row: dict[str, str], key: str, source: str) -> str:
    value = str(row.get(key) or "").strip()
    if not value:
        raise ValueError(f"{source}: missing required {key}")
    return value


def _utc(value: str, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field}: invalid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ValueError(f"{field}: timestamp must be explicit UTC")
    return parsed.astimezone(timezone.utc)


def _bool_false(value: str, field: str) -> None:
    if str(value).strip().lower() not in {"false", "0"}:
        raise ValueError(f"{field} must remain false in research-only output")


def _index_unique(rows: list[dict[str, str]], source: str) -> dict[str, dict[str, str]]:
    indexed: dict[str, dict[str, str]] = {}
    for row in rows:
        sid = _required(row, "provider_season_id", source)
        if sid in indexed:
            raise ValueError(f"{source}: duplicate provider_season_id {sid}")
        indexed[sid] = row
    return indexed


def audit_catalogue(
    registry_rows: list[dict[str, str]],
    plan_rows: list[dict[str, str]],
    excluded_rows: list[dict[str, str]],
    crosswalk_rows: list[dict[str, str]],
    history_start: date = EXPECTED_START,
    history_end: date = EXPECTED_END,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    if history_start != EXPECTED_START or history_end != EXPECTED_END:
        raise ValueError("this governed audit is locked to 2024-01-01 through 2026-11-04")
    if not registry_rows or not plan_rows or not crosswalk_rows:
        raise ValueError("registry, plan and crosswalk must be non-empty")

    registry = _index_unique(registry_rows, "registry")
    planned = _index_unique(plan_rows, "plan")
    excluded = _index_unique(excluded_rows, "excluded")
    if set(planned) & set(excluded):
        raise ValueError("plan and exclusion IDs overlap")
    if set(planned) | set(excluded) != set(registry):
        missing = sorted(set(registry) - (set(planned) | set(excluded)))
        extra = sorted((set(planned) | set(excluded)) - set(registry))
        raise ValueError(f"catalogue partition mismatch; missing={missing[:5]} extra={extra[:5]}")

    for sid, row in registry.items():
        _required(row, "provider_league_name", "registry")
        _required(row, "provider_season_label", "registry")
        if row.get("provider") != "FootyStats":
            raise ValueError(f"registry {sid}: unexpected provider")
        if row.get("catalogue_scope") != "chosen_leagues_only":
            raise ValueError(f"registry {sid}: unexpected catalogue scope")

    for sid, row in planned.items():
        source = f"plan {sid}"
        source_row = registry[sid]
        for key in ("provider_league_name", "provider_season_label"):
            if row.get(key) != source_row.get(key):
                raise ValueError(f"{source}: exact registry {key} mismatch")
        if row.get("provider") != "FootyStats":
            raise ValueError(f"{source}: unexpected provider")
        if row.get("history_start_date") != history_start.isoformat():
            raise ValueError(f"{source}: wrong history_start_date")
        if row.get("history_end_date") != history_end.isoformat():
            raise ValueError(f"{source}: wrong history_end_date")
        if row.get("fixture_filter_start_utc") != EXPECTED_START_UTC:
            raise ValueError(f"{source}: wrong inclusive UTC start boundary")
        if row.get("fixture_filter_end_utc_inclusive") != EXPECTED_END_UTC:
            raise ValueError(f"{source}: wrong inclusive UTC end boundary")
        if str(row.get("fixture_kickoff_filter_required", "")).lower() != "true":
            raise ValueError(f"{source}: fixture kickoff filter is not required")
        if row.get("plan_status") != "PLANNED_NOT_RETRIEVED":
            raise ValueError(f"{source}: unexpected plan status")
        _bool_false(row.get("production_eligible", ""), f"{source} production_eligible")
        _bool_false(row.get("betting_eligible", ""), f"{source} betting_eligible")
        parsed = normalize_season_year(row.get("provider_season_label"))
        if parsed.start_year is None:
            raise ValueError(f"{source}: planned season label is not parseable")
        expected_end = parsed.end_year if parsed.end_year is not None else parsed.start_year
        if int(row.get("season_start_year", -1)) != parsed.start_year:
            raise ValueError(f"{source}: season_start_year conflicts with raw provider label")
        if int(row.get("season_end_year", -1)) != expected_end:
            raise ValueError(f"{source}: season_end_year conflicts with raw provider label")
        if parsed.start_year > history_end.year or expected_end < history_start.year:
            raise ValueError(f"{source}: season-year envelope does not intersect history window")

    boundary_review: list[dict[str, str]] = []
    exclusion_status_counts: Counter[str] = Counter()
    for sid, row in excluded.items():
        source = f"excluded {sid}"
        source_row = registry[sid]
        for key in ("provider_league_name", "provider_season_label"):
            if row.get(key) != source_row.get(key):
                raise ValueError(f"{source}: exact registry {key} mismatch")
        parsed = normalize_season_year(row.get("provider_season_label"))
        if row.get("season_year_parse_status") != parsed.status:
            raise ValueError(f"{source}: parse status conflicts with raw provider label")
        if row.get("exclusion_reason") != "SEASON_OUTSIDE_HISTORY_WINDOW":
            raise ValueError(f"{source}: unexpected exclusion reason; requires manual review")
        if parsed.start_year is None:
            raise ValueError(f"{source}: invalid label cannot be classified as outside window")
        season_end = parsed.end_year if parsed.end_year is not None else parsed.start_year
        if not (parsed.start_year > history_end.year or season_end < history_start.year):
            raise ValueError(f"{source}: exclusion conflicts with season-year overlap")
        exclusion_status_counts[parsed.status] += 1
        if parsed.status == "START_YEAR_ONLY" and parsed.start_year == 2023:
            boundary_review.append({
                "provider_league_name": row["provider_league_name"],
                "provider_season_label": row["provider_season_label"],
                "provider_season_id": sid,
                "issue": "CALENDAR_2023_SEASON_EXCLUDED_BY_LABEL_ONLY",
                "required_action": "Keep excluded from the current plan but verify actual kickoff dates before declaring no 2024 spillover; no fixture evidence is available offline.",
            })

    registry_by_league: dict[str, list[dict[str, str]]] = defaultdict(list)
    plan_by_league: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in registry_rows:
        registry_by_league[row["provider_league_name"]].append(row)
    for row in plan_rows:
        plan_by_league[row["provider_league_name"]].append(row)

    crosswalk_by_league: dict[str, dict[str, str]] = {}
    for row in crosswalk_rows:
        league = _required(row, "provider_league_name", "crosswalk")
        if league in crosswalk_by_league:
            raise ValueError(f"crosswalk: duplicate provider league {league}")
        crosswalk_by_league[league] = row
    if set(crosswalk_by_league) != set(registry_by_league):
        raise ValueError("crosswalk league set does not exactly equal provider registry league set")

    queue: list[dict[str, str]] = []
    mapping_status_counts: Counter[str] = Counter()
    history_id_mismatch_count = 0
    country_populated_total = sum(bool(str(r.get("provider_country") or "").strip()) for r in registry_rows)
    provider_comp_id_populated_total = sum(bool(str(r.get("provider_competition_id") or "").strip()) for r in registry_rows)

    for league in sorted(registry_by_league):
        catalogue = registry_by_league[league]
        history = plan_by_league.get(league, [])
        cross = crosswalk_by_league[league]
        expected_ids = [r["provider_season_id"] for r in history]
        expected_labels = [r["provider_season_label"] for r in history]
        cross_ids = [v for v in str(cross.get("history_provider_season_ids") or "").split(";") if v]
        cross_labels = [v for v in str(cross.get("history_season_labels") or "").split(";") if v]
        if int(cross.get("catalogue_season_count", -1)) != len(catalogue):
            raise ValueError(f"{league}: crosswalk catalogue season count mismatch")
        if int(cross.get("history_season_count", -1)) != len(history):
            raise ValueError(f"{league}: crosswalk history season count mismatch")
        if cross_ids != expected_ids or cross_labels != expected_labels:
            history_id_mismatch_count += 1
            raise ValueError(f"{league}: crosswalk history IDs/labels do not exactly match the season plan")
        for row in catalogue:
            if row.get("provider") != "FootyStats":
                raise ValueError(f"{league}: unexpected provider in catalogue")
        country_count = sum(bool(str(r.get("provider_country") or "").strip()) for r in catalogue)
        competition_id_count = sum(bool(str(r.get("provider_competition_id") or "").strip()) for r in catalogue)
        status = str(cross.get("canonical_mapping_status") or "UNSPECIFIED")
        mapping_status_counts[status] += 1
        candidate = str(cross.get("candidate_canonical_id_from_prior_research") or "").strip()
        comp_master = str(cross.get("provider_comp_master_id_observed_2026_10_27") or "").strip()
        comp_master_semantics = str(cross.get("provider_comp_master_id_semantics") or "").strip()
        parent_id = str(cross.get("provider_parent_competition_id") or "").strip()
        mapping_identity_complete = bool(country_count and competition_id_count and parent_id)
        if status == "CANDIDATE_REQUIRES_HUMAN_APPROVAL_NOT_CANONICAL":
            decision = "HUMAN_APPROVAL_REQUIRED_FOR_CANDIDATE; VERIFY_AUTHORITATIVE_COUNTRY_AND_COMPETITION_ID"
        elif status == "NO_MATCH_IN_CURRENT_PROTECTED_27_LEAGUE_REGISTRY":
            decision = "OWNER_DECISION_REQUIRED; FIND_AUTHORITATIVE_CANONICAL_MAPPING_OR_RETAIN_UNMAPPED"
        elif status == "NOT_ASSESSED_AGAINST_CURRENT_PROTECTED_REGISTRY":
            decision = "ASSESS_NEW_CATALOGUE_LEAGUE_AGAINST_APPROVED_EXPANDED_ORACLE_REGISTRY"
        else:
            decision = "REVIEW_UNRECOGNIZED_MAPPING_STATUS"
        if not country_count or not competition_id_count:
            decision += "; PROVIDER_COUNTRY_OR_COMPETITION_ID_MISSING_IN_CURRENT_REGISTRY"
        if comp_master and comp_master_semantics != "VERIFIED_PARENT_COMPETITION_ID":
            decision += "; COMP_MASTER_ID_OBSERVED_BUT_NOT_APPROVED"
        queue.append({
            "provider": "FootyStats",
            "provider_league_name": league,
            "catalogue_season_count": str(len(catalogue)),
            "history_season_count": str(len(history)),
            "history_provider_season_ids": ";".join(expected_ids),
            "history_season_labels": ";".join(expected_labels),
            "provider_country_populated_rows": str(country_count),
            "provider_competition_id_populated_rows": str(competition_id_count),
            "provider_competition_id_from_crosswalk": str(cross.get("provider_competition_id_from_current_catalogue") or ""),
            "provider_comp_master_id_observed": comp_master,
            "provider_comp_master_id_semantics": comp_master_semantics,
            "provider_parent_competition_id": parent_id,
            "legacy50_reconciliation_status": str(cross.get("legacy50_reconciliation_status") or ""),
            "candidate_canonical_id": candidate,
            "candidate_canonical_competition": str(cross.get("candidate_canonical_competition_from_prior_research") or ""),
            "prior_protected_registry_match_state": str(cross.get("prior_protected_registry_match_state") or ""),
            "canonical_mapping_status": status,
            "mapping_identity_status": "LEAGUE_IDENTITY_INCOMPLETE" if not mapping_identity_complete else "EVIDENCE_PRESENT_REQUIRES_APPROVAL",
            "decision_required": decision,
            "mapping_approved": "False",
            "production_eligible": "False",
            "betting_eligible": "False",
        })

    crosswalk_candidates = sum(bool(str(r.get("candidate_canonical_id_from_prior_research") or "").strip()) for r in crosswalk_rows)
    summary = {
        "schema_version": "1.0",
        "diagnostic": "FOOTYSTATS_49_LEAGUE_SEASON_MAPPING_AND_DATE_BOUNDARY_AUDIT",
        "scope": "offline_sanitized_metadata_only",
        "history_start_utc_inclusive": EXPECTED_START_UTC,
        "history_end_utc_inclusive": EXPECTED_END_UTC,
        "provider_catalogue_rows": len(registry_rows),
        "provider_catalogue_unique_season_ids": len(registry),
        "provider_league_count": len(registry_by_league),
        "planned_season_rows": len(plan_rows),
        "planned_league_count": len(plan_by_league),
        "excluded_season_rows": len(excluded_rows),
        "catalogue_partition_complete": len(registry) == len(planned) + len(excluded),
        "planned_and_excluded_ids_exactly_partition_catalogue": True,
        "planned_season_ids_unique": True,
        "crosswalk_rows": len(crosswalk_rows),
        "crosswalk_league_set_exact": True,
        "crosswalk_history_ids_and_labels_exactly_match_plan": history_id_mismatch_count == 0,
        "provider_country_populated_rows": country_populated_total,
        "provider_competition_id_populated_rows": provider_comp_id_populated_total,
        "provider_parent_competition_ids_verified": sum(bool(r.get("provider_parent_competition_id")) for r in crosswalk_rows),
        "observed_comp_master_ids_not_approved_count": sum(
            bool(r.get("provider_comp_master_id_observed_2026_10_27")) and
            str(r.get("provider_comp_master_id_semantics") or "") != "VERIFIED_PARENT_COMPETITION_ID"
            for r in crosswalk_rows
        ),
        "candidate_canonical_id_count": crosswalk_candidates,
        "canonical_mapping_status_counts": dict(sorted(mapping_status_counts.items())),
        "approved_canonical_mapping_count": sum(
            str(r.get("canonical_mapping_status") or "") == "APPROVED" for r in crosswalk_rows
        ),
        "calendar_2023_start_year_only_exclusions_requiring_fixture_date_review": len(boundary_review),
        "calendar_2023_exclusion_review": boundary_review,
        "excluded_season_parse_status_counts": dict(sorted(exclusion_status_counts.items())),
        "cross_year_2023_2024_planned_count": sum(
            str(r.get("provider_season_label")) == "20232024" for r in plan_rows
        ),
        "cross_year_2026_2027_planned_count": sum(
            str(r.get("provider_season_label")) == "20262027" for r in plan_rows
        ),
        "fixture_level_start_and_end_filter_required": True,
        "season_membership_is_not_fixture_date_coverage": True,
        "raw_payloads_read": False,
        "api_requests_made": 0,
        "production_logic_changed": False,
        "production_eligible": False,
        "betting_eligible": False,
        "mapping_decisions": queue,
    }
    return summary, queue


def write_outputs(summary: dict[str, Any], queue: list[dict[str, str]], queue_csv: Path, summary_json: Path) -> None:
    queue_csv.parent.mkdir(parents=True, exist_ok=True)
    summary_json.parent.mkdir(parents=True, exist_ok=True)
    with queue_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=QUEUE_FIELDS)
        writer.writeheader()
        writer.writerows(queue)
    summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--excluded", required=True, type=Path)
    parser.add_argument("--crosswalk", required=True, type=Path)
    parser.add_argument("--queue-csv", required=True, type=Path)
    parser.add_argument("--summary-json", required=True, type=Path)
    args = parser.parse_args()
    summary, queue = audit_catalogue(
        read_csv(args.registry), read_csv(args.plan), read_csv(args.excluded), read_csv(args.crosswalk)
    )
    write_outputs(summary, queue, args.queue_csv, args.summary_json)
    print(json.dumps({k: v for k, v in summary.items() if k != "mapping_decisions"}, indent=2))


if __name__ == "__main__":
    main()
