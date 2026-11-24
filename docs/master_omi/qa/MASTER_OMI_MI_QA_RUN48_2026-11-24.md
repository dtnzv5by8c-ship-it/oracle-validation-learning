# Master OMI MI QA Run 48 — Independent Binary Audit — 2026-11-24 21:33 SAST

RELEASE_DECISION=FAIL-CLOSED

Exact workbook: Oracle_Master_OMI_V2_1_1_REMEDIATION_RUN48_EXACT_AET.xlsx
SHA-256: 8eb384e626fcca292443632b76a5c261ec72e90ceb67aef95f205bab3f8fc742
Market Intelligence: 755 rows x 264 columns; 754 governed fixture rows.

Structural: 264/264 headings; 264/264 comments; 0 blank headings; 754/754 fixture IDs nonblank and unique; 0 duplicate IDs; 0 formulas; 0 Excel errors.

Numeric type: 15,599 numeric-looking text cells total; 15,574 are inside immutable A:ET; 25 outside ET are all GG:GJ FootyStats provenance/source-fixture IDs. Supported governed analytical numeric-looking text outside ET = 0. The Run 48 remediation's 21,749 supported type conversions are preserved with no analytical value changes.

Provenance/cutoff: exact FootyStats fixture identity 754/754; overall source IDs 754/754; venue source IDs 748/754 home and 749/754 away, with missing venue IDs matching zero venue sample. History/pre-match cutoff fields 754/754 populated; no cutoff date later than fixture date.

Schedule: 67/754 REVIEW_REQUIRED, all KICKOFF_MISMATCH. No timezone normalization or silent promotion.

Cross-field actuals: 316/316 populated actual rows pass score/result/BTTS/O1.5/O2.5/U4.5 consistency. Settlement: 316 SETTLED, 42 UNSETTLED, 396 NOT_AVAILABLE_FROM_CURRENT_SOURCE. Actual review status: 275 ACTUAL VERIFIED; 479 blank. 40 of those blank rows have populated research-source actuals and require governed status mapping; no invented status was applied.

xG: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP; prediction use remains quarantined.

Eligibility: Production Eligible 754/754 NO; Betting Eligible 754/754 NO. LTSS/team-score: 406 BACKTESTED_LEAGUE_WINDOW, 348 STATE_FALLBACK_RESEARCH. H2H sample N 754/754. Venue sample/source consistency passes.

CMOI: no CMOI fields exist in the 264-column production contract; therefore CMOI is explicitly UNAVAILABLE/UNVERIFIED and no value was invented.

Governance: no fuzzy matching, timezone normalization, historical backfill, zero-fill, estimation, unsupported provenance substitution, fixture-ID rewrite, A:ET mutation, or Oracle V1.6 redesign.

Mandatory blockers remain: immutable A:ET numeric-looking text, 67 schedule exceptions, 754 xG temporal provenance gaps, 479 review-status blanks (including 40 populated research actuals), Formula Input/backtest blocked, and CMOI unavailable/unverified.