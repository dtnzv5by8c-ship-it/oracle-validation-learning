# Master OMI Formula Input Release Gate — Run 8

Date: 2026-11-20
Repository: dtnzv5by8c-ship-it/oracle-validation-learning

## Release status

**FAIL-CLOSED / NOT RELEASE-ELIGIBLE**

The current candidate was audited against the locked V2.1.1 canonical baseline. The permanent release gate identified a configuration defect in the candidate's per-fixture QA decisions: rows carrying identity-review notes and/or sub-100% required Market Intelligence coverage were still marked PASS/Prediction Input Ready. This violated the permanent rule that mandatory blockers may never coexist with RELEASE_DECISION=PASS.

## Canonical/A:ET integrity

Canonical V2.1.1 workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Candidate before Run 8 repair SHA-256: 94fc17760c4383e3422a9bdd31c7a927bbbd9023ef23930c98f8df56302d6744
After Run 8 QA-gate repair, semantic comparison of Market Intelligence A:ET against the canonical baseline: 0 differences.
No Oracle V1.6 production logic, probability, calibration, threshold or A:ET structure was changed.
Market Intelligence dimensions: 755 rows x 264 columns.
Heading comments: 264/264.

## Permanent gate checks

- Canonical V2.1.1 schema: PASS
- A:ET immutable semantic comparison: PASS (0 differences)
- Governed heading comments: PASS (264/264)
- Exact FootyStats identity: exact-ID joins only; no fuzzy matching admitted
- Last-3 / Last-5 chronology: governed gate retained
- PPG / GF/M / GA/M denominator and cutoff controls: governed gate retained
- Venue metrics: governed gate retained
- BTTS / goal intelligence: governed gate retained
- xG: unverified point-in-time provenance remains quarantined; not formula/betting eligible
- LTSS V1.1: governed gate retained
- Source IDs / sample sizes / status / confidence / as-of: governed gate retained
- Native numeric-type scan: no numeric-looking text detected in governed EU:JD numeric cells
- Duplicate headings: three pre-existing duplicate legacy headings remain inside immutable A:ET and were not altered
- Missingness: no missing value converted to zero or estimate
- Leakage: pre-match gate retained; no post-match substitution permitted
- Actuals: independently verified actuals remain separate from pre-match inputs
- Formula/backtest eligibility: re-evaluated with strict release decision logic

## Run 8 finding

Formula Input QA contained 387 target fixtures. Before repair:
- Prediction Input Ready = YES: 340
- Release Decision = PASS: 340
- Backtest Ready = YES: 21
- 324 PASS rows carried an identity-review note.
- 152 PASS rows had MI coverage below 100%.
- 340 PASS rows carried notes, demonstrating the release-decision field was not being treated as a strict mandatory-gate output.

This was a genuine QA/configuration defect and was corrected without changing Market Intelligence A:ET or Oracle V1.6.

## Post-fix results

- Formula Input Ready = YES: 5 / 387 (1.29%)
- Formula Input Ready = NO: 382 / 387 (98.71%)
- Release Decision = PASS: 5 / 387 (1.29%)
- Release Decision = FAIL: 382 / 387 (98.71%)
- Backtest Ready = 0 / 387 in the repaired candidate because the five fully eligible pre-match rows do not have independently verified actuals.
- Forbidden PASS + blocker combinations: 0.

The 382 blocked fixtures are blocked by the permanent gate because at least one mandatory condition is unresolved, including required coverage below 100%, identity review, kickoff/date reconciliation, or invalid numeric-range evidence.

## Goal-environment quarantine

Implausible goal-environment values remain UNAVAILABLE/UNVERIFIED. No divide-by-10, rescaling or other guessed repair was applied. Any future correction must be proven by source-level transformation evidence.

## Output

Run 8 fail-closed workbook: Oracle_Master_OMI_Report_14-24_Nov_2026_FORMULA_GATE_RUN8_FAIL_CLOSED.xlsx
Workbook SHA-256: 643695bc94f318fe10bbd7e47d9781db8921896dbc0c6fb7400598b8f3c3d237

## Next action

The release must remain FAIL-CLOSED. The hourly QA continues. The next run must re-audit the repaired candidate and only promote to PASS if every mandatory schema, provenance, identity, chronology, numeric, leakage, actuals and formula-eligibility gate passes for every governed fixture.