# Master OMI Formula Input Release Gate — Automation Run 11

Audit timestamp: 2026-11-21T10:51:16Z

## Release
**FAIL-CLOSED**

## Canonical baseline
- Baseline workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED(2).xlsx
- Canonical SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Candidate SHA-256: f9b6e030dbe4b9eb38da785e9bc5effcf5331395e13f841102621e3bc3516fed
- Market Intelligence: 755 x 264
- A:ET value differences: 21,774
- A:ET type differences: 21,774
- Finding: candidate A:ET representation differs from immutable canonical baseline; fail closed. No A:ET repair/coercion performed.

## QA
- Governed Formula QA fixtures: 387
- Exact FootyStats identity: 387/387 PASS
- Last-3 PPG: 387/387 PASS
- Last-5 PPG: 387/387 PASS
- GF/M & GA/M: 387/387 PASS
- Venue metrics: 387/387 PASS
- Team strength/LTSS: 387/387 PASS
- Pre-match leakage: 387/387 PASS
- MI coverage 100%: 218/387
- MI coverage <100%: 169/387
- Kickoff/date review: 38/387
- Implausible goal-environment records: 15 quarantined
- Verified actuals: 31/387
- Actual Results populated: 40; exact reconciled verified actuals: 31
- xG point-in-time capture timestamps: 0/754
- Formula Input READY: 0/387
- Formula Input BLOCKED: 387/387
- BACKTEST_READY: 0/387
- RELEASE_DECISION PASS: 0/387
- RELEASE_DECISION FAIL: 387/387

## Governance
- Market Intelligence governed headings with comments: 204/204 header cells
- Exact identity only; no fuzzy matching
- Missing values not converted to zero or estimates
- VERIFIED_PREMATCH, VERIFIED_ACTUALS and UNAVAILABLE/UNVERIFIED kept separate
- No post-match evidence admitted into pre-match inputs
- Oracle V1.6 production logic unchanged
- No A:ET insertion, deletion, reordering, renaming or repair

## Hard blockers
1. Immutable A:ET comparison fails.
2. V2.1.1 explicit schema marker is not independently certifiable; workbook configuration reports 1.1.0.
3. Required MI coverage below 100% for 169 fixtures.
4. Kickoff/date reconciliation remains unresolved for 38 governed Formula QA fixtures.
5. 15 goal-environment records are implausible and quarantined as UNAVAILABLE/UNVERIFIED; no guessed rescaling/division.
6. xG provenance lacks independently verified point-in-time capture timestamps for all 754 rows.
7. Native Excel numeric-type requirements cannot be repaired inside immutable A:ET.

## Fixture decisions
All 387 governed fixtures have:
- FORMULA_INPUT_STATUS = BLOCKED
- BACKTEST_READY = NO
- RELEASE_DECISION = FAIL

No blocker note is permitted to coexist with PASS.

## Final
The Master OMI release remains FAIL-CLOSED. Continue hourly QA. Do not release until every mandatory schema, immutable A:ET, provenance, identity, kickoff/date, numeric-type, coverage, leakage and actuals gate passes.
