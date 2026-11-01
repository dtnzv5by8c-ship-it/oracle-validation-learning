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
