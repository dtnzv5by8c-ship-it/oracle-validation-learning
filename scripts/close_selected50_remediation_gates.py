#!/usr/bin/env python3
"""Close-out diagnostics for the selected-50 Oracle research gates; no API calls or production writes."""
import csv, json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "reports/oracle-selected50-footystats-identity-crosswalk-probe-2026-10-29.csv"
CONFIG = ROOT / "data/oracle-footystats-selected-50-season-id-manifest.csv"
OUT = ROOT / "audit-output"
OUT.mkdir(exist_ok=True)

# These are exact Oracle source keys visible in the production repository config.
# A source key is not asserted to be a global canonical competition ID.
KNOWN_ORACLE_CODES = {
    ("England","Premier League"): ("E0","FOOTBALL_DATA_CODE"),
    ("England","Championship"): ("E1","FOOTBALL_DATA_CODE"),
    ("England","EFL League One"): ("E2","FOOTBALL_DATA_CODE"),
    ("France","Ligue 1"): ("F1","FOOTBALL_DATA_CODE"),
    ("France","Ligue 2"): ("F2","FOOTBALL_DATA_CODE"),
    ("Germany","Bundesliga"): ("D1","FOOTBALL_DATA_CODE"),
    ("Germany","2. Bundesliga"): ("D2","FOOTBALL_DATA_CODE"),
    ("Italy","Serie A"): ("I1","FOOTBALL_DATA_CODE"),
    ("Italy","Serie B"): ("I2","FOOTBALL_DATA_CODE"),
    ("Netherlands","Eredivisie"): ("N1","FOOTBALL_DATA_CODE"),
    ("Portugal","LigaPro"): ("POR2","FUTPYTHONTRADER_CODE"),
    ("Turkey","Süper Lig"): ("T1","FOOTBALL_DATA_CODE"),
    ("Belgium","Pro League"): ("B1","FOOTBALL_DATA_CODE"),
    ("Scotland","Premiership"): ("SC0","FOOTBALL_DATA_CODE"),
    ("Austria","Bundesliga"): ("AUT","ORACLE_CONFIG_CODE"),
    ("Switzerland","Super League"): ("SWZ","ORACLE_CONFIG_CODE"),
    ("Poland","Ekstraklasa"): ("POL","ORACLE_CONFIG_CODE"),
    ("Czech Republic","First League"): ("CZE","ORACLE_CONFIG_CODE"),
    ("Croatia","Prva HNL"): ("CRO","FUTPYTHONTRADER_CODE"),
    ("South Africa","Premier Soccer League"): ("RSA","ORACLE_CONFIG_CODE"),
    ("Spain","La Liga"): ("SP1","FOOTBALL_DATA_CODE"),
    ("Spain","Segunda División"): ("SP2","FOOTBALL_DATA_CODE"),
    ("Romania","Liga I"): ("ROU","ORACLE_CONFIG_CODE"),
    ("Ukraine","Ukrainian Premier League"): ("UKR","FUTPYTHONTRADER_CODE"),
    ("Serbia","SuperLiga"): ("SRB","FUTPYTHONTRADER_CODE"),
    ("Greece","Super League"): ("G1","FOOTBALL_DATA_CODE"),
}

def read_csv(p):
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

if not CROSSWALK.exists():
    raise SystemExit("STOP: verified FootyStats crosswalk input missing.")
source = read_csv(CROSSWALK)
if len(source) != 50 or len({r["selected_season_id"] for r in source}) != 50:
    raise SystemExit("STOP: expected exactly 50 unique selected season rows.")

identity = []
for r in source:
    key = (r["country"], r["competition"])
    if key in KNOWN_ORACLE_CODES:
        code, namespace = KNOWN_ORACLE_CODES[key]
        status = "VERIFIED_ORACLE_SOURCE_CODE_NOT_GLOBAL_CANONICAL"
        note = "Exact country/name match to a code in Oracle data_config; namespace retained; provider ID not substituted."
    else:
        code, namespace = "", ""
        status = "PROVIDER_ONLY_UNMAPPED"
        note = "No exact source-code mapping in inspected Oracle config; do not guess or fuzzy-promote."
    identity.append({
        "selected_season_id": r["selected_season_id"],
        "country": r["country"], "competition": r["competition"],
        "footystats_comp_master_id": r["comp_master_id"],
        "oracle_source_code": code, "oracle_code_namespace": namespace,
        "identity_status": status, "production_eligible": "NO",
        "evidence": "reports/oracle-selected50-footystats-identity-crosswalk-probe-2026-10-29.csv",
        "note": note
    })
