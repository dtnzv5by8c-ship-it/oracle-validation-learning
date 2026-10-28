# Oracle Selected-50 Execution Checkpoint — 2026-10-28 06:45 SAST

## Executive status

**Research QA: PASS for previously completed runs.** New staging-adapter regression runs are queued after correcting JSONL newline handling, fixing the package import, and wiring the staging tests into the contract workflow. **Production and betting release remain NO-GO.** Deadline target: 2026-10-28 12:00 SAST.

## Work completed in this checkpoint

1. Corrected offline staging adapter output to use real newline separators in accepted/quarantined JSONL and its manifest.
2. Corrected the adapter's import to use the package path so tests can import it from repository-root test discovery.
3. Added the offline identity-contract and staging-adapter tests to the safety contract workflow.
4. Added staging adapter/test paths to the archive audit trigger so the complete research audit runs when these files change.
5. Confirmed the accessible production-branch current-feed manifest remains old: generated 2026-10-06T07:49:26.139704+00:00, last requested date 2026-10-08. This is a stale checked-in manifest; it does not prove whether a newer artifact exists outside the branch.
6. Queried the production repository's release list: newest visible Selected-50 normalized runtime candidate release is dated 2026-10-26, not a live current-feed refresh. Do not treat it as proof of current feed freshness.

## Latest relevant Actions

- [Contract tests run 40633734326](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633734326) passed on commit `c8d0ac63654f3a92eddc49b3b815d445440fba28`, but that run started before the final archive trigger change; the new staging tests must be confirmed in a run that includes them.
- [Dry-run planner run 40633734282](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633734282) passed on the same commit.
- [Archive audit run 40633801455](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633801455), [dry-run run 40633801419](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633801419), and [contract test run 40633801353](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40633801353) were queued after the final trigger update at checkpoint time.

## Identity/feed findings

- Root cause in the inspected production ingestion script: fixtures are admitted by display name, not a reviewed exact league-ID allowlist; country/category is not preserved as an identity safeguard.
- Current feed identity audit: 0/50 approved provider-season-to-FotMob bridges; 0 verified canonical fixture joins; 0 verified canonical team joins.
- Research allowlist remains empty intentionally. No real IDs are inferred or approved.
- Offline adapter must be tested against already-acquired rows and produce accepted/quarantined files and checksummed manifest. It must not make network/provider calls or write production ledgers.
- Do not run the legacy name-only ingestion workflow as a refresh workaround. A new staging snapshot can only be trusted after the identity contract is applied and provenance/freshness is verified.

## Other release blockers

- 210 prediction-ledger staging rows lack home-team IDs and 210 lack away-team IDs.
- A separate fixture-candidate audit found 105 competition-aligned candidates, 20 competition/crosswalk gaps and 85 without exact kickoff/team candidates; none verified or score-eligible.
- 7,066 non-complete records with numeric 0–0 remain excluded from settled truth.
- Combo settlement disagreement persists; Combo probabilities remain masked.
- The historical archive is not the same thing as a live current fixture feed.
- No provider API calls were made in this checkpoint; the one approved identity probe remains complete.

## Next execution gates

1. Verify final results of runs 40633801455, 40633801419 and 40633801353.
2. If the staging adapter tests pass, run it only on an existing, locally available/acquired staging JSONL source and preserve checksums; if no source exists in the repository/runtime, report that limitation rather than inventing rows.
3. Locate an authoritative newer current-feed manifest/run record. The visible release list did not show a later Selected-50 release than 2026-10-26; live manifest status remains unresolved.
4. Populate no allowlist entries until source ID+country mapping evidence is authoritative and reviewed.
5. Publish final 50-row go/no-go matrix and completion pack before noon. Deadline does not override release gates.

## Governance

Research branch only. No production repository changes. No changes to Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected registry, ledgers or governance. No additional provider requests. Production/betting eligibility remains false.
