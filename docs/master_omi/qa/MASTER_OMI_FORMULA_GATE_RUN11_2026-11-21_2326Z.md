# Master OMI Formula Input Release Gate — Automation Run 11

Date: 2026-11-21 23:26 SAST

## Release decision
**FAIL-CLOSED**. The current canonical V2.1.1 workbook is not releasable.

## Canonical workbook
- File: Oracle_Master_OMI_CANONICAL_V2_1_1_CMOI_FINAL_LOCKED_21Nov2026.xlsx
- Whole-workbook SHA-256: 828b723e14452834dd301ba0f2aec553b059e437b928e9c2d02bd5e221219be4
- Market Intelligence: 755 rows x 266 columns
- Immutable A:ET scope: 150 columns
- A:ET semantic/type audit hash: 54b4eb99777271fbb11705b8c22638dd30df5f775f55ae82f121054718706c95

## Schema/configuration
- Workbook naming and sheet structure are consistent with the V2.1.1 CMOI candidate.
- **FAIL:** Report Configuration contains configuration_version = 1.1.0, not 2.1.1. This is a genuine configuration defect and is not silently accepted.
- All 150 governed A:ET headings have non-empty comments/definitions: 150/150 PASS.

## Fixture identity and reconciliation
- 754 populated fixture rows; 754 unique Fixture IDs.
- Duplicate governed composite keys: 0.
- Exact composite identity is present in xG evidence: 754/754 PASS_EXACT_COMPOSITE_IDENTITY.
- Schedule reconciliation: 687 MATCH; 67 REVIEW_REQUIRED.
- Evidence/Schedule gate: 687 EXACT_JOIN_EVIDENCE_AVAILABLE; 67 REVIEW_REQUIRED_SCHEDULE_DISCORDANCE.
- No silent fuzzy matching is used.

## Formula-input controls
- Home/Away Last-5 N populated: 754/754.
- Several governed numeric fields are stored as Excel text strings rather than native numeric cells, including Last-5 GF/M, GA/M, PPG and goal-research/lambda fields. This is a native-type gate failure; no in-place coercion was made.
- Goal research status: 734 EXPERIMENTAL_UNCALIBRATED; 20 BLOCKED_LEAGUE_BASELINE_LT20.
- Production Eligible: 754/754 NO.
- Betting Eligible: 754/754 NO.
- Therefore FORMULA_INPUT_STATUS is BLOCKED for every governed fixture and no fixture is formula-ready.

## xG provenance
- 754 numeric pre-match-labelled xG rows are present.
- 0/754 have a verified point-in-time capture timestamp.
- xG remains UNAVAILABLE/UNVERIFIED for release/backtest purposes.

## Goal-environment quarantine
- Pre-Fixture League Goal Avg reaches 33.9185; 30 rows exceed 10 goals.
- Latest Season League Total Avg Goals also reaches 33.9185; 14 rows exceed 10 goals.
- These records are quarantined as UNAVAILABLE/UNVERIFIED. No division, rescaling or guessed repair was applied.

## Actuals
- Actual Settlement Status: 316 SETTLED, 42 UNSETTLED, 396 NOT_AVAILABLE_FROM_CURRENT_SOURCE.
- Actual Results Source: 275 recovered prospective evidence rows and 83 FootyStats rows; 396 have no current source.
- 275 rows are marked ACTUAL VERIFIED.
- Backtest readiness remains NO for all fixtures because mandatory pre-match, provenance and release gates are not clean.

## Release gate
- FORMULA_INPUT_STATUS: 0 READY / 754 BLOCKED.
- BACKTEST_READY: 0 YES / 754 NO.
- RELEASE_DECISION: 0 PASS / 754 FAIL.
- Missing values were not converted to zero or estimates.
- Oracle V1.6 production logic was not changed.
- A:ET was not inserted, reordered, renamed, or coerced.

## Required remediation
1. Correct configuration_version through the reviewed configuration path to 2.1.1.
2. Regenerate the governed numeric fields through the canonical extraction/mapping path so native Excel numeric types are preserved, without mutating A:ET in-place.
3. Resolve 67 schedule/kickoff/date review rows.
4. Keep all unverified xG quarantined until point-in-time capture provenance exists.
5. Quarantine and trace the implausible goal-environment values back to their source; do not mathematically repair them without source proof.
6. Re-run the complete gate and release only if every mandatory gate passes.

## Per-fixture evidence
754 explicit fixture-level decisions were generated and retained in the run workspace.