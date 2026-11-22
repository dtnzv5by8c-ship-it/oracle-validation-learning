# Master OMI MI QA — Automation Run 11 — 2026-11-22 16:34 SAST

## Final release
**FAIL-CLOSED**

## Scope
- Canonical candidate audited: `Oracle_Master_OMI_RUN11_EXHAUSTIVE_QA_FAIL_CLOSED_2026-11-22_1311SAST.xlsx`
- Market Intelligence: 755 rows × 264 columns
- Governed fixtures: 754
- Every governed fixture row and every MI column audited.
- Permanent V2.1.1 Formula Input Release Gate enforced.

## Workbook / immutable baseline
- Candidate SHA-256: `5a868b00f8eed176c878bc04faa7e42bd6962cef10db9ec085fd4616bf9cfd3c`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- A:ET value differences: **0**
- A:ET native-type differences: **140**, all blank-cell serialization differences
- A:ET mutation: **NONE**
- Oracle V1.6: **UNCHANGED**

## Structural / identity gates
- V2.1.1 configuration: **2.1.1**
- Heading comments: **264/264**
- Fixture IDs populated: **754/754**
- Duplicate Fixture IDs: **0**
- Exact FootyStats identity: **754/754**
- Fuzzy matching: **NONE**
- Excel error cells: **0**
- Numeric-looking text in canonical numeric-dominant columns: **0** on direct workbook recheck.
- Mandatory blanks: **0**
- Optional unavailable classifications recorded by prior QA matrix: **21,838**

## Formula gate
- FORMULA_INPUT_STATUS=BLOCKED: **754/754**
- Prediction Input Ready: **0/754**
- Verified pre-match: **0/754**
- Backtest Ready: **0/754**
- Release PASS: **0/754**
- Release FAIL: **754/754**
- Verified actuals: **31/754**
- Other actuals remain UNAVAILABLE/UNVERIFIED and are not injected without exact identity/date match.

## Remaining blockers
- Kickoff/date reconciliation review: **67**
- xG temporal provenance: **754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP**
- Goal intelligence production eligible: **0/754**
- Required 100% formula-input coverage: **not proven for 754/754**
- Native Excel numeric gate: **FAIL-CLOSED** because immutable A:ET representation differs from the canonical baseline in 140 blank-cell type/serialization positions; no coercion performed.
- No missing evidence converted to zero, estimate or guessed value.
- No timezone normalization, historical backfill or fuzzy matching performed.

## Per-fixture states
- All 754 fixtures: `FORMULA_INPUT_STATUS=BLOCKED`
- All 754 fixtures: `PREMATCH_STATE=UNAVAILABLE/UNVERIFIED`
- 31 fixtures: `ACTUALS_STATE=VERIFIED_ACTUALS`
- 723 fixtures: `ACTUALS_STATE=UNAVAILABLE/UNVERIFIED`
- All 754: `BACKTEST_READY=NO`
- All 754: `RELEASE_DECISION=FAIL`

## CMOI / derived intelligence
- CMOI blanks: **0/754**
- Last-3 / Last-5: separately governed; no chronology blocker detected in the current Formula Input QA.
- GF/M, GA/M, PPG and venue metrics: separately governed and remain subject to formula eligibility.
- xG values remain quarantined from production eligibility without independently timestamped point-in-time provenance.

## Disposition
No production workbook mutation was made. No Oracle V1.6 logic was changed. The release gate remains fail-closed and the next hourly audit must repeat the complete fixture × column controls.
