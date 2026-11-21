# Master OMI Formula Input Release Gate — QA Status

Date: 2026-11-21
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Canonical baseline: Master OMI V2.1.1
Production model: Oracle V1.6 unchanged

## Permanent release-gate policy

A Master OMI release is PASS only when every governed fixture passes the canonical V2.1.1 schema, A:ET immutable contract, heading definitions/comments, exact fixture identity, kickoff/date reconciliation, chronology, provenance, leakage, native Excel numeric types, numeric ranges, duplicates, missingness, actuals reconciliation and formula-eligibility gates.

Missing evidence remains UNAVAILABLE/UNVERIFIED and is never converted to zero or an estimate.

- FORMULA_INPUT_STATUS = READY only when all required pre-match inputs pass and no leakage/provenance/identity/kickoff-date defect exists.
- BACKTEST_READY additionally requires independently verified actuals and exact governed fixture/date identity.
- RELEASE_DECISION = FAIL unless every mandatory gate for that fixture passes.
- Notes such as identity review, kickoff/date review, invalid numeric ranges or sub-100% required coverage may never coexist with PASS.
- VERIFIED_PREMATCH, VERIFIED_ACTUALS and UNAVAILABLE/UNVERIFIED remain separate.

## 2026-11-21 immutable re-audit

**Release status: FAIL-CLOSED / NOT RELEASE-ELIGIBLE.**

Canonical reference workbook:
`Oracle_Master_OMI_Report_FINAL_14Nov2026_FOOTYSTATS_APPENDED_ET_FIXED.xlsx`

Canonical reference workbook SHA-256:
`84f557fdc297169a47a66458ba6ea9421ae94d003f71e7b55ccc96fbcd1761f1`

Current audited candidate:
`Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_FINAL_FAIL_CLOSED.xlsx`

Current candidate SHA-256:
`d74a4568640c81bfd7c39dabbfd0df9086c0f65d98ecd49942fd6880041de597`

### Critical immutable A:ET finding

Direct A:ET comparison detected **5,760 cell-value differences across 9 A:ET headings**.

Examples:
- AE2 H2H Avg Total Goals: 3 vs 3.2
- BJ2 H2H Last-5: dated score history vs L/D/W encoding
- BK2 H2H N: 3 vs 5
- DJ2 H2H Available History Window: 2025-04-18 to 2026-05-10 vs 2025-03-21 to 2026-09-20
- DK2 H2H Current Home Avg Goals: 2.333 vs blank
- DL2 H2H Current Away Avg Goals: 0.667 vs blank
- DM2 H2H Avg Total Goals (2Y Available): 3 vs blank
- DN2 H2H Sample N (2Y Available): 3 vs 0
- DO2 H2H Goal Trend: INSUFFICIENT_SAMPLE vs NO VERIFIED H2H

This is a hard release-gate failure. **No A:ET repair or coercion was performed.**

### Structural / identity gates

- Candidate Market Intelligence: **755 × 264**
- Canonical reference Market Intelligence: **755 × 239**
- Candidate governed header comments: **264/264**
- Duplicate headings retained: H2H Avg Total Goals; Historical Accuracy Status; A+ Setup Status
- Formula Input QA governed fixtures: **387**
- FootyStats identity: **387/387 EXACT_FIXTURE_ID_JOIN**
- Fixture Identity: **16 PASS / 371 FAIL**
- Last-3 PPG: **387/387 PASS**
- Last-5 PPG: **387/387 PASS**
- GF/M & GA/M status: **387/387 PASS at QA/status layer**
- Venue Metrics: **387/387 PASS**
- Team Strength/LTSS: **387/387 PASS**
- Pre-match leakage: **387/387 PASS**

### Coverage

- 100% required MI coverage: **218/387**
- Below 100%: **169/387**

### Kickoff/date

- Upcoming fixture rows: **754**
- Exact archive fixture joins: **754**
- Kickoff matches: **687**
- Kickoff mismatches requiring manual review: **67**
- Automatic correction: **none**

### Native Excel numeric types

The current candidate contains **17,082 numeric-looking text cells within A:ET**. Required numeric pre-match fields stored as text are not coerced because A:ET is immutable. Native numeric type failure therefore remains a hard blocker.

### Goal environment

Historical Goal Context contains implausible values, including:
- League Avg Home Goals: **16.059259...**
- League Avg Away Goals: **17.859259...**
- League Avg Total Goals: **33.918518...**
- Pre-Fixture League Goal Avg: **33.918518...**

These remain **UNAVAILABLE/UNVERIFIED**. No divide-by-10, rescaling, interpolation, estimate or guessed repair was applied.

### xG provenance

- Numeric pre-match-labelled xG candidates: **754**
- Verified point-in-time capture timestamps: **0/754**
- Production-eligible xG: **0**
- Betting-eligible xG: **0**

### Actuals / backtesting

- Verified Actuals in Formula Input QA: **31/387**
- BACKTEST_READY: **0/387**

### Final per-fixture decisions

- FORMULA_INPUT_STATUS READY: **0/387**
- FORMULA_INPUT_STATUS BLOCKED: **387/387**
- BACKTEST_READY YES: **0/387**
- RELEASE_DECISION PASS: **0/387**
- RELEASE_DECISION FAIL: **387/387**
- Forbidden PASS + blocker combinations: **0**

### Production-model protection

- Oracle V1.6: unchanged
- A:ET: not repaired, reordered, inserted, renamed or coerced
- Missing values: not converted to zero or estimates
- Fuzzy FootyStats matching: not admitted
- Implausible goal-environment evidence: quarantined

### Evidence

Immutable re-audit:
`docs/master_omi/qa/MASTER_OMI_FORMULA_GATE_IMMUTABLE_REAUDIT_2026-11-21_RUN11.md`

Commit:
`98ec6ac414527316f8f58535876729c8c6c906f7`

The current candidate must be rejected until the controlled workbook-generation process produces an A:ET-identical candidate from the canonical baseline. Then rerun the complete release gate from scratch.

**Release remains FAIL-CLOSED.**


## Automation Run 11 final audit — 2026-11-21

Current candidate SHA-256: `d74a4568640c81bfd7c39dabbfd0df9086c0f65d98ecd49942fd6880041de597`

Final decision: **FAIL-CLOSED / NOT RELEASE-ELIGIBLE**.

- Formula Input Ready: **0/387**
- Backtest Ready: **0/387**
- Release Decision PASS: **0/387**
- Release Decision FAIL: **387/387**
- Exact FootyStats joins: **387/387**
- MI coverage 100%: **218/387**
- MI coverage below 100%: **169/387**
- Verified actuals: **31/387**
- Kickoff/date reconciliation requiring review: **67/754**
- xG point-in-time provenance verified: **0/754**
- Market Intelligence: **755 x 264**
- Header comments: **264/264**
- Duplicate exact fixture keys: **0**

The current candidate is not certifiable as A:ET-identical to the canonical foundation. A:ET remains immutable; no repair or coercion was performed. Required numeric fields stored as text remain blocked. Implausible goal-environment values remain UNAVAILABLE/UNVERIFIED. Missing values remain distinct from zero and estimates.

Run evidence: `docs/master_omi/qa/MASTER_OMI_FORMULA_GATE_AUTOMATION_RUN11_2026-11-21_FINAL.md`
Commit: `2adaa195d2485e0776fe8add2441ea09a0fc5f46`
