# Master OMI MI Root-Cause Cycle — 2026-11-26 08:51 SAST

## Release decision
FAIL-CLOSED.

## Current authoritative QA
- QA artifact: MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-26_0754SAST.md
- QA blob SHA: b161e3d82ca9c60549b82a077fb0e3e1a07bee3f
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- Canonical A:ET protected SHA-256: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564

## Fresh-source gate
The latest accepted rolling 50-league source is stale for the current cycle. The latest manifest in the public repository was generated at 2026-11-26T04:41:44.338347Z and contains 371 fixtures, 371 unique provider Fixture IDs, zero duplicates, 50 governed leagues, pre_match_only=true, fuzzy_matching_used=false, historical_fallback_used=false. No dated weekly spine was substituted.

## Root-cause finding
The private Oracle Current Data workflow had a `push: main` trigger intended to accelerate fresh current-data staging. That trigger is not a reliable execution dependency for commits produced with GitHub Actions' GITHUB_TOKEN; downstream workflows are not guaranteed to trigger from those token-authored pushes. The repository therefore had a misleading trigger control without a dependable execution guarantee.

## Fix
Commit 72bbab439fa471fecd4c190809ee4ffdbb718ce6 removes the ineffective `push: main` trigger from `.github/workflows/oracle_current_data.yml`. The authoritative schedule remains hourly and `workflow_dispatch` remains available. This prevents a false sense of automatic execution and leaves the hourly scheduled path as the durable execution contract.

## Remaining blockers
1. Fresh rolling 50-league source for this cycle.
2. Current prediction ledger absent from the public default branch.
3. Current prematch Team State and matches are not authoritative populated current sources.
4. Current MI artifact is 139 columns versus the locked 264-column canonical surface.
5. Production scope is 754 governed fixtures versus 371 current rolling fixtures.
6. xG temporal capture provenance remains UNVERIFIED_NO_CAPTURE_TIMESTAMP.
7. Public final-gate reconciliation has 21 unmatched identities out of 385 audited rows.
8. Candidate workbook native XLSX/XML binary is not exposed for independent certification.

## Integrity policy
No fabrication, estimation, zero-fill, fuzzy matching, timezone normalization, historical backfill, post-kickoff evidence, stale-spine substitution, A:ET modification, or Oracle V1.6 production-logic modification was performed.

## Next gate
At the next scheduled current-data execution, verify non-empty current Team State/matches, manifest parity, SHA/row-count persistence, then rebuild the current rolling 50-league MI source and re-run independent QA. Do not promote a release workbook until every mandatory gate passes.
