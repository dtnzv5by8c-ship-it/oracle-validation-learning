# Master OMI MI QA — 2026-11-25 20:48 SAST

## Decision
RELEASE_DECISION=FAIL-CLOSED

## Scope
- Permanent V2.1.1 Master OMI contract
- Formula Input Release Gate
- Canonical Market Intelligence surface: 755 rows x 264 columns
- Governed fixture rows: 754
- Full-row/full-column release-gate audit
- Rolling 50-league fixture-spine freshness explicitly checked

## Evidence reviewed
- Latest independent QA evidence: docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-25_1926SAST.md
- Latest QA evidence blob: 2ed3e5f2a7dc5a7944461e588f6f5cfc77b3c2d7
- Latest remediation evidence: Run 69
- Latest remediation ref: e070e3cc7ecd0ab4b829aa2796277ececb80de68
- Canonical V2.1.1 workbook SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical A:ET protected hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564

## Exhaustive gate status
- Fixture IDs: 754/754 unique
- Duplicate Fixture IDs: 0
- Formula cells: 0
- Excel error literals: 0
- Governed analytical numeric-looking text outside ET: 0
- Residual numeric-looking text outside ET: 25, all verified GG:GJ provenance/source-fixture identifiers
- Authorised native numeric conversions: 21,749
- Genuine text preserved in governed remediation ranges: 117
- Analytical value changes: 0
- A:ET changes: 0
- Oracle V1.6 changes: 0

## Rolling 50-league spine
- The workflow has been corrected to require current rolling artifacts:
  - data/fixtures/governed_50league_current.csv
  - research/four_model/outputs/omi_prediction_ledger_current.csv
- The workflow explicitly fails when dated frozen spine/ledger artifacts are detected.
- Separate 50-league workflow was changed from fixed dates to rolling UTC today + 7-day window.
- This is a workflow-level root-cause fix, not proof that a fresh current source artifact was successfully generated and independently audited in this cycle.
- No stale dated weekly spine is accepted as the current governed spine.

## FootyStats / chronology
- FootyStats PPG/GF/M/GA/M type remediation remains 21,749 type-only conversions with no analytical value changes.
- Direct provider values must carry explicit source/provenance/quality metadata.
- Missing provider evidence remains explicit and is never converted to zero/estimate.
- xG temporal provenance remains 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP and is a release blocker.
- Last-5/Recent Form workflow root cause was identified: prior LastX retrieval lacked fixture-specific cutoff.
- Workflow fix now uses completed league matches strictly before target kickoff and records home_last5_cutoff_utc / away_last5_cutoff_utc.
- The fix requires a fresh run and independent re-audit before it can be considered release-certified.
- H2H remains same-league and strictly pre-match in the governed evidence design.

## Remaining release blockers
- Kickoff reconciliation: 67/754 KICKOFF_MISMATCH
- xG temporal provenance: 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP
- LTSS: 406 BACKTESTED_LEAGUE_WINDOW / 348 STATE_FALLBACK_RESEARCH
- Research actuals: 41 populated rows retain blank immutable DI review status
- Formula Input/backtest eligibility: BLOCKED
- Production eligibility: 0/754
- Betting eligibility: 0/754
- CMOI: research-only; UNAVAILABLE/UNVERIFIED for promoted production eligibility
- Exact Run 69 XLSX binary is not exposed through the connected GitHub file surface; hashes alone are not independent workbook/XML certification.

## Root-cause progression
1. Frozen weekly spine root cause: FIXED IN WORKFLOW; current source artifacts still required.
2. 50-league fixed-date dispatch root cause: FIXED IN WORKFLOW.
3. Last-5 cutoff root cause: FIXED IN WORKFLOW; next-run validation required.
4. FootyStats numeric-type defect: REMEDIATED; re-audit required.
5. xG capture timestamp: NOT FIXED; authoritative timestamp still absent.
6. Kickoff mismatches: NOT FIXED; authoritative event-time review required.
7. CMOI promotion: NOT FIXED BY DESIGN; remains research-only/fail-closed.
8. Binary certification: BLOCKED until exact candidate XLSX bytes are exposed.

## Matrices
- Coverage matrix SHA-256: 746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed
- Row exception matrix SHA-256: 7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Preservation controls
No fuzzy matching, timezone normalization, estimation, zero-fill, historical backfill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, schema redesign, or Oracle V1.6 redesign.

## Release rule
100% QA is not demonstrated. RELEASE_DECISION remains FAIL-CLOSED.
