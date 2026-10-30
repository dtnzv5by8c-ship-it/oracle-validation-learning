#!/usr/bin/env python3
"""Research-only Selected-50 scoring DNA from the pinned archive; aggregate outputs only."""
import argparse, csv, datetime as dt, hashlib, json, math, statistics, zipfile
from collections import Counter, defaultdict
from pathlib import Path
MARKETS={"BTTS","DC_HOME","DC_AWAY"}
PRIMARY_START=dt.date(2025,3,20)
PRIMARY_END=dt.date(2026,9,20)
def read_csv(p):
    with Path(p).open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def write_csv(p, rows):
    rows=list(rows); fields=list(rows[0]) if rows else []
    with Path(p).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(rows)
def score(v):
    try:
        x=float(v)
        return int(x) if math.isfinite(x) and x>=0 and x.is_integer() else None
    except (TypeError,ValueError,OverflowError): return None
def day(row):
    for k in ("date_unix","kickoff_unix","timestamp","date","datetime","kickoff","match_date"):
        v=row.get(k)
        if v in (None,""): continue
        try:
            x=float(v)
            if x>1_000_000_000:
                if x>100_000_000_000: x/=1000
                return dt.datetime.fromtimestamp(x,dt.timezone.utc).date()
        except (TypeError,ValueError,OverflowError,OSError): pass
        try:
            x=dt.datetime.fromisoformat(str(v).replace("Z","+00:00"))
            if x.tzinfo is None: x=x.replace(tzinfo=dt.timezone.utc)
            return x.astimezone(dt.timezone.utc).date()
        except ValueError: pass
    return None
def flag(v):
    try:
        x=int(float(v)); return x if x in (0,1) else None
    except (TypeError,ValueError,OverflowError): return None
def fid(row):
    for k in ("id","match_id","fixture_id","game_id"):
        if row.get(k) not in (None,""): return str(row[k]).strip()
    return ""
def as_list(x):
    if isinstance(x,list): return x
    if isinstance(x,dict):
        for k in ("data","matches","fixtures"):
            if isinstance(x.get(k),list): return x[k]
    return []
