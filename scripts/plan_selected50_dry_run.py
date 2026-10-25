#!/usr/bin/env python3
"""Research-only selected-50 planner. Never makes network/API calls."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "oracle-footystats-selected-50-season-id-manifest.csv"
OUT = ROOT / "audit-output"
OUT.mkdir(exist_ok=True)
MATRIX = OUT / "selected50_dry_run_coverage_matrix.csv"
SUMMARY = OUT / "selected50_dry_run_summary.json"

with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 50, f"Expected 50 selected rows; got {len(rows)}"
ids = [r.get("selected_id", "").strip() for r in rows]
assert all(ids), "Blank selected_id"
assert len(set(ids)) == 50, "Duplicate selected_id"

# Archive evidence is based on the prior Run 56 audit: 31 exact IDs matched, 19 absent.
# Keep status explicit; absent does not mean provider unavailable.
known_matched = {
    "16571","17181","17171","16544","17087","17157","17146","17184","17180",
    "17102","17117","17210","17212","17356","17084","17404","17099","17097",
    "16558","17112","17215","17247","17426","17148","17444","17199","17269",
    "17129","17265","16504","17191"
}
# Only report archive status from prior exact-ID reconciliation; never fuzzy-match.
with MATRIX.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=[
        "selected_id","country","competition_name","archive_exact_id_status",
        "ingestion_manifest_status","provider_competition_id","provider_season_id","live_ingestion_status",
        "match_page_count","estimated_minimum_calls","production_eligible"
    ])
    w.writeheader()
    for r in rows:
        sid = r["selected_id"].strip()
        w.writerow({
            "selected_id": sid,
            "country": r.get("country",""),
            "competition_name": r.get("competition_name",""),
            "archive_exact_id_status": "ARCHIVE_MATCHED" if sid in known_matched else "ARCHIVE_ABSENT_UNVERIFIED",
            "ingestion_manifest_status": "MANIFEST_RECORD_PRESENT" if sid in known_matched else "NO_MANIFEST_RECORD_IN_RUN56",
            "provider_competition_id": "",
            "provider_season_id": sid,
            "live_ingestion_status": "NOT_REQUESTED_DRY_RUN_ONLY",
            "match_page_count": "UNKNOWN_UNTIL_PROVIDER_RESPONSE",
            "estimated_minimum_calls": 4,
            "production_eligible": "NO"
        })
summary = {
    "mode": "DRY_RUN_ONLY",
    "network_calls_made": 0,
    "paid_provider_calls_made": 0,
    "selected_season_ids": len(rows),
    "archive_exact_id_matches_from_prior_audit": len(known_matched),
    "archive_ids_absent_unverified": len(rows)-len(known_matched),
    "minimum_endpoint_calls_if_live_one_pass": len(rows)*4,
    "minimum_call_breakdown_per_selected_season": {
        "season_metadata": 1,
        "teams": 1,
        "tables": 1,
        "matches": "at least 1 request; pagination/page count unknown"
    },
    "additional_calls": "Any match pagination, retries, multi-year history, catalogue refresh or verification adds calls; not estimated without provider response/config.",
    "scope_rule": "The 50 manifest IDs are treated as season IDs; competition IDs remain unresolved and are not inferred.",
    "safety_gate": "Live ingestion requires explicit user approval because it may consume provider credits.",
    "production_eligible": False
}
SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print("PASS: selected-50 dry-run plan generated; 50 IDs; 0 network calls.")
print(f"Minimum one-pass live request estimate: {len(rows)*4} calls, excluding pagination/retries.")
