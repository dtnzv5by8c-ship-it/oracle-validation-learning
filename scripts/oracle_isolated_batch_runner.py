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
    for item in items:
        grouped[item.league].append(item)

    outcomes: list[dict] = []
    results: list[dict] = []
    summary: dict[str, dict[str, int]] = {}

    for league in sorted(grouped):
        league_items = grouped[league]
        counts = {"PREDICTED": 0, "SKIPPED_DATA_GAP": 0, "FAILED_PROCESSING": 0}
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
