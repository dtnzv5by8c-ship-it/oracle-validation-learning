# Master OMI Independent 100% Release Gate — Current Cycle

Audit time: 2026-11-27 12:47 SAST  
Decision: **FAIL-CLOSED / NOT RELEASED**

## Historical-first control
Inspected live GitHub state, active automation state, `docs/PROJECT_ORACLE_LESSONS_LEARNED.md`, `docs/PROJECT_ORACLE_CONTINUATION_STATE.md`, latest QA/root-cause artifacts, and recent commits before raising findings. Closed defects were not reopened.

## Rolling 50-league fixture universe
- Governed leagues: **50**
- Current rolling fixture rows: **392**
- Unique provider Fixture IDs: **392**
- Fixture-bearing league-season IDs: **41** — valid; governed universe is 50 leagues, not 50 season IDs.
- Rolling manifest generated: **2026-11-27T08:33:39.602844Z**
- Provider: FootyStats
- pre_match_only: true
- fuzzy_matching_used: false
- historical_fallback_used: false
- A:ET changed: false
- Oracle V1.6 changed: false
- Current fixture Git blob SHA: `03fa7094fe1b1dda1126327b5e0f86d29dd5fc63`
- Manifest-declared SHA-256 for the fixture CSV: `29108354e12b184d9418c2973816c20a737eeec925c3462d54288143338b8774`

**Freshness:** FAIL at this audit point. The current snapshot was generated at 08:33:39 UTC; the audit point is approximately 10:47 UTC, exceeding the 90-minute freshness gate. No stale snapshot is promoted.

## Exact fixture identity
- 392/392 exact provider Fixture IDs in the current 392-row MI artifact.
- Duplicate Fixture IDs: 0.
- The fixed-fixture-count remediation is runtime validated by workflow run **45966547927**, run 72, completed successfully at 2026-11-27T08:33:46Z.
- Closed root cause: hard-coded 385-row assertion. Fix commit: `c183a070214105616f3e35e43d3e3a7ca562f80f`.
- Root-cause evidence updated in commit `27b002247c46676202c16397e9e52f3816d4323d`.

## Current Market Intelligence artifact
- Path: `oracle_upcoming_50/footystats_market_intelligence.csv`
- Rows: **392**
- Columns: **139**
- Git blob SHA: `a6867ccdcaba3490bd2ca03d77f24c872d7b3751`
- `provider_status`: 2 complete / 390 incomplete
- `intelligence_status`: 392 DIRECT_PROVIDER_PREMATCH
- xG: 392 UNVERIFIED_NO_CAPTURE_TIMESTAMP — inadmissible for production.
- Last-5: 391 VERIFIED_PRE_KICKOFF; 1 UNAVAILABLE_INSUFFICIENT_SAMPLE.
- Venue Last-5: 375 VERIFIED_PRE_KICKOFF; 17 UNAVAILABLE_INSUFFICIENT_SAMPLE.
- H2H: 41 VERIFIED_PRE_KICKOFF; 351 UNAVAILABLE_NO_AUTHORITATIVE_H2H.
- FootyStats PPG overall/home/away: 392/392 VERIFIED_PRE_KICKOFF.
- Direct GF/M: 392 UNAVAILABLE.
- Direct GA/M: 392 UNAVAILABLE.
- No inference or zero-fill accepted.

The complete 139-column coverage and row-exception matrices from the unchanged current MI blob remain the authoritative detailed field audit; because the blob SHA is unchanged, no closed column finding is reopened.

## Prediction ledger / Team State
- `research/four_model/outputs/omi_prediction_ledger_current.csv`: **ABSENT** at live public HEAD.
- `database/current_prematch_team_state.csv`: present but empty; **inadmissible**.
- Therefore exact prediction-ledger Fixture-ID parity cannot be certified.

## Canonical workbook gate
The canonical production surface remains **754 fixtures × 264 MI columns**. The current upstream artifact is only 392 × 139.

No admissible current candidate XLSX/XML was found. Therefore the following remain unverified/blocked:
- native Excel numeric types
- governed numeric-looking text
- Excel errors
- formula compatibility/readiness
- exact A:ET cell equality
- candidate XML/binary integrity
- candidate SHA-256/provenance
- actuals/derived formula inputs
- LTSS/CMOI
- final workbook certification

## Protected controls
- A:ET unchanged.
- Oracle V1.6 unchanged.
- No stale/historical fallback.
- No fuzzy fixture matching.
- No estimation or zero-fill.
- No timezone normalization.
- No post-kickoff evidence admitted.
- Independent process timestamps are not used as identity equality.

## Gate progression
PASS and closed: 50-league semantics; exact fixture identity; duplicate control; fixed-count remediation; A:ET protection; Oracle V1.6 protection.

Outstanding release gates:
1. Fresh rolling spine.
2. Exact rolling-spine SHA-256 and Fixture-ID-set SHA certification against a current comparator.
3. Authoritative current prediction ledger and exact Fixture-ID parity.
4. Current prematch Team State.
5. Fresh 754 × 264 MI rebuild.
6. PIT-valid xG.
7. GF/M, GA/M and goal/BTTS authoritative evidence or explicit classification.
8. LTSS, CMOI, actuals and derived inputs.
9. Candidate XLSX/XML.
10. Native Excel type/error/formula audit.
11. Exact A:ET comparison.
12. Final hashes/provenance.
13. Final 100% release.

## Release decision
**FAIL-CLOSED. No release workbook is certified.**
