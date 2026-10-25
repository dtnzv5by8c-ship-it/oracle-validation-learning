#!/usr/bin/env python3
"""Research-only reconciliation of the selected 50 IDs against FootyStats catalogue CSV.

Inputs:
  catalogue CSV columns: league_name,season_year,season_id
  selected CSV columns: selected_id,country,competition_name

The selected IDs are treated as season IDs because the live catalogue evidence
shows exact ID + country/competition-name matches. This does not approve a
canonical Oracle mapping or imply data/market readiness.
"""
import argparse
import csv
import re
import unicodedata
from pathlib import Path


def norm(value):
    value = unicodedata.normalize("NFKD", str(value or ""))
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalogue-csv", required=True)
    ap.add_argument("--selected-csv", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    catalogue = read_csv(args.catalogue_csv)
    selected = read_csv(args.selected_csv)
    if not catalogue or not {"league_name", "season_year", "season_id"}.issubset(catalogue[0]):
        raise SystemExit("Catalogue CSV must contain league_name,season_year,season_id.")
    if not selected or not {"selected_id", "country", "competition_name"}.issubset(selected[0]):
        raise SystemExit("Selected CSV must contain selected_id,country,competition_name.")

    selected_ids = [str(r.get("selected_id", "")).strip() for r in selected]
    if any(not v for v in selected_ids) or len(selected_ids) != len(set(selected_ids)):
        raise SystemExit("Selected manifest contains blank or duplicate IDs; refusing to continue.")
    catalogue_ids = [str(r.get("season_id", "")).strip() for r in catalogue]
    if any(not v for v in catalogue_ids):
        raise SystemExit("Catalogue contains blank season IDs; refusing to continue.")
    if len(catalogue_ids) != len(set(catalogue_ids)):
        raise SystemExit("Catalogue contains duplicate season IDs; refusing to continue.")

    index = {str(r["season_id"]).strip(): r for r in catalogue}
    output = []
    for row in selected:
        sid = str(row["selected_id"]).strip()
        cat = index.get(sid)
        expected = norm(str(row["country"]).strip() + " " + str(row["competition_name"]).strip())
        observed = norm(cat["league_name"]) if cat else ""
        exact = bool(cat and expected == observed)
        output.append({
            "selected_id": sid,
            "identifier_type": "FOOTYSTATS_SEASON_ID" if cat else "UNRESOLVED",
            "selected_country": row["country"],
            "selected_competition_name": row["competition_name"],
            "catalogue_competition_name": cat["league_name"] if cat else "",
            "catalogue_season_year": cat["season_year"] if cat else "",
            "id_found_in_catalogue": "YES" if cat else "NO",
            "country_competition_name_match": "YES" if exact else ("NO" if cat else "NOT_CHECKED"),
            "canonical_oracle_mapping": "NOT_APPROVED",
            "production_eligibility": "NOT_GRANTED",
            "note": "Catalogue identity only; historical/current fixture joins and market readiness require separate evidence."
        })

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)

    matched = sum(r["id_found_in_catalogue"] == "YES" for r in output)
    exact = sum(r["country_competition_name_match"] == "YES" for r in output)
    print(f"selected_rows={len(output)}")
    print(f"season_id_matches={matched}")
    print(f"exact_country_competition_matches={exact}")
    print("canonical_mappings_approved=0")
    print("production_eligibility=NOT_GRANTED")


if __name__ == "__main__":
    main()
