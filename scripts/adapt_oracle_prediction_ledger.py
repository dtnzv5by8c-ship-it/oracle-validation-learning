#!/usr/bin/env python3
"""Research-only adapter for Oracle prediction CSV rows.

Schema adaptation is deliberately separate from evaluation and production
eligibility. Challenger rows may be staged for research, but are never relabelled
as production. Missing canonical team IDs are surfaced as evaluation blockers.
No canonical or production ledger is modified.
"""
import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

ALIASES = {
    "prediction_id": ("prediction_id",),
    "fixture_id": ("fixture_id",),
    "competition_id": ("competition_id", "competition"),
    "home_team_id": ("home_team_id",),
    "away_team_id": ("away_team_id",),
    "market": ("market", "model"),
    "selection": ("selection",),
    "probability": ("probability", "raw_probability"),
    "prediction_timestamp_utc": ("prediction_timestamp_utc", "prediction_timestamp"),
    "model_version": ("model_version",),
    "model_commit": ("model_commit", "model_code_sha"),
    "archive_release_id": ("archive_release_id", "feature_snapshot_id"),
    "source_manifest_hash": ("source_manifest_hash",),
}

MARKET_MAP = {
    "BTTS_YES": ("BTTS", "YES"),
    "BTTS_NO": ("BTTS", "NO"),
    "HOME_1X": ("DOUBLE_CHANCE", "1X"),
    "AWAY_X2": ("DOUBLE_CHANCE", "X2"),
    "HOME_1X_U45": ("COMPOSITE", "HOME_1X_U45"),
    "AWAY_X2_U45": ("COMPOSITE", "AWAY_X2_U45"),
}

def parse_aware(value):
    if not value:
        return None
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed

def resolve_kickoff(row):
    """Combine date/time only when kickoff_time explicitly carries a UTC offset."""
    direct = row.get("scheduled_kickoff_utc")
    if direct:
        parsed = parse_aware(direct)
        return (parsed.isoformat() if parsed else ""), ("scheduled_kickoff_utc" if parsed else None)
    date, time = row.get("fixture_date", ""), row.get("kickoff_time", "")
    if not date or not time:
        return "", None
    try:
        parsed = parse_aware(f"{date}T{time}")
    except ValueError:
        return "", None
    if parsed is None:
        return "", None
    return parsed.isoformat(), "fixture_date+kickoff_time (explicit offset in source time)"

def first_value(row, names):
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return value, name
    return "", None

def adapt_row(row, row_number):
    adapted, source_columns = {}, {}
    for target, candidates in ALIASES.items():
        value, source_column = first_value(row, candidates)
        adapted[target] = value
        if source_column:
            source_columns[target] = source_column

    kickoff, kickoff_source = resolve_kickoff(row)
    adapted["scheduled_kickoff_utc"] = kickoff
    if kickoff_source:
        source_columns["scheduled_kickoff_utc"] = kickoff_source

    reasons = []
    blockers = []
    model_label = str(row.get("model", "")).strip().upper()
    explicit_market = str(row.get("market", "")).strip()
    if not explicit_market and model_label:
        if model_label in MARKET_MAP:
            adapted["market"], adapted["selection"] = MARKET_MAP[model_label]
            source_columns["market"] = "model (explicit alias map)"
            source_columns["selection"] = "model (explicit alias map)"
        else:
            reasons.append("UNRECOGNIZED_MARKET_LABEL:" + model_label)

    for key in ("prediction_id", "fixture_id", "competition_id", "market", "selection",
                "model_version", "prediction_timestamp_utc", "source_manifest_hash"):
        if not adapted.get(key):
            reasons.append("MISSING_REQUIRED_FIELD:" + key)

    if not adapted.get("scheduled_kickoff_utc"):
        reasons.append("MISSING_OR_UNVERIFIED_KICKOFF")
    if not adapted.get("home_team_id"):
        blockers.append("MISSING_HOME_TEAM_ID")
    if not adapted.get("away_team_id"):
        blockers.append("MISSING_AWAY_TEAM_ID")

    try:
        probability = float(adapted.get("probability", ""))
        if not 0 <= probability <= 1:
            raise ValueError
        adapted["probability"] = probability
    except (TypeError, ValueError):
        reasons.append("INVALID_OR_MISSING_PROBABILITY")

    pred = None
    try:
        pred = parse_aware(adapted.get("prediction_timestamp_utc"))
    except ValueError:
        pass
    if adapted.get("prediction_timestamp_utc") and pred is None:
        reasons.append("PREDICTION_TIMESTAMP_NOT_TIMEZONE_AWARE")

    kick = None
    try:
        kick = parse_aware(adapted.get("scheduled_kickoff_utc"))
    except ValueError:
        pass
    if adapted.get("scheduled_kickoff_utc") and kick is None:
        reasons.append("KICKOFF_TIMESTAMP_NOT_TIMEZONE_AWARE")
    if pred and kick and pred >= kick:
        reasons.append("PREDICTION_NOT_STRICTLY_PRE_KICKOFF")

    model_status = str(row.get("model_status", "")).strip().upper()
    adapted["source_model_status"] = model_status or "STATUS_MISSING"
    adapted["production_eligibility"] = "NOT_GRANTED"
    adapted["evaluation_blockers"] = blockers

    # Research staging accepts structurally interpretable prediction rows, while
    # evaluation remains blocked until identity/provenance blockers are resolved.
    return {
        "source_row_number": row_number,
        "source_row": row,
        "source_columns": source_columns,
        "adapted_prediction": adapted,
        "quarantine_reasons": reasons,
        "evaluation_blockers": blockers,
    }

def run(input_path, accepted_path, quarantine_path, summary_path):
    with Path(input_path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("INPUT_CSV_HAS_NO_HEADER")
        staged, quarantined = [], []
        for row_number, row in enumerate(reader, start=2):
            item = adapt_row(row, row_number)
            if item["quarantine_reasons"]:
                quarantined.append(item)
            else:
                staged.append(item)
    for path, rows in ((accepted_path, staged), (quarantine_path, quarantined)):
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in rows), encoding="utf-8")
    summary = {
        "status": "RESEARCH_ONLY_ADAPTER_COMPLETE",
        "input_rows": len(staged) + len(quarantined),
        "research_staged_rows": len(staged),
        "quarantined_rows": len(quarantined),
        "staged_rows_blocked_from_evaluation": sum(bool(x["evaluation_blockers"]) for x in staged),
        "quarantine_reason_counts": {},
        "evaluation_blocker_counts": {},
        "production_eligibility": "NOT_GRANTED",
        "warning": "Research staging is not a verified evaluation set. Missing team IDs, provenance and other blockers must be resolved before scoring."
    }
    for item in quarantined:
        for reason in item["quarantine_reasons"]:
            code = reason.split(":", 1)[0]
            summary["quarantine_reason_counts"][code] = summary["quarantine_reason_counts"].get(code, 0) + 1
    for item in staged:
        for blocker in item["evaluation_blockers"]:
            summary["evaluation_blocker_counts"][blocker] = summary["evaluation_blocker_counts"].get(blocker, 0) + 1
    out = Path(summary_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--accepted-out", required=True)
    parser.add_argument("--quarantine-out", required=True)
    parser.add_argument("--summary-out", required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.accepted_out, args.quarantine_out, args.summary_out), sort_keys=True))

if __name__ == "__main__":
    main()
