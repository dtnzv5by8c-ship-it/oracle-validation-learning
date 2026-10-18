#!/usr/bin/env python3
"""Read-only audit of OpenFoot coverage for Oracle's specifically requested competitions."""
import json, os, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
import requests

BASE = "https://openfootapi.com/v1"
KEY = os.getenv("OPENFOOT_API_KEY", "").strip()
OUT = Path("artifacts/openfoot_target_competition_coverage.json")
TARGETS = [
 ("Spain — Segunda División","Spain",["Segunda División","Segunda Division"],"league"),
 ("Argentina — Liga Profesional","Argentina",["Liga Profesional","Liga Profesional de Fútbol"],"league"),
 ("France — Ligue 2","France",["Ligue 2"],"league"),
 ("Portugal — Liga Portugal 2","Portugal",["Liga Portugal 2","Segunda Liga","Liga Portugal 2 Meu Super"],"league"),
 ("Ireland — Premier Division","Ireland",["League of Ireland Premier Division","Premier Division"],"league"),
 ("Belgium — Pro League","Belgium",["Pro League","Jupiler Pro League","Belgian Pro League"],"league"),
 ("Greece — Super League","Greece",["Super League","Super League Greece","Super League 1"],"league"),
 ("Romania — Liga I","Romania",["Superliga României","Superliga Romaniei","Superliga","Liga I","Romanian Liga I"],"league"),
 ("Iceland — Úrvalsdeild","Iceland",["Besta deildin","Úrvalsdeild","Urvalsdeild"],"league"),
 ("Peru — Liga 1","Peru",["Liga 1","Liga 1 Peru","Liga 1 Perú"],"league"),
 ("USA — MLS Next Pro","USA",["MLS Next Pro","MLS NEXT Pro"],"league"),
 ("Argentina — Copa Argentina","Argentina",["Copa Argentina","Copa Argentina AXION Energy"],"cup"),
 ("Portugal — Taça de Portugal","Portugal",["Taça de Portugal","Taca de Portugal","Taça de Portugal Placard","Taca de Portugal Placard","Portuguese Cup"],"cup"),
]
def norm(s): return re.sub(r"[^a-z0-9]+","",str(s or "").lower())
def rows(p):
    if isinstance(p,list): return p
    if isinstance(p,dict):
        for k in ("data","matches","competitions","standings","results","items","table"):
            v=p.get(k)
            if isinstance(v,list): return v
            if isinstance(v,dict):
                for kk in ("data","items","results","rows","standings"):
                    if isinstance(v.get(kk),list): return v[kk]
    return []
def get(path, params=None):
    try: r=requests.get(BASE+path,headers={"Accept":"application/json","Authorization":"Bearer "+KEY},params=params,timeout=30)
    except requests.RequestException as e: return None,{"status":"NETWORK_ERROR","exception_type":type(e).__name__}
    meta={"http_status":r.status_code}
    try: body=r.json()
    except Exception: body=None
    if r.status_code != 200:
        err=body.get("error",{}) if isinstance(body,dict) else {}
        if isinstance(err,dict) and err.get("code"): meta["provider_error_code"]=str(err["code"])
        meta["status"]="RATE_LIMIT_OR_QUOTA" if r.status_code==429 else "AUTH_OR_PLAN_RESTRICTION" if r.status_code in (401,403) else "NOT_FOUND_OR_UNAVAILABLE" if r.status_code==404 else "HTTP_ERROR"
        return None,meta
    if isinstance(body,dict) and isinstance(body.get("error"),dict) and body["error"].get("code"):
        meta.update({"status":"PROVIDER_ERROR_IN_200","provider_error_code":str(body["error"]["code"])})
        return body,meta
    meta["status"]="OK"
    return body,meta
def first(d, keys):
    if not isinstance(d,dict): return None
    return next((d[k] for k in keys if d.get(k) is not None and d.get(k)!=""),None)
