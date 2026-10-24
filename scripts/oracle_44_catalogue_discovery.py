#!/usr/bin/env python3
# Research refresh marker: 2026-10-24 — broadened catalogue candidate review; fuzzy matches remain unapproved.
"""Research-only FootyStats catalogue discovery for Oracle's 44 target competitions.

Does not fetch matches, create predictions, or alter the governed 27-league registry.
Writes a sanitized catalogue snapshot and a candidate crosswalk; never writes the API key.
"""
import csv, difflib, hashlib, json, os, re, sys, time, unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE = "https://api.football-data-api.com/"
TARGETS = [
("ZA","South Africa","Premier Soccer League",["South Africa Premier Soccer League","South Africa PSL"]),
("E0","England","Premier League",["England Premier League"]),("E1","England","Championship",["England Championship"]),
("SP1","Spain","La Liga",["Spain La Liga"]),("D1","Germany","Bundesliga",["Germany Bundesliga"]),
("I1","Italy","Serie A",["Italy Serie A"]),("F1","France","Ligue 1",["France Ligue 1"]),
("N1","Netherlands","Eredivisie",["Netherlands Eredivisie"]),("P1","Portugal","Primeira Liga",["Portugal Liga NOS","Portugal Primeira Liga"]),
("B1","Belgium","Pro League",["Belgium Pro League"]),("T1","Turkey","Süper Lig",["Turkey Süper Lig","Turkey Super Lig"]),
("DK","Denmark","Superliga",["Denmark Superliga","Denmark Superligaen"]),("SE","Sweden","Allsvenskan",["Sweden Allsvenskan"]),
("NO","Norway","Eliteserien",["Norway Eliteserien"]),("FI","Finland","Veikkausliiga",["Finland Veikkausliiga"]),
("SWZ","Switzerland","Super League",["Switzerland Super League","Switzerland Swiss Super League"]),
("AUT","Austria","Bundesliga",["Austria Bundesliga","Austria Austrian Bundesliga"]),("GR","Greece","Super League",["Greece Super League"]),
("POL","Poland","Ekstraklasa",["Poland Ekstraklasa"]),("CZE","Czech Republic","First League",["Czech First League","Czech Republic First League"]),
("CRO","Croatia","HNL",["Croatia HNL","Croatia Croatian HNL"]),("RS","Serbia","SuperLiga",["Serbia SuperLiga"]),
("ROU","Romania","Liga I",["Romania Liga I"]),("UKR","Ukraine","Premier League",["Ukraine Premier League","Ukraine Ukrainian Premier League"]),
("RU","Russia","Premier League",["Russia Premier League","Russia Russian Premier League"]),
("IE","Republic of Ireland","Premier Division",["Republic of Ireland Premier Division","Ireland Premier Division"]),
("SC0","Scotland","Premiership",["Scotland Premiership"]),("US","United States","MLS",["USA MLS","United States MLS"]),
("CA","Canada","Canadian Premier League",["Canada Canadian Premier League"]),("MX","Mexico","Liga MX",["Mexico Liga MX"]),
("BR","Brazil","Serie A",["Brazil Serie A","Brazil Serie A (Brasileiro)"]),("AR","Argentina","Primera División",["Argentina Primera Division","Argentina Primera División"]),
("CO","Colombia","Primera A",["Colombia Primera A"]),("CL","Chile","Primera División",["Chile Primera Division","Chile Primera División"]),
("UY","Uruguay","Primera División",["Uruguay Primera Division","Uruguay Primera División"]),("PY","Paraguay","Division Profesional",["Paraguay Division Profesional"]),
("EC","Ecuador","Serie A",["Ecuador Serie A"]),("PE","Peru","Primera División",["Peru Primera Division","Peru Primera División"]),
("VE","Venezuela","Primera División",["Venezuela Primera Division","Venezuela Primera División"]),("AU","Australia","A-League",["Australia A-League"]),
("JP","Japan","J1 League",["Japan J1 League"]),("KR","South Korea","K League 1",["South Korea K League 1","Korea Republic K League 1"]),
("CN","China","Chinese Super League",["China Chinese Super League"]),("IN","India","Indian Super League",["India Indian Super League"])
]

def api_catalogue(key):
    url = BASE + "league-list?" + urlencode({"key": key, "chosen_leagues_only": "false"})
    for attempt in range(4):
        try:
            req = Request(url, headers={"User-Agent":"Oracle-44-League-Catalogue-Discovery/1.0"})
            with urlopen(req, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict) or payload.get("success") is not True or not isinstance(payload.get("data"), list):
                raise RuntimeError("Provider returned an unexpected catalogue response; response details withheld.")
            return payload
        except HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(min(2 ** attempt, 8)); continue
            raise RuntimeError(f"Catalogue request failed with HTTP {exc.code}") from None
        except Exception as exc:
            if attempt < 3 and not isinstance(exc, RuntimeError):
                time.sleep(min(2 ** attempt, 8)); continue
            raise

