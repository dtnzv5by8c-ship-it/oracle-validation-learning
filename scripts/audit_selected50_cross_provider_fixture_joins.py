#!/usr/bin/env python3
"""Research-only exact fixture crosswalk audit: FootyStats private archive vs FotMob current/historical CSV.

No network calls; the workflow supplies already-acquired local files. No writes to production.
"""
import argparse, csv, io, json, re, unicodedata, zipfile
from collections import defaultdict, Counter
from datetime import datetime, timezone
from pathlib import Path

def norm(s):
    s=unicodedata.normalize("NFKD",str(s or "")).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+"," ",s).strip()

def timestamp(row, keys):
    for key in keys:
        value=row.get(key)
        if value in (None,""): continue
        try:
            if key.endswith("_unix") or key in ("date_unix","kickoff_unix"):
                n=int(float(value))
                if n>10**12: n//=1000
                return n
            s=str(value).strip().replace("Z","+00:00")
            return int(datetime.fromisoformat(s).timestamp())
        except (ValueError,TypeError,OverflowError):
            continue
    return None

def rows_from_csv_zip(zf, selected_ids):
    candidates=[]
    inventory=[]
    for name in zf.namelist():
        if not name.lower().endswith(".csv"): continue
        try:
            with zf.open(name) as raw:
                wrapper=io.TextIOWrapper(raw,encoding="utf-8-sig",errors="replace",newline="")
                reader=csv.DictReader(wrapper)
                fields={x.strip() for x in (reader.fieldnames or [])}
                inventory.append({"member":name,"fields":sorted(fields)})
                has_home=bool(fields & {"home_name","home_team","homeTeam","team_a","home_team_name","home"})
                has_away=bool(fields & {"away_name","away_team","awayTeam","team_b","away_team_name","away"})
                has_time=bool(fields & {"date_unix","kickoff_unix","date_utc","kickoff_utc","date","match_date","timestamp","kickoff","datetime","date_GMT"})
                has_comp=bool(fields & {"competition_id","selected_season_id","season_id","provider_season_id","league_season_id"})
                if has_home and has_away and has_time and has_comp:
                    candidates.append((name,fields))
        except Exception:
            continue
    if not candidates:
        return [],[],[],inventory
    all_rows=[]; member_names=[]; selected_seen=Counter()
    for name,fields in candidates:
        member_names.append(name)
        with zf.open(name) as raw:
            reader=csv.DictReader(io.TextIOWrapper(raw,encoding="utf-8-sig",errors="replace",newline=""))
            for row in reader:
                comp=str(row.get("selected_season_id") or row.get("season_id") or row.get("provider_season_id") or row.get("competition_id") or "").strip()
                if comp not in selected_ids: continue
                ts=timestamp(row,("date_unix","kickoff_unix","kickoff_utc","date_utc","date"))
                home=row.get("home_name") or row.get("home_team") or row.get("homeTeam") or row.get("team_a") or ""
                away=row.get("away_name") or row.get("away_team") or row.get("awayTeam") or row.get("team_b") or ""
                mid=str(row.get("id") or row.get("match_id") or row.get("fixture_id") or "").strip()
                if not (ts and home and away and mid): continue
                all_rows.append({"season_id":comp,"match_id":mid,"home":str(home),"away":str(away),"home_norm":norm(home),"away_norm":norm(away),"kickoff_unix":ts,"status":str(row.get("status") or "").strip().lower(),"home_goals":row.get("homeGoalCount") or row.get("home_goals") or row.get("home_score") or "","away_goals":row.get("awayGoalCount") or row.get("away_goals") or row.get("away_score") or ""})
                selected_seen[comp]+=1
    # Deduplicate by selected season and source match ID across archive files.
    dedup={}
    for r in all_rows: dedup[(r["season_id"],r["match_id"])]=r
    return list(dedup.values()),member_names,selected_seen,inventory

