# Oracle Selected-50 Archive QA Milestone — 2026-10-25

## Status

Research-only validation. Production readiness remains NOT GRANTED. Oracle production logic, production probabilities, calibration and thresholds were not changed.

## Verified workflow results

- Private archive QA: success — https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40179979282
- Regression/dry-run planner: success — https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40179979357
- QA artifact: `oracle-selected50-private-archive-qa`, sanitized-only, short retention.
- Private source release: `research-selected50-footystats-ingestion-20261025`.

## Archive QA findings

- 50/50 selected seasons have `INGESTED` manifest status and all required JSON files parse.
- 14,051 match records; 14,051 unique season/fixture-ID pairs; no duplicate fixture-ID pairs detected within seasons.
- Kickoff-like field, team-ID pair, team-name pair, and explicit score pair exist in all 14,051 records.
- Observed date range: 2026-01-16 to 2027-06-06 UTC/string date.
- Date-based preliminary split: 6,912 records have past kickoff dates; 7,004 have future kickoff dates. The remainder fall on the current UTC date or have classification edge cases.
- Provider status values: `complete` 6,916; `incomplete` 7,083; `suspended` 52.
- Non-empty odds-named values appear in 7,330 records. This is not proof of valid bookmaker, market, timestamp, or pre-kickoff odds.
- Non-empty xG-named and prematch-xG-named values appear in all 14,051 records. This is not proof that values are genuine, correctly scaled, valid for the fixture, or available as of kick-off.
- The raw archive remains private. The QA artifact contains sanitized aggregate data and observed field names only.

## Important interpretation

A populated score pair is not sufficient evidence that a match is settled: future-dated records also contain numeric score fields, and provider status/date semantics require further verification. Likewise, field presence and non-empty values do not establish point-in-time provenance. Do not use these counts as prediction-input coverage or model accuracy.

## Existing gaps

1. **Root cause confirmed:** a one-request sanitized catalogue schema audit found the provider `league-list` objects expose `country`, `image`, `name`, and `season`, but no parent `id` field. Each season object exposes `country`, `id`, and `year`. Therefore the blank `provider_league_id` is not a failed exact season match; the provider catalogue does not expose a parent competition ID in this response shape. The ingestion workflow was updated so future ledgers explicitly record `NOT_EXPOSED_BY_CATALOGUE` rather than a blank. Do not invent or infer a parent ID.
2. The current archive covers the selected 50 season IDs, but it is not a validated prediction feature store.
3. Recent form, H2H, standings chronology, fixture identity joins, xG provenance, odds provenance, and market-specific feature readiness have not passed dedicated tests.
4. Historical prediction accuracy and calibration improvement have not been demonstrated.
5. Earlier dry-run market gates remain conservative: BTTS Yes, Double Chance, DC + Under 4.5 are NOT VERIFIED; M-1UP is BLOCKED.

## Next actions

1. Audit the exact league-list catalogue object schema and safely resolve the parent competition ID only from an explicit provider field; do not guess IDs or spend credits on a full re-ingestion just to test this.
2. Extend QA with strict status/date/score settlement rules, numeric value distributions and sample-level consistency checks that do not publish raw provider payloads.
3. Validate standings, team identity, recent form, H2H, xG and odds separately, including as-of-kickoff availability.
4. Join selected fixture IDs to Oracle prediction outputs exactly; quantify missingness and reject ambiguous/fuzzy joins.
5. Backtest only on predictions actually recorded before kick-off, settle against verified outcomes, report hit rate by market/league and calibration metrics, and compare selection filters out-of-sample.
6. Keep production model logic and probabilities unchanged until evidence is sufficient for a separately governed approval.

## Governance

No model redesign, production code change, probability change, calibration change, or production promotion is authorized by this milestone. No accuracy or profitability claim is made.


## Follow-up check — 2026-10-25 09:25 UTC

- Latest research QA and dry-run planner executions continue to pass (QA run [40180314626](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180314626); dry-run [40180445784](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180445784)).
- The follow-up exact-ID ingestion processed all 50 selected seasons successfully and made 201 provider requests, but the overall workflow ended in failure at the private-release transfer step because release tag `research-selected50-footystats-ingestion-20261025` already exists. The sanitized ledger was still uploaded; the existing private release was not overwritten. This is a packaging/transfer failure, not a provider-ingestion failure. Do not repeat the 201 requests to fix it.
- The selected-50 catalogue schema audit completed successfully. Provider `league-list` exposes no parent competition ID field; the explicit season IDs are available and matched. Future ledgers now represent this limitation as `NOT_EXPOSED_BY_CATALOGUE`.
- The latest production repository runs checked on 2026-10-25 include failures in current-data staging, prospective learning, historical intelligence, and external forecast archive. Their GitHub job records exposed no step-level diagnostics in the API response, so root cause cannot responsibly be inferred from those summaries alone. The production workflows must be diagnosed from the actual run logs before retrying or modifying them.
- No production model logic, probabilities, calibration, or thresholds were changed. Production readiness remains `NOT_GRANTED`.


## Prioritised continuation review — 2026-10-25 09:27 UTC

### Verified archive state
- The latest private-archive QA run passed after the follow-up ingestion workflow failed at release transfer: [QA run 40180314626](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180314626). This verifies the pre-existing private release can be downloaded and audited; do not spend more API credits re-ingesting merely to address the duplicate release tag.
- The follow-up ingest's provider work succeeded (50/50 seasons, 201 requests) but its newly generated package did not replace or upload to the existing private release because the workflow deliberately refuses to overwrite a tag. The sanitized artifact is available on [run 40180281634](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180281634). Existing release remains the QA input; the new archive from the failed runner was ephemeral and should be treated as not persisted.
- Latest dry-run planner passed: [run 40180625415](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40180625415).

### Production failure triage
- Recent main-branch runs checked: current-data staging [40179475855], prospective learning [40179353874], historical intelligence [40179723228], external forecast archive [40177200715]. GitHub's jobs API returns zero step summaries for these failed jobs, and the log endpoint did not return usable decoded logs. Therefore the first failing step/root cause cannot be established from the available evidence. Do not patch production scripts or retry paid/data-ingest steps based on speculation.
- Historical-intelligence workflow has explicit preconditions for the canonical historical spine and point-in-time leakage audit; the currently checked-in manifests report 12,836 matches and 12,836 pre-match states, reconciliation PASS, strict pre-match PASS, and zero leakage violations. These manifest values are dated 2026-10-02, so they are not evidence that the selected 50-league current workflow is ready.
- Next production action is a diagnostics-only rerun/inspection once usable GitHub runner logs are available, followed by fixing only a demonstrated infrastructure or script failure. Preserve production prediction logic and probabilities.

### Highest-priority remaining readiness gates
1. Keep the existing private archive as the current audited source; no additional FootyStats calls unless a specific missing field is shown to be necessary.
2. Diagnose the no-step production workflow failures with runner/job diagnostics before changing code.
3. Tighten settlement QA: date plus numeric score is not proof a fixture is finally settled. Require explicit provider final status or independently verified result.
4. Reconcile exact team/fixture identity and verify recent form, standings and H2H coverage per selected fixture.
5. Treat xG and odds as unavailable for production gating until point-in-time provenance is evidenced; non-empty values alone do not prove pre-kickoff availability.
6. Only then produce historical market metrics from prediction records demonstrably captured before kick-off and verified settlements.

Production readiness remains NOT_GRANTED; production model logic, probabilities, calibration and thresholds remain unchanged.
