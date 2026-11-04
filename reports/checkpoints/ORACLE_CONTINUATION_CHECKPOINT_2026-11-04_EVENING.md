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

## Evening automation continuation — central FootyStats gateway implemented (2026-11-04)

### Latest live state
- Branch HEAD after this update: `c7493b9f721b910522f6db71b9625882f5abcbc5`.
- The provider catalogue reconciliation confirms 49 selected leagues, 756 catalogue season records and 182 2024-forward season partitions.
- Important canonical mapping distinction: the current reconciliation has 44 exact-name country/competition pairs versus the prior manifest, 22 human-review-only canonical ID candidates, 22 no-match rows in the protected 27-league registry, five newly selected leagues not assessed against that registry, six prior selected leagues absent, **zero approved Oracle canonical mappings**, and zero verified provider parent competition IDs. Do not report canonical league mapping as complete.
- The current FootyStats selected catalogue is the source of truth for this research lane; do not silently force it to 50.

### New central endpoint preflight implementation
- Added `scripts/footystats_budgeted_endpoint_preflight.py`.
- Added `.github/workflows/footystats-global-budgeted-endpoint-preflight.yml`, manual-dispatch only, serialized by `footystats-global-api-gateway`.
- Added `.github/workflows/footystats-budgeted-preflight-contract-tests.yml` for fast isolated contract testing.
- Added `tests/test_footystats_budgeted_endpoint_preflight.py` and central gateway/legacy path assertions in `tests/test_footystats_ingestion_workflow_contract.py`.
- Updated `.github/workflows/oracle-selected50-contract-tests.yml` to include the new preflight tests.
- Updated `docs/PROJECT_ORACLE_EXECUTION_PROTOCOL.md` Section 10, plus:
  - `reports/ORACLE_FOOTYSTATS_BUDGETED_PREFLIGHT_GATEWAY_2026-11-04.md`
  - `reports/oracle-footystats-current-catalogue-reconciliation-2026-11-04.md`

### Request and data controls
- Absolute FootyStats ceiling: 1,800 requests in any rolling 60 minutes.
- Operational cap: 1,500 with 300 headroom.
- Durable timestamp-only reservation is committed before any provider call; the ledger is `data/footystats/rolling-request-ledger.json`.
- A lower provider `request_limit` is binding. `request_remaining` is never treated as monthly credit evidence.
- No retries; stop and checkpoint on 429/401/403, provider failure, transport error, malformed response, pagination failure or identity mismatch.
- The preflight keeps raw responses in memory and writes only sanitized field/pagination metadata and response hashes. It does not write raw payloads to the public repository or protected private archive.
- The current ledger still has only the earlier catalogue request timestamp (2026-11-04T14:34:00Z) and no active reservations. No new provider API request was made by this implementation run.
- Full raw-data ingestion remains gated until the protected private archive write path is explicitly authorized and validated.

### Test evidence and limitation
- Targeted workflow run `41864509844`, job `126695135837`.
- The job log records successful py_compile and:
  - 9 request-budget tests passed;
  - 8 endpoint pagination tests passed;
  - 7 sanitized preflight tests passed;
  - 11 workflow/legacy-isolation tests passed.
- Total: 35 tests reported OK in the job log. The GitHub run/job metadata reader still reports queued/no final conclusion despite the completed test and cleanup log entries. Do not label the Actions run formally completed until a final conclusion is retrievable.

### Next execution
1. Manually dispatch **FootyStats Global Budgeted Endpoint Preflight (Research Only)** with `confirm_provider_api_usage=true`, `max_seasons=182`, `max_requests=1000`. The available GitHub connector can inspect runs/logs but cannot dispatch workflows.
2. Inspect the sanitized per-season endpoint/field report. It checks matches page 1, teams page 1, tables, season and one exact match-details/H2H sample where available. It does not claim full pagination or full ingestion.
3. Resolve canonical mapping candidates and the six legacy exclusions/five new competitions with explicit owner approval.
4. Validate protected private archive write authorization before building/running full raw historical ingestion.
5. Keep standings fixture-time validity, H2H chronology, recent/home-away form and xG provenance as separate fail-closed gates.
6. Preserve frozen Oracle V1.6 production logic/probabilities and research/betting eligibility false.

## Final continuation delta — budgeted gateway and ingestion manifest (2026-11-04)

- Live branch HEAD before this checkpoint update: `176305f3a32ad0bdaf8a60416d97122de2d6d9f4`.
- Added offline full-ingestion planner `scripts/build_footystats_full_ingestion_manifest.py`. It creates exact-ID paginated match/team tasks plus one current-snapshot tables and season request per preflight-verified season, retains blocked rows for every other planned season, and divides planned work into batches capped at 1,500 requests.
- The planner does not call the API or persist raw data. It marks private raw archive writing as required and leaves production/betting eligibility false. H2H, recent form and home/away form are derived from the complete exact chronological match spine; fixture-time standings remain unverified and xG quarantined.
- The central manual-dispatch preflight workflow now invokes this planner after the preflight attempt, then commits/uploads the sanitized report and manifest.
- Latest targeted contract log: run `41865887561`, job `126699886190`. The log shows py_compile and 42 tests OK: 6 manifest planner, 9 rolling budget, 8 endpoint pagination, 7 preflight, 12 workflow/legacy-path tests. GitHub run metadata still reports queued/no final conclusion despite the completed test and cleanup log entries; treat the logs as evidence but do not claim formal Actions completion.
- No provider API requests were made. The public rolling ledger still has only the earlier catalogue request timestamp and no active reservations.
- No raw data was written to the public repository or protected private archive. No Oracle V1.6 production logic/probabilities/thresholds/calibration/ledgers/eligibility were changed.
- Remaining live gate: manually dispatch **FootyStats Global Budgeted Endpoint Preflight (Research Only)** with `confirm_provider_api_usage=true`, `max_seasons=182`, `max_requests=1000`. The available GitHub connection cannot dispatch it.
- Canonical mapping remains unapproved: current catalogue reconciliation reports zero approved Oracle canonical mappings and zero verified provider parent competition IDs. Do not mark the mapping complete until the exact IDs and scope decisions are approved.

## Saved-state refresh after documentation reconciliation

- Latest live research branch HEAD: `b472f5371140f4d4f6f9a92aca3834a36cd7c447`.
- Gateway implementation report refreshed at `reports/ORACLE_FOOTYSTATS_BUDGETED_PREFLIGHT_GATEWAY_2026-11-04.md`.
- Current catalogue reconciliation report updated with the offline ingestion-manifest design and 42-test evidence.
- Latest targeted test evidence remains run `41865887561`, job `126699886190`: the job log shows 42 tests passing. GitHub run metadata still has no final conclusion; do not overstate it as formally completed.
- No FootyStats API calls, raw payload writes, private archive writes, or production model changes occurred in this continuation.
- The only live external action required to progress endpoint evidence is manual dispatch of the central preflight workflow. Full raw ingestion remains gated by private archive write authorization.
