#!/usr/bin/env python3
"""Replay Selected-50 team histories from the pinned archive for blocked runtime sides.

Research/reporting only. Mirrors the existing runtime's archive grouping, strict
kickoff cutoff, completion/score gate, fixture-ID deduplication and duplicate
signature quarantine. It does not alter runtime features or predictions.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

FINISHED = {"complete", "completed", "finished", "full time", "full-time", "ft", "ended", "played"}
SIDE_FEATURES = ("gf5", "ga5", "btts5", "fts5", "cs5", "shots5", "sot5")


def first(row, keys):
    for key in keys:
        value = row.get(key)
        if value not in (None, ""):
            return value
    return None


def team_ids(match):
    home = first(match, ("homeID", "home_id", "home_team_id"))
    away = first(match, ("awayID", "away_id", "away_team_id"))
    return (str(home).strip() if home is not None else "",
            str(away).strip() if away is not None else "")


def stamp(match):
    for key in ("date_unix", "kickoff_unix", "timestamp", "kickoff", "date", "datetime", "match_date"):
        value = match.get(key)
        if value in (None, ""):
            continue
        try:
            number = float(value)
            if math.isfinite(number) and number > 1_000_000_000:
                if number >= 1_000_000_000_000:
                    number /= 1000.0
                if math.isfinite(number):
                    return number
        except (TypeError, ValueError, OverflowError):
            pass
        try:
            parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            number = parsed.timestamp()
            return number if math.isfinite(number) else None
        except (TypeError, ValueError, OverflowError):
            pass
    return None


def number(value):
    if isinstance(value, bool):
        return None
    try:
        result = float(value)
        return result if math.isfinite(result) and result >= 0 else None
    except (TypeError, ValueError, OverflowError):
        return None


def match_score(match):
    return (number(first(match, ("homeGoalCount", "home_goals", "home_score"))),
            number(first(match, ("awayGoalCount", "away_goals", "away_score"))))


def valid_integer_score(home, away):
    return (home is not None and away is not None and
            float(home).is_integer() and float(away).is_integer())


def finished(match):
    status = str(first(match, ("status", "game_status")) or "").strip().lower()
    home, away = match_score(match)
    return status in FINISHED and home is not None and away is not None


def completed_signature(row):
    if not row["finished"] or not valid_integer_score(row["home_goals"], row["away_goals"]):
        return None
    home_id, away_id = row["home_id"], row["away_id"]
    if not row["competition_id"] or not home_id or not away_id or home_id == away_id:
        return None
    kickoff = row["kickoff_unix"]
    if kickoff is None or not math.isfinite(kickoff):
        return None
    return row["competition_id"], kickoff, tuple(sorted((home_id, away_id)))


def load_selected_manifest(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = {}
    labels = {}
    for row in rows:
        selected_id = str(row.get("selected_id") or "").strip()
        label = (str(row.get("country") or "").strip(),
                 str(row.get("competition_name") or "").strip())
        if not selected_id or not all(label) or selected_id in selected or label in labels:
            raise ValueError("Selected manifest has blank or duplicate IDs/labels")
        selected[selected_id] = label
        labels[label] = selected_id
    if not selected:
        raise ValueError("Selected manifest is empty")
    return selected, labels


def load_archive(archive_path, selected_labels):
    """Load the same label-mapped season groups used by the existing runtime."""
    rows = []
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
        manifest_name = next((name for name in names if name.endswith("ingestion_manifest.json")), None)
        if not manifest_name:
            raise ValueError("Pinned archive ingestion_manifest.json is missing")
        manifest = json.loads(archive.read(manifest_name).decode("utf-8"))
        if not isinstance(manifest, list):
            raise ValueError("Unexpected ingestion manifest shape")
        mapped_seasons = 0
        for meta in manifest:
            if not isinstance(meta, dict):
                continue
            season_id = str(meta.get("season_id") or "").strip()
            label = (str(meta.get("selected_country") or "").strip(),
                     str(meta.get("selected_competition_name") or "").strip())
            selected_id = selected_labels.get(label)
            if not selected_id:
                continue
            mapped_seasons += 1
            match_path = f"seasons/{season_id}/matches.json"
            if match_path not in names:
                continue
            source = json.loads(archive.read(match_path).decode("utf-8"))
            if not isinstance(source, list):
                continue
            for source_row, match in enumerate(source):
                if not isinstance(match, dict):
                    continue
                home_id, away_id = team_ids(match)
                kickoff = stamp(match)
                home_goals, away_goals = match_score(match)
                status = str(first(match, ("status", "game_status")) or "")
                rows.append({
                    "competition_id": selected_id, "season_id": season_id,
                    "country": label[0], "league": label[1],
                    "source_file": match_path, "source_row": source_row,
                    "fixture_id": str(match.get("id") or "").strip(),
                    "kickoff_unix": kickoff, "home_id": home_id, "away_id": away_id,
                    "home_goals": home_goals, "away_goals": away_goals,
                    "finished": finished(match), "status_raw": status,
                    "raw": match,
                    "raw_record_sha256": hashlib.sha256(
                        json.dumps(match, sort_keys=True, ensure_ascii=False).encode("utf-8")
                    ).hexdigest(),
                })
    if mapped_seasons == 0:
        raise ValueError("No archive seasons map to the Selected-50 manifest")
    return rows, mapped_seasons


def deduplicate(rows):
    """Mirror runtime fixture-ID collision quarantine and first-record deduplication."""
    groups = defaultdict(list)
    for row in rows:
        if row["kickoff_unix"] is None or not row["home_id"] or not row["away_id"]:
            continue
        fixture_id = row["fixture_id"]
        if not fixture_id:
            continue
        pair = tuple(sorted((row["home_id"], row["away_id"]))) if row["home_id"] != row["away_id"] else None
        score = None
        if pair and valid_integer_score(row["home_goals"], row["away_goals"]):
            score = ((int(row["home_goals"]), int(row["away_goals"])) if row["home_id"] == pair[0]
                     else (int(row["away_goals"]), int(row["home_goals"])))
        groups[(row["competition_id"], fixture_id)].append(
            (row["kickoff_unix"], pair, score, bool(row["finished"]))
        )
    conflicting = {key for key, values in groups.items() if len(values) > 1 and len(set(values)) > 1}
    exact_extra = set()
    seen_ids = set()
    normalized = []
    for row in rows:
        if row["kickoff_unix"] is None or not row["home_id"] or not row["away_id"]:
            continue
        fixture_id = row["fixture_id"]
        key_id = (row["competition_id"], fixture_id)
        if fixture_id and key_id in conflicting:
            continue
        if fixture_id:
            if key_id in seen_ids:
                exact_extra.add((row["source_file"], row["source_row"]))
                continue
            seen_ids.add(key_id)
            dedup_key = key_id
        else:
            dedup_key = (row["competition_id"], row["season_id"], row["kickoff_unix"],
                         row["home_id"], row["away_id"])
        normalized.append(row)
    signature_groups = defaultdict(list)
    for row in normalized:
        signature = completed_signature(row)
        if signature is not None:
            signature_groups[signature].append(row)
    duplicate_signatures = {key for key, values in signature_groups.items() if len(values) > 1}
    # Preserve exact runtime semantics: every row in a duplicate completed signature is quarantined.
    return normalized, conflicting, exact_extra, duplicate_signatures


def parse_target_time(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        result = parsed.timestamp()
        return result if math.isfinite(result) else None
    except (TypeError, ValueError, OverflowError):
        return None


def numeric_feature_completeness(sample, side, team_id):
    if len(sample) < 5:
        return {f"{side}_{name}": "NO_FIVE_MATCH_SAMPLE" for name in SIDE_FEATURES}
    shot_key = "team_a_shots" if side == "home" else "team_b_shots"
    sot_key = "team_a_shotsOnTarget" if side == "home" else "team_b_shotsOnTarget"
    shot_n = sum(number(row["raw"].get(shot_key)) is not None for row in sample)
    sot_n = sum(number(row["raw"].get(sot_key)) is not None for row in sample)
    result = {f"{side}_{name}": "COMPLETE_FROM_FIVE_MATCHES" for name in SIDE_FEATURES[:5]}
    result[f"{side}_shots5"] = "COMPLETE" if shot_n else "NO_NUMERIC_SOURCE_VALUES"
    result[f"{side}_sot5"] = "COMPLETE" if sot_n else "NO_NUMERIC_SOURCE_VALUES"
    return result


def audit(runtime_rows, archive_rows, selected_ids):
    normalized, conflicting_ids, exact_extra, duplicate_signatures = deduplicate(archive_rows)
    by_source = {(r["source_file"], r["source_row"]): r for r in archive_rows}
    normalized_sources = {(r["source_file"], r["source_row"]) for r in normalized}
    sides_out, details_out = [], []
    reason_counts = Counter()
    count_mismatches = []
    blocked_fixtures = set()
    for target in runtime_rows:
        missing = [x for x in str(target.get("missing_required_features") or "").split(";") if x]
        if (str(target.get("feature_support_status") or "") != "BLOCKED_MISSING_REQUIRED_FEATURES"
                and str(target.get("prediction_status") or "") != "BLOCKED_MISSING_REQUIRED_FEATURES"
                and not missing):
            continue
        fixture_id = str(target.get("fixture_id") or "").strip()
        selected_id = str(target.get("selected_id") or "").strip()
        if not fixture_id or selected_id not in selected_ids:
            raise ValueError("Blocked runtime row has missing fixture ID or unknown selected_id")
        blocked_fixtures.add(fixture_id)
        cutoff = parse_target_time(target.get("date_utc") or target.get("kickoff_utc"))
        for side in ("home", "away"):
            side_missing = [x for x in missing if x.startswith(side + "_")]
            if not side_missing:
                continue
            team_id = str(target.get(f"{side}_team_provider_id") or "").strip()
            if not team_id:
                sides_out.append({
                    "fixture_id": fixture_id, "selected_id": selected_id, "side": side,
                    "team_id": "", "audit_status": "BLOCKED_INVALID_TARGET_TEAM_ID",
                    "runtime_history_count": target.get(f"{side}_recent5_n", ""),
                    "reconstructed_history_count": "", "history_count_reconciles": "NO",
                    "considered_source_rows": 0, "included_history_match_ids": "",
                    "excluded_history_match_ids": "", "missing_side_features": ";".join(side_missing),
                    "root_cause": "TARGET_TEAM_PROVIDER_ID_UNAVAILABLE",
                })
                count_mismatches.append(f"{fixture_id}:{side}:missing_target_team_id")
                continue
            candidates = [r for r in archive_rows if r["competition_id"] == selected_id
                          and team_id in {r["home_id"], r["away_id"]}]
            included = []
            exclusions = Counter()
            for row in candidates:
                home_id, away_id = row["home_id"], row["away_id"]
                if row["kickoff_unix"] is None:
                    reason, detail = "OTHER_EVIDENCED_REASON", "MISSING_OR_INVALID_KICKOFF"
                elif cutoff is None:
                    reason, detail = "OTHER_EVIDENCED_REASON", "TARGET_KICKOFF_UNAVAILABLE"
                elif row["kickoff_unix"] >= cutoff:
                    reason, detail = "AFTER_CUTOFF", "NOT_STRICTLY_BEFORE_TARGET_KICKOFF"
                elif not home_id or not away_id or home_id == away_id:
                    reason, detail = "ORIENTATION_UNAVAILABLE", "MISSING_OR_IDENTICAL_TEAM_IDS"
                elif row["fixture_id"] and (selected_id, row["fixture_id"]) in conflicting_ids:
                    reason, detail = "DUPLICATE_RECORD", "CONFLICTING_COMPETITION_SCOPED_FIXTURE_ID"
                elif (row["source_file"], row["source_row"]) in exact_extra:
                    reason, detail = "DUPLICATE_RECORD", "EXACT_DUPLICATE_FIXTURE_ID_EXTRA_ROW"
                elif not row["finished"]:
                    reason, detail = "REQUIRED_FEATURE_MISSING", "SOURCE_STATUS_NOT_FINISHED"
                elif not valid_integer_score(row["home_goals"], row["away_goals"]):
                    reason, detail = "REQUIRED_FEATURE_MISSING", "MISSING_OR_INVALID_INTEGER_SCORE"
                else:
                    signature = completed_signature(row)
                    if signature in duplicate_signatures:
                        reason, detail = "DUPLICATE_RECORD", "DUPLICATE_COMPLETED_FIXTURE_SIGNATURE"
                    elif (row["source_file"], row["source_row"]) not in normalized_sources:
                        reason, detail = "INVALID_IDENTITY", "NOT_RETAINED_BY_RUNTIME_NORMALIZATION"
                    else:
                        reason, detail = "INCLUDED_IN_RUNTIME_HISTORY", "PASSED_RUNTIME_HISTORY_GATES"
                        included.append(row)
                if reason != "INCLUDED_IN_RUNTIME_HISTORY":
                    exclusions[reason] += 1
                reason_counts[reason] += 1
                historical_side = ("home" if home_id == team_id else "away" if away_id == team_id else "unknown")
                details_out.append({
                    "target_fixture_id": fixture_id, "selected_id": selected_id, "target_side": side,
                    "target_team_id": team_id, "target_kickoff_utc": target.get("date_utc", ""),
                    "historical_fixture_id": row["fixture_id"], "archive_season_id": row["season_id"],
                    "historical_kickoff_utc": datetime.fromtimestamp(row["kickoff_unix"], timezone.utc).isoformat()
                        if row["kickoff_unix"] is not None else "",
                    "historical_team_orientation": historical_side, "historical_home_team_id": home_id,
                    "historical_away_team_id": away_id, "historical_status": row["status_raw"],
                    "historical_home_score": row["home_goals"], "historical_away_score": row["away_goals"],
                    "source_file": row["source_file"], "source_record_index": row["source_row"],
                    "source_record_sha256": row["raw_record_sha256"],
                    "history_decision": reason, "exclusion_detail": detail,
                    "historical_shots_numeric": number(row["raw"].get("team_a_shots" if historical_side == "home" else "team_b_shots")) is not None,
                    "historical_sot_numeric": number(row["raw"].get("team_a_shotsOnTarget" if historical_side == "home" else "team_b_shotsOnTarget")) is not None,
                })
            included.sort(key=lambda r: (r["kickoff_unix"], r["fixture_id"]))
            runtime_count_raw = str(target.get(f"{side}_recent5_n") or "").strip()
            try:
                runtime_count = int(float(runtime_count_raw))
                if float(runtime_count_raw) != runtime_count or runtime_count < 0:
                    raise ValueError
            except (TypeError, ValueError, OverflowError):
                runtime_count = None
            reconstructed = min(len(included), 5)
            reconciles = runtime_count is not None and runtime_count == reconstructed
            if not reconciles:
                count_mismatches.append(f"{fixture_id}:{side}:runtime={runtime_count_raw}:archive={reconstructed}")
            sample = included[-5:]
            completeness = numeric_feature_completeness(sample, side, team_id)
            root_cause = ("INSUFFICIENT_QUALIFYING_PRE_KICKOFF_HISTORY" if len(included) < 5
                          else "FIVE_MATCH_HISTORY_PRESENT_FEATURE_FIELD_GAP")
            sides_out.append({
                "fixture_id": fixture_id, "selected_id": selected_id, "country": target.get("country", ""),
                "league": target.get("league", ""), "side": side, "team_name": target.get(f"{side}_team", ""),
                "team_id": team_id, "target_kickoff_utc": target.get("date_utc", ""),
                "runtime_history_count": runtime_count_raw, "reconstructed_history_count": reconstructed,
                "all_qualifying_prior_matches": len(included), "history_count_reconciles": "YES" if reconciles else "NO",
                "considered_source_rows": len(candidates),
                "included_history_match_ids": ";".join(r["fixture_id"] or f"NO_ID:{r['source_row']}" for r in included),
                "last_five_included_match_ids": ";".join(r["fixture_id"] or f"NO_ID:{r['source_row']}" for r in sample),
                "excluded_history_match_ids": ";".join(
                    str(d["historical_fixture_id"] or f"NO_ID:{d['source_record_index']}")
                    for d in details_out if d["target_fixture_id"] == fixture_id and d["target_side"] == side
                    and d["history_decision"] != "INCLUDED_IN_RUNTIME_HISTORY"
                ),
                "excluded_reason_counts": json.dumps(dict(sorted(exclusions.items())), separators=(",", ":")),
                "missing_side_features": ";".join(side_missing),
                **completeness,
                "root_cause": root_cause,
                "audit_status": "PASS_RESEARCH_ONLY" if reconciles else "REVIEW_REQUIRED_COUNT_MISMATCH",
                "features_imputed": 0, "predictions_created": 0, "production_eligible": "NO",
            })
    summary = {
        "status": "PASS_RESEARCH_ONLY_ROW_LEVEL_FEATURE_PROVENANCE" if not count_mismatches else "REVIEW_REQUIRED_ROW_LEVEL_FEATURE_PROVENANCE",
        "runtime_fixture_rows": len(runtime_rows), "blocked_fixture_count": len(blocked_fixtures),
        "blocked_team_side_rows_audited": len(sides_out), "historical_match_detail_rows": len(details_out),
        "history_decision_counts": dict(sorted(reason_counts.items())),
        "runtime_archive_history_count_mismatches": count_mismatches,
        "all_side_history_counts_reconcile": not count_mismatches,
        "selected_competition_grouping": "EXACT_COUNTRY_COMPETITION_LABEL_TO_SELECTED_ID_AS_EXISTING_RUNTIME",
        "history_rules": "EXISTING_RUNTIME_FINISHED_INTEGER_SCORE_DISTINCT_TEAM_ID_DEDUPLICATED_SIGNATURE_STRICT_PRE_KICKOFF",
        "minimum_history_required": 5, "minimum_history_changed": False,
        "feature_imputation": 0, "production_model_logic_changed": False,
        "production_probabilities_changed": False, "provider_api_calls": 0,
        "production_eligible": False, "betting_eligible": False,
        "interpretation": "This is an independent research-only replay of existing runtime history rules. Any count mismatch remains unresolved; no missing match or feature is inferred.",
    }
    return sides_out, details_out, summary


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--selected-manifest", required=True, type=Path)
    parser.add_argument("--runtime-report", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    selected_ids, selected_labels = load_selected_manifest(args.selected_manifest)
    archive_rows, mapped_seasons = load_archive(args.archive, selected_labels)
    with args.runtime_report.open(encoding="utf-8-sig", newline="") as handle:
        runtime_rows = list(csv.DictReader(handle))
    sides, details, summary = audit(runtime_rows, archive_rows, set(selected_ids))
    summary.update({
        "archive_sha256": hashlib.sha256(args.archive.read_bytes()).hexdigest(),
        "archive_match_rows_loaded": len(archive_rows), "archive_seasons_mapped": mapped_seasons,
        "selected_league_groups": len(selected_ids),
    })
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "oracle_selected50_history_provenance_sides.csv", sides)
    write_csv(args.out_dir / "oracle_selected50_history_provenance_matches.csv", details)
    (args.out_dir / "oracle_selected50_history_provenance_qa.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
