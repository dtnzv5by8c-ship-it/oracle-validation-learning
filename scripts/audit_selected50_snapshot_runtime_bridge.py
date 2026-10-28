#!/usr/bin/env python3
"""Read-only exact-ID audit between a sanitized FootyStats snapshot and research runtime report.

This tool does not generate predictions, alter model logic, or approve production/betting.
"""
import argparse, csv, hashlib, json
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

def no_home_away_flag(value):
    """Return True/False only for explicit provider values; unknown stays unknown."""
    if isinstance(value, bool):
        return value
    raw = s(value).casefold()
    if raw in {"1", "1.0", "true", "yes"}:
        return True
    if raw in {"0", "0.0", "false", "no"}:
        return False
    return None

def verify_runtime_provenance(args, snapshot_sha256):
    """Verify the exact snapshot, runtime run, selected archive and report hashes."""
    result = {
        "verified": False,
        "status": "UNVERIFIED_RUNTIME_PROVENANCE_MISSING",
        "runtime_provenance_sha256": None,
        "runtime_provenance_runtime_run_id": None,
        "runtime_provenance_snapshot_run_id": None,
        "runtime_input_archive_sha256": None,
        "runtime_input_archive_sha256_before_runtime": None,
        "runtime_report_sha256": None,
        "snapshot_artifact_name": None,
        "snapshot_artifact_id": None,
        "snapshot_artifact_digest": None,
        "snapshot_artifact_metadata_sha256": None,
        "snapshot_artifact_workflow_run_id": None,
        "checks": {},
    }
    path = args.runtime_provenance
    if path is None or not path.is_file():
        return result

    raw = path.read_bytes()
    provenance = json.loads(raw.decode("utf-8"))
    result["runtime_provenance_sha256"] = hashlib.sha256(raw).hexdigest()
    result["runtime_provenance_runtime_run_id"] = s(provenance.get("runtime_run_id"))
    result["runtime_provenance_snapshot_run_id"] = s(provenance.get("snapshot_run_id"))
    result["runtime_input_archive_sha256"] = s(provenance.get("selected_runtime_input_archive_sha256"))
    result["runtime_input_archive_sha256_before_runtime"] = s(provenance.get("selected_runtime_input_archive_sha256_before_runtime"))
    result["runtime_report_sha256"] = s(provenance.get("runtime_report_sha256"))
    result["snapshot_artifact_name"] = s(provenance.get("snapshot_artifact_name"))
    result["snapshot_artifact_id"] = s(provenance.get("snapshot_artifact_id"))
    result["snapshot_artifact_digest"] = s(provenance.get("snapshot_artifact_digest"))
    result["snapshot_artifact_metadata_sha256"] = s(provenance.get("snapshot_artifact_metadata_sha256"))
    result["snapshot_artifact_workflow_run_id"] = s(provenance.get("snapshot_artifact_workflow_run_id"))

    checks = {
        "snapshot_consumption_flag_true": provenance.get("snapshot_consumption_verified") is True,
        "snapshot_consumption_status_pass": s(provenance.get("snapshot_consumption_status")) == "PASS_SNAPSHOT_TO_RUNTIME_INPUT_HASH_VERIFIED",
        "snapshot_sha256_matches_supplied_snapshot": s(provenance.get("snapshot_file_sha256")) == snapshot_sha256,
        "expected_snapshot_run_id_matches": bool(args.expected_snapshot_run_id) and s(provenance.get("snapshot_run_id")) == s(args.expected_snapshot_run_id),
        "expected_runtime_run_id_matches": bool(args.expected_runtime_run_id) and s(provenance.get("runtime_run_id")) == s(args.expected_runtime_run_id),
        "snapshot_artifact_name_matches_expected": s(provenance.get("snapshot_artifact_name")) == "oracle-selected50-current-fixture-snapshot",
        "snapshot_artifact_id_present": bool(s(provenance.get("snapshot_artifact_id"))),
        "snapshot_artifact_digest_is_sha256": s(provenance.get("snapshot_artifact_digest")).startswith("sha256:") and len(s(provenance.get("snapshot_artifact_digest")).split(":", 1)[1]) == 64,
        "snapshot_artifact_metadata_sha256_is_valid": len(s(provenance.get("snapshot_artifact_metadata_sha256"))) == 64,
        "snapshot_artifact_run_id_matches": bool(args.expected_snapshot_run_id) and s(provenance.get("snapshot_artifact_workflow_run_id")) == s(args.expected_snapshot_run_id),
        "selected_input_matches_overlay_flag": provenance.get("selected_input_matches_overlay") is True,
        "selected_input_hash_matches_overlay_hash": bool(s(provenance.get("selected_runtime_input_archive_sha256"))) and s(provenance.get("selected_runtime_input_archive_sha256")) == s(provenance.get("overlay_archive_sha256")),
        "runtime_input_hash_matches_pre_runtime_fingerprint": bool(s(provenance.get("selected_runtime_input_archive_sha256_before_runtime"))) and s(provenance.get("selected_runtime_input_archive_sha256_before_runtime")) == s(provenance.get("selected_runtime_input_archive_sha256")),
        "runtime_report_hash_matches_downloaded_report": bool(s(provenance.get("runtime_report_sha256"))) and s(provenance.get("runtime_report_sha256")) == hashlib.sha256(args.runtime_report.read_bytes()).hexdigest(),
    }
    result["checks"] = checks
    failed = [name for name, passed in checks.items() if not passed]
    result["verified"] = not failed
    result["status"] = "PASS_SNAPSHOT_TO_RUNTIME_PROVENANCE_VERIFIED" if not failed else "BLOCKED_RUNTIME_PROVENANCE_CHECKS_FAILED"
    result["failed_checks"] = failed
    result["runtime_ref"] = s(provenance.get("runtime_ref"))
    result["runtime_commit_sha"] = s(provenance.get("runtime_commit_sha"))
    result["runtime_archive_env"] = s(provenance.get("runtime_archive_env"))
    result["selected_runtime_input_archive"] = s(provenance.get("selected_runtime_input_archive"))
    result["snapshot_file_sha256"] = s(provenance.get("snapshot_file_sha256"))
    result["overlay_archive_sha256"] = s(provenance.get("overlay_archive_sha256"))
    result["selected_runtime_input_archive_sha256_before_runtime"] = s(provenance.get("selected_runtime_input_archive_sha256_before_runtime"))
    result["snapshot_artifact_metadata_sha256"] = s(provenance.get("snapshot_artifact_metadata_sha256"))
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--snapshot", required=True, type=Path)
    p.add_argument("--runtime-report", required=True, type=Path)
    p.add_argument("--runtime-provenance", type=Path)
    p.add_argument("--expected-snapshot-run-id")
    p.add_argument("--expected-runtime-run-id")
    p.add_argument("--require-runtime-provenance", action="store_true", help="Return a nonzero exit if exact runtime provenance is missing or invalid")
    p.add_argument("--out-dir", required=True, type=Path)
    args=p.parse_args()
    snapshot_bytes=args.snapshot.read_bytes()
    snapshot_sha256=hashlib.sha256(snapshot_bytes).hexdigest()
    snap=json.loads(snapshot_bytes.decode("utf-8"))
    runtime=list(csv.DictReader(args.runtime_report.open(encoding="utf-8-sig", newline="")))
    provenance=verify_runtime_provenance(args, snapshot_sha256)
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
        noha=no_home_away_flag(f.get("no_home_away"))
        if noha is True:
            eligibility="QUARANTINE_NO_HOME_AWAY"
        elif noha is None:
            eligibility="QUARANTINE_NO_HOME_AWAY_FLAG_UNKNOWN"
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
            ids_match = home_ok and away_ok
            source_quarantined = (
                noha is not False
                or any(x in status for x in ("suspend", "postpon", "cancel", "abandon", "void"))
                or ko is None
                or (ko <= now and status not in {"complete","completed","finished","ft","full time"})
            )
            if not ids_match:
                join="EXACT_FIXTURE_ID_TEAM_ID_MISMATCH"
                counts["exact_id_team_mismatch"] += 1
            elif source_quarantined:
                join="EXACT_ID_TEAM_IDS_MATCH_BUT_SOURCE_QUARANTINED"
                counts["exact_id_and_team_ids_match_but_source_quarantined"] += 1
            else:
                join="EXACT_ID_AND_TEAM_IDS_MATCH"
                counts["exact_id_and_team_ids_match"] += 1
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
    report_window_end=now.timestamp()+7*24*60*60
    def kickoff_epoch(row):
        parsed=utc(row.get("kickoff_utc"))
        return parsed.timestamp() if parsed else None
    future_7d=[r for r in future if kickoff_epoch(r) is not None and kickoff_epoch(r) <= report_window_end]
    future_7d_joined=[r for r in future_7d if r["runtime_join_status"]=="EXACT_ID_AND_TEAM_IDS_MATCH"]
    future_7d_unmatched=[r for r in future_7d if r["runtime_join_status"]!="EXACT_ID_AND_TEAM_IDS_MATCH"]
    future_beyond_7d=[r for r in future if kickoff_epoch(r) is not None and kickoff_epoch(r) > report_window_end]
    unsafe_runtime_rows=[r for r in rows if r["runtime_join_status"]=="EXACT_ID_TEAM_IDS_MATCH_BUT_SOURCE_QUARANTINED"]
    qa={
      "status":"PASS_BRIDGE_AUDIT_RESEARCH_ONLY" if not (unsafe_runtime_rows or future_7d_unmatched or not provenance["verified"]) else "PASS_BRIDGE_AUDIT_WITH_RELEASE_BLOCKERS",
      "generated_utc":now.isoformat(),
      "snapshot_retrieved_utc":snap.get("retrieved_utc"),
      "snapshot_sha256":snapshot_sha256,
      "snapshot_artifact_name":provenance.get("snapshot_artifact_name"),
      "snapshot_artifact_id":provenance.get("snapshot_artifact_id"),
      "snapshot_artifact_digest":provenance.get("snapshot_artifact_digest"),
      "runtime_input_archive":provenance.get("selected_runtime_input_archive"),
      "runtime_input_archive_sha256":provenance.get("runtime_input_archive_sha256"),
      "runtime_input_archive_sha256_before_runtime":provenance.get("runtime_input_archive_sha256_before_runtime"),
      "runtime_report_sha256":provenance.get("runtime_report_sha256"),
      "snapshot_consumption_verified":provenance["verified"],
      "snapshot_consumption_status":provenance["status"],
      "snapshot_runtime_provenance":provenance,
      "expected_snapshot_run_id":s(args.expected_snapshot_run_id),
      "expected_runtime_run_id":s(args.expected_runtime_run_id),
      "selected_seasons":len(season_ids),
      "snapshot_fixture_rows":len(snap.get("fixture_rows",[])),
      "runtime_report_rows":len(runtime),
      "unique_runtime_exact_keys":len(rt),
      "duplicate_runtime_exact_keys":duplicate_runtime,
      "future_research_candidates":len(future),
      "future_candidates_exact_id_and_team_match":len(future_joined),
      "future_candidates_without_exact_id_and_team_match":len(future)-len(future_joined),
      "seven_day_report_window_end_utc":datetime.fromtimestamp(report_window_end,timezone.utc).isoformat(),
      "future_candidates_within_7d_window":len(future_7d),
      "future_candidates_within_7d_exactly_matched":len(future_7d_joined),
      "future_candidates_within_7d_missing_runtime_match":len(future_7d_unmatched),
      "future_candidates_beyond_7d_report_window":len(future_beyond_7d),
      "within_7d_match_coverage_pct":round(100*len(future_7d_joined)/len(future_7d),2) if future_7d else None,
      "within_7d_missing_fixture_ids":[{"season_id":r["source_season_id"],"fixture_id":r["source_match_id"],"kickoff_utc":r["kickoff_utc"],"home_team":r["home_team"],"away_team":r["away_team"]} for r in future_7d_unmatched],
      "runtime_rows_matching_source_but_source_quarantined":len(unsafe_runtime_rows),
      "runtime_rows_with_safe_future_candidate_status":len(future_joined),
      "all_source_rows_exactly_joined":sum(r["runtime_join_status"] in {"EXACT_ID_AND_TEAM_IDS_MATCH","EXACT_ID_TEAM_IDS_MATCH_BUT_SOURCE_QUARANTINED"} for r in rows),
      "counts":dict(sorted(counts.items())),
      "production_eligible":False,
      "betting_eligible":False,
      "prediction_generated":False,
      "interpretation":"Exact join coverage is not proof of snapshot consumption. Snapshot consumption is marked verified only when the supplied runtime provenance artifact matches the exact snapshot SHA-256 and expected snapshot/runtime run IDs, confirms the selected runtime input archive hash equals the overlay archive hash, and matches the downloaded runtime prediction-report SHA-256. Missing or mismatched provenance remains a release blocker. This audit does not grant production or betting eligibility."
    }
    (args.out_dir/"oracle_selected50_snapshot_runtime_bridge_qa.json").write_text(json.dumps(qa,indent=2,sort_keys=True) + "\\n",encoding="utf-8")
    print(json.dumps(qa,indent=2,sort_keys=True))
    if args.require_runtime_provenance and not provenance["verified"]:
        raise SystemExit("FAIL: required snapshot-to-runtime provenance is missing or failed verification; see bridge QA output")
if __name__=="__main__":
    main()
