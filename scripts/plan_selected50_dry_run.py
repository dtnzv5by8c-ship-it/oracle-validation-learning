#!/usr/bin/env python3
"""Research-only selected-50 planner; performs no network/API calls."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "oracle-footystats-selected-50-season-id-manifest.csv"
EVIDENCE = ROOT / "data" / "run56_selected50_archive_evidence.csv"
OUT = ROOT / "audit-output"
OUT.mkdir(exist_ok=True)
MATRIX = OUT / "selected50_dry_run_coverage_matrix.csv"
SUMMARY = OUT / "selected50_dry_run_summary.json"

def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

selected = read_csv(MANIFEST)
evidence_rows = read_csv(EVIDENCE)
assert len(selected) == 50, f"Expected 50 selected rows; got {len(selected)}"
ids = [r.get("selected_id", "").strip() for r in selected]
assert all(ids), "Blank selected_id"
assert len(set(ids)) == 50, "Duplicate selected_id"
evidence_ids = [r.get("selected_id", "").strip() for r in evidence_rows]
assert len(evidence_ids) == 50, f"Expected 50 evidence rows; got {len(evidence_ids)}"
assert len(set(evidence_ids)) == 50, "Duplicate evidence selected_id"
assert set(ids) == set(evidence_ids), "Evidence IDs do not exactly equal selected manifest IDs"
evidence = {r["selected_id"].strip(): r for r in evidence_rows}
matched = sum(evidence[sid]["run56_manifest_status"] == "MANIFEST_RECORD_PRESENT" for sid in ids)
absent = sum(evidence[sid]["run56_manifest_status"] == "NO_MANIFEST_RECORD_IN_RUN56" for sid in ids)
assert matched + absent == 50, "Unexpected or missing evidence status"
assert matched == 31 and absent == 19, f"Unexpected evidence counts: {matched}/{absent}"

with MATRIX.open("w", encoding="utf-8", newline="") as f:
    fields = [
        "selected_id","country","competition_name","run56_manifest_status",
        "run56_ingestion_status","run56_match_count","run56_team_count","run56_matches_pages",
        "run56_tables_status","run56_season_stats_status","provider_competition_id",
        "provider_season_id","live_ingestion_status","estimated_minimum_calls",
        "production_eligible"
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
print(f"PASS: {len(selected)} selected IDs reconciled against exact Run 56 manifest evidence.")
print(f"Run 56 records present: {matched}; no manifest record: {absent}.")
print("DRY RUN: 0 network calls and 0 paid provider calls.")
print(f"Minimum one-pass live request estimate: {len(selected)*4}, excluding pagination/retries.")
