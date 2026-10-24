# Oracle Private Expansion Run #206 — Source-Level Failure Surface Review
- Review date: 2026-10-25 (SAST)
- Scope: read-only inspection of the private workflow source after run #206 failed.
- Production impact: none; no private workflow or model files changed.

## Verified run evidence
- Run: https://github.com/dtnzv5by8c-ship-it/oracle-football-data/actions/runs/40125710200
- Workflow: `.github/workflows/oracle_autonomous_league_expansion.yml`
- Workflow file blob SHA on `main`: `2ee55125c00759f90f48ec4dc965530050aa2225`
- Run status: `completed/failure`; job `prepare` failed; `controlled`, `controlled_gate`, `expansion` and `finalize` were skipped.
- Job ID: `120966544550`.
- Direct job-log retrieval was retried on 2026-10-25 and returned Azure `BlobNotFound` (HTTP 404). The log is unavailable through the current connector; the failure step and exception cannot be established from run evidence.

## Source-level inspection of prepare
The `prepare` job:
1. Checks whether `research/oracle_walk_forward/full_league_expansion_manifest.json` already says `COMPLETE` or `COMPLETE_RESEARCH_ONLY`; if so, it exits normally with `proceed=false`.
2. Otherwise calls GitHub REST API `/actions/workflows/374216126/runs?per_page=20&exclude_pull_requests=true` to look for a prior completed run.
3. For candidate completed runs, calls `/actions/runs/{id}/artifacts?per_page=100` to find five required `oracle-v2-controlled-*` artifacts.
4. Uses `urllib.request.urlopen(..., timeout=20)` in a helper with no explicit exception handling for HTTP errors, authorization failures, API rate limits, timeouts or transport errors.

## Diagnostic conclusion (not a proven root cause)
Because logs are unavailable, it is **not possible to attribute run #206's failure to a specific command**. The API lookup in the prepare gate is a concrete failure surface: an HTTP/authorization/rate-limit/transport error would raise an uncaught exception and fail the job. This is a hypothesis for targeted diagnosis, not a verified root cause. A normal API response with no matching artifacts should instead leave the resume ID empty and allow the controlled jobs to run.

## Safe next diagnostic
When logs are available, identify the failing step and exact exception before changing code. If the failure is the API lookup, a future reporting-only fix could add explicit error classification and a safe fallback to an empty resume ID, but only after confirming the failure mode and preserving artifact selection checks. Do not bypass the controlled gate, reuse unverified artifacts, or modify production model logic/weights/probabilities/thresholds/calibration/registry/ledgers.

## Audit context
- The quality-matrix workflow run #4 completed successfully and published its research artifact/release, but this is a separate workflow and does not repair run #206.
- The connected GitHub tool surface does not expose a workflow-dispatch action for this audit run; no rerun was triggered.
- The 50-league audit remains incomplete: 22 candidate mappings require review, 28 selected competitions remain unresolved, provider-ID-to-fixture-to-canonical-team joins are 0/50, and all selected-ID-specific market readiness remains unverified or blocked.

## Governance
Read-only inspection only. No production or private repository writes occurred during this source-level review.
