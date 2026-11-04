# Project Oracle — continuation handover checkpoint (2026-11-04 evening)

## Live state at checkpoint
- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`.
- Governed research branch: `research/oracle-50-league-readiness-audit`.
- Branch HEAD recovered immediately before this checkpoint: `d9e1545220c65b9950a0605489a76943424a4658`.
- This checkpoint records continuity and execution instructions only; it does not claim new ingestion or league readiness.

## Frozen production governance
- Oracle V1.6 production logic, production probabilities, thresholds, calibration, ledgers and betting eligibility remain frozen and must not be modified.
- All new mapping, ingestion, data-quality and reporting work remains research-only (`production_eligible=false`, `betting_eligible=false`).
- No fabricated data, fuzzy/name-only joins, silent drops, imputation of required fields, or unsupported accuracy/readiness claims.
- Raw provider data and credentials must not be committed to the public research repository. Use only the approved private destination for raw data.
- Keep xG quarantined unless fixture-level point-in-time capture provenance is verified.

## FootyStats catalogue and completed staging
- The selected-league catalogue artifact was verified and staged through `.github/workflows/stage-footystats-provider-catalogue.yml`.
- Catalogue scope is explicitly `chosen_leagues_only`; it represents the account's selected catalogue, not proof of every league offered by FootyStats.
- Verified catalogue size: 49 unique league names, 756 league-season rows and 756 unique provider season IDs.
- Registry/data files are staged under `data/footystats/`, with provenance documentation.
- Staging workflow run `41852118541` completed successfully; offline contract-test run `41852117772` completed successfully. These validate catalogue staging/contracts only, not historical endpoint ingestion.
- A date-window analysis of the staged catalogue identified 182 season rows across the 49 selected leagues intersecting 2024-01-01 through 2026-11-04. Fixture-level kickoff filters must still enforce the exact requested date window; do not ingest pre-2024 fixtures merely because a 2023/24 season is included.

## User-confirmed API usage limit
- User confirmed FootyStats credits are available for this work, provided the hard limit is respected.
- Enforce a single shared global ceiling of 1,800 API requests in every rolling 60-minute window across all Oracle automations, workflows and endpoints.
- Use durable shared accounting, reserved headroom, checkpointing and bounded retries. Parallel tasks must never create separate counters or evade the ceiling.
- Stop on 429/401/403, permission failures, data-integrity failures, or evidence that the request ceiling could be exceeded. Do not use uncontrolled retries.

## Active hourly workstreams
1. `Oracle hourly completion`: existing hourly continuation task, scheduled from 2026-11-04 17:00 SAST through 2026-11-05 12:00 SAST.
2. `Oracle league mapping & data audit`: additional task created at the user's request, scheduled hourly from 2026-11-04 17:45 SAST through 2026-11-05 12:00 SAST.
- The second task is intentionally scoped to provider-to-Oracle league/season mapping, 2024-forward historical coverage, endpoint/field investigation, resumable ingestion and QA.
- Both tasks must coordinate on the same live branch, inspect HEAD before commits, avoid conflicting edits and share the global API request counter.
- Automation schedule creation is confirmed. At the time of this checkpoint, the new task had no recorded run yet; schedule creation is not evidence that background work has completed.

## Immediate execution order
1. Recover latest branch HEAD and inspect the two latest automation run results before making changes.
2. Build and test a catalogue-driven historical season planner for the exact 2024-01-01 to current date window; parse year tokens robustly and retain exact provider season IDs.
3. Inspect authoritative FootyStats API endpoint documentation and existing adapters before writing ingestion code. Establish actual endpoint parameters, pagination semantics, request cost and field availability; do not guess.
4. Implement the shared rolling-hour request ledger and resumable checkpoints before broad ingestion.
5. Build exact provider league/season/team/fixture mappings and field-level coverage evidence. Validate pagination and kickoff chronology.
6. Store raw data only in the approved private destination; publish sanitized metadata/QA to this research branch.
7. Validate fixtures, results, team identity, H2H, recent form, home/away form, standings, goals and xG separately. xG remains quarantined absent valid point-in-time provenance.
8. Rebuild Master OMI / Visual Intelligence outputs only from verified inputs and the governed template; keep missing data explicit.
9. Run tests, inspect workflow logs and artifacts, commit evidence-based changes, and report exact run IDs/commit SHAs.

## Explicit status — do not overstate
- Catalogue staging: VERIFIED.
- Dynamic catalogue registry: STAGED.
- Offline contract tests for the staging change: VERIFIED successful in run `41852117772`.
- Full 2024-forward historical ingestion: NOT YET COMPLETED.
- Provider endpoint coverage for all selected leagues/seasons: NOT YET VERIFIED.
- Complete canonical team/fixture crosswalk: NOT YET VERIFIED.
- Full league readiness for Oracle probability calculations: NOT YET VERIFIED.
- Master OMI completion for the full historical scope: NOT YET VERIFIED.
- No claim is made here that the two new hourly runs have executed successfully.

## Continuation rule
Continue from the live research branch and this checkpoint. Preserve all previous artifacts and snapshots. Do not restart or redesign Project Oracle. Do not modify production logic. Prioritise evidence-backed mapping and historical coverage from 2024 onward, and stop only at verified completion or a genuine access/data-integrity blocker.
