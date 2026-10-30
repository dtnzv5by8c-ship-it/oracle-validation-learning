#!/usr/bin/env python3
"""Offline Selected-50 season/event-time QA from sanitized archive outputs only."""
from __future__ import annotations
import argparse, csv, json
from collections import Counter
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from statistics import median

FLAGS = ("table_payload_present","season_stats_payload_present","matches_file_present",
         "teams_file_present","tables_file_present","season_stats_file_present")

def integer(v, name):
    if isinstance(v, bool): raise ValueError(f"{name}: boolean is not a count")
    try: n=Decimal(str(v).strip())
    except (InvalidOperation,TypeError,ValueError): raise ValueError(f"{name}: invalid count {v!r}") from None
    if not n.is_finite() or n < 0 or n != n.to_integral_value(): raise ValueError(f"{name}: invalid count {v!r}")
    return int(n)

def boolean(v, name):
    s=str(v).strip().lower()
    if s in ("true","1","yes"): return True
    if s in ("false","0","no"): return False
    raise ValueError(f"{name}: invalid boolean {v!r}")

def day(v, name):
    if not str(v or "").strip(): return None
    try: return date.fromisoformat(str(v)[:10])
    except ValueError: raise ValueError(f"{name}: invalid date {v!r}") from None

def statuses(v):
    try: obj=json.loads(str(v)) if v not in (None,"") else {}
    except json.JSONDecodeError: raise ValueError("invalid provider_status_counts_json") from None
    if not isinstance(obj,dict): raise ValueError("provider status counts must be an object")
    return {str(k).lower():integer(x,f"status {k}") for k,x in obj.items()}

def validate_report(r):
    if r.get("status")!="QA_COMPLETE_REVIEW_REQUIRED": raise ValueError("unexpected archive QA status")
    if r.get("official_settlement_truth_verified") is not False or r.get("production_eligible") is not False:
        raise ValueError("settlement truth and production eligibility must remain false")
    if integer(r.get("selected_leagues_in_manifest"),"selected groups")!=50 or integer(r.get("historical_season_manifest_rows"),"seasons")!=200:
        raise ValueError("expected 50 groups and 200 season rows")
    start,end,audit=(day(r.get(k),k) for k in ("primary_window_start","primary_window_end","audit_date_utc"))
    if not start or not end or not audit or start>end: raise ValueError("invalid primary window/audit date")
    return start,end,audit

