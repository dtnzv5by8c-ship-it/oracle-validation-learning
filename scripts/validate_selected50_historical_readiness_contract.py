#!/usr/bin/env python3
"""Offline 2024-current Selected-50 historical readiness contract.

This validator never calls a provider and never grants production eligibility.
It validates the structural evidence needed before the bounded historical
ingestion can be admitted: 50 governed season IDs, one-to-one crosswalk,
explicit provider-season identity fields, pagination/chronology contracts and
Oracle feature gates. Missing evidence is a hard BLOCK, never an inferred
PASS.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "oracle-footystats-selected-50-season-id-manifest.csv"
CROSSWALK = ROOT / "reports" / "oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r17.csv"
OUT = ROOT / "audit-output"
START_YEAR = 2024
CURRENT_YEAR = 2026
EXPECTED_LEAGUES = 50

REQUIRED_EVIDENCE_FIELDS = (
    "provider_season_id",
    "provider_season_start_year",
    "provider_season_end_year",
    "provider_fixture_id_coverage_pct",
    "provider_kickoff_field_coverage_pct",
    "provider_team_id_pair_coverage_pct",
    "provider_score_pair_field_coverage_pct",
    "provider_recent_form5_both_teams_coverage_pct",
    "provider_h2h_prior_meeting_rows",
    "provider_standings_payload_status",
    "provider_xg_point_in_time_provenance",
    "provider_odds_point_in_time_provenance",
)

def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise AssertionError(f"Missing required evidence file: {path}")
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))

def nonblank(row: dict[str, str], key: str) -> bool:
    return str(row.get(key, "")).strip() != ""

def pct(value: str) -> float:
    return float(str(value).strip())

def validate_contract(manifest: list[dict[str, str]], crosswalk: list[dict[str, str]]) -> dict:
    result = {
        "contract": "ORACLE_SELECTED50_HISTORICAL_2024_CURRENT_READINESS_V1",
        "historical_window": {"start_year": START_YEAR, "end_year": CURRENT_YEAR, "end_semantics": "CURRENT"},
        "governed_universe": EXPECTED_LEAGUES,
        "network_calls": 0,
        "provider_calls": 0,
        "production_eligible": False,
        "betting_eligible": False,
        "status": "BLOCKED",
        "checks": {},
        "blockers": [],
    }

    ids = [str(r.get("selected_id", "")).strip() for r in manifest]
    result["checks"]["manifest_50_rows"] = len(manifest) == EXPECTED_LEAGUES
    result["checks"]["manifest_unique_nonblank_ids"] = len(ids) == EXPECTED_LEAGUES and len(set(ids)) == EXPECTED_LEAGUES and all(ids)

    xids = [str(r.get("footystats_provider_id", "")).strip() for r in crosswalk]
    result["checks"]["crosswalk_50_rows"] = len(crosswalk) == EXPECTED_LEAGUES
    result["checks"]["crosswalk_unique_provider_ids"] = len(xids) == EXPECTED_LEAGUES and len(set(xids)) == EXPECTED_LEAGUES and all(xids)
    result["checks"]["manifest_to_crosswalk_country_competition_coverage"] = (
        len({(r.get("country","").strip(), r.get("competition_name","").strip()) for r in manifest})
        == EXPECTED_LEAGUES
        and len({(r.get("country","").strip(), r.get("provider_competition_name","").strip()) for r in crosswalk})
        == EXPECTED_LEAGUES
    )

    if not all(result["checks"].values()):
        result["blockers"].append("GOVERNED_50_SCOPE_OR_IDENTITY_EVIDENCE_INVALID")

    # The crosswalk is a research mapping snapshot. Candidate mappings are not
    # promoted to production admission by this contract.
    result["checks"]["crosswalk_candidate_mapping_present"] = all(
        nonblank(r, "canonical_code_candidate") and nonblank(r, "crosswalk_status")
        for r in crosswalk
    )
    approved = sum(str(r.get("crosswalk_status","")).strip() == "APPROVED" for r in crosswalk)
    result["mapping"] = {
        "candidate_rows": len(crosswalk),
        "approved_rows": approved,
        "non_approved_rows": len(crosswalk) - approved,
    }
    if approved != EXPECTED_LEAGUES:
        result["blockers"].append("CANONICAL_MAPPING_NOT_FULLY_APPROVED")

    # If a per-season evidence layer is supplied later, validate every required
    # field and numeric coverage here. With no evidence layer, stay blocked.
    evidence_path = OUT / "selected50_historical_season_readiness_evidence.csv"
    result["checks"]["historical_evidence_layer_present"] = evidence_path.is_file()
    if not evidence_path.is_file():
        result["blockers"].extend([
            "NO_AUTHENTICATED_HISTORICAL_SEASON_EVIDENCE",
            "NO_PROVIDER_SEASON_ID_TO_FIXTURE_TEAM_EVIDENCE",
            "NO_PAGINATION_COMPLETENESS_EVIDENCE",
            "NO_KICKOFF_CHRONOLOGY_EVIDENCE",
            "NO_RECENT_FORM_H2H_STANDINGS_XG_ODDS_POINT_IN_TIME_EVIDENCE",
        ])
    else:
        evidence = read_csv(evidence_path)
        eids = [str(r.get("provider_season_id","")).strip() for r in evidence]
        result["checks"]["evidence_50_unique_seasons"] = len(evidence) == EXPECTED_LEAGUES and len(set(eids)) == EXPECTED_LEAGUES and all(eids)
        missing_fields = sorted({f for r in evidence for f in REQUIRED_EVIDENCE_FIELDS if not nonblank(r, f)})
        result["checks"]["required_evidence_fields_complete"] = not missing_fields
        result["missing_evidence_fields"] = missing_fields
        result["checks"]["season_years_cover_2024_current"] = all(
            int(r["provider_season_start_year"]) <= START_YEAR <= int(r["provider_season_end_year"])
            and int(r["provider_season_end_year"]) <= CURRENT_YEAR + 1
            for r in evidence
            if nonblank(r, "provider_season_start_year") and nonblank(r, "provider_season_end_year")
        )
        for key in ("provider_fixture_id_coverage_pct","provider_kickoff_field_coverage_pct",
                    "provider_team_id_pair_coverage_pct","provider_score_pair_field_coverage_pct",
                    "provider_recent_form5_both_teams_coverage_pct"):
            try:
                result["checks"][f"{key}_is_100"] = all(pct(r[key]) == 100.0 for r in evidence)
            except (KeyError, ValueError):
                result["checks"][f"{key}_is_100"] = False
        result["checks"]["standings_status_present"] = all(nonblank(r, "provider_standings_payload_status") for r in evidence)
        result["checks"]["xg_point_in_time_verified"] = all(
            "VERIFIED" in str(r.get("provider_xg_point_in_time_provenance","")).upper()
            and "NOT_VERIFIED" not in str(r.get("provider_xg_point_in_time_provenance","")).upper()
            for r in evidence
        )
        result["checks"]["odds_point_in_time_verified"] = all(
            "VERIFIED" in str(r.get("provider_odds_point_in_time_provenance","")).upper()
            and "NOT_VERIFIED" not in str(r.get("provider_odds_point_in_time_provenance","")).upper()
            for r in evidence
        )
        if not all(v for k,v in result["checks"].items() if k not in {"historical_evidence_layer_present"}):
            result["blockers"].append("HISTORICAL_EVIDENCE_CONTRACT_FAILED")

    # Gateway/archive admission is an independent mandatory gate.
    receipt = OUT / "footystats_signed_ingestion_receipt.json"
    result["checks"]["authenticated_private_archive_receipt_present"] = receipt.is_file()
    if not receipt.is_file():
        result["blockers"].append("SIGNED_PRIVATE_ARCHIVE_RECEIPT_MISSING")

    result["blockers"] = list(dict.fromkeys(result["blockers"]))
    if not result["blockers"]:
        result["status"] = "READY_FOR_BOUNDED_INGESTION"
    result["next_action"] = (
        "Keep the 728-task plan blocked. Prove the approved gateway and signed private archive receipt, "
        "then create the per-season evidence layer and run this contract before admitting any ingestion batch."
        if result["status"] == "BLOCKED"
        else "Admit only a bounded batch and re-run the contract plus pagination/chronology QA after each checkpoint."
    )
    return result

def main() -> int:
    result = validate_contract(read_csv(MANIFEST), read_csv(CROSSWALK))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "selected50_historical_2024_current_readiness_contract.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
