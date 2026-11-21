# Master OMI Formula Input Release Gate — Run 11 current re-audit

Date: 2026-11-22 01:38 Africa/Johannesburg

## Final release
MASTER_OMI_RELEASE=FAIL-CLOSED
RELEASE_PASS=0/754
RELEASE_FAIL=754/754
FORMULA_INPUT_READY=0/754
FORMULA_INPUT_BLOCKED=754/754
VERIFIED_PREMATCH=0/754
VERIFIED_ACTUALS=275/754
BACKTEST_READY=0/754

## Canonical V2.1.1 / workbook
Canonical workbook: Oracle_Master_OMI_CANONICAL_V2_1_1_CMOI_FINAL_LOCKED_21Nov2026.xlsx
Current audited candidate: Oracle_Master_OMI_RUN11_CURRENT_AUDITED_FAIL_CLOSED.xlsx
Candidate SHA-256: bc97e9eff9f5e941cf4c10726c1ee064fe5ee8e649396572363fcc13f57627c7
Market Intelligence: 755 x 266
Immutable A:ET: 755 x 150
A:ET semantic/value differences versus canonical: 0
A:ET native-type differences versus canonical: 0
Canonical native numeric-type gate: FAIL-CLOSED
Observed numeric-looking strings in candidate A:ET: 15,574
These are canonical-contract data-quality defects, not candidate mutations. A:ET was not coerced.

Report Configuration configuration_version: 2.1.1

## Governance
Market Intelligence heading comments: 266/266 present.
A:ET heading comments: 150/150 present.
Exact governed fixture identity: 754/754.
Duplicate governed fixture keys: 0.
Fuzzy identity matching: NONE.

## Schedule / kickoff
Schedule reconciliation: 687 MATCH; 67 REVIEW_REQUIRED.
All 67 REVIEW_REQUIRED rows are KICKOFF_MISMATCH and remain ineligible.
No automatic kickoff/date correction was applied.

## Pre-match formula inputs
FORMULA_INPUT_STATUS: BLOCKED for 754/754.
PREMATCH_STATE: UNAVAILABLE/UNVERIFIED for 754/754.
Mandatory gate reasons include production eligibility, goal research validation and canonical native numeric-type failure; 67 rows additionally carry kickoff/date and identity/schedule review; 20 rows additionally carry goal-research baseline blocking.
No PASS row exists with a blocker note.

Last-3/Last-5 chronology, PPG/GF/M/GA/M denominator and cutoff controls, venue controls, BTTS/goal intelligence, LTSS V1.1, source IDs, sample sizes, status/confidence/as-of and numeric range checks remain subject to the fail-closed eligibility gate.

## FootyStats
Exact identity is governed by fixture identity/source IDs. No silent fuzzy matching is used.

## xG provenance
754/754 xG rows have temporal_provenance_status=UNVERIFIED_NO_CAPTURE_TIMESTAMP.
capture_time_utc is missing for 754/754.
prediction_eligible=NO and betting_eligible=NO for all 754.
xG remains UNAVAILABLE/UNVERIFIED.

## Goal intelligence
Goal Market Research:
- 734 EXPERIMENTAL_UNCALIBRATED
- 20 BLOCKED_LEAGUE_BASELINE_LT20
All 754 are non-production and non-betting eligible.
Implausible goal-environment values remain quarantined; no guessing, division or rescaling was applied.

## Actuals / backtest
Actual Results contains 275 populated exact actual-result rows.
These remain separate VERIFIED_ACTUALS evidence.
Because the pre-match gate is failed, BACKTEST_READY remains 0/754.
No actuals are allowed to overwrite or contaminate pre-match state.

## Missingness / leakage
Missing and insufficient values remain explicit unavailable/unverified states.
No missing value was converted to zero or an estimate.
No post-match data was admitted into the pre-match eligibility state.

## Production protection
Oracle V1.6 production logic: UNCHANGED.
A:ET insertion/deletion/reordering/renaming/coercion: NONE.
No workbook repair was performed inside immutable A:ET.

## Final
FAIL-CLOSED. No report release is authorised.
The canonical native numeric-type defect must be resolved only through the approved canonical template/extraction/configuration path. The 67 kickoff/date reviews, goal-research validation gates and xG temporal provenance gates must also pass before any fixture can become formula-ready or backtest-ready.
