#!/usr/bin/env python3
"""Exact-name, report-only join of OpenFoot season xG aggregates to Oracle fixtures."""
import csv, json, re, sys, unicodedata
from datetime import datetime, timezone
from pathlib import Path

def norm(value):
    value = unicodedata.normalize("NFKD", str(value or "").casefold()).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", value)

def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: join_openfoot_xg_to_oracle_fixtures.py <fixture_csv> <team_xg_csv>")
    fixtures_path, xg_path = map(Path, sys.argv[1:])
    with fixtures_path.open(encoding="utf-8-sig", newline="") as f:
        fixtures = list(csv.DictReader(f))
    with xg_path.open(encoding="utf-8-sig", newline="") as f:
        xg_rows = list(csv.DictReader(f))
    required = {"league_code", "date", "home_team", "away_team"}
    if fixtures and not required.issubset(fixtures[0]):
        raise ValueError("Fixture schedule lacks required identity/date columns")
    lookup = {}
    for row in xg_rows:
        key = (str(row.get("league_code", "")).upper(), norm(row.get("team_name")))
        lookup.setdefault(key, []).append(row)
    generated = datetime.now(timezone.utc).isoformat()
    output = []
    for fixture in fixtures:
        row = dict(fixture)
        if not row.get("fixture_id"):
            row["fixture_id"] = "SCHED-" + str(fixture.get("league_code", "")).upper() + "-" + str(fixture.get("date", "")) + "-" + norm(fixture.get("home_team")) + "-" + norm(fixture.get("away_team"))
        found = {}
        for side in ("home", "away"):
            team = fixture.get(side + "_team", "")
            candidates = lookup.get((str(fixture.get("league_code", "")).upper(), norm(team)), [])
            item = candidates[0] if len(candidates) == 1 else None
            status = "MATCHED_EXACT_NORMALIZED" if item else (
                "AMBIGUOUS_XG_TEAM_NAME" if len(candidates) > 1 else "NO_XG_TEAM_MATCH")
            found[side] = item
            row[f"{side}_xg_for_season"] = item.get("xg_for_season", "") if item else ""
            row[f"{side}_xg_against_season"] = item.get("xg_against_season", "") if item else ""
            row[f"{side}_xg_difference_season"] = item.get("xg_difference_season", "") if item else ""
            row[f"{side}_xg_matches_played"] = item.get("matches_played", "") if item else ""
            row[f"{side}_xg_status"] = status if item else status
            row[f"{side}_xg_competition"] = item.get("competition_name", "") if item else ""
            row[f"{side}_xg_season"] = item.get("season", "") if item else ""
        try:
            h = float(found["home"]["xg_for_season"])
            a = float(found["away"]["xg_for_season"])
            row["home_minus_away_xg_for_season"] = round(h-a, 4)
        except (TypeError, ValueError, KeyError):
            row["home_minus_away_xg_for_season"] = ""
        row["xg_source"] = "OpenFoot API"
        row["xg_retrieved_utc"] = generated
        row["xg_feature_type"] = "CURRENT_SEASON_AGGREGATE_NOT_LAST_3_OR_LAST_5"
        output.append(row)
    outdir = Path("artifacts/openfoot_xg_probe")
    outdir.mkdir(parents=True, exist_ok=True)
    out_csv = outdir / "oracle_fixture_xg_season_aggregates.csv"
    fields = list(dict.fromkeys(k for row in output for k in row))
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
    both = sum(r["home_xg_status"] == "MATCHED_EXACT_NORMALIZED" and r["away_xg_status"] == "MATCHED_EXACT_NORMALIZED" for r in output)
    by_league = {}
    for r in output:
        item = by_league.setdefault(r.get("league_code", "UNKNOWN"), {"fixtures": 0, "both_teams_xg_matched": 0})
        item["fixtures"] += 1
        item["both_teams_xg_matched"] += int(r["home_xg_status"] == "MATCHED_EXACT_NORMALIZED" and r["away_xg_status"] == "MATCHED_EXACT_NORMALIZED")
    manifest = {
      "artifact": "ORACLE-OPENFOOT-XG-FIXTURE-ENRICHMENT-V1", "status": "PASS" if output else "EMPTY_FIXTURE_INPUT",
      "mode": "REPORT_ONLY_NOT_PRODUCTION_INPUT", "generated_utc": generated,
      "fixture_count": len(output), "fixtures_with_both_teams_xg": both,
      "both_team_fixture_coverage": both/len(output) if output else 0,
      "coverage_by_league_code": by_league,
      "matching_policy": "Exact normalized team name within the same governed league code. No fuzzy matching or goal-based fallback.",
      "feature_definition": "Current-season aggregate xG for, xG against and xG difference. Not last-3/last-5 form.",
      "output_csv": str(out_csv)
    }
    (outdir / "fixture_xg_join_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