def pct(a,b): return round(100*a/b,3) if b else None
def score_period(g,period,start,end,records,season_n):
    dated=[r for r in records if r["date"] and start<=r["date"]<=end]
    complete_status=[r for r in dated if r["status"]=="complete"]
    completed=[r for r in complete_status if r["home"] is not None and r["away"] is not None]
    noncomplete_scored=[r for r in dated if r["status"]!="complete" and r["home"] is not None and r["away"] is not None]
    h2=[r for r in completed if r["no_home_away"]==0]
    n,n2=len(completed),len(h2)
    tg=[r["home"]+r["away"] for r in completed]
    hs=[r["home"] for r in h2]; aws=[r["away"] for r in h2]
    buckets={str(k):sum(x==k for x in tg) for k in range(5)}; buckets["5plus"]=sum(x>=5 for x in tg)
    home_cs=sum(r["away"]==0 for r in completed); away_cs=sum(r["home"]==0 for r in completed)
    home_fts=sum(r["home"]==0 for r in completed); away_fts=sum(r["away"]==0 for r in completed)
    row={"selected_id":g["selected_id"],"country":g["country"],"league":g["competition_name"],
      "period":period,"period_start":start.isoformat(),"period_end":end.isoformat(),"season_folders":season_n,
      "dated_archive_rows":len(dated),"completed_status_rows":len(complete_status),"completed_dated_score_rows":n,
      "complete_status_missing_or_invalid_score_rows":len(complete_status)-n,
      "noncomplete_status_rows_with_numeric_scores_excluded":len(noncomplete_scored),
      "valid_1x2_rows_no_home_away_zero":n2,
      "no_home_away_one_excluded_from_1x2":sum(r["no_home_away"]==1 for r in completed),
      "no_home_away_unknown_excluded_from_1x2":sum(r["no_home_away"] is None for r in completed),
      "home_win_rate_pct":pct(sum(r["home"]>r["away"] for r in h2),n2),
      "draw_rate_pct":pct(sum(r["home"]==r["away"] for r in h2),n2),
      "away_win_rate_pct":pct(sum(r["home"]<r["away"] for r in h2),n2),
      "home_scoring_rate_pct":pct(sum(x>0 for x in hs),n2),"away_scoring_rate_pct":pct(sum(x>0 for x in aws),n2),
      "btts_rate_pct":pct(sum(r["home"]>0 and r["away"]>0 for r in completed),n),
      "over15_rate_pct":pct(sum(x>=2 for x in tg),n),"over25_rate_pct":pct(sum(x>=3 for x in tg),n),"over35_rate_pct":pct(sum(x>=4 for x in tg),n),
      "home_clean_sheet_rate_pct":pct(sum(r["away"]==0 for r in h2),n2),
      "away_clean_sheet_rate_pct":pct(sum(r["home"]==0 for r in h2),n2),
      "team_clean_sheet_rate_pct":pct(home_cs+away_cs,2*n),
      "home_failed_to_score_rate_pct":pct(sum(r["home"]==0 for r in h2),n2),
      "away_failed_to_score_rate_pct":pct(sum(r["away"]==0 for r in h2),n2),
      "team_failed_to_score_rate_pct":pct(home_fts+away_fts,2*n),
      "any_team_clean_sheet_match_rate_pct":pct(sum(r["home"]==0 or r["away"]==0 for r in completed),n),
      "mean_home_goals_valid_home_away":round(statistics.mean(hs),3) if hs else None,
      "mean_away_goals_valid_home_away":round(statistics.mean(aws),3) if aws else None,
      "mean_total_goals":round(statistics.mean(tg),3) if tg else None,
      "median_total_goals":statistics.median(tg) if tg else None,
      "stddev_total_goals":round(statistics.pstdev(tg),3) if len(tg)>1 else (0 if tg else None),
      "sample_band":"NO_SAMPLE" if not n else "LT_100" if n<100 else "100_299" if n<300 else "300_999" if n<1000 else "GE_1000",
      "score_profile_status":"AVAILABLE_PROVIDER_COMPLETE_STATUS_RESEARCH_ONLY" if n else "NO_COMPLETED_DATED_SCORE_ROWS",
      "label_validity":"PROVIDER_STATUS_COMPLETE_NUMERIC_SCORE_ONLY_OFFICIAL_SETTLEMENT_UNVERIFIED",
      "production_eligible":"NO","betting_eligible":"NO"}
    for k,v in buckets.items(): row[f"total_goals_{k}_n"]=v; row[f"total_goals_{k}_rate_pct"]=pct(v,n)
    return row
