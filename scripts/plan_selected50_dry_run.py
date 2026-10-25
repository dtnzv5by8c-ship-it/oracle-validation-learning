#!/usr/bin/env python3
"""Research-only selected-50 planner; performs no network/API calls."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "oracle-footystats-selected-50-season-id-manifest.csv"
EVIDENCE = ROOT / "data" / "run56_selected50_archive_evidence.csv"
COVERAGE = ROOT / "data" / "run56_selected50_archive_feature_coverage.csv"
OUT = ROOT / "audit-output"
OUT.mkdir(exist_ok=True)
MATRIX = OUT / "selected50_dry_run_coverage_matrix.csv"
SUMMARY = OUT / "selected50_dry_run_summary.json"

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

selected = read_csv(MANIFEST)
evidence_rows = read_csv(EVIDENCE)
coverage_rows = read_csv(COVERAGE)
assert len(selected) == 50, f"Expected 50 selected rows; got {len(selected)}"
ids = [r.get("selected_id", "").strip() for r in selected]
assert all(ids), "Blank selected_id"
assert len(set(ids)) == 50, "Duplicate selected_id"
evidence_ids = [r.get("selected_id", "").strip() for r in evidence_rows]
assert len(evidence_ids) == 50, f"Expected 50 evidence rows; got {len(evidence_ids)}"
assert len(set(evidence_ids)) == 50, "Duplicate evidence selected_id"
assert set(ids) == set(evidence_ids), "Evidence IDs do not exactly equal selected manifest IDs"
evidence = {r["selected_id"].strip(): r for r in evidence_rows}
coverage_ids = [r.get("selected_id", "").strip() for r in coverage_rows]
assert len(coverage_ids) == 31, f"Expected 31 exact archive coverage rows; got {len(coverage_ids)}"
assert len(set(coverage_ids)) == 31, "Duplicate archive coverage IDs"
assert set(coverage_ids) == {sid for sid in ids if evidence[sid]["run56_manifest_status"] == "MANIFEST_RECORD_PRESENT"}, "Archive feature coverage IDs do not match manifest-present IDs"
coverage = {r["selected_id"].strip(): r for r in coverage_rows}
matched = sum(evidence[sid]["run56_manifest_status"] == "MANIFEST_RECORD_PRESENT" for sid in ids)
absent = sum(evidence[sid]["run56_manifest_status"] == "NO_MANIFEST_RECORD_IN_RUN56" for sid in ids)
assert matched + absent == 50, "Unexpected or missing evidence status"
assert matched == 31 and absent == 19, f"Unexpected evidence counts: {matched}/{absent}"

with MATRIX.open("w", encoding="utf-8", newline="") as f:
    fields = [
        "selected_id","country","competition_name","run56_manifest_status",
        "run56_ingestion_status","run56_match_count","run56_team_count","run56_matches_pages",
        "run56_tables_status","run56_season_stats_status","archive_season_folder","archive_records",
        "archive_parseable_kickoff","archive_team_ids_complete","archive_settled_status_allowed",
        "archive_score_complete","archive_explicit_score_pairs","archive_event_array_score_pairs",
        "archive_missing_team_names","provider_competition_id","provider_season_id",
        "live_ingestion_status","estimated_minimum_calls","production_eligible"
    ]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in selected:
        sid = r["selected_id"].strip()
        ev = evidence[sid]
        w.writerow({
            "selected_id": sid,
            "country": r.get("country", ""),
            "competition_name": r.get("competition_name", ""),
            "run56_manifest_status": ev["run56_manifest_status"],
            "run56_ingestion_status": ev["run56_ingestion_status"],
            "run56_match_count": ev["match_count"],
            "run56_team_count": ev["team_count"],
            "run56_matches_pages": ev["matches_pages"],
            "run56_tables_status": ev["tables_status"],
            "run56_season_stats_status": ev["season_stats_status"],
            "archive_season_folder": coverage.get(sid, {}).get("season_folder", ""),
            "archive_records": coverage.get(sid, {}).get("records", ""),
            "archive_parseable_kickoff": coverage.get(sid, {}).get("parseable_kickoff", ""),
            "archive_team_ids_complete": coverage.get(sid, {}).get("team_ids_complete", ""),
            "archive_settled_status_allowed": coverage.get(sid, {}).get("settled_status_allowed", ""),
            "archive_score_complete": coverage.get(sid, {}).get("score_complete", ""),
            "archive_explicit_score_pairs": coverage.get(sid, {}).get("explicit_score_pairs", ""),
            "archive_event_array_score_pairs": coverage.get(sid, {}).get("event_array_score_pairs", ""),
            "archive_missing_team_names": coverage.get(sid, {}).get("missing_team_names", ""),
            "provider_competition_id": "",
            "provider_season_id": sid,
            "live_ingestion_status": "NOT_REQUESTED_DRY_RUN_ONLY",
            "estimated_minimum_calls": 4,
            "production_eligible": "NO"
        })
summary = {
    "mode": "DRY_RUN_ONLY",
    "network_calls_made": 0,
    "paid_provider_calls_made": 0,
    "selected_season_ids": len(selected),
    "run56_manifest_records_present": matched,
    "no_run56_manifest_record": absent,
    "exact_archive_coverage_rows": len(coverage_rows),
    "archive_records_across_exact_matched_selected_seasons": sum(int(r["records"]) for r in coverage_rows),
    "archive_score_complete_rows_across_exact_matched_selected_seasons": sum(int(r["score_complete"]) for r in coverage_rows),
    "archive_settled_status_allowed_rows_across_exact_matched_selected_seasons": sum(int(r["settled_status_allowed"]) for r in coverage_rows),
    "archive_rows_with_parseable_kickoff": sum(int(r["parseable_kickoff"]) for r in coverage_rows),
    "archive_rows_with_complete_team_ids": sum(int(r["team_ids_complete"]) for r in coverage_rows),
    "archive_rows_missing_team_names": sum(int(r["missing_team_names"]) for r in coverage_rows),
    "minimum_endpoint_calls_if_live_one_pass": len(selected) * 4,
    "minimum_call_breakdown_per_selected_season": {
        "season_metadata": 1,
        "teams": 1,
        "tables": 1,
        "matches": "at least 1 request; pagination/page count unknown"
    },
    "additional_calls": "Match pagination, retries, catalogue refresh, historical season expansion and validation add calls.",
    "scope_rule": "Selected IDs are season IDs. Parent competition IDs are not inferred.",
    "evidence_source": "Run 56 ingestion_manifest.csv, reconciled by exact selected season ID.",
    "limitation": "No manifest record does not prove a provider request failed or was never attempted; Run 56 ingestion_errors.json was empty.",
    "safety_gate": "Live ingestion requires explicit user approval because it may consume provider credits.",
    "production_eligible": False
}
SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
# Reconcile evidence layers without conflating selected season IDs, parent competition IDs,
# exact Run 56 archive evidence, and the separate multi-season research runtime.
RECONCILIATION = OUT / "selected50_evidence_layer_reconciliation.json"
reconciliation = {
    "status": "RESEARCH_ONLY_EVIDENCE_SCOPE_RECONCILIATION",
    "selected_group_count": len(selected),
    "selected_id_semantics": "Each selected_id is a provider season ID; it is not a parent competition ID.",
    "run56_exact_id_evidence": {
        "manifest_records_present": matched,
        "no_manifest_record": absent,
        "exact_archive_coverage_rows": len(coverage_rows),
        "archive_records": sum(int(r["records"]) for r in coverage_rows),
        "archive_score_complete_rows": sum(int(r["score_complete"]) for r in coverage_rows),
        "archive_settled_status_allowed_rows": sum(int(r["settled_status_allowed"]) for r in coverage_rows),
        "archive_parseable_kickoff_rows": sum(int(r["parseable_kickoff"]) for r in coverage_rows),
        "archive_complete_team_id_rows": sum(int(r["team_ids_complete"]) for r in coverage_rows),
        "archive_rows_missing_team_names": sum(int(r["missing_team_names"]) for r in coverage_rows)
    },
    "identity_findings": {
        "provider_parent_competition_ids_populated_by_this_dry_run": 0,
        "parent_ids_inferred_from_season_ids": False,
        "canonical_fixture_team_join_verified": False,
        "settlement_truth_verified": False
    },
    "scope_warning": "Run 56 counts are exact selected-season-ID matches. The separate multi-season runtime groups historical seasons by exact country/competition labels. Do not add or equate those counts as if they represented the same ID-level population until a canonical parent competition/team/fixture crosswalk is verified.",
    "missing_manifest_warning": "NO_MANIFEST_RECORD_IN_RUN56 means no exact matching manifest row was present in that evidence snapshot; it does not prove the provider request failed or was never attempted.",
    "live_ingestion": {
        "network_calls_made": 0,
        "paid_provider_calls_made": 0,
        "minimum_endpoint_calls_if_one_pass": len(selected) * 4,
        "pagination_and_retries_included": False,
        "requires_separate_explicit_confirmation": True
    },
    "production_eligible": False,
    "decision": "Keep all selected-50 outputs research-only and production-ineligible until canonical IDs, joins, settlement truth, freshness and point-in-time inputs are verified."
}
(RECONCILIATION).write_text(json.dumps(reconciliation, indent=2) + "\n", encoding="utf-8")
print(f"PASS: {len(selected)} selected IDs reconciled against exact Run 56 manifest evidence.")
print(f"Run 56 records present: {matched}; no manifest record: {absent}.")
print("DRY RUN: 0 network calls and 0 paid provider calls.")
print(f"Minimum one-pass live request estimate: {len(selected)*4}, excluding pagination/retries.")