def build_rows(rows, report, start, end):
    if len(rows)!=200: raise ValueError(f"expected 200 season rows, got {len(rows)}")
    seen=set(); groups=Counter(); current=Counter(); out=[]
    for r in rows:
        sid=str(r.get("season_id","")).strip(); country=str(r.get("country","")).strip(); league=str(r.get("competition_name","")).strip()
        if not sid or not country or not league or sid in seen: raise ValueError("missing identity or duplicate season_id")
        seen.add(sid); g=(country,league); groups[g]+=1
        selected=boolean(r.get("selected_current_season"),"selected_current_season")
        if selected: current[g]+=1
        n=integer(r.get("match_records"),"match_records"); teams=integer(r.get("team_records"),"team_records")
        pw=integer(r.get("primary_window_match_records"),"primary_window_match_records")
        uid=integer(r.get("primary_window_unique_provider_match_ids"),"primary_window_unique_provider_match_ids")
        comp=integer(r.get("primary_window_complete_status_records"),"primary_window_complete_status_records")
        noncomp=integer(r.get("primary_window_noncomplete_status_records"),"primary_window_noncomplete_status_records")
        dup=integer(r.get("duplicate_match_ids_within_season"),"duplicate_match_ids_within_season")
        past=integer(r.get("incomplete_status_records_with_past_kickoff"),"incomplete_status_records_with_past_kickoff")
        future=integer(r.get("complete_status_records_with_future_kickoff"),"complete_status_records_with_future_kickoff")
        susp=integer(r.get("suspended_status_records_with_parseable_score_pair"),"suspended_status_records_with_parseable_score_pair")
        if pw>n or uid>pw or comp+noncomp!=pw or max(dup,past,future,susp)>n: raise ValueError(f"count reconciliation failed: {sid}")
        sc=statuses(r.get("provider_status_counts_json"))
        if sum(sc.values())!=n: raise ValueError(f"provider statuses do not sum to match rows: {sid}")
        if not all(boolean(r.get(f),f) for f in FLAGS): raise ValueError(f"archive payload missing: {sid}")
        first,last=day(r.get("kickoff_date_min"),"kickoff_date_min"),day(r.get("kickoff_date_max"),"kickoff_date_max")
        if n and (not first or not last or first>last): raise ValueError(f"invalid date range: {sid}")
        bucket=("INTERSECTS_PRIMARY_WINDOW" if pw else
                "FUTURE_ONLY_AFTER_PRIMARY_WINDOW" if first and first>end else
                "HISTORICAL_ONLY_BEFORE_PRIMARY_WINDOW" if last and last<start else
                "NO_PRIMARY_ROWS_UNCLASSIFIED")
        out.append({"season_id":sid,"country":country,"competition_name":league,"selected_current_season":selected,
            "ingestion_status":r.get("ingestion_status",""),"match_records":n,"team_records":teams,
            "kickoff_date_min":first.isoformat() if first else "","kickoff_date_max":last.isoformat() if last else "",
            "primary_window_match_records":pw,"primary_window_unique_provider_match_ids":uid,
            "primary_window_complete_status_records":comp,"primary_window_noncomplete_status_records":noncomp,
            "coverage_bucket":bucket,"status_counts":sc,"incomplete_status_records_with_past_kickoff":past,
            "complete_status_records_with_future_kickoff":future,"suspended_status_records_with_parseable_score_pair":susp,
            "duplicate_match_ids_within_season":dup})
    if len(groups)!=50 or any(v!=4 for v in groups.values()) or any(current[g]!=1 for g in groups):
        raise ValueError("expected 50 groups, four seasons and exactly one current season per group")
    if sum(x["primary_window_match_records"] for x in out)!=integer(report.get("primary_window_archive_match_records"),"archive primary rows"):
        raise ValueError("season primary-window rows do not reconcile to archive")
    return out

def summarize(r, rows, start, end, audit):
    cur=[x for x in rows if x["selected_current_season"]]; all_b=Counter(x["coverage_bucket"] for x in rows); cur_b=Counter(x["coverage_bucket"] for x in cur)
    cur_status=Counter()
    for x in cur: cur_status.update(x["status_counts"])
    past_cur=sum(x["incomplete_status_records_with_past_kickoff"] for x in cur)
    past_old=sum(x["incomplete_status_records_with_past_kickoff"] for x in rows if not x["selected_current_season"])
    team=[x["team_records"] for x in cur]; matches=[x["match_records"] for x in cur]
    future=[{k:x[k] for k in ("country","competition_name","season_id","match_records","team_records","kickoff_date_min","kickoff_date_max","status_counts")} for x in cur if x["coverage_bucket"]=="FUTURE_ONLY_AFTER_PRIMARY_WINDOW"]
    nc=integer(r.get("noncomplete_status_records_with_parseable_score_pair"),"noncomplete score pairs")
    nz=integer(r.get("noncomplete_status_records_with_zero_zero_score_pair"),"noncomplete 0-0 pairs")
    nn=integer(r.get("noncomplete_status_records_with_nonzero_score_pair"),"noncomplete nonzero pairs")
    return {"audit_date_utc":audit.isoformat(),"primary_window":{"start":start.isoformat(),"end":end.isoformat()},
        "archive_sha256":r.get("archive_sha256"),"archive_release_tag":r.get("archive_release_tag"),
        "selected_league_groups":50,"season_rows":200,"seasons_per_league_group":4,
        "ingested_season_rows":sum(x["ingestion_status"].upper()=="INGESTED" for x in rows),
        "all_required_season_payloads_present":True,"archive_match_records":integer(r.get("total_match_records"),"archive rows"),
        "archive_team_records_across_seasons":integer(r.get("total_team_records"),"team records"),
        "primary_window_match_records":integer(r.get("primary_window_archive_match_records"),"primary rows"),
        "primary_window_unique_provider_match_ids":integer(r.get("primary_window_archive_unique_provider_match_ids"),"unique IDs"),
        "primary_window_provider_status_counts":r.get("primary_window_provider_status_counts",{}),
        "season_coverage_buckets_all":dict(all_b),"current_season_count":len(cur),
        "current_season_coverage_buckets":dict(cur_b),"current_season_match_records":sum(matches),
        "current_season_status_counts":dict(cur_status),"current_season_team_record_count_sum":sum(team),
        "current_season_team_record_count_min_median_max":{"min":min(team),"median":median(team),"max":max(team)},
        "current_season_match_record_count_min_median_max":{"min":min(matches),"median":median(matches),"max":max(matches)},
        "current_seasons_future_only_after_primary_window":future,
        "incomplete_status_past_kickoff":{"all_archive":integer(r.get("incomplete_status_records_with_past_kickoff"),"past incomplete"),
            "current_selected_seasons":past_cur,"historical_seasons":past_old,
            "affected_current_seasons":sum(x["incomplete_status_records_with_past_kickoff"]>0 for x in cur),
            "affected_historical_seasons":sum(x["incomplete_status_records_with_past_kickoff"]>0 for x in rows if not x["selected_current_season"]),
            "primary_window_incomplete_status_rows":integer(r.get("primary_window_provider_status_counts",{}).get("incomplete",0),"primary incomplete")},
        "future_complete_status_rows":integer(r.get("complete_status_records_with_future_kickoff"),"future complete"),
        "noncomplete_score_pair_diagnostics":{"parseable_pairs":nc,"zero_zero_pairs":nz,"nonzero_pairs":nn,"all_zero_zero":nc==nz and nn==0},
        "completed_zero_zero_score_pairs":integer(r.get("complete_status_records_with_zero_zero_score_pair"),"complete 0-0"),
        "duplicate_match_ids_within_season":sum(x["duplicate_match_ids_within_season"] for x in rows),
        "official_settlement_truth_verified":False,"production_eligible":False,
        "interpretation":"EVENT_TIME_AND_ARCHIVE_STATUS_ONLY; NOT SOURCE_RETRIEVAL_FRESHNESS OR OFFICIAL SETTLEMENT TRUTH"}

