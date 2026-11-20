# Master OMI Formula Input Release Gate — Automation Run 11

Audit timestamp: 2026-11-20T22:43:28+02:00

## Release decision
FAIL-CLOSED — NOT RELEASE ELIGIBLE.

## Canonical / immutable controls
- Canonical V2.1.1 workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Current candidate workbook SHA-256: eb6121d128027716867ca042c1dd60ac3e9d065fe8936d11674f4f1d25801021
- Market Intelligence: 755 x 264
- A:ET values: no value differences against the locked canonical baseline.
- A:ET non-value data-type differences: 140 blank cells only (inlineStr vs empty); no nonblank A:ET value mutation detected.
- Governed heading definitions/comments: 264/264 present.
- Oracle V1.6 production logic: unchanged.
- A:ET not inserted, reordered, renamed, or value-mutated.

## Governed fixture QA
- Governed fixtures: 387
- Fixture identity: 387/387 PASS
- FootyStats identity: 387/387 EXACT_FIXTURE_ID_JOIN
- Last-3 PPG: 387/387 PASS
- Last-5 PPG: 387/387 PASS
- GF/M & GA/M status: 387/387 PASS
- Venue metrics status: 387/387 PASS
- Team-strength/LTSS status: 387/387 PASS
- Pre-match leakage check: 387/387 PASS
- MI coverage = 100%: 218/387
- MI coverage <100%: 169/387
- Independently verified actuals: 31/387
- BACKTEST_READY: 0/387
- FORMULA_INPUT_STATUS/Prediction Input Ready: 0/387
- RELEASE_DECISION: 0 PASS / 387 FAIL
- Forbidden PASS + blocker combinations: 0

## Mandatory blockers
1. Native Excel numeric-type gate: all 387 governed fixtures have required pre-match PPG/GF/M/GA/M display fields in immutable A:ET stored as text. Because A:ET is immutable, these cells were not coerced or rewritten.
2. Kickoff/date reconciliation: 38 governed fixtures remain failed.
3. Implausible goal-environment evidence: 24 governed fixtures contain invalid goal-intelligence range evidence, including repeated league-total-goal values of 33.9185 and 19.5668. These remain UNAVAILABLE/UNVERIFIED; no divide-by-10, rescaling, estimate, or other guessed repair was applied.
4. Required MI coverage below 100%: 169 governed fixtures.
5. xG temporal provenance: 0/754 rows have verified capture timestamps; xG remains QUARANTINED_RESEARCH_AUDIT_ONLY and ineligible for production formula use.
6. Backtesting additionally requires independently verified actuals and exact governed fixture/date identity; current result is 0/387.

## State discipline
VERIFIED_PREMATCH, VERIFIED_ACTUALS and UNAVAILABLE/UNVERIFIED remain separate. Missing values are never converted to zero or estimated.

## Per-fixture status manifest
The canonical per-fixture status sheet is Formula Input QA in the audited workbook. Its deterministic manifest SHA-256 is:
56aa21d2965f7bfca4d1d61cd40081cb7ed54a0302b8c351d49aaa73af640198

## Final
Release remains FAIL-CLOSED. Continue hourly checks. Do not release until every mandatory governed schema, identity, chronology, provenance, numeric-type/range, leakage, actuals and formula-eligibility gate passes.
