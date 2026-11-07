# Project Oracle — Evidence/Backtest Control Checkpoint

Date: 2026-11-07 09:55 SAST
Branch: `research/oracle-50-league-readiness-audit`

## Major milestone
The current private settlement ledger was re-read from `oracle-football-data/main` after the controlled provenance-only code correction `3fefb69ef0f72941ee0fdc0e0a571a2a62e175e7`.

The correction is present in the private builder but has **not yet been exercised by a new prospective-learning cycle**. The live settlement ledger still contains settled challenger rows with blank `settlement_source` / `event_truth_source` fields. Therefore settlement provenance remains **BLOCKED for production admission**.

## Current evidence
- Current canonical settlement ledger contains 25 SETTLED CHALLENGER rows across 5 fixtures.
- The rows contain final scores and scoring components, but the live persisted rows inspected still have blank settlement/event-truth provenance.
- The corrected builder now emits:
  - `settlement_source=FotMob governed current-match feed: database/current_matches.csv`
  - `event_truth_source=NOT_REQUIRED_FINAL_SCORE_MARKETS`
- The correction is research/evidence-control only and does not alter Oracle V1.6 logic, probabilities, thresholds, calibration or governance.
- Existing 25-row shadow metrics remain research-only and below the prospective 100-row / 8-day gate.
- No production probability or production settlement evidence has been promoted.

## Highest-value remaining gate
Exercise the already-corrected prospective settlement builder on private `main`, then re-audit the resulting immutable prediction -> fixture -> pre-kickoff feature snapshot -> verified settlement chain.

This is now a **gated manual action**: the available GitHub connector can inspect and rerun existing workflow jobs but cannot dispatch the required new `workflow_dispatch` cycle. No new provider/API acquisition is justified.

## Safety
- Do not rerun exhausted acquisition.
- Do not repeat HTTP-417 recovery.
- Do not use public provider transport.
- Do not infer historical results.
- Keep 80 provider-blocked tasks quarantined.
- Keep `production_eligible=false` and `betting_eligible=false`.

## Downstream after the cycle
If provenance is correctly emitted, re-score only admissible settled rows, then apply sample-size and chronology gates before any market/league/risk-band analysis. Challenger/shadow evidence remains separate from Oracle V1.6 production evidence.
