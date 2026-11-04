#!/usr/bin/env python3
"""Offline audit of sanitized Run56 archive evidence against the current FootyStats 49-league plan."""
from __future__ import annotations
import csv, json, re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    "crosswalk": ROOT / "data/footystats/current-catalogue-reconciliation-2026-11-04/current-catalogue-provider-to-oracle-candidate-crosswalk.csv",
    "archive_evidence": ROOT / "data/run56_selected50_archive_evidence.csv",
    "feature_coverage": ROOT / "data/run56_selected50_archive_feature_coverage.csv",
    "settlement_register": ROOT / "data/oracle-identity-settlement-evidence-register-2026-10-28.csv",
    "season_plan": ROOT / "data/footystats/historical-season-plan-2024-2026/season-plan.csv",
}
OUTPUT_DIR = ROOT / "data/footystats/existing-archive-id-scope-audit-2026-11-04"
COVERAGE_FIELDS = [
    "provider_league_name", "legacy50_selected_provider_season_id", "canonical_mapping_status",
    "run56_archive_status", "run56_match_count", "run56_team_count", "run56_feature_records",
    "team_id_field_complete_rows", "parseable_kickoff_rows", "score_complete_rows",
    "explicit_score_pair_rows", "settled_status_allowed_rows",
    "exact_provider_season_id_in_current_plan", "exact_plan_league_name_match",
    "fixture_id_values_available_in_run56_sanitized_source",
    "team_id_values_available_in_run56_sanitized_source", "cross_season_identity_status",
    "production_eligible", "betting_eligible",
]

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]

def unique_index(rows: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    out = {}
    for row in rows:
        value = str(row.get(key) or "").strip()
        if not value:
            raise ValueError(f"{label} contains blank {key}")
        if value in out:
            raise ValueError(f"{label} contains duplicate {key}={value}")
        out[value] = row
    return out

def integer(row: dict[str, Any], key: str, label: str) -> int:
    value = row.get(key)
    if value is None or str(value).strip() == "":
        raise ValueError(f"{label} has missing {key}")
    try:
        result = int(str(value).strip())
    except (TypeError, ValueError, OverflowError):
        raise ValueError(f"{label} has invalid {key}") from None
    if result < 0:
        raise ValueError(f"{label} has negative {key}")
    return result

def is_yes(value: Any) -> bool:
    return str(value or "").strip().casefold() in {"yes", "true", "1"}

def duplicate_values(values: list[str]) -> list[str]:
    seen, duplicates = set(), set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)

