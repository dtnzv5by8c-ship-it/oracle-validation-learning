# Project Oracle — 50-League Autonomous Audit Checkpoint (Run 8)
Audit time: 2026-10-25 04:45 SAST / 02:45 UTC
Branch: `research/oracle-50-league-readiness-audit`
Decision: **INCOMPLETE — production eligibility NOT GRANTED**
Scope: exactly the owner-approved 50 FootyStats provider IDs. Research/reporting only.

## Live-state checks performed
- Re-read the recovered selected-50 manifest and current crosswalk revision 5.
- Re-read the protected private canonical registry `config/oracle_major_league_registry_v1.json`, the private `data/league_readiness_matrix.csv`, current source manifest, source reconciliation manifest, current team-state manifest, upcoming-fixture manifest, FootyStats source manifest, historical match-spine manifest, four-model readiness JSON, and immutable feature snapshot manifest.
- Re-read the research-only archive feature audit workflow and relevant feature/crosswalk/integrity scripts.
- Queried current private and public workflow run inventories, latest jobs and artifacts.

## Verified source state
- Owner-selected manifest: exactly 50 rows and 50 unique provider IDs.
- Protected canonical registry: 27 canonical entries; registry is not the scope for this audit.
- Readiness matrix last successful refresh: 2026-10-01T17:25:35.759116Z. It contains 27 legacy rows and is stale for current selected-50 decisions.
- Current-source manifest generated 2026-10-08T04:32:49Z; its dates are 2026-10-01 through 2026-10-10.
- Current reconciliation generated 2026-10-07T04:33:52Z: 108 FotMob rows, zero SofaScore rows, zero matched, 108 unverified; recorded source errors include eight HTTP 403 failures.
- Current team-state manifest generated 2026-10-07T04:33:53Z; 12,883 rows and history window 5, but not linked to the selected provider IDs.
- Upcoming fixture manifest generated 2026-10-08; 27 active leagues and window 2026-10-08 through 2026-10-22. It is stale and not selected-50 coverage.
- Historical spine manifest generated 2026-10-02: 80,550 source rows, 12,836 admitted rows, 27 active leagues, with G1, SRB and T2 excluded.
- FootyStats current-season page manifest generated 2026-10-01: eight targets returned HTTP 403, zero newly retrieved rows; controlled total 10,783 remains a separate legacy 27-target evidence set.
- `archive/FEATURE_SNAPSHOT_MANIFEST.csv` is header-only: zero immutable feature snapshot rows.
- Existing four-model readiness snapshot is dated 2026-10-07. It marks M-1UP BLOCKED and BTTS/DC/COMBO READY for a development run only; this is not selected-50 readiness evidence.

## Crosswalk integrity and current decision
- Crosswalk revision 5 was verified as 50 rows and 50 unique provider IDs matching the selected manifest's ID set.
- 22 canonical candidates remain review-only; 28 remain UNRESOLVED.
- No selected provider-ID -> API fixture -> canonical home/away team join has been verified.
- Selected-ID-specific readiness remains unverified for M-1UP, BTTS Yes, Double Chance and Double Chance + Under 4.5.
- xG and odds as-of-kickoff provenance is not established for the selected 50.
- All production eligibility states remain NOT_GRANTED.

## New reporting-only fail-closed scope guard
Added:
- `scripts/validate_selected50_scope.py` — validates the exact 50 manifest IDs, crosswalk ID-set equality, provider catalogue ID-set equality, and nonblank `provider_league_id` in archive manifest rows. It explicitly refuses to substitute `season_id` for provider competition ID.
- `tests/test_selected50_scope_guard.py` — seven unit tests covering exact-set pass, missing archive IDs, missing catalogue ID, crosswalk mismatch, duplicate manifest IDs, ambiguous ID columns, and attempted approval state.
- Updated `.github/workflows/oracle-footystats-archive-feature-audit.yml` to run this diagnostic in the research-only archive audit and include the script/tests/manifest/crosswalk in push-trigger paths. A blocked scope is written as a diagnostic artifact; it never grants production eligibility.

Commits:
- Script: `0d6edbb8ef252a21d290ce839b9a159cab1d85e5`
- Tests: `42f8f8216f161be9b8d1dafd3526397bf0080a44`
- Workflow wiring: `45518b0407a1681141855f3c57b6512d19344657`
- Crosswalk revision 6: `5580b31fc838805ff706669318e78a92de6f1d49`

Revision 6 adds audit/run metadata to all 50 rows without changing any candidate to approved. It was re-opened and verified as 50 rows, 50 unique IDs, 122 columns.

## CI state at checkpoint
The workflow triggered by the workflow update is:
- Run #54: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40155615819
- Head SHA: `45518b0407a1681141855f3c57b6512d19344657`
- Last checked: `in_progress`, job `archive-feature-audit` in progress, no artifact yet.
- The run is not yet evidence of passing tests or a completed scope guard. Its artifact must be inspected when available.

Latest private runs still visible:
- Expansion #208 (40149882862): failure in prepare; controlled/downstream jobs skipped; no artifacts.
- Live Prediction #78 (40145302396): failure.
- Live Settlement #38 (40146540242): failure.
- Run To Completion #26 (40135975383): failure.
The #208 job log download still returns `BlobNotFound`; job-step API returns no steps, so the root cause is not verified. The workflow source's gate intends `COMPLETE_RESEARCH_ONLY` to exit successfully, yet #208 failed at prepare; do not infer the cause.

## Scope-guard interpretation
The existing archive feature builder derives `provider_league_id` from competition ID fields in archived payloads, but the previously audited archive manifest had that field blank for all 126 season rows. The new guard is designed to report that as a blocker. A successful workflow run or a good non-null field-coverage percentage must not override an ID-set/provenance failure.

## Next safe actions
1. Inspect run #54's test logs and `selected50_scope_guard.json` artifact when available.
2. Use the guard output to determine whether the provider catalogue IDs and archive manifest IDs exactly match the selected 50. If IDs are missing/ambiguous, preserve BLOCKED and fix only the research ingestion/manifest path.
3. Obtain a fresh, exact-ID provider response and fresh current fixtures/event truth; do not treat old 27-league data as selected-50 evidence.
4. Build exact fixture/team joins, immutable pre-kickoff feature snapshots, xG/odds as-of-kickoff provenance, and market-specific readiness.
5. Keep each of M-1UP, BTTS Yes, Double Chance and DC Under 4.5 gated independently.

No production model logic, weights, probabilities, thresholds, calibration, model version, protected registry or canonical ledgers were modified. No draft PR was merged, no gate bypassed, and no paid provider change was made.
