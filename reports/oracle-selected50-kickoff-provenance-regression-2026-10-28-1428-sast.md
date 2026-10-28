# Oracle Selected-50 Kickoff Provenance & Runtime Revalidation — 2026-10-28 14:28 SAST

## Decision

**Research-only improvement validated. Runtime QA PASS. Combo remains masked. Production and betting release remain NOT_GRANTED.**

A source-integrity defect was found in the FootyStats adapter: naive kickoff timestamps were silently assigned UTC, and completed-status records with future kickoffs could be classified as historical completed candidates. The adapter now requires explicit timezone evidence, normalizes valid offset timestamps to UTC while retaining the raw source value, and quarantines completed-status/future-kickoff contradictions. No model logic or probability outputs changed.

## Live branch and change

- Repository: dtnzv5by8c-ship-it/oracle-validation-learning
- Branch: research/oracle-50-league-readiness-audit
- Adapter + regression-test commit: [48ee494b8fc6802d2b086793420f90681179fc61](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/48ee494b8fc6802d2b086793420f90681179fc61)
- Files changed: scripts/oracle_selected50_footystats_adapter.py; tests/test_oracle_selected50_footystats_adapter.py.
- The change is research-adapter-only. The Selected-50 runtime builder, Combo predictor target, settlement helper, model training, thresholds, calibration, production registry, ledgers and governance were not modified.

## Workflow verification

All runs below used the exact adapter/test commit above and completed successfully.

| Workflow | Run | Job | Result |
|---|---:|---|---|
| Research Runtime and Backtest | [#154 / 40687715830](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40687715830) | 122814261363 | PASS |
| Dry-Run Planner | [#529 / 40687715761](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40687715761) | 122814261183 | PASS |
| Safety Contract Tests | [#231 / 40687715712](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40687715712) | 122814261052 | PASS |
| Identity & Settlement Evidence Tests | [#11 / 40687715668](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40687715668) | 122814260830 | PASS |

Job logs were inspected. Runtime #154 passed the existing private archive checksum gate and both Combo/feature-support test steps. The existing archive tag remained research-selected50-footystats-history-40447419806; archive SHA-256 was af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875.

Identity & Settlement run #11 passed:
- Evidence-register tests: **10/10**
- Identity-resolver tests: **7/7**
- Adapter tests: **15/15**, including the three new kickoff regressions
- **32/32 tests total** across these three suites

Dry-run #529 passed the three Combo settlement-governance tests. Safety #231 passed its offline contract suite. Dry-run/identity logs report zero provider API calls; dry-run reports zero network calls and zero paid-provider calls.

## Artifact verification

Downloaded artifacts were independently SHA-256 hashed and matched GitHub metadata.

| Artifact | ID | Size | SHA-256 |
|---|---:|---:|---|
| Runtime #154 | [12816016919](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40687715830/artifacts/12816016919) | 158,044 bytes | b7fb063b5d5f6b1e41b10930114468497fdd04cd2881bd56dd2e8ddb8e5bdb66 |
| Dry-run #529 | [12815002999](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40687715761/artifacts/12815002999) | 36,351 bytes | 7f106b1eb2a334663c8d9a223038947a7ceef9c243a3521a27efa8c948b1b00b |
| Identity/settlement #11 | [12816165727](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40687715668/artifacts/12816165727) | 7,379 bytes | 1f50fd184e8ede130b474b56552e037f361489945cb0ffeeff3b8418104b0f68 |

The runtime validator reports PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT. I extracted the runtime artifact and compared each CSV/JSON file byte-for-byte with runtime #153; all report files are identical, confirming this adapter-only change did not alter the model's outputs.

## Feature/training blocker investigation

The current runtime remains:
- 50 selected league groups; 200 historical seasons.
- 59,049 deduplicated historical records; 51,983 explicitly completed records.
- 463 upcoming fixture rows; 438 with at least one raw research-market output.
- **25** blocked by missing required features; **0** blocked by unavailable model training.
- 250 league-market readiness rows; 750 league-market walk-forward rows.
- Zero production-eligible fixtures.

The 25 blocked fixtures are unchanged from the previous runtime except the previously reconciled rolling-horizon fixture has left the schedule. The precise missingness in Runtime #154 is:
- 16 fixtures have fewer than five qualifying home matches; their seven home form features (home_gf5, home_ga5, home_btts5, home_fts5, home_cs5, home_shots5, home_sot5) are missing.
- 10 fixtures have fewer than five qualifying away matches; the analogous seven away features are missing.
- One fixture is in both groups, so 16 + 10 − 1 = 25.
- Six dependent pair/environment features (pair_btts_mean, pair_fts_mean, pair_cs_mean, score_environment, shot_environment, score_gap5) are missing on all 25 rows.
- Every blocked row reports PASS_ALL_MARKET_MODELS; each of the five markets has 44,568 eligible training rows.

These are genuine feature-history gaps under the existing five-match home/away rule, not training failures. Do not relax the rule, borrow unapproved prior-season/team identities, impute or fabricate features.

## Combo target and settlement

The research predictor remains Double Chance AND **2–4 total goals inclusive**. The unchanged settlement helper implements Double Chance AND total goals **<5**, including 0–1 goals. The diagnostic enumerates 121 scorelines and identifies:
- Home Combo disagreement: 0–0 and 1–0.
- Away Combo disagreement: 0–0 and 0–1.

The authoritative bookmaker market definition remains unverified. Combo probabilities remain blank in both exports. Do not unmask them until market semantics are approved and canonical fixture/team joins plus official settlement truth are verified.

## Identity, settlement and freshness gates

The latest evidence-register artifact contains ten exact ordered-team/UTC-kickoff candidate joins: six completed cross-provider score agreements, one Canadian score/status conflict quarantined, and three English postponed/suspended 0–0 placeholders excluded from settlement truth. It reports:
- Approved canonical bridges: **0**
- Verified official settlement truth: **0**
- Unmasked Combo rows: **0**
- Production-eligible rows: **0**
- Provider API calls and production writes: **0**

The current governed feed remains stale (manifest generated 8 October; last fixture date 17 October; schedule window ended 22 October). The separate FootyStats schedule snapshot does not refresh or authorize the FotMob feed. xG/odds point-in-time provenance remains unverified.

## Governance and next step

The latest runtime was an automatically triggered **public research-repository** workflow and read only the already-existing private archive using the governed tag; no private-repository Actions workflow was run. No provider API calls, private production repository writes, PR merges or production model changes were made.

**Next action:** keep all release gates closed and continue with authoritative source identity, exact canonical fixture/team joins, official settlement evidence and a governed current-feed refresh path. The adapter correction is validated; it does not resolve the 25 genuine feature-history gaps or the Combo market-definition mismatch.
