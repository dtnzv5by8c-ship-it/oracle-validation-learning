# Master OMI Formula Input Release Gate — Automation Run 11 Re-Audit

Date: 2026-11-21
Decision: FAIL-CLOSED

## Canonical integrity
- Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED(2).xlsx
- Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Candidate workbook: Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_AUTOMATION11_CORRECTED_FAIL_CLOSED.xlsx
- Candidate SHA-256: f9b6e030dbe4b9eb38da785e9bc5effcf5331395e13f841102621e3bc3516fed
- Market Intelligence: 755 rows x 264 columns
- A:ET value integrity: 0 value differences observed in the persisted QA evidence; native-type compliance remains blocked by 1,269 canonical float/int representation differences.

## Gate results
- Governed fixtures: 387
- Exact FootyStats identity: 387/387 PASS; no fuzzy matching permitted or used.
- Last-3 PPG: 387/387 PASS
- Last-5 PPG: 387/387 PASS
- GF/M and GA/M: 387/387 PASS
- Venue metrics: 387/387 PASS
- LTSS/team-strength: 387/387 PASS
- Pre-match leakage: 387/387 PASS
- Required MI coverage: 218/387 at 100%; 169/387 below 100%
- Kickoff/date reconciliation: 38/387 blockers remain
- Implausible goal-environment records: 15 quarantined UNAVAILABLE/UNVERIFIED
- Verified actuals: 31/387 independently linked to governed fixture/date identity
- xG capture timestamps: 0/754 independently verified
- FORMULA_INPUT_STATUS READY: 0/387
- FORMULA_INPUT_STATUS BLOCKED: 387/387
- BACKTEST_READY: 0/387
- RELEASE_DECISION PASS: 0/387
- RELEASE_DECISION FAIL: 387/387

## Schema / provenance controls
- V2.1.1 explicit schema marker: NOT CERTIFIED; workbook configuration reports 1.1.0, so gate fails closed.
- Governed heading comments: 264/264 retained.
- Missingness: no missing value converted to zero or estimated.
- Goal anomalies: no guessing, dividing, rescaling, interpolation, or repair without source proof.
- Actuals remain separate from VERIFIED_PREMATCH; unmatched actuals are not injected into Market Intelligence.
- Oracle V1.6 production logic unchanged.
- No A:ET insertion, reordering, renaming, coercion, or value repair performed.

## Release rule
Any identity defect, kickoff/date defect, invalid numeric range, sub-100% required coverage, provenance defect, leakage defect, schema defect, or immutable A:ET native-type defect forces RELEASE_DECISION=FAIL. Overall Master OMI release therefore remains FAIL-CLOSED.
