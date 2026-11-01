# Project Oracle — Selected-50 Execution Gate & FootyStats Entitlement Clarification

**Evidence cutoff:** 1 November 2026, 05:02 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research/reporting-only. No private archive access, authenticated provider API calls, production writes, or Oracle V1.6 changes were made.

## 1. Live repository and workflow evidence

The research branch's latest inspected PR head is `6498ad81a02232a7fba57c9e154c0a35c8506a49` (documentation correction). The latest verified successful CI run for the Market Intelligence repair was run `41263509084` against commit `7263afc0656fb635b0206ebd6c8f0edfd31094eb`.

The successful run was push-triggered. Its job completed successfully and the test step passed, but these steps were skipped because they are conditional on `workflow_dispatch`:

- explicit private-archive consent and token validation;
- pinned private archive download and SHA-256 verification;
- exact source runtime artifact download and provenance verification;
- archive-wide feature/provenance audit;
- Market Intelligence workbook rebuild;
- 50-league field-by-field audit rebuild;
- report artifact upload.

The run's artifact listing is empty. This is therefore a successful test run, **not** a successful full report rebuild. The two other inspected checks (safety contract and dry-run planner) also passed; their artifacts are unrelated to the rebuilt Market Intelligence workbook.

The branch workflow file is a manual-dispatch workflow with the rebuild stages guarded by `github.event_name == 'workflow_dispatch'`. The connected GitHub actions available in this session support repository reads and file writes, but do not expose a workflow-dispatch action. No dispatch is claimed.

## 2. Branch integration guard

The live comparison reports the research branch as diverged from `main`: 1,564 commits ahead and 28 behind at the inspected comparison point. Open PR #31 is titled **Research-only: FootyStats-first dynamic identity resolver for selected 50**; its own description says the draft must not be merged into production as-is.

This PR is not a clean release vehicle for the Market Intelligence reporting work. Do not merge the entire branch or retarget the PR as a shortcut. Any future integration should isolate the required report-only commits and pass the normal review and governance gates.

## 3. FootyStats public package-capacity discrepancy

Official FootyStats public product pages currently show different Hobby league caps by locale:

| Official page | Hobby maximum leagues | Hobby requests/hour |
|---|---:|---:|
| English | 50 | 1,800 |
| Dutch | 50 | 1,800 |
| French | 50 | 1,800 |
| Arabic | 40 | 1,800 |

The English page also lists Serious at 150 leagues and 3,600 requests/hour. The API setup guide says users select the leagues available to their package and that selections can be changed monthly.

This discrepancy means public marketing-page values are not a substitute for the account's actual entitlement. The active subscription tier, selected league allocation, request limit and remaining allowance have **not** been verified. If the 50 selected competitions are 50 distinct active leagues and the account is Hobby with a 50-league cap, the selection would be at the published maximum; do not assume that this is the user's account state.

Official references:
- https://footystats.org/api
- https://footystats.org/nl/api
- https://footystats.org/fr/api
- https://footystats.org/ara/api
- https://footystats.org/api/documentations/setup-the-api

## 4. Proposed bounded xG capture budget (planning only)

The existing capture specification proposes four pre-kickoff observations (approximately T-24h, T-60m, T-20m, T-5m) and an optional post-kickoff diagnostic (approximately T+20–25m). Assuming one Match Details request per fixture per checkpoint:

| Pilot fixtures | Pre-kickoff requests | Optional post-kickoff requests | Maximum planned requests |
|---:|---:|---:|---:|
| 5 | 20 | 5 | 25 |
| 10 | 40 | 10 | 50 |
| 20 | 80 | 20 | 100 |

This is a conservative planning estimate, not a verified provider billing rule. Actual request count depends on the endpoint and retrieval method. The published 1,800/hour Hobby rate limit does not establish the user's account entitlement, credit balance, or per-call cost.

**No pilot has been run.** Before any authenticated call, require:
1. written or account-screen confirmation of the active package and all 50 selected league allocations;
2. the account's actual rate limit and remaining request/credit allowance;
3. provider confirmation of the three `*_xg_prematch` field definitions, first-availability timing, revision policy and historical snapshot capability;
4. explicit approval of the pilot fixture sample, cadence and maximum request budget.

