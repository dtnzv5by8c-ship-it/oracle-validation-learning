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
