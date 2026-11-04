#!/usr/bin/env python3
"""Fail-closed rolling-hour FootyStats request budget ledger (offline core)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

SCHEMA_VERSION = 1
DEFAULT_GLOBAL_LIMIT = 1800
DEFAULT_HEADROOM = 300
DEFAULT_RESERVATION_TTL_SECONDS = 7200


def parse_utc(value: Any, field: str = "timestamp_utc") -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include an explicit timezone")
    return parsed.astimezone(timezone.utc)


def utc_text(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("datetime must include an explicit timezone")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def empty_ledger() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "provider": "FootyStats",
        "global_limit_per_rolling_hour": DEFAULT_GLOBAL_LIMIT,
        "reserved_headroom": DEFAULT_HEADROOM,
        "actual_requests": [],
        "reservations": [],
    }


def validate_ledger(ledger: dict[str, Any]) -> None:
    if not isinstance(ledger, dict) or ledger.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("request ledger schema/version is invalid")
    if ledger.get("provider") != "FootyStats":
        raise ValueError("request ledger provider must be FootyStats")
    if ledger.get("global_limit_per_rolling_hour") != DEFAULT_GLOBAL_LIMIT:
        raise ValueError("request ledger global rolling-hour limit must remain 1800")
    if not isinstance(ledger.get("actual_requests"), list) or not isinstance(ledger.get("reservations"), list):
        raise ValueError("request ledger must contain actual_requests and reservations lists")
    seen_reservations: set[str] = set()
    for event in ledger["actual_requests"]:
        if not isinstance(event, dict):
            raise ValueError("actual request ledger event must be an object")
        parse_utc(event.get("timestamp_utc"), "actual_request.timestamp_utc")
    for reservation in ledger["reservations"]:
        if not isinstance(reservation, dict):
            raise ValueError("reservation ledger entry must be an object")
        rid = str(reservation.get("reservation_id") or "").strip()
        if not rid or rid in seen_reservations:
            raise ValueError("reservation IDs must be nonblank and unique")
        seen_reservations.add(rid)
        parse_utc(reservation.get("reserved_at_utc"), "reservation.reserved_at_utc")
        parse_utc(reservation.get("expires_at_utc"), "reservation.expires_at_utc")
        count = reservation.get("reserved_count")
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            raise ValueError("reservation reserved_count must be a positive integer")


def prune_ledger(ledger: dict[str, Any], now: datetime) -> dict[str, Any]:
    validate_ledger(ledger)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must include an explicit timezone")
    now = now.astimezone(timezone.utc)
    cutoff = now - timedelta(hours=1)
    ledger["actual_requests"] = [
        event for event in ledger["actual_requests"]
        if cutoff < parse_utc(event["timestamp_utc"]) <= now
    ]
    ledger["reservations"] = [
        reservation for reservation in ledger["reservations"]
        if parse_utc(reservation["expires_at_utc"]) > now
    ]
    return ledger


def active_usage(ledger: dict[str, Any], now: datetime) -> dict[str, int]:
    current = prune_ledger(ledger, now)
    actual = len(current["actual_requests"])
    reserved = sum(item["reserved_count"] for item in current["reservations"])
    return {"actual_requests_in_rolling_hour": actual, "active_reserved_requests": reserved, "active_total": actual + reserved}


def reserve_block(
    ledger: dict[str, Any],
    now: datetime,
    requested_count: int,
    reservation_id: str,
    request_limit: int | None = None,
    global_limit: int = DEFAULT_GLOBAL_LIMIT,
    reserved_headroom: int = DEFAULT_HEADROOM,
    ttl_seconds: int = DEFAULT_RESERVATION_TTL_SECONDS,
) -> tuple[dict[str, Any], int]:
    if isinstance(requested_count, bool) or not isinstance(requested_count, int) or requested_count < 1:
        raise ValueError("requested_count must be a positive integer")
    if isinstance(global_limit, bool) or not isinstance(global_limit, int) or global_limit < 1:
        raise ValueError("global_limit must be a positive integer")
    if request_limit is not None and (isinstance(request_limit, bool) or not isinstance(request_limit, int) or request_limit < 1):
        raise ValueError("provider request_limit must be a positive integer when supplied")
    if isinstance(reserved_headroom, bool) or not isinstance(reserved_headroom, int) or reserved_headroom < 0:
        raise ValueError("reserved_headroom must be a non-negative integer")
    if isinstance(ttl_seconds, bool) or not isinstance(ttl_seconds, int) or ttl_seconds < 1:
        raise ValueError("ttl_seconds must be a positive integer")
    if not isinstance(reservation_id, str) or not reservation_id.strip():
        raise ValueError("reservation_id is required")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must include an explicit timezone")

    current = prune_ledger(ledger, now)
    if any(item["reservation_id"] == reservation_id for item in current["reservations"]):
        raise ValueError(f"reservation already exists: {reservation_id}")
    effective_limit = min(global_limit, request_limit) if request_limit is not None else global_limit
    headroom = min(reserved_headroom, max(0, effective_limit - 1))
    usage = active_usage(current, now)["active_total"]
    available = max(0, effective_limit - headroom - usage)
    count = min(requested_count, available)
    if count < 1:
        raise ValueError(
            f"rolling-hour budget exhausted or reserved: usage={usage}, "
            f"effective_limit={effective_limit}, headroom={headroom}"
        )
    start = now.astimezone(timezone.utc)
    current["reservations"].append({
        "reservation_id": reservation_id,
        "reserved_at_utc": utc_text(start),
        "expires_at_utc": utc_text(start + timedelta(seconds=ttl_seconds)),
        "reserved_count": count,
        "status": "RESERVED_FAIL_CLOSED",
    })
    current["reservations"].sort(key=lambda item: item["reserved_at_utc"])
    validate_ledger(current)
    return current, count


def finalize_reservation(
    ledger: dict[str, Any],
    reservation_id: str,
    actual_timestamps: Iterable[str],
    now: datetime,
) -> dict[str, Any]:
    current = prune_ledger(ledger, now)
    matching = [item for item in current["reservations"] if item["reservation_id"] == reservation_id]
    if len(matching) != 1:
        raise ValueError(f"exactly one active reservation required: {reservation_id}")
    reservation = matching[0]
    timestamps = [utc_text(parse_utc(value, "actual_request.timestamp_utc")) for value in actual_timestamps]
    if len(timestamps) > reservation["reserved_count"]:
        raise ValueError("actual request count exceeds reserved block")
    reserved_at = parse_utc(reservation["reserved_at_utc"])
    now_utc = now.astimezone(timezone.utc)
    for value in timestamps:
        event_time = parse_utc(value)
        if event_time < reserved_at or event_time > now_utc:
            raise ValueError("actual request timestamp falls outside its reservation interval")
    current["reservations"] = [
        item for item in current["reservations"] if item["reservation_id"] != reservation_id
    ]
    current["actual_requests"].extend(
        {"timestamp_utc": value, "source": "FootyStats API workflow"}
        for value in timestamps
    )
    current["actual_requests"].sort(key=lambda item: item["timestamp_utc"])
    validate_ledger(current)
    return current