def market_metrics(runtime_csv):
    rows=[r for r in read_csv(runtime_csv) if r.get("market") in MARKETS]
    groups=defaultdict(list)
    for r in rows: groups[(str(r["selected_id"]),r["country"],r["league"],r["market"])].append(r)
    if len(groups)!=150: raise ValueError(f"Expected 150 league-market groups, got {len(groups)}")
    folds=[]; markets=[]
    for (sid,country,league,market),rs in sorted(groups.items()):
        rs=sorted(rs,key=lambda x:x.get("fold","")); skills=[]; eces=[]; tr=[]; te=[]; gates=0
        for r in rs:
            sk=float(r["brier_skill_vs_league_prevalence"]) if r.get("brier_skill_vs_league_prevalence") not in (None,"") else None
            ec=float(r["ece_10_bins"]) if r.get("ece_10_bins") not in (None,"") else None
            tn=int(float(r.get("train_n") or 0)); en=int(float(r.get("test_n") or 0)); gate=r.get("sample_gate","")
            if gate=="SAMPLE_GATE_MET_DIAGNOSTIC_ONLY" and tn>=100 and en>=100: gates+=1
            if sk is not None and math.isfinite(sk): skills.append(sk)
            if ec is not None and math.isfinite(ec): eces.append(ec)
            tr.append(tn); te.append(en)
            folds.append({"selected_id":sid,"country":country,"league":league,"market":market,"fold":r.get("fold",""),
              "train_n":tn,"test_n":en,"sample_gate":gate,"brier_skill_vs_league_prevalence":sk,
              "brier":r.get("brier",""),"log_loss":r.get("log_loss",""),"auc":r.get("auc",""),"ece_10_bins":ec})
        pos=sum(x>0 for x in skills); mx=max(eces) if eces else None
        if len(rs)==3 and gates==3 and len(skills)==3 and pos==3 and mx is not None and mx<.10: status="REPEATABLE_POSITIVE_SKILL_DIAGNOSTIC_ONLY"
        elif len(rs)==3 and gates==3 and len(skills)==3 and pos==3: status="POSITIVE_SKILL_CALIBRATION_WARNING"
        elif len(rs)==3 and gates==3 and len(skills)==3 and pos==0: status="NO_POSITIVE_BRIER_SKILL"
        elif len(rs)==3 and gates==3 and len(skills)==3 and 0<pos<3: status="MIXED_BRIER_SKILL"
        else: status="INSUFFICIENT_SAMPLE_OR_METRIC"
        markets.append({"selected_id":sid,"country":country,"league":league,"market":market,"folds_observed":len(rs),
          "sample_gate_pass_folds":gates,"positive_brier_skill_folds":pos,"minimum_fold_train_n":min(tr),"minimum_fold_test_n":min(te),
          "mean_brier_skill":round(statistics.mean(skills),6) if skills else None,
          "minimum_brier_skill":min(skills) if skills else None,"maximum_fold_ece_10_bins":mx,
          "market_suitability_status":status,
          "recommendation":"DIAGNOSTIC_CANDIDATE_ONLY" if status=="REPEATABLE_POSITIVE_SKILL_DIAGNOSTIC_ONLY" else "NO_SUPPORTED_MARKET_RECOMMENDATION",
          "label_validity":"PROVISIONAL_INTERNAL_STATUS_SCORE_LABELS_OFFICIAL_SETTLEMENT_UNVERIFIED",
          "production_eligible":"NO","betting_eligible":"NO"})
    counts=dict(Counter(r["market_suitability_status"] for r in markets))
    expected={"REPEATABLE_POSITIVE_SKILL_DIAGNOSTIC_ONLY":26,"POSITIVE_SKILL_CALIBRATION_WARNING":13,
      "MIXED_BRIER_SKILL":47,"INSUFFICIENT_SAMPLE_OR_METRIC":60,"NO_POSITIVE_BRIER_SKILL":4}
    recon="MATCHES_2026_10_31_CHECKPOINT" if counts==expected else "STATUS_COUNTS_DIFFER_REVIEW_REQUIRED"
    return folds,markets,counts,recon