with (OUT / "selected50_identity_terminal_status.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(identity[0])); w.writeheader(); w.writerows(identity)

# Governance documents define Combo as Double Chance + Under 4.5 (0-4 total goals).
# This is a specification gate only: do not mutate frozen probabilities or assert official settlements.
combo = {
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "market_definition": "Double Chance outcome is true AND total_goals <= 4",
    "equivalent_total_goal_range": "0-4 inclusive",
    "conflicting_legacy_definition": "Double Chance outcome is true AND total_goals in 2-4 inclusive",
    "resolution": "Use the documented DC + Under 4.5 definition for a separately labelled research diagnostic; do not rewrite frozen predictions.",
    "settlement_eligibility": "Only explicit finished/complete status plus valid final home/away score and source provenance; never settle non-finished rows merely because numeric scores exist.",
    "official_settlement_truth": "UNVERIFIED",
    "production_eligible": False,
    "required_next_computation": "Recompute research-only outcome labels from authoritative finished fixtures; compare against predictor and prior ledger; retain discrepancy report."
}
(OUT / "selected50_combo_definition_gate.json").write_text(json.dumps(combo,indent=2)+"\n",encoding="utf-8")

# PIT policy is executable policy metadata; no field is approved merely by its name.
pit = {
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "policy": "Include historical feature only when immutable source evidence provides observed_at < kickoff_at.",
    "allowed_only_with_evidence": ["recent form", "standings", "xG", "odds", "injuries/availability"],
    "excluded_without_evidence": ["actual/post-match xG", "standings without as-of timestamp", "odds without capture timestamp", "any feature with missing observation timestamp"],
    "imputation": "PROHIBITED_FOR_REQUIRED_FEATURES",
    "minimum_recent_form": 5,
    "production_eligible": False,
    "current_selected50_fixture_rows": 435,
    "current_rows_missing_required_features": 24,
    "current_missing_feature_rows_action": "KEEP_BLOCKED_UNTIL_REAL_FEATURES_ARE_VERIFIED"
}
(OUT / "selected50_point_in_time_policy_gate.json").write_text(json.dumps(pit,indent=2)+"\n",encoding="utf-8")

# Consolidated matrix: explicit per-league status, per-market status remains blocked until fixture/feature truth passes.
matrix=[]
for r in identity:
    matrix.append({
        "selected_season_id": r["selected_season_id"], "country": r["country"], "competition": r["competition"],
        "identity_status": r["identity_status"], "oracle_source_code": r["oracle_source_code"],
        "fixture_team_join": "BLOCKED_NOT_VERIFIED",
        "freshness": "BLOCKED_UNTIL_CURRENT_SNAPSHOT_QA",
        "recent_form": "BLOCKED_IF_LESS_THAN_5_PRIOR_MATCHES_OR_MISSING",
        "standings_as_of_kickoff": "BLOCKED_NO_PROVEN_AS_OF_SNAPSHOT",
        "xg_point_in_time": "BLOCKED_NO_PROVEN_AS_OF_SNAPSHOT",
        "odds_point_in_time": "BLOCKED_NO_PROVEN_CAPTURE_TIMESTAMP",
        "settlement_truth": "BLOCKED_OFFICIAL_TRUTH_UNVERIFIED",
        "btts_yes": "NOT_APPROVED",
        "double_chance": "NOT_APPROVED",
        "dc_under_4_5": "NOT_APPROVED",
        "m1up": "NOT_APPROVED",
        "production_eligible": "NO"
    })
with (OUT / "selected50_terminal_readiness_matrix.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(matrix[0])); w.writeheader(); w.writerows(matrix)
summary={
    "status":"PASS_TERMINAL_STATUS_FILES_CREATED_RESEARCH_ONLY",
    "selected_leagues":50,
    "mapped_to_existing_oracle_source_code":sum(1 for r in identity if r["oracle_source_code"]),
    "provider_only_unmapped":sum(1 for r in identity if not r["oracle_source_code"]),
    "official_settlement_truth":"UNVERIFIED",
    "combo_definition":"DC_AND_TOTAL_GOALS_0_TO_4_INCLUSIVE",
    "point_in_time_provenance":"NOT_VERIFIED; features without proof excluded",
    "production_eligible":False,
    "production_changes":0,
    "api_calls":0,
    "note":"This closes inventory/status ambiguity, not all underlying evidence gates. Do not treat any league/market as production-ready."
}
(OUT / "selected50_terminal_readiness_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
