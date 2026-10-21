#!/usr/bin/env python3
"""Research-only validation of a settlement event linked to an immutable prediction."""
from datetime import datetime

ALLOWED = {"WIN", "LOSS", "PUSH", "VOID", "UNSETTLED"}
REQUIRED = ("prediction_id", "fixture_id", "outcome", "settled_at_utc", "result_source", "settlement_rule_version")

def _parse(value):
    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("SETTLEMENT_TIMESTAMP_TIMEZONE_REQUIRED")
    return parsed

def validate_settlement(event, prediction_ids, fixture_ids):
    missing = [k for k in REQUIRED if event.get(k) in (None, "")]
    if missing:
        raise ValueError("SETTLEMENT_MISSING_FIELDS:" + ",".join(missing))
    if event["prediction_id"] not in prediction_ids:
        raise ValueError("UNKNOWN_PREDICTION_ID")
    if event["fixture_id"] not in fixture_ids:
        raise ValueError("UNVERIFIED_FIXTURE_ID")
    outcome = str(event["outcome"]).upper()
    if outcome not in ALLOWED:
        raise ValueError("INVALID_SETTLEMENT_OUTCOME")
    _parse(event["settled_at_utc"])
    if outcome == "UNSETTLED":
        return {"status": "PENDING", "scorable": False, "reason": "OUTCOME_UNSETTLED"}
    return {"status": "VALIDATED", "scorable": outcome in {"WIN", "LOSS"}, "outcome": outcome}
