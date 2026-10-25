#!/usr/bin/env python3
"""Emit conservative research-only market readiness gates for selected-50 scope."""
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MATRIX=ROOT/"audit-output"/"selected50_dry_run_coverage_matrix.csv"
OUT=ROOT/"audit-output"
with MATRIX.open(encoding="utf-8",newline="") as f:
    rows=list(csv.DictReader(f))
assert len(rows)==50 and len({r["selected_id"] for r in rows})==50
fields=[
 "selected_id","country","competition_name","archive_status",
 "fixture_join_gate","freshness_gate","point_in_time_xg_gate","point_in_time_odds_gate",
 "btts_yes_gate","double_chance_gate","dc_under_4_5_gate","m1up_gate",
 "production_eligible","gate_reason"
]
with (OUT/"selected50_market_readiness_gates.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for r in rows:
        matched=r["run56_manifest_status"]=="MANIFEST_RECORD_PRESENT"
        archive_status="ARCHIVE_EXACT_ID_PRESENT" if matched else "NO_EXACT_ARCHIVE_ID"
        reason=("Archive row exists, but selected-50 current fixture joins, freshness and point-in-time xG/odds provenance are not verified."
                if matched else "No exact selected season record in Run 56 archive; coverage is unverified.")
        w.writerow({
          "selected_id":r["selected_id"],"country":r["country"],"competition_name":r["competition_name"],
          "archive_status":archive_status,
          "fixture_join_gate":"BLOCKED_NOT_VERIFIED",
          "freshness_gate":"BLOCKED_STALE_SOURCE_EVIDENCE",
          "point_in_time_xg_gate":"BLOCKED_NO_VERIFIED_AS_OF_PROVENANCE",
          "point_in_time_odds_gate":"BLOCKED_NO_VERIFIED_AS_OF_PROVENANCE",
          "btts_yes_gate":"NOT_VERIFIED",
          "double_chance_gate":"NOT_VERIFIED",
          "dc_under_4_5_gate":"NOT_VERIFIED",
          "m1up_gate":"BLOCKED_STALE_EVENT_TRUTH_AND_MISSING_SELECTED50_JOINS",
          "production_eligible":"NO",
          "gate_reason":reason
        })
summary={
 "selected_leagues":50,
 "all_production_eligible":False,
 "all_fixture_join_gates_blocked":True,
 "all_point_in_time_xg_gates_blocked":True,
 "all_point_in_time_odds_gates_blocked":True,
 "btts_yes":"NOT_VERIFIED",
 "double_chance":"NOT_VERIFIED",
 "dc_under_4_5":"NOT_VERIFIED",
 "m1up":"BLOCKED",
 "live_api_calls_made":0,
 "rule":"No market can be marked ready without exact fixture/team joins, freshness checks and point-in-time source provenance.",
 "note":"This is a conservative gate report, not a model prediction or production approval."
}
(OUT/"selected50_market_readiness_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print("PASS: 50 selected leagues evaluated; no market or league marked production-ready.")
