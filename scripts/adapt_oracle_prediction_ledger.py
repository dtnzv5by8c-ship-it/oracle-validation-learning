#!/usr/bin/env python3
"""Research-only adapter for the canonical Oracle prediction CSV.

The adapter never invents team IDs, UTC timestamps, or model metadata. Rows that
lack required evidence are written to a quarantine JSONL with explicit reasons.
It does not write to the production repository or any canonical ledger.
"""
import argparse
import csv
import json
from pathlib import Path

# These are field-name aliases only. Values are preserved verbatim; no timezone,
# competition, team, market, or selection semantics are inferred.
ALIASES = {
    "prediction_id": ("prediction_id",),
    "fixture_id": ("fixture_id",),
    "competition_id": ("competition_id", "competition"),
    "scheduled_kickoff_utc": ("scheduled_kickoff_utc",),
    "home_team_id": ("home_team_id",),
    "away_team_id": ("away_team_id",),
    "market": ("market", "model"),
    "selection": ("selection",),
    "probability": ("probability", "raw_probability"),
    "prediction_timestamp_utc": ("prediction_timestamp_utc", "prediction_timestamp"),
    "model_version": ("model_version",),
    "model_commit": ("model_commit", "model_code_sha"),
    "archive_release_id": ("archive_release_id", "feature_snapshot_id"),
    "archive_sha256": ("archive_sha256",),
}
REQUIRED = tuple(ALIASES)

def first_value(row, names):
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return value, name
    return "", None

def adapt_row(row, row_number):
    adapted, source_columns, missing = {}, {}, []
    for target, candidates in ALIASES.items():
        value, source_column = first_value(row, candidates)
        adapted[target] = value
        if source_column:
            source_columns[target] = source_column
        else:
            missing.append(target)
    reasons = []
    # Translate only explicitly recognized production ledger model labels. Unknown
    # composite labels are quarantined rather than guessed into a market.
    model_label = str(row.get("model", "")).strip().upper()
    explicit_market = str(row.get("market", "")).strip()
    if not explicit_market and model_label:
        market_map = {
            "BTTS_YES": ("BTTS", "YES"),
            "BTTS_NO": ("BTTS", "NO"),
            "HOME_1X": ("DOUBLE_CHANCE", "1X"),
            "AWAY_X2": ("DOUBLE_CHANCE", "X2"),
        }
        if model_label in market_map:
            adapted["market"], adapted["selection"] = market_map[model_label]
            source_columns["market"] = "model (explicit alias map)"
            source_columns["selection"] = "model (explicit alias map)"
        elif model_label.endswith("_U45"):
            reasons.append("UNSUPPORTED_COMPOSITE_MARKET:" + model_label)
        else:
            reasons.append("UNRECOGNIZED_MARKET_LABEL:" + model_label)
    # Recompute after explicit market alias mapping, which may supply market and selection.
    missing = [key for key, value in adapted.items() if value in (None, "")]
    if missing:
        reasons.append("MISSING_REQUIRED_FIELDS:" + ",".join(missing))
    if row.get("source_manifest_hash") and not row.get("archive_sha256"):
        reasons.append("SOURCE_MANIFEST_HASH_IS_NOT_ARCHIVE_HASH")
    # Preserve the source's original status and values; challenger/shadow rows
    # must not be presented as production predictions.
    model_status = row.get("model_status", "")
    if model_status.upper() not in {"PRODUCTION", "LIVE"}:
        reasons.append("NOT_CONFIRMED_PRODUCTION:" + (model_status or "STATUS_MISSING"))
    try:
        probability = float(adapted.get("probability", ""))
        if not 0 <= probability <= 1:
            raise ValueError
        adapted["probability"] = probability
    except (TypeError, ValueError):
        reasons.append("INVALID_OR_MISSING_PROBABILITY")
    # Strictly require timezone-aware timestamps; date + kickoff_time are not
    # converted because fixture-specific timezone evidence is absent.
    for key in ("scheduled_kickoff_utc", "prediction_timestamp_utc"):
        value = adapted.get(key)
        if value:
            try:
                from datetime import datetime
                parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
                if parsed.tzinfo is None or parsed.utcoffset() is None:
                    raise ValueError
            except (TypeError, ValueError):
                reasons.append("TIMESTAMP_NOT_TIMEZONE_AWARE:" + key)
    if adapted.get("scheduled_kickoff_utc") and adapted.get("prediction_timestamp_utc"):
        try:
            from datetime import datetime
            kick = datetime.fromisoformat(str(adapted["scheduled_kickoff_utc"]).replace("Z", "+00:00"))
            pred = datetime.fromisoformat(str(adapted["prediction_timestamp_utc"]).replace("Z", "+00:00"))
            if kick.tzinfo and pred.tzinfo and pred >= kick:
                reasons.append("PREDICTION_NOT_STRICTLY_PRE_KICKOFF")
        except ValueError:
            pass
    envelope = {
        "source_row_number": row_number,
        "source_row": row,
        "source_columns": source_columns,
        "adapted_prediction": adapted,
        "quarantine_reasons": reasons,
    }
    return envelope

def run(input_path, accepted_path, quarantine_path, summary_path):
    with Path(input_path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("INPUT_CSV_HAS_NO_HEADER")
        accepted, quarantined = [], []
        for row_number, row in enumerate(reader, start=2):
            item = adapt_row(row, row_number)
            if item["quarantine_reasons"]:
                quarantined.append(item)
            else:
                accepted.append(item["adapted_prediction"])
    for path, rows in ((accepted_path, accepted), (quarantine_path, quarantined)):
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("".join(json.dumps(x, sort_keys=True) + "\n" for x in rows), encoding="utf-8")
    summary = {
        "status": "RESEARCH_ONLY_ADAPTER_COMPLETE",
        "input_rows": len(accepted) + len(quarantined),
        "accepted_rows": len(accepted),
        "quarantined_rows": len(quarantined),
        "quarantine_reason_counts": {},
        "production_eligibility": "NOT_GRANTED",
        "warning": "Accepted means schema-adaptable only; it does not independently prove provenance or authorize production evaluation."
    }
    for item in quarantined:
        for reason in item["quarantine_reasons"]:
            code = reason.split(":", 1)[0]
            summary["quarantine_reason_counts"][code] = summary["quarantine_reason_counts"].get(code, 0) + 1
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
