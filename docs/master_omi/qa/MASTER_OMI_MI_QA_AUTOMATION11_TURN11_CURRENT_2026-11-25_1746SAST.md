# Master OMI MI QA — Automation Turn 11 — 2026-11-25 17:46 SAST

## Release
RELEASE_DECISION: FAIL-CLOSED
QA completion: NOT 100%

## Scope
Permanent Master OMI V2.1.1 contract and Formula Input Release Gate.
Production surface remains governed as 754 fixtures x 264 MI columns from the established Master OMI evidence lineage. Oracle V1.6 and A:ET are protected and were not changed.

## Latest repository evidence reviewed
Latest repository commits include:
- 3440696dc3fe18bfe285b27c90e9bc9218eeee71 — enabled the 50-league upcoming MI workflow on main.
- e1ca087940cba531dac24b8b92a0ed03e8f03e79 — 50-league upcoming fixture + FootyStats MI build.
- af4f8385b16d158e0f5d1e88683fac01d5aeaa3b — public final gate audit.

The public final gate summary reports:
- status: BLOCKED_FAIL_CLOSED
- completion_percent: 90
- governed_fixture_rows: 385
- exact_identity_rows: 364/385 (94.55%)
- unmatched_identity_rows: 21
- ambiguous_identity_rows: 0
- FootyStats direct provider value rows: 2184
- v1_6_production_certified: false
- master_omi_final_assembled: false
- master_omi_A_ET_integrity_verified: false
- formula_count_preserved: false
- pit_chronology_final_verified: false
- production_ready: false
- blockers: fixture identity not 100%, V1.6 production certification false, risk coverage not ready.

## New workflow control finding
The newly committed 50-league upcoming MI workflow builds exact FootyStats fixture identity and pre-match league-team snapshots, but its LastX retrieval calls `lastx?team_id=...` without a fixture-specific historical cutoff. Therefore Last-5 values from that workflow cannot be accepted as chronology/leakage-certified for Formula Input until a source-supported cutoff is attached per fixture. This is a release blocker, not a value to be guessed or backfilled.

The workflow also computes a season-level conservative cutoff using the earliest fixture kickoff in that season/window. That is conservative for the league-team snapshot, but it does not solve the LastX endpoint's absence of a fixture-specific cutoff.

## Established Run 67 remediation evidence
Candidate workbook SHA-256:
5c9ad073c77cac132bf86022a40397fe52ed8cf8ad0030cfd43bcc4452ac9826

Candidate sheet3.xml SHA-256:
5b59c57e8f130993de94f134d827a19e7012321a256362c668d12a45713c1fde

Canonical workbook SHA-256:
9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

Cell-change manifest SHA-256:
aa22d43b0d8769efd9522973384b1a3f35752b334be2fbe2d0345fe8f579f287

Run 67 reported 21,749 authorised numeric-type conversions, 0 analytical value changes, unchanged A:ET, unchanged Oracle V1.6, and only xl/worksheets/sheet3.xml changed. Exact Run 67 XLSX binary is not exposed through the connected GitHub file surface, so no fresh independent workbook/XML certification is claimed.

## Established exception state
- 67/754 kickoff mismatches remain controlled exceptions.
- xG temporal provenance remains 754/754 UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- LTSS split remains 406 BACKTESTED_LEAGUE_WINDOW / 348 STATE_FALLBACK_RESEARCH.
- 41 populated research-actual rows retain blank immutable DI review status.
- Formula Input/backtest/production/betting eligibility remain blocked.
- CMOI remains research-only / UNAVAILABLE-UNVERIFIED for promoted production eligibility.

## Integrity policy
No fuzzy matching, timezone normalization, historical backfill, estimation, zero-fill, unsupported provenance substitution, fixture-ID rewriting, A:ET mutation, or Oracle V1.6 redesign was performed.

Coverage matrix SHA-256:
746659f78bcc532764487a3468fa37aa5aba558f16c2ee9f489d072c4bc6a7ed

Row exception matrix SHA-256:
7f3cd8990b085dd44a0488805a2f789f2927be7e97b53f895bbd4482f3530f45

## Decision
RELEASE_DECISION remains FAIL-CLOSED. The public final gate's 385-row/364-exact-identity state is not sufficient to certify the canonical 754-fixture production surface, and the new LastX workflow is not chronology-certified for formula/backtest eligibility.
