# Selected-50 Runtime & Regression Checkpoint — Run #119

**Date:** 2026-10-27 (UTC)  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Code revision tested:** `9438a9f743cb84b9b130586ea2f7dbbdbaa1be58`  
**Runtime run:** [40577750724](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724)  
**Artifact:** [12768701010](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724/artifacts/12768701010)  
**Artifact SHA-256:** `3f8a9ad3d8d922ffef85a604081574f4919bd090ef9610ac1a78ca86d06733ca`  
**Research-only fix PR:** [#29](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/29), merged into the research branch as commit `9438a9f743cb84b9b130586ea2f7dbbdbaa1be58`.

## Verified workflow and test results

- Runtime Run #119: **SUCCESS**; job `selected50-runtime` passed all steps.
- Private archive tag: `research-selected50-footystats-history-40447419806`; checksum verification returned `OK`.
- Combo target contract: **5/5 tests passed**, including home target, away target, five-goal rejection, export masking, and the new disagreement-diagnostic regression.
- Feature/training support diagnostics: **4/4 tests passed**.
- Output validator: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Safety Contract Tests Run #157: **SUCCESS**.
- Dry-Run Planner Run #463: **SUCCESS**.
- No FootyStats API calls were made.

## Artifact inspection

The ZIP contains 14 files. Local SHA-256 of the downloaded artifact exactly matches the GitHub-reported digest.

| Output | Verified result |
|---|---:|
| Selected league groups | 50 |
| Historical seasons loaded | 200 |
| Deduplicated historical match records | 59,049 |
| Explicitly completed historical records | 51,983 |
| Fixture rows in the rolling seven-day report | 459 |
| Unique source fixture IDs | 459 |
| Prediction rows | 2,295 (459 × 5 markets) |
| League-market readiness rows | 250 |
| League-market walk-forward rows | 750 |
| Fixtures blocked by missing required features | 25 |
| Fixtures with research predictions for at least one market | 434 |
| Fixtures blocked by unavailable model training | 0 |
| Combo probability cells remaining in prediction export | 0 |
| Combo probability cells remaining in governed export | 0 |

All rows remain research-only and production-ineligible. Raw non-Combo market estimates are not approved for betting.

## Defect found and fixed

Before PR #29, each league's Combo predictor-versus-settlement counters were initialized to zero but never incremented. That made the internal QA output falsely claim no disagreements even though the existing target-contract tests demonstrated disagreement on low-total scorelines.

The fix adds an explicit scoreline comparison between:
- the research predictor target: Double Chance AND 2–4 total goals; and
- the existing settlement helper: Double Chance AND total goals ≤ 4.

It counts only deduplicated records with an explicitly finished status and valid non-negative integer scores. Nonfinal records with numeric score placeholders are excluded. The predictor target and settlement helper were not changed.

### Computed internal disagreement counts

| Diagnostic | Count |
|---|---:|
| Home Combo predictor-vs-settlement disagreement rows | 9,335 |
| Away Combo predictor-vs-settlement disagreement rows | 8,017 |
| Selected groups with a nonzero home disagreement count | 50/50 |
| Selected groups with a nonzero away disagreement count | 50/50 |
| Completed low-total (0–1 goals) rows, internal status/score QA | 13,346 |

These are **internal status/score diagnostics**, not independently verified official settlement truth. The aggregate feature-QA counters reconcile exactly with the sum of the 50 per-league settlement-QA rows. The output validator now fails if the counters do not reconcile or if the known disagreement is incorrectly reported as zero.

## Combo and feature-support status

Combo probabilities remain blank in both exported reports, with `BLOCKED_SETTLEMENT_SPEC_MISMATCH`. The mismatch between the research target and settlement helper is documented, not resolved. Canonical fixture/team joins and official settlement truth remain unverified.

The 25 blocked fixtures remain blocked because required feature history is insufficient. No missing values were imputed, and no training gate was reported unavailable. The rolling-horizon count changed from 25 in the prior run only as fixture candidates entered/exited the horizon; it is not evidence of a model improvement.

## Release gates

- Provider parent competition IDs verified: **0/50**.
- Provider-to-canonical bridges verified: **0**.
- Canonical fixture/team joins: unverified.
- Official settlement truth against the production market specification: unverified.
- Walk-forward results: raw and uncalibrated; no approved odds/ROI benchmark.
- Production model logic/probabilities changed: **false / false**.
- Production eligibility: `NOT_GRANTED`.
- Betting eligibility: `NOT_GRANTED`.

## Ancillary workflow note — updated after Run #119

H2H Exact-ID Join Tests Run #34 failed before test execution because the workflow omitted `scikit-learn`, while `unittest discover -s tests` imports Selected-50 runtime tests. The error was verified in job logs: `ModuleNotFoundError: No module named 'sklearn'`.

**Fix completed and validated:** PR [#30](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/30) added the same `numpy scikit-learn` installation used by the Selected-50 runtime workflow. The PR was merged into the research branch only as commit `99017b1ff38b1d32079fe633bc6cc1bc8a402968`. H2H Exact-ID Join Tests [Run #35](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40593513957) passed: compile step succeeded and **196 tests passed**, including the three Combo settlement-gate tests, five Combo target-contract tests, and four feature/training support tests. No production repository or Oracle model logic was changed.

## Artifact reinspection

Run #119 artifact [12768701010](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40577750724/artifacts/12768701010) was downloaded and inspected. The local SHA-256 matched GitHub's digest: `3f8a9ad3d8d922ffef85a604081574f4919bd090ef9610ac1a78ca86d06733ca`.

- Prediction report: 459 rows, 459 unique fixture IDs; 434 rows have research-market outputs and 25 are blocked for missing required features.
- Governed fixture report: 459 rows; all rows remain production-ineligible; both Combo probability columns are blank for all rows.
- Runtime validation: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`; unavailable market models: 0; production and betting eligibility: false.
- Settlement QA: all 50 selected groups label the results `INTERNAL_STATUS_SCORE_QA_ONLY_OFFICIAL_SETTLEMENT_UNVERIFIED`; non-final status/score combinations remain separated from completed-score rows. The settlement helper rejects unsupported non-final statuses rather than treating placeholder 0-0 scores as settled outcomes.
- Combo predictor target remains Double Chance AND 2–4 total goals, while the settlement helper uses Double Chance AND fewer than five total goals. The disagreement remains explicit and Combo remains masked.

The latest full runtime is still Run #119 because the subsequent research-branch changes were documentation and a test-workflow dependency correction only. A new full runtime dispatch was not necessary.

## Next safe actions

1. Continue identity, canonical-join, settlement-truth, and point-in-time provenance work from existing evidence.
2. Keep ambiguous identity candidates quarantined; do not infer parent competition IDs from season IDs.
3. Keep Combo masked until the authoritative market definition, canonical joins, and official settlement truth are verified.
4. Do not make any provider request without fresh explicit approval and a verified credit budget.
5. Keep production Oracle V1.6/V1.6.3, probabilities, thresholds, calibration, protected registry, ledgers, and governance unchanged.