def run(archive,selected_manifest,runtime_dir,coverage_dir,out,audit_date):
    selected=read_csv(selected_manifest)
    if len(selected)!=50: raise ValueError("Selected-50 manifest must have 50 rows")
    by_id={str(r["selected_id"]).strip():r for r in selected}
    if len(by_id)!=50 or "" in by_id: raise ValueError("Selected-50 manifest has duplicate/blank IDs")
    out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        names=set(z.namelist()); mn=[n for n in names if n.endswith("ingestion_manifest.json")]
        if len(mn)!=1: raise ValueError("Expected exactly one ingestion_manifest.json")
        raw=json.loads(z.read(mn[0]).decode("utf-8")); seasons={}
        for m in raw:
            sid=str(m.get("season_id","")).strip()
            if not sid or sid in seasons: raise ValueError("Missing/duplicate season ID in archive manifest")
            seasons[sid]=m
        if len(seasons)!=200 or set(by_id)-set(seasons): raise ValueError("Archive must contain 200 seasons and all 50 selected IDs")
        groups={}
        for sid,s in by_id.items():
            m=seasons[sid]; key=(s["country"].strip(),s["competition_name"].strip())
            if (str(m.get("selected_country","")).strip(),str(m.get("selected_competition_name","")).strip())!=key: raise ValueError(f"Exact selected-ID label mismatch: {sid}")
            if key in groups: raise ValueError(f"Duplicate selected group: {key}")
            groups[key]={"selected_id":sid,"country":key[0],"competition_name":key[1]}
        group_seasons=defaultdict(list)
        for sid,m in seasons.items():
            key=(str(m.get("selected_country","")).strip(),str(m.get("selected_competition_name","")).strip())
            if key in groups: group_seasons[key].append(sid)
        if len(group_seasons)!=50 or any(len(v)!=4 or v.count(groups[k]["selected_id"])!=1 for k,v in group_seasons.items()):
            raise ValueError("Each selected group must have exactly four seasons and one selected current season ID")
        records={}; all_ids=Counter(); total_rows=complete_scores=noncomplete_scores=undated=0
        for key,sids in group_seasons.items():
            rr=[]
            for sid in sids:
                paths=[n for n in names if n.endswith(f"seasons/{sid}/matches.json")]
                if len(paths)!=1: raise ValueError(f"Missing/duplicate matches.json for season {sid}")
                matches=as_list(json.loads(z.read(paths[0]).decode("utf-8"))); total_rows+=len(matches)
                for m in matches:
                    if not isinstance(m,dict): raise ValueError(f"Non-object match row in season {sid}")
                    match_id=fid(m)
                    if not match_id: raise ValueError(f"Missing fixture ID in season {sid}")
                    all_ids[match_id]+=1; d=day(m)
                    if d is None: undated+=1
                    hs=score(next((m.get(k) for k in ("homeGoalCount","home_goals","home_score","home_score_ft","homeScore") if m.get(k) not in (None,"")),None))
                    aw=score(next((m.get(k) for k in ("awayGoalCount","away_goals","away_score","away_score_ft","awayScore") if m.get(k) not in (None,"")),None))
                    status=str(m.get("status","")).strip().lower()
                    if status=="complete" and hs is not None and aw is not None: complete_scores+=1
                    if status!="complete" and hs is not None and aw is not None: noncomplete_scores+=1
                    rr.append({"fixture_id":match_id,"date":d,"status":status,"home":hs,"away":aw,"no_home_away":flag(m.get("no_home_away"))})
            records[key]=rr
        duplicates=sum(v>1 for v in all_ids.values())
        if duplicates or total_rows!=59049 or complete_scores!=51983 or noncomplete_scores!=7066:
            raise ValueError(f"Archive integrity drift: rows={total_rows}, complete={complete_scores}, noncomplete_scored={noncomplete_scores}, duplicates={duplicates}")
    calendar=read_csv(Path(coverage_dir)/"calendar_year_coverage"/"selected50_calendar_year_coverage_by_league.csv")
    primary=read_csv(Path(coverage_dir)/"selected50_primary_window_coverage.csv")
    if len(calendar)!=200 or len(primary)!=50: raise ValueError("Existing QA coverage artifacts must contain 200 and 50 rows")
    cal={(r["country"],r["competition_name"],int(r["calendar_year"])):(int(r["rows_on_or_before_audit_date"]),int(r["complete_status_rows_on_or_before_audit_date"])) for r in calendar}
    pri={(r["country"],r["competition_name"]):r for r in primary}
    periods=[("2024_CALENDAR",dt.date(2024,1,1),dt.date(2024,12,31)),("2025_CALENDAR",dt.date(2025,1,1),dt.date(2025,12,31)),
      ("2026_CALENDAR_YTD_TO_AUDIT",dt.date(2026,1,1),audit_date),("2026_PRIMARY_WINDOW",dt.date(2026,1,1),PRIMARY_END),
      ("PRIMARY_VALIDATION_WINDOW",PRIMARY_START,PRIMARY_END)]
    year_rows=[]
    for key,g in sorted(groups.items()):
        for period,start,end in periods:
            row=score_period(g,period,start,end,records[key],4)
            if period in ("2024_CALENDAR","2025_CALENDAR","2026_CALENDAR_YTD_TO_AUDIT"):
                expected=cal[(g["country"],g["competition_name"],start.year)]
            elif period=="2026_PRIMARY_WINDOW":
                p=pri[(g["country"],g["competition_name"])]
                expected=(int(p["primary_window_calendar_2026_match_records"]),int(json.loads(p["primary_window_calendar_2026_status_counts_json"]).get("complete",0)))
            else:
                p=pri[(g["country"],g["competition_name"])]
                expected=(int(p["primary_window_match_records"]),int(p["primary_window_complete_status_records"]))
            row["qa_expected_archive_rows"],row["qa_expected_completed_status_rows"]=expected
            row["archive_row_delta_vs_qa"]=row["dated_archive_rows"]-expected[0]
            row["complete_status_delta_vs_qa"]=row["completed_status_rows"]-expected[1]
            row["coverage_reconciliation_status"]="PASS" if row["archive_row_delta_vs_qa"]==0 and row["complete_status_delta_vs_qa"]==0 and row["complete_status_missing_or_invalid_score_rows"]==0 else "FAIL"
            if row["coverage_reconciliation_status"]!="PASS": raise ValueError(f"QA coverage reconciliation failed: {g['country']} / {g['competition_name']} / {period}")
            year_rows.append(row)
    if len(year_rows)!=250: raise ValueError("Expected 250 group-period rows")
    byid={(r["selected_id"],r["period"]):r for r in year_rows}
    summary=[]
    for g in groups.values():
        r={"selected_id":g["selected_id"],"country":g["country"],"league":g["competition_name"],"season_folders":4}
        prefixes={"2024_CALENDAR":"y2024","2025_CALENDAR":"y2025","2026_CALENDAR_YTD_TO_AUDIT":"y2026_ytd","2026_PRIMARY_WINDOW":"y2026_primary","PRIMARY_VALIDATION_WINDOW":"primary_window"}
        for period,prefix in prefixes.items():
            src=byid[(g["selected_id"],period)]
            for metric in ("completed_dated_score_rows","btts_rate_pct","over15_rate_pct","over25_rate_pct","over35_rate_pct","home_win_rate_pct","draw_rate_pct","away_win_rate_pct","team_clean_sheet_rate_pct","team_failed_to_score_rate_pct","mean_total_goals","sample_band"):
                r[f"{prefix}_{metric}"]=src[metric]
        summary.append(r)
    fold_rows,market_rows,market_counts,market_recon=market_metrics(Path(runtime_dir)/"oracle_selected50_league_walk_forward_metrics.csv")
    market_by_id=defaultdict(list)
    for r in market_rows: market_by_id[r["selected_id"]].append(r)
    join=[]
    for r in market_rows:
        p=byid[(r["selected_id"],"PRIMARY_VALIDATION_WINDOW")]
        join.append({**r,"primary_window_completed_score_rows":p["completed_dated_score_rows"],"primary_window_btts_rate_pct":p["btts_rate_pct"],"primary_window_over25_rate_pct":p["over25_rate_pct"]})
    for r in summary:
        candidates=[x for x in market_by_id[r["selected_id"]] if x["market_suitability_status"]=="REPEATABLE_POSITIVE_SKILL_DIAGNOSTIC_ONLY"]
        candidates.sort(key=lambda x:(-(x["minimum_brier_skill"] if x["minimum_brier_skill"] is not None else -999),x["maximum_fold_ece_10_bins"] if x["maximum_fold_ece_10_bins"] is not None else 999,x["market"]))
        r["strongest_diagnostic_market"]=candidates[0]["market"] if candidates else "NONE_SUPPORTED"
        r["repeatable_diagnostic_markets"]=";".join(x["market"] for x in candidates)
        r["market_evidence_status"]="REPEATABLE_DIAGNOSTIC_CANDIDATE_ONLY" if candidates else "MIXED_OR_INSUFFICIENT_EVIDENCE"
    write_csv(out/"oracle_selected50_league_year_scoring_dna_2026-10-31.csv",year_rows)
    write_csv(out/"oracle_selected50_league_scoring_dna_summary_2026-10-31.csv",summary)
    write_csv(out/"oracle_selected50_league_market_suitability_2026-10-31.csv",market_rows)
    write_csv(out/"oracle_selected50_league_market_fold_metrics_2026-10-31.csv",fold_rows)
    write_csv(out/"oracle_selected50_league_market_scoring_join_2026-10-31.csv",join)
    counts=defaultdict(lambda:{"archive_rows":0,"completed_score_rows":0})
    for r in year_rows:
        counts[r["period"]]["archive_rows"]+=r["dated_archive_rows"]; counts[r["period"]]["completed_score_rows"]+=r["completed_dated_score_rows"]
    h=hashlib.sha256(Path(archive).read_bytes()).hexdigest()
    report={"status":"RESEARCH_ONLY_SELECTED50_SCORING_DNA_AND_MARKET_JOIN_COMPLETE","audit_date":audit_date.isoformat(),
      "source_archive_sha256":h,"source_archive_release_tag":"research-selected50-footystats-history-40375285207",
      "source_archive_qa_run_id":41115501513,"source_archive_qa_artifact_id":13004648723,
      "source_runtime_run_id":41119141526,"source_runtime_artifact_id":13006609602,
      "selected_groups":50,"season_folders":200,"archive_match_rows":total_rows,
      "completed_numeric_score_rows_all_archive":complete_scores,"noncomplete_numeric_score_rows_excluded":noncomplete_scores,
      "undated_rows_all_archive":undated,"duplicate_fixture_ids":duplicates,"calendar_period_totals":dict(counts),
      "market_suitability_counts":market_counts,"market_suitability_reconciliation":market_recon,
      "coverage_reconciliation":"PASS_EXACT_ARCHIVE_AND_COMPLETE_STATUS_COUNTS_FOR_250_GROUP_PERIODS",
      "provider_api_calls":0,"production_model_logic_changed":False,"production_probabilities_changed":False,
      "production_eligible":False,"betting_eligible":False,
      "limitations":["Rates use provider status=complete and dated non-negative integer score pairs; official settlement truth is not verified.",
        "1X2 and home/away-side rates exclude no_home_away=1 and unknown flags; total-goal/BTTS/over and team-level CS/FTS rates include valid neutral-venue score pairs.",
        "2026 calendar profile is year-to-date through the pinned 2026-10-30 archive audit date, not a completed calendar year.",
        "Selected IDs are provider season-ID surrogates; competition labels are inherited from exact selected-season catalogue relations, not canonical competition IDs.",
        "Walk-forward market labels are provisional internal status-score diagnostics; canonical fixture/team joins and official settlement truth remain unverified."]}
    (out/"oracle_selected50_scoring_dna_summary_2026-10-31.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2,sort_keys=True))
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",type=Path,required=True); p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--runtime-dir",type=Path,required=True); p.add_argument("--coverage-dir",type=Path,required=True)
    p.add_argument("--out-dir",type=Path,required=True); p.add_argument("--audit-date",type=dt.date.fromisoformat,default=dt.date(2026,10,30))
    a=p.parse_args(); run(a.archive,a.manifest,a.runtime_dir,a.coverage_dir,a.out_dir,a.audit_date)
if __name__=="__main__": main()