def build_audit(crosswalk, archive_evidence, feature_coverage, settlement_register, season_plan):
    if not crosswalk:
        raise ValueError("current crosswalk is empty")
    unique_index(crosswalk, "provider_league_name", "current crosswalk")
    if any(str(r.get("provider") or "") != "FootyStats" for r in crosswalk):
        raise ValueError("non-FootyStats provider in current crosswalk")
    plan = unique_index(season_plan, "provider_season_id", "historical season plan")
    archive = unique_index(archive_evidence, "selected_id", "Run56 archive evidence")
    features = unique_index(feature_coverage, "selected_id", "Run56 feature coverage")

    legacy_ids = [str(r.get("legacy50_selected_provider_season_id") or "").strip()
                  for r in crosswalk if str(r.get("legacy50_selected_provider_season_id") or "").strip()]
    if len(legacy_ids) != len(set(legacy_ids)):
        raise ValueError("duplicate legacy selected season IDs in current crosswalk")

    output = []
    ingested_ids = set()
    for r in crosswalk:
        league = str(r["provider_league_name"]).strip()
        sid = str(r.get("legacy50_selected_provider_season_id") or "").strip()
        item = {
            "provider_league_name": league,
            "legacy50_selected_provider_season_id": sid,
            "canonical_mapping_status": str(r.get("canonical_mapping_status") or "UNRECORDED"),
            "run56_archive_status": "",
            "run56_match_count": "",
            "run56_team_count": "",
            "run56_feature_records": "",
            "team_id_field_complete_rows": "",
            "parseable_kickoff_rows": "",
            "score_complete_rows": "",
            "explicit_score_pair_rows": "",
            "settled_status_allowed_rows": "",
            "exact_provider_season_id_in_current_plan": False,
            "exact_plan_league_name_match": False,
            "fixture_id_values_available_in_run56_sanitized_source": False,
            "team_id_values_available_in_run56_sanitized_source": False,
            "cross_season_identity_status": "",
            "production_eligible": False,
            "betting_eligible": False,
        }
        if not sid:
            item["run56_archive_status"] = "NO_LEGACY_SELECTED_SEASON_ID_NEW_CATALOGUE_ENTRY"
            item["cross_season_identity_status"] = "NO_PRIOR_SELECTED_SEASON_ID_EVIDENCE"
            output.append(item)
            continue
        plan_row = plan.get(sid)
        if plan_row is None:
            raise ValueError(f"legacy selected season ID {sid} absent from current historical plan")
        if str(plan_row.get("provider_league_name") or "").strip() != league:
            raise ValueError(f"exact season ID {sid} maps to a different provider league in the plan")
        item["exact_provider_season_id_in_current_plan"] = True
        item["exact_plan_league_name_match"] = True

        ar = archive.get(sid)
        if ar is None:
            item["run56_archive_status"] = "NO_RUN56_MANIFEST_ROW"
            item["cross_season_identity_status"] = "NO_ARCHIVE_ID_LEVEL_EVIDENCE"
            output.append(item)
            continue
        if str(ar.get("run56_ingestion_status") or "").strip() != "INGESTED":
            item["run56_archive_status"] = "RUN56_NOT_INGESTED_OR_NO_MANIFEST"
            item["cross_season_identity_status"] = "NO_ARCHIVED_FIXTURE_OR_TEAM_ID_EVIDENCE"
            output.append(item)
            continue

        ft = features.get(sid)
        if ft is None:
            raise ValueError(f"Run56 ingested season {sid} has no feature-coverage row")
        records = integer(ft, "records", f"Run56 feature season {sid}")
        matches = integer(ar, "match_count", f"Run56 archive season {sid}")
        teams = integer(ar, "team_count", f"Run56 archive season {sid}")
        if matches != records:
            raise ValueError(f"Run56 match_count and feature records disagree for season {sid}")
        if integer(ar, "matches_pages", f"Run56 archive season {sid}") != 1:
            raise ValueError(f"Run56 season {sid} is not a single-page archive snapshot")
        if ar.get("tables_status") != "SUCCESS" or ar.get("season_stats_status") != "SUCCESS":
            raise ValueError(f"Run56 tables/season status is not SUCCESS for season {sid}")
        for field in ("team_ids_complete", "parseable_kickoff", "score_complete", "explicit_score_pairs"):
            if integer(ft, field, f"Run56 feature season {sid}") != records:
                raise ValueError(f"Run56 {field} is incomplete for season {sid}")
        if integer(ft, "missing_team_names", f"Run56 feature season {sid}") != 0:
            raise ValueError(f"Run56 missing team names in season {sid}")
        settled = integer(ft, "settled_status_allowed", f"Run56 feature season {sid}")
        if settled > records or teams <= 0:
            raise ValueError(f"Run56 invalid settled/team count for season {sid}")
        ingested_ids.add(sid)
        item.update({
            "run56_archive_status": "RUN56_INGESTED_AGGREGATE_ONLY",
            "run56_match_count": matches,
            "run56_team_count": teams,
            "run56_feature_records": records,
            "team_id_field_complete_rows": records,
            "parseable_kickoff_rows": records,
            "score_complete_rows": records,
            "explicit_score_pair_rows": records,
            "settled_status_allowed_rows": settled,
            "cross_season_identity_status": "TEAM_ID_FIELD_COMPLETENESS_ONLY_NO_ID_VALUES",
        })
        output.append(item)

    if set(features) != ingested_ids:
        raise ValueError("Run56 feature IDs do not exactly equal ingested archive IDs")
    if not ingested_ids.issubset(set(legacy_ids)):
        raise ValueError("Run56 ingested IDs absent from current exact crosswalk")

    settlement_fields = set(settlement_register[0]) if settlement_register else set()
    fs_ids = [str(r.get("footystats_fixture_id") or "").strip() for r in settlement_register]
    fm_ids = [str(r.get("fotmob_fixture_id") or "").strip() for r in settlement_register]
    if any(not x for x in fs_ids + fm_ids):
        raise ValueError("settlement register has blank fixture ID")
    if duplicate_values(fs_ids) or duplicate_values(fm_ids):
        raise ValueError("settlement register contains duplicate fixture IDs")
    team_id_columns = sorted(
        name for name in settlement_fields
        if re.search(r"(^|_)(home|away)_?(team|club)?_?id$|^(home|away)id$", name, re.I)
    )
    exact_name_time = sum(
        r.get("join_precision") == "EXACT_ORDERED_TEAM_NAMES_AND_UTC_KICKOFF"
        for r in settlement_register
    )
    canonical_approved = sum(is_yes(r.get("canonical_bridge_approved")) for r in settlement_register)
    settlement_truth = sum(is_yes(r.get("settlement_truth_verified")) for r in settlement_register)
    settlement_seasons = sorted({str(r.get("footystats_season_id") or "").strip()
                                 for r in settlement_register if r.get("footystats_season_id")})

    run56_ingested = [r for r in archive_evidence if str(r.get("run56_ingestion_status") or "").strip() == "INGESTED"]
    current_ingested = [r for r in output if r["run56_archive_status"] == "RUN56_INGESTED_AGGREGATE_ONLY"]
    current_missing = [r for r in output if r["run56_archive_status"] != "RUN56_INGESTED_AGGREGATE_ONLY"]
    current_new = [r for r in output if r["run56_archive_status"] == "NO_LEGACY_SELECTED_SEASON_ID_NEW_CATALOGUE_ENTRY"]
    current_legacy_not_ingested = [r for r in output if r["run56_archive_status"] == "RUN56_NOT_INGESTED_OR_NO_MANIFEST"]
    archive_ids_not_current = sorted(set(archive) - set(legacy_ids))

    total_records = sum(integer(features[sid], "records", f"Run56 feature season {sid}") for sid in ingested_ids)
    total_teams = sum(integer(archive[sid], "team_count", f"Run56 archive season {sid}") for sid in ingested_ids)
    sum_field = lambda field: sum(integer(features[sid], field, f"Run56 feature season {sid}") for sid in ingested_ids)
    summary = {
        "schema_version": "1.0",
        "audit": "FOOTYSTATS_EXISTING_RUN56_ARCHIVE_ID_SCOPE",
        "evidence_scope": "OFFLINE_SANITIZED_AGGREGATES_ONLY",
        "source_row_counts": {
            "current_crosswalk": len(crosswalk), "run56_archive_evidence": len(archive_evidence),
            "run56_feature_coverage": len(feature_coverage), "settlement_register": len(settlement_register),
            "current_historical_plan": len(season_plan),
        },
        "current_catalogue": {
            "league_count": len(crosswalk), "legacy_selected_season_id_overlap_count": len(legacy_ids),
            "new_catalogue_leagues_without_legacy_selected_id": len(current_new),
            "historical_plan_season_count": len(season_plan), "historical_plan_unique_season_ids": len(plan),
            "history_start_date": "2024-01-01", "history_end_date_inclusive": "2026-11-04",
        },
        "run56_archive": {
            "legacy_manifest_rows": len(archive_evidence), "ingested_season_rows": len(run56_ingested),
            "not_ingested_or_no_manifest_rows": len(archive_evidence) - len(run56_ingested),
            "current_catalogue_leagues_with_exact_ingested_selected_id": len(current_ingested),
            "current_catalogue_leagues_without_run56_archive_evidence": len(current_missing),
            "current_catalogue_missing_archive_split": {
                "legacy_selected_id_present_but_not_ingested": len(current_legacy_not_ingested),
                "new_catalogue_league_without_legacy_selected_id": len(current_new),
            },
            "current_leagues_without_run56_archive": [r["provider_league_name"] for r in current_missing],
            "legacy_archive_ids_not_in_current_49_crosswalk": archive_ids_not_current,
            "ingested_archive_ids_all_exactly_match_current_crosswalk_and_plan": True,
            "match_records": total_records, "team_count_sum_across_season_folders": total_teams,
            "team_id_field_complete_rows": sum_field("team_ids_complete"),
            "team_id_field_completeness_pct": round(100 * sum_field("team_ids_complete") / total_records, 2),
            "parseable_kickoff_rows": sum_field("parseable_kickoff"),
            "score_complete_rows": sum_field("score_complete"),
            "explicit_score_pair_rows": sum_field("explicit_score_pairs"),
            "settled_status_allowed_rows": sum_field("settled_status_allowed"),
            "settled_status_allowed_pct": round(100 * sum_field("settled_status_allowed") / total_records, 2),
            "missing_team_names": sum_field("missing_team_names"),
            "fixture_id_values_present_in_sanitized_aggregate": False,
            "team_id_values_present_in_sanitized_aggregate": False,
            "historical_2024_to_2026_coverage_certified": False,
        },
        "settlement_register_sample": {
            "rows": len(settlement_register), "distinct_footystats_fixture_ids": len(set(fs_ids)),
            "distinct_fotmob_fixture_ids": len(set(fm_ids)),
            "distinct_footystats_season_ids": len(settlement_seasons),
            "exact_ordered_team_name_and_utc_kickoff_joins": exact_name_time,
            "home_away_team_id_columns_present": bool(team_id_columns),
            "home_away_team_id_columns": team_id_columns,
            "canonical_bridge_approved_rows": canonical_approved,
            "settlement_truth_verified_rows": settlement_truth,
            "sample_fixture_ids_unique": True, "full_archive_fixture_id_collision_audit_possible": False,
        },
        "identity_assessment": {
            "cross_season_fixture_id_stability_assessed": False,
            "cross_season_team_id_stability_assessed": False,
            "exact_team_id_values_available": False,
            "exact_fixture_id_values_available_for_run56_archive": False,
            "reason": "Run56 evidence is aggregate-only. The separate settlement register has fixture IDs but no home/away team IDs and joins by ordered team names plus UTC kickoff; it is not a full archive extract.",
            "team_id_field_completeness_is_not_team_id_identity_stability": True,
            "settled_status_allowed_is_not_official_settlement_truth": True,
        },
        "governance": {
            "production_eligible": False, "betting_eligible": False,
            "production_logic_changed": False, "provider_api_calls_made": 0,
            "raw_provider_payloads_written": False, "private_repository_accessed": False,
        },
    }
    return output, summary

