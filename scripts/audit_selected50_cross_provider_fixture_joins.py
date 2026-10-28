#!/usr/bin/env python3
"""Research-only exact fixture joins across FootyStats archive, FotMob current feed, and Oracle historical ledger.

No network calls. Workflow supplies already-acquired files. No production writes or canonical approvals.
"""
import argparse,csv,json,re,unicodedata,zipfile
from collections import defaultdict,Counter
from datetime import datetime,timezone
from pathlib import Path

def norm(s):
    s=unicodedata.normalize("NFKD",str(s or "")).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+"," ",s).strip()

def timestamp(row,keys):
    for key in keys:
        value=row.get(key)
        if value in (None,""): continue
        if key.endswith("_unix") or key in ("date_unix","kickoff_unix","timestamp","timestamp_unix"):
            try:
                n=float(value)
                if n>1_000_000_000:
                    if n>1_000_000_000_000:n/=1000
                    return int(n)
            except (ValueError,TypeError,OverflowError):
                pass
        try:
            s=str(value).strip().replace("Z","+00:00")
            # Exact fixture joins require a time-of-day; date-only values are not midnight UTC.
            if not re.search(r"\d{2}:\d{2}",s): continue
            parsed=datetime.fromisoformat(s)
            if parsed.tzinfo is None: parsed=parsed.replace(tzinfo=timezone.utc)
            return int(parsed.timestamp())
        except (ValueError,TypeError,OverflowError): continue
    return None

def match_array(payload):
    if isinstance(payload,list):return payload
    if isinstance(payload,dict):
        for key in ("data","matches","results","fixtures","response"):
            value=payload.get(key)
            if isinstance(value,list):return value
            if isinstance(value,dict):
                nested=match_array(value)
                if nested:return nested
    return []

def load_footystats_archive(zf,selected_ids):
    rows=[];members=[];inventory=[]
    for name in zf.namelist():
        if not name.lower().endswith("/matches.json"):continue
        m=re.search(r"/seasons/(\d+)/matches\.json$",name)
        if not m:continue
        sid=m.group(1)
        if sid not in selected_ids:continue
        try:payload=json.loads(zf.read(name).decode("utf-8-sig"))
        except Exception as exc:
            inventory.append({"member":name,"season_id":sid,"parse_error":type(exc).__name__});continue
        arr=match_array(payload);first=next((x for x in arr if isinstance(x,dict)),{})
        inventory.append({"member":name,"season_id":sid,"row_count":len(arr),"fields":sorted(first.keys()) if first else []})
        members.append(name)
        for r in arr:
            if not isinstance(r,dict):continue
            ts=timestamp(r,("date_unix","kickoff_unix","kickoff_utc","date_utc","date","timestamp"))
            home=r.get("home_name") or r.get("home_team") or r.get("homeTeam") or r.get("home_team_name") or r.get("home") or ""
            away=r.get("away_name") or r.get("away_team") or r.get("awayTeam") or r.get("away_team_name") or r.get("away") or ""
            mid=str(r.get("id") or r.get("match_id") or r.get("fixture_id") or "").strip()
            if not(ts and home and away and mid):continue
            rows.append({"source_system":"FootyStats","selected_season_id":sid,"source_match_id":mid,"home":str(home),"away":str(away),"home_norm":norm(home),"away_norm":norm(away),"kickoff_unix":ts,"status":str(r.get("status") or "").strip().lower(),"home_goals":str(r.get("homeGoalCount") if r.get("homeGoalCount") is not None else r.get("home_goals") or r.get("home_score") or "").strip(),"away_goals":str(r.get("awayGoalCount") if r.get("awayGoalCount") is not None else r.get("away_goals") or r.get("away_score") or "").strip()})
    dedup={(r["selected_season_id"],r["source_match_id"]):r for r in rows}
    return list(dedup.values()),members,inventory

