# Master OMI Formula Input Release Gate — Run 11 Re-audit

Date: 2026-11-20
Repository: dtnzv5by8c-ship-it/oracle-validation-learning
Canonical baseline: Master OMI V2.1.1
Production model: Oracle V1.6 unchanged

## Release decision

**FAIL-CLOSED / NOT RELEASE-ELIGIBLE**

The current candidate was re-audited and the permanent Formula Input Release Gate was re-enforced. The candidate cannot be released.

## Immutable baseline

Canonical workbook SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`

Candidate Run 11 workbook SHA-256 before re-audit gate repair: `1335b0e9dd4b37b0470df1a1b6f5c4f4e591988fd4d57fd1fe7e109c4dbf14b3`

Re-audited fail-closed workbook SHA-256: `eb6121d128027716867ca042c1dd60ac3e9d065fe8936d11674f4f1d25801021`

## Structural gate

- Market Intelligence: 755 rows × 264 columns.
- A:ET semantic differences versus canonical baseline: **0**.
- Governed heading comments: **264/264 present**.
- A:ET was not inserted, reordered, renamed, or mutated.
- Oracle V1.6 production logic unchanged.

## Fixture/provenance gates

- Governed fixtures: **387**.
- FootyStats source status: **387/387 EXACT_FIXTURE_ID_JOIN**; no silent fuzzy matching admitted.
- Fixture IDs: **387/387 present and unique**.
- Last-3 PPG status: **387/387 PASS** in the governed QA layer.
- Last-5 PPG status: **387/387 PASS** in the governed QA layer.
- GF/M & GA/M status: **387/387 PASS** in the governed QA layer.
- Venue metrics: **387/387 PASS**.
- Team strength/LTSS gate: **387/387 PASS** in the governed QA layer.
- Pre-match leakage check: **387/387 PASS** in the governed QA layer.
- xG point-in-time provenance: **0/754 verified capture timestamps**; all unverified xG remains UNAVAILABLE/UNVERIFIED and ineligible.
- Verified actuals remain separate from pre-match inputs.

## Critical native Excel numeric-type blocker

The immutable A:ET baseline stores all 387 rows' core required pre-match PPG/GF/M/GA/M fields as **text**, not native Excel numeric values:

- Home Goals For Avg: 387/387 text
- Home Goals Against Avg: 387/387 text
- Home Points Per Game: 387/387 text
- Away Goals For Avg: 387/387 text
- Away Goals Against Avg: 387/387 text
- Away Points Per Game: 387/387 text

This is a genuine formula-input eligibility defect under the permanent native-type gate. It cannot be repaired by converting A:ET values because A:ET is immutable. The safe correction is therefore to **fail closed**, not to coerce values or mutate the canonical structure.

## Goal-environment blocker

The re-audit found **15 governed fixtures** containing implausible goal-environment values above the allowed football plausibility range, including league averages such as 16.0593, 17.8593 and 33.9185 goals.

These values were **not divided, rescaled, estimated, or otherwise guessed**. They remain quarantined as **UNAVAILABLE/UNVERIFIED** for formula eligibility.

## Per-fixture release state after re-audit

Because the immutable A:ET numeric-type gate fails for every governed fixture, the per-fixture Formula Input Gate was hardened as follows:

- FORMULA_INPUT_STATUS / Prediction Input Ready: **0/387 READY; 387/387 BLOCKED**.
- BACKTEST_READY: **0/387**.
- RELEASE_DECISION: **0/387 PASS; 387/387 FAIL**.
- No forbidden PASS + blocker combinations remain.
- Missing evidence was not converted to zero or an estimate.

The previous Run 11 state of 340/387 formula-ready is superseded by this stricter re-audit because the permanent native Excel numeric-type requirement was not previously enforced at the per-fixture eligibility layer.

## Actuals

The workbook contains 40 independently sourced actual-result rows. They remain separated from pre-match inputs. No actual is promoted to BACKTEST_READY unless exact governed fixture/date identity and all formula-input gates pass. Under this re-audit, **0/387 are backtest-ready** because formula-input eligibility is blocked by the immutable numeric-type defect.

## Fixes made

Only the Formula Input QA decision layer was changed. The workbook's Market Intelligence A:ET data was not changed. The QA layer now fails every fixture closed where the immutable required numeric fields are stored as text, and explicitly quarantines the 15 implausible goal-environment fixtures.

No Oracle V1.6 production logic was changed. No missing value was fabricated. No fuzzy identity match was introduced. No A:ET column was inserted, deleted, renamed, or reordered.

## Release status

**FAIL-CLOSED. Continue hourly checks.**

Release may only be promoted to PASS after a complete re-audit demonstrates 100% compliance with schema, immutable A:ET contract, identity, kickoff/date, chronology, provenance, native numeric types, ranges, leakage, actuals, regression and formula-eligibility gates.
