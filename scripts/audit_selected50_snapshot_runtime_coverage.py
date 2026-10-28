#!/usr/bin/env python3
"""Offline exact-ID comparison of a saved FootyStats snapshot and runtime report."""
from __future__ import annotations
import argparse, csv, datetime as dt, json, math
from pathlib import Path

FINISHED = {"complete", "completed", "finished", "full time", "full-time", "ft", "ended", "played"}
CANCELLED = {"cancelled", "canceled", "abandoned", "postponed", "suspended", "void"}
REQUIRED_RUNTIME = {"fixture_id", "selected_id", "date_utc", "COMBO_HOME_probability_pct", "COMBO_AWAY_probability_pct"}


def aware_utc(value, field):
    raw = str(value or "").strip()
    if not raw:
        raise ValueError(f"{field} is required")
    try:
        parsed = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO timestamp with an explicit timezone") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include an explicit timezone")
    return parsed.astimezone(dt.timezone.utc)


def score(value):
    """Parse a score only when it is a finite, non-negative integer.

    Booleans, fractional values, negatives, NaN and infinity are not valid
    settlement scores and must never be used to exclude a row as completed.
    """
    if isinstance(value, bool) or value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    try:
        n = float(raw)
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(n) or n < 0 or not n.is_integer():
        return None
    return int(n)


