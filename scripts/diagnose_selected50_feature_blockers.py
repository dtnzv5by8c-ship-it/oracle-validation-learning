#!/usr/bin/env python3
"""Offline fail-closed diagnostics for Selected-50 feature-blocked fixtures.

Consumes an existing sanitized runtime CSV only. No provider calls, joins,
team mapping, feature imputation, predictions, or production eligibility.
"""
from __future__ import annotations
import argparse, csv, json, math, re, unicodedata
from collections import defaultdict
from pathlib import Path

MIN_HISTORY = 5
BLOCKED = "BLOCKED_MISSING_REQUIRED_FEATURES"
PAIR_FEATURES = {"pair_btts_mean", "pair_fts_mean", "pair_cs_mean",
                 "score_environment", "shot_environment", "score_gap5"}
REQUIRED = {"fixture_id", "selected_id", "country", "league", "home_team", "away_team",
            "home_team_provider_id", "away_team_provider_id", "home_recent5_n", "away_recent5_n",
            "feature_support_status", "missing_required_features", "training_support_status",
            "COMBO_HOME_probability_pct", "COMBO_AWAY_probability_pct"}


def normalize_label(value):
    """Display-label grouping only; never an identity or join key."""
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).casefold()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text).split())


def features(value):
    return list(dict.fromkeys(x.strip() for x in str(value or "").split(";") if x.strip()))


def count(value, field):
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        n = float(raw)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{field} must be a non-negative integer or blank") from exc
    if not math.isfinite(n) or n < 0 or not n.is_integer():
        raise ValueError(f"{field} must be a non-negative integer or blank")
    return int(n)


def source_team_key(season, team_id, country, league, name):
    if season and team_id and team_id.casefold() not in {"0", "none", "null"}:
        return f"provider-season:{season}|provider-team:{team_id}", "SEASON_SCOPED_PROVIDER_ID"
    return (f"label-only:{normalize_label(country)}|{normalize_label(league)}|{normalize_label(name)}",
            "LABEL_ONLY_NOT_JOINABLE")


