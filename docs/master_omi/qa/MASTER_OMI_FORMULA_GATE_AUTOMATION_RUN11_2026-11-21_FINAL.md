# Master OMI Formula Input Release Gate — Run 11 Audit (2026-11-21)

## Release decision
**FAIL-CLOSED / NOT RELEASE-ELIGIBLE**

No governed fixture is formula-ready and no governed fixture is backtest-ready.

## Canonical controls
- Canonical V2.1.1 foundation: `Oracle_Master_OMI_Report_FINAL_14Nov2026_FOOTYSTATS_APPENDED_ET_FIXED.xlsx`
- Canonical foundation SHA-256: `84f557fdc297169a47a66458ba6ea9421ae94d003f71e7b55ccc96fbcd1761f1`
- Current candidate: `Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_FINAL_FAIL_CLOSED.xlsx`
- Current candidate SHA-256: `d74a4568640c81bfd7c39dabbfd0df9086c0f65d98ecd49942fd6880041de597`
- Market Intelligence dimensions: 755 x 264
- A:ET protected span: columns A:ET
- Header comments: 264/264
- A:ET is immutable; no A:ET repair, coercion, insertion, deletion, reordering or renaming was performed.

## Formula Input QA
- Governed QA rows: 387
- Formula Input Ready: 0/387
- Backtest Ready: 0/387
- Release Decision PASS: 0/387
- Release Decision FAIL: 387/387
- Forbidden PASS + blocker combinations: 0
- Exact FootyStats fixture-ID joins: 387/387
- Last-3 status: 387/387 PASS
- Last-5 status: 387/387 PASS
- GF/M & GA/M status: 387/387 PASS at QA/status layer
- Venue metrics status: 387/387 PASS
- Team strength/LTSS status: 387/387 PASS
- Pre-match leakage check: 387/387 PASS
- Required MI coverage = 100%: 218/387
- Required MI coverage <100%: 169/387
- Independently verified actuals: 31/387

## Mandatory blockers
1. **Immutable A:ET baseline cannot be certified as identical for this candidate.** The canonical SHA-256 is fixed at `84f557fd...`; the candidate file SHA-256 is different. The GitHub-persisted immutable re-audit also records material A:ET differences in the candidate. Fail closed.
2. **Native Excel numeric-type gate:** required schema-defined numeric inputs include text states/numeric-looking text in the immutable A:ET layer. No coercion is permitted because A:ET is locked.
3. **Coverage:** 169/387 governed QA fixtures are below 100% required Market Intelligence coverage.
4. **Fixture/provider identity review:** Formula Input QA has 371/387 fixtures marked identity FAIL; no silent fuzzy matching is admitted.
5. **Kickoff/date reconciliation:** Schedule Reconciliation contains 67 REVIEW_REQUIRED records; these are not overridden.
6. **Goal-environment integrity:** implausible goal-environment values remain UNAVAILABLE/UNVERIFIED; no guessed divide-by-10 or rescaling is applied.
7. **xG provenance:** 0/754 xG evidence rows have verified point-in-time capture timestamps; xG remains quarantined.
8. **Backtest eligibility:** 31 exact actuals matches exist, but none can become BACKTEST_READY because the pre-match gate is not satisfied.

## State model enforced
- VERIFIED_PREMATCH
- VERIFIED_ACTUALS
- UNAVAILABLE/UNVERIFIED

Missing values are never converted to zero or estimates.

## Structural checks
- Market Intelligence populated rows: 754
- Duplicate exact fixture keys in Market Intelligence: 0
- Duplicate exact fixture/date/team keys in Actual Results: 0
- All 264 Market Intelligence headings have required comments.
- No Oracle V1.6 production logic was changed.

## Outcome
**MASTER OMI RELEASE = FAIL-CLOSED**

The correct remediation is upstream: produce a candidate from the locked canonical A:ET baseline and resolve genuine identity/kickoff, coverage, numeric-type, goal-environment and xG provenance defects. Do not patch A:ET or guess transformations.

