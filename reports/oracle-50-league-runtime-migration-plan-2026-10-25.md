# Oracle 50-League Runtime Migration Plan — 2026-10-25

## Decision and guardrails

This is a research-branch migration plan, not a production deployment. The target is a separately versioned Selected-50 runtime namespace. The existing 27-league production runtime and its historical 12,836-fixture baseline remain immutable. No production model logic, probabilities, calibration, thresholds, paid-provider access, or live prediction behaviour may change under this work.

Machine-readable contract: [oracle_50_league_runtime_migration_contract_v1.json](../config/oracle_50_league_runtime_migration_contract_v1.json).

## Workstream order

| Priority | Workstream | Required implementation/evidence | Exit condition | Current disposition |
|---|---|---|---|---|
| P0 | Private Actions runner diagnosis | Owner-visible Actions run/job initialization details and billing/usage view for failed production runs 40183610511 and 40190338066. Capture runner allocation, job initialization error, and any billing/spending-limit notice. | Explicit root cause supported by GitHub evidence; no speculative retries. | BLOCKED_EXTERNAL_OWNER_DIAGNOSTICS |
| P0 | Separate runtime contract | 50-season manifest, separate runtime namespace, immutable legacy namespace, exact IDs, feature/settlement gates, strict probability parity. | Contract regression passes; no legacy manifest/ledger edits. | CONTRACT_DEFINED_RESEARCH_ONLY |
| P0 | Consumer migration inventory | For each of the 13 audited consumers, classify whether it is legacy-only, shared-but-parameterized, or must gain a separate Selected-50 entry point. No global replacement of 27 or 12,836 constants. | Consumer-by-consumer mapping and test coverage; 27 historical baseline stays byte-for-byte stable. | INVENTORY_EXISTS_MIGRATION_NOT_IMPLEMENTED |
| P1 | Canonical fixture slate | Freeze one fixture table with canonical fixture ID, season ID, home/away stable team IDs, UTC kickoff, source/provider IDs and provenance. | Exact one-to-one join for each eligible fixture; unresolved IDs quarantined. | BLOCKED_CANONICAL_SLATE_NOT_PRESENT_IN_RESEARCH_BRANCH |
| P1 | Identity crosswalk | Versioned explicit source-to-canonical fixture/team crosswalk, evidence URL/file/hash, source IDs, resolution status and reviewer. No name-only or fuzzy match can qualify a row. | All admitted joins exact; unresolved/ambiguous rows excluded and counted. | BLOCKED_CROSS_SOURCE_EVIDENCE |
| P1 | Settlement truth | Outcome ledger with canonical fixture ID, source, explicit final status, home/away score, settlement timestamp, retrieval timestamp and evidence hash. Postponed/abandoned/suspended/contradictory outcomes remain unlabelled. | All backtest labels have verifiable final status and exact identity. | BLOCKED_VERIFIED_SETTLEMENT_EVIDENCE |
| P1 | Point-in-time features | Feature evidence ledger: canonical fixture ID, source, field, semantics, scale/units, market/bookmaker where applicable, source timestamp, captured timestamp, as-of-kickoff check and source payload hash. | Each feature proven available before kickoff and correctly mapped; missing/late/invalid values fail closed. | BLOCKED_POINT_IN_TIME_PROVENANCE |
| P2 | Genuine production validation | Immutable pre-kickoff production predictions with model/version, market, probability, timestamp, fixture key, plus verified outcomes. Exclude CHALLENGER rows from production metrics. | Exact-key joins; reproducible coverage, sample size, accuracy, Brier score, log loss and calibration; ROI only if contemporaneous odds and settlement rules are verified. | BLOCKED_NO_PRODUCTION_LABELLED_SAMPLE |
| CI | Public regression and dry run | Run public contract/data-gate tests and planner dry-run; inspect GitHub API run records, steps and artifacts at candidate SHA. | Actual successful runs for the same candidate SHA, not merely workflow files or previous runs. | PARTIALLY_VERIFIED_PRIOR_SHA_RUNS_EXIST |

## Migration sequence

1. **Freeze and fingerprint legacy baselines.** Capture the baseline manifest, historical fixture count and relevant production prediction output fixtures. Add tests asserting the existing 27/12,836 historical sample is not rewritten. Do not alter historical files to make them resemble the new universe.
2. **Add Selected-50 manifest and namespace.** Contract points to the governed selected-season manifest. Runtime output paths, caches, ledgers and artifacts must be namespaced so a 50-league run cannot overwrite the legacy 27-league run.
3. **Inventory all 13 runtime consumers.** Keep historical/research tools that intentionally operate on the old sample. Add separate parameters or entry points only where required. Do not change a hard-coded count globally; tests must distinguish historical sample size from active runtime selection.
4. **Resolve canonical identities.** Use exact stable IDs and UTC kickoff. Record all crosswalk evidence. Do not admit fuzzy/name-only matches.
5. **Admit settlement and features independently.** A numeric score is not proof of settlement. A non-empty xG/odds field is not proof of semantics, scale, bookmaker/market or pre-kickoff availability.
6. **Validate only genuine production predictions.** Join immutable pre-kickoff predictions to verified outcomes using canonical fixture ID + market + model/version + prediction timestamp. Do not relabel challenger output as production.
7. **Run isolated dry-run and parity checks.** No network/provider calls; no live predictions. Verify old outputs unchanged and exact probability parity where the same fixtures and model version overlap.
8. **Human release review.** Release only if every P0/P1/P2 gate and public CI gate has evidence. Otherwise remain NOT_GRANTED.

## Probability-parity rule

For overlapping fixtures and markets, compare the candidate runtime against the frozen production version using the same model version, same input snapshot, same market, and same feature cutoff. Require exact decimal equality (absolute tolerance 0) unless a separately approved numerical-representation specification says otherwise. Any difference is a hard failure and must not be “fixed” by calibration or threshold changes in this migration.

## Runner diagnosis — owner action required

The public research runner is healthy in the verified run cited below. That does not diagnose the private production runner. The private runs previously failed before any step with runner ID 0, no runner name, zero steps and unusable log retrieval. This is consistent with an initialization-stage failure but does not prove a billing cause.

Owner should open each failed run in GitHub Actions and capture:
- run summary and failed job details;
- runner allocation/initialization error and any runner group/label or policy message;
- repository Actions usage/billing and spending-limit status for the failure time;
- organization/repository Actions policies if the job was blocked before allocation.

Do not rerun private workflows, change spending limits, or start paid data ingestion as a diagnostic. Once evidence identifies the cause, repair only that cause and request approval before any private execution.

## Verified public CI evidence

- [Data Gate Contract run 40193763438](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40193763438) — completed success at commit `1248151312dd307af75bbe65e8c3b83823175f6b`.
- [Selected-50 Dry-Run Planner run 40193795700](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40193795700) — completed success at commit `0e943c54511b33b5f5b63dc6a2f6240158943be6`. Steps included plan generation without network calls, conservative market gates, planner and market regressions, exact catalogue resolver, prediction input contract, output validation, and artifact upload. Runner was a GitHub-hosted runner; artifact SHA-256 was `faac4c2e47609e0b474aaedac02e5bd7e45b046a03cbd6be7e264d81d07b891b`.
- These runs validate research contracts and dry-run plumbing only. They do not certify production runtime migration, 50-league data coverage, production accuracy, or release readiness.
