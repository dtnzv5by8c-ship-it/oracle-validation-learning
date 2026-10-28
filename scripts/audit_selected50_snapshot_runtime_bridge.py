#!/usr/bin/env python3
"""Read-only exact-ID audit between a sanitized FootyStats snapshot and research runtime report.

This tool does not generate predictions, alter model logic, or approve production/betting.
"""
import argparse, csv, json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

def utc(value):
    if not value:
        return None
    try:
        d = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if d.tzinfo is None:
            return None
        return d.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None

def s(value):
    return "" if value is None else str(value).strip()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--snapshot", required=True, type=Path)
    p.add_argument("--runtime-report", required=True, type=Path)
    p.add_argument("--out-dir", required=True, type=Path)
    args=p.parse_args()
    snap=json.loads(args.snapshot.read_text(encoding="utf-8"))
    runtime=list(csv.DictReader(args.runtime_report.open(encoding="utf-8-sig", newline="")))
    if len(snap.get("per_season", [])) != 50 or len({s(x.get("selected_season_id")) for x in snap.get("per_season", [])}) != 50:
        raise SystemExit("FAIL: snapshot must contain exactly 50 unique selected season IDs")
    season_ids={s(x.get("selected_season_id")) for x in snap["per_season"]}
    if any(not x for x in season_ids):
        raise SystemExit("FAIL: blank selected season ID in snapshot")
    if not runtime or not {"fixture_id","provider_season_id","home_team_provider_id","away_team_provider_id"}.issubset(runtime[0]):
        raise SystemExit("FAIL: runtime report lacks required provider identity columns")
    rt={}
    duplicate_runtime=0
    for r in runtime:
        key=(s(r.get("provider_season_id")),s(r.get("fixture_id")))
        if not all(key):
            continue
        if key in rt:
            duplicate_runtime += 1
        else:
            rt[key]=r
    now=datetime.now(timezone.utc)
    rows=[]
    counts=Counter()
    seen=set()
    for f in snap.get("fixture_rows", []):
        season=s(f.get("selected_season_id")); match=s(f.get("id"))
        key=(season,match)
        if not season or not match or season not in season_ids:
            counts["invalid_source_identity"] += 1
            continue
        if key in seen:
            counts["duplicate_source_identity"] += 1
            continue
        seen.add(key)
        ko=utc(f.get("kickoff_utc"))
        status=s(f.get("status")).lower()
        noha=str(f.get("no_home_away","")).lower() in {"1","true","yes"}
        if noha:
            eligibility="QUARANTINE_NO_HOME_AWAY"
        elif any(x in status for x in ("suspend","postpon","cancel","abandon","void")):
            eligibility="QUARANTINE_NONSTANDARD_STATUS"
        elif ko is None:
            eligibility="QUARANTINE_INVALID_KICKOFF"
        elif ko <= now and status not in {"complete","completed","finished","ft","full time"}:
            eligibility="QUARANTINE_NONFUTURE_UNSETTLED"
        elif ko <= now:
            eligibility="HISTORICAL_NOT_CURRENT_FIXTURE"
        else:
            eligibility="FUTURE_RESEARCH_CANDIDATE"
        r=rt.get(key)
        if r is None:
            join="NO_EXACT_RUNTIME_ROW"
        else:
            counts["exact_season_match_join"] += 1
            home_ok=s(f.get("homeID")) == s(r.get("home_team_provider_id"))
            away_ok=s(f.get("awayID")) == s(r.get("away_team_provider_id"))
            join="EXACT_ID_AND_TEAM_IDS_MATCH" if home_ok and away_ok else "EXACT_FIXTURE_ID_TEAM_ID_MISMATCH"
            if join == "EXACT_ID_AND_TEAM_IDS_MATCH":
                counts["exact_id_and_team_ids_match"] += 1
            else:
                counts["exact_id_team_mismatch"] += 1
        rows.append({
            "source_season_id":season,"source_match_id":match,
            "kickoff_utc":s(f.get("kickoff_utc")),"source_status":s(f.get("status")),
            "home_team":s(f.get("home_name")),"away_team":s(f.get("away_name")),
            "source_home_team_id":s(f.get("homeID")),"source_away_team_id":s(f.get("awayID")),
            "fixture_eligibility":eligibility,"runtime_join_status":join,
            "runtime_fixture_id":s(r.get("fixture_id")) if r else "",
            "runtime_home_team_id":s(r.get("home_team_provider_id")) if r else "",
            "runtime_away_team_id":s(r.get("away_team_provider_id")) if r else "",
        })
        counts[eligibility] += 1
    args.out_dir.mkdir(parents=True,exist_ok=True)
    fields=list(rows[0]) if rows else ["source_season_id","source_match_id","fixture_eligibility","runtime_join_status"]
    with (args.out_dir/"oracle_selected50_snapshot_runtime_bridge.csv").open("w",encoding="utf-8",newline="") as h:
        w=csv.DictWriter(h,fieldnames=fields); w.writeheader(); w.writerows(rows)
    future=[r for r in rows if r["fixture_eligibility"]=="FUTURE_RESEARCH_CANDIDATE"]
    future_joined=[r for r in future if r["runtime_join_status"]=="EXACT_ID_AND_TEAM_IDS_MATCH"]
    qa={
      "status":"PASS_BRIDGE_AUDIT_EXECUTED_RESEARCH_ONLY",
      "generated_utc":now.isoformat(),
      "snapshot_retrieved_utc":snap.get("retrieved_utc"),
      "snapshot_sha256":None,
      "selected_seasons":len(season_ids),
      "snapshot_fixture_rows":len(snap.get("fixture_rows",[])),
      "runtime_report_rows":len(runtime),
      "unique_runtime_exact_keys":len(rt),
      "duplicate_runtime_exact_keys":duplicate_runtime,
      "future_research_candidates":len(future),
      "future_candidates_exact_id_and_team_match":len(future_joined),
      "future_candidates_without_exact_id_and_team_match":len(future)-len(future_joined),
      "all_source_rows_exactly_joined":sum(r["runtime_join_status"]=="EXACT_ID_AND_TEAM_IDS_MATCH" for r in rows),
      "counts":dict(sorted(counts.items())),
      "production_eligible":False,
      "betting_eligible":False,
      "prediction_generated":False,
      "interpretation":"Exact join coverage audit only. Runtime predictions were generated from the existing archive; this report does not claim the current snapshot was consumed by the model runtime."
    }
    (args.out_dir/"oracle_selected50_snapshot_runtime_bridge_qa.json").write_text(json.dumps(qa,indent=2,sort_keys=True),encoding="utf-8")
    print(json.dumps(qa,indent=2,sort_keys=True))
if __name__=="__main__":
    main()
