#!/usr/bin/env python3
"""Report-only FootyStats archive audit and leakage-safe historical feature builder."""
import argparse, collections, csv, hashlib, json, re, zipfile
from pathlib import Path
from datetime import datetime, timezone

SETTLED = {"complete","completed","finished","ft","full time","full_time","played","after extra time","aet","penalties"}
CANCELLED = {"cancelled","canceled","suspended","postponed","abandoned","walkover"}
DATE_KEYS = ("date_unix","kickoff","date","timestamp","match_date","datetime")
ID_KEYS = ("id","match_id","fixture_id","game_id")
HOME_ID_KEYS = ("homeID","home_id","team_a_id","home_team_id","homeID")
AWAY_ID_KEYS = ("awayID","away_id","team_b_id","away_team_id")
HOME_NAME_KEYS = ("home_name","homeTeam","home_team_name","team_a_name","home")
AWAY_NAME_KEYS = ("away_name","awayTeam","away_team_name","team_b_name","away")
STATUS_KEYS = ("status","status_name","match_status","game_status")
HG_KEYS = ("homeGoalCount","home_goal_count","home_score","homeGoalsCount","home_goals")
AG_KEYS = ("awayGoalCount","away_goal_count","away_score","awayGoalsCount","away_goals")

def first(d, keys):
    for k in keys:
        v=d.get(k)
        if v is not None and v != "":
            return v
    return None

def as_date(v):
    if v is None: return None
    try:
        n=float(v)
        if n > 100000000000: n/=1000
        if n > 1000000000: return datetime.fromtimestamp(n,timezone.utc)
    except (ValueError,TypeError,OverflowError,OSError): pass
    try:
        s=str(v).strip().replace("Z","+00:00")
        dt=datetime.fromisoformat(s)
        return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)
    except (ValueError,TypeError): return None

def score(d, keys, event_key):
    v=first(d,keys)
    if v is not None:
        try:
            n=float(v)
            if n >= 0 and n.is_integer(): return int(n), "explicit_score_field"
        except (ValueError,TypeError): pass
    ev=d.get(event_key)
    if isinstance(ev,list):
        # Only event arrays of goal-minute strings/numbers are supported.
        if all(isinstance(x,(str,int,float)) for x in ev):
            return len(ev), "counted_goal_event_array"
    return None, "unavailable"

def status(d):
    v=first(d,STATUS_KEYS)
    return str(v).strip().lower() if v is not None else ""

def settled(d):
    s=status(d)
    # Fail closed: unknown statuses are not treated as settled.
    return s in SETTLED

def nonempty(d, keys):
    return first(d,keys) is not None

