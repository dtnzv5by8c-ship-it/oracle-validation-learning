#!/usr/bin/env python3
"""Exact-ID reconciliation of the prior 50-league provider identity probe to current 49.

Offline only. Joins solely on exact FootyStats season ID. It verifies country/name
and comp_master equality where a prior probe exists, but never promotes
comp_master_id or candidate canonical IDs to approved competition identity.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

CURRENT_FIELDS = [
    "provider_league_name", "legacy50_selected_provider_season_id",
    "current_plan_season_id_present", "prior_probe_country",
    "prior_probe_competition_name", "prior_probe_comp_master_id",
    "current_crosswalk_comp_master_id", "country_exact_match",
    "competition_exact_match", "current_composite_name_exact_match",
    "comp_master_exact_match", "prior_probe_identity_status",
    "prior_probe_master_id_stability_status", "canonical_candidate_id",
    "canonical_mapping_status", "provider_identity_evidence_status",
    "mapping_approved", "production_eligible", "betting_eligible",
]
ABSENT_FIELDS = [
    "prior_probe_country", "prior_probe_competition_name",
    "prior_probe_season_id", "prior_probe_comp_master_id",
    "current_catalogue_presence", "evidence_date", "disposition",
]
def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path}: missing CSV header")
        return [dict(row) for row in reader]


def _index(rows: list[dict[str, str]], field: str, source: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = str(row.get(field) or "").strip()
        if not value:
            raise ValueError(f"{source}: missing {field}")
        if value in result:
            raise ValueError(f"{source}: duplicate {field} {value}")
        result[value] = row
    return result


def reconcile(
    crosswalk_rows: list[dict[str, str]],
    prior_probe_rows: list[dict[str, str]],
    plan_rows: list[dict[str, str]],
) -> tuple[dict[str, Any], list[dict[str, str]], list[dict[str, str]]]:
    crosswalk = _index(crosswalk_rows, "provider_league_name", "current crosswalk")
    probe = _index(prior_probe_rows, "footystats_season_id", "prior identity probe")
    plan = _index(plan_rows, "provider_season_id", "current season plan")

    referenced_ids: set[str] = set()
    current_output: list[dict[str, str]] = []
    exact_country = exact_competition = exact_composite = exact_master = 0
    no_probe: list[str] = []

    for league, row in sorted(crosswalk.items()):
        selected_id = str(row.get("legacy50_selected_provider_season_id") or "").strip()
        canonical_status = str(row.get("canonical_mapping_status") or "UNSPECIFIED")
        candidate = str(row.get("candidate_canonical_id_from_prior_research") or "").strip()
        if not selected_id:
            if row.get("legacy50_reconciliation_status") != "NEW_IN_CURRENT_SELECTED_CATALOGUE_NOT_IN_LEGACY50":
                raise ValueError(f"{league}: blank legacy selected ID is not marked as a new catalogue league")
            no_probe.append(league)
            current_output.append({
                "provider_league_name": league,
                "legacy50_selected_provider_season_id": "",
                "current_plan_season_id_present": "NOT_APPLICABLE",
                "prior_probe_country": "",
                "prior_probe_competition_name": "",
                "prior_probe_comp_master_id": "",
                "current_crosswalk_comp_master_id": "",
                "country_exact_match": "NOT_ASSESSED",
                "competition_exact_match": "NOT_ASSESSED",
                "current_composite_name_exact_match": "NOT_ASSESSED",
                "comp_master_exact_match": "NOT_ASSESSED",
                "prior_probe_identity_status": "NO_PRIOR_PROBE_ROW",
                "prior_probe_master_id_stability_status": "NOT_ASSESSED",
                "canonical_candidate_id": candidate,
                "canonical_mapping_status": canonical_status,
                "provider_identity_evidence_status": "NEW_CURRENT_CATALOGUE_NO_PRIOR_PROBE_EVIDENCE",
                "mapping_approved": "False",
                "production_eligible": "False",
                "betting_eligible": "False",
            })
            continue

        if selected_id in referenced_ids:
            raise ValueError(f"current crosswalk: duplicate legacy selected provider season ID {selected_id}")
        referenced_ids.add(selected_id)
        if selected_id not in probe:
            raise ValueError(f"{league}: selected provider season ID {selected_id} missing from prior identity probe")
        if selected_id not in plan:
            raise ValueError(f"{league}: selected provider season ID {selected_id} missing from current history plan")
        plan_row = plan[selected_id]
        if plan_row.get("provider_league_name") != league:
            raise ValueError(f"{league}: exact selected season ID maps to a different current plan league")

        evidence = probe[selected_id]
        country = str(evidence.get("country") or "").strip()
        competition = str(evidence.get("competition") or "").strip()
        provider_country = str(evidence.get("provider_country_observed") or "").strip()
        provider_competition = str(evidence.get("provider_competition_name_observed") or "").strip()
        prior_master = str(evidence.get("footystats_comp_master_id_observed") or "").strip()
        current_master = str(row.get("provider_comp_master_id_observed_2026_10_27") or "").strip()
        if not all((country, competition, provider_country, provider_competition, prior_master, current_master)):
            raise ValueError(f"{league}: incomplete prior probe identity fields")
        country_match = country == provider_country
        competition_match = competition == provider_competition
        composite_match = f"{provider_country} {provider_competition}" == league
        master_match = prior_master == current_master
        if not country_match:
            raise ValueError(f"{league}: prior probe country does not match its selected manifest country")
        if not competition_match:
            raise ValueError(f"{league}: prior probe competition does not match its selected manifest competition")
        if not composite_match:
            raise ValueError(f"{league}: prior provider country/name does not reconstruct the current exact league label")
        if not master_match:
            raise ValueError(f"{league}: prior and current crosswalk comp_master values conflict")
        if str(evidence.get("oracle_canonical_league_code") or "").strip():
            raise ValueError(f"{league}: prior probe unexpectedly contains an Oracle canonical approval")
        exact_country += int(country_match)
        exact_competition += int(competition_match)
        exact_composite += int(composite_match)
        exact_master += int(master_match)
        current_output.append({
            "provider_league_name": league,
            "legacy50_selected_provider_season_id": selected_id,
            "current_plan_season_id_present": "True",
            "prior_probe_country": provider_country,
            "prior_probe_competition_name": provider_competition,
            "prior_probe_comp_master_id": prior_master,
            "current_crosswalk_comp_master_id": current_master,
            "country_exact_match": "True",
            "competition_exact_match": "True",
            "current_composite_name_exact_match": "True",
            "comp_master_exact_match": "True",
            "prior_probe_identity_status": str(evidence.get("identity_status") or ""),
            "prior_probe_master_id_stability_status": str(evidence.get("master_id_stability_status") or ""),
            "canonical_candidate_id": candidate,
            "canonical_mapping_status": canonical_status,
            "provider_identity_evidence_status": "EXACT_ONE_SEASON_ID_COUNTRY_NAME_AND_COMP_MASTER_MATCH; PARENT_SEMANTICS_AND_CROSS_SEASON_STABILITY_UNVERIFIED",
            "mapping_approved": "False",
            "production_eligible": "False",
            "betting_eligible": "False",
        })

    absent_rows: list[dict[str, str]] = []
    for sid, evidence in sorted(probe.items()):
        if sid in referenced_ids:
            continue
        absent_rows.append({
            "prior_probe_country": str(evidence.get("provider_country_observed") or ""),
            "prior_probe_competition_name": str(evidence.get("provider_competition_name_observed") or ""),
            "prior_probe_season_id": sid,
            "prior_probe_comp_master_id": str(evidence.get("footystats_comp_master_id_observed") or ""),
            "current_catalogue_presence": "NOT_PRESENT_IN_CURRENT_49_SELECTED_CATALOGUE",
            "evidence_date": str(evidence.get("evidence_date") or ""),
            "disposition": "LEGACY_SELECTED50_ONLY; DO_NOT_ASSUME_PROVIDER_DISCONTINUED; OWNER_DECISION_REQUIRED",
        })

    if len(current_output) != 49:
        raise ValueError(f"expected 49 current crosswalk rows, found {len(current_output)}")
    if len(absent_rows) != 6:
        raise ValueError(f"expected six prior selected-50 IDs absent from current 49, found {len(absent_rows)}")

    summary = {
        "schema_version": "1.0",
        "diagnostic": "FOOTYSTATS_PRIOR_IDENTITY_PROBE_TO_CURRENT_49_CATALOGUE_EXACT_ID_RECONCILIATION",
        "scope": "offline_sanitized_identity_metadata_only",
        "prior_identity_probe_rows": len(prior_probe_rows),
        "current_catalogue_crosswalk_rows": len(crosswalk_rows),
        "current_leagues_with_exact_prior_selected_season_id_probe": len(referenced_ids),
        "exact_country_matches": exact_country,
        "exact_competition_name_matches": exact_competition,
        "exact_country_plus_competition_composite_matches_current_provider_league_name": exact_composite,
        "exact_comp_master_value_matches": exact_master,
        "new_current_catalogue_leagues_without_prior_probe": len(no_probe),
        "new_current_catalogue_league_names_without_prior_probe": no_probe,
        "legacy_probe_ids_absent_from_current_selected_catalogue": len(absent_rows),
        "legacy_probe_ids_absent_from_current_selected_catalogue_details": absent_rows,
        "comp_master_parent_semantics_verified": False,
        "comp_master_cross_season_stability_verified": False,
        "provider_parent_competition_ids_verified": 0,
        "approved_canonical_mappings": 0,
        "all_current_mappings_remain_unapproved": all(r["mapping_approved"] == "False" for r in current_output),
        "api_requests_made": 0,
        "raw_payloads_read": False,
        "production_logic_changed": False,
        "production_eligible": False,
        "betting_eligible": False,
    }
    return summary, current_output, absent_rows


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crosswalk", required=True, type=Path)
    parser.add_argument("--prior-probe", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--current-output", required=True, type=Path)
    parser.add_argument("--absent-output", required=True, type=Path)
    parser.add_argument("--summary-json", required=True, type=Path)
    args = parser.parse_args()
    summary, current_rows, absent_rows = reconcile(
        read_csv(args.crosswalk), read_csv(args.prior_probe), read_csv(args.plan)
    )
    write_csv(args.current_output, CURRENT_FIELDS, current_rows)
    write_csv(args.absent_output, ABSENT_FIELDS, absent_rows)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
