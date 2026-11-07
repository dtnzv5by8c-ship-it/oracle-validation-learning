#!/usr/bin/env python3
"""Deterministically reconcile the live 50-league source-validation board.

Research/control-plane only. This does not change Oracle production code or
promote any league/market. It verifies that the live validation artifact
preserves all 50 governed identities and produces a compact board for the
next controlled downstream-scope decision.
"""
import csv, json, sys
from pathlib import Path

REGISTRY = Path("data/prospective/oracle_50_league_fixture_source_registry.csv")
VALIDATION = Path("artifacts/oracle_50_league_live_fixture_source_validation.json")
OUT = Path("artifacts/oracle_50_league_fixture_source_reconciliation.json")

def main():
    if not REGISTRY.exists() or not VALIDATION.exists():
        print("BLOCKED: registry or live validation artifact missing")
        return 2

    with REGISTRY.open(encoding="utf-8", newline="") as f:
        registry = list(csv.DictReader(f))
    report = json.loads(VALIDATION.read_text(encoding="utf-8"))
    leagues = report.get("leagues", [])

    reg_ids = [r["footystats_league_id"] for r in registry]
    live_ids = [r.get("footystats_league_id") for r in leagues]
    reg_set, live_set = set(reg_ids), set(live_ids)

    duplicates = sorted({x for x in live_ids if live_ids.count(x) > 1})
    missing = sorted(reg_set - live_set)
    unexpected = sorted(live_set - reg_set)

    board = []
    for r in registry:
        matches = [x for x in leagues if x.get("footystats_league_id") == r["footystats_league_id"]]
        x = matches[0] if matches else None
        board.append({
            "ordinal": r["ordinal"],
            "footystats_league_id": r["footystats_league_id"],
            "league": r["governed_league_name"],
            "source_code": r["source_code"],
            "competition_id": r["openfoot_competition_id"],
            "catalog_season": r["openfoot_catalog_season"],
            "catalog_status": r["source_resolution_status"],
            "classification": x.get("classification") if x else "MISSING_VALIDATION_ROW",
            "fixture_count_in_window": x.get("fixture_count_in_window", 0) if x else 0,
            "reason": x.get("reason") if x else "MISSING_VALIDATION_ROW",
        })

    summary = {}
    for row in board:
        summary[row["classification"]] = summary.get(row["classification"], 0) + 1

    scope_passed = (
        len(registry) == 50
        and len(reg_set) == 50
        and len(leagues) == 50
        and len(live_set) == 50
        and not missing
        and not unexpected
        and not duplicates
    )

    output = {
        "status": "PASS" if scope_passed else "BLOCKED",
        "mode": "READ_ONLY_50_LEAGUE_FIXTURE_SOURCE_RECONCILIATION",
        "governed_leagues": 50,
        "registry_rows": len(registry),
        "validation_rows": len(leagues),
        "missing_league_ids": missing,
        "unexpected_league_ids": unexpected,
        "duplicate_league_ids": duplicates,
        "classification_counts": summary,
        "fixtures_in_window": sum(int(x["fixture_count_in_window"] or 0) for x in board),
        "production_model_changed": False,
        "production_eligible": False,
        "betting_eligible": False,
        "board": board,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": output["status"],
        "classification_counts": summary,
        "fixtures_in_window": output["fixtures_in_window"],
        "missing": missing,
        "unexpected": unexpected,
        "duplicates": duplicates,
        "output": str(OUT),
    }, ensure_ascii=False))
    return 0 if scope_passed else 1

if __name__ == "__main__":
    sys.exit(main())
