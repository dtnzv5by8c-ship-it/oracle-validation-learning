# Selected-50 Snapshot Overlay Trace and Provenance Checkpoint
**28 October 2026 — 18:34 SAST**

## Verified repository state

- Branch: `research/oracle-50-league-readiness-audit`
- Source head before this documentation checkpoint: `b23f8f8d4e4abc8cc006a8f87d3ac2654e49aa0f`
- Candidate trace implementation: `57948ef15a984964f65a774fe8eedb0d76f9f8e6`
- Test import correction: `317a3e25a922ec2610cb17918c61afc64cdbffaf`
- Per-league no-home-away diagnostics: `b23f8f8d4e4abc8cc006a8f87d3ac2654e49aa0f`

## Concrete research-only improvements verified by CI

The overlay now emits a sanitized row-level candidate trace with:
- SHA-256 hashes for the exact snapshot file and input archive;
- snapshot retrieval time and selected season/country/competition;
- provider-native fixture and ordered team IDs, kickoff, status and no-home-away flag;
- an explicit classification/reason for quarantine, historical rows, rows beyond seven days, unsupported archive season, already-present ID/team pair, or a row staged into the isolated research archive;
- explicit `production_eligible=NO`, `betting_eligible=NO`, and unverified canonical fixture/team and official-settlement-truth fields.

The trace does not include team display names or raw provider payloads. It is provenance and diagnostic evidence only; it does not approve identity joins or settlement truth.

The overlay also:
- deduplicates `unsupported_selected_leagues` by selected season instead of repeating one league for every fixture row;
- rejects Boolean, zero-like, fractional and non-finite numeric IDs;
- quarantines unknown `no_home_away` values instead of treating missing/unknown as false;
- emits per-league counts for true/false/unknown `no_home_away` values and nonstandard statuses;
- writes a header-only trace artifact when the runtime overlay is disabled, so the output contract is consistent.

### Validation

- [Safety Contract Tests #258](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40727007643): **PASS** on source head `b23f8f8d4e4abc8cc006a8f87d3ac2654e49aa0f`. The overlay suite passed 7/7, including a synthetic integration test for nested archive paths, per-fixture trace outcomes, source hashes and unique unsupported-league reporting.
- [Dry-Run Planner #556](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40727007654): **PASS**, zero network calls and zero paid-provider calls. Artifact #12833027229 SHA-256: `daeb7c61cfbbd36338ca2a95cd3c54ea88a41342cbcec55f3305ba61334c2a5a`.
- [Runtime #159](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40725720521) remains the latest completed runtime, source commit `ae6450efcf1cac05bdb6423662bcf1ac99d4dc32`. Its artifact #12831029975 SHA-256 `0109f15c570aef954f4354ce84294d1c52962e73f29dc6e90bb022fc87c9335e` was independently verified. This run predates the new candidate trace; it is a baseline, not proof the new trace has been generated against the live archive.

## Runtime and artifact findings

Runtime #159's overlay QA reports:
- 2,250 snapshot fixture rows; retrieval `2026-10-28T14:44:00.366308Z`;
- snapshot age 6,064 seconds at overlay execution;
- 370 rows already present by exact provider fixture ID and ordered team IDs;
- zero rows added, zero unsupported archive rows, zero team-ID conflicts;
- 104 quarantined/invalid rows, 1,384 historical rows, and 392 rows beyond the seven-day staging window.

The nested archive-path resolver corrected the earlier 370-row unsupported-path diagnosis. These rows were already represented by matching provider fixture/team IDs; the overlay correctly did not duplicate them.

The runtime report contains 460 fixture rows, 25 missing-feature blocks, zero unavailable-training blocks, zero production-eligible rows, and zero visible Combo probabilities. The five-match venue-specific history requirement remains unchanged.

Three previously examined snapshot candidates still require row-level reconciliation:
- FootyStats fixture 8551578 (kickoff 14:00 UTC) and 8551579 (16:00 UTC) were already past kickoff by Runtime #159's start at 16:24 UTC.
- Fixture 8432254 (kickoff 23:30 UTC) was future-dated in the snapshot but absent from the generated runtime report.

The existing artifact does not establish why fixture 8432254 is absent. The new trace has not yet been produced against the live archive. It will show the candidate's staging/duplicate/quarantine path, but archive-vs-snapshot kickoff/status divergence remains an additional diagnostic to add if the trace shows the row was already present.

## Combo, settlement and release gates

The dry-run Combo matrix still evaluates 121 scorelines and shows the unresolved target mismatch:
- Predictor: Double Chance AND 2–4 total goals inclusive.
- Existing settlement helper: Double Chance AND total goals below five, including 0–1 goals.
- Home disagreement: 0–0 and 1–0.
- Away disagreement: 0–0 and 0–1.

This diagnostic does not establish the official bookmaker rule. Combo remains masked.

The governed readiness artifact still reports zero current fixture rows, a stale schedule (last fixture date 17 October; window end 22 October), zero approved canonical bridges, zero verified fixture/team joins, zero verified official settlement truth, and unverified point-in-time xG/odds provenance.

## Required next runtime validation

The new trace code has passed offline CI but has not yet been exercised by a runtime build. A public research workflow dispatch is required; dispatch is unavailable through the tools used in this run, so **no new runtime run is claimed**.

- Workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml
- Branch: `research/oracle-50-league-readiness-audit`
- Inputs:
  - `confirm_private_archive_read=true`
  - `private_archive_release_tag=research-selected50-footystats-history-40447419806`
  - `include_current_snapshot=true`
  - `snapshot_run_id=40708750173`

This uses the existing snapshot artifact and the governed private archive; it does not require new provider API calls. Inspect the generated `current_snapshot_candidate_trace.csv` and `current_snapshot_overlay_qa.json` before deciding whether a separate archive-metadata comparison is needed.

## Governance

No production repository writes, no private-repository Actions runs, no provider API calls, and no changes to Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers or governance. All research outputs remain non-production and non-betting eligible.
