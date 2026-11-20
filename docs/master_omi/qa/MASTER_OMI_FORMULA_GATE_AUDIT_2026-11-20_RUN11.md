# Master OMI Formula Input Release Gate — Run 11 — 2026-11-20

## Release status

**FAIL-CLOSED — NOT RELEASE-ELIGIBLE**

Run 11 audited the current library candidate:
`Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_REPAIRED.xlsx`

A genuine configuration defect was found in the Formula Input QA release-decision layer: 340 fixtures were marked `RELEASE_DECISION=PASS` despite 324 carrying identity-review notes and 152 having MI coverage below 100%. The permanent gate prohibits PASS in either condition.

The gate was corrected without modifying Oracle V1.6 or Market Intelligence A:ET.

## Canonical integrity

- Canonical workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Candidate pre-fix SHA-256: `94fc17760c4383e3422a9bdd31c7a927bbbd9023ef23930c98f8df56302d6744`
- Candidate post-fix SHA-256: `1335b0e9dd4b37b0470df1a1b6f5c4f4e591988fd4d57fd1fe7e109c4dbf14b3`
- Market Intelligence: 755 rows × 264 columns
- A:ET semantic differences versus canonical baseline: **0**
- Governed heading comments missing: **0**
- Governed heading comment differences: **0**
- No insertion/reorder/rename of A:ET
- Oracle V1.6 production logic unchanged

## Per-fixture gate result

- Governed target fixtures: **387**
- FORMULA_INPUT_STATUS / Prediction Input Ready = YES: **340/387 (87.86%)**
- Formula-input blocked: **47/387 (12.14%)**
- RELEASE_DECISION = PASS after enforcement: **5/387 (1.29%)**
- RELEASE_DECISION = FAIL after enforcement: **382/387 (98.71%)**
- BACKTEST_READY = YES: **21/387 (5.43%)**
- Forbidden PASS + identity/coverage/kickoff/invalid-range blocker: **0**

Formula-ready requires all mandatory pre-match gates, exact identity, no leakage, and 100% required MI coverage. Backtest-ready additionally requires independently verified actuals and exact governed fixture/date identity.

## Remaining blockers

1. **38 target fixtures** have kickoff/date reconciliation failures.
2. **9 target fixtures** have invalid/implausible goal-intelligence values and remain quarantined as UNAVAILABLE/UNVERIFIED.
3. **xG point-in-time provenance remains unverified** where capture timestamps are absent; those values remain quarantined and are not formula/betting eligible.
4. **21 backtest-ready rows** have exact governed fixture/date identity and independently verified actuals; the remaining rows do not satisfy the actuals gate.
5. Missing values were not converted to zero and no estimates or guessed transformations were applied.

## Source/provenance controls

- FootyStats identity: exact Fixture-ID joins only; no silent fuzzy matching.
- Last-3/Last-5 chronology and pre-match cutoff controls remain enforced.
- PPG/GF/M/GA/M and venue metrics remain governed inputs.
- BTTS/goal intelligence remains subject to numeric-range and provenance gates.
- LTSS V1.1 remains unchanged.
- VERIFIED_PREMATCH, VERIFIED_ACTUALS and UNAVAILABLE/UNVERIFIED remain separate states.
- Implausible goal-environment values were quarantined; no divide-by-10 or other guessed repair was applied.
- Native Excel numeric-type validation remains enforced.

## Repair

Only the Formula Input QA release-decision configuration was corrected. The repaired workbook was written to the Library as:

`/Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN11_FAIL_CLOSED.xlsx`

The repair was validated against the canonical A:ET baseline with **0 differences**.

## Next state

The Master OMI release remains **FAIL-CLOSED**. Hourly QA must continue until a full re-audit reaches 100% PASS with no unresolved schema, provenance, identity, chronology, numeric, leakage, regression or formula-eligibility defects.
