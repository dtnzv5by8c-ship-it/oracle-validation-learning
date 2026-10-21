#!/usr/bin/env python3
"""Research-only fail-closed validation for prospective Oracle prediction snapshots."""
import argparse, json, math, hashlib
from datetime import datetime
from pathlib import Path

REQUIRED = ["prediction_id", "fixture_id", "competition_id", "scheduled_kickoff_utc", "home_team_id", "away_team_id", "market", "selection", "probability", "model_version", "model_commit", "archive_release_id", "archive_sha256", "prediction_created_at_utc", "max_source_timestamp_utc", "schema_version"]

def dt(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return parsed

def validate_record(record, existing):
    missing = [key for key in REQUIRED if key not in record or record[key] is None or record[key] == ""]
    if missing:
        raise ValueError("MISSING_FIELDS:" + ",".join(missing))
    try:
        probability = float(record["probability"])
    except (TypeError, ValueError):
        raise ValueError("INVALID_PROBABILITY")
    if not math.isfinite(probability) or probability < 0 or probability > 1:
        raise ValueError("INVALID_PROBABILITY")
    created = dt(str(record["prediction_created_at_utc"]))
    kickoff = dt(str(record["scheduled_kickoff_utc"]))
    source_max = dt(str(record["max_source_timestamp_utc"]))
    if created >= kickoff:
        raise ValueError("PREDICTION_NOT_PREMATCH")
    if source_max > created:
        raise ValueError("SOURCE_DATA_AFTER_PREDICTION")
    digest = str(record["archive_sha256"])
    if len(digest) != 64 or any(c not in "0123456789abcdefABCDEF" for c in digest):
        raise ValueError("INVALID_ARCHIVE_SHA256")
    key = "|".join(str(record[k]) for k in ("fixture_id", "market", "selection", "model_version", "prediction_created_at_utc"))
    normalized = dict(record)
    normalized["probability"] = probability
    payload = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    content_hash = hashlib.sha256(payload.encode()).hexdigest()
    if key in existing:
        if existing[key] == content_hash:
            return {"status": "DUPLICATE_IDENTICAL", "idempotency_key": key, "content_sha256": content_hash}
        raise ValueError("CONFLICTING_DUPLICATE")
    return {"status": "ACCEPTED", "idempotency_key": key, "content_sha256": content_hash, "record": normalized}

def load_existing(path):
    existing = {}
    if not path.exists():
        return existing
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        key = "|".join(str(row[k]) for k in ("fixture_id", "market", "selection", "model_version", "prediction_created_at_utc"))
        payload = json.dumps(row, sort_keys=True, separators=(",", ":"))
        existing[key] = hashlib.sha256(payload.encode()).hexdigest()
    return existing

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--ledger", required=True)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    record = json.loads(Path(a.input).read_text(encoding="utf-8"))
    ledger = Path(a.ledger)
    existing = load_existing(ledger)
    result = validate_record(record, existing)
    result.pop("record", None)
    print(json.dumps(result, sort_keys=True))
    if result["status"] == "ACCEPTED" and not a.dry_run:
        ledger.parent.mkdir(parents=True, exist_ok=True)
        with ledger.open("a", encoding="utf-8") as f:
            f.write(json.dumps(validate_record(record, existing)["record"], sort_keys=True, separators=(",", ":")) + "\n")
if __name__ == "__main__":
    main()
