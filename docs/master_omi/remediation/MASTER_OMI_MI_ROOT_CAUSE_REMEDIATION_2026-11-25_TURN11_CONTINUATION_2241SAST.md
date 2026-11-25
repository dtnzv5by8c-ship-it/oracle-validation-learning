# Master OMI MI Root-Cause Remediation — Automation Turn 11 continuation — 2026-11-25 22:41 SAST

RELEASE_DECISION=FAIL-CLOSED

## Work completed
1. Directly re-read latest QA evidence at 22:11 SAST.
2. Directly scanned the live rolling fixture spine and manifest.
3. Confirmed 368 current FootyStats fixture IDs are unique and exact.
4. Found a persisted manifest/CSV fixture-date-bound mismatch: manifest requested window ends 2026-12-02 while the current CSV contains fixtures through 2026-12-03.
5. Fixed the rolling producer so it records actual fixture_date_min/fixture_date_max and validates manifest-to-CSV bounds before persistence.
6. Fixed a field-mapping defect where overall Last-5 fields were populated from venue-only samples.
7. Fixed persistence of FootyStats season metrics: PPG, PPG_HOME, PPG_AWAY, GF/M, GA/M, average goals, BTTS and over/under metrics are now joined into fixture-level rolling MI with source/status/cutoff provenance.
8. Added fixture-specific H2H aggregation from exact provider team IDs using completed league-matches strictly before target kickoff.
9. Preserved xG as UNVERIFIED_NO_CAPTURE_TIMESTAMP because authoritative capture-time provenance is still unavailable.

## Live commits
- 1413af40ac9fe4a6df98bf55fd0f8fb2c326b500 — separate overall/venue Last-5, persist FootyStats metrics, add cutoff-safe H2H and explicit xG provenance status.
- b26f0e69c4fcec5e4336a0e5af3469a3ac320061 — persist actual fixture-date bounds and fail closed on manifest/CSV mismatch.
- 759ddb1b5012d4e1ce44ff24efdbb6b77adcd6ca — persist current root-cause matrix.

## Current source evidence
- Current fixture spine blob SHA observed now: 34f11025d1b72305126e124602838826859739d3
- Current fixture rows: 368
- Unique fixture IDs: 368
- Duplicate IDs: 0
- Date range: 2026-11-25 to 2026-12-03
- Current manifest blob SHA: 9c18a500b673e3809627b2c74e60e148518b956a
- Current MI artifact blob SHA: 02d759da779838f334bfe767751b9f08bdd9005c
- Manifest reports 351 fixtures with fully verified Last-5 under the prior producer implementation.

## Remaining release blockers
- research/four_model/outputs/omi_prediction_ledger_current.csv is absent from the public default branch.
- database/current_prematch_team_state.csv is absent from the public default branch.
- database/matches.csv is absent from the public default branch.
- Canonical production surface is 754 governed fixture rows; current rolling 50-league spine is 368 rows. Scope cannot be padded or silently reconciled.
- 67/754 kickoff mismatches remain in the canonical evidence.
- 754/754 xG temporal provenance remains UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- Formula Input, Production and Betting eligibility remain BLOCKED.
- CMOI remains UNAVAILABLE/UNVERIFIED for production promotion.

## Governance
No A:ET changes. No Oracle V1.6 changes. No fuzzy matching. No timezone normalization. No estimation. No zero-fill. No historical backfill. No post-kickoff evidence. No stale weekly spine. No unsupported provenance substitution.

## Next gate
The next scheduled rolling producer execution must validate the new workflow code, regenerate current MI, persist the reconciled current spine, and then the independent QA task must re-audit the resulting source and candidate. No release workbook is certified by this remediation cycle.