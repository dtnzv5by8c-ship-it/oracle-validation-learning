# FootyStats cross-repository request-gateway audit — 2026-11-04

**Evidence time:** 2026-11-04 16:46 UTC  
**Implementation lane:** `research/oracle-50-league-readiness-audit` in `oracle-validation-learning`  
**Purpose:** Verify whether the approved 1,800-request rolling-hour control covers every Oracle workflow that can call FootyStats.  
**Method:** Read-only inspection of workflow YAML, repository metadata, branch refs, the current public gateway run, and the current sanitized mapping artifacts. No additional provider request was initiated by this audit.

## Executive finding

The six legacy provider workflows on the public repository's `main` branch have now been replaced with fail-closed stubs, and the central gateway is registered on `main`. This resolves the previously identified public-repository dispatch/bypass problem.

However, the private controlled data repository `dtnzv5by8c-ship-it/oracle-football-data` still contains an independently dispatchable FootyStats ingestion workflow. It calls the provider directly and does not use the public research branch's rolling request ledger, reservation mechanism, or concurrency group. Therefore, the hard global 1,800-request ceiling is **not yet proven across all Oracle repositories and workflows**.

No in-progress GitHub Actions run was returned for the private repository at the evidence time. The independent workflow nevertheless remains executable and is a bypass risk if manually or push-triggered.

## 1. Public repository controls — verified

Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`

- `main` HEAD: `fc998b224b2cce924355af11bc7c153e8d519889`.
- Governed research branch HEAD at audit time: `59242831fe75ee876df21559dc602d9d7ff2532d`.
- The six previously identified legacy workflows on `main` now contain only fail-closed stubs, with no FootyStats API host or API-key reference:
  - `.github/workflows/footystats-api-catalogue-audit.yml`
  - `.github/workflows/footystats-api-endpoint-coverage-audit.yml`
  - `.github/workflows/footystats-full-selected-league-historical-ingestion.yml`
  - `.github/workflows/footystats-full-universe-catalogue-transfer.yml`
  - `.github/workflows/footystats-historical-season-coverage-audit.yml`
  - `.github/workflows/oracle-selected50-footystats-live-ingestion.yml`
- The bounded endpoint probe and one-call identity probe are also disabled stubs on `main`.
- The central `.github/workflows/footystats-global-budgeted-endpoint-preflight.yml` is registered on `main`, checks out the governed research branch, and uses concurrency group `footystats-global-api-gateway`.

### Current central preflight run

Run [41869437030](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41869437030) was in progress at evidence time.

Observed job state:
- Input approval and numeric-limit validation: passed.
- Current-date 2024-forward season plan: passed.
- Durable 1,000-request reservation: passed and committed before provider access.
- Sanitized endpoint/field preflight: in progress.
- Manifest generation, final ledger commit and artifact upload: pending.

The durable branch ledger records reservation `gha-41869437030-1`, count 1,000, with a two-hour fail-closed reservation lifetime. The operational ceiling is 1,500 and the hard rolling-hour limit is 1,800, preserving 300 requests of headroom. The run's actual request timestamps and endpoint outcomes had not yet been committed at evidence time; do not infer the consumed request count from the reservation alone.

The run is the only in-progress public-repository Actions run observed at evidence time. Do not start another FootyStats run while it remains active.

## 2. Private repository bypass — confirmed

Repository: `dtnzv5by8c-ship-it/oracle-football-data`  
Visibility: private  
`main` HEAD at audit time: `256493c8974863e4b6c01a5f2dcc2c18530b603e`.

The repository README describes this as the controlled Oracle data foundation. Its workflow `.github/workflows/footystats-private-historical-ingestion.yml` was added by commit `cb89e5bd1c24810fe821a6b2c3c2c1c19272b381` on 2026-10-20 and remains present on `main`.

Static inspection confirms that this workflow:
- Has both `workflow_dispatch` and a push trigger on the workflow file.
- Reads `secrets.FOOTYSTATS_API_KEY` and calls `https://api.football-data-api.com/` directly.
- Maintains a process-local `REQUESTS` variable only; it does not read, reserve, update, or finalize the public rolling request ledger.
- Increments that local counter only after a successful HTTP response, so failed attempts are not durably counted.
- Retries HTTP 429 and 500/502/503/504 responses up to three attempts, contrary to the required stop-on-429 rule.
- Uses 0.12-second pacing and has no shared global concurrency/lock.
- Uses a hard-coded 27-code alias map rather than the current 49-league selected catalogue.
- Selects seasons only when the season start year is in `{2024, 2025, 2026}`; this excludes 2023/24 season partitions containing fixtures from 2024.
- Does not apply the explicit 2024-01-01 through current-date kickoff filter.
- Follows `max_page` for matches but does not validate provider page number, total row count, exact expected page size, or final pagination completeness. It does not paginate the teams endpoint.
- Saves complete provider records as JSON inside a private GitHub Actions artifact with 90-day retention. It is not a resumable, durable raw-data archive.
- Reports xG field presence only; it does not establish point-in-time capture or revision provenance.
- Does not reconstruct fixture-time standings, chronological H2H, or strict pre-kickoff recent/home-away form.