def main():
    key = os.environ.get("FOOTYSTATS_API_KEY", "").strip()
    if not key:
        print("ERROR: FOOTYSTATS_API_KEY secret is missing.", file=sys.stderr); return 2
    payload = api_catalogue(key)
    leagues = [x for x in payload["data"] if isinstance(x, dict)]
    # Keep only catalogue identity and season metadata. No secret or full response is written.
    catalogue = []
    for league in leagues:
        seasons = league.get("season") if isinstance(league.get("season"), list) else []
        catalogue.append({
            "provider_league_id": str(league.get("id") or league.get("league_id") or league.get("competition_id") or ""),
            "provider_name": str(league.get("name", "")),
            "country": str(league.get("country", league.get("country_name", ""))),
            "seasons": [{"season_id": str(s.get("id","")), "season_label": str(s.get("year","")),
                         "season_start": str(s.get("start_date","")), "season_end": str(s.get("end_date",""))}
                        for s in seasons if isinstance(s, dict)]
        })
    by_name = {}
    for item in catalogue:
        by_name.setdefault(item["provider_name"].strip().casefold(), []).append(item)
    def norm(value):
        value = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii").casefold()
        return re.sub(r"[^a-z0-9]+", " ", value).strip()

    def similarity(a, b):
        aa, bb = norm(a), norm(b)
        if not aa or not bb:
            return 0.0
        seq = difflib.SequenceMatcher(None, aa, bb).ratio()
        at, bt = set(aa.split()), set(bb.split())
        overlap = len(at & bt) / max(1, len(at | bt))
        return max(seq, overlap)

    crosswalk = []
    for code, country, competition, aliases in TARGETS:
        matches = []
        for alias in aliases:
            matches.extend(by_name.get(alias.strip().casefold(), []))
        unique = {x["provider_league_id"]: x for x in matches}
        matches = list(unique.values())
        if matches:
            status = "AMBIGUOUS_ALIAS" if len(matches) > 1 else "EXACT_ALIAS_CANDIDATE"
            candidates = [(m, 1.0) for m in matches]
        else:
            # Rank candidates using competition-name similarity and country hints.
            # This is discovery assistance only; it never approves or auto-maps an ID.
            ranked = []
            for item in catalogue:
                name_score = max([similarity(competition, item["provider_name"])] +
                                 [similarity(alias, item["provider_name"]) for alias in aliases])
                country_score = similarity(country, item["country"])
                score = min(1.0, 0.8 * name_score + 0.2 * country_score)
                if name_score >= 0.35:
                    ranked.append((item, score, name_score, country_score))
            ranked.sort(key=lambda row: (-row[1], row[0]["provider_name"], row[0]["provider_league_id"]))
            candidates = [(item, score) for item, score, _, _ in ranked[:5]]
            status = "FUZZY_CANDIDATE_REVIEW_ONLY" if candidates else "NO_CANDIDATE_FOUND"
        if not candidates:
            candidates = [({}, 0.0)]
        for match, score in candidates:
            crosswalk.append({
                "target_code": code, "target_country": country, "target_competition": competition,
                "catalogue_status": status, "candidate_similarity_score": round(score, 4),
                "provider_league_id": match.get("provider_league_id", match.get("id", "")),
                "provider_name": match.get("provider_name",""), "provider_country": match.get("country",""),
                "candidate_season_ids": ";".join(s["season_id"] for s in match.get("seasons",[])),
                "candidate_season_labels": ";".join(s["season_label"] for s in match.get("seasons",[])),
                "candidate_season_dates": ";".join(f'{s["season_start"]}/{s["season_end"]}' for s in match.get("seasons",[])),
                "decision": "REVIEW_REQUIRED_NOT_AUTO_MAPPED"
            })
    out = Path("oracle-catalogue-discovery"); out.mkdir(exist_ok=True)
    with (out/"oracle_44_league_broader_catalogue_crosswalk.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(crosswalk[0].keys())); writer.writeheader(); writer.writerows(crosswalk)
    safe = {"generated_utc":datetime.now(timezone.utc).isoformat(), "catalogue_league_count":len(catalogue),
            "target_league_count":len(TARGETS), "targets_with_exact_alias_candidates":sum(any(r["target_code"]==t[0] and r["catalogue_status"]=="EXACT_ALIAS_CANDIDATE" for r in crosswalk) for t in TARGETS),
            "targets_with_fuzzy_candidates_for_review":sum(any(r["target_code"]==t[0] and r["catalogue_status"]=="FUZZY_CANDIDATE_REVIEW_ONLY" for r in crosswalk) for t in TARGETS),
            "targets_with_no_candidate_found":sum(not any(r["target_code"]==t[0] and r["catalogue_status"] not in ("NO_CANDIDATE_FOUND", "NO_EXACT_ALIAS_MATCH") for r in crosswalk) for t in TARGETS),
            "catalogue_sha256":hashlib.sha256(json.dumps(payload,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
            "provider_catalogue_top_level_keys_sample":sorted(set(k for row in leagues[:25] for k in row.keys())),
            "provider_season_keys_sample":sorted(set(k for row in leagues[:25] for season in (row.get("season") if isinstance(row.get("season"),list) else []) if isinstance(season,dict) for k in season.keys())),
            "scope":"Unfiltered catalogue discovery only; candidate mappings require human/independent validation; no matches or predictions fetched; production registry untouched."}
    (out/"oracle_44_league_broader_catalogue_summary.json").write_text(json.dumps(safe,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(safe,indent=2))
    return 0

if __name__ == "__main__":
    try: raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr); raise SystemExit(1)
