#!/usr/bin/env python3
"""Build an offline exact-name reconciliation of the current FootyStats catalogue.

This is a provider-to-legacy-manifest / canonical-candidate audit, not an
approved Oracle canonical mapping. It never makes API calls or edits production.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

OUTPUT_FIELDS = (
    "provider",
    "provider_league_name",
    "catalogue_scope",
    "catalogue_season_count",
    "history_window_start",
    "history_window_end_inclusive",
    "history_season_count",
    "history_provider_season_ids",
    "history_season_labels",
    "legacy50_exact_country_competition_match",
    "legacy50_selected_provider_season_id",
    "legacy50_selected_id_present_under_same_provider_name",
    "legacy50_reconciliation_status",
    "provider_competition_id_from_current_catalogue",
    "provider_comp_master_id_observed_2026_10_27",
    "provider_comp_master_id_semantics",
    "candidate_canonical_id_from_prior_research",
    "candidate_canonical_competition_from_prior_research",
    "prior_protected_registry_match_state",
    "canonical_mapping_status",
    "historical_ledger_code_candidate",
    "historical_ledger_team_date_join_count",
    "historical_ledger_join_precision",
    "historical_ledger_candidate_status",
    "provider_parent_competition_id",
    "parent_competition_id_status",
    "data_coverage_status",
    "production_eligible",
    "betting_eligible",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_legacy_manifest(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            raise ValueError(f"legacy manifest line {line_no} has fewer than four columns")
        row_number, provider_id, country, competition = cells[:4]
        if not row_number.isdigit() or not provider_id or not country or not competition:
            raise ValueError(f"legacy manifest line {line_no} has invalid identity fields")
        rows.append({
            "manifest_row": row_number,
            "selected_provider_season_id": provider_id,
            "country": country,
            "competition": competition,
            "provider_league_name": f"{country} {competition}",
        })
    if not rows:
        raise ValueError("legacy selected-50 manifest contains no league rows")
    names = [row["provider_league_name"] for row in rows]
    ids = [row["selected_provider_season_id"] for row in rows]
    if len(names) != len(set(names)):
        raise ValueError("legacy manifest contains duplicate country/competition names")
    if len(ids) != len(set(ids)):
        raise ValueError("legacy manifest contains duplicate selected provider IDs")
    return rows


def _bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def build_reconciliation(
    catalogue_rows: list[dict[str, str]],
    plan_rows: list[dict[str, str]],
    legacy_rows: list[dict[str, str]],
    prior_crosswalk_rows: list[dict[str, str]],
    expected_start: str,
    expected_end: str,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    if not catalogue_rows or not plan_rows:
        raise ValueError("catalogue and historical season plan must both be non-empty")

    catalogue_by_id: dict[str, dict[str, str]] = {}
    catalogue_by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    scopes = set()
    for row in catalogue_rows:
        sid = str(row.get("provider_season_id") or "").strip()
        name = str(row.get("provider_league_name") or "").strip()
        scope = str(row.get("catalogue_scope") or "").strip()
        if not sid or not name:
            raise ValueError("catalogue rows require exact provider season ID and league name")
        if sid in catalogue_by_id:
            raise ValueError(f"duplicate provider season ID in catalogue: {sid}")
        if scope not in {"chosen_leagues_only", "all_available"}:
            raise ValueError(f"unsupported or missing catalogue scope for season {sid}")
        scopes.add(scope)
        catalogue_by_id[sid] = row
        catalogue_by_name[name].append(row)
    if len(scopes) != 1:
        raise ValueError("catalogue rows have mixed catalogue scopes")

    plan_by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    plan_ids: set[str] = set()
    plan_windows: set[tuple[str, str]] = set()
    for row in plan_rows:
        sid = str(row.get("provider_season_id") or "").strip()
        name = str(row.get("provider_league_name") or "").strip()
        start = str(row.get("history_start_date") or "").strip()
        end = str(row.get("history_end_date") or "").strip()
        if not sid or not name:
            raise ValueError("historical plan rows require exact provider season ID and league name")
        if sid in plan_ids:
            raise ValueError(f"duplicate provider season ID in historical plan: {sid}")
        if sid not in catalogue_by_id or catalogue_by_id[sid].get("provider_league_name") != name:
            raise ValueError(f"historical plan season {sid} does not exactly reconcile to the catalogue")
        if str(row.get("plan_status") or "") != "PLANNED_NOT_RETRIEVED":
            raise ValueError(f"unexpected historical plan status for season {sid}")
        if _bool_text(row.get("production_eligible")) or _bool_text(row.get("betting_eligible")):
            raise ValueError(f"historical plan season {sid} has an invalid eligibility flag")
        plan_ids.add(sid)
        plan_windows.add((start, end))
        plan_by_name[name].append(row)
    if plan_windows != {(expected_start, expected_end)}:
        raise ValueError(f"historical plan window does not equal {expected_start} through {expected_end}: {sorted(plan_windows)}")

    legacy_by_name = {row["provider_league_name"]: row for row in legacy_rows}
    prior_by_name: dict[str, dict[str, str]] = {}
    for row in prior_crosswalk_rows:
        name = str(row.get("provider_catalogue_name") or "").strip()
        if not name:
            continue
        if name in prior_by_name:
            raise ValueError(f"duplicate prior crosswalk provider name: {name}")
        prior_by_name[name] = row

    output: list[dict[str, str]] = []
    for name in sorted(catalogue_by_name):
        catalogue_seasons = catalogue_by_name[name]
        history = sorted(
            plan_by_name.get(name, []),
            key=lambda row: (str(row.get("provider_season_label") or ""), str(row.get("provider_season_id") or "")),
        )
        if not history:
            raise ValueError(f"current provider league has no 2024-forward season plan: {name}")

        legacy = legacy_by_name.get(name)
        if legacy:
            selected_id = legacy["selected_provider_season_id"]
            exact_id_rows = [
                row for row in catalogue_seasons
                if str(row.get("provider_season_id") or "") == selected_id
            ]
            if len(exact_id_rows) == 1:
                legacy_status = "EXACT_LEGACY_NAME_AND_SELECTED_SEASON_ID_PRESENT"
                legacy_id_present = "TRUE"
            else:
                legacy_status = "LEGACY_NAME_MATCH_BUT_SELECTED_SEASON_ID_NOT_IN_CURRENT_CATALOGUE"
                legacy_id_present = "FALSE"
            legacy_exact = "TRUE"
        else:
            selected_id = ""
            legacy_status = "NEW_IN_CURRENT_SELECTED_CATALOGUE_NOT_IN_LEGACY50"
            legacy_id_present = "NOT_APPLICABLE"
            legacy_exact = "FALSE"

        prior = prior_by_name.get(name, {})
        candidate_id = str(prior.get("canonical_candidate_id") or "").strip()
        candidate_comp = str(prior.get("canonical_candidate_competition") or "").strip()
        prior_state = str(prior.get("match_state") or "").strip()
        if candidate_id:
            canonical_status = "CANDIDATE_REQUIRES_HUMAN_APPROVAL_NOT_CANONICAL"
        elif prior_state == "NO_MATCH_IN_CURRENT_27_LEAGUE_REGISTRY":
            canonical_status = "NO_MATCH_IN_CURRENT_PROTECTED_27_LEAGUE_REGISTRY"
        else:
            canonical_status = "NOT_ASSESSED_AGAINST_CURRENT_PROTECTED_REGISTRY"

        output.append({
            "provider": "FootyStats",
            "provider_league_name": name,
            "catalogue_scope": next(iter(scopes)),
            "catalogue_season_count": str(len(catalogue_seasons)),
            "history_window_start": expected_start,
            "history_window_end_inclusive": expected_end,
            "history_season_count": str(len(history)),
            "history_provider_season_ids": ";".join(str(row["provider_season_id"]) for row in history),
            "history_season_labels": ";".join(str(row["provider_season_label"]) for row in history),
            "legacy50_exact_country_competition_match": legacy_exact,
            "legacy50_selected_provider_season_id": selected_id,
            "legacy50_selected_id_present_under_same_provider_name": legacy_id_present,
            "legacy50_reconciliation_status": legacy_status,
            "provider_competition_id_from_current_catalogue": str(catalogue_seasons[-1].get("provider_competition_id") or ""),
            "provider_comp_master_id_observed_2026_10_27": str(prior.get("provider_comp_master_id_observed") or ""),
            "provider_comp_master_id_semantics": "OBSERVED_PROVIDER_FIELD_NOT_APPROVED_AS_PARENT_OR_CANONICAL_ID" if prior.get("provider_comp_master_id_observed") else "NOT_OBSERVED_FOR_THIS_CURRENT_CATALOGUE_ENTRY",
            "candidate_canonical_id_from_prior_research": candidate_id,
            "candidate_canonical_competition_from_prior_research": candidate_comp,
            "prior_protected_registry_match_state": prior_state,
            "canonical_mapping_status": canonical_status,
            "historical_ledger_code_candidate": str(prior.get("historical_ledger_code_candidate") or ""),
            "historical_ledger_team_date_join_count": str(prior.get("historical_ledger_team_date_join_count") or ""),
            "historical_ledger_join_precision": str(prior.get("historical_ledger_join_precision") or ""),
            "historical_ledger_candidate_status": str(prior.get("historical_ledger_candidate_status") or ""),
            "provider_parent_competition_id": "",
            "parent_competition_id_status": "UNVERIFIED_DO_NOT_PROMOTE_COMP_MASTER_ID",
            "data_coverage_status": "OFFLINE_SEASON_PLAN_ONLY_NO_2024_FORWARD_PROVIDER_DATA_RETRIEVED_BY_THIS_AUDIT",
            "production_eligible": "false",
            "betting_eligible": "false",
        })

    legacy_names = set(legacy_by_name)
    current_names = set(catalogue_by_name)
    removed = sorted(legacy_names - current_names)
    added = sorted(current_names - legacy_names)
    counts = Counter(row["canonical_mapping_status"] for row in output)
    summary = {
        "schema_version": "1.0",
        "diagnostic": "FOOTYSTATS_CURRENT_CATALOGUE_TO_LEGACY50_AND_CANONICAL_CANDIDATE_RECONCILIATION",
        "source_of_truth": "FootyStats",
        "catalogue_scope": next(iter(scopes)),
        "history_start_date": expected_start,
        "history_end_date_inclusive": expected_end,
        "current_provider_league_count": len(catalogue_by_name),
        "current_catalogue_season_row_count": len(catalogue_rows),
        "historical_plan_provider_league_count": len(plan_by_name),
        "historical_plan_season_row_count": len(plan_rows),
        "legacy50_manifest_row_count": len(legacy_rows),
        "exact_legacy_country_competition_matches": sum(row["legacy50_exact_country_competition_match"] == "TRUE" for row in output),
        "legacy50_selected_ids_present_under_exact_current_provider_names": sum(row["legacy50_selected_id_present_under_same_provider_name"] == "TRUE" for row in output),
        "legacy50_leagues_absent_from_current_selected_catalogue_count": len(removed),
        "new_current_catalogue_leagues_not_in_legacy50_count": len(added),
        "canonical_candidate_requires_human_approval_count": counts["CANDIDATE_REQUIRES_HUMAN_APPROVAL_NOT_CANONICAL"],
        "no_match_in_current_protected_27_registry_count": counts["NO_MATCH_IN_CURRENT_PROTECTED_27_LEAGUE_REGISTRY"],
        "not_assessed_against_current_protected_registry_count": counts["NOT_ASSESSED_AGAINST_CURRENT_PROTECTED_REGISTRY"],
        "historical_ledger_code_candidate_count": sum(bool(row["historical_ledger_code_candidate"]) for row in output),
        "legacy50_leagues_absent_from_current_selected_catalogue": removed,
        "new_current_catalogue_leagues_not_in_legacy50": added,
        "provider_parent_competition_ids_verified": 0,
        "approved_oracle_canonical_mappings": 0,
        "api_requests_made": 0,
        "raw_provider_data_written": False,
        "production_logic_changed": False,
        "production_eligible": False,
        "betting_eligible": False,
        "limitations": [
            "The current catalogue is chosen_leagues_only and contains 49 leagues; it is not the complete public FootyStats universe.",
            "Canonical IDs from prior research are candidates only and require human review; the current protected 27-league registry is not the full intended expanded universe.",
            "Provider comp_master_id was observed in a prior probe but its parent-competition semantics remain unverified.",
            "The 2024-forward season plan identifies season partitions only; it does not prove that fixtures, results, teams, H2H, standings, recent form or xG have been ingested.",
            "Historical ledger code candidates use team-pair/date joins and do not establish kickoff-precise canonical identity.",
        ],
    }
    if len(plan_ids) != len(plan_rows):
        raise ValueError("historical plan contains duplicate provider season IDs")
    if set(plan_ids) != {
        str(row.get("provider_season_id") or "").strip()
        for row in catalogue_rows
        if str(row.get("provider_season_id") or "").strip() in plan_ids
    }:
        raise ValueError("historical plan/catalogue season identity reconciliation failed")
    return output, summary


def write_outputs(rows: list[dict[str, str]], summary: dict[str, Any], out_csv: Path, out_json: Path) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    out_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogue", required=True, type=Path)
    parser.add_argument("--season-plan", required=True, type=Path)
    parser.add_argument("--legacy50-manifest", required=True, type=Path)
    parser.add_argument("--prior-canonical-crosswalk", required=True, type=Path)
    parser.add_argument("--history-start", default="2024-01-01")
    parser.add_argument("--history-end", required=True)
    parser.add_argument("--out-csv", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    args = parser.parse_args()
    rows, summary = build_reconciliation(
        read_csv(args.catalogue),
        read_csv(args.season_plan),
        parse_legacy_manifest(args.legacy50_manifest),
        read_csv(args.prior_canonical_crosswalk),
        args.history_start,
        args.history_end,
    )
    write_outputs(rows, summary, args.out_csv, args.out_json)
    print(json.dumps({key: summary[key] for key in (
        "current_provider_league_count",
        "current_catalogue_season_row_count",
        "historical_plan_season_row_count",
        "exact_legacy_country_competition_matches",
        "legacy50_leagues_absent_from_current_selected_catalogue_count",
        "new_current_catalogue_leagues_not_in_legacy50_count",
        "canonical_candidate_requires_human_approval_count",
        "no_match_in_current_protected_27_registry_count",
        "not_assessed_against_current_protected_registry_count",
        "historical_ledger_code_candidate_count",
        "api_requests_made",
        "approved_oracle_canonical_mappings",
        "production_eligible",
        "betting_eligible",
    )}, indent=2))


if __name__ == "__main__":
    main()
