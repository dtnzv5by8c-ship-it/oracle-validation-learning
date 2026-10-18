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
    try: r=requests.get(BASE+path,headers={"Accept":"application/json","Authorization":"Bearer "+KEY},params=params,timeout=12)
    except requests.RequestException as e: return None,{"status":"NETWORK_ERROR","exception_type":type(e).__name__}
    time.sleep(1.05)  # Respect OpenFoot's published 60 requests/minute Starter limit.
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
    # Many OpenFoot endpoints return useful records nested inside objects rather
    # than as top-level lists. Report nested population, not just HTTP 200.
    rs = rows(payload)
    root = payload if isinstance(payload, dict) else {}
    nested = {}
    def walk(obj, path="", depth=0):
        if depth > 3 or not isinstance(obj, dict):
            return
        for key, value in obj.items():
            p = f"{path}.{key}" if path else str(key)
            if isinstance(value, list):
                nested[p] = {"type": "list", "count": len(value),
                             "sample_item_fields": sorted(value[0].keys())[:40] if value and isinstance(value[0], dict) else []}
                for i, item in enumerate(value[:1]):
                    if isinstance(item, dict):
                        walk(item, p + "[0]", depth + 1)
            elif isinstance(value, dict):
                nested[p] = {"type": "object", "keys": sorted(value.keys())[:40],
                             "nonempty_values": sum(v not in (None, "", [], {}) for v in value.values())}
                walk(value, p, depth + 1)
    walk(root)
    return {
        "top_level_fields": sorted(root.keys())[:80],
        "top_level_rows_returned": len(rs),
        "nested_payloads": nested,
        "has_populated_nested_data": any(
            (v.get("count", 0) > 0 if v.get("type") == "list" else v.get("nonempty_values", 0) > 0)
            for v in nested.values()
        )
    }

