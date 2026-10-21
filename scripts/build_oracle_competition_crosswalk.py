#!/usr/bin/env python3
"""Research-only candidate crosswalk; all matches require human review."""
import argparse, csv, json, re, unicodedata
from pathlib import Path

# Explicit full-name aliases only. Never strip a country prefix generically:
# that can falsely map e.g. Brazil Serie A to Italy's Serie A.
ALIASES = {
    "austria bundesliga": "austrian bundesliga",
    "belgium pro league": "belgian pro league",
    "croatia prva hnl": "croatian hnl",
    "czech republic first league": "czech first league",
    "england efl league one": "league one",
    "england efl league two": "league two",
    "england championship": "championship",
    "england premier league": "premier league",
    "france ligue 1": "ligue 1",
    "france ligue 2": "ligue 2",
    "germany bundesliga": "bundesliga",
    "germany 2 bundesliga": "2 bundesliga",
    "italy serie a": "serie a",
    "italy serie b": "serie b",
    "netherlands eredivisie": "eredivisie",
    "netherlands eerste divisie": "eerste divisie",
    "poland ekstraklasa": "ekstraklasa",
    "portugal liga nos": "primeira liga",
    "portugal ligapro": "liga portugal 2",
    "scotland premiership": "scottish premiership",
    "south africa premier soccer league": "south african psl",
    "spain la liga": "la liga",
    "spain segunda division": "segunda division",
    "turkey super lig": "turkish super lig",
    "ukraine ukrainian premier league": "ukrainian premier league",
    # Deliberately no Brazil Serie A alias to Italian Serie A.
}

def norm(value):
    s = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"\b(fc|afc|club)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def candidate_norm(name):
    n = norm(name)
    return norm(ALIASES.get(n, n))

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--registry", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--catalogue", help="Previously acquired provider catalogue CSV; no API call.")
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
        rows.append({"provider_competition_name": name, "normalized_provider_name": norm(name),
                     "candidate_normalized_name": key, "crosswalk_state": state,
                     "candidate_canonical_id": cid, "candidate_canonical_competition": comp,
                     "source_name_type": source_type, "human_approval_required": True,
                     "production_eligibility": "NOT_GRANTED"})
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ["provider_competition_name", "crosswalk_state"]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    summary = {"status":"PROVISIONAL_CROSSWALK_BUILT", "provider_unique_names":len(provider_names),
               "source_name_type":source_type,
               "candidate_matches_requiring_review":sum(r["crosswalk_state"]=="CANDIDATE_MATCH_REQUIRES_REVIEW" for r in rows),
               "ambiguous":sum(r["crosswalk_state"]=="AMBIGUOUS_CANONICAL_MATCH" for r in rows),
               "unmatched":sum(r["crosswalk_state"]=="UNMATCHED_REQUIRES_REVIEW" for r in rows),
               "canonical_registry_leagues":len(canonical),
               "registry_active_universe_count":reg.get("active_universe",{}).get("league_count"),
               "intended_44_universe_reconciled":False,
               "warning":"Full-name aliases generate candidates only. Human review required; no production eligibility granted. Generic country-prefix stripping is intentionally disabled to prevent cross-country false matches."}
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(summary))
if __name__ == "__main__":
    main()