def load_fotmob_current(path):
    rows=[];header=[]
    with open(path,encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f);header=reader.fieldnames or []
        for r in reader:
            ts=timestamp(r,("date_utc","kickoff_utc","date_unix","date"))
            home=r.get("home_team") or r.get("home_name") or ""
            away=r.get("away_team") or r.get("away_name") or ""
            lid=str(r.get("league_id") or "").strip()
            mid=str(r.get("fotmob_match_id") or r.get("match_id") or r.get("id") or "").strip()
            if not(ts and home and away and lid and mid):continue
            rows.append({"source_system":"FotMob current snapshot","fotmob_match_id":mid,"fotmob_league_id":lid,"fotmob_league_name":str(r.get("league") or "").strip(),"home":str(home),"away":str(away),"home_norm":norm(home),"away_norm":norm(away),"kickoff_unix":ts,"status":str(r.get("status") or "").strip().lower(),"finished":str(r.get("finished") or "").strip().lower() in ("true","1","yes"),"cancelled":str(r.get("cancelled") or "").strip().lower() in ("true","1","yes"),"home_goals":str(r.get("home_goals") or "").strip(),"away_goals":str(r.get("away_goals") or "").strip()})
    return rows,header

def load_historical_ledger(path):
    rows=[];header=[]
    stats={"source_rows_seen":0,"rows_exact_kickoff":0,"rows_date_only":0,"rows_missing_exact_kickoff":0}
    with open(path,encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f);header=reader.fieldnames or []
        for r in reader:
            stats["source_rows_seen"]+=1
            ts=timestamp(r,("date_unix","kickoff_unix","timestamp_unix","date_utc","kickoff_utc","date"))
            raw_date=str(r.get("date_utc") or r.get("date") or r.get("kickoff_utc") or "").strip()
            date_key=raw_date[:10] if re.match(r"^\d{4}-\d{2}-\d{2}",raw_date) else ""
            if ts is not None:
                precision="EXACT_UTC_KICKOFF";stats["rows_exact_kickoff"]+=1
                if not date_key: date_key=datetime.fromtimestamp(ts,timezone.utc).date().isoformat()
            elif date_key and not re.search(r"\d{2}:\d{2}",raw_date):
                precision="DATE_ONLY_NO_KICKOFF_PROOF";stats["rows_date_only"]+=1
            else:
                stats["rows_missing_exact_kickoff"]+=1
                continue
            home=r.get("home_team") or r.get("home_name") or ""
            away=r.get("away_team") or r.get("away_name") or ""
            code=str(r.get("league_code") or "").strip()
            mid=str(r.get("match_id") or r.get("id") or r.get("source_match_id") or "").strip()
            if not (home and away and code and mid and date_key):continue
            rows.append({"source_system":"Oracle historical ledger","ledger_match_id":mid,
                         "canonical_league_code_candidate":code,"ledger_league_name":str(r.get("league") or "").strip(),
                         "home":str(home),"away":str(away),"home_norm":norm(home),"away_norm":norm(away),
                         "kickoff_unix":ts,"join_precision":precision,"date_key":date_key,
                         "source":str(r.get("source") or "").strip(),
                         "home_goals":str(r.get("home_goals") or "").strip(),
                         "away_goals":str(r.get("away_goals") or "").strip()})
    return rows,header,stats

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive",required=True);ap.add_argument("--current-matches",required=True)
    ap.add_argument("--historical-matches",required=True);ap.add_argument("--manifest",required=True)
    ap.add_argument("--identity-crosswalk",required=True);ap.add_argument("--current-source-manifest",default="")
    ap.add_argument("--out",required=True);args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    selected={}
    for line in Path(args.manifest).read_text(encoding="utf-8").splitlines():
        m=re.match(r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$",line)
        if m:selected[m.group(2).strip()]={"season_id":m.group(2).strip(),"country":m.group(3).strip(),"competition":m.group(4).strip()}
    if len(selected)!=50:raise SystemExit(f"Expected 50 selected seasons; got {len(selected)}.")
    master={}
    with open(args.identity_crosswalk,encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f):master[str(r.get("selected_manifest_id") or "").strip()]=str(r.get("provider_comp_master_id_observed") or "").strip()
    with zipfile.ZipFile(args.archive) as zf:
        footy,archive_members,inventory=load_footystats_archive(zf,set(selected));archive_member_count=len(zf.namelist())
    current,current_header=load_fotmob_current(args.current_matches)
    ledger,ledger_header,ledger_stats=load_historical_ledger(args.historical_matches)
    manifest_info={}
    if args.current_source_manifest and Path(args.current_source_manifest).is_file():
        try:
            m=json.loads(Path(args.current_source_manifest).read_text(encoding="utf-8"))
            manifest_info={"generated_utc":m.get("generated_utc"),"source":m.get("source"),"path":m.get("path")}
        except Exception:manifest_info={"parse_status":"UNAVAILABLE"}
    snapshot_ts=timestamp({"generated_utc":manifest_info.get("generated_utc")},("generated_utc",))
    for current_row in current:
        current_row["snapshot_generated_utc"]=manifest_info.get("generated_utc") or ""
        current_row["snapshot_pre_kickoff"]=bool(snapshot_ts is not None and snapshot_ts < current_row["kickoff_unix"])
    current_by_key=defaultdict(list)
    for r in current:current_by_key[(r["home_norm"],r["away_norm"],r["kickoff_unix"])].append(r)
    ledger_by_key=defaultdict(list);ledger_by_date_key=defaultdict(list)
    for r in ledger:
        if r["join_precision"]=="EXACT_UTC_KICKOFF" and r["kickoff_unix"] is not None:
            ledger_by_key[(r["home_norm"],r["away_norm"],r["kickoff_unix"])].append(r)
        elif r["join_precision"]=="DATE_ONLY_NO_KICKOFF_PROOF":
            ledger_by_date_key[(r["home_norm"],r["away_norm"],r["date_key"])].append(r)
    joins=[];date_only_joins=[];fotmob_groups=defaultdict(list);canonical_groups=defaultdict(list);date_only_groups=defaultdict(list)
    for f in footy:
        sid=f["selected_season_id"];s=selected.get(sid)
        if not s:continue
        base={"country":s["country"],"competition":s["competition"],"selected_season_id":sid,"provider_comp_master_id_observed":master.get(sid,""),"footystats_match_id":f["source_match_id"],"kickoff_utc":datetime.fromtimestamp(f["kickoff_unix"],timezone.utc).isoformat(),"home_team":f["home"],"away_team":f["away"],"footystats_status":f["status"],"footystats_score":f'{f["home_goals"]}-{f["away_goals"]}',"join_precision":"EXACT_UTC_KICKOFF"}
        for c in current_by_key.get((f["home_norm"],f["away_norm"],f["kickoff_unix"]),[]):
            snapshot_pre_kickoff=bool(c.get("snapshot_pre_kickoff"))
            score_known_raw=bool(f["home_goals"] and f["away_goals"] and c["home_goals"] and c["away_goals"])
            score_known=score_known_raw and not snapshot_pre_kickoff
            f_complete=f["status"] in ("complete","completed","ft","finished")
            c_complete=c["finished"] or c["status"] in ("ft","aet","pen","complete","completed")
            score_agree=score_known and f_complete and c_complete and f["home_goals"]==c["home_goals"] and f["away_goals"]==c["away_goals"]
            score_conflict=score_known and (f["home_goals"]!=c["home_goals"] or f["away_goals"]!=c["away_goals"])
            status_agree="NOT_COMPARABLE_PRE_KICKOFF" if snapshot_pre_kickoff else ((f_complete==c_complete) or (f["status"] in ("suspended","postponed","cancelled","canceled") and (c["cancelled"] or c["status"] in ("pp","postponed","suspended","cancelled","canceled"))))
            row={**base,"join_type":"FOTMOB_CURRENT","fotmob_league_id":c["fotmob_league_id"],"fotmob_league_name":c["fotmob_league_name"],"fotmob_match_id":c["fotmob_match_id"],"canonical_league_code_candidate":"","ledger_match_id":"","fotmob_score":f'{c["home_goals"]}-{c["away_goals"]}',"ledger_score":"","snapshot_generated_utc":c.get("snapshot_generated_utc",""),"snapshot_pre_kickoff":snapshot_pre_kickoff,"score_known_both_sources":bool(score_known),"score_agree":bool(score_agree),"score_conflict":bool(score_conflict),"status_agree":status_agree}
            joins.append(row);fotmob_groups[(sid,c["fotmob_league_id"],c["fotmob_league_name"])].append(row)
        exact_ledger_matches=ledger_by_key.get((f["home_norm"],f["away_norm"],f["kickoff_unix"]),[])
        date_ledger_matches=[] if exact_ledger_matches else ledger_by_date_key.get((f["home_norm"],f["away_norm"],datetime.fromtimestamp(f["kickoff_unix"],timezone.utc).date().isoformat()),[])
        for h,precision in [(h,"EXACT_UTC_KICKOFF") for h in exact_ledger_matches]+[(h,"DATE_ONLY_NO_KICKOFF_PROOF") for h in date_ledger_matches]:
            score_known=bool(f["home_goals"] and f["away_goals"] and h["home_goals"] and h["away_goals"])
            f_complete=f["status"] in ("complete","completed","ft","finished")
            score_agree=score_known and f_complete and f["home_goals"]==h["home_goals"] and f["away_goals"]==h["away_goals"]
            score_conflict=score_known and f_complete and (f["home_goals"]!=h["home_goals"] or f["away_goals"]!=h["away_goals"])
            row={**base,"join_type":"ORACLE_HISTORICAL_LEDGER" if precision=="EXACT_UTC_KICKOFF" else "ORACLE_HISTORICAL_LEDGER_DATE_ONLY","join_precision":precision,"fotmob_league_id":"","fotmob_league_name":"","fotmob_match_id":"","canonical_league_code_candidate":h["canonical_league_code_candidate"],"ledger_match_id":h["ledger_match_id"],"fotmob_score":"","ledger_score":f'{h["home_goals"]}-{h["away_goals"]}',"score_known_both_sources":bool(score_known),"score_agree":bool(score_agree),"score_conflict":bool(score_conflict),"status_agree":None}
            if precision=="EXACT_UTC_KICKOFF":
                joins.append(row);canonical_groups[(sid,h["canonical_league_code_candidate"],h["ledger_league_name"])].append(row)
            else:
                date_only_joins.append(row);date_only_groups[(sid,h["canonical_league_code_candidate"],h["ledger_league_name"])].append(row)
    def aggregate(groups,kind):
        outrows=[]
        for key,rr in sorted(groups.items()):
            sid=key[0]; vals=[r for r in rr if r["score_known_both_sources"]]
            agree=[r for r in vals if r["score_agree"]]
            conflicts=[r for r in rr if r.get("score_conflict") or r.get("status_agree") is False]
            pre_kickoff=sum(1 for r in rr if r.get("snapshot_pre_kickoff"))
            strong=len(rr)>=3 and (len(agree)>=1 or not vals)
            status="STRONG_CANDIDATE_HUMAN_REVIEW_REQUIRED" if strong else "LOW_SAMPLE_CANDIDATE_HUMAN_REVIEW_REQUIRED"
            if conflicts or any(r.get("status_agree") is False for r in rr):status+="_SOURCE_CONFLICT"
            if pre_kickoff:status+="_CONTAINS_PRE_KICKOFF_SNAPSHOT_ROWS"
            base={"country":selected[sid]["country"],"competition":selected[sid]["competition"],"selected_season_id":sid,"provider_comp_master_id_observed":master.get(sid,""),"exact_fixture_joins":len(rr),"score_agreements":len(agree),"score_conflicts":len(conflicts),"pre_kickoff_snapshot_rows":pre_kickoff,"bridge_status":status,"production_eligible":"NO"}
            if kind=="fotmob":base.update({"fotmob_league_id_candidate":key[1],"fotmob_league_name_observed":key[2]})
            else:base.update({"canonical_league_code_candidate":key[1],"ledger_league_name_observed":key[2]})
            outrows.append(base)
        return outrows
    fotmob_candidates=aggregate(fotmob_groups,"fotmob")
    canonical_candidates=aggregate(canonical_groups,"canonical")
    date_only_candidates=[]
    for key,rr in sorted(date_only_groups.items()):
        known=[r for r in rr if r["score_known_both_sources"]]
        agree=[r for r in known if r["score_agree"]]
        conflicts=[r for r in rr if r.get("score_conflict")]
        date_only_candidates.append({"country":selected[key[0]]["country"],"competition":selected[key[0]]["competition"],
            "selected_season_id":key[0],"canonical_league_code_candidate":key[1],"ledger_league_name_observed":key[2],
            "date_only_overlap_rows":len(rr),"score_agreements":len(agree),"score_conflicts":len(conflicts),
            "bridge_status":"DATE_ONLY_OVERLAP_HUMAN_REVIEW_REQUIRED_NO_KICKOFF_PROOF","production_eligible":"NO"})
    exact_fields=list(joins[0].keys()) if joins else ["selected_season_id","join_type","join_precision"]
    date_only_fields=list(date_only_joins[0].keys()) if date_only_joins else ["selected_season_id","join_type","join_precision"]
    outputs=[
        ("exact_fixture_join_rows.csv",joins,exact_fields),
        ("date_only_ledger_candidate_rows.csv",date_only_joins,date_only_fields),
        ("fotmob_bridge_candidates.csv",fotmob_candidates,list(fotmob_candidates[0].keys()) if fotmob_candidates else ["selected_season_id"]),
        ("canonical_code_candidates.csv",canonical_candidates,list(canonical_candidates[0].keys()) if canonical_candidates else ["selected_season_id"]),
        ("date_only_ledger_candidates.csv",date_only_candidates,list(date_only_candidates[0].keys()) if date_only_candidates else ["selected_season_id","bridge_status"])
    ]
    for name,rows,fields in outputs:
        with open(out/name,"w",encoding="utf-8",newline="") as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
    summary={"diagnostic":"SELECTED50_EXACT_CROSS_PROVIDER_FIXTURE_JOIN_AUDIT","generated_utc":datetime.now(timezone.utc).isoformat(),"selected_seasons":len(selected),"footystats_archive_rows":len(footy),"footystats_archive_match_json_members":len(archive_members),"archive_members_seen":archive_member_count,"fotmob_current_rows":len(current),"fotmob_current_header":current_header,"oracle_historical_ledger_rows":len(ledger),"oracle_historical_ledger_source_rows_seen":ledger_stats["source_rows_seen"],"oracle_historical_ledger_exact_kickoff_rows":ledger_stats["rows_exact_kickoff"],"oracle_historical_ledger_rows_date_only":ledger_stats["rows_date_only"],"oracle_historical_ledger_rows_missing_exact_kickoff":ledger_stats["rows_missing_exact_kickoff"],"oracle_historical_ledger_header":ledger_header,"exact_join_rows_total":len(joins),"fotmob_exact_join_rows":sum(1 for r in joins if r["join_type"]=="FOTMOB_CURRENT"),"pre_kickoff_snapshot_rows":sum(1 for r in joins if r["join_type"]=="FOTMOB_CURRENT" and r.get("snapshot_pre_kickoff")),"historical_ledger_exact_join_rows":sum(1 for r in joins if r["join_type"]=="ORACLE_HISTORICAL_LEDGER"),"historical_ledger_date_only_join_rows":len(date_only_joins),"selected_seasons_with_any_exact_join":len({r["selected_season_id"] for r in joins}),"selected_seasons_with_date_only_overlap":len({r["selected_season_id"] for r in date_only_joins}),"fotmob_bridge_candidate_groups":len(fotmob_candidates),"strong_fotmob_candidates":sum(r["bridge_status"].startswith("STRONG") for r in fotmob_candidates),"canonical_code_candidate_groups":len(canonical_candidates),"date_only_ledger_candidate_groups":len(date_only_candidates),"date_only_ledger_score_conflict_rows":sum(1 for r in date_only_joins if r.get("score_conflict")),"strong_canonical_code_candidates":sum(r["bridge_status"].startswith("STRONG") for r in canonical_candidates),"source_conflict_rows":sum(bool(r.get("score_conflict")) or r.get("status_agree") is False for r in joins if r["join_type"]=="FOTMOB_CURRENT"),"approved_canonical_bridges":0,"production_eligible":False,"current_source_manifest":manifest_info,"method":"Exact normalized ordered home/away names plus exact UTC kickoff; no display-name-only or fuzzy joins. Candidate statuses never grant production eligibility."}
    (out/"audit_summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps(summary,indent=2,sort_keys=True))
    print("FOTMOB_BRIDGE_CANDIDATES="+json.dumps(fotmob_candidates,sort_keys=True))
    print("CANONICAL_CODE_CANDIDATES="+json.dumps(canonical_candidates,sort_keys=True))

if __name__=="__main__":main()
