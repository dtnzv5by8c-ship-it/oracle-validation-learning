#!/usr/bin/env python3
"""Build a dynamic, FootyStats-authoritative league/season registry from a saved catalogue CSV.

Offline only: this tool makes no provider requests and never consults the legacy fixed-50 manifest.
"""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from datetime import datetime
from pathlib import Path

REQUIRED = ("league_name", "season_id")
FIELDS = ("provider", "provider_country", "provider_league_name", "provider_season_label",
          "provider_season_id", "provider_competition_id", "catalogue_scope", "mapping_status")

def build_registry(rows, retrieved_utc, scope="chosen_leagues_only"):
    if not isinstance(retrieved_utc, str) or not retrieved_utc.strip():
        raise ValueError("catalogue retrieval timestamp is required")
    try:
        stamp = datetime.fromisoformat(retrieved_utc.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("catalogue retrieval timestamp must be ISO-8601") from exc
    if stamp.tzinfo is None or stamp.utcoffset() is None:
        raise ValueError("catalogue retrieval timestamp must include timezone")
    if scope not in {"chosen_leagues_only", "all_available"}:
        raise ValueError("catalogue scope must be chosen_leagues_only or all_available")
    out, seen = [], set()
    for n, raw in enumerate(rows, start=2):
        row = {str(k).strip(): str(v or "").strip() for k, v in raw.items()}
        missing = [k for k in REQUIRED if not row.get(k)]
        if missing:
            raise ValueError(f"catalogue row {n} missing required fields: {', '.join(missing)}")
        sid = row["season_id"]
        if sid in seen:
            raise ValueError(f"duplicate FootyStats season ID {sid!r}; refusing ambiguous provider identity")
        seen.add(sid)
        out.append({
            "provider": "FootyStats",
            "provider_country": row.get("country", ""),
            "provider_league_name": row["league_name"],
            "provider_season_label": row.get("season_year", ""),
            "provider_season_id": sid,
            "provider_competition_id": row.get("competition_id", ""),
            "catalogue_scope": scope,
            "mapping_status": "PROVIDER_NATIVE_IDENTITY",
        })
    if not out:
        raise ValueError("provider catalogue is empty; no league configuration can be generated")
    league_names = {r["provider_league_name"] for r in out}
    return {
        "schema_version": "1.0",
        "source_of_truth": "FootyStats",
        "catalogue_scope": scope,
        "catalogue_retrieved_utc": stamp.isoformat(),
        "provider_league_count": len(league_names),
        "provider_season_count": len(out),
        "provider_season_ids_unique": True,
        "legacy_fixed_50_manifest_used": False,
        "production_logic_changed": False,
        "production_eligible": False,
        "betting_eligible": False,
        "seasons": out,
    }

def write_registry(registry, json_path, csv_path):
    json_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(registry["seasons"])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogue-csv", required=True, type=Path)
    parser.add_argument("--retrieved-utc", required=True)
    parser.add_argument("--scope", choices=("chosen_leagues_only", "all_available"), default="chosen_leagues_only")
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    args = parser.parse_args()
    with args.catalogue_csv.open(encoding="utf-8-sig", newline="") as handle:
        registry = build_registry(csv.DictReader(handle), args.retrieved_utc, args.scope)
    write_registry(registry, args.output_json, args.output_csv)
    print(json.dumps({k: registry[k] for k in ("source_of_truth", "catalogue_scope", "provider_league_count", "provider_season_count", "legacy_fixed_50_manifest_used", "production_eligible", "betting_eligible")}, indent=2))

if __name__ == "__main__":
    main()
