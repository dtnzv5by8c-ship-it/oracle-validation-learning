"""Research-only league-isolated batch runner contract.

This module is deliberately not wired into the governed live predictor yet.
It defines safe orchestration semantics for review and acceptance testing.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Iterable, Any


@dataclass(frozen=True)
class BatchItem:
    fixture_id: str
    league: str
    ready: bool = True
    gap_reason: str = ""


def run_isolated_batches(
    items: Iterable[BatchItem],
    processor: Callable[[BatchItem], Any],
    *,
    global_preflight: Callable[[], None],
) -> dict:
    """Run independent fixtures after a fail-closed global preflight.

    Global integrity/provenance/freshness failures abort before processing.
    Fixture-level gaps and processing exceptions are recorded and do not stop
    unrelated fixtures. No model probabilities or selection logic are changed.
    """
    global_preflight()  # Intentionally fail closed; do not swallow this error.
    results: list[dict] = []
    outcomes: list[dict] = []
    by_league: dict[str, dict[str, int]] = defaultdict(
        lambda: {"PREDICTED": 0, "SKIPPED_DATA_GAP": 0, "FAILED_PROCESSING": 0}
    )

    for item in items:
        if not item.ready:
            status = "SKIPPED_DATA_GAP"
            outcomes.append({
                "fixture_id": item.fixture_id,
                "league": item.league,
                "status": status,
                "reason": item.gap_reason or "PREMATCH_STATE_MISSING",
            })
            by_league[item.league][status] += 1
            continue
        try:
            value = processor(item)
        except Exception as exc:  # isolate fixture error, retain explicit failure
            status = "FAILED_PROCESSING"
            outcomes.append({
                "fixture_id": item.fixture_id,
                "league": item.league,
                "status": status,
                "reason": f"{type(exc).__name__}:{exc}",
            })
            by_league[item.league][status] += 1
            continue
        results.append({"fixture_id": item.fixture_id, "league": item.league, "result": value})
        outcomes.append({"fixture_id": item.fixture_id, "league": item.league, "status": "PREDICTED"})
        by_league[item.league]["PREDICTED"] += 1

    return {
        "status": "PARTIAL" if any(
            x["status"] != "PREDICTED" for x in outcomes
        ) else "SUCCESS",
        "results": results,
        "fixture_outcomes": outcomes,
        "league_summary": dict(by_league),
        "global_preflight_passed": True,
    }


def run_isolated_leagues(
    items: Iterable[BatchItem],
    league_processor: Callable[[str, list[BatchItem]], dict[str, Any]],
    *,
    global_preflight: Callable[[], None],
) -> dict:
    """Process each league as an independent batch after global safety gates.

    The callback receives one league and only its ready fixtures, and must
    return {fixture_id: result}. A league-level exception or malformed/missing
    output is recorded for that league while other leagues continue. Missing
    state remains a fixture-level skip. This is a research orchestration
    contract only; callers must not connect it to production until reviewed.
    """
    global_preflight()  # Integrity/provenance/freshness gates fail closed.
    grouped: dict[str, list[BatchItem]] = defaultdict(list)
    item_list = list(items)
    for item in item_list:
        grouped[item.league].append(item)
    if not item_list:
        return {
            "status": "NO_FIXTURES",
            "results": [],
            "fixture_outcomes": [],
            "league_summary": {},
            "global_preflight_passed": True,
            "execution_scope": "RESEARCH_ONLY_LEAGUE_BATCHES",
        }

    outcomes: list[dict] = []
    results: list[dict] = []
    summary: dict[str, dict[str, int]] = {}

    for league in sorted(grouped):
        league_items = grouped[league]
        counts = {"PREDICTED": 0, "SKIPPED_DATA_GAP": 0, "FAILED_PROCESSING": 0}
        ids = [item.fixture_id for item in league_items]
        if len(ids) != len(set(ids)):
            for item in league_items:
                outcomes.append({
                    "fixture_id": item.fixture_id, "league": league,
                    "status": "FAILED_PROCESSING",
                    "reason": "DUPLICATE_FIXTURE_ID_WITHIN_LEAGUE_BATCH",
                })
                counts["FAILED_PROCESSING"] += 1
            summary[league] = counts
            continue
        ready = []
        for item in league_items:
            if not item.ready:
                outcomes.append({
                    "fixture_id": item.fixture_id, "league": league,
                    "status": "SKIPPED_DATA_GAP",
                    "reason": item.gap_reason or "PREMATCH_STATE_MISSING",
                })
                counts["SKIPPED_DATA_GAP"] += 1
            else:
                ready.append(item)

        if ready:
            try:
                batch_results = league_processor(league, ready)
                if not isinstance(batch_results, dict):
                    raise TypeError("league_processor must return a fixture_id-to-result dict")
                expected_ids = {item.fixture_id for item in ready}
                unexpected_ids = set(batch_results) - expected_ids
                if unexpected_ids:
                    raise ValueError("league_processor returned unknown fixture IDs")
                for item in ready:
                    if item.fixture_id not in batch_results:
                        outcomes.append({
                            "fixture_id": item.fixture_id, "league": league,
                            "status": "FAILED_PROCESSING",
                            "reason": "MISSING_RESULT_FROM_LEAGUE_BATCH",
                        })
                        counts["FAILED_PROCESSING"] += 1
                    else:
                        results.append({
                            "fixture_id": item.fixture_id, "league": league,
                            "result": batch_results[item.fixture_id],
                        })
                        outcomes.append({
                            "fixture_id": item.fixture_id, "league": league,
                            "status": "PREDICTED",
                        })
                        counts["PREDICTED"] += 1
            except Exception as exc:
                for item in ready:
                    outcomes.append({
                        "fixture_id": item.fixture_id, "league": league,
                        "status": "FAILED_PROCESSING",
                        "reason": f"{type(exc).__name__}:{exc}",
                    })
                    counts["FAILED_PROCESSING"] += 1
        summary[league] = counts

    failed = any(o["status"] != "PREDICTED" for o in outcomes)
    return {
        "status": "PARTIAL" if failed else "SUCCESS",
        "results": results,
        "fixture_outcomes": outcomes,
        "league_summary": summary,
        "global_preflight_passed": True,
        "execution_scope": "RESEARCH_ONLY_LEAGUE_BATCHES",
    }


def validate_market_output(
    rows: Iterable[dict],
    *,
    expected_markets: Iterable[str],
    expected_fixture_ids: Iterable[str] | None = None,
) -> dict:
    """Research-only reconciliation for fixture/market output rows.

    Checks schema-level completeness and probability bounds without changing
    or recalculating any probability. This validator is intended to sit at
    the research integration boundary after the existing predictor runs.
    """
    market_list = list(expected_markets)
    if not market_list or len(market_list) != len(set(market_list)):
        return {"status": "BLOCKED", "errors": ["EXPECTED_MARKETS_EMPTY_OR_DUPLICATED"],
                "row_count": 0, "fixture_count": 0}
    materialized = list(rows)
    expected_fixtures = None if expected_fixture_ids is None else {
        str(fixture_id).strip() for fixture_id in expected_fixture_ids
    }
    if expected_fixtures is not None and ("" in expected_fixtures or len(expected_fixtures) != len(list(expected_fixture_ids))):
        return {"status": "BLOCKED", "errors": ["EXPECTED_FIXTURE_IDS_EMPTY_OR_DUPLICATED"],
                "row_count": len(materialized), "fixture_count": 0}
    errors: list[str] = []
    required = {"fixture_id", "selection", "raw_probability"}
    for index, row in enumerate(materialized):
        missing = required - set(row)
        if missing:
            errors.append(f"ROW_{index}_MISSING_FIELDS:{','.join(sorted(missing))}")
    if errors:
        return {"status": "BLOCKED", "errors": errors,
                "row_count": len(materialized), "fixture_count": 0}

    seen: set[tuple[str, str]] = set()
    fixture_markets: dict[str, set[str]] = defaultdict(set)
    for index, row in enumerate(materialized):
        fixture_id = str(row["fixture_id"]).strip()
        market = str(row["selection"]).strip()
        if not fixture_id or not market:
            errors.append(f"ROW_{index}_EMPTY_FIXTURE_OR_MARKET")
            continue
        key = (fixture_id, market)
        if key in seen:
            errors.append(f"DUPLICATE_FIXTURE_MARKET:{fixture_id}:{market}")
        seen.add(key)
        fixture_markets[fixture_id].add(market)
        try:
            probability = float(row["raw_probability"])
        except (TypeError, ValueError):
            errors.append(f"INVALID_PROBABILITY:{fixture_id}:{market}")
            continue
        if not 0.0 <= probability <= 1.0:
            errors.append(f"PROBABILITY_OUT_OF_RANGE:{fixture_id}:{market}")
    expected = set(market_list)
    if expected_fixtures is not None:
        missing_fixtures = sorted(expected_fixtures - set(fixture_markets))
        unexpected_fixtures = sorted(set(fixture_markets) - expected_fixtures)
        for fixture_id in missing_fixtures:
            errors.append(f"MISSING_FIXTURE_OUTPUT:{fixture_id}")
        for fixture_id in unexpected_fixtures:
            errors.append(f"UNEXPECTED_FIXTURE_OUTPUT:{fixture_id}")
    for fixture_id, markets in fixture_markets.items():
        missing_markets = sorted(expected - markets)
        unexpected_markets = sorted(markets - expected)
        if missing_markets:
            errors.append(f"MISSING_MARKETS:{fixture_id}:{','.join(missing_markets)}")
        if unexpected_markets:
            errors.append(f"UNEXPECTED_MARKETS:{fixture_id}:{','.join(unexpected_markets)}")
    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "row_count": len(materialized),
        "fixture_count": len(fixture_markets),
        "expected_market_count": len(market_list),
    }
