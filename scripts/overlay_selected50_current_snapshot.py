#!/usr/bin/env python3
"""Research-only, fail-closed overlay of fresh FootyStats fixtures onto the historical archive.

Only future, standard home/away fixtures inside the next 7 days are staged.
No predictions are produced here. Production model logic and probabilities are untouched.
"""
import argparse, csv, hashlib, json, math, zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

BAD_STATUS=("suspend","postpon","cancel","abandon","void","delay")

def future_status_quarantine_reason(value):
    """Fail closed against the documented provider status enum for future fixtures."""
    status = str(value or "").strip().casefold()
    if not status:
        return "MISSING_STATUS"
    # The documented enum is complete/suspended/canceled/incomplete.
    # Only incomplete is coherent with a future scheduled fixture.
    if status == "incomplete":
        return None
    if status == "complete":
        return "STATUS_INCONSISTENT_WITH_FUTURE_KICKOFF"
    if status in {"suspended", "canceled"} or any(token in status for token in BAD_STATUS):
        return "NONSTANDARD_STATUS"
    return "UNKNOWN_STATUS_VALUE"
TRACE_COLUMNS = [
    "snapshot_row_number", "snapshot_file_sha256", "source_archive_sha256", "snapshot_retrieved_utc",
    "selected_season_id", "selected_country", "selected_competition", "fixture_id", "kickoff_utc", "status", "no_home_away",
    "home_team_provider_id", "away_team_provider_id", "trace_outcome", "trace_reason",
    "target_archive_season_id", "production_eligible", "betting_eligible",
    "canonical_fixture_join_status", "canonical_team_join_status",
    "official_settlement_truth_status",
]

def parse_utc(v):
    if not isinstance(v,str) or not v.strip(): return None
    try: d=datetime.fromisoformat(v.strip().replace("Z","+00:00"))
    except ValueError: return None
    if d.tzinfo is None or d.utcoffset() is None: return None
    return d.astimezone(timezone.utc)

def valid_id(v):
    if isinstance(v, bool) or v is None:
        return False
    raw = str(v).strip()
    if raw.casefold() in {"", "0", "0.0", "none", "null", "false", "true"}:
        return False
    try:
        numeric = float(raw)
    except (TypeError, ValueError, OverflowError):
        numeric = None
    if numeric is not None and (not math.isfinite(numeric) or numeric <= 0 or not numeric.is_integer()):
        return False
    return True

