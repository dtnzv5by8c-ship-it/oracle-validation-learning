# Master OMI Formula Input Release Gate — Automation Run 11 Strict Re-audit

**Release decision: FAIL-CLOSED**

## Current candidate
- Workbook: `Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_STRICT_FAIL_CLOSED.xlsx`
- Candidate SHA-256: `22976945971c2f7d5e88a20f0c7302dd759cb60ce8cb76ee0085d5b942f245e0`
- Canonical baseline: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`

## Immutable A:ET re-audit
Direct comparison of the current candidate Market Intelligence A:ET against the canonical workbook found **21,774 cell-level value/representation differences** and **23,043 nonblank type differences**. Examples include canonical numeric floats versus candidate integers and canonical numeric strings versus candidate floats. This is treated as an immutable-range mutation/serialization defect and fails closed. No A:ET coercion or repair was performed.

## Governance
- Market Intelligence: 755 x 264
- Header comments: 264/264
- Exact FootyStats identity: 387/387 according to the governed QA layer; no fuzzy matching admitted.
- Required MI coverage below 100%: 169/387.
- Kickoff/date review: 67 schedule rows.
- xG point-in-time capture timestamps: 0/754 verified.
- Implausible goal-environment records: 15 quarantined as UNAVAILABLE/UNVERIFIED.
- Verified actuals: 31/387 exact governed links.
- Formula input readiness: FAIL-CLOSED; the current workbook's embedded gate evidence is not accepted as release authority because the immutable A:ET comparison fails.
- Backtest readiness: 0/387 accepted.
- Overall release: FAIL-CLOSED.

## Required state model
`VERIFIED_PREMATCH`, `VERIFIED_ACTUALS`, and `UNAVAILABLE/UNVERIFIED` remain separate. Missing values are not converted to zero or estimates. Post-match evidence is not admitted into pre-match inputs.

## Scope/schema
The workbook does not expose an independently certifiable explicit V2.1.1 schema-version marker. Schema certification therefore remains FAIL-CLOSED rather than inferred.

## Production protection
Oracle V1.6 production logic was not changed. No A:ET insertion, deletion, reordering, renaming, coercion, or repair was performed.

## Release rule
No fixture may be released with `RELEASE_DECISION=PASS` if any mandatory gate fails or any blocker note remains. Overall Master OMI release remains FAIL-CLOSED until a candidate is regenerated from the immutable canonical A:ET baseline and the complete audit passes.