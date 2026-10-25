#!/usr/bin/env python3
"""Research-only reconciliation of the owner-selected FootyStats IDs to league-list season IDs.

This utility deliberately does not call the provider API and never handles API credentials.
Supply a sanitized league-list JSON response and a CSV with columns:
selected_id,country,competition_name

It treats season.id as a candidate match, not proof that a saved UI checkbox ID
has season-ID semantics. Exact ID and normalized display-name checks are reported
separately; no fuzzy match is approved automatically.
"""
import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path


def norm(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalogue-json", required=True, help="Sanitized league-list JSON response")
    ap.add_argument("--selected-csv", required=True, help="Selected ID manifest CSV")
    ap.add_argument("--out", required=True, help="Output CSV path")
    args = ap.parse_args()

    payload = json.loads(Path(args.catalogue_json).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("success") is not True or not isinstance(payload.get("data"), list):
        raise SystemExit("Invalid catalogue schema; expected success=true and data=list.")

    with Path(args.selected_csv).open(encoding="utf-8-sig", newline="") as f:
        selected = list(csv.DictReader(f))
    required = {"selected_id", "country", "competition_name"}
    if not selected or not required.issubset(selected[0]):
        raise SystemExit("Selected manifest must contain selected_id,country,competition_name.")
    ids = [str(r.get("selected_id", "")).strip() for r in selected]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise SystemExit("Selected manifest has blank or duplicate IDs; fail closed.")

    season_index = {}
    for league in payload["data"]:
        if not isinstance(league, dict):
            continue
        name = str(league.get("name", "")).strip()
        seasons = league.get("season", [])
        if not isinstance(seasons, list):
            continue
        for season in seasons:
            if not isinstance(season, dict) or season.get("id") in (None, ""):
                continue
            sid = str(season["id"]).strip()
            season_index.setdefault(sid, []).append({
                "catalogue_name": name,
                "season_year": str(season.get("year", "")),
                "country": str(league.get("country") or league.get("country_name") or ""),
            })

    out = []
    for row in selected:
        sid = str(row["selected_id"]).strip()
        candidates = season_index.get(sid, [])
        selected_name = norm(row["competition_name"])
        selected_country = norm(row["country"])
        exact_name = [c for c in candidates if norm(c["catalogue_name"]) == selected_name]
        name_contains = [c for c in candidates if selected_name and
                         (selected_name in norm(c["catalogue_name"]) or norm(c["catalogue_name"]) in selected_name)]
        country_match = [c for c in candidates if not selected_country or
                         selected_country == norm(c["country"]) or
                         selected_country in norm(c["catalogue_name"])]
        status = "EXACT_ID_AND_NAME" if len(exact_name) == 1 else (
            "ID_MATCH_NAME_REVIEW" if len(candidates) and name_contains else
            "ID_MATCH_NAME_MISMATCH" if len(candidates) else "ID_NOT_FOUND")
        out.append({
            "selected_id": sid,
            "selected_country": row["country"],
            "selected_competition_name": row["competition_name"],
            "candidate_count_for_season_id": len(candidates),
            "candidate_catalogue_names": " || ".join(sorted({c["catalogue_name"] for c in candidates})),
            "candidate_season_years": " || ".join(sorted({c["season_year"] for c in candidates})),
            "country_consistent_candidate_count": len(country_match),
            "exact_name_candidate_count": len(exact_name),
            "reconciliation_status": status,
            "approved_mapping": "NO",
            "note": "A season-ID match alone does not prove saved checkbox ID semantics or production readiness."
        })

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        writer.writeheader()
        writer.writerows(out)
    counts = {}
    for row in out:
        counts[row["reconciliation_status"]] = counts.get(row["reconciliation_status"], 0) + 1
    print(json.dumps({
        "selected_rows": len(selected),
        "unique_selected_ids": len(set(ids)),
        "catalogue_season_ids": len(season_index),
        "status_counts": counts,
        "approved_mappings": 0,
        "production_readiness": "NOT_ASSESSED"
    }, indent=2))


if __name__ == "__main__":
    main()
