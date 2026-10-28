#!/usr/bin/env python3
"""Bounded research-only current fixture snapshot from FootyStats selected-50 seasons.

Makes one sequential league-matches request per selected season (50 total), no retries,
no raw response persistence, no production ledger writes. Output remains provider-native
and does not imply a FotMob/Oracle canonical bridge.
"""
import csv, json, os, re, time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OUT=Path("oracle-selected50-one-season-identity-probe"); OUT.mkdir(exist_ok=True)
manifest=Path("reports/oracle-footystats-selected-50-league-manifest-2026-10-24.md")
crosswalk=Path("reports/oracle-selected50-provider-identity-reconciliation-2026-10-27.csv")
if not manifest.is_file() or not crosswalk.is_file():
    raise SystemExit("Required selected-50 manifest/crosswalk missing; zero requests made.")
selected=[]
for line in manifest.read_text(encoding="utf-8").splitlines():
    m=re.match(r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$",line)
    if m: selected.append({"row":int(m.group(1)),"selected_season_id":m.group(2).strip(),"country":m.group(3).strip(),"competition":m.group(4).strip()})
if len(selected)!=50 or len({x["selected_season_id"] for x in selected})!=50:
    raise SystemExit("Manifest guard failed: expected 50 unique selected season IDs; zero requests made.")
with crosswalk.open(encoding="utf-8",newline="") as f:
    cross={r["selected_manifest_id"]:r for r in csv.DictReader(f)}
for x in selected:
    r=cross.get(x["selected_season_id"],{})
    x["provider_comp_master_id_observed"]=r.get("provider_comp_master_id_observed","")
    x["provider_master_id_semantic_status"]=r.get("provider_master_id_semantic_status","REVIEW_REQUIRED_NOT_CANONICAL")
key=os.environ.get("FOOTYSTATS_API_KEY","").strip()
if not key: raise SystemExit("FOOTYSTATS_API_KEY missing; zero requests made.")
now=datetime.now(timezone.utc); now_ts=int(now.timestamp())
past_cutoff=now_ts-int(timedelta(days=30).total_seconds())
future_cutoff=now_ts+int(timedelta(days=14).total_seconds())
fields=("id","homeID","awayID","home_name","away_name","season","status","roundID","game_week",
        "homeGoalCount","awayGoalCount","totalGoalCount","date_unix","competition_id","no_home_away",
        "home_ppg","away_ppg","pre_match_home_ppg","pre_match_away_ppg","btts_potential","o25_potential")
results=[]; all_window_matches=[]; request_failures=[]; pagination_gaps=[]
for item in selected:
    query={"key":key,"season_id":item["selected_season_id"],"max_per_page":1000}
    url="https://api.football-data-api.com/league-matches?"+urlencode(query)
    result={**item,"http_status":None,"provider_success":False,"returned_match_count":0,
            "max_page":None,"current_page":None,"error_class":None,"matches_in_window":0,
            "future_14d_count":0,"recent_completed_30d_count":0,"schedule_status":"UNVERIFIED"}
    payload=None
    try:
        req=Request(url,headers={"User-Agent":"Oracle-Selected50-Current-Fixture-Snapshot/1.0"})
        with urlopen(req,timeout=35) as response:
            result["http_status"]=response.status
            payload=json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        result["http_status"]=exc.code; result["error_class"]="HTTPError"
    except URLError as exc: result["error_class"]=type(exc).__name__
    except Exception as exc: result["error_class"]=type(exc).__name__
    if isinstance(payload,dict):
        result["provider_success"]=payload.get("success") is True
        pager=payload.get("pager") if isinstance(payload.get("pager"),dict) else {}
        result["max_page"]=pager.get("max_page"); result["current_page"]=pager.get("current_page")
        data=payload.get("data")
        if isinstance(data,list):
            result["returned_match_count"]=len(data)
            if result["max_page"] and int(result["max_page"])>1:
                pagination_gaps.append(item["selected_season_id"])
            for match in data:
                if not isinstance(match,dict): continue
                try: kick=int(match.get("date_unix") or 0)
                except (TypeError,ValueError): kick=0
                if not kick or kick<past_cutoff or kick>future_cutoff: continue
                clean={k:match.get(k) for k in fields if k in match and isinstance(match.get(k),(str,int,float,bool,type(None)))}
                clean.update({
                    "selected_season_id":item["selected_season_id"],
                    "provider_comp_master_id_observed":item["provider_comp_master_id_observed"],
                    "manifest_country":item["country"],"manifest_competition":item["competition"],
                    "kickoff_utc":datetime.fromtimestamp(kick,tz=timezone.utc).isoformat(),
                    "window_class":"FUTURE_14D" if kick>=now_ts else "RECENT_30D"
                })
                all_window_matches.append(clean); result["matches_in_window"]+=1
                if kick>=now_ts: result["future_14d_count"]+=1
                elif str(match.get("status","")).lower()=="complete": result["recent_completed_30d_count"]+=1
        if result["http_status"]==200 and result["provider_success"]:
            result["schedule_status"]="REQUIRES_PAGINATION" if result["max_page"] and int(result["max_page"])>1 else "ONE_PAGE_RESPONSE"
    if not (result["http_status"]==200 and result["provider_success"]):
        request_failures.append(item["selected_season_id"])
    results.append(result)
    time.sleep(0.15)

summary={
 "diagnostic":"BOUNDED_SELECTED50_CURRENT_FIXTURE_SNAPSHOT",
 "retrieved_utc":datetime.now(timezone.utc).isoformat(),
 "window_start_utc":datetime.fromtimestamp(past_cutoff,tz=timezone.utc).isoformat(),
 "window_end_utc":datetime.fromtimestamp(future_cutoff,tz=timezone.utc).isoformat(),
 "endpoint":"league-matches","selected_leagues":len(selected),
 "requests_planned":len(selected),"requests_attempted":sum(1 for x in results if x["http_status"] is not None or x["error_class"] is not None),
 "http_200_success":sum(1 for x in results if x["http_status"]==200 and x["provider_success"]),
 "request_failures":len(request_failures),"request_failure_season_ids":request_failures,
 "seasons_needing_pagination":pagination_gaps,"complete_one_page_responses":sum(1 for x in results if x["schedule_status"]=="ONE_PAGE_RESPONSE"),
 "seasons_with_future_14d_fixtures":sum(1 for x in results if x["future_14d_count"]>0),
 "future_14d_fixture_rows":sum(1 for x in all_window_matches if x["window_class"]=="FUTURE_14D"),
 "recent_completed_14d_rows":sum(1 for x in all_window_matches if x["window_class"]=="RECENT_14D" and str(x.get("status","")).lower()=="complete"),
 "raw_provider_payload_persisted":False,"api_key_persisted":False,"production_ledger_written":False,
 "production_eligibility":"NOT_GRANTED","betting_eligibility":"NOT_GRANTED",
 "identity_warning":"FootyStats-native season/team/match IDs only; comp_master_id semantics and FotMob/Oracle canonical bridge are not approved.",
 "fixture_rows":all_window_matches,"per_season":results
}
(OUT/"identity-probe-summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8")
print(json.dumps({k:v for k,v in summary.items() if k not in ("fixture_rows","per_season")},indent=2,sort_keys=True))
print("PER_SEASON_SUMMARY")
print(json.dumps([{k:r[k] for k in ("country","competition","selected_season_id","provider_comp_master_id_observed","http_status","provider_success","returned_match_count","max_page","future_14d_count","recent_completed_30d_count","schedule_status","error_class")} for r in results],indent=2,sort_keys=True))
