# Identity Contract Test Result and Next Gate — 2026-10-28 06:20 SAST

## Verified results

The following runs on research branch commit `c167b7ebf97bbfdeba18c2358ba148d69a15fed9` completed successfully:

- [Archive Feature Audit #62 / run 40630847423](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630847423) — success; artifact [12791402647](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630847423/artifacts/12791402647), SHA-256 `2d9375590eb6f87db34a6c8939fd602d83c58dbd1925671d1189231330bbf3f0`.
- [Dry-run Planner #470 / run 40630847460](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630847460) — success; artifact [12791890404](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630847460/artifacts/12791890404), SHA-256 `4f5e33aa5efb59b13d3da0a80aea95c1465590c146192d0f5f11e5951aa0d9de`.
- [Safety Contract Tests #164 / run 40630847483](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40630847483) — success.

The archive audit's job steps all completed successfully, including dependency install, unit tests, archive freshness check, selected-50 scope validation, archive identity/season audit, provisional standings, feature coverage, crosswalk generation, prediction adapter, team identity audit, exact kickoff candidate audit, and artifact upload.

## Identity contract implementation (research only)

The research branch now contains:
- `scripts/validate_current_feed_identity_contract.py`
- `tests/test_current_feed_identity_contract.py`
- `data/current_feed_identity_allowlist.research.json`

The test suite exercises exact approved ID+country admission, same-name/different-ID quarantine, wrong country, unknown IDs, missing country, absent/unapproved allowlist and display-name-only rejection. The research allowlist intentionally contains zero real entries. The tests verify the contract behaviour, not any actual league mapping.

## Current-feed finding

Read-only inspection of the production branch's `data/current_source_manifest.json` (blob `c06a400da8a85335ec44a96719dda2b982115599`) shows:
- generated `2026-10-06T07:49:26.139704+00:00`
- requested dates `2026-09-29` through `2026-10-08`
- source FotMob public data endpoints.

This checked-in manifest is stale at the 2026-10-28 checkpoint. It does not prove no newer artifact exists elsewhere and does not establish why a scheduler/ingestion stopped. The legacy ingestion workflow remains unsuitable for execution before identity protection because it admits by display name alone.

## Decision

Research tests and archive QA: **PASS for the cited runs**.
Feed freshness: **FAIL / STALE**.
Real approved selected-50 league ID/country mappings: **0/50**.
Verified fixture/team joins in the ledger audit: **0**.
Production and betting release: **NO-GO**.

## Next action

The next safe implementation unit is an isolated staging adapter that consumes an externally reviewed allowlist and applies the exact-ID contract to already-acquired rows, producing accepted/quarantined counts and a manifest. It must not fetch provider data, modify the production ingestion script, write production ledgers, or promote any mapping. Populate allowlist entries only after authoritative evidence and review. In parallel, locate a newer approved staging artifact/run manifest via repository release/artifact metadata; do not run the old name-only ingestion path as a refresh workaround.

No production repository, Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected registry, ledgers or governance were changed. No provider API calls were made.
