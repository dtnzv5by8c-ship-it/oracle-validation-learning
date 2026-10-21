#!/usr/bin/env python3
"""Research-only candidate crosswalk between FootyStats names and Oracle registry.

Candidates are never production-approved automatically. Country prefixes and a
small explicit alias table help surface likely matches for human review.
"""
import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path

COUNTRY_PREFIXES = (
    "argentina", "austria", "belgium", "brazil", "croatia", "czech republic",
    "england", "france", "germany", "greece", "italy", "mexico", "netherlands",
    "norway", "poland", "portugal", "qatar", "romania", "saudi arabia",
    "scotland", "south africa", "spain", "switzerland", "turkey", "usa", "ukraine",
)
ALIASES = {
    "austria bundesliga": "austrian bundesliga",
    "belgium pro league": "belgian pro league",
    "croatia prva hnl": "croatian hnl",
    "czech republic first league": "czech first league",
    "england efl league one": "league one",
    "england efl league two": "league two",
    "portugal liga nos": "primeira liga",
    "portugal ligapro": "liga portugal 2",
    "saudi arabia professional league": "saudi pro league",
    "scotland premiership": "scottish premiership",
    "south africa premier soccer league": "south african psl",
    "turkey super lig": "turkish super lig",
    "ukraine ukrainian premier league": "ukrainian premier league",
}

def norm(value):
    s = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\b(fc|afc|club)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def candidate_norm(name):
    n = norm(name)
    # Use normalized original first, then remove a known leading country.
    stripped = n
    for country in sorted((norm(x) for x in COUNTRY_PREFIXES), key=len, reverse=True):
        if stripped.startswith(country + " "):
            stripped = stripped[len(country) + 1:].strip()
            break
    return norm(ALIASES.get(n, ALIASES.get(stripped, stripped)))

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--registry", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--catalogue", help="Already acquired provider catalogue CSV; no API call is made.")
    a = p.parse_args()
    reg = json.loads(Path(a.registry).read_text(encoding="utf-8"))
    manifest = read_csv(a.manifest)
    canonical = reg.get("leagues", [])
    bynorm = {}
    for league in canonical:
        bynorm.setdefault(norm(league.get("competition")), []).append(league)
    if a.catalogue and Path(a.catalogue).exists():
        catalogue = read_csv(a.catalogue)
        provider_names = sorted({str(r.get("provider_league_name") or "").strip()
                                 for r in catalogue if str(r.get("provider_league_name") or "").strip()})
        source_type = "provider_selected_catalogue"
    else:
        provider_names = sorted({str(r.get("provider_competition_name") or r.get("league_name") or
                                      r.get("provider_league_name") or r.get("league_folder") or "").strip()
                                 for r in manifest if str(r.get("provider_competition_name") or r.get("league_name") or
                                                          r.get("provider_league_name") or r.get("league_folder") or "").strip()})
        source_type = "provider_display_name" if provider_names else "archive_folder_slug"
    rows = []
    for name in provider_names:
        key = candidate_norm(name)
        matches = bynorm.get(key, []) if source_type != "archive_folder_slug" else []
        if len(matches) == 1:
            league = matches[0]
            state, cid, comp = "CANDIDATE_MATCH_REQUIRES_REVIEW", league.get("id", ""), league.get("competition", "")
        elif len(matches) > 1:
            state, cid, comp = "AMBIGUOUS_CANONICAL_MATCH", "", "; ".join(x.get("competition", "") for x in matches)
        else:
            state, cid, comp = "UNMATCHED_REQUIRES_REVIEW", "", ""
        rows.append({
            "provider_competition_name": name,
            "normalized_provider_name": norm(name),
            "candidate_normalized_name": key,
            "crosswalk_state": state,
            "candidate_canonical_id": cid,
            "candidate_canonical_competition": comp,
            "source_name_type": source_type,
            "human_approval_required": True,
            "production_eligibility": "NOT_GRANTED",
        })
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ["provider_competition_name", "crosswalk_state"]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "status": "PROVISIONAL_CROSSWALK_BUILT",
        "provider_unique_names": len(provider_names),
        "source_name_type": source_type,
        "candidate_matches_requiring_review": sum(r["crosswalk_state"] == "CANDIDATE_MATCH_REQUIRES_REVIEW" for r in rows),
        "ambiguous": sum(r["crosswalk_state"] == "AMBIGUOUS_CANONICAL_MATCH" for r in rows),
        "unmatched": sum(r["crosswalk_state"] == "UNMATCHED_REQUIRES_REVIEW" for r in rows),
        "canonical_registry_leagues": len(canonical),
        "registry_active_universe_count": reg.get("active_universe", {}).get("league_count"),
        "intended_44_universe_reconciled": False,
        "warning": "Country-prefix/alias normalization only generates candidates. Human review is required; no production eligibility is granted.",
    }
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary))

if __name__ == "__main__":
    main()
