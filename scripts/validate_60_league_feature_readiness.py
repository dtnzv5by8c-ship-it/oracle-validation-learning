#!/usr/bin/env python3
"""Offline 50-league feature-readiness matrix contract.

Consumes only a canonical manifest/readiness CSV. It does not call providers,
calculate Oracle probabilities, or change production logic. A league is READY
only when its 2024-current evidence covers the governed Oracle input families.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

FEATURES = (
    "recent_form","h2h","league_position","xg_goals","btts",
    "win_draw_probability","fixture_team_ids","pagination","chronology","freshness"
)
REQUIRED = ("league_id","league_name","provider_league_id","provider_league_name",
            "provider_season_id","season_start","season_end") + FEATURES

def truth(v: str) -> bool:
    return str(v).strip().upper() in {"1","TRUE","PASS","READY","YES","OK"}


def classify_league(row):
    """Classify a league without admitting incomplete data."""
    identity_ok = all(str(row.get(k, "")).strip() for k in (
        "league_id", "league_name", "provider_league_id", "provider_league_name",
        "provider_season_id", "season_start", "season_end"
    ))
    season_start = str(row.get("season_start", "")).strip()
    season_end = str(row.get("season_end", "")).strip().lower()
    window_ok = season_start[:4] == "2024" and (
        season_end == "current" or season_end[:4].isdigit()
    )
    ready_features = [f for f in FEATURES if truth(row.get(f, ""))]
    if identity_ok and window_ok and len(ready_features) == len(FEATURES):
        status = "READY"
    elif identity_ok and window_ok and ready_features:
        status = "PARTIAL"
    else:
        status = "BLOCKED"
    return {
        "league_id": str(row.get("league_id", "")).strip(),
        "league_name": str(row.get("league_name", "")).strip(),
        "status": status,
        "ready_feature_count": len(ready_features),
        "required_feature_count": len(FEATURES),
        "missing_features": [f for f in FEATURES if f not in ready_features],
    }

def readiness_matrix(rows):
    return [classify_league(r) for r in rows]

def validate(rows, expected_leagues=50):
    errors=[]
    ids=[str(r.get("league_id","")).strip() for r in rows]
    if len(rows)!=expected_leagues:
        errors.append(f"league_count={len(rows)} expected={expected_leagues}")
    if any(not x for x in ids):
        errors.append("blank_league_id")
    if len(set(ids))!=len(ids):
        errors.append("duplicate_league_id")
    provider_ids=[str(r.get("provider_league_id","")).strip() for r in rows]
    if any(not x for x in provider_ids):
        errors.append("blank_provider_league_id")
    if len(set(provider_ids))!=len(provider_ids):
        errors.append("duplicate_provider_league_id")
    season_ids=[str(r.get("provider_season_id","")).strip() for r in rows]
    if any(not x for x in season_ids):
        errors.append("blank_provider_season_id")
    if len(set(season_ids))!=len(season_ids):
        errors.append("duplicate_provider_season_id")
    for i,r in enumerate(rows,1):
        missing=[k for k in REQUIRED if not str(r.get(k,"")).strip()]
        if missing:
            errors.append(f"row{i}:missing_fields:{','.join(missing)}")
        try:
            start=int(str(r.get("season_start",""))[:4])
            end=str(r.get("season_end","")).strip().lower()
            if start != 2024: errors.append(f"row{i}:season_start_must_be_2024")
            if end not in {"current"}:
                end_year=int(end[:4])
                if end_year < start: errors.append(f"row{i}:season_end_before_start")
        except ValueError:
            errors.append(f"row{i}:invalid_season_window")
        failed=[f for f in FEATURES if not truth(r.get(f,""))]
        if failed: errors.append(f"row{i}:feature_not_ready:{','.join(failed)}")
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--matrix",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--expected-leagues",type=int,default=50)
    a=ap.parse_args()
    with open(a.matrix,encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    errors=validate(rows,a.expected_leagues)
    ready=sum(1 for r in rows if all(truth(r.get(f,"")) for f in FEATURES))
    matrix = readiness_matrix(rows)
    status_counts = {s: sum(1 for x in matrix if x["status"] == s) for s in ("READY", "PARTIAL", "BLOCKED")}
    result={"status":"PASS" if not errors else "BLOCK",
            "expected_leagues":a.expected_leagues,"rows":len(rows),
            "fully_ready_leagues":ready,"status_counts":status_counts,
            "readiness_matrix":matrix,"errors":errors,
            "required_features":list(FEATURES),
            "governance":{"provider_called":False,"oracle_v1_6_modified":False,
                          "probabilities_recalculated":False,"fail_closed":True}}
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if not errors else 2)

if __name__=="__main__":
    main()
