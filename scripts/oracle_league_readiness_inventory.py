#!/usr/bin/env python3
"""Research-only Oracle league and fixture readiness inventory; no predictions or provider calls."""
import csv
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from dateutil.parser import parse as parse_datetime

ROOT = Path(os.environ.get("ORACLE_INPUT_DIR", "oracle-input"))
OUT = Path(os.environ.get("ORACLE_OUTPUT_DIR", "oracle-readiness-output"))
OUT.mkdir(parents=True, exist_ok=True)

def load_json(name):
    with (ROOT / name).open(encoding="utf-8") as f:
        return json.load(f)

def load_csv(name):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

registry = load_json("oracle_major_league_registry_v1.json")
memory = load_json("ORACLE_BTTS_YES_MEMORY_PACK.json")
fixtures = load_csv("oracle_upcoming_fixtures.csv")
now = datetime.now(timezone.utc)
today = now.date().isoformat()

def fixture_kickoff(row):
    raw_date = (row.get("date") or "").strip()
    raw_time = (row.get("kickoff_time") or "").strip()
    if not raw_date:
        return None
    try:
        parsed = parse_datetime(f"{raw_date}T{raw_time}" if raw_time else raw_date)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (ValueError, TypeError, OverflowError):
        return None

valid_kickoffs = [(row, fixture_kickoff(row)) for row in fixtures]
future_fixture_count = sum(1 for _, dt in valid_kickoffs if dt is not None and dt > now)
unparseable_kickoff_count = sum(1 for _, dt in valid_kickoffs if dt is None)
latest_fixture_kickoff = max((dt for _, dt in valid_kickoffs if dt is not None), default=None)
source_columns = set(fixtures[0].keys()) if fixtures else set()
provenance_columns = {"source_name", "source_match_id", "source_match_slug", "source_competition_id", "source_home_team_id", "source_away_team_id", "source_retrieved_utc", "source_record_sha256"}
missing_provenance_columns = sorted(provenance_columns - source_columns)

leagues = registry.get("leagues", [])
readiness_counts = Counter(str(x.get("readiness", "UNKNOWN")) for x in leagues)
fixture_counts = Counter((x.get("league_code") or "").strip() for x in fixtures)

rows = []
for league in leagues:
    code = league.get("id", "")
    count = fixture_counts.get(code, 0)
    future_for_league = any((x.get("league_code") or "").strip() == code and dt is not None and dt > now for x, dt in valid_kickoffs)
    rows.append({
        "canonical_league_id": code,
        "competition": league.get("competition", ""),
        "country": league.get("country", ""),
        "wave": league.get("wave", ""),
        "registry_readiness": league.get("readiness", "UNKNOWN"),
        "fixture_rows_in_current_csv": count,
        "future_fixture_in_current_csv": "YES" if future_for_league else "NO",
        "recent_form_coverage": "NOT_AUDITED",
        "h2h_coverage": "NOT_AUDITED",
        "standings_coverage": "NOT_AUDITED",
        "xg_provenance": "NOT_AUDITED",
        "market_predictions_available": "NOT_AUDITED",
        "production_eligibility": "NOT_GRANTED",
        "notes": "Retained CSV row counts do not prove freshness or future kickoff."
    })

with (OUT / "oracle_league_readiness_inventory.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["canonical_league_id"])
    writer.writeheader()
    writer.writerows(rows)

major = memory.get("league_universe", {})
named_legacy = []
for group in ("MAJOR", "MINOR"):
    for name in major.get(group, []):
        named_legacy.append({"legacy_group": group, "legacy_competition": name})
with (OUT / "oracle_legacy_universe_inventory.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["legacy_group", "legacy_competition"])
    writer.writeheader()
    writer.writerows(named_legacy)

summary = {
    "generated_utc": now.isoformat(),
    "canonical_registry_version": registry.get("version"),
    "canonical_registry_status": registry.get("status"),
    "canonical_league_count": len(leagues),
    "canonical_readiness_counts": dict(readiness_counts),
    "legacy_named_league_count": len(named_legacy),
    "legacy_major_count": len(major.get("MAJOR", [])),
    "legacy_minor_count": len(major.get("MINOR", [])),
    "legacy_exotic_discovery_is_placeholder_categories": bool(major.get("EXOTIC_DISCOVERY")),
    "current_fixture_csv_rows": len(fixtures),
    "future_fixture_rows_in_retained_csv": future_fixture_count,
    "unparseable_fixture_kickoffs": unparseable_kickoff_count,
    "latest_fixture_kickoff_utc": latest_fixture_kickoff.isoformat() if latest_fixture_kickoff else None,
    "fixture_csv_missing_provenance_columns": missing_provenance_columns,
    "fixture_csv_league_codes": sorted({(x.get("league_code") or "").strip() for x in fixtures if (x.get("league_code") or "").strip()}),
    "fixture_rows_by_code": dict(fixture_counts),
    "today_utc": today,
    "important_limitations": [
        "This inventory does not query providers and does not verify external feed freshness.",
        "A retained CSV row is not a future fixture or a production prediction.",
        "Future fixture count is calculated against current UTC using only the retained CSV.",
        "Recent form, H2H, standings, xG provenance and market coverage are not audited by this inventory.",
        "No production eligibility or model accuracy is inferred."
    ]
}
(OUT / "oracle_readiness_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
lines = [
    "# Oracle league readiness inventory",
    "",
    f"- Generated UTC: {summary['generated_utc']}",
    f"- Canonical registry: {summary['canonical_league_count']} leagues ({registry.get('version')})",
    f"- Readiness counts: {json.dumps(dict(readiness_counts), sort_keys=True)}",
    f"- Named leagues in legacy memory pack: {len(named_legacy)}",
    f"- Rows in retained fixture CSV: {len(fixtures)}",
    f"- Future fixtures in retained CSV: {future_fixture_count}",
    f"- Latest retained kickoff UTC: {latest_fixture_kickoff.isoformat() if latest_fixture_kickoff else 'NONE'}",
    f"- Missing source provenance columns: {', '.join(missing_provenance_columns) if missing_provenance_columns else 'none'}",
    "",
    "## Interpretation",
    "This is a static inventory, not a live fixture feed. It does not create predictions, query providers, verify external fixture availability, or grant production eligibility.",
    "Coverage fields are NOT_AUDITED until a source-backed join proves availability and as-of timestamps.",
    "",
    "## Files",
    "- oracle_league_readiness_inventory.csv",
    "- oracle_legacy_universe_inventory.csv",
    "- oracle_readiness_summary.json"
]
(OUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
