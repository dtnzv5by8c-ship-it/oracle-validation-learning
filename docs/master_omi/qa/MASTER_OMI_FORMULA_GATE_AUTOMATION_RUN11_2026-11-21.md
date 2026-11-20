# Master OMI Formula Input Release Gate — Automation Run 11 Audit

**Audit date:** 2026-11-21  
**Release decision:** FAIL-CLOSED  
**Workbook:** `Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_FINAL_FAIL_CLOSED.xlsx`  
**Workbook SHA-256:** `d74a4568640c81bfd7c39dabbfd0df9086c0f65d98ecd49942fd6880041de597`

## Canonical / structural gates

- Canonical V2.1.1 schema: PASS at the workbook governance layer.
- Market Intelligence: 755 rows × 264 columns.
- A:ET nonblank value mutation detected in current candidate: none based on the persisted immutable comparison result; A:ET remains untouched.
- Governed heading definitions/comments: 264/264 present.
- Oracle V1.6 production logic: unchanged.
- Append boundary after ET: preserved.

## Formula Input QA

387 governed QA fixtures were evaluated.

- FORMULA_INPUT_STATUS=READY: 0/387
- BACKTEST_READY=YES: 0/387
- RELEASE_DECISION=PASS: 0/387
- RELEASE_DECISION=FAIL: 387/387
- Fixture Identity PASS: 16/387
- Fixture Identity FAIL: 371/387
- FootyStats exact fixture-ID join: 387/387
- Last-3 status: 387/387 PASS
- Last-5 status: 387/387 PASS
- GF/M & GA/M status: 387/387 PASS at the QA/status layer
- Venue metrics: 387/387 PASS
- Team-strength/LTSS status: 387/387 PASS
- Pre-match leakage check: 387/387 PASS

## Coverage and actuals

MI coverage across the 387 QA fixtures:
- 100%: 218
- 98.2%: 18
- 99.1%: 2
- 96.5%: 23
- 95.6%: 6
- 94.7%: 2
- 86%: 114
- 84.2%: 4

Therefore 169/387 fixtures have less than 100% required coverage and cannot pass the release gate.

Independently matched actual-result rows: 31/387. All 31 exact QA fixture/date/team keys are present in the Actual Results sheet. BACKTEST_READY remains 0/387 because the pre-match release gate is not satisfied.

## Native Excel numeric-type gate

The current workbook contains numeric-looking text in the immutable Market Intelligence range. A scan of A:ET found 17,082 numeric-looking text cells. Because A:ET is immutable, no coercion or rewriting was performed. Required pre-match numeric-type defects therefore remain release blockers.

## Kickoff/date reconciliation

The Schedule Reconciliation sheet contains explicit KICKOFF_MISMATCH / REVIEW_REQUIRED records. These are not overridden by identity matching. Any governed fixture with unresolved kickoff/date reconciliation remains FAIL.

## Goal-environment quarantine

Implausible goal-environment evidence remains quarantined as UNAVAILABLE/UNVERIFIED. No divide-by-10, rescaling, interpolation, or guessed repair was applied.

## xG provenance

The workbook's xG provenance audit records 0/754 fixture rows with a verified point-in-time capture timestamp. xG therefore remains quarantined from production formula eligibility, historical backtesting and betting eligibility.

## Missingness / leakage / identity

- Missing values are not converted to zero or estimates.
- No silent fuzzy FootyStats matching is admitted.
- VERIFIED_PREMATCH, VERIFIED_ACTUALS and UNAVAILABLE/UNVERIFIED remain separate concepts.
- Post-match leakage gate remains enforced.
- Any blocker note is incompatible with RELEASE_DECISION=PASS.

## Scope/configuration inconsistency requiring fail-closed handling

The workbook contains multiple scope counters that must not be conflated: Market Intelligence has 754 populated fixture rows, Formula Input QA governs 387 rows, while Report Metadata states a 37-row target subset. Report Metadata also states 30 verified actuals while the exact QA-to-Actual Results reconciliation yields 31. These are configuration/metadata inconsistencies, not grounds for silently changing fixture data. They remain fail-closed until reconciled.

## Final decision

**MASTER_OMI_RELEASE = FAIL-CLOSED**

No Oracle V1.6 logic was changed. No A:ET insertion, deletion, reorder, rename, coercion or value repair was performed. The release must remain blocked until every mandatory schema, identity, kickoff/date, chronology, provenance, numeric-type, range, coverage, leakage, actuals and formula-eligibility gate passes.

Continue hourly QA.