def no_home_away_flag(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        if not math.isfinite(float(value)):
            return None
        if float(value) == 1:
            return True
        if float(value) == 0:
            return False
        return None
    raw = str(value or "").strip().casefold()
    if raw in {"1", "1.0", "true", "yes"}:
        return True
    if raw in {"0", "0.0", "false", "no"}:
        return False
    return None

def make_trace_row(row_number, row, snapshot_sha256, archive_sha256, retrieved_utc, season_meta=None):
    source = row if isinstance(row, dict) else {}
    season_meta = season_meta or {}
    return {
        "snapshot_row_number": row_number,
        "snapshot_file_sha256": snapshot_sha256,
        "source_archive_sha256": archive_sha256,
        "snapshot_retrieved_utc": retrieved_utc,
        "selected_season_id": str(source.get("selected_season_id") or "").strip(),
        "selected_country": str(season_meta.get("country") or "").strip(),
        "selected_competition": str(season_meta.get("competition") or "").strip(),
        "fixture_id": str(source.get("id") or "").strip(),
        "kickoff_utc": str(source.get("kickoff_utc") or "").strip(),
        "status": str(source.get("status") or "").strip(),
        "no_home_away": str(source.get("no_home_away") if source.get("no_home_away") is not None else ""),
        "home_team_provider_id": str(source.get("homeID") or "").strip(),
        "away_team_provider_id": str(source.get("awayID") or "").strip(),
        "trace_outcome": "",
        "trace_reason": "",
        "target_archive_season_id": "",
        "production_eligible": "NO",
        "betting_eligible": "NO",
        "canonical_fixture_join_status": "NOT_VERIFIED",
        "canonical_team_join_status": "NOT_VERIFIED",
        "official_settlement_truth_status": "NOT_VERIFIED",
    }

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def write_trace(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as trace_file:
        writer = csv.DictWriter(trace_file, fieldnames=TRACE_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def find_archive_path(names, season_id, kind):
    suffix=f"seasons/{season_id}/{kind}.json"
    matches=[name for name in names if name.endswith(suffix)]
    if len(matches)>1:
        raise SystemExit(f"FAIL: ambiguous archive path for season {season_id} {kind}")
    return matches[0] if matches else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--archive",required=True,type=Path)
    ap.add_argument("--snapshot",required=True,type=Path)
    ap.add_argument("--out-archive",required=True,type=Path)
    ap.add_argument("--out-qa",required=True,type=Path)
    ap.add_argument("--out-trace",type=Path,help="Sanitized row-level snapshot staging trace CSV")
    args=ap.parse_args()
    trace_path=args.out_trace or args.out_qa.with_name("current_snapshot_candidate_trace.csv")
    now=datetime.now(timezone.utc)
    snapshot_bytes=args.snapshot.read_bytes()
    snapshot_sha256=hashlib.sha256(snapshot_bytes).hexdigest()
    archive_sha256=sha256_file(args.archive)
    snap=json.loads(snapshot_bytes.decode("utf-8"))
    retrieved=parse_utc(snap.get("retrieved_utc"))
    if retrieved is None or retrieved>now or now-retrieved>timedelta(hours=24):
        raise SystemExit("FAIL: snapshot provenance missing, future-dated, or older than 24 hours")
    seasons=snap.get("per_season")
    if not isinstance(seasons,list) or len(seasons)!=50:
        raise SystemExit("FAIL: expected exactly 50 per-season snapshot records")
    season_ids=[str(x.get("selected_season_id") or "").strip() for x in seasons]
    if any(not x for x in season_ids) or len(set(season_ids))!=50:
        raise SystemExit("FAIL: selected season IDs must be 50 unique nonblank values")
    if any(x.get("http_status")!=200 or x.get("provider_success") is not True for x in seasons):
        raise SystemExit("FAIL: one or more selected-season provider requests did not succeed")
    fixture_rows=snap.get("fixture_rows")
    if not isinstance(fixture_rows,list):
        raise SystemExit("FAIL: snapshot fixture_rows must be a list")
    season_set=set(season_ids)
    season_meta_by_id={str(x.get("selected_season_id") or "").strip():x for x in seasons if isinstance(x,dict)}
    staged=[]; trace_rows=[]; quarantined=0; beyond=0; beyond_total=0; beyond_quarantined=0; historical=0
    quarantine_reason_counts={}
    no_home_away_by_league={}
    for row_number, row in enumerate(fixture_rows, start=1):
        trace=make_trace_row(row_number,row,snapshot_sha256,archive_sha256,snap.get("retrieved_utc") or "",season_meta_by_id.get(str(row.get("selected_season_id") or "").strip()) if isinstance(row,dict) else None)
        trace_rows.append(trace)
        if not isinstance(row,dict):
            quarantined+=1
            trace["trace_outcome"]="QUARANTINED_NON_OBJECT_ROW"
            trace["trace_reason"]="FIXTURE_ROW_NOT_OBJECT"
            quarantine_reason_counts["FIXTURE_ROW_NOT_OBJECT"]=quarantine_reason_counts.get("FIXTURE_ROW_NOT_OBJECT",0)+1
            continue
        sid=str(row.get("selected_season_id") or "").strip()
        if sid not in season_set: raise SystemExit("FAIL: fixture row references season outside selected-50 manifest")
        ko=parse_utc(row.get("kickoff_utc"))
        if ko is None:
            quarantined+=1
            trace["trace_outcome"]="QUARANTINED_INVALID_KICKOFF"
            trace["trace_reason"]="KICKOFF_MISSING_MALFORMED_OR_TIMEZONE_NAIVE"
            quarantine_reason_counts["KICKOFF_MISSING_MALFORMED_OR_TIMEZONE_NAIVE"]=quarantine_reason_counts.get("KICKOFF_MISSING_MALFORMED_OR_TIMEZONE_NAIVE",0)+1
            continue
        if ko<=now:
            historical+=1
            trace["trace_outcome"]="HISTORICAL_NOT_STAGED"
            trace["trace_reason"]="KICKOFF_NOT_AFTER_OVERLAY_START"
            continue
        status=str(row.get("status") or "").strip().lower()
        flag=no_home_away_flag(row.get("no_home_away"))
        meta=season_meta_by_id.get(sid,{})
        within_7d = ko <= now+timedelta(days=7)
        if not within_7d:
            beyond_total+=1
        league_key=f"{meta.get('country', '')} | {meta.get('competition', '')}"
        league_diag=no_home_away_by_league.setdefault(league_key,{
            "selected_season_id":sid,"country":meta.get("country",""),"competition":meta.get("competition",""),
            "future_rows_in_7d":0,"future_rows_beyond_7d":0,
            "no_home_away_true":0,"no_home_away_false":0,"no_home_away_unknown":0,
            "no_home_away_true_beyond_7d":0,"no_home_away_false_beyond_7d":0,"no_home_away_unknown_beyond_7d":0,
            "suspended_or_nonstandard_status":0,"status_not_eligible_for_future_fixture":0,
            "suspended_or_nonstandard_status_beyond_7d":0,"status_not_eligible_for_future_fixture_beyond_7d":0
        })
        if within_7d:
            league_diag["future_rows_in_7d"]+=1
            league_diag["no_home_away_true" if flag is True else "no_home_away_false" if flag is False else "no_home_away_unknown"]+=1
        else:
            league_diag["future_rows_beyond_7d"]+=1
            league_diag["no_home_away_true_beyond_7d" if flag is True else "no_home_away_false_beyond_7d" if flag is False else "no_home_away_unknown_beyond_7d"]+=1
        reasons=[]
        if flag is True: reasons.append("NO_HOME_AWAY_FLAGGED")
        elif flag is None: reasons.append("NO_HOME_AWAY_FLAG_UNKNOWN")
        status_reason=future_status_quarantine_reason(status)
        if status_reason:
            reasons.append(status_reason)
            if within_7d:
                league_diag["status_not_eligible_for_future_fixture"]+=1
                if status_reason != "MISSING_STATUS":
                    league_diag["suspended_or_nonstandard_status"]+=1
            else:
                league_diag["status_not_eligible_for_future_fixture_beyond_7d"]+=1
                if status_reason != "MISSING_STATUS":
                    league_diag["suspended_or_nonstandard_status_beyond_7d"]+=1
        if not valid_id(row.get("id")): reasons.append("INVALID_FIXTURE_ID")
        if not valid_id(row.get("homeID")): reasons.append("INVALID_HOME_TEAM_ID")
        if not valid_id(row.get("awayID")): reasons.append("INVALID_AWAY_TEAM_ID")
        if not str(row.get("home_name") or "").strip(): reasons.append("MISSING_HOME_TEAM_NAME")
        if not str(row.get("away_name") or "").strip(): reasons.append("MISSING_AWAY_TEAM_NAME")
        if reasons:
            quarantined+=1
            if not within_7d:
                beyond_quarantined+=1
                reasons.append("OUTSIDE_7D_STAGING_HORIZON")
            trace["trace_outcome"]="QUARANTINED_INVALID_OR_NONSTANDARD"
            trace["trace_reason"]=";".join(reasons)
            for reason in reasons:
                quarantine_reason_counts[reason]=quarantine_reason_counts.get(reason,0)+1
            continue
        if not within_7d:
            beyond+=1
            trace["trace_outcome"]="BEYOND_7D_NOT_STAGED"
            trace["trace_reason"]="KICKOFF_AFTER_SEVEN_DAY_STAGING_HORIZON"
            continue
        trace["trace_outcome"]="ELIGIBLE_FOR_ARCHIVE_TARGET_RESOLUTION"
        trace["trace_reason"]="VALID_FUTURE_STANDARD_FIXTURE_WITH_SOURCE_TEAM_IDS"
        staged.append((sid,row,ko,trace))
    if len(staged)>1000: raise SystemExit("FAIL: unexpectedly large staging batch; manual review required")
    with zipfile.ZipFile(args.archive,"r") as src:
        names=src.namelist()
        manifest_path=next((n for n in names if n.endswith("ingestion_manifest.json")),None)
        if not manifest_path: raise SystemExit("FAIL: private archive ingestion manifest missing")
        manifest=json.loads(src.read(manifest_path).decode("utf-8"))
        if not isinstance(manifest,list): raise SystemExit("FAIL: unexpected private archive manifest shape")
        meta_by_id={str(m.get("season_id") or "").strip():m for m in manifest if isinstance(m,dict)}
        # Runtime groups historical season files by exact country + competition labels.
        # Current selected-season IDs may have no matches file; stage into a historical
        # season file from the same exact label only, never by fuzzy display-name matching.
        selected_labels={}
        for m in seasons:
            sid=str(m.get("selected_season_id") or "").strip()
            label=(str(m.get("country") or "").strip(),str(m.get("competition") or "").strip())
            if not all(label): raise SystemExit("FAIL: blank country/competition label in selected-50 snapshot")
            if label in selected_labels: raise SystemExit("FAIL: duplicate country/competition label in selected-50 snapshot")
            selected_labels[label]=sid
        archive_target={}
        unsupported_labels=[]
        for sid in season_ids:
            meta=meta_by_id.get(sid)
            if not meta: raise SystemExit(f"FAIL: selected season {sid} missing from archive manifest")
            label=(str(meta.get("selected_country") or "").strip(),str(meta.get("selected_competition_name") or "").strip())
            if label not in selected_labels or selected_labels[label]!=sid:
                raise SystemExit(f"FAIL: selected season {sid} label does not exactly match current snapshot manifest")
        unsupported_by_sid={}
        for sid in dict.fromkeys(item[0] for item in staged):
            meta=meta_by_id[sid]
            label=(str(meta.get("selected_country") or "").strip(),str(meta.get("selected_competition_name") or "").strip())
            candidates=[]
            for aid,ameta in meta_by_id.items():
                alabel=(str(ameta.get("selected_country") or "").strip(),str(ameta.get("selected_competition_name") or "").strip())
                mp=find_archive_path(names,aid,"matches")
                tp=find_archive_path(names,aid,"teams")
                if alabel==label and mp and tp:
                    candidates.append((aid,ameta))
            if not candidates:
                unsupported_by_sid[sid]={"selected_season_id":sid,"country":label[0],"competition":label[1],"reason":"NO_EXACT_LABEL_ARCHIVE_SEASON_WITH_MATCHES_AND_TEAMS"}
                continue
            # Prefer the selected season file if it has one; otherwise prefer the latest
            # season start label available, using manifest order only as deterministic tie-break.
            candidates.sort(key=lambda item:(item[0]==sid,str(item[1].get("season") or item[1].get("season_start") or "")),reverse=True)
            archive_target[sid]=candidates[0][0]
        unsupported_labels=list(unsupported_by_sid.values())
        season_files={}; season_match_paths={}
        for archive_sid in set(archive_target.values()):
            p=find_archive_path(names,archive_sid,"matches")
            if not p: raise SystemExit(f"FAIL: matches file missing for archive season {archive_sid}")
            season_match_paths[archive_sid]=p
            season_files[archive_sid]=json.loads(src.read(p).decode("utf-8"))
            if not isinstance(season_files[archive_sid],list): raise SystemExit(f"FAIL: archive match container is not a list for season {archive_sid}")
        seen=set(); add_count=0; already=0; refreshed=0; conflicts=0; unsupported_rows=0
        for sid,row,ko,trace in staged:
            if sid not in archive_target:
                unsupported_rows+=1
                trace["trace_outcome"]="UNSUPPORTED_ARCHIVE_NO_EXACT_LABEL_SEASON_WITH_MATCHES_AND_TEAMS"
                trace["trace_reason"]="NO_EXACT_LABEL_ARCHIVE_SEASON_WITH_MATCHES_AND_TEAMS"
                continue
            archive_sid=archive_target[sid]
            trace["target_archive_season_id"]=archive_sid
            records=season_files[archive_sid]
            by_id={str(m.get("id")):m for m in records if isinstance(m,dict) and valid_id(m.get("id"))}
            fid=str(row.get("id") or "").strip()
            if not fid:
                quarantined+=1
                trace["trace_outcome"]="QUARANTINED_INVALID_OR_NONSTANDARD"
                trace["trace_reason"]="INVALID_FIXTURE_ID"
                continue
            if fid in by_id:
                old=by_id[fid]
                old_pair=(str(old.get("homeID") or ""),str(old.get("awayID") or ""))
                new_pair=(str(row.get("homeID") or ""),str(row.get("awayID") or ""))
                if old_pair!=new_pair:
                    conflicts+=1
                    trace["trace_outcome"]="CONFLICT_FIXTURE_ID_TEAM_PAIR"
                    trace["trace_reason"]="EXACT_PROVIDER_FIXTURE_ID_HAS_DIFFERENT_HOME_AWAY_TEAM_IDS"
                    write_trace(trace_path,trace_rows)
                    raise SystemExit(f"FAIL: fixture ID {fid} conflicts with archive team IDs in archive season {archive_sid}")
                # An exact ID/team match can still carry stale schedule/status fields in the
                # historical archive. Refresh only provider-supplied, non-empty identity and
                # scheduling fields in this isolated research copy; preserve historical stats
                # and all fields absent from the fresh snapshot.
                refresh_fields = (
                    "kickoff_utc", "date_unix", "kickoff_unix", "timestamp", "kickoff",
                    "date", "datetime", "match_date", "status", "game_status",
                    "no_home_away", "homeID", "awayID", "home_id", "away_id",
                    "home_name", "away_name", "homeTeam", "awayTeam",
                )
                changed_fields = []
                for field in refresh_fields:
                    fresh_value = row.get(field)
                    if fresh_value not in (None, "") and old.get(field) != fresh_value:
                        old[field] = fresh_value
                        changed_fields.append(field)
                if changed_fields:
                    refreshed += 1
                    trace["trace_outcome"]="REFRESHED_PRESENT_EXACT_FIXTURE_ID_AND_TEAM_IDS"
                    trace["trace_reason"]="EXACT_PROVIDER_FIXTURE_ID_AND_ORDERED_TEAM_IDS_MATCH; FRESH_NONEMPTY_SCHEDULE_FIELDS_REFRESHED: " + ";".join(changed_fields)
                else:
                    already+=1
                    trace["trace_outcome"]="ALREADY_PRESENT_EXACT_FIXTURE_ID_AND_TEAM_IDS"
                    trace["trace_reason"]="PROVIDER_FIXTURE_ID_AND_ORDERED_TEAM_IDS_MATCH_ARCHIVE; NO_REFRESHABLE_FIELD_CHANGED"
                continue
            if (archive_sid,fid) in seen:
                trace["trace_outcome"]="DUPLICATE_SNAPSHOT_FIXTURE_KEY"
                trace["trace_reason"]="DUPLICATE_ARCHIVE_SEASON_AND_FIXTURE_ID_IN_SNAPSHOT"
                write_trace(trace_path,trace_rows)
                raise SystemExit(f"FAIL: duplicate snapshot fixture key {archive_sid}/{fid}")
            seen.add((archive_sid,fid))
            # Keep provider-native fields, with no derived identities or invented data.
            clean=dict(row)
            clean["id"]=row["id"]
            records.append(clean)
            add_count+=1
            trace["trace_outcome"]="STAGED_PROVIDER_NATIVE_ROW_RESEARCH_ONLY"
            trace["trace_reason"]="EXACT_PROVIDER_NATIVE_ID_STAGED_WITHOUT_CANONICAL_JOIN_APPROVAL"
        args.out_archive.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(args.out_archive,"w",zipfile.ZIP_DEFLATED) as dst:
            for info in src.infolist():
                archive_sid=next((sid for sid,p in season_match_paths.items() if info.filename==p),None)
                data=json.dumps(season_files[archive_sid],separators=(",",":"),ensure_ascii=False).encode("utf-8") if archive_sid is not None else src.read(info.filename)
                dst.writestr(info,data)
    trace_outcome_counts={}
    for trace in trace_rows:
        outcome=trace.get("trace_outcome") or "UNCLASSIFIED_TRACE_OUTCOME"
        trace_outcome_counts[outcome]=trace_outcome_counts.get(outcome,0)+1
    write_trace(trace_path,trace_rows)
    # Hash the exact overlay ZIP that the runtime workflow must select as its input.
    overlay_archive_sha256=sha256_file(args.out_archive)
    qa={
      "status":"PASS_RESEARCH_ONLY_STAGED" if conflicts==0 and not unsupported_labels else ("PARTIAL_RESEARCH_ONLY_UNSUPPORTED_LEAGUES" if conflicts==0 else "FAIL"),
      "source_provider":"FootyStats","snapshot_retrieved_utc":snap.get("retrieved_utc"),
      "snapshot_file_sha256":snapshot_sha256,"source_archive_sha256":archive_sha256,
      "overlay_archive_sha256":overlay_archive_sha256,
      "snapshot_age_seconds":int((now-retrieved).total_seconds()),
      "selected_seasons":50,"snapshot_fixture_rows":len(fixture_rows),
      "staged_window_days":7,"candidate_rows_added":add_count,
      "future_rows_beyond_7d_total":beyond_total,"future_rows_beyond_7d_quarantined":beyond_quarantined,
      "already_present_exact_fixture_ids":already,
      "refreshed_present_exact_fixture_ids":refreshed,
      "quarantined_or_invalid_rows":quarantined,
      "quarantine_reason_counts":dict(sorted(quarantine_reason_counts.items())),
      "no_home_away_flag_semantics":"DOCUMENTED_FIELD_SEMANTICS; official FootyStats League Matches schema defines no_home_away=1 as no home/away distinction; the provider flag is not independently cross-checked against venue metadata; flagged rows remain quarantined from standard home/away-dependent markets",
      "future_status_semantics":"DOCUMENTED_ENUM_FAIL_CLOSED; only status=incomplete is eligible for a future fixture; status=complete conflicts with a future kickoff; suspended/canceled and missing or unknown statuses remain quarantined",
      "no_home_away_flag_by_league":sorted(no_home_away_by_league.values(),key=lambda x:(x["country"],x["competition"])),
      "unsupported_archive_rows_not_staged":unsupported_rows,
      "unsupported_selected_league_count":len(unsupported_labels),
      "unsupported_selected_leagues":unsupported_labels,
      "historical_rows_not_staged":historical,"future_rows_beyond_7d_not_staged":beyond,
      "candidate_trace_rows":len(trace_rows),
      "candidate_trace_outcome_counts":dict(sorted(trace_outcome_counts.items())),
      "candidate_trace_file":trace_path.name,
      "team_id_conflicts":conflicts,"production_writes":0,"model_logic_changed":False,
      "prediction_generated":False,"production_eligible":False,"betting_eligible":False,
      "guard":"Trace is sanitized row-level evidence only; provider-native IDs are preserved, canonical joins and official settlement truth remain unverified."
    }
    args.out_qa.parent.mkdir(parents=True,exist_ok=True)
    args.out_qa.write_text(json.dumps(qa,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(qa,indent=2,sort_keys=True))
if __name__=="__main__": main()
