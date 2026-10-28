#!/usr/bin/env python3
"""Create a fail-closed, report-only current-fixture view from the saved snapshot.

Requires exact provider season, fixture ID, and ordered home/away team IDs.
Does not generate predictions or change model probabilities.
"""
import argparse
import csv
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

FINISHED = {"complete", "completed", "finished", "ft", "full time", "full-time", "ended", "played"}
BAD_STATUS_PARTS = ("suspend", "postpon", "cancel", "abandon", "void", "delay")
MAX_SNAPSHOT_AGE = timedelta(hours=24)

def text(v):
    return "" if v is None else str(v).strip()

def parse_utc(v):
    if not v:
        return None
    try:
        d = datetime.fromisoformat(str(v).replace("Z", "+00:00"))
        return d.astimezone(timezone.utc) if d.tzinfo else None
    except (ValueError, TypeError):
        return None

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--snapshot", required=True, type=Path)
    p.add_argument("--runtime-report", required=True, type=Path)
    p.add_argument("--out-dir", required=True, type=Path)
    p.add_argument("--as-of-utc", help="Fixed ISO-8601 audit time for repeatable tests")
    a = p.parse_args()
    now = parse_utc(a.as_of_utc) if a.as_of_utc else datetime.now(timezone.utc)
    if now is None:
        raise SystemExit("FAIL: --as-of-utc must include a timezone")
    snapshot_bytes = a.snapshot.read_bytes()
    snapshot_sha256 = hashlib.sha256(snapshot_bytes).hexdigest()
    try:
        snap = json.loads(snapshot_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FAIL: snapshot JSON is invalid: {exc}")
    retrieved = parse_utc(snap.get("retrieved_utc"))
    if retrieved is None:
        raise SystemExit("FAIL: snapshot retrieval timestamp must be valid timezone-aware ISO-8601")
    snapshot_age_seconds = int((now - retrieved).total_seconds())
    if snapshot_age_seconds < 0:
        raise SystemExit("FAIL: snapshot retrieval timestamp is in the future relative to report as-of time")
    if retrieved < now - MAX_SNAPSHOT_AGE:
        raise SystemExit("FAIL: snapshot is older than the 24-hour current-report freshness limit")
    seasons = snap.get("per_season", [])
    fixture_rows = snap.get("fixture_rows", [])
    if not isinstance(seasons, list) or not isinstance(fixture_rows, list):
        raise SystemExit("FAIL: snapshot per_season and fixture_rows must be lists")
    season_ids = {text(x.get("selected_season_id")) for x in seasons}
    if len(seasons) != 50 or len(season_ids) != 50 or "" in season_ids:
        raise SystemExit("FAIL: snapshot must contain exactly 50 unique nonblank selected season IDs")
    with a.runtime_report.open(encoding="utf-8-sig", newline="") as h:
        runtime = list(csv.DictReader(h))
    required = {"provider_season_id", "fixture_id", "home_team_provider_id", "away_team_provider_id"}
    if not runtime or not required.issubset(runtime[0]):
        raise SystemExit("FAIL: runtime report missing required exact identity columns")
    runtime_by_key = {}
    duplicate_runtime_keys = 0
    for r in runtime:
        k = (text(r.get("provider_season_id")), text(r.get("fixture_id")))
        if not all(k):
            continue
        if k in runtime_by_key:
            duplicate_runtime_keys += 1
        else:
            runtime_by_key[k] = r
    season_meta = {text(x.get("selected_season_id")): x for x in seasons}
    seen = set()
    out_rows = []
    reason_counts = {}
    total_valid_source_rows = 0
    now_end = now + timedelta(days=7)
    for f in fixture_rows:
        season, fid = text(f.get("selected_season_id")), text(f.get("id"))
        if not season or not fid or season not in season_ids:
            reason = "QUARANTINE_INVALID_SOURCE_IDENTITY"
        elif (season, fid) in seen:
            reason = "QUARANTINE_DUPLICATE_SOURCE_IDENTITY"
        else:
            seen.add((season, fid))
            ko = parse_utc(f.get("kickoff_utc"))
            status_raw = text(f.get("status"))
            status = status_raw.lower()
            flag_raw = text(f.get("no_home_away")).lower()
            if flag_raw in {"1", "1.0", "true", "yes"}:
                reason = "QUARANTINE_NO_HOME_AWAY_TRUE"
            elif flag_raw not in {"0", "0.0", "false", "no"}:
                reason = "QUARANTINE_NO_HOME_AWAY_UNKNOWN"
            elif not status:
                reason = "QUARANTINE_MISSING_STATUS"
            elif any(part in status for part in BAD_STATUS_PARTS):
                reason = "QUARANTINE_NONSTANDARD_STATUS"
            elif ko is None:
                reason = "QUARANTINE_INVALID_KICKOFF"
            elif ko <= now and status not in FINISHED:
                reason = "QUARANTINE_NONFUTURE_UNSETTLED"
            elif ko <= now:
                reason = "NOT_FUTURE_FIXTURE"
            elif ko > now_end:
                reason = "OUTSIDE_7_DAY_REPORT_WINDOW"
            else:
                reason = "CANDIDATE_FOR_EXACT_JOIN"
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
        if reason != "CANDIDATE_FOR_EXACT_JOIN":
            continue
        total_valid_source_rows += 1
        r = runtime_by_key.get((season, fid))
        if r is None:
            reason_counts["BLOCKED_NO_EXACT_RUNTIME_ROW"] = reason_counts.get("BLOCKED_NO_EXACT_RUNTIME_ROW", 0) + 1
            continue
        if text(f.get("homeID")) != text(r.get("home_team_provider_id")) or text(f.get("awayID")) != text(r.get("away_team_provider_id")):
            reason_counts["BLOCKED_ORDERED_TEAM_ID_MISMATCH"] = reason_counts.get("BLOCKED_ORDERED_TEAM_ID_MISMATCH", 0) + 1
            continue
        row = dict(r)
        row["snapshot_country"] = text(season_meta[season].get("country"))
        row["snapshot_competition"] = text(season_meta[season].get("competition"))
        row["snapshot_kickoff_utc"] = text(f.get("kickoff_utc"))
        row["snapshot_home_name"] = text(f.get("home_name"))
        row["snapshot_away_name"] = text(f.get("away_name"))
        row["snapshot_status"] = text(f.get("status"))
        row["snapshot_no_home_away"] = text(f.get("no_home_away"))
        row["snapshot_exact_join_status"] = "EXACT_SEASON_FIXTURE_AND_ORDERED_TEAM_IDS_MATCH"
        row["snapshot_retrieved_utc"] = retrieved.isoformat()
        row["snapshot_age_seconds"] = snapshot_age_seconds
        row["snapshot_file_sha256"] = snapshot_sha256
        row["snapshot_provenance_status"] = "PASS_FRESH_TIMEZONE_AWARE"
        row["production_eligible"] = "NO"
        row["betting_eligible"] = "NO"
        out_rows.append(row)
        reason_counts["PASS_SAFE_EXACT_JOIN"] = reason_counts.get("PASS_SAFE_EXACT_JOIN", 0) + 1
    a.out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = a.out_dir / "oracle_selected50_safe_current_fixture_report.csv"
    fields = list(dict.fromkeys([k for row in out_rows for k in row]))
    if not fields:
        fields = ["provider_season_id", "fixture_id", "snapshot_exact_join_status", "production_eligible", "betting_eligible"]
    with csv_path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)
    qa = {
        "status": "PASS_REPORT_ONLY_WITH_BLOCKERS" if any(k.startswith("BLOCKED_") or k.startswith("QUARANTINE_") for k in reason_counts) else "PASS_REPORT_ONLY",
        "generated_utc": now.isoformat(),
        "snapshot_retrieved_utc": retrieved.isoformat(),
        "snapshot_age_seconds": snapshot_age_seconds,
        "snapshot_file_sha256": snapshot_sha256,
        "snapshot_provenance_status": "PASS_FRESH_TIMEZONE_AWARE",
        "selected_seasons": len(seasons),
        "snapshot_fixture_rows": len(fixture_rows),
        "runtime_report_rows": len(runtime),
        "duplicate_runtime_exact_keys": duplicate_runtime_keys,
        "source_candidates_in_7_day_window": total_valid_source_rows,
        "safe_exact_join_rows": len(out_rows),
        "source_candidates_blocked_by_missing_runtime_or_team_identity": total_valid_source_rows - len(out_rows),
        "reason_counts": dict(sorted(reason_counts.items())),
        "probability_policy": "Existing runtime fields copied unchanged; no prediction, recalibration, or model-logic change.",
        "production_eligible": False,
        "betting_eligible": False,
        "release_status": "NOT_APPROVED"
    }
    (a.out_dir / "oracle_selected50_safe_current_fixture_report_qa.json").write_text(json.dumps(qa, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(qa, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
