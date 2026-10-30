#!/usr/bin/env python3
"""Independent, research-only chronology audit for paired H2H prediction rows."""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import math


def _utc_timestamp(value):
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        # The paired artifact contract is explicitly UTC. Do not silently
        # interpret a timezone-naive timestamp as UTC: its source timezone is
        # unknown, so chronology cannot be independently verified.
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            return None
        return parsed.astimezone(timezone.utc).timestamp()
    except (TypeError, ValueError, OverflowError, OSError):
        return None


def audit_h2h_paired_predictions(rows, expected_markets):
    """Check paired H2H output keys, feature dates, elapsed days and market coverage.

    This is a reporting/validation contract only. It does not fit models, alter
    probabilities, or infer canonical fixture/team identity.
    """
    expected = {str(m) for m in expected_markets}
    seen_keys = set()
    markets_by_fixture = defaultdict(set)
    metadata_by_fixture = defaultdict(set)
    market_counts = Counter()
    missing_fixture_market_keys = 0
    duplicate_fixture_market_rows = 0
    unexpected_market_rows = 0
    missing_kickoff_rows = 0
    invalid_kickoff_rows = 0
    missing_h2h_date_rows = 0
    invalid_h2h_date_rows = 0
    non_strict_prior_rows = 0
    invalid_days_since_last_rows = 0
    days_since_last_mismatch_rows = 0
    invalid_prior_count_rows = 0
    invalid_h2h_rate_rows = 0
    invalid_h2h_average_goals_rows = 0
    fixture_metadata_conflict_count = 0
    invalid_probability_rows = 0
    invalid_actual_rows = 0

    for row in rows:
        fixture_id = str(row.get("fixture_id") or "").strip()
        competition_id = str(row.get("competition_id") or "").strip()
        market = str(row.get("market") or "").strip()
        if not fixture_id or not competition_id or not market:
            missing_fixture_market_keys += 1
        fixture_key = (competition_id, fixture_id)
        key = (competition_id, fixture_id, market)
        if key in seen_keys:
            duplicate_fixture_market_rows += 1
        seen_keys.add(key)
        market_counts[market] += 1
        if market not in expected:
            unexpected_market_rows += 1
        if fixture_id and competition_id:
            markets_by_fixture[fixture_key].add(market)

        kickoff = _utc_timestamp(row.get("date_utc"))
        prior = _utc_timestamp(row.get("h2h_last_date_utc"))
        if row.get("date_utc") in (None, ""):
            missing_kickoff_rows += 1
        elif kickoff is None:
            invalid_kickoff_rows += 1
        if row.get("h2h_last_date_utc") in (None, ""):
            missing_h2h_date_rows += 1
        elif prior is None:
            invalid_h2h_date_rows += 1
        if kickoff is not None and prior is not None:
            if prior >= kickoff:
                non_strict_prior_rows += 1
            try:
                days = float(row.get("h2h_days_since_last"))
                if not math.isfinite(days) or days < 0:
                    invalid_days_since_last_rows += 1
                elif abs(days - ((kickoff - prior) / 86400.0)) > 1e-6:
                    days_since_last_mismatch_rows += 1
            except (TypeError, ValueError, OverflowError):
                invalid_days_since_last_rows += 1

        try:
            prior_n = float(row.get("h2h_prior_n"))
            if not math.isfinite(prior_n) or prior_n <= 0 or not prior_n.is_integer():
                invalid_prior_count_rows += 1
        except (TypeError, ValueError, OverflowError):
            invalid_prior_count_rows += 1
        try:
            rate = float(row.get("h2h_btts_rate_last5"))
            if not math.isfinite(rate) or not 0 <= rate <= 1:
                invalid_h2h_rate_rows += 1
        except (TypeError, ValueError, OverflowError):
            invalid_h2h_rate_rows += 1
        try:
            average_goals = float(row.get("h2h_avg_total_goals_last5"))
            if not math.isfinite(average_goals) or average_goals < 0:
                invalid_h2h_average_goals_rows += 1
        except (TypeError, ValueError, OverflowError):
            invalid_h2h_average_goals_rows += 1
        try:
            baseline_probability = float(row.get("baseline_probability"))
            candidate_probability = float(row.get("h2h_candidate_probability"))
            if (not math.isfinite(baseline_probability) or not 0 <= baseline_probability <= 1
                    or not math.isfinite(candidate_probability) or not 0 <= candidate_probability <= 1):
                invalid_probability_rows += 1
        except (TypeError, ValueError, OverflowError):
            invalid_probability_rows += 1
        if str(row.get("actual")) not in {"0", "1"}:
            invalid_actual_rows += 1

        if fixture_id and competition_id:
            metadata_by_fixture[fixture_key].add(tuple(
                str(row.get(name) or "")
                for name in (
                    "date_utc", "h2h_last_date_utc", "competition_id", "league",
                    "home_team", "away_team", "h2h_prior_n", "h2h_btts_rate_last5",
                    "h2h_avg_total_goals_last5", "h2h_days_since_last",
                )
            ))

    incomplete_market_sets = sum(
        1 for fixture_id in markets_by_fixture
        if markets_by_fixture[fixture_id] != expected
    )
    fixture_metadata_conflict_count = sum(
        1 for values in metadata_by_fixture.values() if len(values) > 1
    )
    row_count = len(rows)
    failures = {
        "missing_fixture_market_keys": missing_fixture_market_keys,
        "duplicate_fixture_market_rows": duplicate_fixture_market_rows,
        "unexpected_market_rows": unexpected_market_rows,
        "incomplete_fixture_market_sets": incomplete_market_sets,
        "missing_kickoff_rows": missing_kickoff_rows,
        "invalid_kickoff_rows": invalid_kickoff_rows,
        "missing_h2h_date_rows": missing_h2h_date_rows,
        "invalid_h2h_date_rows": invalid_h2h_date_rows,
        "non_strict_prior_rows": non_strict_prior_rows,
        "invalid_days_since_last_rows": invalid_days_since_last_rows,
        "days_since_last_mismatch_rows": days_since_last_mismatch_rows,
        "invalid_prior_count_rows": invalid_prior_count_rows,
        "invalid_h2h_rate_rows": invalid_h2h_rate_rows,
        "invalid_h2h_average_goals_rows": invalid_h2h_average_goals_rows,
        "fixture_metadata_conflict_count": fixture_metadata_conflict_count,
        "invalid_probability_rows": invalid_probability_rows,
        "invalid_actual_rows": invalid_actual_rows,
    }
    passed = row_count > 0 and all(value == 0 for value in failures.values())
    return {
        "status": "PASS_H2H_PAIRED_OUTPUT_CHRONOLOGY" if passed else (
            "BLOCKED_NO_PAIRED_ROWS" if row_count == 0 else "BLOCKED_H2H_PAIRED_OUTPUT_INTEGRITY"
        ),
        "row_count": row_count,
        "unique_fixture_count": len(markets_by_fixture),
        "expected_markets": sorted(expected),
        "market_row_counts": dict(sorted(market_counts.items())),
        **failures,
        "scope": "Research-only artifact integrity; not canonical identity, official settlement, calibration or betting approval.",
        "production_eligible": False,
        "betting_eligible": False,
    }
