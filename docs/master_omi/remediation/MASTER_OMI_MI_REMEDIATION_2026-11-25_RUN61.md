# Master OMI MI Remediation — Run 61

**Date:** 2026-11-25 10:03 SAST  
**Release decision:** FAIL-CLOSED  
**Additional cells changed in Run 61:** 0

## Authoritative inputs
- Canonical V2.1.1 workbook: `Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx`
- Canonical SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
- Latest independently available QA evidence: `docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_0518SAST.md`
- QA evidence blob SHA: `8acba1b4eb2ee11439052143f36058848215521e`
- QA commit: `45faf3c4eacc2ed1e58ae1cf7691c818ecb5a7a3`
- QA decision: `FAIL-CLOSED`
- Latest controlled candidate referenced by QA: SHA-256 `838549f6188a392037103f4052598e35fcf806a1444e19de937210a6742fca08`

## Source-backed remediation assessment
The latest QA evidence states that the exact latest remediation XLSX is not exposed through the connected GitHub file surface and therefore cannot be independently binary-re-audited there. No newer authoritative source evidence was available to justify changing production analytical values, provenance, fixture IDs, chronology, or configuration.

The controlled candidate already contains the previously authorised append-only numeric type correction: **21,749** valid governed analytical numeric-looking text cells converted to native Excel numeric values outside immutable A:ET. Those conversions remain unchanged in Run 61.

## Direct cell-level validation
- Market Intelligence: **755 rows × 264 columns**
- Governed fixtures: **754**
- Fixture IDs nonblank: **754/754**
- Fixture IDs unique: **754/754**
- Duplicate Fixture IDs: **0**
- Formula cells: **0**
- Excel error cells: **0**
- Numeric-looking text in immutable A:ET: **15,574**
- Previously authorised analytical type conversions: **21,749**
- Remaining numeric-looking text outside ET: **25**
- Remaining numeric-looking text in GG:GJ provenance/source-ID fields: **25**
- Governed analytical numeric-looking text outside ET: **0**

The 25 remaining numeric-looking strings outside ET are genuine FootyStats provenance/source-fixture IDs and are preserved as text.

## Immutable controls
- A:ET: **unchanged**
- Oracle V1.6: **unchanged**
- Production schema: **unchanged**
- No fixture-ID rewriting
- No fuzzy matching
- No timezone normalization
- No estimation
- No zero-fill
- No historical backfill
- No unsupported provenance substitution

## QA matrix/direct-scan discrepancy
The latest QA evidence identifies the actuals/review-status exception. Direct validation establishes **41** affected rows with populated research actuals but blank `Actuals / Research Review Status` in immutable `DI`:

`4, 25, 49, 54, 55, 78, 79, 80, 134, 186–191, 221, 222, 224, 232–239, 269, 313, 338, 353, 357, 364, 366–368, 397–402`

Because `DI` is inside immutable A:ET, no correction was made. No status was inferred, estimated, zero-filled, or backfilled.

## Remaining QA-owned exceptions
- **15,574** immutable A:ET numeric-looking analytical values.
- **41** populated-actual rows with blank DI review status.
- **67/754** schedule `REVIEW_REQUIRED / KICKOFF_MISMATCH`.
- **754/754** xG temporal provenance `UNVERIFIED_NO_CAPTURE_TIMESTAMP`.
- Production Eligible: **0/754**.
- Betting Eligible: **0/754**.
- Formula Input/backtest: **BLOCKED**.
- CMOI: **UNAVAILABLE/UNVERIFIED** because no CMOI fields exist in the permanent 264-column production contract.
- Any venue, Last-3/Last-5, H2H, BTTS/goal, LTSS, actual or derived-field defect lacking authoritative source evidence remains unchanged and explicitly QA-owned.

## Run 61 integrity
- Candidate workbook SHA-256: `8eb384e626fcca292443632b76a5c261ec72e90ceb67aef95f205bab3f8fc742`
- `sheet3.xml` SHA-256: `f19e5c2c06e3b3704fbd6439dd7f6ba60fb69937cf2b662d6d96565cf3dd0830`
- Run 61 additional cell changes: **0**
- Run 61 is byte-identical to the controlled candidate used as the starting point for this remediation cycle.

## Release
**FAIL-CLOSED.** The separate Master OMI MI QA task remains the release authority and must independently re-audit the exact Run 61 binary before any release decision.