def no_home_away(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        if float(value) == 1.0:
            return True
        if float(value) == 0.0:
            return False
        return None
    raw = str(value or "").strip().casefold()
    if raw in {"1", "1.0", "true", "yes"}:
        return True
    if raw in {"0", "0.0", "false", "no"}:
        return False
    return None


def runtime_finished(row):
    status = str(row.get("status") or row.get("game_status") or "").strip().casefold()
    h = score(row.get("homeGoalCount", row.get("home_goals", row.get("home_score"))))
    a = score(row.get("awayGoalCount", row.get("away_goals", row.get("away_score"))))
    return status in FINISHED and h is not None and a is not None


def key(season_id, fixture_id):
    return str(season_id or "").strip(), str(fixture_id or "").strip()


def audit(snapshot, runtime_rows, runtime_started_utc, minimum_lead_minutes=15, horizon_days=7,
          snapshot_artifact_id="", snapshot_artifact_sha256="", runtime_run_id="",
          runtime_artifact_id="", runtime_artifact_sha256=""):
    start = aware_utc(runtime_started_utc, "runtime_started_utc")
    retrieved = aware_utc(snapshot.get("retrieved_utc"), "snapshot.retrieved_utc")
    if retrieved > start:
        raise ValueError("snapshot retrieval is later than runtime start; cannot claim it was available to that run")
    fixture_rows = snapshot.get("fixture_rows")
    if not isinstance(fixture_rows, list) or not fixture_rows:
        raise ValueError("snapshot.fixture_rows must be a non-empty list")
    if snapshot.get("api_key_persisted") is True or snapshot.get("raw_provider_payload_persisted") is True:
        raise ValueError("snapshot fails sanitized-artifact guard")
    missing_runtime = sorted(REQUIRED_RUNTIME - set(runtime_rows[0] if runtime_rows else {}))
    if not runtime_rows or missing_runtime:
        raise ValueError("runtime report is empty or missing required columns: " + ", ".join(missing_runtime))
    if any(str(r.get(c) or "").strip() for r in runtime_rows
           for c in ("COMBO_HOME_probability_pct", "COMBO_AWAY_probability_pct")):
        raise ValueError("Combo probability mask is violated; refusing coverage audit")

    lower = start + dt.timedelta(minutes=minimum_lead_minutes)
    upper = start + dt.timedelta(days=horizon_days)
    snapshot_candidates = {}
    quarantined_invalid_scores = {}
    for r in fixture_rows:
        if not isinstance(r, dict):
            continue
        sid, fid = key(r.get("selected_season_id"), r.get("id"))
        if not sid or not fid:
            continue
        kickoff = aware_utc(r.get("kickoff_utc"), f"snapshot fixture {fid} kickoff_utc")
        status = str(r.get("status") or r.get("game_status") or "").strip().casefold()
        if not (kickoff > lower and kickoff <= upper) or status in CANCELLED:
            continue
        k = (sid, fid)
        if status in FINISHED:
            if runtime_finished(r):
                continue
            if k in snapshot_candidates or k in quarantined_invalid_scores:
                raise ValueError(f"duplicate snapshot fixture key: {k}")
            quarantined_invalid_scores[k] = r
            continue
        if k in snapshot_candidates or k in quarantined_invalid_scores:
            raise ValueError(f"duplicate snapshot fixture key: {k}")
        snapshot_candidates[k] = r

    runtime_candidates = {}
    for r in runtime_rows:
        k = key(r.get("selected_id"), r.get("fixture_id"))
        if not all(k):
            raise ValueError("runtime report contains blank selected_id or fixture_id")
        if k in runtime_candidates:
            raise ValueError(f"duplicate runtime fixture key: {k}")
        kickoff = aware_utc(r.get("date_utc"), f"runtime fixture {k[1]} date_utc")
        if not (kickoff > lower and kickoff <= upper):
            raise ValueError(f"runtime fixture {k} is outside the declared runtime window")
        runtime_candidates[k] = r

    snapshot_keys, runtime_keys = set(snapshot_candidates), set(runtime_candidates)
    common, snapshot_only, runtime_only = snapshot_keys & runtime_keys, snapshot_keys - runtime_keys, runtime_keys - snapshot_keys
    diffs = []
    for k in sorted(snapshot_only):
        r = snapshot_candidates[k]
        flag = no_home_away(r.get("no_home_away"))
        if flag is True:
            classification = "SNAPSHOT_ONLY_NO_HOME_AWAY_FLAGGED_REVIEW"
        elif flag is False:
            classification = "SNAPSHOT_ONLY_FLAG_FALSE_NOT_IN_RUNTIME_OUTPUT"
        else:
            classification = "SNAPSHOT_ONLY_NO_HOME_AWAY_FLAG_UNKNOWN_REVIEW"
        diffs.append({
            "selected_season_id": k[0], "fixture_id": k[1], "side": "SNAPSHOT_ONLY",
            "classification": classification, "no_home_away": "" if flag is None else int(flag),
            "kickoff_utc": str(r.get("kickoff_utc") or ""),
            "country": str(r.get("manifest_country") or ""), "league": str(r.get("manifest_competition") or ""),
            "home_team": str(r.get("home_name") or ""), "home_team_provider_id": str(r.get("homeID") or ""),
            "away_team": str(r.get("away_name") or ""), "away_team_provider_id": str(r.get("awayID") or ""),
            "snapshot_status": str(r.get("status") or ""), "runtime_status": "",
            "canonical_join_created": 0, "prediction_created": 0, "production_eligible": "NO",
        })
    for k in sorted(runtime_only):
        r = runtime_candidates[k]
        diffs.append({
            "selected_season_id": k[0], "fixture_id": k[1], "side": "RUNTIME_ONLY",
            "classification": "RUNTIME_ONLY_NOT_IN_SNAPSHOT_REVIEW",
            "no_home_away": "", "kickoff_utc": str(r.get("date_utc") or ""),
            "country": str(r.get("country") or ""), "league": str(r.get("league") or ""),
            "home_team": str(r.get("home_team") or ""), "home_team_provider_id": str(r.get("home_team_provider_id") or ""),
            "away_team": str(r.get("away_team") or ""), "away_team_provider_id": str(r.get("away_team_provider_id") or ""),
            "snapshot_status": "", "runtime_status": str(r.get("prediction_status") or r.get("feature_support_status") or ""),
            "canonical_join_created": 0, "prediction_created": 0, "production_eligible": "NO",
        })

    for k, r in sorted(quarantined_invalid_scores.items()):
        flag = no_home_away(r.get("no_home_away"))
        diffs.append({
            "selected_season_id": k[0], "fixture_id": k[1], "side": "SNAPSHOT_QUARANTINED",
            "classification": "QUARANTINE_FINISHED_STATUS_INVALID_SCORE",
            "no_home_away": "" if flag is None else int(flag),
            "kickoff_utc": str(r.get("kickoff_utc") or ""),
            "country": str(r.get("manifest_country") or ""), "league": str(r.get("manifest_competition") or ""),
            "home_team": str(r.get("home_name") or ""), "home_team_provider_id": str(r.get("homeID") or ""),
            "away_team": str(r.get("away_name") or ""), "away_team_provider_id": str(r.get("awayID") or ""),
            "snapshot_status": str(r.get("status") or r.get("game_status") or ""), "runtime_status": "",
            "canonical_join_created": 0, "prediction_created": 0, "production_eligible": "NO",
        })

    valid_flag_false = [k for k in snapshot_only if no_home_away(snapshot_candidates[k].get("no_home_away")) is False]
    flagged = [k for k in snapshot_only if no_home_away(snapshot_candidates[k].get("no_home_away")) is True]
    unknown_flag = [k for k in snapshot_only if no_home_away(snapshot_candidates[k].get("no_home_away")) is None]
    summary = {
        "status": "PASS_RESEARCH_ONLY_SNAPSHOT_RUNTIME_COVERAGE_AUDIT",
        "runtime_started_utc": start.isoformat(), "snapshot_retrieved_utc": retrieved.isoformat(),
        "snapshot_age_minutes_at_runtime_start": round((start - retrieved).total_seconds() / 60, 2),
        "window_start_exclusive_utc": lower.isoformat(), "window_end_inclusive_utc": upper.isoformat(),
        "minimum_lead_minutes": minimum_lead_minutes, "horizon_days": horizon_days,
        "snapshot_rows_in_runtime_window": len(snapshot_candidates),
        "snapshot_finished_invalid_score_rows": len(quarantined_invalid_scores),
        "snapshot_finished_invalid_score_keys": [list(k) for k in sorted(quarantined_invalid_scores)],
        "runtime_rows_in_declared_window": len(runtime_candidates),
        "exact_season_id_and_fixture_id_matches": len(common),
        "snapshot_only_rows": len(snapshot_only), "runtime_only_rows": len(runtime_only),
        "snapshot_only_no_home_away_flag_true": len(flagged),
        "snapshot_only_no_home_away_flag_false": len(valid_flag_false),
        "snapshot_only_no_home_away_flag_unknown": len(unknown_flag),
        "snapshot_only_flag_false_fixture_keys": [list(k) for k in sorted(valid_flag_false)],
        "snapshot_only_flag_true_fixture_keys": [list(k) for k in sorted(flagged)],
        "runtime_only_fixture_keys": [list(k) for k in sorted(runtime_only)],
        "combo_masking_verified": True, "combo_probability_rows_visible": 0,
        "canonical_joins_created": 0, "predictions_created": 0, "provider_api_calls": 0,
        "production_eligible": False,
        "interpretation": "Exact same-provider season-ID + fixture-ID comparison only. Difference rows are candidates for source/input review, not canonical joins or settlement truth.",
        "snapshot_artifact_id": str(snapshot_artifact_id), "snapshot_artifact_sha256": str(snapshot_artifact_sha256),
        "runtime_run_id": str(runtime_run_id), "runtime_artifact_id": str(runtime_artifact_id),
        "runtime_artifact_sha256": str(runtime_artifact_sha256),
    }
    return diffs, summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--snapshot-json", required=True, type=Path)
    p.add_argument("--runtime-csv", required=True, type=Path)
    p.add_argument("--runtime-started-utc", required=True)
    p.add_argument("--output-diff-csv", required=True, type=Path)
    p.add_argument("--output-summary-json", required=True, type=Path)
    p.add_argument("--snapshot-artifact-id", default="")
    p.add_argument("--snapshot-artifact-sha256", default="")
    p.add_argument("--runtime-run-id", default="")
    p.add_argument("--runtime-artifact-id", default="")
    p.add_argument("--runtime-artifact-sha256", default="")
    a = p.parse_args()
    snapshot = json.loads(a.snapshot_json.read_text(encoding="utf-8"))
    with a.runtime_csv.open("r", encoding="utf-8-sig", newline="") as f:
        runtime_rows = list(csv.DictReader(f))
    diffs, summary = audit(snapshot, runtime_rows, a.runtime_started_utc,
        snapshot_artifact_id=a.snapshot_artifact_id, snapshot_artifact_sha256=a.snapshot_artifact_sha256,
        runtime_run_id=a.runtime_run_id, runtime_artifact_id=a.runtime_artifact_id,
        runtime_artifact_sha256=a.runtime_artifact_sha256)
    a.output_diff_csv.parent.mkdir(parents=True, exist_ok=True)
    with a.output_diff_csv.open("w", encoding="utf-8", newline="") as f:
        fields = list(diffs[0]) if diffs else ["selected_season_id", "fixture_id", "side", "classification"]
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(diffs)
    a.output_summary_json.parent.mkdir(parents=True, exist_ok=True)
    a.output_summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
