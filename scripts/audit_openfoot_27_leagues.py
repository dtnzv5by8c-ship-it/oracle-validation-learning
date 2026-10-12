#!/usr/bin/env python3
"""Read-only authenticated OpenFoot coverage audit for Oracle's governed 27 leagues.

Makes one competition-catalogue request, then at most one fixture request for
each uniquely mapped competition. Never writes to Oracle's historical database,
never logs credentials, and never treats a missing field as covered.
"""
import json, os, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE = "https://openfootapi.com/v1"
KEY = os.getenv("OPENFOOT_API_KEY", "").strip()
OUT = Path("artifacts/openfoot_27_league_coverage.json")
LEAGUES = [
("E0","England",["Premier League","English Premier League"]),
("E1","England",["Championship","EFL Championship","English Championship"]),
("E2","England",["League One","League One England","EFL League One"]),
("E3","England",["League Two","League Two England","EFL League Two"]),
("SP1","Spain",["La Liga","Primera División","Primera Division"]),
("SP2","Spain",["Segunda División","Segunda Division","LaLiga 2"]),
("D1","Germany",["Bundesliga","German Bundesliga"]),
("D2","Germany",["2. Bundesliga","2 Bundesliga","2nd Bundesliga"]),
("I1","Italy",["Serie A","Serie A Italy"]),
("I2","Italy",["Serie B","Serie B Italy"]),
("F1","France",["Ligue 1","Ligue 1 France"]),
("F2","France",["Ligue 2","Ligue 2 France"]),
("N1","Netherlands",["Eredivisie","Dutch Eredivisie"]),
("NED2","Netherlands",["Eerste Divisie","Keuken Kampioen Divisie"]),
("P1","Portugal",["Primeira Liga","Liga Portugal","Liga Portugal Betclic"]),
("POR2","Portugal",["Liga Portugal 2","Segunda Liga","Liga Portugal 2 Meu Super"]),
("T1","Turkey",["Turkish Super Lig","Süper Lig","Super Lig"]),
("B1","Belgium",["Belgian Pro League","Jupiler Pro League","Pro League"]),
("SC0","Scotland",["Scottish Premiership","Premiership Scotland"]),
("AUT","Austria",["Austrian Bundesliga","Bundesliga Austria"]),
("SWZ","Switzerland",["Swiss Super League","Super League Switzerland"]),
("POL","Poland",["Ekstraklasa","Polish Ekstraklasa"]),
("ROU","Romania",["Romanian Liga I","SuperLiga","Superliga României","Liga I"]),
("CZE","Czech Republic",["Czech First League","Czech First Football League","Chance Liga","1. Liga"]),
("CRO","Croatia",["Croatian HNL","HNL","Croatian Football League"]),
("UKR","Ukraine",["Ukrainian Premier League","Premier League Ukraine","UPL"]),
("RSA","South Africa",["South African PSL","South African Premier Division","Betway Premiership","Premier Soccer League"]),
]
def norm(s):
    return re.sub(r"[^a-z0-9]+","",str(s or "").lower())
def first(d, keys):
    if not isinstance(d,dict): return ""
    for k in keys:
        v=d.get(k)
        if isinstance(v,(str,int,float)) and str(v).strip(): return str(v).strip()
    return ""
def rows_from(payload):
    if isinstance(payload,list): return payload
    if isinstance(payload,dict):
        for k in ("data","competitions","results","items","matches"):
            v=payload.get(k)
            if isinstance(v,list): return v
            if isinstance(v,dict):
                for kk in ("data","items","results"): 
                    if isinstance(v.get(kk),list): return v[kk]
    return []
def get_json(url, headers, params=None):
    try:
        r=requests.get(url,headers=headers,params=params,timeout=35)
    except requests.RequestException as exc:
        # Record only the exception class; never include URLs, headers, or credentials.
        return None,{"error_class":"NETWORK_ERROR","exception_type":type(exc).__name__}
    safe={"http_status":r.status_code}
    if r.status_code != 200:
        # OpenFoot commonly returns 429 when the account's request quota/rate limit
        # has been reached. Capture only non-sensitive diagnostic headers.
        if r.status_code == 429:
            safe["error_class"]="RATE_LIMIT_OR_QUOTA_EXCEEDED"
            for header in ("Retry-After","X-RateLimit-Limit","X-RateLimit-Remaining","X-RateLimit-Reset"):
                value=r.headers.get(header)
                if value is not None:
                    safe[header.lower().replace("-","_")]=value
        else:
            safe["error_class"]="HTTP_ERROR"
        # Deliberately do not store response body or request URL (which may contain data).
        return None,safe
    try: return r.json(),safe
    except ValueError: return None,{"http_status":r.status_code,"error_class":"INVALID_JSON"}
