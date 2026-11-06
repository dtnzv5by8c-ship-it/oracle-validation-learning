# Project Oracle — 50-League OMI Readiness Checkpoint

**As of:** 2026-11-06 23:42 SAST  
**Scope:** research-only downstream readiness. Exactly 50 governed leagues / 182 provider seasons / 728 endpoint tasks.

## Gate state

The acquisition queue is treated as exhausted. No new provider acquisition is initiated by this checkpoint. Downstream admission remains fail-closed and accepts only evidence that passes deterministic READY, provenance, chronology/freshness and settlement gates.

The latest validated control-plane checkpoint records 648 completed tasks and 80 quarantined/provider-blocked tasks. Task completion is not treated as feature readiness.

## Downstream readiness contract

The public branch already contains dedicated validation/readiness assets for:

- selected-50 scope and manifest validation;
- historical readiness;
- exact-ID H2H integration and backtest controls;
- league/team validation readiness;
- current fixture snapshot validation;
- prediction-input validation;
- runtime-output validation;
- result-snapshot provenance;
- prospective prediction and settlement provenance;
- xG/odds masking audit;
- team-form uncertainty and league/team DNA diagnostics;
- market-intelligence actual-signal and uncertainty diagnostics.

These assets remain research-only. They must not promote PARTIAL/BLOCKED/unvalidated evidence.

## Feature admission

Fixture identity is structurally supported but still requires exact identity/provenance evidence before production admission.

Recent form, home/away splits, H2H, goals for/against, total-goal distributions, BTTS, Over 1.5/2.5/3.5, clean sheets, failed-to-score and standings/strength remain gated by settled prior samples, chronology and explicit sample-size evidence.

xG for/against remains BLOCKED unless point-in-time source provenance and timestamps are available.

Timestamped odds remain BLOCKED unless pre-kickoff timestamp, market identity and source provenance are available.

Confidence is derived only from admitted feature coverage; it is never imputed.

Actual-result settlement requires exact fixture identity, verified final result and settlement provenance. Prediction-to-settlement backtesting requires an immutable pre-kickoff prediction, immutable probability, retained feature snapshot and verified settlement.

## Coverage accounting

The defensible upstream task-level statement remains:

- 728 governed tasks
- 648 completed
- 80 quarantined/provider-blocked
- 0 pending
- 0 missing task IDs
- 0 out-of-manifest task IDs
- 0 completed/quarantine overlap
- completed-task share: 89.01%
- blocked-task share: 10.99%

No league/season/endpoint/feature-family percentage is asserted without a validated row-level evidence set tied to the authoritative manifest identity. No missing feature is inferred from another endpoint, season, provider or proxy.

## Highest-value blockers

1. Produce deterministic row-level coverage from the validated READY evidence set.
2. Resolve any authoritative-manifest identity discrepancy before treating the evidence universe as immutable.
3. Establish point-in-time xG provenance.
4. Establish timestamped pre-kickoff odds provenance.
5. Establish immutable Oracle prediction-to-settlement pairs.
6. Keep the 80 quarantined tasks BLOCKED until their evidence gates pass.

## Minimum evidence to resolve blockers

- Row-level coverage: canonical fixture/team/league-season IDs, endpoint/task ID, source timestamp, cutoff, provenance and explicit feature state.
- xG: source record plus timestamp demonstrating availability before kickoff.
- Odds: market identity, quoted price, source and timestamp strictly before kickoff.
- Backtesting: immutable prediction timestamp/probability + exact fixture ID + feature snapshot + verified final settlement.
- Quarantined tasks: deterministic provider evidence sufficient to pass identity, chronology, completeness, provenance and settlement gates.

## Governance

No Oracle V1.6 production probabilities, thresholds, decision logic, calibration or governance are changed. Future, unsettled, PARTIAL, BLOCKED or otherwise unvalidated evidence remains excluded from production/betting admission.

## Next action

Build and test the deterministic row-level coverage matrix from READY evidence only, then report league × season × endpoint × feature-family coverage, missingness, chronology/freshness pass rates, provenance/settlement status, risk and the minimum evidence required for each blocker.
