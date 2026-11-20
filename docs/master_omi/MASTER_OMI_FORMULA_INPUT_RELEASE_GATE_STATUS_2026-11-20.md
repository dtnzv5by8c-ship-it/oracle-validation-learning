# Master OMI Formula Input Release Gate — QA Status

Date: 2026-11-20
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Canonical baseline: Master OMI V2.1.1
Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
Production model: Oracle V1.6 unchanged

## Permanent release-gate policy

A Master OMI release is PASS only when every governed fixture passes the canonical V2.1.1 schema, A:ET immutable contract, heading definitions/comments, exact fixture identity, kickoff/date reconciliation, chronology, provenance, leakage, native Excel numeric types, numeric ranges, duplicates, missingness, actuals reconciliation and formula-eligibility gates.

Missing evidence remains UNAVAILABLE/UNVERIFIED and is never converted to zero or an estimate.

- FORMULA_INPUT_STATUS = READY only when all required pre-match inputs pass and no leakage/provenance/identity/kickoff-date defect exists.
- BACKTEST_READY additionally requires independently verified actuals and exact governed fixture/date identity.
- RELEASE_DECISION = FAIL unless every mandatory gate for that fixture passes.
- Notes such as identity review, kickoff/date review, invalid numeric ranges or sub-100% required coverage may never coexist with PASS.
- VERIFIED_PREMATCH, VERIFIED_ACTUALS and UNAVAILABLE/UNVERIFIED remain separate.

## Automation Run 11 — current re-audit

**Release status: FAIL-CLOSED / NOT RELEASE-ELIGIBLE.**

Canonical SHA-256:
`9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`

Current audited candidate SHA-256:
`eb6121d128027716867ca042c1dd60ac3e9d065fe8936d11674f4f1d25801021`

Per-fixture status manifest SHA-256:
`56aa21d2965f7bfca4d1d61cd40081cb7ed54a0302b8c351d49aaa73af640198`

### Structural / identity gates

- Market Intelligence: **755 × 264**
- A:ET nonblank values versus canonical baseline: **0 value differences**
- A:ET non-value type differences: **140 blank cells only**; no nonblank A:ET value mutation detected
- Governed heading definitions/comments: **264/264**
- Fixture identity: **387/387 PASS**
- FootyStats identity: **387/387 EXACT_FIXTURE_ID_JOIN**
- Last-3 chronology/status: **387/387 PASS**
- Last-5 chronology/status: **387/387 PASS**
- GF/M & GA/M status: **387/387 PASS**
- Venue metrics: **387/387 PASS**
- LTSS/team-strength: **387/387 PASS**
- Pre-match leakage: **387/387 PASS**
- Oracle V1.6: **unchanged**
- A:ET: **no insertion, reorder, rename or nonblank value mutation**

### Mandatory blockers

#### 1. Native Excel numeric-type gate — BLOCKER

The immutable A:ET baseline stores the core required pre-match PPG/GF/M/GA/M display inputs as text. Because A:ET is immutable, these cells were not coerced or rewritten.

This gate therefore fails closed for the governed formula-input layer.

#### 2. Kickoff/date reconciliation

**38/387** governed fixtures fail kickoff/date reconciliation.

#### 3. Required MI coverage

**169/387** governed fixtures have required MI coverage below 100%.
**218/387** have 100% coverage.

#### 4. Implausible goal-environment values

**24/387** governed fixtures contain invalid goal-environment evidence.

Examples include repeated league-total-goal values of:
- **33.9185**
- **19.5668**

These remain **UNAVAILABLE/UNVERIFIED**.

No divide-by-10, rescaling, estimate or guessed transformation was applied.

#### 5. xG provenance

**0/754** rows have verified point-in-time capture timestamps. xG remains quarantined and is not eligible for production formula use.

#### 6. Verified actuals / backtesting

**31/387** governed fixtures have independently verified actuals in the current QA layer.

Nevertheless:
- BACKTEST_READY = **0/387**
- because the formula-input gate is not fully passed.

### Final per-fixture decisions

- FORMULA_INPUT_STATUS / Prediction Input Ready: **0/387 READY; 387/387 BLOCKED**
- BACKTEST_READY: **0/387**
- RELEASE_DECISION: **0/387 PASS; 387/387 FAIL**
- Forbidden PASS + blocker combinations: **0**

### Evidence

Current automation audit:
`docs/master_omi/qa/MASTER_OMI_FORMULA_GATE_AUDIT_2026-11-20_AUTOMATION_RUN11.md`

The per-fixture status table is retained in the audited workbook's **Formula Input QA** sheet and represented by the manifest hash above.

**Release remains FAIL-CLOSED. Continue hourly checks. Do not promote to PASS until a complete audit reaches 100% compliance with every mandatory governed gate.**


## Run 11 final re-audit — 2026-11-21

**Release remains FAIL-CLOSED.** Current audited workbook SHA-256: `d74a4568640c81bfd7c39dabbfd0df9086c0f65d98ecd49942fd6880041de597`. Per-fixture manifest SHA-256: `e38d5070b951e8b18cd8b31563c4b40db078825af6a5f0e8464e4297b9ef219e`. FORMULA_INPUT_STATUS READY 0/387; BACKTEST_READY 0/387; RELEASE_DECISION PASS 0/387, FAIL 387/387. 371 Formula Input QA rows with identity-review notes were corrected from Fixture Identity=PASS to FAIL; no A:ET or Oracle V1.6 changes were made. Remaining blockers: 38 kickoff/date reconciliation failures, 169 fixtures below 100% required MI coverage, 24 implausible goal-environment fixtures quarantined as UNAVAILABLE/UNVERIFIED, and 0/754 xG point-in-time provenance timestamps verified. Continue hourly fail-closed checks.
