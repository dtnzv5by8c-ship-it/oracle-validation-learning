#!/usr/bin/env python3
"""Research-only one-call audit of FootyStats selected-50 season identity.

Uses the documented league-list endpoint once. It checks whether each selected
season ID is present under the exact country/competition entry and inventories
other seasons listed under that same provider competition object. It does NOT
claim independent per-season master-ID stability if the API exposes the parent
comp_master_id only once for the competition object.
"""
import csv, json, os, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

REG = Path("reports/oracle-selected50-footystats-first-identity-registry-2026-10-29.csv")
OUT = Path("oracle-selected50-cross-season-stability")
OUT.mkdir(exist_ok=True)
key = os.environ.get("FOOTYSTATS_API_KEY", "").strip()
if not REG.is_file(): raise SystemExit("Registry missing; zero provider calls.")
if not key: raise SystemExit("FOOTYSTATS_API_KEY secret missing; zero provider calls.")
with REG.open(encoding="utf-8-sig", newline="") as f:
    registry = list(csv.DictReader(f))
if len(registry) != 50:
    raise SystemExit(f"Expected 50 registry rows, got {len(registry)}; zero provider calls.")

def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s or "").casefold())
def val(obj, *keys):
    for k in keys:
        x = obj.get(k) if isinstance(obj, dict) else None
        if x not in (None, ""): return x
    return ""
url = "https://api.football-data-api.com/league-list?" + urlencode({"key": key, "chosen_leagues_only": "true"})
try:
    req = Request(url, headers={"User-Agent":"Oracle-Selected50-LeagueList-Audit/1.0","Accept":"application/json"})
    with urlopen(req, timeout=45) as response:
        status = response.status
        payload = json.loads(response.read().decode("utf-8"))
except HTTPError as e:
    raise SystemExit(f"FootyStats league-list request failed with HTTP {e.code}; no retries.")
except URLError as e:
    raise SystemExit(f"FootyStats league-list request failed ({type(e).__name__}); no retries.")
except Exception as e:
    raise SystemExit(f"FootyStats league-list response could not be parsed ({type(e).__name__}); no retries.")
if status != 200 or payload.get("success") is not True or not isinstance(payload.get("data"), list):
    raise SystemExit("FootyStats league-list response did not satisfy success/data contract; no retries.")
provider = payload["data"]
rows=[]
for r in registry:
    country, comp = r["country"], r["competition"]
    selected_id = str(r["footystats_season_id"]).strip()
    expected_master = str(r.get("footystats_comp_master_id_observed","")).strip()
    matches=[]
    for p in provider:
        pname = val(p,"name","competition_name","league_name","english_name")
        pcountry = val(p,"country","country_name")
        # Some provider records encode country into the display name; exact normalized
        # full display-name match is allowed only when the country field is absent.
        name_ok = norm(pname) == norm(comp) or norm(pname) == norm(f"{country} {comp}") or norm(pname) == norm(f"{comp} {country}")
        country_ok = norm(pcountry) == norm(country) if pcountry else (norm(pname) in {norm(f"{country} {comp}"),norm(f"{comp} {country}")})
        if name_ok and country_ok:
            matches.append(p)
    base={"country":country,"competition":comp,"selected_season_id":selected_id,
          "observed_comp_master_id":expected_master,"matching_provider_competition_objects":len(matches),
          "current_season_id_present":"NO","listed_season_count":0,"listed_prior_season_count":0,
          "listed_season_ids":"","listed_season_years":"","provider_comp_master_id":"",
          "master_id_matches_observed":"UNVERIFIED","assessment":"NO_EXACT_PROVIDER_COMPETITION_MATCH"}
    if len(matches)==1:
        p=matches[0]
        seasons=p.get("season") or p.get("seasons") or []
        if isinstance(seasons,dict): seasons=[seasons]
        if not isinstance(seasons,list): seasons=[]
        season_ids=[]; years=[]
        for s in seasons:
            if not isinstance(s,dict): continue
            sid=str(val(s,"id","season_id","seasonID")).strip()
            yr=str(val(s,"year","season","season_year")).strip()
            if sid: season_ids.append(sid)
            if yr: years.append(yr)
        master=str(val(p,"comp_master_id","compMasterId","parent_competition_id")).strip()
        base.update({"listed_season_count":len(set(season_ids)),
          "listed_prior_season_count":sum(1 for sid in set(season_ids) if sid != selected_id),
          "listed_season_ids":";".join(sorted(set(season_ids))),
          "listed_season_years":";".join(sorted(set(years))),
          "provider_comp_master_id":master,
          "current_season_id_present":"YES" if selected_id in season_ids else "NO",
          "master_id_matches_observed":"YES" if master and expected_master and master==expected_master else ("NO" if master and expected_master else "UNVERIFIED")})
        if base["current_season_id_present"]=="YES" and base["master_id_matches_observed"]=="YES" and len(set(season_ids))>1:
            base["assessment"]="SELECTED_SEASON_AND_MULTIPLE_SEASONS_CONFIRMED_UNDER_COMPETITION_OBJECT"
        elif base["current_season_id_present"]=="YES" and base["master_id_matches_observed"]=="YES":
            base["assessment"]="SELECTED_SEASON_AND_MASTER_ID_MATCH; MULTI_SEASON_EVIDENCE_INSUFFICIENT"
        elif base["current_season_id_present"]!="YES":
            base["assessment"]="SELECTED_SEASON_ID_NOT_FOUND_IN_EXACT_COMPETITION_OBJECT"
        elif base["master_id_matches_observed"]=="NO":
            base["assessment"]="MASTER_ID_CONFLICT_REVIEW_REQUIRED"
        else:
            base["assessment"]="CANONICAL_COMPETITION_IDENTITY_UNVERIFIED"
    elif len(matches)>1:
        base["assessment"]="AMBIGUOUS_PROVIDER_COMPETITION_MATCH"
    rows.append(base)
fields=list(rows[0].keys())
with (OUT/"cross_season_stability.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
counts={}
for r in rows: counts[r["assessment"]]=counts.get(r["assessment"],0)+1
summary={"generated_utc":datetime.now(timezone.utc).isoformat(),"endpoint":"FootyStats league-list?chosen_leagues_only=true",
"provider_requests_attempted":1,"retries":0,"selected_leagues":len(rows),"provider_success":True,
"counts":counts,"raw_provider_payload_saved":False,"production_eligible":False,"betting_eligible":False,
"interpretation":"This one-call audit verifies selected-season membership and observed comp_master_id alignment within provider competition objects. It does not independently prove that comp_master_id is stable on each season record or establish Oracle canonical IDs."}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