def value_quality(payload, endpoint):
    """Check actual key values needed for match analysis, not just object presence."""
    root = payload.get("data", payload) if isinstance(payload, dict) else {}
    result = {"sample_values_checked": True}
    if endpoint == "match_context":
        home = root.get("home", {}) if isinstance(root, dict) else {}
        away = root.get("away", {}) if isinstance(root, dict) else {}
        analytics = root.get("analytics", {}) if isinstance(root, dict) else {}
        xg = analytics.get("expectedGoals", {}) if isinstance(analytics, dict) else {}
        result["teams"] = {
            side: {
                "team_name_present": bool((team.get("team") or {}).get("name")) if isinstance(team, dict) else False,
                "form_present": bool(team.get("form")) if isinstance(team, dict) else False,
                "form_sample": team.get("form") if isinstance(team, dict) else None,
                "form_length": len(str(team.get("form") or "")) if isinstance(team, dict) else 0,
                "form_is_wdl_sequence": bool(re.fullmatch(r"[WDL]{5}", str(team.get("form") or "").upper())) if isinstance(team, dict) else False,
                "goals_scored_last5_present": isinstance(team.get("goalsScoredLast5"), (int, float)) if isinstance(team, dict) else False,
                "goals_conceded_last5_present": isinstance(team.get("goalsConcededLast5"), (int, float)) if isinstance(team, dict) else False,
                "table_position_present": isinstance(team.get("tablePosition"), (int, float)) if isinstance(team, dict) else False,
                "goals_average_present": isinstance(team.get("goalsAverage"), (int, float)) if isinstance(team, dict) else False,
                "form_freshness": (root.get("freshness") or {}).get("form") if isinstance(root.get("freshness"), dict) else None
            } for side, team in (("home", home), ("away", away))
        }
        result["xg_values"] = {
            "home_xg_present": isinstance(xg.get("homeXG"), (int, float)),
            "away_xg_present": isinstance(xg.get("awayXG"), (int, float)),
            "total_xg_present": isinstance(xg.get("totalExpectedGoals"), (int, float))
        }
        result["match_date_present"] = bool((root.get("match") or {}).get("kickoffAt")) if isinstance(root, dict) else False
        result["score_values_present"] = all(isinstance(v, (int, float)) for v in ((root.get("match") or {}).get("score") or {}).values()) if isinstance(root, dict) else False
    elif endpoint == "h2h":
        meetings = root.get("recentMeetings", []) if isinstance(root, dict) else []
        result["meeting_count"] = len(meetings) if isinstance(meetings, list) else 0
        result["meetings_with_date"] = sum(bool(m.get("date")) for m in meetings if isinstance(m, dict)) if isinstance(meetings, list) else 0
        result["meetings_with_numeric_score"] = sum(
            isinstance((m.get("score") or {}).get("home"), (int, float)) and
            isinstance((m.get("score") or {}).get("away"), (int, float))
            for m in meetings if isinstance(m, dict)
        ) if isinstance(meetings, list) else 0
        result["summary_total_matches"] = (root.get("summary") or {}).get("totalMatches") if isinstance(root.get("summary"), dict) else None
    elif endpoint == "standings":
        table = root.get("table", []) if isinstance(root, dict) else []
        result["table_rows"] = len(table) if isinstance(table, list) else 0
        result["rows_with_position_points_gd"] = sum(
            isinstance(row.get("position"), (int, float)) and
            isinstance((row.get("total") or {}).get("points"), (int, float)) and
            isinstance((row.get("total") or {}).get("goalDifference"), (int, float))
            for row in table if isinstance(row, dict)
        ) if isinstance(table, list) else 0
        result["standings_season"] = root.get("season") if isinstance(root, dict) else None
    return result
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
            rec["mapping_status"]="NOT_IN_CATALOGUE"
            # Preserve nearby catalogue entries to diagnose aliases/country labels.
            country_aliases = {
                "USA": {"usa", "united states", "united states of america", "us"},
                "Ireland": {"ireland", "republic of ireland"},
                "Greece": {"greece", "hellas"},
                "Iceland": {"iceland"},
                "Argentina": {"argentina"},
                "Portugal": {"portugal"},
            }.get(country, {country.lower()})
            tokens = [norm(a) for a in aliases]
            candidates = []
            for item in catalog:
                cname = norm(item.get("country"))
                nname = norm(item.get("name"))
                same_country = cname in {norm(x) for x in country_aliases}
                name_related = any(tok and (tok in nname or nname in tok) for tok in tokens)
                if same_country and name_related:
                    candidates.append({"id": item.get("id"), "name": item.get("name"),
                                       "country": item.get("country"), "season": item.get("season")})
            rec["nearby_catalogue_candidates"] = candidates[:15]
            rec["tests"]["fixtures"]={"status":"NOT_TESTED_NO_COMPETITION_ID"}
            report["targets"].append(rec); continue
        c=next(iter(unique.values())); cid=c["id"]; season=c.get("season")
        rec.update({"mapping_status":"MAPPED","competition_id":cid,"catalogue_name":c["name"],"catalogue_season":season,"season_freshness":"CURRENT_LABEL" if season in ("2026","2026/27","2026-2027") else ("UNVERIFIED" if not season else "STALE_OR_UNVERIFIED"),"catalogue_coverage":c["coverage"]})
        fx,fm=get("/matches",{"competition":cid,"season":season,"limit":10})
        frows=rows(fx) if fx is not None else []
        rec["tests"]["fixtures"]={**fm,"rows_returned":len(frows),"usable_sample":bool(frows)}
        def tid(t): return first(t,("id","teamId","team_id","key")) if isinstance(t,dict) else None
        sampled_checks=[]
        sample_matches=[m for m in frows[:3] if isinstance(m,dict)]
        for idx,m in enumerate(sample_matches):
            mid=first(m,("id","matchId","match_id"))
            home=first(m,("homeTeam","home_team","home")); away=first(m,("awayTeam","away_team","away"))
            check={"match_id_present":bool(mid),"kickoff_present":bool(first(m,("kickoffAt","date","kickoff","datetime"))),"home_team_id_present":bool(tid(home)),"away_team_id_present":bool(tid(away)),"context_status":"NOT_TESTED","h2h_status":"NOT_TESTED"}
            cp=None; hp=None
            if mid:
                cp,cm2=get("/matches/"+str(mid)+"/context")
                cq=value_quality(cp,"match_context") if cp is not None else {}
                check["context_status"]=cm2.get("status")
                teams=cq.get("teams",{})
                check["complete_form_and_goals"]=all(teams.get(side,{}).get("form_is_wdl_sequence") and teams.get(side,{}).get("goals_scored_last5_present") and teams.get(side,{}).get("goals_conceded_last5_present") for side in ("home","away"))
                xgv=cq.get("xg_values",{})
                check["xg_both_teams_present"]=bool(xgv.get("home_xg_present") and xgv.get("away_xg_present"))
                check["match_date_present"]=bool(cq.get("match_date_present"))
                if idx==0:
                    rec["sample_fixture"]={"match_id_present":check["match_id_present"],"kickoff_present":check["kickoff_present"],"home_team_id_present":check["home_team_id_present"],"away_team_id_present":check["away_team_id_present"],"score_field_present":first(m,("score","scores","homeScore")) is not None}
                    rec["tests"]["match_context"]={**cm2,**sample_fields(cp),**cq}
            else:
                check.update({"complete_form_and_goals":False,"xg_both_teams_present":False,"match_date_present":False})
                if idx==0: rec["tests"]["match_context"]={"status":"NOT_TESTED_NO_MATCH_ID"}
            if tid(home) and tid(away):
                hp,hm=get("/teams/"+str(tid(home))+"/h2h",{"opponent":str(tid(away))})
                hq=value_quality(hp,"h2h") if hp is not None else {}
                check["h2h_status"]=hm.get("status")
                check["h2h_meeting_count"]=hq.get("meeting_count",0)
                check["h2h_scored_meetings"]=hq.get("meetings_with_numeric_score",0)
                check["h2h_dated_meetings"]=hq.get("meetings_with_date",0)
                if idx==0: rec["tests"]["h2h"]={**hm,**sample_fields(hp),**hq}
            else:
                check.update({"h2h_meeting_count":0,"h2h_scored_meetings":0,"h2h_dated_meetings":0})
                if idx==0: rec["tests"]["h2h"]={"status":"NOT_TESTED_TEAM_IDS_MISSING"}
            sampled_checks.append(check)
            time.sleep(0.15)
        if not sample_matches:
            rec["tests"]["match_context"]={"status":"NOT_TESTED_NO_FIXTURE"}
            rec["tests"]["h2h"]={"status":"NOT_TESTED_NO_FIXTURE"}
        rec["tests"]["multi_fixture_validation"]={
            "sample_size":len(sampled_checks),
            "fixtures_with_complete_form_and_last5_goals":sum(bool(x.get("complete_form_and_goals")) for x in sampled_checks),
            "fixtures_with_both_xg_values":sum(bool(x.get("xg_both_teams_present")) for x in sampled_checks),
            "fixtures_with_match_date":sum(bool(x.get("match_date_present")) for x in sampled_checks),
            "fixtures_with_at_least_five_scored_h2h_meetings":sum((x.get("h2h_meeting_count",0) or 0)>=5 and (x.get("h2h_scored_meetings",0) or 0)>=5 for x in sampled_checks),
            "sample_checks":sampled_checks
        }
        if kind=="league":
            sp,sm=get("/standings",{"competition":cid,"season":season})
            rec["tests"]["standings"]={**sm,**(sample_fields(sp) if sp is not None else {}),**(value_quality(sp,"standings") if sp is not None else {})}
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
    report["summary"]={"mapped":sum(r["mapping_status"]=="MAPPED" for r in report["targets"]),"not_in_catalogue":sum(r["mapping_status"]=="NOT_IN_CATALOGUE" for r in report["targets"]),"ambiguous":sum(r["mapping_status"]=="AMBIGUOUS" for r in report["targets"]),"fixture_probes_ok_with_rows":sum(r.get("tests",{}).get("fixtures",{}).get("status")=="OK" and r.get("tests",{}).get("fixtures",{}).get("usable_sample") for r in report["targets"]),"fixture_empty_or_failed":sum(r["mapping_status"]=="MAPPED" and not (r.get("tests",{}).get("fixtures",{}).get("status")=="OK" and r.get("tests",{}).get("fixtures",{}).get("usable_sample")) for r in report["targets"]),"standings_probes_ok":sum(r.get("tests",{}).get("standings",{}).get("status")=="OK" and r.get("tests",{}).get("standings",{}).get("has_populated_nested_data") for r in report["targets"]),"context_probes_ok":sum(r.get("tests",{}).get("match_context",{}).get("status")=="OK" and r.get("tests",{}).get("match_context",{}).get("has_populated_nested_data") for r in report["targets"]),"h2h_probes_ok":sum(r.get("tests",{}).get("h2h",{}).get("status")=="OK" and r.get("tests",{}).get("h2h",{}).get("has_populated_nested_data") for r in report["targets"]), "h2h_with_scored_meetings":sum((r.get("tests",{}).get("h2h",{}).get("meetings_with_numeric_score",0) or 0)>0 for r in report["targets"]), "context_with_both_teams_recent_goals":sum(all(r.get("tests",{}).get("match_context",{}).get("teams",{}).get(side,{}).get("goals_scored_last5_present") and r.get("tests",{}).get("match_context",{}).get("teams",{}).get(side,{}).get("goals_conceded_last5_present") for side in ("home","away")) for r in report["targets"]), "standings_with_numeric_core_fields":sum(r.get("tests",{}).get("standings",{}).get("rows_with_position_points_gd",0)>0 for r in report["targets"])}
    required_ok = True
    for r in report["targets"]:
        if r.get("mapping_status") != "MAPPED":
            required_ok = False
            continue
        t = r.get("tests", {})
        if t.get("fixtures", {}).get("status") != "OK" or not t.get("fixtures", {}).get("usable_sample"):
            required_ok = False
        for endpoint in (["match_context", "h2h"] + (["standings"] if r.get("kind") == "league" else [])):
            result = t.get(endpoint, {})
            if result.get("status") != "OK" or not result.get("has_populated_nested_data"):
                required_ok = False
    # Field-level acceptance labels for the report; these do not alter Oracle.
    for r in report["targets"]:
        tests = r.get("tests", {})
        ctx = tests.get("match_context", {})
        h2h = tests.get("h2h", {})
        standings = tests.get("standings", {})
        team_values = ctx.get("teams", {})
        multi = tests.get("multi_fixture_validation", {})
        sample_size = multi.get("sample_size", 0) or 0
        complete_form_samples = multi.get("fixtures_with_complete_form_and_last5_goals", 0) or 0
        complete_xg_samples = multi.get("fixtures_with_both_xg_values", 0) or 0
        complete_h2h_samples = multi.get("fixtures_with_at_least_five_scored_h2h_meetings", 0) or 0
        both_goals = all(
            team_values.get(side, {}).get("goals_scored_last5_present") and
            team_values.get(side, {}).get("goals_conceded_last5_present")
            for side in ("home", "away")
        )
        form_present = all(team_values.get(side, {}).get("form_is_wdl_sequence") for side in ("home", "away"))
        sample_threshold = max(1, int(sample_size * 0.8 + 0.999)) if sample_size else 1
        season_label = str(r.get("catalogue_season") or "")
        season_current = season_label in ("2026", "2026/27", "2026-2027")
        xg_context = bool(ctx.get("xg_values", {}).get("home_xg_present") and ctx.get("xg_values", {}).get("away_xg_present"))
        xg_endpoint = tests.get("league_xg", {})
        if not xg_endpoint and report.get("xg_plan_probe", {}).get("competition_tested") == r.get("target"):
            xg_endpoint = report.get("xg_plan_probe", {})
        h2h_count = h2h.get("meeting_count", 0) or 0
        h2h_scored = h2h.get("meetings_with_numeric_score", 0) or 0
        table_count = standings.get("table_rows", 0) or 0
        table_core = standings.get("rows_with_position_points_gd", 0) or 0
        fx_ok = tests.get("fixtures", {}).get("status") == "OK" and tests.get("fixtures", {}).get("usable_sample")
        r["field_acceptance"] = {
            "fixtures": "SUPPORTED" if fx_ok else "UNSUPPORTED",
            "recent_form_and_last5_goals": "SUPPORTED" if sample_size and complete_form_samples >= sample_threshold else ("PARTIAL" if complete_form_samples > 0 or (form_present and both_goals) else "UNSUPPORTED"),
            "h2h": "SUPPORTED" if sample_size and complete_h2h_samples >= sample_threshold else ("PARTIAL" if (sample_size and complete_h2h_samples > 0) or (h2h_count > 0 and h2h_scored > 0) else "UNSUPPORTED"),
            "standings": "SUPPORTED" if table_count > 0 and table_core > 0 and season_current else ("PARTIAL" if table_count > 0 and table_core > 0 else ("NOT_APPLICABLE" if r.get("kind") == "cup" else "UNSUPPORTED")),
            "xg_in_match_context": "SUPPORTED" if sample_size and complete_xg_samples >= sample_threshold and r.get("catalogue_coverage", {}).get("advancedStats") is True else ("PARTIAL" if complete_xg_samples > 0 or xg_context else "UNSUPPORTED"),
            "league_xg_endpoint": "SUPPORTED" if xg_endpoint.get("status") == "OK" and xg_endpoint.get("has_populated_nested_data") else ("UNSUPPORTED" if xg_endpoint.get("status") in ("NOT_FOUND_OR_UNAVAILABLE", "AUTH_OR_PLAN_RESTRICTION", "RATE_LIMIT_OR_QUOTA") else "UNVERIFIED")
        }
    report["summary"]["required_feature_endpoints_passed"] = required_ok
    report["summary"]["competitions_with_multi_fixture_samples"] = sum((r.get("tests", {}).get("multi_fixture_validation", {}).get("sample_size", 0) or 0) >= 3 for r in report["targets"])
    report["summary"]["field_acceptance_counts"] = {
        field: {status: sum(r.get("field_acceptance", {}).get(field) == status for r in report["targets"])
                for status in ("SUPPORTED", "PARTIAL", "UNSUPPORTED", "NOT_APPLICABLE")}
        for field in ("fixtures", "recent_form_and_last5_goals", "h2h", "standings", "xg_in_match_context", "league_xg_endpoint")
    }
    # Final acceptance requires every requested competition mapped and all requested
    # data classes supported. A successful HTTP workflow alone is never acceptance.
    required_fields = ("fixtures", "recent_form_and_last5_goals", "h2h", "xg_in_match_context")
    final_acceptance = True
    for r in report["targets"]:
        fa = r.get("field_acceptance", {})
        if r.get("mapping_status") != "MAPPED":
            final_acceptance = False
            continue
        if any(fa.get(field) != "SUPPORTED" for field in required_fields):
            final_acceptance = False
        if r.get("kind") == "league" and fa.get("standings") != "SUPPORTED":
            final_acceptance = False
        if fa.get("league_xg_endpoint") != "SUPPORTED":
            final_acceptance = False
    report["summary"]["final_acceptance_passed"] = final_acceptance
    report["status"]="AUDIT_COMPLETE" if final_acceptance else "AUDIT_COMPLETE_WITH_GAPS"
    OUT.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"summary":report["summary"],"catalogue_rows":report["catalogue_rows"],"xg_plan_probe":report.get("xg_plan_probe"),"report":str(OUT)},ensure_ascii=False))
    return 0
if __name__=="__main__": sys.exit(main())
