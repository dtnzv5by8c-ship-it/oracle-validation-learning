# Master OMI Formula Input Release Gate — Automation Run 11 Re-audit

Timestamp: 2026-11-22 04:31 SAST / 2026-11-22 02:31 UTC

## Final release decision
FAIL-CLOSED. No Master OMI report is authorised for release.

## Canonical integrity
- Canonical workbook: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
- Canonical whole-workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Current candidate A:ET content/type hash: 2abda90aad8613203e17ffafcc8245a4f22530b195c14494c5010e2a72ca1510
- Direct A:ET value differences: 0
- Direct A:ET native-type differences: 1269 (float/int representation differences; values identical)
- No A:ET mutation/coercion/insertion/deletion/reorder/rename performed.
- A:ET immutable gate: FAIL-CLOSED because canonical representation is not preserved in the candidate.
- The canonical workbook itself also contains 15,574 numeric-looking strings in A:ET; these were not coerced.

## Schema / governance
- Report Configuration version: 2.1.1
- Governed selected leagues: 50
- Market Intelligence: 755 rows x 264 columns
- Governed fixtures: 754
- Heading comments: 264/264
- Exact FootyStats identity: 754/754
- Silent fuzzy matching: none
- Duplicate governed fixture keys: 0

## Reconciliation
- Schedule rows: 67
- Exact kickoff matches: 687
- Kickoff/date review required: 67
- Exact season/fixture/team-ID joins are retained; no automatic kickoff correction.
- Stale Report Scope / legacy metadata describing 387 rows and 40 verified actuals was corrected in the fail-closed QA candidate.
- False FIXTURE_IDENTITY_REVIEW notes were removed where exact Fixture-ID join is already PASS; kickoff/date review remains explicit where applicable.

## Formula gate
- FORMULA_INPUT_STATUS=READY: 0/754
- FORMULA_INPUT_STATUS=BLOCKED: 754/754
- VERIFIED_PREMATCH: 0/754
- VERIFIED_ACTUALS: 31/754
- UNAVAILABLE/UNVERIFIED actual state: 723/754
- BACKTEST_READY=YES: 0/754
- BACKTEST_READY=NO: 754/754
- RELEASE_DECISION=PASS: 0/754
- RELEASE_DECISION=FAIL: 754/754
- Prediction Input Ready: 0/754

## Mandatory blockers
1. Immutable A:ET native representation gate: 1,269 candidate-vs-canonical type differences.
2. 67 kickoff/date reconciliation reviews.
3. 754/754 xG rows lack independently verified point-in-time capture timestamps; all remain quarantined.
4. Goal Market Research is not production eligible: 734 EXPERIMENTAL_UNCALIBRATED and 20 BLOCKED_LEAGUE_BASELINE_LT20.
5. Required formula-input coverage is not proven at 100% for the governed release gate; no missing value is converted to zero or estimated.
6. Native Excel numeric-type eligibility fails for governed PPG/GF/M/GA/M inputs; A:ET is immutable.

## Leakage / chronology / actuals
- Last-3 / Last-5 chronology gates retained.
- PPG, GF/M, GA/M denominator and pre-match cutoff controls retained.
- Post-match leakage: no admitted leakage.
- Verified actuals remain separate from pre-match evidence.
- Only exact governed fixture/date actual links are eligible for VERIFIED_ACTUALS; 31 are verified.
- No actuals with identity/date mismatch are injected into governed pre-match rows.

## Production protection
- Oracle V1.6 production logic unchanged.
- No production probabilities changed.
- Missing values were not converted to zeros or estimates.
- Implausible goal-environment values remain UNAVAILABLE/UNVERIFIED; no guessed division/rescaling/repair was performed.

## Candidate artifact
- Re-audited fail-closed candidate SHA-256: f4d4a25d166466bc8e9742cbc00e95259ee3bf52334f4586cf4bfa56c1c399fb
- Library path: /Master OMI/Oracle_Master_OMI_RUN11_FINAL_QA_REAUDITED_FAIL_CLOSED.xlsx