A repository code search found this as the private repository's direct FootyStats API host/secret workflow. The private repository's in-progress Actions query returned zero runs at evidence time; that does not make the workflow safe to dispatch.

**Conclusion:** This private workflow must not be used for the 49-league 2024-forward acquisition until it is retired or refactored to use the same globally shared reservation service and fail-closed request policy. In particular, it must stop retrying 429 responses.

## 3. Why the global ceiling is not yet guaranteed

The public gateway's concurrency group and JSON ledger protect the public repository's central workflow. They do not, by themselves, coordinate a separate private repository runner. The private workflow does not share either control.

Consequently:
- The public gateway's 1,000-request reservation is valid for its own controlled run.
- It is not evidence that another repository cannot make provider calls concurrently.
- The current hard 1,800-per-rolling-60-minute requirement cannot be certified across all Oracle workflows until the private workflow is gated by the same atomic global reservation/accounting service or is made fail-closed.

No new provider call was made by this audit. No private repository file, secret, archive, or workflow was modified.

## 4. Current catalogue and canonical mapping checkpoint

The current FootyStats `chosen_leagues_only=true` catalogue artifact records:
- 49 provider leagues.
- 756 provider league-season catalogue rows.
- 182 exact provider season IDs intersecting 2024-01-01 through 2026-11-04 inclusive.
- 49 leagues represented in the historical season plan.

The 49-row crosswalk contains exact provider season IDs and season labels. It does **not** complete Oracle canonical mapping:
- 22 provider leagues have prior canonical-code candidates requiring owner approval.
- 22 have no match in the protected 27-league registry.
- 5 newly selected leagues have not yet been assessed against an owner-approved expanded registry.
- Approved Oracle canonical mappings: 0.
- Verified provider parent competition IDs: 0.

The current selected catalogue also differs from the prior 50-league manifest: 44 exact country/competition matches, six legacy entries absent from the current selected catalogue, and five new selected entries. No substitution or automatic re-addition is justified by this catalogue comparison.

Machine-readable evidence:
- `data/footystats/current-catalogue-reconciliation-2026-11-04/current-catalogue-provider-to-oracle-candidate-crosswalk.csv`
- `data/footystats/current-catalogue-reconciliation-2026-11-04/current-catalogue-reconciliation-summary.json`
- `data/footystats/historical-season-plan-2024-2026/season-plan.csv`

## 5. Historical data coverage and endpoint limits

The current 182-season plan is an acquisition worklist, not evidence of 2024-forward data ingestion.

The active preflight checks only endpoint/field samples (matches page 1, teams page 1, tables, season and one match-detail/H2H sample). It does not claim full pagination or full historical field coverage.

Still unverified for the current 49-league / 182-season scope:
- Full fixtures/results pagination and kickoff-date filtering.
- Complete team identity and season membership.
- Full chronological match spine and exact fixture/team identity.
- H2H chronology and recent/home-away form derived with strict pre-kickoff cutoffs.
- Fixture-time standings.
- Goal-field coverage across all completed fixtures.
- xG point-in-time capture/revision provenance.

xG remains quarantined. Raw provider data remains excluded from the public research repository. The private repository is the controlled data foundation, but this audit does not approve a new raw-data write path or bypass its existing archive safeguards.

## 6. Safe next actions

1. Let central preflight run `41869437030` finish; inspect its final job logs, sanitized report, request timestamps, endpoint outcomes and manifest before another provider run.
2. Keep every other FootyStats request path stopped while the central run is active.
3. Do not dispatch `footystats-private-historical-ingestion.yml`. Its local counter and retry behavior are incompatible with the global policy.
4. Keep implementation changes on `research/oracle-50-league-readiness-audit`. This audit did not modify the private repository because the workstream is restricted to the governed research branch.
5. Before any full ingestion, obtain a single cross-repository budget gate that all provider-capable workflows must use, with atomic durable reservation, exact attempt accounting (including failed requests), at least 300 headroom, no retries on 429/401/403, and a fail-closed stop when the shared service is unavailable.
6. Resolve owner-approved canonical IDs for the 22 candidate rows and provide an authoritative expanded Oracle registry for the 22 unmatched and five unassessed rows.
7. Only after the global gate and approved private archive write path are validated, build resumable page-level ingestion with exact row-count/pagination checks and per-season checkpoints.

## Governance

Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility were not changed by this audit. Research outputs remain non-production and non-betting-eligible. No league readiness is claimed.
