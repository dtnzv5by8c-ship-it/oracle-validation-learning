#!/usr/bin/env python3
"""Research-only cross-season stability probe for FootyStats comp_master_id.
Reads the selected-50 registry and archived ingestion manifest, then makes at most
one sequential league-season request per league. Never writes production data.
"""
import csv, json, os, re, time, zipfile
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime, timezone

REG = Path("reports/oracle-selected50-footystats-first-identity-registry-2026-10-29.csv")
ARCHIVE = Path(os.environ.get("ORACLE_ARCHIVE", "private-download/oracle-selected50-footystats-private-ingestion.zip"))
OUT = Path("oracle-selected50-cross-season-stability")
OUT.mkdir(exist_ok=True)
key = os.environ.get("FOOTYSTATS_API_KEY", "").strip()
if not REG.is_file(): raise SystemExit("Registry missing; zero provider calls.")
if not ARCHIVE.is_file(): raise SystemExit("Private archive missing; zero provider calls.")
if not key: raise SystemExit("FOOTYSTATS_API_KEY secret missing; zero provider calls.")

with REG.open(encoding="utf-8-sig", newline="") as f: registry = list(csv.DictReader(f))
if len(registry) != 50: raise SystemExit(f"Expected 50 registry rows, got {len(registry)}; zero provider calls.")
with zipfile.ZipFile(ARCHIVE) as z:
    candidates = [n for n in z.namelist() if n.endswith("ingestion_manifest.csv")]
    if not candidates: raise SystemExit("Archive ingestion_manifest.csv missing; zero provider calls.")
    raw = z.read(candidates[0]).decode("utf-8-sig")
import io
with io.StringIO(raw) as f: manifest = list(csv.DictReader(f))
if not manifest: raise SystemExit("Archive manifest empty; zero provider calls.")
def norm(s): return re.sub(r"[^a-z0-9]", "", str(s or "").casefold())
# The manifest is only used to locate prior season IDs. Names are exact-normalized;
# no fuzzy match or provider ID is promoted to canonical Oracle identity.
results=[]
for r in registry:
    name=norm(r.get("competition"))
    current_id=str(r.get("footystats_season_id","")).strip()
    rows=[m for m in manifest if norm(m.get("provider_league_name") or m.get("provider_competition_name") or m.get("league_name")) == name]
    prior=[]
    for m in rows:
        sid=str(m.get("season_id") or m.get("provider_season_id") or "").strip()
        year=str(m.get("season_start_year") or m.get("season_year") or "").strip()
        if sid and sid != current_id and year.isdigit():
            prior.append((int(year), sid))
    prior=[x for x in prior if x[0] < 2026]
    row={ "country":r["country"],"competition":r["competition"],"current_season_id":current_id,
          "current_comp_master_id":r.get("footystats_comp_master_id_observed",""),
          "prior_season_id":"","prior_season_year":"","prior_comp_master_id":"",
          "http_status":"","provider_success":False,"assessment":"NO_EXACT_PRIOR_SEASON_CANDIDATE",
          "error_class":""}
    if prior:
        year,sid=sorted(prior, reverse=True)[0]
        row["prior_season_id"]=sid; row["prior_season_year"]=str(year)
        url="https://api.football-data-api.com/league-season?"+urlencode({"key":key,"season_id":sid})
        try:
            req=Request(url,headers={"User-Agent":"Oracle-Selected50-CrossSeason-Stability/1.0","Accept":"application/json"})
            with urlopen(req,timeout=25) as resp:
                row["http_status"]=str(resp.status); payload=json.loads(resp.read().decode("utf-8"))
            row["provider_success"]=payload.get("success") is True
            data=payload.get("data")
            if isinstance(data,list): data=data[0] if data and isinstance(data[0],dict) else {}
            if not isinstance(data,dict): data={}
            got=str(data.get("comp_master_id") or "").strip()
            row["prior_comp_master_id"]=got
            cur=str(row["current_comp_master_id"] or "").strip()
            if row["http_status"]=="200" and row["provider_success"] and got and cur and got==cur:
                row["assessment"]="STABLE_ACROSS_TWO_SEASONS_OBSERVED"
            elif row["http_status"]=="200" and row["provider_success"] and got and cur and got!=cur:
                row["assessment"]="MASTER_ID_CHANGED_REVIEW_REQUIRED"
            elif row["http_status"]=="200" and row["provider_success"]:
                row["assessment"]="PRIOR_MASTER_ID_MISSING"
            else: row["assessment"]="PROVIDER_RESPONSE_NOT_SUCCESSFUL"
        except HTTPError as e: row["http_status"]=str(e.code); row["error_class"]="HTTPError"; row["assessment"]="PROVIDER_REQUEST_FAILED"
        except URLError as e: row["error_class"]=type(e).__name__; row["assessment"]="PROVIDER_REQUEST_FAILED"
        except Exception as e: row["error_class"]=type(e).__name__; row["assessment"]="PROVIDER_RESPONSE_PARSE_FAILED"
        time.sleep(1.25)
    results.append(row)
fields=list(results[0].keys()) if results else ["assessment"]
with (OUT/"cross_season_stability.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(results)
counts={}
for r in results: counts[r["assessment"]]=counts.get(r["assessment"],0)+1
summary={"generated_utc":datetime.now(timezone.utc).isoformat(),"scope":"selected 50 only","provider_requests_attempted":sum(bool(r["http_status"] or r["error_class"]) for r in results),
"max_requests":50,"retries":0,"sequential":True,"raw_provider_payload_saved":False,
"current_master_id_source":"previously observed sanitized identity crosswalk",
"prior_master_id_source":"one exact-normalized competition-name prior-season row from existing private archive manifest",
"counts":counts,"production_eligible":False,"betting_eligible":False,
"warning":"Two-season equality is supporting evidence only, not proof of canonical Oracle identity or production approval."}
(OUT/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2,sort_keys=True))
