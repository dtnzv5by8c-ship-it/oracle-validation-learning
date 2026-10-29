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
    p.add_argument("--report-horizon-days", type=int, default=7, help="Snapshot assessment horizon (1-14 days); does not extend runtime generation")
    p.add_argument("--runtime-horizon-days", type=int, default=7, help="Declared runtime generation horizon (currently capped at 7 days)")
    p.add_argument("--runtime-started-utc", help="Timezone-aware start of the runtime whose rows are being joined; required for report horizons over 7 days")
    p.add_argument("--minimum-lead-minutes", type=int, default=15, help="Minimum future lead before a fixture can be reported")
    a = p.parse_args()
    now = parse_utc(a.as_of_utc) if a.as_of_utc else datetime.now(timezone.utc)
    if now is None:
        raise SystemExit("FAIL: --as-of-utc must include a timezone")
    report_horizon_days = a.report_horizon_days
    runtime_horizon_days = a.runtime_horizon_days
    minimum_lead_minutes = a.minimum_lead_minutes
    if not 1 <= report_horizon_days <= 14:
        raise SystemExit("FAIL: --report-horizon-days must be between 1 and 14, matching the saved snapshot's declared future coverage")
    if not 1 <= runtime_horizon_days <= 7 or runtime_horizon_days > report_horizon_days:
        raise SystemExit("FAIL: --runtime-horizon-days must be between 1 and 7 and no greater than the report horizon")
    if minimum_lead_minutes < 0:
        raise SystemExit("FAIL: --minimum-lead-minutes must be non-negative")
    if report_horizon_days > 7 and not a.runtime_started_utc:
        raise SystemExit("FAIL: --runtime-started-utc is required when assessing a report horizon beyond seven days")
    runtime_started = parse_utc(a.runtime_started_utc) if a.runtime_started_utc else now
    if runtime_started is None:
        raise SystemExit("FAIL: --runtime-started-utc must include a timezone")
    if runtime_started > now:
        raise SystemExit("FAIL: runtime start cannot be later than report as-of time")
    runtime_end = runtime_started + timedelta(days=runtime_horizon_days)
    report_end = now + timedelta(days=report_horizon_days)
    minimum_lead_cutoff = now + timedelta(minutes=minimum_lead_minutes)
    snapshot_bytes = a.snapshot.read_bytes()
    snapshot_sha256 = hashlib.sha256(snapshot_bytes).hexdigest()
    try:
        snap = json.loads(snapshot_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FAIL: snapshot JSON is invalid: {exc}")
    retrieved = parse_utc(snap.get("retrieved_utc"))
    if retrieved is None:
        raise SystemExit("FAIL: snapshot retrieval timestamp must be valid timezone-aware ISO-8601")
    if report_horizon_days > runtime_horizon_days and retrieved > runtime_started:
        raise SystemExit(
            "FAIL: snapshot retrieval timestamp is later than runtime start; "
            "a post-runtime snapshot cannot establish out-of-window versus missing-join coverage"
        )
    snapshot_window_start = parse_utc(snap.get("window_start_utc"))
    snapshot_window_end = parse_utc(snap.get("window_end_utc"))
    if report_horizon_days > runtime_horizon_days:
        if snapshot_window_start is None:
            raise SystemExit(
                "FAIL: snapshot window_start_utc must be valid timezone-aware ISO-8601 "
                "when assessing beyond the runtime generation horizon"
            )
        if snapshot_window_start > runtime_started:
            raise SystemExit(
                "FAIL: snapshot window_start_utc is later than runtime start; "
                "the snapshot cannot establish complete runtime-window coverage"
            )
        if snapshot_window_end is None:
            raise SystemExit(
                "FAIL: snapshot window_end_utc must be valid timezone-aware ISO-8601 "
                "when assessing beyond the runtime generation horizon"
            )
        if snapshot_window_end <= retrieved:
            raise SystemExit("FAIL: snapshot window_end_utc must be later than snapshot retrieval")
        if report_end > snapshot_window_end:
            shortfall_seconds = int((report_end - snapshot_window_end).total_seconds())
            raise SystemExit(
                f"FAIL: requested report horizon extends {shortfall_seconds} seconds beyond "
                "declared snapshot window_end_utc; cannot classify full horizon safely"
            )
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
    combo_probability_columns = [
        name for name in runtime[0]
        if "combo" in name.casefold()
        and ("probability" in name.casefold() or "prob" in name.casefold())
        and not any(token in name.casefold() for token in ("status", "reason", "mask", "blocked", "eligibility"))
    ]
    visible_combo_columns = sorted({
        name for row in runtime for name in combo_probability_columns
        if text(row.get(name))
    })
    if visible_combo_columns:
        raise SystemExit(
            "FAIL: Combo probability values must remain masked until canonical joins "
            "and official settlement truth are verified; nonblank values found in: "
            + ", ".join(visible_combo_columns)
        )
    combo_masking_status = (
        "PASS_ALL_COMBO_PROBABILITY_VALUES_BLANK"
        if combo_probability_columns else "PASS_NO_COMBO_PROBABILITY_COLUMNS_PRESENT"
    )
    runtime_by_key = {}
    duplicate_runtime_key_occurrences = 0
    duplicate_runtime_key_set = set()
    for r in runtime:
        k = (text(r.get("provider_season_id")), text(r.get("fixture_id")))
        if not all(k):
            continue
        if k in runtime_by_key:
            duplicate_runtime_key_occurrences += 1
            duplicate_runtime_key_set.add(k)
        else:
            runtime_by_key[k] = r
    season_meta = {text(x.get("selected_season_id")): x for x in seasons}
    # Reverse coverage index: runtime rows absent from the snapshot must not disappear
    # silently, and must not be mislabeled as ordinary out-of-window fixtures.
    snapshot_rows_by_key = {}
    snapshot_seasons_by_fixture_id = {}
    for source_row in fixture_rows:
        if not isinstance(source_row, dict):
            continue
        source_season = text(source_row.get("selected_season_id"))
        source_fixture = text(source_row.get("id"))
        if source_season and source_fixture:
            snapshot_rows_by_key.setdefault((source_season, source_fixture), []).append(source_row)
            snapshot_seasons_by_fixture_id.setdefault(source_fixture, set()).add(source_season)
    seen = set()
    out_rows = []
    exclusion_rows = []
    reason_counts = {}
    total_valid_source_rows = 0
    snapshot_window_covers_runtime_start = bool(
        snapshot_window_start and snapshot_window_start <= runtime_started
    )
    snapshot_window_covers_requested_report_horizon = bool(
        snapshot_window_covers_runtime_start
        and snapshot_window_end
        and report_end <= snapshot_window_end
    )
    reporting_horizon_coverage_status = (
        "PASS_DECLARED_SNAPSHOT_WINDOW_COVERS_REQUESTED_HORIZON"
        if report_horizon_days > runtime_horizon_days and snapshot_window_covers_requested_report_horizon
        else "NOT_REQUIRED_NO_HORIZON_EXPANSION"
        if report_horizon_days <= runtime_horizon_days
        else "NOT_VERIFIED"
    )
    snapshot_runtime_chronology_gate = (
        "PASS_SNAPSHOT_PRECEDES_RUNTIME_START"
        if retrieved <= runtime_started
        else "NOT_REQUIRED_NO_HORIZON_EXPANSION"
    )

    def record_exclusion(f, season, fid, reason, runtime_row=None):
        meta = season_meta.get(season, {})
        runtime_row = runtime_row or {}
        feature_status = text(runtime_row.get("feature_support_status"))
        prediction_status = text(runtime_row.get("prediction_status"))
        if reason.startswith("QUARANTINE_"):
            market_gate, feature_gate = "BLOCKED_SOURCE_QUARANTINE", "NOT_EVALUATED_SOURCE_QUARANTINE"
        elif reason == "OUTSIDE_RUNTIME_GENERATION_WINDOW_NOT_MISSING_JOIN":
            market_gate, feature_gate = "NOT_EVALUATED_OUTSIDE_RUNTIME_GENERATION_WINDOW", "NOT_EVALUATED_NO_RUNTIME_GENERATION"
        elif reason == "OUTSIDE_MINIMUM_LEAD_WINDOW_NOT_MISSING_JOIN":
            market_gate, feature_gate = "NOT_EVALUATED_MINIMUM_LEAD_WINDOW", "NOT_EVALUATED_MINIMUM_LEAD_WINDOW"
        elif reason.startswith("OUTSIDE_"):
            market_gate, feature_gate = "NOT_EVALUATED_OUTSIDE_REPORTING_WINDOW", "NOT_EVALUATED_OUTSIDE_REPORTING_WINDOW"
        elif reason == "BLOCKED_NO_EXACT_RUNTIME_ROW":
            market_gate, feature_gate = "BLOCKED_NO_EXACT_RUNTIME_ROW", "NOT_EVALUATED_NO_RUNTIME_ROW"
        elif reason == "BLOCKED_ORDERED_TEAM_ID_MISMATCH":
            market_gate, feature_gate = "BLOCKED_ORDERED_TEAM_ID_MISMATCH", "NOT_EVALUATED_IDENTITY_BLOCKED"
        elif reason == "BLOCKED_KICKOFF_MISMATCH":
            market_gate, feature_gate = "BLOCKED_KICKOFF_MISMATCH", "NOT_EVALUATED_TEMPORAL_IDENTITY_BLOCKED"
        elif reason == "BLOCKED_DUPLICATE_RUNTIME_EXACT_KEY":
            market_gate, feature_gate = "BLOCKED_DUPLICATE_RUNTIME_EXACT_KEY", "NOT_EVALUATED_AMBIGUOUS_RUNTIME_KEY"
        elif reason == "NOT_FUTURE_FIXTURE":
            market_gate, feature_gate = "NOT_EVALUATED_NOT_FUTURE", "NOT_EVALUATED_NOT_FUTURE"
        else:
            market_gate, feature_gate = "BLOCKED_SOURCE_OR_IDENTITY_REVIEW", feature_status or "NOT_VERIFIED"
        exclusion_rows.append({
            "provider_season_id": season, "fixture_id": fid,
            "snapshot_country": text(meta.get("country")),
            "snapshot_competition": text(meta.get("competition")),
            "snapshot_kickoff_utc": text(f.get("kickoff_utc")),
            "runtime_kickoff_utc": text(runtime_row.get("date_utc")),
            "snapshot_status": text(f.get("status")),
            "snapshot_no_home_away": text(f.get("no_home_away")),
            "snapshot_retrieved_utc": retrieved.isoformat(),
            "snapshot_age_seconds": snapshot_age_seconds,
            "snapshot_file_sha256": snapshot_sha256,
            "snapshot_provenance_status": "PASS_FRESH_TIMEZONE_AWARE",
            "snapshot_window_start_utc": snapshot_window_start.isoformat() if snapshot_window_start else "",
            "snapshot_window_end_utc": snapshot_window_end.isoformat() if snapshot_window_end else "",
            "runtime_started_utc": runtime_started.isoformat(),
            "runtime_generation_end_utc": runtime_end.isoformat(),
            "requested_report_end_utc": report_end.isoformat(),
            "snapshot_runtime_chronology_gate": snapshot_runtime_chronology_gate,
            "snapshot_window_covers_runtime_start": snapshot_window_covers_runtime_start,
            "snapshot_window_covers_requested_report_horizon": snapshot_window_covers_requested_report_horizon,
            "reporting_horizon_coverage_status": reporting_horizon_coverage_status,
            "home_team_provider_id": text(f.get("homeID")),
            "away_team_provider_id": text(f.get("awayID")),
            "classification": reason,
            "report_horizon_days": report_horizon_days,
            "runtime_generation_horizon_days": runtime_horizon_days,
            "runtime_feature_support_status": feature_status,
            "runtime_prediction_status": prediction_status,
            "market_gate_status": market_gate, "feature_gate_status": feature_gate,
            "canonical_fixture_join_status": "NOT_VERIFIED",
            "canonical_team_join_status": "NOT_VERIFIED",
            "official_settlement_truth_status": "NOT_VERIFIED",
            "combo_masked": "YES", "combo_probability_emitted": 0,
            "prediction_created": 0, "production_eligible": "NO", "betting_eligible": "NO",
        })

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
            elif ko > now and status in FINISHED:
                # A completed/played status conflicts with a future kickoff.
                # Quarantine before horizon classification so it cannot be
                # mislabeled as an ordinary out-of-window fixture.
                reason = "QUARANTINE_STATUS_INCONSISTENT_WITH_FUTURE_KICKOFF"
            elif ko > now and status != "incomplete":
                # Match the FootyStats overlay's documented future-status contract:
                # only "incomplete" is eligible; unknown values fail closed before
                # they can be counted as clean out-of-runtime-window candidates.
                reason = "QUARANTINE_UNKNOWN_OR_UNSUPPORTED_FUTURE_STATUS"
            elif ko <= now and status not in FINISHED:
                reason = "QUARANTINE_NONFUTURE_UNSETTLED"
            elif ko <= now:
                reason = "NOT_FUTURE_FIXTURE"
            elif not text(f.get("homeID")) or not text(f.get("awayID")):
                reason = "QUARANTINE_MISSING_ORDERED_TEAM_IDS"
            elif ko <= minimum_lead_cutoff:
                reason = "OUTSIDE_MINIMUM_LEAD_WINDOW_NOT_MISSING_JOIN"
            elif ko > report_end:
                reason = f"OUTSIDE_{report_horizon_days}_DAY_REPORT_WINDOW"
            elif ko > runtime_end:
                reason = "OUTSIDE_RUNTIME_GENERATION_WINDOW_NOT_MISSING_JOIN"
            else:
                reason = "CANDIDATE_FOR_EXACT_JOIN"
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
        if reason != "CANDIDATE_FOR_EXACT_JOIN":
            record_exclusion(f, season, fid, reason)
            continue
        total_valid_source_rows += 1
        runtime_key = (season, fid)
        if runtime_key in duplicate_runtime_key_set:
            reason_counts["BLOCKED_DUPLICATE_RUNTIME_EXACT_KEY"] = reason_counts.get("BLOCKED_DUPLICATE_RUNTIME_EXACT_KEY", 0) + 1
            record_exclusion(f, season, fid, "BLOCKED_DUPLICATE_RUNTIME_EXACT_KEY", runtime_by_key.get(runtime_key))
            continue
        r = runtime_by_key.get(runtime_key)
        if r is None:
            reason_counts["BLOCKED_NO_EXACT_RUNTIME_ROW"] = reason_counts.get("BLOCKED_NO_EXACT_RUNTIME_ROW", 0) + 1
            record_exclusion(f, season, fid, "BLOCKED_NO_EXACT_RUNTIME_ROW")
            continue
        if text(f.get("homeID")) != text(r.get("home_team_provider_id")) or text(f.get("awayID")) != text(r.get("away_team_provider_id")):
            reason_counts["BLOCKED_ORDERED_TEAM_ID_MISMATCH"] = reason_counts.get("BLOCKED_ORDERED_TEAM_ID_MISMATCH", 0) + 1
            record_exclusion(f, season, fid, "BLOCKED_ORDERED_TEAM_ID_MISMATCH", r)
            continue
        snapshot_kickoff = parse_utc(f.get("kickoff_utc"))
        runtime_kickoff = parse_utc(r.get("date_utc"))
        if snapshot_kickoff is None or runtime_kickoff is None or snapshot_kickoff != runtime_kickoff:
            reason_counts["BLOCKED_KICKOFF_MISMATCH"] = reason_counts.get("BLOCKED_KICKOFF_MISMATCH", 0) + 1
            record_exclusion(f, season, fid, "BLOCKED_KICKOFF_MISMATCH", r)
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
        row["snapshot_window_start_utc"] = snapshot_window_start.isoformat() if snapshot_window_start else ""
        row["snapshot_window_end_utc"] = snapshot_window_end.isoformat() if snapshot_window_end else ""
        row["runtime_started_utc"] = runtime_started.isoformat()
        row["runtime_generation_end_utc"] = runtime_end.isoformat()
        row["requested_report_end_utc"] = report_end.isoformat()
        row["snapshot_runtime_chronology_gate"] = snapshot_runtime_chronology_gate
        row["snapshot_window_covers_runtime_start"] = snapshot_window_covers_runtime_start
        row["snapshot_window_covers_requested_report_horizon"] = snapshot_window_covers_requested_report_horizon
        row["reporting_horizon_coverage_status"] = reporting_horizon_coverage_status
        row["report_horizon_days"] = report_horizon_days
        row["runtime_generation_horizon_days"] = runtime_horizon_days
        row["market_gate_status"] = ("BLOCKED_FEATURE_SUPPORT" if "BLOCKED_MISSING_REQUIRED_FEATURES" in text(r.get("feature_support_status")) or "BLOCKED" in text(r.get("prediction_status")) else "RAW_RESEARCH_ONLY_NOT_FOR_BETTING")
        row["canonical_fixture_join_status"] = "NOT_VERIFIED"
        row["canonical_team_join_status"] = "NOT_VERIFIED"
        row["official_settlement_truth_status"] = "NOT_VERIFIED"
        row["combo_masked"] = "YES"
        row["combo_probability_emitted"] = 0
        row["canonical_join_created"] = 0
        row["prediction_created"] = 0
        row["production_eligible"] = "NO"
        row["betting_eligible"] = "NO"
        out_rows.append(row)
        reason_counts["PASS_SAFE_EXACT_JOIN"] = reason_counts.get("PASS_SAFE_EXACT_JOIN", 0) + 1
    # Reverse audit of runtime rows that have no matching snapshot season/fixture key.
    # Source quarantines remain represented in the per-snapshot exclusion CSV above;
    # only rows absent from that source key are classified here.
    runtime_snapshot_gap_rows = []
    for runtime_row in runtime:
        runtime_season = text(runtime_row.get("provider_season_id"))
        runtime_fixture = text(runtime_row.get("fixture_id"))
        if not runtime_season or not runtime_fixture:
            classification = "BLOCKED_INVALID_RUNTIME_IDENTITY"
        elif (runtime_season, runtime_fixture) in snapshot_rows_by_key:
            continue
        else:
            runtime_kickoff = parse_utc(runtime_row.get("date_utc"))
            if runtime_kickoff is None:
                classification = "BLOCKED_RUNTIME_KICKOFF_INVALID"
            elif runtime_kickoff <= now:
                classification = "NOT_FUTURE_RUNTIME_ROW_NOT_SNAPSHOT_GAP"
            elif runtime_kickoff > report_end:
                classification = f"OUTSIDE_{report_horizon_days}_DAY_REPORT_WINDOW_NOT_SNAPSHOT_GAP"
            elif runtime_kickoff > runtime_end:
                classification = "OUTSIDE_RUNTIME_GENERATION_WINDOW_NOT_MISSING_SNAPSHOT_JOIN"
            elif runtime_fixture in snapshot_seasons_by_fixture_id:
                classification = "BLOCKED_SNAPSHOT_SEASON_ID_MISMATCH"
            else:
                classification = "BLOCKED_NO_SNAPSHOT_FIXTURE_ROW"
        if classification == "BLOCKED_NO_SNAPSHOT_FIXTURE_ROW":
            market_gate = "BLOCKED_NO_EXACT_SNAPSHOT_SOURCE"
            feature_gate = "NOT_EVALUATED_NO_SNAPSHOT_SOURCE"
        elif classification == "BLOCKED_SNAPSHOT_SEASON_ID_MISMATCH":
            market_gate = "BLOCKED_SNAPSHOT_SEASON_ID_MISMATCH"
            feature_gate = "NOT_EVALUATED_SNAPSHOT_IDENTITY_BLOCKED"
        elif classification.startswith("OUTSIDE_"):
            market_gate = "NOT_EVALUATED_OUTSIDE_REPORTING_OR_RUNTIME_WINDOW"
            feature_gate = "NOT_EVALUATED_OUTSIDE_REPORTING_OR_RUNTIME_WINDOW"
        elif classification == "NOT_FUTURE_RUNTIME_ROW_NOT_SNAPSHOT_GAP":
            market_gate = "NOT_EVALUATED_NOT_FUTURE"
            feature_gate = "NOT_EVALUATED_NOT_FUTURE"
        else:
            market_gate = "BLOCKED_RUNTIME_SOURCE_OR_IDENTITY_REVIEW"
            feature_gate = "NOT_EVALUATED_RUNTIME_SOURCE_OR_IDENTITY_REVIEW"
        runtime_snapshot_gap_rows.append({
            "provider_season_id": runtime_season,
            "fixture_id": runtime_fixture,
            "runtime_kickoff_utc": text(runtime_row.get("date_utc")),
            "runtime_home_team_provider_id": text(runtime_row.get("home_team_provider_id")),
            "runtime_away_team_provider_id": text(runtime_row.get("away_team_provider_id")),
            "runtime_prediction_status": text(runtime_row.get("prediction_status")),
            "runtime_feature_support_status": text(runtime_row.get("feature_support_status")),
            "classification": classification,
            "market_gate_status": market_gate,
            "feature_gate_status": feature_gate,
            "canonical_fixture_join_status": "NOT_VERIFIED",
            "canonical_team_join_status": "NOT_VERIFIED",
            "official_settlement_truth_status": "NOT_VERIFIED",
            "combo_masked": "YES",
            "combo_probability_emitted": 0,
            "prediction_created": 0,
            "production_eligible": "NO",
            "betting_eligible": "NO",
        })
    a.out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = a.out_dir / "oracle_selected50_safe_current_fixture_report.csv"
    fields = list(dict.fromkeys([k for row in out_rows for k in row]))
    if not fields:
        fields = ["provider_season_id", "fixture_id", "snapshot_exact_join_status", "production_eligible", "betting_eligible"]
    with csv_path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)
    exclusion_path = a.out_dir / "oracle_selected50_safe_current_fixture_exclusions.csv"
    exclusion_fields = [
        "provider_season_id", "fixture_id", "snapshot_country", "snapshot_competition",
        "snapshot_kickoff_utc", "runtime_kickoff_utc", "snapshot_status", "snapshot_no_home_away",
        "snapshot_retrieved_utc", "snapshot_age_seconds", "snapshot_file_sha256", "snapshot_provenance_status",
        "snapshot_window_start_utc", "snapshot_window_end_utc", "runtime_started_utc",
        "runtime_generation_end_utc", "requested_report_end_utc", "snapshot_runtime_chronology_gate",
        "snapshot_window_covers_runtime_start", "snapshot_window_covers_requested_report_horizon",
        "reporting_horizon_coverage_status", "home_team_provider_id", "away_team_provider_id", "classification",
        "report_horizon_days", "runtime_generation_horizon_days",
        "runtime_feature_support_status", "runtime_prediction_status",
        "market_gate_status", "feature_gate_status", "canonical_fixture_join_status",
        "canonical_team_join_status", "official_settlement_truth_status",
        "combo_masked", "combo_probability_emitted", "prediction_created",
        "production_eligible", "betting_eligible"
    ]
    with exclusion_path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=exclusion_fields)
        w.writeheader()
        w.writerows(exclusion_rows)
    runtime_gap_path = a.out_dir / "oracle_selected50_runtime_snapshot_coverage_gaps.csv"
    runtime_gap_fields = [
        "provider_season_id", "fixture_id", "runtime_kickoff_utc",
        "runtime_home_team_provider_id", "runtime_away_team_provider_id",
        "runtime_prediction_status", "runtime_feature_support_status", "classification",
        "market_gate_status", "feature_gate_status", "canonical_fixture_join_status",
        "canonical_team_join_status", "official_settlement_truth_status", "combo_masked",
        "combo_probability_emitted", "prediction_created", "production_eligible", "betting_eligible"
    ]
    with runtime_gap_path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=runtime_gap_fields)
        w.writeheader()
        w.writerows(runtime_snapshot_gap_rows)
    runtime_snapshot_missing_count = sum(
        row["classification"] == "BLOCKED_NO_SNAPSHOT_FIXTURE_ROW" for row in runtime_snapshot_gap_rows
    )
    runtime_snapshot_season_mismatch_count = sum(
        row["classification"] == "BLOCKED_SNAPSHOT_SEASON_ID_MISMATCH" for row in runtime_snapshot_gap_rows
    )
    runtime_snapshot_out_of_window_count = sum(
        row["classification"].startswith("OUTSIDE_") for row in runtime_snapshot_gap_rows
    )
    qa = {
        "status": "PASS_REPORT_ONLY_WITH_BLOCKERS" if report_horizon_days > runtime_horizon_days or any(k.startswith("BLOCKED_") or k.startswith("QUARANTINE_") for k in reason_counts) else "PASS_REPORT_ONLY",
        "generated_utc": now.isoformat(),
        "snapshot_retrieved_utc": retrieved.isoformat(),
        "snapshot_window_start_utc": snapshot_window_start.isoformat() if snapshot_window_start else None,
        "snapshot_window_end_utc": snapshot_window_end.isoformat() if snapshot_window_end else None,
        "requested_report_end_utc": report_end.isoformat(),
        "snapshot_window_covers_runtime_start": snapshot_window_covers_runtime_start,
        "snapshot_window_covers_requested_report_horizon": snapshot_window_covers_requested_report_horizon,
        "reporting_horizon_coverage_status": reporting_horizon_coverage_status,
        "snapshot_age_seconds": snapshot_age_seconds,
        "snapshot_file_sha256": snapshot_sha256,
        "snapshot_provenance_status": "PASS_FRESH_TIMEZONE_AWARE",
        "snapshot_retrieved_at_or_before_runtime_start": retrieved <= runtime_started,
        "snapshot_runtime_chronology_gate": snapshot_runtime_chronology_gate,
        "selected_seasons": len(seasons),
        "snapshot_fixture_rows": len(fixture_rows),
        "runtime_report_rows": len(runtime),
        "runtime_rows_without_exact_snapshot_key": len(runtime_snapshot_gap_rows),
        "runtime_rows_missing_snapshot_fixture_row": runtime_snapshot_missing_count,
        "runtime_rows_with_snapshot_season_mismatch": runtime_snapshot_season_mismatch_count,
        "runtime_rows_outside_window_not_snapshot_gaps": runtime_snapshot_out_of_window_count,
        "runtime_snapshot_coverage_gap_report": runtime_gap_path.name,
        "runtime_snapshot_coverage_gap_rows": len(runtime_snapshot_gap_rows),
        "duplicate_runtime_exact_keys": duplicate_runtime_key_occurrences,
        "ambiguous_runtime_exact_key_count": len(duplicate_runtime_key_set),
        "combo_probability_columns_checked": combo_probability_columns,
        "combo_probability_nonblank_cells": 0,
        "combo_masking_status": combo_masking_status,
        "source_candidates_blocked_by_duplicate_runtime_exact_key": reason_counts.get("BLOCKED_DUPLICATE_RUNTIME_EXACT_KEY", 0),
        "report_horizon_days": report_horizon_days,
        "runtime_generation_horizon_days": runtime_horizon_days,
        "runtime_started_utc": runtime_started.isoformat(),
        "minimum_lead_minutes": minimum_lead_minutes,
        "source_candidates_in_7_day_window": total_valid_source_rows,
        "source_candidates_within_runtime_generation_window": total_valid_source_rows,
        "source_candidates_in_report_horizon": total_valid_source_rows + reason_counts.get("OUTSIDE_RUNTIME_GENERATION_WINDOW_NOT_MISSING_JOIN", 0),
        "source_candidates_outside_runtime_window_not_missing_join": reason_counts.get("OUTSIDE_RUNTIME_GENERATION_WINDOW_NOT_MISSING_JOIN", 0),
        "source_candidates_outside_minimum_lead_window_not_missing_join": reason_counts.get("OUTSIDE_MINIMUM_LEAD_WINDOW_NOT_MISSING_JOIN", 0),
        "source_candidates_outside_report_horizon": reason_counts.get(f"OUTSIDE_{report_horizon_days}_DAY_REPORT_WINDOW", 0),
        "per_fixture_exclusion_report": exclusion_path.name,
        "per_fixture_exclusion_rows": len(exclusion_rows),
        "per_fixture_quarantine_preserved": True,
        "market_gates_preserved": True,
        "canonical_joins_created": 0,
        "official_settlement_truth_verified": 0,
        "expanded_prediction_report_approved": False,
        "reporting_window_expansion_status": "ASSESSMENT_ONLY_RUNTIME_REMAINS_AT_DECLARED_HORIZON" if report_horizon_days > runtime_horizon_days else "REPORT_WITHIN_RUNTIME_HORIZON_ONLY",
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
