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
    # Retry only transient transport failures and HTTP 5xx. Do not retry 401/403, 404, or 429.
    attempts = 3
    for attempt in range(1, attempts + 1):
        try:
            r = requests.get(BASE+path, headers={"Accept":"application/json", "Authorization":"Bearer "+KEY}, params=params, timeout=12)
        except requests.RequestException as e:
            if attempt < attempts:
                time.sleep(1.5 * attempt)
                continue
            return None, {"status":"NETWORK_ERROR", "exception_type":type(e).__name__, "attempts":attempt, "retry_exhausted":True}
        if r.status_code >= 500 and attempt < attempts:
            time.sleep(1.5 * attempt)
            continue
        break
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
def standings_form_map(payload):
    """Extract valid five-match form only when a team name is present."""
    root = payload.get("data", payload) if isinstance(payload, dict) else {}
    table = root.get("table", []) if isinstance(root, dict) else []
    out = {}
    if not isinstance(table, list):
        return out
    for row in table:
        if not isinstance(row, dict):
            continue
        team = first(row, ("team", "club", "participant"))
        name = first(team, ("name", "teamName", "displayName")) if isinstance(team, dict) else None
        name = name or first(row, ("teamName", "team_name", "name", "clubName"))
        form = first(row, ("form", "recentForm", "lastFive", "last5"))
        if isinstance(form, list):
            form = "".join(str(x.get("result", x.get("outcome", "")) if isinstance(x, dict) else x) for x in form)
        form = re.sub(r"[^WDL]", "", str(form or "").upper())
        if name and re.fullmatch(r"[WDL]{5}", form):
            out[norm(name)] = {"team_name": name, "form": form}
    return out

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
            # Supplement the full catalogue with OpenFoot's documented fuzzy search.
            # Search hits are diagnostic only: never auto-map an ambiguous or approximate hit.
            search_queries = list(dict.fromkeys([aliases[0], label.split("—", 1)[-1].strip()]))[:2]
            search_evidence = []
            for query in search_queries:
                search_payload, search_meta = get("/search", {"q": query})
                search_rows = rows(search_payload) if search_payload is not None else []
                compact = []
                for item in search_rows[:10]:
                    if isinstance(item, dict):
                        compact.append({
                            "id": first(item, ("id", "competitionId", "competition_id", "teamId", "team_id", "slug", "code")),
                            "name": first(item, ("name", "competitionName", "competition_name", "title", "displayName")),
                            "country": first(item, ("country", "countryName", "country_name", "nation")),
                            "type": first(item, ("type", "entityType", "entity_type", "kind")),
                            "season": first(item, ("season", "currentSeason", "current_season"))
                        })
                search_evidence.append({"query": query, **search_meta, "result_count": len(search_rows), "results": compact})
            rec["provider_search_diagnostics"] = search_evidence
            rec["tests"]["fixtures"]={"status":"NOT_TESTED_NO_VERIFIED_COMPETITION_ID"}
            report["targets"].append(rec); continue
        c=next(iter(unique.values())); cid=c["id"]; season=c.get("season")
        rec.update({"mapping_status":"MAPPED","competition_id":cid,"catalogue_name":c["name"],"catalogue_season":season,"season_freshness":"CURRENT_LABEL" if season in ("2026","2026/27","2026-2027") else ("UNVERIFIED" if not season else "STALE_OR_UNVERIFIED"),"catalogue_coverage":c["coverage"]})
        if rec["season_freshness"] != "CURRENT_LABEL":
            # Verify stale/unclear season labels through provider search, without changing season.
            search_payload, search_meta = get("/search", {"q": c["name"] or label.split("—", 1)[-1].strip()})
            search_rows = rows(search_payload) if search_payload is not None else []
            rec["season_search_diagnostics"] = {
                "query": c["name"] or label.split("—", 1)[-1].strip(),
                **search_meta,
                "result_count": len(search_rows),
                "results": [{
                    "id": first(item, ("id", "competitionId", "competition_id", "slug", "code")),
                    "name": first(item, ("name", "competitionName", "competition_name", "title", "displayName")),
                    "country": first(item, ("country", "countryName", "country_name", "nation")),
                    "season": first(item, ("season", "currentSeason", "current_season")),
                    "seasons": item.get("seasons") if isinstance(item, dict) else None
                } for item in search_rows[:10] if isinstance(item, dict)]
            }
        fx,fm=get("/matches",{"competition":cid,"season":season,"limit":10})
        frows=rows(fx) if fx is not None else []
        rec["tests"]["fixtures"]={**fm,"rows_returned":len(frows),"usable_sample":bool(frows)}
        def tid(t): return first(t,("id","teamId","team_id","key")) if isinstance(t,dict) else None
        sampled_checks=[]
        sample_matches=[m for m in frows[:3] if isinstance(m,dict)]
        for idx,m in enumerate(sample_matches):
            mid=first(m,("id","matchId","match_id"))
            home=first(m,("homeTeam","home_team","home")); away=first(m,("awayTeam","away_team","away"))
            fixture_comp_obj = m.get("competition") if isinstance(m.get("competition"), dict) else {}
            fixture_comp_id = first(m,("competitionId","competition_id","leagueId","league_id")) or first(fixture_comp_obj,("id","competitionId","competition_id","slug","code"))
            check={"match_id_present":bool(mid),"kickoff_present":bool(first(m,("kickoffAt","date","kickoff","datetime"))),"home_team_id_present":bool(tid(home)),"away_team_id_present":bool(tid(away)),"fixture_competition_id":fixture_comp_id,"context_competition_id":None,"competition_identity_status":"NOT_VERIFIED","context_status":"NOT_TESTED","h2h_status":"NOT_TESTED"}
            cp=None; hp=None
            if mid:
                cp,cm2=get("/matches/"+str(mid)+"/context")
                cq=value_quality(cp,"match_context") if cp is not None else {}
                check["context_status"]=cm2.get("status")
                teams=cq.get("teams",{})
                context_root = cp.get("data", cp) if isinstance(cp, dict) else {}
                context_match = context_root.get("match", {}) if isinstance(context_root, dict) else {}
                context_comp_obj = context_match.get("competition") if isinstance(context_match.get("competition"), dict) else {}
                context_comp_id = first(context_match,("competitionId","competition_id","leagueId","league_id")) or first(context_comp_obj,("id","competitionId","competition_id","slug","code"))
                check["context_competition_id"] = context_comp_id
                observed_ids = [str(v) for v in (fixture_comp_id, context_comp_id) if v not in (None, "")]
                expected_id = str(cid)
                if any(v != expected_id for v in observed_ids):
                    check["competition_identity_status"] = "MISMATCH"
                elif observed_ids:
                    check["competition_identity_status"] = "VERIFIED"
                else:
                    check["competition_identity_status"] = "UNVERIFIED_ID_MISSING"
                for side in ("home", "away"):
                    side_obj = context_root.get(side, {}) if isinstance(context_root, dict) else {}
                    side_team = side_obj.get("team", {}) if isinstance(side_obj, dict) else {}
                    check[side+"_team_name"] = first(side_team, ("name", "teamName")) or first(side_obj, ("teamName", "team_name", "name"))
                    check[side+"_context_form"] = str(side_obj.get("form") or "").upper() if isinstance(side_obj, dict) else ""
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
                check["h2h_http_status"]=hm.get("http_status")
                check["h2h_provider_error_code"]=hm.get("provider_error_code")
                check["h2h_exception_type"]=hm.get("exception_type")
                check["h2h_attempts"]=hm.get("attempts", 1)
                check["h2h_retry_exhausted"]=bool(hm.get("retry_exhausted", False))
                check["h2h_meeting_count"]=hq.get("meeting_count",0)
                check["h2h_scored_meetings"]=hq.get("meetings_with_numeric_score",0)
                check["h2h_dated_meetings"]=hq.get("meetings_with_date",0)
                if idx==0: rec["tests"]["h2h"]={**hm,**sample_fields(hp),**hq}
            else:
                check.update({"h2h_meeting_count":0,"h2h_scored_meetings":0,"h2h_dated_meetings":0,"h2h_http_status":None,"h2h_provider_error_code":None,"h2h_exception_type":None})
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
            form_map = standings_form_map(sp) if sp is not None and sm.get("status") == "OK" else {}
            verified_fallbacks = 0
            verified_matches = 0
            for sample in sampled_checks:
                for side in ("home", "away"):
                    team_name = sample.get(side+"_team_name")
                    context_form = sample.get(side+"_context_form", "")
                    stand_form = form_map.get(norm(team_name)) if team_name else None
                    if stand_form:
                        verified_matches += 1
                        if not re.fullmatch(r"[WDL]{5}", context_form):
                            sample[side+"_standings_form_fallback"] = stand_form["form"]
                            sample[side+"_form_source"] = "standings_fallback_exact_team_name_match"
                            verified_fallbacks += 1
                        else:
                            sample[side+"_form_source"] = "match_context"
            rec["tests"]["standings_form_validation"] = {"standings_teams_with_valid_five_match_form":len(form_map),"sampled_team_name_matches_with_valid_standings_form":verified_matches,"verified_fallbacks_used_for_missing_context_form":verified_fallbacks,"fallback_is_reporting_only":True,"note":"Exact normalized team-name match and five-character W/D/L sequence required; fallback does not fill recent goals scored/conceded."}
            # Separate form completeness from the stricter form + last-five-goals requirement.
            # This is reporting-only and never feeds Oracle predictions.
            for sample in sampled_checks:
                valid_forms = []
                for side in ("home", "away"):
                    context_form = str(sample.get(side+"_context_form", "")).upper()
                    fallback_form = sample.get(side+"_standings_form_fallback", "")
                    valid_forms.append(bool(re.fullmatch(r"[WDL]{5}", context_form) or re.fullmatch(r"[WDL]{5}", fallback_form)))
                sample["both_teams_five_match_form_available"] = all(valid_forms)
            rec["tests"]["multi_fixture_validation"]["fixtures_with_both_teams_five_match_form"] = sum(bool(x.get("both_teams_five_match_form_available")) for x in sampled_checks)
            rec["tests"]["multi_fixture_validation"]["form_completeness_is_reporting_only"] = True
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
    report["summary"]={"mapped":sum(r["mapping_status"]=="MAPPED" for r in report["targets"]),"not_in_catalogue":sum(r["mapping_status"]=="NOT_IN_CATALOGUE" for r in report["targets"]),"ambiguous":sum(r["mapping_status"]=="AMBIGUOUS" for r in report["targets"]),"fixture_probes_ok_with_rows":sum(r.get("tests",{}).get("fixtures",{}).get("status")=="OK" and r.get("tests",{}).get("fixtures",{}).get("usable_sample") for r in report["targets"]),"fixture_empty_or_failed":sum(r["mapping_status"]=="MAPPED" and not (r.get("tests",{}).get("fixtures",{}).get("status")=="OK" and r.get("tests",{}).get("fixtures",{}).get("usable_sample")) for r in report["targets"]),"standings_probes_ok":sum(r.get("tests",{}).get("standings",{}).get("status")=="OK" and r.get("tests",{}).get("standings",{}).get("has_populated_nested_data") for r in report["targets"]),"context_probes_ok":sum(r.get("tests",{}).get("match_context",{}).get("status")=="OK" and r.get("tests",{}).get("match_context",{}).get("has_populated_nested_data") for r in report["targets"]),"h2h_probes_ok":sum(r.get("tests",{}).get("h2h",{}).get("status")=="OK" and r.get("tests",{}).get("h2h",{}).get("has_populated_nested_data") for r in report["targets"]), "h2h_with_scored_meetings":sum((r.get("tests",{}).get("h2h",{}).get("meetings_with_numeric_score",0) or 0)>0 for r in report["targets"]), "context_with_both_teams_recent_goals":sum(all(r.get("tests",{}).get("match_context",{}).get("teams",{}).get(side,{}).get("goals_scored_last5_present") and r.get("tests",{}).get("match_context",{}).get("teams",{}).get(side,{}).get("goals_conceded_last5_present") for side in ("home","away")) for r in report["targets"]), "standings_with_numeric_core_fields":sum(r.get("tests",{}).get("standings",{}).get("rows_with_position_points_gd",0)>0 for r in report["targets"]), "h2h_transient_retries_exhausted":sum(bool(x.get("h2h_retry_exhausted")) for r in report["targets"] for x in r.get("tests",{}).get("multi_fixture_validation",{}).get("sample_checks",[])), "verified_standings_form_fallbacks":sum(r.get("tests",{}).get("standings_form_validation",{}).get("verified_fallbacks_used_for_missing_context_form",0) for r in report["targets"])}
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
        form_only_samples = multi.get("fixtures_with_both_teams_five_match_form", 0) or 0
        complete_xg_samples = multi.get("fixtures_with_both_xg_values", 0) or 0
        complete_h2h_samples = multi.get("fixtures_with_at_least_five_scored_h2h_meetings", 0) or 0
        any_h2h_data = any((x.get("h2h_meeting_count", 0) or 0) > 0 and (x.get("h2h_scored_meetings", 0) or 0) > 0 for x in multi.get("sample_checks", []))
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
        # Keep xG evidence layers independent: observed match-context values, the
        # provider's catalogue capability flag, and the dedicated league endpoint
        # are different facts and must not be conflated.
        observed_xg_pct = (complete_xg_samples / sample_size) if sample_size else 0.0
        catalogue_advanced_stats = r.get("catalogue_coverage", {}).get("advancedStats")
        r["xg_diagnostics"] = {
            "sample_size": sample_size,
            "fixtures_with_both_home_away_xg": complete_xg_samples,
            "observed_match_context_xg_coverage_pct": round(100 * observed_xg_pct, 1),
            "observed_xg_evidence": "OBSERVED_IN_SAMPLE" if complete_xg_samples else "NOT_OBSERVED_IN_SAMPLE",
            "catalogue_advanced_stats_flag": catalogue_advanced_stats,
            "catalogue_flag_interpretation": "DECLARED_SUPPORTED" if catalogue_advanced_stats is True else "DECLARED_UNSUPPORTED" if catalogue_advanced_stats is False else "NOT_DECLARED",
            "dedicated_league_xg_endpoint_status": xg_endpoint.get("status", "NOT_TESTED"),
            "interpretation": "Observed sample values do not prove full competition coverage; catalogue flags do not negate directly observed match-context values."
        }
        r["field_acceptance"] = {
            "fixtures": "SUPPORTED" if fx_ok else "UNSUPPORTED",
            "recent_form_only": "SUPPORTED" if sample_size and form_only_samples >= sample_threshold else ("PARTIAL" if form_only_samples > 0 or form_present else "UNSUPPORTED"),
            "recent_form_and_last5_goals": "SUPPORTED" if sample_size and complete_form_samples >= sample_threshold else ("PARTIAL" if complete_form_samples > 0 or (form_present and both_goals) else "UNSUPPORTED"),
            "h2h": "SUPPORTED" if sample_size and complete_h2h_samples >= sample_threshold else ("PARTIAL" if (sample_size and complete_h2h_samples > 0) or any_h2h_data else "UNSUPPORTED"),
            "standings": "SUPPORTED" if table_count > 0 and table_core > 0 and season_current else ("PARTIAL" if table_count > 0 and table_core > 0 else ("NOT_APPLICABLE" if r.get("kind") == "cup" else "UNSUPPORTED")),
            "xg_in_match_context": "SUPPORTED" if sample_size and complete_xg_samples >= sample_threshold else ("PARTIAL" if complete_xg_samples > 0 or xg_context else "UNSUPPORTED"),
            "league_xg_endpoint": "SUPPORTED" if xg_endpoint.get("status") == "OK" and xg_endpoint.get("has_populated_nested_data") else ("UNSUPPORTED" if xg_endpoint.get("status") in ("NOT_FOUND_OR_UNAVAILABLE", "AUTH_OR_PLAN_RESTRICTION", "RATE_LIMIT_OR_QUOTA") else "UNVERIFIED")
        }
    # Aggregate H2H quality across every sampled fixture, not only the first
    # fixture's endpoint payload. Empty successful responses are distinct from
    # request/network failures and from meetings with incomplete scores/dates.
    h2h_samples = [x for r in report["targets"] for x in r.get("tests", {}).get("multi_fixture_validation", {}).get("sample_checks", [])]
    h2h_ok = [x for x in h2h_samples if x.get("h2h_status") == "OK"]
    h2h_failed = [x for x in h2h_samples if x.get("h2h_status") not in (None, "OK", "NOT_TESTED")]
    h2h_with_meetings = [x for x in h2h_ok if (x.get("h2h_meeting_count", 0) or 0) > 0]
    report["summary"]["competition_identity_diagnostics"] = {
        "sampled_fixtures": len([x for x in h2h_samples if x.get("match_id_present")]),
        "verified": sum(x.get("competition_identity_status") == "VERIFIED" for x in h2h_samples),
        "mismatches": sum(x.get("competition_identity_status") == "MISMATCH" for x in h2h_samples),
        "unverified_id_missing": sum(x.get("competition_identity_status") == "UNVERIFIED_ID_MISSING" for x in h2h_samples),
        "mismatch_details": [
            {"target": r.get("target"), "fixture_competition_id": x.get("fixture_competition_id"), "context_competition_id": x.get("context_competition_id"), "expected_competition_id": r.get("competition_id")}
            for r in report["targets"] for x in r.get("tests", {}).get("multi_fixture_validation", {}).get("sample_checks", [])
            if x.get("competition_identity_status") == "MISMATCH"
        ],
        "interpretation": "Competition identity is verified only when at least one fixture/context competition ID is present and every observed ID matches the mapped target ID."
    }
    report["summary"]["h2h_diagnostics"] = {
        "http_status_counts": {
            str(code): sum(str(x.get("h2h_http_status")) == str(code) for x in h2h_samples)
            for code in sorted({x.get("h2h_http_status") for x in h2h_samples if x.get("h2h_http_status") is not None}, key=lambda v: str(v))
        },
        "provider_error_code_counts": {
            str(code): sum(str(x.get("h2h_provider_error_code")) == str(code) for x in h2h_samples)
            for code in sorted({x.get("h2h_provider_error_code") for x in h2h_samples if x.get("h2h_provider_error_code")}, key=lambda v: str(v))
        },
        "exception_type_counts": {
            str(code): sum(str(x.get("h2h_exception_type")) == str(code) for x in h2h_samples if x.get("h2h_exception_type") is not None)
            for code in sorted({x.get("h2h_exception_type") for x in h2h_samples if x.get("h2h_exception_type")}, key=lambda v: str(v))
        },
        "sampled_requests": len([x for x in h2h_samples if x.get("h2h_status") not in (None, "NOT_TESTED")]),
        "successful_requests": len(h2h_ok),
        "successful_empty_meeting_responses": sum((x.get("h2h_meeting_count", 0) or 0) == 0 for x in h2h_ok),
        "successful_responses_with_meetings": len(h2h_with_meetings),
        "responses_with_meetings_and_at_least_one_scored_meeting": sum((x.get("h2h_scored_meetings", 0) or 0) > 0 for x in h2h_with_meetings),
        "responses_with_all_meetings_scored": sum((x.get("h2h_meeting_count", 0) or 0) > 0 and x.get("h2h_scored_meetings", 0) == x.get("h2h_meeting_count", 0) for x in h2h_with_meetings),
        "responses_with_all_meetings_dated": sum((x.get("h2h_meeting_count", 0) or 0) > 0 and x.get("h2h_dated_meetings", 0) == x.get("h2h_meeting_count", 0) for x in h2h_with_meetings),
        "failed_requests": len(h2h_failed),
        "transient_retries_exhausted": sum(bool(x.get("h2h_retry_exhausted")) for x in h2h_samples),
        "interpretation": "A successful empty response is not counted as a network failure; meeting count, score completeness and date completeness are reported separately."
    }
    report["summary"]["required_feature_endpoints_passed"] = required_ok
    report["summary"]["competitions_with_multi_fixture_samples"] = sum((r.get("tests", {}).get("multi_fixture_validation", {}).get("sample_size", 0) or 0) >= 3 for r in report["targets"])
    report["summary"]["field_acceptance_counts"] = {
        field: {status: sum(r.get("field_acceptance", {}).get(field) == status for r in report["targets"])
                for status in ("SUPPORTED", "PARTIAL", "UNSUPPORTED", "NOT_APPLICABLE")}
        for field in ("fixtures", "recent_form_only", "recent_form_and_last5_goals", "h2h", "standings", "xg_in_match_context", "league_xg_endpoint")
    }
    report["summary"]["xg_diagnostics"] = {
        "competitions_with_any_observed_match_context_xg": sum((r.get("xg_diagnostics", {}).get("fixtures_with_both_home_away_xg", 0) or 0) > 0 for r in report["targets"]),
        "competitions_with_sample_threshold_match_context_xg": sum(r.get("field_acceptance", {}).get("xg_in_match_context") == "SUPPORTED" for r in report["targets"]),
        "catalogue_advanced_stats_declared_true": sum(r.get("xg_diagnostics", {}).get("catalogue_advanced_stats_flag") is True for r in report["targets"]),
        "catalogue_advanced_stats_declared_false": sum(r.get("xg_diagnostics", {}).get("catalogue_advanced_stats_flag") is False for r in report["targets"]),
        "catalogue_advanced_stats_undeclared": sum(r.get("xg_diagnostics", {}).get("catalogue_advanced_stats_flag") is None for r in report["targets"]),
        "dedicated_league_xg_endpoint_supported": sum(r.get("field_acceptance", {}).get("league_xg_endpoint") == "SUPPORTED" for r in report["targets"]),
        "note": "Match-context sample evidence, catalogue capability declaration, and dedicated league xG endpoint status are separate measurements."
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
        identity_checks = r.get("tests", {}).get("multi_fixture_validation", {}).get("sample_checks", [])
        if not identity_checks or any(x.get("competition_identity_status") != "VERIFIED" for x in identity_checks):
            final_acceptance = False
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