## 5. Provider clarification request (draft; not sent)

Please confirm, for `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch`:

1. The exact definition, unit and calculation method of each field.
2. The first time each value becomes available relative to fixture kickoff.
3. Whether a value can be backfilled or revised after publication, kickoff or full-time.
4. Whether an immutable historical value, `created_at`, `updated_at`, `effective_at`, revision ID or snapshot ID can be retrieved.
5. Whether `max_time` affects these exact match-level xG fields, and if so whether it returns the value effective at the supplied timestamp.
6. Whether a historical export exists with one pre-kickoff snapshot and its verifiable as-of time per fixture.
7. The active subscription tier, selected-league limit, currently enabled league allocation, request rate limit and request/credit cost for the proposed endpoints.

A completed-match response that currently contains a field ending in `_prematch` is not, by itself, proof that the value was available before kickoff.

## 6. Current Selected-50 controls remain unchanged

- Field-level audit baseline: 50 selected league-season groups, 325 field occurrences, 16,250 league-field scope records, 965 final exception records after report-only normalisation, and zero unmapped rows.
- Existing CI: report tests passed (21 Market Intelligence + 6 goal-market research + 3 field-coverage tests); the full rebuild steps did not run.
- Historical xG: 434 upcoming fixture candidates, zero verified capture timestamps, all quarantined.
- Production eligibility: zero.
- Betting eligibility: zero.
- Oracle V1.6 logic, probabilities, thresholds, calibration and market definitions: unchanged.

## 7. Single next execution gate

Run the existing manual-dispatch report rebuild on the governed research branch only after the user explicitly confirms read-only use of the pinned private archive and the existing repository secret is available. Then verify the workflow-generated workbook and CSV artifacts. Separately, obtain FootyStats' written field-semantics and account-entitlement response before authorising any prospective xG capture.

Until those gates pass, do not promote the research branch, run authenticated provider calls, or use any xG values in backtesting, forecasting, calibration or betting.


---

## 8. Execution update — full Selected-50 repair completed (1 November 2026, 05:22 SAST)

The previously outstanding manual report rebuild has now been executed successfully. This update supersedes the earlier statement in Sections 1 and 7 that no dispatch had occurred.

### Verified GitHub Actions execution

- Workflow: `Oracle Selected-50 Market Intelligence Report Repair`
- Event: `workflow_dispatch`
- Run: `41268816105`
- Job: `124737140818` (`market-intelligence-repair`)
- Result: `completed / success`
- Branch: `research/oracle-50-league-readiness-audit`
- Workflow head SHA: `a1daa35249bd1af92f496f5bdeb3bc572a56364e`
- Artifact: `oracle-selected50-market-intelligence-repair` (ID `13068825279`)
- Artifact SHA-256: `bf75ba3fb17ed6b6ef432369e65a0ecca717161d76fef16bfa834ab086d3d7e1`
- Artifact size: 2,868,542 bytes.

The job completed all guarded stages: explicit archive-read guard, pinned archive download and SHA-256 verification, exact runtime artifact provenance and digest verification, tests, archive feature audit, goal-market research, Market Intelligence rebuild, Selected-50 field audit and artifact upload.

Source runtime:
- Run `41175230838`, completed successfully on this branch.
- Source commit: `ea3f46dab4e54b71a818ab8d8723f36426e36bef`.
- Source runtime artifact ID: `13032880970`.
- Source artifact SHA-256: `e4bca38c8ab8e6afd5c23d241e4b55fe3ce6277e656172e8cda910718c897ae0`.
- Runtime provenance verified 434 fixture rows, 50 governed selected season IDs and 46 fixture-bearing groups.
- The report-repair job verified the exact runtime run, branch, commit, source report hash, pinned archive hash and artifact digest before processing.

Pinned archive:
- Release: `research-selected50-footystats-history-40375285207`.
- SHA-256 verified: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- 59,049 match records across 200 season folders; 51,983 records have an allowed finished status and complete scores; zero parse errors.
- Ingestion manifest rows: **0**.
- Provider API calls during this run: **0**.

### Rebuilt Market Intelligence and field audit