def main():
    rows = {name: read_csv(path) for name, path in INPUTS.items()}
    expected = {"crosswalk": 49, "archive_evidence": 50, "feature_coverage": 31,
                "settlement_register": 10, "season_plan": 182}
    for name, count in expected.items():
        if len(rows[name]) != count:
            raise SystemExit(f"Expected {count} rows in {name}; found {len(rows[name])}. Source snapshot changed.")
    coverage, summary = build_audit(rows["crosswalk"], rows["archive_evidence"],
                                    rows["feature_coverage"], rows["settlement_register"], rows["season_plan"])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_DIR / "current-49-run56-archive-scope.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COVERAGE_FIELDS)
        writer.writeheader()
        writer.writerows(coverage)
    (OUTPUT_DIR / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "current_leagues": summary["current_catalogue"]["league_count"],
        "run56_ingested_current_leagues": summary["run56_archive"]["current_catalogue_leagues_with_exact_ingested_selected_id"],
        "current_leagues_without_run56_archive": summary["run56_archive"]["current_catalogue_leagues_without_run56_archive_evidence"],
        "run56_match_records": summary["run56_archive"]["match_records"],
        "team_id_values_available": summary["identity_assessment"]["exact_team_id_values_available"],
        "fixture_id_values_available_for_run56": summary["identity_assessment"]["exact_fixture_id_values_available_for_run56_archive"],
        "production_eligible": False, "betting_eligible": False,
    }, indent=2))

if __name__ == "__main__":
    main()
