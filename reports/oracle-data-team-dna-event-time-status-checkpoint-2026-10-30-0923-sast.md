# Oracle Data & Team DNA — Event-Time and Status Checkpoint

**Date:** 30 October 2026, 09:23 SAST  
**Branch:** research/oracle-50-league-readiness-audit  
**Source:** Private Archive QA #38, run 41014563323, artifact 12959146668  
**Archive SHA-256:** af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875

## Verified results

- 50 league groups × four seasons = 200 season rows; all 200 are INGESTED and all required season file/payload flags are present.
- Archive: 59,049 match rows and 3,366 season-scoped team records. Primary window 20 Mar 2025–20 Sep 2026: 22,291 rows and 22,291 unique provider match IDs (not canonical fixture count).
- Event-time buckets: 130 seasons intersect the primary window, 68 are historical-only and two are entirely after the window.
- The two current seasons with no primary-window rows are Australia A-League (156 rows, 16 Oct 2026–9 May 2027) and India Indian Super League (78 rows, 10 Oct 2026–17 Jan 2027). Both archive folders are present; their schedules start after the locked window.
- Current selected seasons contain 14,051 rows: 7,040 complete, 6,958 incomplete and 53 suspended. Current-season roster records sum to 841 (8–30 per league; median 16), not unique canonical teams or match samples.
- 116 incomplete-status records have past kickoff dates: 112 across 28 current seasons and 4 across 4 historical seasons. This is a manual reconciliation queue, not evidence that outcomes are settled.
- All 7,066 non-complete rows with parseable score pairs in the full archive are 0–0; the 35 such rows in the primary window are also all 0–0. Do not settle them. The 4,006 complete-status 0–0 rows are not automatically invalid.
- No complete-status rows have future kickoff dates. Archive event dates span 20 Jan 2023–6 Jun 2027.

## Freshness limitation

QA artifact created 30 Oct 2026 06:32:26 UTC. The 40-day difference between audit date and primary-window end is an event-window gap, not a provider retrieval lag. No source retrieval/update timestamps, bookmaker IDs or quote timestamps are present in the sanitized artifact; point-in-time feature validity remains unverified.

## Files added

- scripts/audit_selected50_season_event_time_readiness.py
- tests/test_selected50_season_event_time_readiness.py — eight regression tests
- docs/PROJECT_ORACLE_SEASON_EVENT_TIME_STATUS_AUDIT_2026-10-30.md
- The updated private archive QA workflow generates a JSON summary and two sanitized CSV rollups in the next QA artifact.

## Next action

Manually reconcile the 116 incomplete-status/past-kickoff records using existing archive-owner metadata or internally held authoritative records. Separately obtain source retrieval timestamps and field/status semantics. Team-market performance remains blocked until the separate identity/settlement workstream supplies canonical joins, pre-kickoff predictions and independently verified settlement labels. Do not duplicate H2H research.

## Governance

No provider/API calls or credits. No raw fixture rows or identifiers exported. No H2H holdout access. No production logic, frozen probabilities, calibration or governance changes. official_settlement_truth_verified=false; production_eligible=false.