def diagnose(rows):
    rows = list(rows)
    if not rows:
        raise ValueError("runtime report contains no fixture rows")
    missing = sorted(REQUIRED - set(rows[0]))
    if missing:
        raise ValueError("runtime report missing required columns: " + ", ".join(missing))
    ids = [str(r.get("fixture_id") or "").strip() for r in rows]
    if any(not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("runtime report has blank or duplicate fixture_id values")
    if any(str(r.get(c) or "").strip() for r in rows
           for c in ("COMBO_HOME_probability_pct", "COMBO_AWAY_probability_pct")):
        raise ValueError("Combo probability mask is violated; refusing diagnostics")

    sides, blocked_ids, unclassified, contradictions = [], [], [], []
    unknown_counts = training_not_pass = 0
    for r in rows:
        if str(r.get("feature_support_status") or "").strip() != BLOCKED and \
           str(r.get("prediction_status") or "").strip() != BLOCKED:
            continue
        fid = str(r["fixture_id"]).strip()
        blocked_ids.append(fid)
        missing_features = features(r.get("missing_required_features"))
        pair = [f for f in missing_features if f in PAIR_FEATURES]
        emitted = 0
        for side in ("home", "away"):
            side_missing = [f for f in missing_features if f.startswith(side + "_")]
            if not side_missing:
                continue
            emitted += 1
            name = str(r.get(f"{side}_team") or "").strip()
            team_id = str(r.get(f"{side}_team_provider_id") or "").strip()
            season = str(r.get("provider_season_id") or r.get("selected_id") or "").strip()
            field = f"{side}_recent5_n"
            n = count(r.get(field), field)
            if n is None:
                diagnosis, shortfall = "HISTORY_COUNT_UNKNOWN", ""
                unknown_counts += 1
            elif n < MIN_HISTORY:
                diagnosis, shortfall = "INSUFFICIENT_ORIENTED_HISTORY", MIN_HISTORY - n
            else:
                diagnosis, shortfall = "COUNT_MEETS_MINIMUM_BUT_FEATURES_MISSING", 0
                contradictions.append(fid)
            key, identity = source_team_key(season, team_id, r.get("country",""),
                                             r.get("league",""), name)
            sides.append({
                "fixture_id": fid, "kickoff_utc": str(r.get("date_utc") or ""),
                "selected_id": str(r.get("selected_id") or ""), "provider_season_id": season,
                "country": str(r.get("country") or ""), "league": str(r.get("league") or ""),
                "side": side, "team_name_source_label": name,
                "normalized_team_label_grouping_only": normalize_label(name),
                "source_provider_team_id": team_id, "source_team_key_not_canonical": key,
                "identity_basis": identity, "oriented_history_count_from_runtime": "" if n is None else n,
                "minimum_oriented_history_required": MIN_HISTORY, "history_count_shortfall": shortfall,
                "history_support_diagnosis": diagnosis, "missing_side_features": ";".join(side_missing),
                "missing_pair_environment_features": ";".join(pair),
                "training_support_status": str(r.get("training_support_status") or ""),
                "unavailable_training_markets": str(r.get("unavailable_training_markets") or ""),
                "mapping_action": "NO_AUTOMATIC_MAPPING_REVIEW_ONLY",
                "history_cutoff_replayed_by_diagnostic": "NO_RUNTIME_COUNT_ONLY",
                "features_imputed": 0, "prediction_created": 0, "production_eligible": "NO",
            })
        if not emitted:
            unclassified.append(fid)
            sides.append({
                "fixture_id": fid, "kickoff_utc": str(r.get("date_utc") or ""),
                "selected_id": str(r.get("selected_id") or ""),
                "provider_season_id": str(r.get("provider_season_id") or r.get("selected_id") or ""),
                "country": str(r.get("country") or ""), "league": str(r.get("league") or ""),
                "side": "PAIR_OR_ENVIRONMENT_ONLY", "team_name_source_label": "",
                "normalized_team_label_grouping_only": "", "source_provider_team_id": "",
                "source_team_key_not_canonical": "", "identity_basis": "NO_TEAM_ATTRIBUTION",
                "oriented_history_count_from_runtime": "", "minimum_oriented_history_required": MIN_HISTORY,
                "history_count_shortfall": "", "history_support_diagnosis": "NO_SIDE_FEATURES_NAMED",
                "missing_side_features": "", "missing_pair_environment_features": ";".join(pair),
                "training_support_status": str(r.get("training_support_status") or ""),
                "unavailable_training_markets": str(r.get("unavailable_training_markets") or ""),
                "mapping_action": "NO_AUTOMATIC_MAPPING_REVIEW_ONLY",
                "history_cutoff_replayed_by_diagnostic": "NO_RUNTIME_COUNT_ONLY",
                "features_imputed": 0, "prediction_created": 0, "production_eligible": "NO",
            })
        if str(r.get("training_support_status") or "") != "PASS_ALL_MARKET_MODELS":
            training_not_pass += 1

    grouped = defaultdict(list)
    for item in sides:
        if item["side"] in {"home", "away"} and item["source_team_key_not_canonical"]:
            grouped[item["source_team_key_not_canonical"]].append(item)
    teams = []
    for key, items in sorted(grouped.items()):
        counts = [int(x["oriented_history_count_from_runtime"]) for x in items
                  if x["oriented_history_count_from_runtime"] != ""]
        teams.append({
            "source_team_key_not_canonical": key, "country": items[0]["country"],
            "league": items[0]["league"], "provider_season_id": items[0]["provider_season_id"],
            "source_provider_team_id": items[0]["source_provider_team_id"],
            "normalized_team_label_grouping_only": items[0]["normalized_team_label_grouping_only"],
            "source_display_labels": ";".join(sorted({x["team_name_source_label"] for x in items})),
            "blocked_fixture_side_rows": len(items),
            "home_side_gaps": sum(x["side"] == "home" for x in items),
            "away_side_gaps": sum(x["side"] == "away" for x in items),
            "minimum_observed_oriented_history_count": min(counts) if counts else "",
            "maximum_observed_oriented_history_count": max(counts) if counts else "",
            "history_support_diagnoses": ";".join(sorted({x["history_support_diagnosis"] for x in items})),
            "mapping_action": "NO_AUTOMATIC_MAPPING_REVIEW_ONLY", "identity_approved": "NO",
            "features_imputed": 0, "prediction_created": 0, "production_eligible": "NO",
        })
    diagnosis_counts = defaultdict(int)
    for x in sides:
        diagnosis_counts[x["history_support_diagnosis"]] += 1
    summary = {
        "status": "PASS_RESEARCH_ONLY_FEATURE_BLOCKER_DIAGNOSTICS",
        "input_fixture_rows": len(rows), "unique_fixture_ids": len(set(ids)),
        "blocked_fixture_rows": len(blocked_ids), "blocked_fixture_ids": blocked_ids,
        "blocked_fixture_side_rows": sum(x["side"] in {"home","away"} for x in sides),
        "home_side_gap_rows": sum(x["side"] == "home" for x in sides),
        "away_side_gap_rows": sum(x["side"] == "away" for x in sides),
        "fixtures_with_both_sides_below_minimum": sum(
            sum(x["fixture_id"] == fid and x["history_support_diagnosis"] == "INSUFFICIENT_ORIENTED_HISTORY"
                for x in sides) == 2 for fid in blocked_ids),
        "history_support_diagnosis_counts": dict(sorted(diagnosis_counts.items())),
        "count_meets_minimum_but_features_missing_rows": len(contradictions),
        "count_contradiction_fixture_ids": sorted(set(contradictions)),
        "unknown_history_count_rows": unknown_counts, "unclassified_blocked_fixture_ids": unclassified,
        "blocked_fixtures_without_all_market_training_support": training_not_pass,
        "source_snapshot_provenance": "INHERITED_FROM_RUNTIME_REPORT_NOT_REVALIDATED_HERE",
        "history_cutoff": "RUNTIME_REPORTED_STRICTLY_BEFORE_KICKOFF; NOT_REPLAYED_BY_THIS_SCRIPT",
        "team_identity": "PROVIDER_IDS_PRESERVED; NO_CANONICAL_JOIN_OR_AUTO_MAPPING",
        "combo_masking_verified": True, "combo_probability_rows_visible": 0,
        "features_imputed": 0, "model_predictions_created": 0, "provider_api_calls": 0,
        "production_eligible": False,
        "interpretation": "Counts and feature names are copied from the supplied runtime report. This diagnostic does not reconstruct match history or prove why a history count is low.",
    }
    return sides, teams, summary


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input-csv", required=True, type=Path)
    p.add_argument("--output-side-csv", required=True, type=Path)
    p.add_argument("--output-team-csv", required=True, type=Path)
    p.add_argument("--output-summary-json", required=True, type=Path)
    p.add_argument("--source-runtime-run-id", default="")
    p.add_argument("--source-runtime-artifact-id", default="")
    p.add_argument("--source-runtime-commit", default="")
    p.add_argument("--source-runtime-artifact-sha256", default="")
    a = p.parse_args()
    with a.input_csv.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    side, team, summary = diagnose(rows)
    summary.update({
        "source_runtime_run_id": a.source_runtime_run_id,
        "source_runtime_artifact_id": a.source_runtime_artifact_id,
        "source_runtime_commit": a.source_runtime_commit,
        "source_runtime_artifact_sha256": a.source_runtime_artifact_sha256,
    })
    write_csv(a.output_side_csv, side)
    write_csv(a.output_team_csv, team)
    a.output_summary_json.parent.mkdir(parents=True, exist_ok=True)
    a.output_summary_json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
