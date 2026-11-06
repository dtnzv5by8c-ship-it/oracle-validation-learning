#!/usr/bin/env python3
"""Fail-closed offline contract for the Master OMI feature join spine.

This contract validates reporting completeness only. It never calls providers,
recalculates Oracle probabilities, or changes Oracle V1.6 logic.
"""
from __future__ import annotations
import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

FEATURE_FIELDS = (
    "recent_form_status","h2h_status","league_position_status","xg_goals_status",
    "btts_status","win_draw_probability_status","fixture_team_ids_status",
    "pagination_status","chronology_status","freshness_status",
)
IDENTITY_FIELDS = (
    "fixture_id","league_id","provider_league_id","provider_season_id",
    "home_team_id","away_team_id","kickoff_utc",
)
ACTUAL_FIELDS = ("actual_home_goals","actual_away_goals","actual_result")
VALID_RESULTS = {"HOME","DRAW","AWAY"}

def present(v):
    return v is not None and str(v).strip() != ""

def truth(v):
    return str(v).strip().upper() in {"1","TRUE","PASS","READY","YES","OK"}

def parse_nonnegative_int(v):
    try:
        n = int(str(v).strip())
        return n if n >= 0 else None
    except (TypeError, ValueError):
        return None

def validate_kickoff(v):
    try:
        dt = datetime.fromisoformat(str(v).strip().replace("Z","+00:00"))
        return dt.tzinfo is not None
    except (TypeError, ValueError):
        return False

def validate(rows, expected_leagues=60, require_complete=False):
    errors = []
    if not rows:
        return ["empty_master_omi"]
    headers = set(rows[0])
    required = IDENTITY_FIELDS + FEATURE_FIELDS + ACTUAL_FIELDS
    missing = [x for x in required if x not in headers]
    if missing:
        return ["missing_headers:" + ",".join(missing)]
    ids = [str(r.get("fixture_id","")).strip() for r in rows]
    if any(not x for x in ids):
        errors.append("blank_fixture_id")
    if len(ids) != len(set(ids)):
        errors.append("duplicate_fixture_id")
    leagues = {str(r.get("league_id","")).strip() for r in rows if present(r.get("league_id"))}
    if len(leagues) > expected_leagues:
        errors.append(f"league_count_exceeds_{expected_leagues}")
    if require_complete and len(leagues) != expected_leagues:
        errors.append(f"league_count_incomplete:{len(leagues)}/{expected_leagues}")
    for i, r in enumerate(rows, 1):
        for f in IDENTITY_FIELDS:
            if not present(r.get(f)):
                errors.append(f"row{i}:missing_identity:{f}")
        if present(r.get("kickoff_utc")) and not validate_kickoff(r.get("kickoff_utc")):
            errors.append(f"row{i}:invalid_kickoff_utc")
        failed = [f for f in FEATURE_FIELDS if not truth(r.get(f))]
        if failed:
            errors.append(f"row{i}:feature_not_ready:{','.join(failed)}")
        if any(not present(r.get(f)) for f in ACTUAL_FIELDS):
            errors.append(f"row{i}:missing_actual_result")
            continue
        hg = parse_nonnegative_int(r.get("actual_home_goals"))
        ag = parse_nonnegative_int(r.get("actual_away_goals"))
        if hg is None:
            errors.append(f"row{i}:invalid_actual_home_goals")
        if ag is None:
            errors.append(f"row{i}:invalid_actual_away_goals")
        result = str(r.get("actual_result","")).strip().upper()
        if result not in VALID_RESULTS:
            errors.append(f"row{i}:invalid_actual_result")
        elif hg is not None and ag is not None:
            expected = "HOME" if hg > ag else "AWAY" if ag > hg else "DRAW"
            if result != expected:
                errors.append(f"row{i}:actual_result_score_mismatch")
    return errors

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--expected-leagues", type=int, default=60)
    ap.add_argument("--require-complete", action="store_true")
    a = ap.parse_args()
    with open(a.input, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    errors = validate(rows, a.expected_leagues, a.require_complete)
    result = {
        "status": "PASS" if not errors else "BLOCK",
        "rows": len(rows),
        "errors": errors,
        "required_feature_families": [
            "recent_form","h2h","league_position","xg_goals","btts","win_draw_probability"
        ],
        "governance": {
            "provider_called": False,
            "oracle_v1_6_modified": False,
            "probabilities_recalculated": False,
            "fail_closed": True,
        },
    }
    Path(a.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not errors else 2)

if __name__ == "__main__":
    main()
