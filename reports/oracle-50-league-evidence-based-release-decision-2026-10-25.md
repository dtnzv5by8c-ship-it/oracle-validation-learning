# Oracle 50-League Evidence-Based Release Decision — 2026-10-25

## Decision

**NOT GRANTED — research validation passes; production release remains blocked.**

The public contract/regression and dry-run workflows passed on candidate commit `8742baad246f7a6ab3f9a3aff7475d9ea9e1c8d9`. This proves the research contracts and no-network dry-run are operational. It does not prove the private production runner is fixed, that the canonical 50-league fixture slate is reconciled, that outcomes/features are verified, or that production accuracy is measurable.

No production model logic, production probabilities, calibration, thresholds, production code, or frozen historical baseline was changed.

## Current gate ledger

| Priority | Gate | State | Evidence / blocker |
|---|---|---|---|
| P0 | Private Actions runner diagnosis | **BLOCKED — owner diagnostics required** | Runs 40183610511 and 40190338066 failed before usable steps. Job-step API returned zero steps; log API returned `BlobNotFound`. This does not identify billing as the cause. No private rerun or spending-limit increase was attempted. |
| P0 | Isolated 50-league runtime migration contract | **PLAN/CONTRACT DEFINED; MIGRATION NOT IMPLEMENTED** | Added `config/oracle_50_league_runtime_migration_contract_v1.json` and `reports/oracle-50-league-runtime-migration-plan-2026-10-25.md`. Contract isolates `selected50_runtime_v1` from `legacy_27_league_runtime`; preserves 27 leagues / 12,836 historical fixtures; forbids changes to model logic, probabilities, calibration and thresholds; requires exact probability parity. Consumer migration and production parity remain unexecuted. |
| P1 | Canonical fixture and team identity | **BLOCKED** | No canonical fixture slate with authoritative fixture/team IDs and kickoff provenance was found in the research branch at the expected paths. Archive structural validity is not cross-source identity proof. Exact crosswalks and exception counts are still required. |
| P1 | Settlement truth | **BLOCKED** | `archive/SETTLEMENT_LEDGER.csv` contains its header only. Scores/date alone cannot qualify settlement. Final-status/source evidence and exact fixture identity are required. |
| P1 | Point-in-time feature provenance | **BLOCKED** | xG/odds-named field presence does not verify semantics, scale, source, market/bookmaker, exact fixture join or timestamp before kickoff. Current 50-row matrix keeps every production eligibility flag at `NO`. |
| P2 | Production accuracy/calibration | **BLOCKED / UNKNOWN** | `archive/PREDICTION_LEDGER.csv` contains challenger-labelled rows only; no genuine production-labelled prediction sample was identified. Settlement, scorecard and probability-error ledgers are empty/header-only. No production accuracy, calibration or ROI claim is supportable. |
| CI | Public regression + dry run | **PASS on candidate SHA** | Both final public runs below completed successfully and their job-step APIs confirm all steps passed. |

## Public workflow evidence

Candidate commit: [8742baad246f7a6ab3f9a3aff7475d9ea9e1c8d9](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/8742baad246f7a6ab3f9a3aff7475d9ea9e1c8d9)

- [Oracle Selected-50 Data Gate Contract — run 40194626027](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40194626027): **success**. Steps verified: compatibility contract tests, runtime migration contract tests, 50-row data-gate matrix regression tests, and 27-reference classification regression tests.
- [Oracle Selected-50 Dry-Run Planner — run 40194625984](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40194625984): **success**. Steps verified: dry-run generation without network calls, conservative market gates, planner/market regressions, exact catalogue resolver, prediction input contract, output validation and artifact upload.
- Earlier dry-run artifact on run 40193795700 had SHA-256 `faac4c2e47609e0b474aaedac02e5bd7e45b046a03cbd6be7e264d81d07b891b`; it predates the final migration-contract test commit, so the candidate-SHA run is the controlling CI evidence.

The migration-contract test initially failed because it checked the paid-provider guard under the wrong JSON object. The failure was read from actual public job logs, corrected, and rerun. The final candidate-SHA contract and dry-run runs both passed.

## Required owner-visible runner diagnosis

For private runs 40183610511 and 40190338066, open the run and failed job in GitHub Actions and preserve the run summary, job initialization error, runner allocation message, and any policy/billing notice. Separately inspect repository/org Actions usage and spending-limit status for the relevant time. The connected read path currently returns no step summaries and `BlobNotFound` for logs, so it cannot distinguish runner allocation, policy, billing, or another initialization failure.

