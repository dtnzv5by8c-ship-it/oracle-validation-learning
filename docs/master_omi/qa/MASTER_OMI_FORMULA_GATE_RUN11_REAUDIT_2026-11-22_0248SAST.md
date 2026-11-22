# Master OMI Formula Input Release Gate — Automation Run 11 Re-audit

**Audit time:** 2026-11-22 02:48 SAST  
**Final release:** FAIL-CLOSED

## Canonical integrity
- Canonical workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Candidate after configuration-only fix SHA-256: `c2674761d2b5fa3ec3a4e4e01c3fc57eec39bf66ebbdb9b55328711ee9083171`
- Market Intelligence: 755 x 264
- Immutable A:ET comparison: **0 value differences; 0 native-type differences**
- A:ET was not modified.

## Configuration defect fixed
Report Configuration contained `configuration_version=1.1.0`. This was corrected to `2.1.1` outside A:ET. Oracle V1.6 logic was not changed.

## Mandatory gates
- Governed fixtures: 387
- Heading comments: 264/264 PASS
- Exact FootyStats identity: 387/387 PASS
- Fuzzy matching: NONE
- Duplicate governed fixture keys: 0
- Kickoff/date blockers: 38
- Required MI coverage below 100%: 169
- Implausible goal-environment records: 15 quarantined
- xG point-in-time capture timestamps verified: 0/754
- Independently verified actuals: 31/387
- Formula input ready: 0/387
- Formula input blocked: 387/387
- Backtest ready: 0/387
- Release PASS: 0/387
- Release FAIL: 387/387

## State separation
- VERIFIED_PREMATCH: 0/387
- VERIFIED_ACTUALS: 31/387
- UNAVAILABLE/UNVERIFIED: remaining blocked pre-match/actual states

Missing values were not converted to zero or estimates. Goal anomalies were quarantined without guessing, dividing, or rescaling.

## Production protection
- Oracle V1.6: unchanged
- A:ET insertion/reorder/rename/coercion: none
- No fuzzy fixture matching
- No silent date normalization
- No post-match leakage admitted

## Final decision
**MASTER_OMI_RELEASE = FAIL-CLOSED**

The configuration-version defect was fixed and the complete gate was re-run. Release remains blocked by mandatory fixture/provenance/data-quality gates, including kickoff/date reconciliation, sub-100% required coverage, quarantined goal-environment values, and unverified xG capture provenance.
