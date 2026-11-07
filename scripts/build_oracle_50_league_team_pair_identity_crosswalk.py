#!/usr/bin/env python3
"""Build a fail-closed 50-league fixture identity crosswalk.

Identity hierarchy:
1. governed OpenFoot competition identity;
2. exact existing Oracle internal identity where already proven;
3. otherwise canonical team-pair identity anchored to the governed competition.

Team names are corroborating identity evidence, not a reason to invent an internal
production league code. Unmapped/conflicted namespaces remain fail-closed.
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "artifacts/oracle_50_league_live_fixture_source_validation.json"
BRIDGE = ROOT / "data/prospective/oracle_50_league_internal_identity_bridge_research.csv"
OUT = ROOT / "data/prospective/oracle_50_league_team_pair_identity_crosswalk.csv"

def main():
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
    with BRIDGE.open(newline="", encoding="utf-8") as f:
        bridge = {r["governed_code"]: r for r in csv.DictReader(f)}

    fields = [
        "match_id","kickoff_at","governed_code","governed_name",
        "home_team","away_team","source_identity","internal_oracle_code",
        "identity_status","production_admission"
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for league in validation["leagues"]:
            b = bridge.get(league["source_code"], {})
            exact = b.get("mapping_status") == "EVIDENCE_EXACT_UNIQUE"
            for fixture in league.get("fixtures", []):
                w.writerow({
                    "match_id": fixture["match_id"],
                    "kickoff_at": fixture["kickoff_at"],
                    "governed_code": league["source_code"],
                    "governed_name": league["league"],
                    "home_team": fixture["home"],
                    "away_team": fixture["away"],
                    "source_identity": f'OpenFoot:{league["competition_id"]}',
                    "internal_oracle_code": b.get("internal_oracle_code", ""),
                    "identity_status": (
                        "SOURCE_PLUS_EXISTING_INTERNAL_IDENTITY"
                        if exact else "SOURCE_PLUS_TEAM_PAIR_IDENTITY"
                    ),
                    "production_admission": (
                        "PENDING_FEATURE_AND_MODEL_GATES"
                        if exact else "FAIL_CLOSED"
                    ),
                })
                count += 1
    print(f"wrote {count} fixture identity rows to {OUT}")

if __name__ == "__main__":
    main()