The uploaded workbook and QA files report:

- 434 runtime rows and 434 report rows.
- 434 exact archive joins; zero unmatched/quarantined join rows.
- 50 selected league-season groups; 46 with fixtures in the seven-day horizon and four with no fixtures in that horizon.
- 38-column output schema gate: PASS.
- All nine required evidence sheets present; zero unmapped source rows.
- 325 field occurrences audited across nine sheets.
- 16,250 league/field matrix rows.
- 965 exception rows: 770 explicitly unavailable/blocked, 99 partial-value coverage, 96 no usable values.
- The earlier local 1,090-exception count is superseded by this workflow-generated 965-row exception register. Use the workflow artifact as the current source of truth; do not combine the counts.
- Schedule reconciliation remains `REVIEW_REQUIRED`: 415 matches and 19 kickoff discrepancies.

The 965 exception rows are field-scope exceptions, not missing fixtures. Of the 770 explicitly blocked rows, 644 correspond to 14 unsupported market fields across the 46 fixture-bearing groups. The three currently supported raw research markets each have 410/434 outputs; 24 fixtures are blocked by missing required feature history. The 12 experimental goal-market estimates blocked by the minimum league-baseline gate remain blocked.

Field-audit output hashes:
- Workbook: `a39030b4c7bd37dc2e37c9d53962a70cce069c309e3f51c7c77f7edcac917f20`.
- 50 × field matrix: `607819ef76ea3ca1b64a78a3ca17b9b7e6d0f34faf7279956e9aa8f06a4001dc`.
- Field summary: `1b06178969ecd315871f756386477b6dad258276bb9a2a35cbb6769efe1e4ca8`.
- Exception register: `03afa33e839b1fe2908f4a3d4c43bf1c11a4b6803b88ec5e87c196b7f8ddea26`.

### FootyStats xG — provenance remains blocked

The archive-wide summary reports non-empty values for each of `team_a_xg_prematch`, `team_b_xg_prematch` and `total_xg_prematch` in 59,049/59,049 archive records. These are field-presence counts, not proof of numeric validity or pre-kickoff availability.

The decisive provenance gap remains:
- archive ingestion manifest rows: 0;
- upcoming fixture audit rows: 434;
- numeric home/away/total pre-match-labelled xG: 434/434 for each field;
- verified xG capture timestamps: 0/434;
- prediction-eligible xG rows: 0;
- betting-eligible xG rows: 0.

All 434 candidates remain `UNVERIFIED_NO_CAPTURE_TIMESTAMP` and `QUARANTINED_RESEARCH_AUDIT_ONLY`. The completed-match API example and `max_time` documentation still do not establish immutable historical per-fixture xG snapshots or revision history. No authenticated FootyStats calls or credits were used.

### Additional reporting gap confirmed: fixture orientation

The verified source runtime's snapshot candidate trace contains 2,262 rows, including 503 with `no_home_away=1`. An exact one-to-one join to the 434 runtime fixtures finds **66/434** with this flag.

The current report-builder script does not reference `no_home_away`, so these 66 fixtures are not explicitly surfaced in the Market Intelligence workbook for orientation review. FootyStats documents the flag as meaning there is no home/away distinction for that match; it must not be reinterpreted automatically as a neutral-venue flag. This is a report-only follow-up: expose an orientation status and flag home/away-oriented markets for review without changing or recalculating any probabilities.

### Governance

- All 50 league groups remain `NOT_ELIGIBLE` for production and betting.
- xG remains quarantined.
- The workflow used only the pinned archive and existing runtime artifact; provider API calls = 0.
- No Oracle V1.6 production logic, probabilities, thresholds or calibration were changed.
- The new workbook and all research outputs remain non-production/non-betting eligible.

### Next actions

1. Add a report-only fixture-orientation field sourced from the exact snapshot join, with regression tests; do not alter model outputs.
2. Resolve the 19 schedule conflicts using authoritative kickoff evidence; do not auto-correct source times.
3. Obtain FootyStats' written definition, publication timing, post-publication revision policy, historical snapshot capability and account-entitlement confirmation. Only then consider a separately approved, bounded prospective capture pilot.
