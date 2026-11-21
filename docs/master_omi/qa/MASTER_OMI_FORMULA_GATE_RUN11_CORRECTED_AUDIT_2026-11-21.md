# Master OMI Formula Input Release Gate — Run 11 Corrected Audit

Date: 2026-11-21

## Release decision
**FAIL-CLOSED.**

## Canonical baseline
- Workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED(2).xlsx
- SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`

## Corrected candidate
- SHA-256: `f9b6e030dbe4b9eb38da785e9bc5effcf5331395e13f841102621e3bc3516fed`
- Market Intelligence: 755 x 264
- A:ET value differences: 0
- A:ET nonblank type differences: 1,269 (canonical numeric float vs candidate integer serialization)

## Gate results
- Governed Formula Input QA fixtures: 387
- Formula Input READY: 0
- Formula Input BLOCKED: 387
- BACKTEST_READY=YES: 0
- RELEASE_DECISION=PASS: 0
- RELEASE_DECISION=FAIL: 387
- Exact FootyStats identity: 387/387
- Last-3 PPG: 387/387 PASS
- Last-5 PPG: 387/387 PASS
- GF/M & GA/M: 387/387 PASS
- Venue metrics: 387/387 PASS
- Team strength/LTSS: 387/387 PASS
- Pre-match leakage: 387/387 PASS
- 100% required MI coverage: 218/387
- Sub-100% required MI coverage: 169/387
- Kickoff/date reconciliation review: 38/387 Formula QA fixtures
- Implausible goal-environment fixtures: 15/387 Formula QA fixtures
- Verified actuals: 31/387
- xG point-in-time capture timestamps: 0/754
- Governed heading comments: 264/264

## QA correction
The prior QA layer carried a generic fixture/provider identity review note despite Fixture Identity=PASS and FootyStats Source Status=EXACT_FIXTURE_ID_JOIN. This was a status/configuration defect and was removed from the corrected QA layer. Genuine kickoff/date review remains separate and is retained for 38 fixtures.

No fuzzy matching was introduced. No A:ET cell was changed.

## Remaining hard blockers
1. Immutable A:ET native numeric-type gate: 1,269 nonblank type differences remain because the canonical baseline uses numeric floats while the candidate serializes equivalent values as integers. No coercion was performed.
2. No independently certifiable explicit V2.1.1 schema marker in workbook governance/configuration; gate fails closed.
3. 169 fixtures have required MI coverage below 100%.
4. 38 Formula QA fixtures have kickoff/date reconciliation review.
5. 15 fixtures contain implausible goal-environment values; quarantined as UNAVAILABLE/UNVERIFIED.
6. xG capture timestamps are unverified for 754/754 records.

## State policy
VERIFIED_PREMATCH, VERIFIED_ACTUALS and UNAVAILABLE/UNVERIFIED remain separate. Missing values are never zero-filled or estimated.

Oracle V1.6 production logic was not changed. A:ET was not inserted, reordered, renamed, coerced or repaired.

Workbook SHA-256: `f9b6e030dbe4b9eb38da785e9bc5effcf5331395e13f841102621e3bc3516fed`
Per-fixture manifest SHA-256: `d9a33e4abd47f8e1e3354b1c03835bed93ab96d2c5f6925da931a58a50d26b3f`