def write_csv(path, rows, fields=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    if fields is None:
        fields=list(rows[0].keys()) if rows else ["status"]
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive",required=True); ap.add_argument("--out",required=True)
    args=ap.parse_args(); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.archive) as z:
        z.extractall(out/"extracted")
    root=out/"extracted"
    files=list(root.rglob("matches.json"))
    if not files: raise SystemExit("No matches.json files found in archive.")
    manifest_files=list(root.rglob("ingestion_manifest.csv"))
    manifest=[]
    if manifest_files:
        with manifest_files[0].open(encoding="utf-8-sig",newline="") as f: manifest=list(csv.DictReader(f))
    records=[]; season_rows=[]; file_errors=[]; field_counts=collections.Counter()
    for fp in files:
        rel=str(fp.relative_to(root)); parts=fp.parts
        league=parts[-3] if len(parts)>=3 else "unknown"
        season=parts[-2] if len(parts)>=2 else "unknown"
        m=re.match(r"(20\d{2})_",season); season_year=m.group(1) if m else ""
        try:
            data=json.loads(fp.read_text(encoding="utf-8"))
            if not isinstance(data,list): raise ValueError("matches.json root is not a list")
        except Exception as e:
            file_errors.append({"file":rel,"error":type(e).__name__}); continue
        # Extract provider display names from match records when explicitly present; never infer from folder slugs.
        name_keys=("league_name","competition_name","leagueName","competitionName","league","competition","league_name_display","competition_name_display")
        provider_names=[]
        for item in data:
            if not isinstance(item,dict): continue
            value=first(item,name_keys)
            if isinstance(value,dict): value=first(value,("name","league_name","competition_name","display_name"))
            if isinstance(value,str) and value.strip() and len(value.strip()) < 160:
                provider_names.append(value.strip())
        name_counts=collections.Counter(provider_names)
        provider_name=name_counts.most_common(1)[0][0] if name_counts else ""
        season_rows.append({"league_folder":league,"provider_competition_name":provider_name,"provider_name_records":len(provider_names),"season_folder":season,"season_start_year":season_year,"records":len(data),"file":rel})
        for i,d in enumerate(data):
            if not isinstance(d,dict): continue
            for k,v in d.items():
                if v is not None and v!="": field_counts[k]+=1
            dt=as_date(first(d,DATE_KEYS))
            ident=first(d,ID_KEYS)
            hid=first(d,HOME_ID_KEYS); aid=first(d,AWAY_ID_KEYS)
            hn=first(d,HOME_NAME_KEYS); an=first(d,AWAY_NAME_KEYS)
            hg,hg_src=score(d,HG_KEYS,"homeGoals")
            ag,ag_src=score(d,AG_KEYS,"awayGoals")
            rec={"league_folder":league,"season_folder":season,"season_start_year":season_year,
                 "source_file":rel,"source_row":i,"fixture_id":str(ident) if ident is not None else "",
                 "provider_league_id":str(first(d,("competition_id","league_id","leagueID")) or ""),
                 "provider_season_id":str(season),"provider_season_id_source":"ARCHIVE_SEASON_FOLDER_ID",
                 "kickoff_utc":dt.isoformat() if dt else "",
                 "date_parse_ok":bool(dt),"home_team_id":str(hid or ""),
                 "away_team_id":str(aid or ""),"home_team":str(hn or ""),
                 "away_team":str(an or ""),"status_raw":status(d),
                 "settled_status_allowed":settled(d),"home_goals":hg,"away_goals":ag,
                 "home_score_source":hg_src,"away_score_source":ag_src,
                 "score_available":hg is not None and ag is not None,
                 "btts_result":int(hg>0 and ag>0) if hg is not None and ag is not None else "",
                 "over25_result":int(hg+ag>2) if hg is not None and ag is not None else "",
                 "home_xg_actual_present":any(d.get(k) not in (None,"") for k in ("team_a_xg","home_xg","homeXg")),
                 "away_xg_actual_present":any(d.get(k) not in (None,"") for k in ("team_b_xg","away_xg","awayXg")),
                 "home_xg_prematch_present":any(d.get(k) not in (None,"") for k in ("team_a_xg_prematch","home_xg_prematch")),
                 "away_xg_prematch_present":any(d.get(k) not in (None,"") for k in ("team_b_xg_prematch","away_xg_prematch")),
                 "odds_fields_present":";".join(k for k,v in d.items() if "odds" in k.lower() and v not in (None,"")),
                 "raw_record_sha256":hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False).encode()).hexdigest()}
            records.append(rec)
    # Use only rows with parseable dates, allowed settled status, valid scores and team IDs.
    valid=[r for r in records if r["date_parse_ok"] and r["settled_status_allowed"] and r["score_available"] and r["home_team_id"] and r["away_team_id"]]
    valid.sort(key=lambda r:(r["league_folder"],r["kickoff_utc"],r["fixture_id"]))
    by_league_team=collections.defaultdict(list); by_h2h=collections.defaultdict(list)
    feature_rows=[]
    # Strict cutoff: all source matches must have kickoff < target kickoff.
    for target in sorted(records,key=lambda r:(r["league_folder"],r["kickoff_utc"],r["fixture_id"])):
        if not target["date_parse_ok"] or not target["home_team_id"] or not target["away_team_id"]:
            continue
        league=target["league_folder"]; cutoff=target["kickoff_utc"]
        h=target["home_team_id"]; a=target["away_team_id"]
        prior_h=[x for x in by_league_team[(league,h)] if x["kickoff_utc"] < cutoff]
        prior_a=[x for x in by_league_team[(league,a)] if x["kickoff_utc"] < cutoff]
        pair=tuple(sorted((h,a)))
        prior_pair=[x for x in by_h2h[(league,pair)] if x["kickoff_utc"] < cutoff]
        f={"fixture_id":target["fixture_id"],"league_folder":league,"season_folder":target["season_folder"],
           "kickoff_utc":cutoff,"home_team_id":h,"away_team_id":a,
           "history_cutoff_rule":"strictly_before_target_kickoff",
           "home_prior_matches":len(prior_h),"away_prior_matches":len(prior_a),"h2h_prior_matches":len(prior_pair)}
        for side,prior,team_id in (("home",prior_h,h),("away",prior_a,a)):
            usable=[x for x in prior if x["settled_status_allowed"] and x["score_available"]]
            usable.sort(key=lambda x:x["kickoff_utc"])
            for n in (3,5,10):
                sample=usable[-n:]
                f[f"{side}_form_n{n}_available"]=len(sample)
                f[f"{side}_form_n{n}_coverage"]=len(sample)/n
                f[f"{side}_form_n{n}_points_per_game"]=round(sum(3 if ((x["home_team_id"]==team_id and x["home_goals"]>x["away_goals"]) or (x["away_team_id"]==team_id and x["away_goals"]>x["home_goals"])) else 1 if x["home_goals"]==x["away_goals"] else 0 for x in sample)/len(sample),4) if sample else ""
                f[f"{side}_form_n{n}_goals_for_avg"]=round(sum(x["home_goals"] if x["home_team_id"]==team_id else x["away_goals"] for x in sample)/len(sample),4) if sample else ""
                f[f"{side}_form_n{n}_goals_against_avg"]=round(sum(x["away_goals"] if x["home_team_id"]==team_id else x["home_goals"] for x in sample)/len(sample),4) if sample else ""
                f[f"{side}_form_n{n}_btts_rate"]=round(sum(x["home_goals"]>0 and x["away_goals"]>0 for x in sample)/len(sample),4) if sample else ""
                f[f"{side}_form_n{n}_over25_rate"]=round(sum(x["home_goals"]+x["away_goals"]>2 for x in sample)/len(sample),4) if sample else ""
        prior_pair.sort(key=lambda x:x["kickoff_utc"]); hs=prior_pair[-5:]
        f["h2h_last5_available"]=len(hs)
        f["h2h_last5_btts_rate"]=round(sum(x["home_goals"]>0 and x["away_goals"]>0 for x in hs)/len(hs),4) if hs else ""
        f["h2h_last5_over25_rate"]=round(sum(x["home_goals"]+x["away_goals"]>2 for x in hs)/len(hs),4) if hs else ""
        feature_rows.append(f)
    # Add each settled match to team/pair history only after all same-kickoff targets are evaluated.
    # This avoids same-timestamp fixtures leaking into one another.
    groups=collections.defaultdict(list)
    for r in valid: groups[(r["league_folder"],r["kickoff_utc"])].append(r)
    target_by_key=collections.defaultdict(list)
    for r in records:
        if r["date_parse_ok"] and r["home_team_id"] and r["away_team_id"]:
            target_by_key[(r["league_folder"],r["kickoff_utc"])].append(r)
    # Features above are built from a separate precomputed archive; insertions are not implicit.
    # Rebuild chronologically to guarantee histories actually advance.
    feature_rows=[]; by_league_team=collections.defaultdict(list); by_h2h=collections.defaultdict(list)
    all_targets=sorted([r for r in records if r["date_parse_ok"] and r["home_team_id"] and r["away_team_id"]],key=lambda r:(r["league_folder"],r["kickoff_utc"]))
    idx=0
    while idx<len(all_targets):
        end=idx+1; groupkey=(all_targets[idx]["league_folder"],all_targets[idx]["kickoff_utc"])
        while end<len(all_targets) and (all_targets[end]["league_folder"],all_targets[end]["kickoff_utc"])==groupkey: end+=1
        for target in all_targets[idx:end]:
            league,cutoff=target["league_folder"],target["kickoff_utc"]; h,a=target["home_team_id"],target["away_team_id"]
            ph=[x for x in by_league_team[(league,h)] if x["kickoff_utc"]<cutoff]
            pa=[x for x in by_league_team[(league,a)] if x["kickoff_utc"]<cutoff]
            pp=[x for x in by_h2h[(league,tuple(sorted((h,a))))] if x["kickoff_utc"]<cutoff]
            f={"fixture_id":target["fixture_id"],"league_folder":league,"season_folder":target["season_folder"],"kickoff_utc":cutoff,"home_team_id":h,"away_team_id":a,"history_cutoff_rule":"strictly_before_target_kickoff","home_prior_matches":len(ph),"away_prior_matches":len(pa),"h2h_prior_matches":len(pp)}
            for side,prior,tid in (("home",ph,h),("away",pa,a)):
                usable=[x for x in prior if x["score_available"] and x["settled_status_allowed"]]
                for n in (3,5,10):
                    sample=usable[-n:]; f[f"{side}_form_n{n}_available"]=len(sample); f[f"{side}_form_n{n}_coverage"]=round(len(sample)/n,4)
                    if sample:
                        gf=[x["home_goals"] if x["home_team_id"]==tid else x["away_goals"] for x in sample]
                        ga=[x["away_goals"] if x["home_team_id"]==tid else x["home_goals"] for x in sample]
                        pts=[3 if gf[j]>ga[j] else 1 if gf[j]==ga[j] else 0 for j in range(len(sample))]
                        f[f"{side}_form_n{n}_points_per_game"]=round(sum(pts)/len(pts),4); f[f"{side}_form_n{n}_goals_for_avg"]=round(sum(gf)/len(gf),4); f[f"{side}_form_n{n}_goals_against_avg"]=round(sum(ga)/len(ga),4)
                        f[f"{side}_form_n{n}_btts_rate"]=round(sum(x["home_goals"]>0 and x["away_goals"]>0 for x in sample)/len(sample),4); f[f"{side}_form_n{n}_over25_rate"]=round(sum(x["home_goals"]+x["away_goals"]>2 for x in sample)/len(sample),4)
                    else:
                        for suffix in ("points_per_game","goals_for_avg","goals_against_avg","btts_rate","over25_rate"): f[f"{side}_form_n{n}_{suffix}"]=""
            hs=pp[-5:]; f["h2h_last5_available"]=len(hs); f["h2h_last5_btts_rate"]=round(sum(x["home_goals"]>0 and x["away_goals"]>0 for x in hs)/len(hs),4) if hs else ""; f["h2h_last5_over25_rate"]=round(sum(x["home_goals"]+x["away_goals"]>2 for x in hs)/len(hs),4) if hs else ""
            feature_rows.append(f)
        # Only settled, score-complete records enter history, after all targets at this timestamp.
        for r in all_targets[idx:end]:
            if r["settled_status_allowed"] and r["score_available"]:
                by_league_team[(r["league_folder"],r["home_team_id"])].append(r); by_league_team[(r["league_folder"],r["away_team_id"])].append(r)
                by_h2h[(r["league_folder"],tuple(sorted((r["home_team_id"],r["away_team_id"]))))].append(r)
        idx=end
    write_csv(out/"match_field_audit.csv",records)
    write_csv(out/"chronological_features.csv",feature_rows)
    write_csv(out/"season_coverage.csv",season_rows)
    write_csv(out/"manifest_reconciliation.csv",manifest)
    write_csv(out/"parse_errors.csv",file_errors,["file","error"])
    summary={"status":"ARCHIVE_FEATURE_AUDIT_COMPLETE","production_readiness":"NOT_ASSESSED","production_logic_changed":False,"provider_api_calls":0,
      "archive_sha256":hashlib.sha256(Path(args.archive).read_bytes()).hexdigest(),"match_files":len(files),"archive_match_records":len(records),
      "records_with_parseable_kickoff":sum(r["date_parse_ok"] for r in records),"settled_status_and_score_complete_records":sum(r["settled_status_allowed"] and r["score_available"] for r in records),
      "records_with_team_ids":sum(bool(r["home_team_id"] and r["away_team_id"]) for r in records),"feature_rows":len(feature_rows),
      "season_folders":len(season_rows),"manifest_rows":len(manifest),"parse_errors":len(file_errors),
      "field_nonempty_counts":dict(field_counts.most_common()),"xg_policy":"Actual-match xG is descriptive only; prematch-labelled fields are presence-audited but excluded from model features until point-in-time provenance is verified.",
      "market_odds_policy":"Odds field presence is audited; no odds feature is built because timestamp/provenance is unverified.",
      "historical_table_policy":"No provider final/current table is treated as historical. Historical standings remain unbuilt pending rules for season formats and a separately validated reconstruction.",
      "crosswalk_policy":"Folder names are provisional provider competition candidates, not canonical Oracle league IDs. Exact 44-league crosswalk remains owner/canonical-registry dependent.",
      "limitations":["No match predictions or settlements are evaluated by this script.","No production model changes are made.","Unknown statuses are excluded from settled history.","Rows at the same kickoff timestamp are not allowed to inform one another.","Historical league-table positions are not generated.","A present field is not evidence it was available before kickoff."]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:summary[k] for k in ("status","match_files","archive_match_records","records_with_parseable_kickoff","settled_status_and_score_complete_records","feature_rows","season_folders","manifest_rows","parse_errors","provider_api_calls","production_readiness")},ensure_ascii=False))
if __name__=="__main__": main()
