#!/usr/bin/env python3
"""Research-only exact-ID current-feed identity contract; never fetches data or writes ledgers."""
from __future__ import annotations
from typing import Any, Mapping

VERIFIED_STATUSES = {"APPROVED", "VERIFIED"}

def classify_match(match: Mapping[str, Any], allowlist: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    """Fail closed unless canonical code has reviewed exact provider league ID and country.

    Expected allowlist item:
      {"status": "APPROVED", "league_id": "17", "country": "England"}
    Display names are retained for diagnostics only and never establish identity.
    """
    league_id = str(match.get("league_id") or "").strip()
    country = str(match.get("country") or match.get("category") or "").strip().casefold()
    display_name = str(match.get("league_name") or match.get("league") or "").strip()
    code = str(match.get("canonical_competition_code") or "").strip()
    base = {
        "canonical_competition_code": code,
        "league_id": league_id,
        "country": str(match.get("country") or match.get("category") or "").strip(),
        "display_name": display_name,
        "identity_status": "QUARANTINED",
        "admitted": False,
        "reason": "",
    }
    if not code:
        base["reason"] = "MISSING_CANONICAL_COMPETITION_CODE"
        return base
    entry = allowlist.get(code)
    if not isinstance(entry, Mapping) or str(entry.get("status", "")).strip().upper() not in VERIFIED_STATUSES:
        base["reason"] = "NO_APPROVED_ALLOWLIST_ENTRY"
        return base
    expected_id = str(entry.get("league_id") or "").strip()
    expected_country = str(entry.get("country") or "").strip().casefold()
    if not league_id:
        base["reason"] = "MISSING_PROVIDER_LEAGUE_ID"
        return base
    if not expected_id or league_id != expected_id:
        base["reason"] = "PROVIDER_LEAGUE_ID_MISMATCH"
        return base
    if not country:
        base["reason"] = "MISSING_COUNTRY_CATEGORY"
        return base
    if not expected_country or country != expected_country:
        base["reason"] = "COUNTRY_CATEGORY_MISMATCH"
        return base
    base["identity_status"] = "VERIFIED_ALLOWLIST_MATCH"
    base["admitted"] = True
    base["reason"] = "EXACT_APPROVED_ID_AND_COUNTRY_MATCH"
    return base