def sample_fields(payload):
    rs=rows(payload)
    sample=rs[0] if rs and isinstance(rs[0],dict) else payload.get("data",payload) if isinstance(payload,dict) else {}
    if not isinstance(sample,dict): sample={}
    return {"rows_returned":len(rs),"sample_fields":sorted(sample.keys())[:80]}
def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    report={"generated_utc":datetime.now(timezone.utc).isoformat(),"mode":"READ_ONLY_TARGET_COMPETITION_FIELD_AUDIT","source":"OpenFoot API","credential_configured":bool(KEY),"credential_value_logged":False,"target_count":len(TARGETS),"targets":[],"governance":"No Oracle production code, predictions, calibration, or historical database is modified."}
    if not KEY:
        report["status"]="BLOCKED_NO_OPENFOOT_API_KEY"; OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n"); print(report["status"]); return 2
    cat,cm=get("/competitions"); report["catalogue_request"]=cm
    if cat is None or cm.get("status")!="OK":
        report["status"]="BLOCKED_CATALOGUE_REQUEST"; OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n"); print(report["status"]); return 1
    catalog=[]
    for c in rows(cat):
        if isinstance(c,dict):
            catalog.append({"id":first(c,("id","competitionId","competition_id","slug","code")),"name":first(c,("name","competitionName","competition_name","title","displayName")),"country":first(c,("country","countryName","country_name","nation")),"season":first(c,("season","currentSeason","current_season")),"coverage":c.get("coverage") if isinstance(c.get("coverage"),dict) else {}})
    report["catalogue_rows"]=len(catalog)
    for label,country,aliases,kind in TARGETS:
        matches=[c for c in catalog if norm(c["country"])==norm(country) and norm(c["name"]) in [norm(a) for a in aliases]]
        unique={str(c["id"]):c for c in matches if c.get("id")}
        rec={"target":label,"kind":kind,"mapping_status":"UNMAPPED","candidate_count":len(unique),"tests":{}}
        if len(unique)>1:
            rec["mapping_status"]="AMBIGUOUS"; rec["candidates"]=[{"id":c["id"],"name":c["name"],"country":c["country"]} for c in unique.values()]
            report["targets"].append(rec); continue
        if not unique:
            rec["mapping_status"]="NOT_IN_CATALOGUE"; rec["tests"]["fixtures"]={"status":"NOT_TESTED_NO_COMPETITION_ID"}
            report["targets"].append(rec); continue
        c=next(iter(unique.values())); cid=c["id"]; season=c.get("season")
        rec.update({"mapping_status":"MAPPED","competition_id":cid,"catalogue_name":c["name"],"catalogue_season":season,"season_freshness":"CURRENT_LABEL" if season in ("2026","2026/27","2026-2027") else ("UNVERIFIED" if not season else "STALE_OR_UNVERIFIED"),"catalogue_coverage":c["coverage"]})
        fx,fm=get("/matches",{"competition":cid,"season":season,"limit":10})
        frows=rows(fx) if fx is not None else []
        rec["tests"]["fixtures"]={**fm,"rows_returned":len(frows),"usable_sample":bool(frows)}
        if frows and isinstance(frows[0],dict):
            m=frows[0]; mid=first(m,("id","matchId","match_id"))
            home=first(m,("homeTeam","home_team","home")); away=first(m,("awayTeam","away_team","away"))
            def tid(t): return first(t,("id","teamId","team_id","key")) if isinstance(t,dict) else None
            rec["sample_fixture"]={"match_id_present":bool(mid),"kickoff_present":bool(first(m,("kickoffAt","date","kickoff","datetime"))),"home_team_id_present":bool(tid(home)),"away_team_id_present":bool(tid(away)),"score_field_present":first(m,("score","scores","homeScore")) is not None}
            if mid:
                cp,cm2=get("/matches/"+str(mid)+"/context")
                rec["tests"]["match_context"]={**cm2,**(sample_fields(cp) if cp is not None else {})}
            else: rec["tests"]["match_context"]={"status":"NOT_TESTED_NO_MATCH_ID"}
            if tid(home) and tid(away):
                hp,hm=get("/teams/"+str(tid(home))+"/h2h",{"opponent":str(tid(away))})
                rec["tests"]["h2h"]={**hm,**(sample_fields(hp) if hp is not None else {})}
            else: rec["tests"]["h2h"]={"status":"NOT_TESTED_TEAM_IDS_MISSING"}
        else:
            rec["tests"]["match_context"]={"status":"NOT_TESTED_NO_FIXTURE"}; rec["tests"]["h2h"]={"status":"NOT_TESTED_NO_FIXTURE"}
        if kind=="league":
            sp,sm=get("/standings",{"competition":cid,"season":season})
            rec["tests"]["standings"]={**sm,**(sample_fields(sp) if sp is not None else {})}
        report["targets"].append(rec); time.sleep(1.0)
    # xG endpoint is documented as Developer-tier. Probe once; avoid repeated calls if plan-gated.
    mapped=next((r for r in report["targets"] if r["mapping_status"]=="MAPPED" and r["kind"]=="league"),None)
    if mapped:
        xp,xm=get("/analytics/xg",{"league":mapped["competition_id"],"season":mapped["catalogue_season"]})
        report["xg_plan_probe"]={**xm,"competition_tested":mapped["target"],**(sample_fields(xp) if xp is not None else {})}
        if xm.get("status")!="OK": report["xg_plan_probe"]["note"]="Only one xG request was made; plan/access failure stops further xG calls."
        else:
            for r in report["targets"]:
                if r is mapped or r.get("mapping_status")!="MAPPED" or r.get("kind")!="league": continue
                xx,xm2=get("/analytics/xg",{"league":r["competition_id"],"season":r["catalogue_season"]})
                r["tests"]["league_xg"]={**xm2,**(sample_fields(xx) if xx is not None else {})}; time.sleep(1.0)
    report["summary"]={"mapped":sum(r["mapping_status"]=="MAPPED" for r in report["targets"]),"not_in_catalogue":sum(r["mapping_status"]=="NOT_IN_CATALOGUE" for r in report["targets"]),"ambiguous":sum(r["mapping_status"]=="AMBIGUOUS" for r in report["targets"]),"fixture_probes_ok_with_rows":sum(r.get("tests",{}).get("fixtures",{}).get("status")=="OK" and r.get("tests",{}).get("fixtures",{}).get("usable_sample") for r in report["targets"]),"fixture_empty_or_failed":sum(r["mapping_status"]=="MAPPED" and not (r.get("tests",{}).get("fixtures",{}).get("status")=="OK" and r.get("tests",{}).get("fixtures",{}).get("usable_sample")) for r in report["targets"]),"standings_probes_ok":sum(r.get("tests",{}).get("standings",{}).get("status")=="OK" for r in report["targets"]),"context_probes_ok":sum(r.get("tests",{}).get("match_context",{}).get("status")=="OK" for r in report["targets"]),"h2h_probes_ok":sum(r.get("tests",{}).get("h2h",{}).get("status")=="OK" for r in report["targets"])}
    required_ok = True
    for r in report["targets"]:
        if r.get("mapping_status") != "MAPPED":
            required_ok = False
            continue
        t = r.get("tests", {})
        if t.get("fixtures", {}).get("status") != "OK" or not t.get("fixtures", {}).get("usable_sample"):
            required_ok = False
        for endpoint in (["match_context", "h2h"] + (["standings"] if r.get("kind") == "league" else [])):
            if t.get(endpoint, {}).get("status") != "OK":
                required_ok = False\n    report["summary"]["required_feature_endpoints_passed"] = required_ok\n    report["status"]="AUDIT_COMPLETE" if required_ok else "AUDIT_COMPLETE_WITH_GAPS"
    OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"summary":report["summary"],"catalogue_rows":report["catalogue_rows"],"xg_plan_probe":report.get("xg_plan_probe"),"report":str(OUT)},ensure_ascii=False))
    return 0
if __name__=="__main__": sys.exit(main())
