#!/usr/bin/env python3
"""Research-only fixture extraction for the locked Oracle historical window."""
import csv, json, os, re, time, hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from oracle_44_catalogue_discovery import TARGETS

BASE="https://api.football-data-api.com/"
START=datetime(2025,3,20,tzinfo=timezone.utc)
END=datetime(2026,9,20,23,59,59,tzinfo=timezone.utc)
START_TS=int(START.timestamp()); END_TS=int(END.timestamp())

def call(key, endpoint, params):
    for attempt in range(4):
        q=dict(params); q["key"]=key
        try:
            req=Request(BASE+endpoint+"?"+urlencode(q),headers={"User-Agent":"Oracle-Historical-Window-Audit/1.0"})
            with urlopen(req,timeout=30) as resp:
                p=json.loads(resp.read().decode("utf-8"))
                if isinstance(p,dict) and p.get("success") is True: return resp.status,p
                raise RuntimeError("Provider API returned unsuccessful or unexpected payload")
        except HTTPError as e:
            if e.code in (429,500,502,503,504) and attempt<3:
                time.sleep(min(2**attempt,8)); continue
            raise RuntimeError("Provider request failed with HTTP "+str(e.code)) from None
    raise RuntimeError("Provider retries exhausted")

def year_pair(label):
    y=[int(v) for v in re.findall(r"(?:19|20)\d{2}",str(label or ""))]
    if not y: return None
    return (min(y),max(y)) if len(y)>1 else (y[0],y[0])

def write_csv(path, rows):
    if not rows: return
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
    key=os.environ.get("FOOTYSTATS_API_KEY","").strip()
    if not key: raise RuntimeError("Required API secret is missing")
    _,payload=call(key,"league-list",{"chosen_leagues_only":"false"})
    catalogue=[x for x in payload.get("data",[]) if isinstance(x,dict)]
    # Preserve all provider entries, including duplicate names.
    output=Path("oracle-44-historical-window-audit"); output.mkdir(exist_ok=True)
    seasons=[]; fixtures=[]; pages=[]; failures=[]
    for code,country,competition,aliases in TARGETS:
        entries=[x for x in catalogue if str(x.get("name","")).strip() in aliases]
        candidates=[]
        for entry in entries:
            for s in entry.get("season",[]) if isinstance(entry.get("season"),list) else []:
                if not isinstance(s,dict) or s.get("id") in ("",None): continue
                pair=year_pair(s.get("year",""))
                if pair and pair[0]<=2026 and pair[1]>=2025:
                    candidates.append((entry,s))
        if not candidates:
            seasons.append({"target_code":code,"country":country,"competition":competition,"season_id":"","season_label":"","status":"PARKED_NO_EXACT_ALIAS_OR_OVERLAPPING_LABEL","rows_total":0,"rows_in_window":0,"pages":0,"notes":"No exact alias/season candidate; no fuzzy mapping used."})
            continue
        # Deduplicate by provider entry identity and season id; never merge distinct entries by name.
        seen=set()
        for entry,s in candidates:
            sid=str(s["id"]); name=str(entry.get("name","")); lid=str(entry.get("id") or entry.get("league_id") or entry.get("competition_id") or "")
            if (lid,name,sid) in seen: continue
            seen.add((lid,name,sid)); total=0; inwin=0; page=1; short=False; error=""
            while page<=100:
                try:
                    status,p=call(key,"league-matches",{"league_id":sid,"max_per_page":100,"page":page})
                    data=p.get("data")
                    if not isinstance(data,list): raise RuntimeError("Unexpected fixture payload")
                    pages.append({"target_code":code,"provider_name":name,"provider_league_id":lid,"season_id":sid,"page":page,"http":status,"rows":len(data),"response_sha256":hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()})
                    total+=len(data)
                    for m in data:
                        if not isinstance(m,dict): continue
                        try: ts=int(m.get("date_unix"))
                        except (TypeError,ValueError): continue
                        if START_TS<=ts<=END_TS:
                            inwin+=1
                            fixtures.append({"target_code":code,"country":country,"competition":competition,"provider_name":name,"provider_league_id":lid,"season_id":sid,"season_label":str(s.get("year","")),"season_start":str(s.get("start_date","")),"season_end":str(s.get("end_date","")),"match_id":m.get("id"),"homeID":m.get("homeID"),"awayID":m.get("awayID"),"home_name":m.get("home_name"),"away_name":m.get("away_name"),"date_unix":ts,"status":m.get("status"),"homeGoals":m.get("homeGoalCount"),"awayGoals":m.get("awayGoalCount"),"team_a_xg":m.get("team_a_xg"),"team_b_xg":m.get("team_b_xg"),"team_a_xg_prematch":m.get("team_a_xg_prematch"),"team_b_xg_prematch":m.get("team_b_xg_prematch")})
                    if len(data)<100: short=True; break
                    page+=1
                except Exception as e:
                    error=str(e)[:150]; failures.append({"target_code":code,"season_id":sid,"page":page,"error":error}); break
            seasons.append({"target_code":code,"country":country,"competition":competition,"provider_name":name,"provider_league_id":lid,"season_id":sid,"season_label":str(s.get("year","")),"season_start":str(s.get("start_date","")),"season_end":str(s.get("end_date","")),"status":"RETRIEVED_SHORT_PAGE_NOT_COMPLETENESS_PROOF" if short else ("FAILED" if error else "SAFETY_PAGE_LIMIT"),"rows_total":total,"rows_in_window":inwin,"pages":page,"notes":error or "Season label is a candidate selector only; exact kickoff window applied. Short page does not prove completeness; point-in-time provenance unverified."})
            # Persist a checkpoint after each season so partial progress survives interruption.
            write_csv(output/"oracle_44_historical_window_fixtures.csv",fixtures)
            write_csv(output/"oracle_44_historical_window_seasons.csv",seasons)
            write_csv(output/"oracle_44_historical_window_pages.csv",pages)
            write_csv(output/"oracle_44_historical_window_failures.csv",failures)
            print(f"Progress: target={code} season={sid} fixture_rows={len(fixtures)} failures={len(failures)}",flush=True)
    write_csv(output/"oracle_44_historical_window_fixtures.csv",fixtures)
    write_csv(output/"oracle_44_historical_window_seasons.csv",seasons)
    write_csv(output/"oracle_44_historical_window_pages.csv",pages)
    write_csv(output/"oracle_44_historical_window_failures.csv",failures)
    summary={"generated_utc":datetime.now(timezone.utc).isoformat(),"window_start":"2025-03-20","window_end":"2026-09-20","target_leagues":len(TARGETS),"season_candidates":len(seasons),"fixture_rows_in_window":len(fixtures),"api_failure_rows":len(failures),"targets_with_fixtures":len(set(r["target_code"] for r in fixtures)),"season_completeness_proven":False,"point_in_time_provenance_established":False,"prediction_ready_targets":0,"odds_included":False,"production_logic_changed":False,"production_registry_changed":False,"interpretation":"Research ingestion only; no predictions/backtests. Candidate season labels and short-page pagination are not completeness proof."}
    (output/"oracle_44_historical_window_summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
    return 0  # Partial retrieval is reported in the artifact; preserve outputs for diagnosis.
if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception:
        print("Historical-window audit failed; inspect workflow diagnostics.",file=__import__("sys").stderr); raise SystemExit(1)
