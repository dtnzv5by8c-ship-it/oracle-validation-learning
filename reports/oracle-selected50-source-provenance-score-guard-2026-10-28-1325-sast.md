# Selected-50 Source Provenance & Score Integrity Guard — 2026-10-28 13:25 SAST

## Decision

Research-only adapter hardening is committed. **Targeted isolated guard tests: 8/8 PASS. Full GitHub Actions validation of the updated adapter test suite is PENDING** because this session cannot dispatch workflows and no run was returned for the updated head. Do not represent the full repository suite as passed.

No provider API calls, private archive reads, production writes, model changes, or release-gate changes were made.

## Live state

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Branch: `research/oracle-50-league-readiness-audit`
- Branch head after research-only changes: `a6e657757a0415c8eb5b244cea9732a92b1dce10`
- Baseline runtime source: `6ac1b0ae89115e77d2a448d7fcbc4091416a862e`
- Latest existing runtime: [Run #150](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40677788876), source `6ac1b0ae89115e77d2a448d7fcbc4091416a862e`.
- Latest existing dry-run: [Run #520](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40677813787), source `2adcc1deaecf012c6e61977fe0a91f6273275bf9`.
- Latest existing safety suite: [Run #222](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40677813708).
- Latest existing resolver/adapter suite: [Run #4](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40677813719); it predates the changes in this report.

The branch diff against runtime #150 contains the adapter, adapter tests, offline test workflow and reports. The production runtime builder, runtime output validator, settlement helper, Combo predictor-target tests and feature-support tests are unchanged. A new full runtime build is not justified by these adapter-only changes.

## Concrete defects corrected

### 1. Missing/unsafe source snapshot provenance

Previously, the adapter allowed a snapshot without `retrieved_utc` to continue and labelled the timestamp `UNKNOWN`. It did not expose a source-snapshot hash on each adapted row.

The adapter now:
- rejects a missing, malformed, timezone-naive or future `retrieved_utc`;
- normalizes the retrieval timestamp to UTC;
- computes a deterministic SHA-256 over canonical JSON (sorted keys, compact separators, UTF-8, finite JSON values only);
- exports the source timestamp and snapshot digest in every row and the manifest; and
- records snapshot age at adaptation time.

The digest is explicitly a canonical-JSON hash, not a byte hash of the original downloaded ZIP/file. It provides repeatable lineage for the parsed snapshot object and does not certify provider truth.

### 2. Invalid source scores were silently coerced

Previously, `int(float(value))` truncated fractional values such as `1.5` to `1` and accepted booleans as numeric scores. That could turn malformed source data into a plausible-looking historical result.

The parser now accepts only finite, non-negative integer scores. Boolean, fractional, negative, NaN and infinite values return blank; for completed rows the existing classifier then quarantines the record as `QUARANTINE_INCOMPLETE_SCORE`. No score is inferred or imputed.

### 3. CI coverage gap closed in workflow configuration

The identity/adapter workflow's push path filter did not include adapter-only changes, despite the pull-request filter including them. The push filter now includes both the adapter and its test file. A manual `workflow_dispatch` trigger was added to the same offline test workflow.

Workflow URL: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle_identity_resolver_tests.yml

Manual run requirements:
- Branch: `research/oracle-50-league-readiness-audit`
- Inputs: none
- Provider API calls: none
- Private archive access: none
- Secrets: none required

The connected GitHub tools in this session do not expose workflow dispatch. No run was started or claimed.

## Test evidence

Eight isolated local tests passed against the updated timestamp/score guard logic:
1. Fractional score rejected.
2. Negative score rejected.
3. Boolean score rejected.
4. Valid integer-valued score preserved.
5. Missing retrieval timestamp rejected.
6. Timezone-naive retrieval timestamp rejected.
7. Future retrieval timestamp rejected.
8. Offset timestamp normalized to UTC.

This is targeted helper-level validation. It is **not** a substitute for running the full repository test file. The adapter suite now includes four provenance tests and three invalid-score regression tests in addition to the five earlier tests. Run the manual offline workflow above to validate the actual committed module and all 12 adapter tests plus the seven identity resolver tests.

## Existing runtime/output evidence rechecked

Downloaded artifacts were independently hashed and extracted:
- Runtime artifact [#12810274858](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40677788876/artifacts/12810274858), SHA-256 `fd03e898ae116910cccc4195e0386be88b06e28002b1266a67cb305a4d7f8701`.
- Dry-run artifact [#12811452579](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40677813787/artifacts/12811452579), SHA-256 `cb67d4524092bfa67db47d5cfac283abf1535705b02e41975549efd4eb4732b5`.
- Existing FootyStats schedule snapshot artifact [#12796207151](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12796207151), SHA-256 `813818e24514e15f542b9cc63deddb92d5507521d364c9b755d318e7bbcb14e4`.

The snapshot has 2,250 fixture rows across 50 selected seasons and retrieval timestamp `2026-10-28T06:19:09.645973+00:00`. Observed statuses: 1,372 `complete`, 859 `incomplete`, 19 `suspended`. These are existing archived observations; no API request was made.

Runtime #150 output still reports 463 fixtures, 438 with at least one raw research-market output, 25 blocked by missing required features, zero blocked by model training, and zero production-eligible rows. Both Combo probability columns remain empty. The runtime output contract is `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.

## Unchanged blockers

- The 25 feature-blocked fixtures lack five qualifying prior matches in the relevant home/away orientation; training support exists for all five markets. Do not impute or fabricate inputs.
- Combo research target remains Double Chance plus 2–4 total goals inclusive; the existing settlement helper includes 0–1 goals under Under 4.5. Official bookmaker semantics remain unverified; keep Combo masked.
- Canonical league bridges: 0 approved; canonical fixture/team joins: 0 verified; official settlement truth: 0 verified.
- FotMob/current-feed snapshot remains stale; the FootyStats schedule snapshot does not refresh or authorize the FotyMob feed.
- Point-in-time standings/xG/odds provenance and calibration/odds-benchmarked edge remain unverified.

## Governance

No provider API calls, no private archive reads, no private Actions, no production repository writes, no PR merge, and no changes to Oracle V1.6/V1.6.3 production logic, probabilities, calibration, thresholds, registry, ledgers or governance.
