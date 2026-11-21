# Master OMI Formula Input Release Gate — Automation Run 11 Re-audit
Date: 2026-11-21

## Final decision
FAIL-CLOSED. No Master OMI release is authorised.

## Canonical integrity
- Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED(2).xlsx
- Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Candidate SHA-256: f9b6e030dbe4b9eb38da785e9bc5effcf5331395e13f841102621e3bc3516fed
- Market Intelligence: 755 x 264
- Direct A:ET value differences: 0
- A:ET nonblank type differences: 249 (equivalent numeric serialization differences only)
- A:ET values were not modified, coerced, reordered, inserted, deleted or renamed.

## Gate results
- Governed Formula Input QA fixtures: 387
- Exact FootyStats fixture identity: 387/387 PASS
- Last-3 PPG: 387/387 PASS
- Last-5 PPG: 387/387 PASS
- GF/M & GA/M: 387/387 PASS
- Venue metrics: 387/387 PASS
- Team strength/LTSS: 387/387 PASS
- Pre-match leakage: 387/387 PASS
- Required MI coverage at 100%: 218/387
- Required MI coverage below 100%: 169/387
- Kickoff/date reconciliation blockers: 38/387 governed QA fixtures
- Implausible goal-environment blockers: 15/387
- Independently verified actuals: 31/387
- xG rows with verified point-in-time capture timestamp: 0/754
- Formula-ready: 0/387
- Backtest-ready: 0/387
- Release PASS: 0/387
- Release FAIL: 387/387

## Governance
- Market Intelligence heading comments: 264/264
- QA fixture-key duplicates: 0
- Missing values were not converted to zero or estimates.
- Exact identity matching only; no fuzzy matching.
- Goal-environment anomalies remain UNAVAILABLE/UNVERIFIED; no guessed rescaling/division was applied.
- Actuals remain separate from pre-match state.
- Oracle V1.6 production logic unchanged.

## Schema blocker
Report Configuration currently exposes configuration_version=1.1.0. An explicit independently certifiable V2.1.1 schema marker is not present. The gate therefore fails closed rather than inferring V2.1.1.

## Numeric-type blocker
The mandatory Home/Away Goals For Avg and Goals Against Avg fields in A:ET are stored as text (387/387 for each field). They were not coerced because A:ET is immutable. PPG fields are native numeric, but the GF/M and GA/M fields remain a mandatory type blocker.

## Actuals
Actual Results contains 40 populated rows. Formula Input QA reconciles 31 independently verified actuals to governed fixtures. No row is BACKTEST_READY because the full pre-match gate is not satisfied.

## Action
No workbook repair was applied because all remaining defects require upstream extraction/configuration/provenance correction or authoritative reconciliation. The permanent gate remains FAIL-CLOSED.