def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    report={"generated_utc":datetime.now(timezone.utc).isoformat(),"source":"OpenFoot API","mode":"READ_ONLY_COVERAGE_AUDIT","league_universe_count":len(LEAGUES),"credential_configured":bool(KEY),"credential_value_logged":False,"league_results":[],"feature_policy":"Fixture probe tests schedule endpoint only; result/event/xG/odds feature coverage is reported only where provider metadata explicitly declares it."}
    if not KEY:
        report["status"]="BLOCKED_NO_OPENFOOT_API_KEY"
        OUT.write_text(json.dumps(report,indent=2)+"\n")
        print(json.dumps({"status":report["status"],"report":str(OUT)})); return 2
    headers={"Accept":"application/json","Authorization":f"Bearer {KEY}"}
    payload,meta=get_json(BASE+"/competitions",headers)
    report["catalogue_request"]=meta
    if payload is None:
        report["status"]="OPENFOOT_RATE_LIMITED_OR_QUOTA_EXCEEDED" if meta.get("http_status")==429 else "CATALOGUE_REQUEST_FAILED"
        report["catalogue_error"]=meta.get("error_class")
        report["next_action"]="Check OpenFoot dashboard/account for remaining monthly requests and rate limits; rerun only after quota is available." if meta.get("http_status")==429 else "Check OpenFoot API status, endpoint documentation, and account access."
        OUT.write_text(json.dumps(report,indent=2)+"\n")
        print(json.dumps({"status":report["status"],"http_status":meta.get("http_status"),"error_class":meta.get("error_class"),"retry_after":meta.get("retry_after"),"rate_limit_remaining":meta.get("xratelimit_remaining"),"report":str(OUT)})); return 1
    catalogue=rows_from(payload)
    report["catalogue_rows"]=len(catalogue)
    # Keep a minimal sanitized catalogue for diagnostics; no raw payloads.
    safe_catalogue=[]
    for c in catalogue:
        if not isinstance(c,dict): continue
        safe_catalogue.append({
          "id":first(c,("id","competitionId","competition_id","slug","key","code")),
          "name":first(c,("name","competitionName","competition_name","title","displayName")),
          "country":first(c,("country","countryName","country_name","nation")),
          "season":first(c,("season","currentSeason","current_season")),
          "features":c.get("features") if isinstance(c.get("features"),(dict,list)) else None,
          "coverage":c.get("coverage") if isinstance(c.get("coverage"),(dict,list)) else None,
          "availableEndpoints":c.get("availableEndpoints") if isinstance(c.get("availableEndpoints"),list) else None
        })
    report["catalogue"]=safe_catalogue
    for code,country,aliases in LEAGUES:
        candidates=[]
        for c in safe_catalogue:
            cn=norm(c.get("country"))
            nm=norm(c.get("name"))
            country_ok=norm(country) in cn or cn in norm(country) if cn else False
            name_ok=any(norm(a)==nm or norm(a) in nm or nm in norm(a) for a in aliases if norm(a) and nm)
            if country_ok and name_ok: candidates.append(c)
        # A name-only exact match is recorded as ambiguous, never silently chosen.
        unique={str(c.get("id")):c for c in candidates if c.get("id")}
        rec={"oracle_league":code,"country":country,"aliases":aliases,"mapping_status":"UNMAPPED","candidate_count":len(unique),"candidates":list(unique.values()),"fixture_probe_status":"NOT_RUN","fixture_rows":None,"fixture_fields":[]}
        if len(unique)==1:
            c=next(iter(unique.values()))
            rec["mapping_status"]="MAPPED"
            rec["openfoot_competition_id"]=c["id"]
            # Keep the probe to one request/league and do not retry: this is a quota-safe audit.
            fixture_payload,fixture_meta=get_json(BASE+"/matches",headers,{"competition":c["id"],"season":"2026/27"})
            rec["fixture_probe_http_status"]=fixture_meta.get("http_status")
            if fixture_payload is not None:
                fixtures=rows_from(fixture_payload)
                rec["fixture_probe_status"]="OK"
                rec["fixture_rows"]=len(fixtures)
                if fixtures and isinstance(fixtures[0],dict):
                    rec["fixture_fields"]=sorted(str(k) for k in fixtures[0].keys())
                    sample=fixtures[0]
                    rec["sample_field_presence"]={
                      "fixture_id":any(k in sample for k in ("id","matchId","match_id")),
                      "date_or_kickoff":any(k in sample for k in ("date","kickoffAt","kickoff","startTime","datetime")),
                      "home_team":any(k in sample for k in ("homeTeam","home_team","home")),
                      "away_team":any(k in sample for k in ("awayTeam","away_team","away")),
                      "status":("status" in sample),
                      "scores":any(k in sample for k in ("homeScore","awayScore","score","scores"))
                    }
            else: rec["fixture_probe_status"]="HTTP_ERROR"
        elif len(unique)>1:
            rec["mapping_status"]="AMBIGUOUS"
        report["league_results"].append(rec)
        time.sleep(2.15)
    mapped=sum(x["mapping_status"]=="MAPPED" for x in report["league_results"])
    fixture_ok=sum(x["fixture_probe_status"]=="OK" for x in report["league_results"])
    report["summary"]={"mapped_competitions":mapped,"unmapped_or_ambiguous":len(LEAGUES)-mapped,"successful_fixture_probes":fixture_ok,"fixture_probe_errors":mapped-fixture_ok,"all_27_mapped_and_probeable":mapped==27 and fixture_ok==27}
    report["status"]="AUDIT_COMPLETE" if mapped==27 and fixture_ok==27 else "AUDIT_COMPLETE_WITH_GAPS"
    OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"summary":report["summary"],"catalogue_rows":len(catalogue),"report":str(OUT)},ensure_ascii=False))
    return 0
if __name__=="__main__": sys.exit(main())
