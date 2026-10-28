# Safe Current-Report Snapshot Provenance Guard
**28 October 2026 — 19:18 SAST**

## Repository state and scope

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Branch: `research/oracle-50-league-readiness-audit`
- Branch head before this change: `a6344589675cf25322c16c2439c675311d9a7389`
- Safe current-report code change: `7691029335a60eb6d320f656253006e14e238853`
- Regression-test change: `8c18d7c1cd349b945bb6a29a3a7eaacc7cf00ad7`

This is a report-only research utility change. No model runtime, prediction, calibration, production ledger, or governance code was changed.

## Defect

`scripts/build_selected50_safe_current_fixture_report.py` previously accepted a saved current-fixture snapshot without validating `retrieved_utc`. A stale, future-dated, timezone-naive, or missing timestamp could still produce a report labelled as a current report. The output also did not carry the exact snapshot-file digest or age, making it harder to audit the evidence used for the report.

## Change implemented

The builder now:

- Requires a valid timezone-aware ISO-8601 `retrieved_utc`.
- Rejects retrieval timestamps later than the report's `--as-of-utc` time.
- Rejects snapshots older than 24 hours relative to the report's as-of time.
- Requires `per_season` and `fixture_rows` to be lists.
- Computes SHA-256 over the exact snapshot file bytes.
- Adds normalized retrieval time, age in seconds, snapshot SHA-256, and `PASS_FRESH_TIMEZONE_AWARE` provenance status to the QA JSON and each exact-joined report row.

The guard uses the report's deterministic as-of timestamp when provided, so the contract is reproducible in tests. The 24-hour rule is a freshness guard for this report-only utility, not a claim that data under 24 hours old is canonical or production-approved.

## Validation

Local execution of the committed script/test logic:

- Existing exact-identity and fail-closed flag test: **PASS**.
- New snapshot-provenance test: **PASS**, exercising four rejection cases: missing timestamp, timezone-naive timestamp, future timestamp, and stale timestamp.
- Valid synthetic snapshot: exact SHA-256 is reported, age is calculated as 36,000 seconds for the 10-hour fixture, and source provenance is carried into the joined row.
- Both report eligibility fields remain `NO`.

**GitHub Actions status for the new commit is not verified in this checkpoint.** The connected GitHub status endpoint returned no status entries and the available GitHub tools do not expose a push-workflow run listing/dispatch operation. Do not describe this change as CI-passed until the public workflow run is inspected.

The public workflow is [Selected-50 Safe Current Fixture Report Contract](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/selected50-safe-current-report-contract.yml). It is push-triggered by changes to this script or its test and requires no inputs, secrets, private archive, or provider calls.

## Existing Oracle blockers unchanged

- 25 runtime fixtures remain blocked by insufficient five-match venue-specific history; no imputation or threshold relaxation.
- Combo predictor (Double Chance AND 2–4 goals inclusive) still disagrees with the existing settlement helper (Double Chance AND total goals below five, including 0–1 goals). Combo probabilities remain masked.
- Canonical competition/fixture/team joins and official settlement truth remain unverified.
- Point-in-time xG/odds provenance and a fresh governed 50-league fixture slate remain unverified.
- Production and betting eligibility remain `NOT_APPROVED`.

No provider API calls, private Actions runs, production-repository writes, or production model changes were performed.
