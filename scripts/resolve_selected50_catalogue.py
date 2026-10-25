#!/usr/bin/env python3
"""Resolve selected season IDs from a saved provider catalogue export, without network calls.

Input should be the JSON body previously saved from the provider league-list endpoint.
The script performs exact ID matching only. It never guesses aliases or calls the API.
"""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "oracle-footystats-selected-50-season-id-manifest.csv"
DEFAULT_OUT = ROOT / "audit-output" / "selected50_catalogue_resolution.csv"

def read_manifest(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 50:
        raise ValueError(f"Expected exactly 50 manifest rows, found {len(rows)}")
    ids = [str(r.get("selected_id", "")).strip() for r in rows]
    if any(not x for x in ids) or len(set(ids)) != 50:
        raise ValueError("Manifest must contain 50 nonblank unique selected_id values")
    return rows

def id_string(value):
    if value is None or isinstance(value, (dict, list, bool)):
        return ""
    return str(value).strip()

def load_catalogue(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, list):
        raise ValueError("Catalogue must be an object with a list at data; no API call was made")
    return data

def resolve(manifest, leagues):
    index = {}
    for league in leagues:
        if not isinstance(league, dict):
            continue
        seasons = league.get("season")
        if not isinstance(seasons, list):
            continue
        for season in seasons:
            if not isinstance(season, dict):
                continue
            sid = id_string(season.get("id"))
            if sid:
                index.setdefault(sid, []).append((league, season))
    out = []
    for row in manifest:
        sid = str(row["selected_id"]).strip()
        matches = index.get(sid, [])
        if len(matches) == 1:
            league, season = matches[0]
            # Only explicit fields are emitted. Do not treat season.id as competition ID.
            parent_id = ""
            for key in ("league_id", "competition_id", "provider_league_id", "provider_competition_id"):
                value = id_string(league.get(key))
                if value:
                    parent_id = value
                    break
            out.append({
                "selected_id": sid, "country": row.get("country", ""),
                "competition_name": row.get("competition_name", ""),
                "catalogue_status": "EXACT_SEASON_ID_MATCH",
                "provider_season_id": sid,
                "provider_competition_id": parent_id,
                "provider_catalogue_name": id_string(league.get("name")),
                "provider_country": id_string(league.get("country")),
                "provider_season_label": id_string(season.get("year")),
                "duplicate_catalogue_matches": 0,
                "mapping_method": "EXACT_NESTED_SEASON_ID",
            })
        elif len(matches) == 0:
            out.append({
                "selected_id": sid, "country": row.get("country", ""),
                "competition_name": row.get("competition_name", ""),
                "catalogue_status": "EXACT_SEASON_ID_NOT_FOUND",
                "provider_season_id": sid, "provider_competition_id": "",
                "provider_catalogue_name": "", "provider_country": "",
                "provider_season_label": "", "duplicate_catalogue_matches": 0,
                "mapping_method": "NO_MATCH_NO_GUESS",
            })
        else:
            out.append({
                "selected_id": sid, "country": row.get("country", ""),
                "competition_name": row.get("competition_name", ""),
                "catalogue_status": "BLOCKED_DUPLICATE_SEASON_ID",
                "provider_season_id": sid, "provider_competition_id": "",
                "provider_catalogue_name": "", "provider_country": "",
                "provider_season_label": "", "duplicate_catalogue_matches": len(matches),
                "mapping_method": "DUPLICATE_EXACT_ID_BLOCKED",
            })
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalogue-json", required=True, help="Path to an already-saved catalogue JSON export; no network access is performed")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    manifest = read_manifest(Path(args.manifest))
    rows = resolve(manifest, load_catalogue(Path(args.catalogue_json)))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = ["selected_id","country","competition_name","catalogue_status","provider_season_id",
              "provider_competition_id","provider_catalogue_name","provider_country",
              "provider_season_label","duplicate_catalogue_matches","mapping_method"]
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    counts = {}
    for row in rows:
        counts[row["catalogue_status"]] = counts.get(row["catalogue_status"], 0) + 1
    print(json.dumps({"selected_ids": len(rows), "status_counts": counts,
                      "network_calls_made": 0, "parent_ids_guessed": 0, "output": str(out)}, indent=2))
    if counts.get("BLOCKED_DUPLICATE_SEASON_ID", 0):
        raise SystemExit("Duplicate exact season IDs detected; output written with blocked rows")

if __name__ == "__main__":
    main()
