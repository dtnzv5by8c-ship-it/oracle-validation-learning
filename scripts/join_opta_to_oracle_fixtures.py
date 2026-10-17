#!/usr/bin/env python3
"""Exact-name, report-only join of Opta Power Rankings to Oracle upcoming fixtures."""
import csv, json, re, sys, unicodedata
from datetime import datetime, timezone
from pathlib import Path

def norm(value):
    value = unicodedata.normalize("NFKD", str(value or "").casefold()).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", value)

def slug(value):
    return norm(value)

def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: join_opta_to_oracle_fixtures.py <fixture_csv> <opta_mens_csv>")
    fixtures_path, rankings_path = map(Path, sys.argv[1:])
    with fixtures_path.open(encoding="utf-8-sig", newline="") as f:
        fixtures = list(csv.DictReader(f))
    with rankings_path.open(encoding="utf-8-sig", newline="") as f:
        rankings = list(csv.DictReader(f))
    required = {"home_team", "away_team", "date", "league_code"}
    if fixtures and not required.issubset(fixtures[0]):
        raise ValueError("Fixture file lacks required identity/date columns")
    lookup = {}
    for row in rankings:
        lookup.setdefault(norm(row.get("contestantName")), []).append(row)
    retrieved = datetime.now(timezone.utc).isoformat()
    output = []
    for fixture in fixtures:
        row = dict(fixture)
        # Oracle's scheduled fixture identity convention, used only when source CSV lacks fixture_id.
        if not row.get("fixture_id"):
            row["fixture_id"] = "SCHED-" + str(fixture.get("league_code", "")).upper() + "-" + str(fixture.get("date", "")) + "-" + slug(fixture.get("home_team", "")) + "-" + slug(fixture.get("away_team", ""))
        matched = {}
        for side in ("home", "away"):
            name = fixture.get(side + "_team", "")
            candidates = lookup.get(norm(name), [])
            item = candidates[0] if len(candidates) == 1 else None
            status = "MATCHED_EXACT_NORMALIZED" if item else (
                "AMBIGUOUS_OPTA_TEAM_NAME" if len(candidates) > 1 else "NO_EXACT_OPTA_MATCH")
            matched[side] = item
            row[f"opta_{side}_match_status"] = status
            row[f"opta_{side}_rating"] = item.get("currentRating") if item else ""
            row[f"opta_{side}_global_rank"] = item.get("currentGlobalRank") or (item.get("rank") if item else "") if item else ""
            row[f"opta_{side}_league"] = item.get("league", "") if item else ""
            row[f"opta_{side}_country"] = item.get("country", "") if item else ""
        try:
            h = float(matched["home"]["currentRating"])
            a = float(matched["away"]["currentRating"])
            row["opta_home_minus_away_rating"] = round(h-a, 6)
        except (TypeError, ValueError, KeyError):
            row["opta_home_minus_away_rating"] = ""
        row["opta_source"] = "Opta Analyst Power Rankings"
        row["opta_retrieved_utc"] = retrieved
        row["opta_data_as_of"] = "retrieval time; source ranking publication timestamp not provided in payload"
        output.append(row)
    out = Path("artifacts/opta_power_rankings")
    out.mkdir(parents=True, exist_ok=True)
    out_csv = out / "oracle_fixture_opta_ratings.csv"
    fields = list(dict.fromkeys(k for row in output for k in row))
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
    home = sum(r["opta_home_match_status"] == "MATCHED_EXACT_NORMALIZED" for r in output)
    away = sum(r["opta_away_match_status"] == "MATCHED_EXACT_NORMALIZED" for r in output)
    both = sum(r["opta_home_match_status"] == "MATCHED_EXACT_NORMALIZED" and r["opta_away_match_status"] == "MATCHED_EXACT_NORMALIZED" for r in output)
    league_coverage = {}
    for r in output:
        item = league_coverage.setdefault(r.get("league_code", "UNKNOWN"), {"fixtures": 0, "both_teams_matched": 0})
        item["fixtures"] += 1
        item["both_teams_matched"] += int(r["opta_home_match_status"] == "MATCHED_EXACT_NORMALIZED" and r["opta_away_match_status"] == "MATCHED_EXACT_NORMALIZED")
    manifest = {
        "artifact": "ORACLE-OPTA-FIXTURE-ENRICHMENT-V1",
        "generated_utc": retrieved,
        "status": "PASS" if output else "EMPTY_FIXTURE_INPUT",
        "mode": "REPORT_ONLY_NOT_PRODUCTION_INPUT",
        "fixture_count": len(output),
        "opta_ranking_rows": len(rankings),
        "home_team_exact_match_count": home,
        "away_team_exact_match_count": away,
        "fixtures_with_both_teams_matched": both,
        "both_team_fixture_coverage": both / len(output) if output else 0,
        "coverage_by_league_code": league_coverage,
        "matching_policy": "Exact normalized team-name match only; ambiguous and unmatched teams remain unavailable. Missing fixture_id is generated using Oracle SCHED-{league_code}-{date}-{home_slug}-{away_slug} convention; no fuzzy aliases.",
        "rating_field": "currentRating as published by Opta Analyst; rank is not converted to rating.",
        "source": "https://dataviz.theanalyst.com/opta-power-rankings/index.js",
        "limitations": [
            "Current rating is the latest value retrieved; the public payload did not expose a publication timestamp.",
            "Public data retrieval is not evidence of an official bulk API entitlement; use subject to source terms.",
            "This is reporting-only. Oracle probabilities, model logic, calibration, thresholds and locked report schema are unchanged."
        ],
        "output_csv": str(out_csv)
    }
    (out / "fixture_join_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