def write_csv(path, rows, columns):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=columns,extrasaction="ignore"); w.writeheader(); w.writerows(rows)

def run(indir,outdir):
    r=json.loads((indir/"selected50_archive_qa.json").read_text(encoding="utf-8")); start,end,audit=validate_report(r)
    with (indir/"selected50_season_qa.csv").open(encoding="utf-8-sig",newline="") as f: rows=build_rows(list(csv.DictReader(f)),r,start,end)
    s=summarize(r,rows,start,end,audit); outdir.mkdir(parents=True,exist_ok=True)
    (outdir/"oracle_selected50_season_event_time_summary.json").write_text(json.dumps(s,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    cur=[x for x in rows if x["selected_current_season"]]
    anomalies=[x for x in rows if x["incomplete_status_records_with_past_kickoff"] or x["suspended_status_records_with_parseable_score_pair"] or x["complete_status_records_with_future_kickoff"]]
    current_cols=["country","competition_name","season_id","match_records","team_records","kickoff_date_min","kickoff_date_max","primary_window_match_records","primary_window_unique_provider_match_ids","primary_window_complete_status_records","primary_window_noncomplete_status_records","coverage_bucket","incomplete_status_records_with_past_kickoff","complete_status_records_with_future_kickoff","suspended_status_records_with_parseable_score_pair","status_counts"]
    anomaly_cols=["country","competition_name","season_id","selected_current_season","match_records","kickoff_date_min","kickoff_date_max","incomplete_status_records_with_past_kickoff","complete_status_records_with_future_kickoff","suspended_status_records_with_parseable_score_pair","coverage_bucket","status_counts"]
    write_csv(outdir/"oracle_selected50_current_season_event_time_coverage.csv",cur,current_cols)
    write_csv(outdir/"oracle_selected50_season_status_anomaly_rollup.csv",anomalies,anomaly_cols)
    return s

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--input-dir",type=Path,required=True); p.add_argument("--output-dir",type=Path,required=True); a=p.parse_args()
    print(json.dumps(run(a.input_dir,a.output_dir),sort_keys=True))
