import json, os, re, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OUT=Path("oracle-selected50-one-season-identity-probe"); OUT.mkdir(exist_ok=True)
manifest=Path("reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md")
if not manifest.is_file(): raise SystemExit("Selected-50 manifest missing; zero requests made.")
selected=[]
for line in manifest.read_text(encoding="utf-8").splitlines():
    m=re.match(r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$",line)
    if m: selected.append({"row":int(m.group(1)),"selected_season_id":m.group(2).strip(),"country":m.group(3).strip(),"competition":m.group(4).strip()})
ids=[x["selected_season_id"] for x in selected]
if len(selected)!=50 or len(set(ids))!=50: raise SystemExit("Manifest guard failed: expected 50 unique selected IDs; zero requests made.")
key=os.environ.get("FOOTYSTATS_API_KEY","").strip()
if not key: raise SystemExit("FOOTYSTATS_API_KEY secret missing; zero requests made.")
allow=("id","comp_master_id","parent_competition_id","parent_id","league_id","competition_id","name","league_name","competition_name","country","country_name","iso","type","division","url","parent_url","shortHand","short_hand","season","season_name","year","starting_year","ending_year","status","verified")
results=[]
for item in selected:
    url="https://api.football-data-api.com/league-season?"+urlencode({"key":key,"season_id":item["selected_season_id"]})
    row={**item,"endpoint":"league-season","http_status":None,"provider_success":False,"returned_data_shape":None,"returned_data_count":None,"returned_fields":{},"error_class":None,"identity_assessment":"UNRESOLVED"}
    payload=None
    try:
        req=Request(url,headers={"User-Agent":"Oracle-Selected50-Identity-Reconciliation/1.0"})
        with urlopen(req,timeout=25) as response: row["http_status"]=response.status; payload=json.loads(response.read().decode("utf-8"))
    except HTTPError as exc: row["http_status"]=exc.code; row["error_class"]="HTTPError"
    except URLError as exc: row["error_class"]=type(exc).__name__
    except Exception as exc: row["error_class"]=type(exc).__name__
    if isinstance(payload,dict):
        row["provider_success"]=payload.get("success") is True; data=payload.get("data")
        if isinstance(data,list):
            row["returned_data_shape"]="list"; row["returned_data_count"]=len(data); data=data[0] if data and isinstance(data[0],dict) else {}
        elif isinstance(data,dict): row["returned_data_shape"]="object"; row["returned_data_count"]=1
        else: row["returned_data_shape"]=type(data).__name__; row["returned_data_count"]=None; data={}
        row["returned_fields"]={k:data.get(k) for k in allow if k in data and isinstance(data.get(k),(str,int,float,bool,type(None)))}
        got_id=str(data.get("id") or "").strip(); got_country=str(data.get("country") or data.get("country_name") or "").strip().casefold()
        got_name=str(data.get("name") or data.get("league_name") or "").strip().casefold()
        exp_country=item["country"].strip().casefold(); exp_name=item["competition"].strip().casefold()
        if row["http_status"]==200 and row["provider_success"] and got_id==item["selected_season_id"]:
            row["identity_assessment"]="SEASON_ID_AND_RESPONSE_SUCCESS_MATCH"
            if got_country==exp_country and got_name and (exp_name in got_name or got_name in exp_name):
                row["identity_assessment"]="SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW"
            elif got_country and got_country!=exp_country: row["identity_assessment"]="COUNTRY_MISMATCH_QUARANTINE"
        elif row["http_status"]==200 and row["provider_success"]: row["identity_assessment"]="RETURNED_ID_MISMATCH_QUARANTINE"
        else: row["identity_assessment"]="PROVIDER_OR_HTTP_FAILURE"
    results.append(row); time.sleep(0.15)
counts={"selected_leagues":len(selected),"requests_planned":len(selected),"requests_attempted":sum(1 for x in results if x["http_status"] is not None or x["error_class"] is not None),
"http_200_success":sum(1 for x in results if x["http_status"]==200 and x["provider_success"]),
"request_failures":sum(1 for x in results if not(x["http_status"]==200 and x["provider_success"])),
"season_id_match":sum(1 for x in results if x["identity_assessment"] in {"SEASON_ID_AND_RESPONSE_SUCCESS_MATCH","SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW"}),
"country_name_match":sum(1 for x in results if x["identity_assessment"]=="SEASON_ID_COUNTRY_NAME_MATCH_PARENT_FIELD_REQUIRES_SEMANTIC_REVIEW"),
"country_mismatches":sum(1 for x in results if x["identity_assessment"]=="COUNTRY_MISMATCH_QUARANTINE"),
"rows_with_comp_master_id":sum(1 for x in results if x["returned_fields"].get("comp_master_id") is not None),
"unique_comp_master_ids":len({str(x["returned_fields"].get("comp_master_id")) for x in results if x["returned_fields"].get("comp_master_id") is not None})}
summary={"diagnostic":"BOUNDED_SELECTED50_IDENTITY_RECONCILIATION","generated_utc":datetime.now(timezone.utc).isoformat(),"endpoint":"league-season","requests_per_selected_season":1,"retries":0,"parallel_requests":False,"raw_provider_payload_persisted":False,"api_key_persisted":False,"production_ledger_written":False,"production_eligibility":"NOT_GRANTED","betting_eligibility":"NOT_GRANTED","interpretation":"comp_master_id is captured as provider-supplied evidence but not automatically promoted to Oracle canonical ID. Verify documented semantics and exact crosswalk before approval.","counts":counts,"results":results}
(OUT/"identity-probe-summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps({"diagnostic":summary["diagnostic"],"generated_utc":summary["generated_utc"],"counts":counts,"results":[{k:r[k] for k in ("selected_season_id","country","competition","http_status","provider_success","identity_assessment","returned_fields","error_class")} for r in results]},indent=2,sort_keys=True))