**Do not rerun private workflows or change spending limits as a diagnostic.** After the owner-visible evidence identifies the cause, fix that specific cause and request explicit approval before any private execution.

## Minimum evidence needed to lift P1/P2

1. Canonical fixture slate with immutable canonical fixture ID, season ID, stable home/away team IDs, UTC kickoff, source/provider IDs, and evidence/hash.
2. Explicit source-to-canonical fixture/team crosswalk. Exact IDs only for approval; ambiguous and unmatched rows quarantined.
3. Settlement evidence per fixture: source, final status, valid score, settlement/retrieval timestamps and evidence reference. Special markets such as M-1UP also need chronological goal truth.
4. Feature provenance ledger per value: source and payload hash, field meaning, scale/units, fixture join, market/bookmaker where relevant, source timestamp, captured timestamp and proof it existed before kickoff.
5. Immutable pre-kickoff production prediction rows with model/version, market, probability, fixture key, feature snapshot, prediction timestamp and code/calibration IDs; then exact-key joins to the verified settlement ledger. Challenger rows must not be relabelled as production.
6. Reproducible production validation with sample size, coverage, accuracy, Brier score, log loss, calibration and, only where valid contemporaneous odds and settlement rules exist, ROI.

## Release rule

Production remains **NOT_GRANTED** until all P0/P1 gates and the P2 evidence gate pass, public regression/dry-run is green for the reviewed candidate, legacy 27/12,836 baseline is unchanged, and an authorized human approves the migration. No unsupported accuracy claim, fuzzy identity join, inferred settlement, paid-provider call, or probability/model change is permitted.


## Billing constraint and execution hold — user clarification (2026-10-25)

The project owner has clarified that the private repository's GitHub Actions runs are failing because the available Actions billing allowance is exhausted, and the allowance is expected to reset on **2026-11-01**. Treat this as the operational constraint for planning; do not spend more cycles trying to diagnose the already-known private-runner failure, and do not attempt private workflow reruns before the reset. This clarification is user-provided; the connected GitHub tools do not independently expose the billing dashboard.

Public standard GitHub-hosted runner jobs have passed on the research branch. GitHub's documentation confirms standard GitHub-hosted runner use is free for public repositories, while private-repository usage is quota/billing constrained. [GitHub Actions billing documentation](https://docs.github.com/en/billing/concepts/product-billing/github-actions).

### Critical distinction: Actions minutes vs provider credits

The 2026-11-01 Actions allowance reset does not itself refresh the FootyStats API quota/credits. The existing public live-ingestion workflow requires its explicit `confirm_provider_credit_usage=true` input and valid `FOOTYSTATS_API_KEY` and `ORACLE_PRIVATE_REPO_TOKEN` secrets. No live provider calls should be triggered until the owner explicitly confirms the provider-credit spend. The public dry-run remains zero-call and is not a substitute for a current fixture/data ingestion.

### First execution sequence after the reset

1. Confirm the private Actions allowance has actually reset; do not assume reset based solely on the calendar date.
2. Obtain explicit provider-credit confirmation and run the guarded Selected-50 exact-ID ingestion only if the required secrets are present.
3. Validate the resulting archive and current fixture schedule for all 50 selected season IDs; quarantine unmatched fixtures and missing/stale features.
4. Run the isolated 50-league candidate runtime only after it exists and proves probability parity with the frozen model on overlapping inputs. The currently inspected private production status still records 27 active leagues and development/challenger gates; no verified 50-league production runtime or calibrated 50-league output was found.
5. Produce predictions from the governed model only for fixtures that pass data gates. Label all other fixtures `BLOCKED/NO_BET`; do not manufacture probabilities.
6. Join predictions to verified outcomes after settlement and report accuracy only from the resulting genuine production-labelled sample.

### Current fixture availability

The inspected private repository's `data/fixtures/oracle_upcoming_fixtures.csv` is an older fixture file whose latest listed fixture is 2026-10-17; its companion manifest is generated 2026-10-08 and declares an active 27-league scope. It is not a valid current 50-league slate for 2026-10-25 onward. A current exact-ID fixture refresh is therefore mandatory before a forward prediction report can be generated.
