# Master OMI Formula Input Release Gate — Automation Run 11 Re-audit

**Overall release: FAIL-CLOSED**

## Immutable baseline
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Candidate SHA-256: `f9b6e030dbe4b9eb38da785e9bc5effcf5331395e13f841102621e3bc3516fed`
- Market Intelligence: 755 x 264
- A:ET value differences: **0**
- A:ET nonblank type differences: **1,269** (canonical float vs candidate int)
- No A:ET coercion or mutation performed.

## Gate results
- Schema V2.1.1: **FAIL-CLOSED** — explicit marker absent; workbook configuration reports 1.1.0.
- Heading comments: **264/264 PASS**
- Exact FootyStats identity: **387/387 PASS**
- Last-3/Last-5: **387/387 PASS**
- GF/M & GA/M: **387/387 PASS**
- Venue metrics: **387/387 PASS**
- Team strength/LTSS: **387/387 PASS**
- Pre-match leakage: **387/387 PASS**
- Required MI coverage: **218/387 at 100%; 169/387 below 100%**
- Kickoff/date review: **38/387 governed fixtures**
- Goal-environment quarantine: **15**
- xG capture timestamps: **0/754 verified**
- Verified actuals: **31/387**

## Per-fixture release gate
- FORMULA_INPUT_STATUS READY: **0/387**
- FORMULA_INPUT_STATUS BLOCKED: **387/387**
- BACKTEST_READY YES: **0/387**
- RELEASE_DECISION PASS: **0/387**
- RELEASE_DECISION FAIL: **387/387**

## State model
- VERIFIED_PREMATCH: **0/387**
- VERIFIED_ACTUALS: **31/387**
- UNAVAILABLE/UNVERIFIED actuals: **356/387**

## Controls
Missing values were not converted to zero or estimates. Exact Fixture-ID matching only; no fuzzy matching. Implausible goal-environment values remain quarantined. Oracle V1.6 production logic was not changed. A:ET was not inserted, reordered, renamed, coerced or repaired.

## Remaining blockers
1. V2.1.1 marker is not explicitly certified.
2. Immutable A:ET native numeric-type gate remains failed closed.
3. 169 fixtures have sub-100% required MI coverage.
4. 38 fixtures have kickoff/date reconciliation failures.
5. 15 fixtures have invalid goal-environment intelligence.
6. 754 xG rows lack verified point-in-time capture timestamps.

**Final release decision: FAIL-CLOSED.**