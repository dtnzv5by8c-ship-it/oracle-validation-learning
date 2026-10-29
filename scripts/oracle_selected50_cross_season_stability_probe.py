#!/usr/bin/env python3
"""Research-only one-call cross-season identity probe for Oracle Selected-50.

Uses the documented unfiltered FootyStats league-list endpoint once. Unlike the
chosen-only response, the full list is inspected for season-level records so
each selected season ID can be matched directly and its comp_master_id compared
against other seasons. No raw payload is saved and no production files are written.
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
    if not isinstance(obj, dict): return ""
    for k in keys:
        x = obj.get(k)
        if x not in (None, ""): return x
    return ""
def season_id(obj):
    direct = val(obj, "season_id", "seasonID", "league_id", "id")
    nested = obj.get("season") if isinstance(obj, dict) else None
    if isinstance(nested, dict):
        direct = val(nested, "id", "season_id", "seasonID") or direct
    return str(direct).strip()
def season_year(obj):
    nested = obj.get("season") if isinstance(obj, dict) else None
    if isinstance(nested, dict):
        return str(val(nested, "year", "season_year", "season") or val(obj, "year") or "")
    return str(val(obj, "year", "season_year", "season") or "")
def comp_name(obj):
    return str(val(obj, "league_name", "english_name", "name", "competition_name"))
def country_name(obj):
    return str(val(obj, "country", "country_name"))

url = "https://api.football-data-api.com/league-list?" + urlencode({"key": key})
try:
    req = Request(url, headers={"User-Agent":"Oracle-Selected50-CrossSeason-Audit/1.1","Accept":"application/json"})
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
# Flatten season objects where the response groups multiple seasons under a parent.
records=[]
for p in provider:
    if not isinstance(p, dict): continue
    nested = p.get("season") or p.get("seasons")
    if isinstance(nested, list):
        for s in nested:
            if isinstance(s, dict):
                records.append({"country": country_name(p), "competition": comp_name(p),
                    "season_id": str(val(s,"id","season_id","seasonID")).strip(),
                    "season_year": str(val(s,"year","season_year","season")).strip(),
                    "comp_master_id": str(val(s,"comp_master_id","compMasterId") or val(p,"comp_master_id","compMasterId","parent_competition_id")).strip(),
                    "raw_name": comp_name(p)})
    elif isinstance(nested, dict):
        records.append({"country": country_name(p), "competition": comp_name(p),
            "season_id": str(val(nested,"id","season_id","seasonID") or val(p,"season_id","seasonID","league_id","id")).strip(),
            "season_year": str(val(nested,"year","season_year","season") or val(p,"year")).strip(),
            "comp_master_id": str(val(nested,"comp_master_id","compMasterId") or val(p,"comp_master_id","compMasterId","parent_competition_id")).strip(),
            "raw_name": comp_name(p)})
    else:
        # The documented full list may also return one season per top-level object.
        sid = str(val(p,"season_id","seasonID","league_id","id")).strip()
        if sid:
            records.append({"country":country_name(p),"competition":comp_name(p),
                "season_id":sid,"season_year":season_year(p),
                "comp_master_id":str(val(p,"comp_master_id","compMasterId","parent_competition_id")).strip(),
                "raw_name":comp_name(p)})

rows=[]
for r in registry:
    country, comp = r["country"], r["competition"]
    selected_id = str(r["footystats_season_id"]).strip()
    expected_master = str(r.get("footystats_comp_master_id_observed","")).strip()
    id_matches=[p for p in records if p["season_id"] == selected_id]
    exact=[p for p in id_matches if norm(p["country"])==norm(country) and norm(p["competition"])==norm(comp)]
    masters=[p["comp_master_id"] for p in exact if p["comp_master_id"]]
    master=masters[0] if len(set(masters))==1 and masters else ""
    same_master=[p for p in records if master and p["comp_master_id"]==master]
    same_master_exact=[p for p in same_master if norm(p["country"])==norm(country) and norm(p["competition"])==norm(comp)]
    master_match="YES" if master and expected_master and master==expected_master else ("NO" if master and expected_master else "UNVERIFIED")
    if len(exact)==1 and master and master_match=="YES" and len({p["season_id"] for p in same_master_exact})>1:
        assessment="SEASON_ID_AND_MASTER_ID_MATCH_MULTI_SEASON_STABILITY_SUPPORTED"
    elif len(exact)==1 and master_match=="NO":
        assessment="MASTER_ID_CONFLICT_REVIEW_REQUIRED"
    elif len(exact)==1 and master and len({p["season_id"] for p in same_master_exact})>1:
        assessment="MULTI_SEASON_GROUP_FOUND_BUT_OBSERVED_MASTER_ID_NOT_VERIFIED"
    elif len(exact)==1 and master:
        assessment="SEASON_ID_MATCHED_MASTER_ID_PRESENT_BUT_STABILITY_NOT_DEMONSTRATED"
    elif len(exact)==1:
        assessment="SEASON_ID_MATCHED_BUT_MASTER_ID_MISSING"
    elif len(id_matches)>1:
        assessment="SELECTED_SEASON_ID_AMBIGUOUS"
    elif len(id_matches)==1:
        assessment="SEASON_ID_FOUND_COUNTRY_OR_COMPETITION_MISMATCH"
    else:
        assessment="SELECTED_SEASON_ID_NOT_FOUND_IN_FULL_PROVIDER_LIST"
    rows.append({
        "country":country,"competition":comp,"selected_season_id":selected_id,
        "observed_comp_master_id":expected_master,"provider_id_matches":len(id_matches),
        "exact_country_competition_matches":len(exact),"provider_season_year":exact[0]["season_year"] if len(exact)==1 else "",
        "provider_comp_master_id":master,"master_id_matches_observed":master_match,
        "seasons_in_same_exact_master_group":len({p["season_id"] for p in same_master_exact}),
        "same_master_season_ids":";".join(sorted({p["season_id"] for p in same_master_exact})),
        "assessment":assessment
    })
fields=list(rows[0].keys())
with (OUT/"cross_season_stability.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
counts={}
for r in rows: counts[r["assessment"]]=counts.get(r["assessment"],0)+1
summary={"generated_utc":datetime.now(timezone.utc).isoformat(),
 "endpoint":"FootyStats league-list (unfiltered full list)",
 "provider_requests_attempted":1,"retries":0,"selected_leagues":len(rows),
 "provider_records_received":len(provider),"season_records_normalized":len(records),
 "provider_success":True,"counts":counts,"raw_provider_payload_saved":False,
 "production_eligible":False,"betting_eligible":False,
 "interpretation":"Direct season-ID matching against the unfiltered provider list; comp_master_id comparisons are evidence for research review only and do not create Oracle canonical mappings or production eligibility."}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