def load_current_matches(path):
    with open(path,encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        rows=[]
        for row in reader:
            ts=timestamp(row,("date_utc","kickoff_utc","date_unix"))
            home=row.get("home_team") or row.get("home_name") or ""
            away=row.get("away_team") or row.get("away_name") or ""
            lid=str(row.get("league_id") or "").strip()
            mid=str(row.get("fotmob_match_id") or row.get("match_id") or row.get("id") or "").strip()
            if not (ts and home and away and lid and mid): continue
            rows.append({"fotmob_match_id":mid,"fotmob_league_id":lid,"fotmob_league_name":str(row.get("league") or "").strip(),"home":str(home),"away":str(away),"home_norm":norm(home),"away_norm":norm(away),"kickoff_unix":ts,"status":str(row.get("status") or "").strip().lower(),"finished":str(row.get("finished") or "").strip().lower() in ("true","1","yes"),"cancelled":str(row.get("cancelled") or "").strip().lower() in ("true","1","yes"),"home_goals":str(row.get("home_goals") or "").strip(),"away_goals":str(row.get("away_goals") or "").strip()})
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive",required=True)
    ap.add_argument("--current-matches",required=True)
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--identity-crosswalk",required=True)
    ap.add_argument("--current-source-manifest",default="")
    ap.add_argument("--out",required=True)
    args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    selected={}
    for line in Path(args.manifest).read_text(encoding="utf-8").splitlines():
        m=re.match(r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$",line)
        if m:selected[m.group(2).strip()]={"season_id":m.group(2).strip(),"country":m.group(3).strip(),"competition":m.group(4).strip()}
    if len(selected)!=50: raise SystemExit(f"Expected 50 selected seasons; got {len(selected)}.")
    master={}
    with open(args.identity_crosswalk,encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f): master[str(r.get("selected_manifest_id") or "").strip()]=str(r.get("provider_comp_master_id_observed") or "").strip()
    with zipfile.ZipFile(args.archive) as zf:
        footy,archive_members,per_season,inventory=rows_from_csv_zip(zf,set(selected))
        member_list=zf.namelist()
    if not footy:
        print("ARCHIVE_SCHEMA_INVENTORY="+json.dumps({"members":member_list,"csv_headers":inventory},sort_keys=True))
        raise SystemExit("No archive CSV with selected season ID, home/away team and kickoff fields was found. No matches inferred.")
    current=load_current_matches(args.current_matches)
    # Exact key only: normalized ordered home/away pair and exact UTC Unix kickoff.
    current_by_key=defaultdict(list)
    for r in current: current_by_key[(r["home_norm"],r["away_norm"],r["kickoff_unix"])].append(r)
    joins=[]
    for f in footy:
        s=selected.get(f["season_id"])
        if not s: continue
        for c in current_by_key.get((f["home_norm"],f["away_norm"],f["kickoff_unix"]),[]):
            score_known=(str(f["home_goals"]).strip()!="" and str(f["away_goals"]).strip()!="" and c["home_goals"]!="" and c["away_goals"]!="")
            score_agree=score_known and str(f["home_goals"]).strip()==c["home_goals"] and str(f["away_goals"]).strip()==c["away_goals"]
            f_complete=f["status"] in ("complete","completed","ft","finished")
            c_complete=c["finished"] or c["status"] in ("ft","aet","pen","complete","completed")
            status_agree=(f_complete==c_complete) or (f["status"] in ("suspended","postponed","cancelled","canceled") and (c["cancelled"] or c["status"] in ("pp","postponed","suspended","cancelled","canceled")))
            joins.append({"country":s["country"],"competition":s["competition"],"selected_season_id":f["season_id"],"provider_comp_master_id_observed":master.get(f["season_id"],""),"fotmob_league_id":c["fotmob_league_id"],"fotmob_league_name":c["fotmob_league_name"],"fotmob_match_id":c["fotmob_match_id"],"footystats_match_id":f["match_id"],"kickoff_utc":datetime.fromtimestamp(f["kickoff_unix"],timezone.utc).isoformat(),"home_team":f["home"],"away_team":f["away"],"fotmob_score":f'{c["home_goals"]}-{c["away_goals"]}',"footystats_score":f'{f["home_goals"]}-{f["away_goals"]}',"fotmob_status":c["status"],"footystats_status":f["status"],"score_known_both_sources":bool(score_known),"score_agree":bool(score_agree),"status_agree":bool(status_agree)})
    # Aggregate by source league ID + selected season. A bridge remains a candidate only.
    groups=defaultdict(list)
    for j in joins: groups[(j["selected_season_id"],j["fotmob_league_id"],j["fotmob_league_name"])].append(j)
    bridge=[]
    for (sid,lid,lname),rr in sorted(groups.items()):
        completed=[x for x in rr if x["score_known_both_sources"] and x["score_agree"] and x["status_agree"]]
        conflicts=[x for x in rr if (x["score_known_both_sources"] and not x["score_agree"]) or not x["status_agree"]]
        if len(rr)>=3 and len(completed)>=1: status="STRONG_CANDIDATE_HUMAN_REVIEW_REQUIRED"
        elif len(rr)>0: status="LOW_SAMPLE_CANDIDATE_HUMAN_REVIEW_REQUIRED"
        else: status="NO_EXACT_OVERLAP_EVIDENCE"
        if conflicts: status+="_SOURCE_CONFLICT"
        s=selected[sid]
        bridge.append({"country":s["country"],"competition":s["competition"],"selected_season_id":sid,"provider_comp_master_id_observed":master.get(sid,""),"fotmob_league_id_candidate":lid,"fotmob_league_name_observed":lname,"exact_fixture_joins":len(rr),"completed_score_and_status_agreements":len(completed),"source_conflict_rows":len(conflicts),"bridge_status":status,"production_eligible":"NO"})
    with open(out/"exact_fixture_join_rows.csv","w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(joins[0].keys()) if joins else ["selected_season_id"]);w.writeheader();w.writerows(joins)
    with open(out/"bridge_candidates.csv","w",encoding="utf-8",newline="") as f:
        fields=list(bridge[0].keys()) if bridge else ["selected_season_id"]
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(bridge)
    manifest_info={}
    if args.current_source_manifest and Path(args.current_source_manifest).is_file():
        try:
            m=json.loads(Path(args.current_source_manifest).read_text(encoding="utf-8"))
            manifest_info={"generated_utc":m.get("generated_utc"),"requested_start":m.get("requested_start"),"requested_end":m.get("requested_end"),"source":m.get("source"),"path":m.get("path")}
        except Exception: manifest_info={"parse_status":"UNAVAILABLE"}
    summary={"diagnostic":"SELECTED50_EXACT_CROSS_PROVIDER_FIXTURE_JOIN_AUDIT","generated_utc":datetime.now(timezone.utc).isoformat(),"selected_seasons":len(selected),"footystats_archive_rows":len(footy),"current_fotmob_rows":len(current),"exact_fixture_joins":len(joins),"selected_seasons_with_any_exact_join":len({x["selected_season_id"] for x in joins}),"fotmob_league_ids_with_exact_joins":len({x["fotmob_league_id"] for x in joins}),"bridge_candidate_groups":len(bridge),"strong_candidates":sum(x["bridge_status"].startswith("STRONG") for x in bridge),"source_conflict_rows":sum(not x["score_agree"] or not x["status_agree"] for x in joins),"approved_canonical_bridges":0,"production_eligible":False,"archive_match_csv_members":archive_members,"archive_members_seen":len(member_list),"current_source_manifest":manifest_info,"method":"Exact normalized ordered home/away names plus exact UTC kickoff timestamp; no display-name-only or fuzzy joins; candidate status never grants production eligibility."}
    (out/"audit_summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps(summary,indent=2,sort_keys=True))
    print("BRIDGE_CANDIDATES")
    print(json.dumps(bridge,indent=2,sort_keys=True))

if __name__=="__main__": main()
