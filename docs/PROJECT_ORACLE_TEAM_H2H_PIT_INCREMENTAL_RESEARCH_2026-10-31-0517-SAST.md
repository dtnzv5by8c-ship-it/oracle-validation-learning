# Project Oracle — Team/H2H Pre-Match Incremental Signal Audit (Run 7)

**Date:** 31 October 2026, 05:17 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Disposition:** research-only; `production_eligible=false`; `betting_eligible=false`

## Objective and source

Test whether exact prior H2H history adds point-in-time (PIT) signal beyond recent team scoring tendencies, using only the verified v12 `H2H Meetings` ledger. Source workbook SHA-256: `1e22b8765114d9beb897ac4e34a01a26ea8be91cc83818d74e349186e8519e65`.

The source ledger has **23,328 unique fixtures**, complete UTC kickoffs, selected IDs, home/away provider team IDs, explicit scores and raw-record hashes. Available history spans 22 February 2024–20 September 2026. The governed primary validation window (20 March 2025–20 September 2026) contains **15,003 fixtures**.

## PIT method

- Exact fixture key and `selected_id + ordered provider team IDs` pair key retained; no fuzzy names.
- Every fixture at an identical UTC kickoff is evaluated before any fixture at that timestamp enters history. This prevents same-kickoff leakage.
- Team baseline: each side's last 10 completed matches before kickoff; each rate shrunk to a trailing 730-day exponentially weighted league prior with fixed `k=10`; home/away team estimates averaged.
- H2H: exact prior pair meetings only, 365-day exponential half-life; Kish effective sample size used for shrinkage to the league prior with fixed `k=10`.
- Fixed H2H blend sensitivity: 10%, 20%, 30%; not optimized and not Oracle V1.6 parameters.
- Markets: BTTS and Over 2.5. Metrics: Brier, log loss, AUC and 10-bin ECE; three fixed chronological folds.
- No venue H2H split: the ledger has no explicit `no_home_away` flag. No venue status was inferred.

## H2H coverage at primary-window kickoff

| Prior exact meetings | Fixtures |
|---|---:|
| 0 | 2,173 |
| 1–2 | 7,097 |
| 3–4 | 4,685 |
| 5+ | 1,048 |

Raw meeting count is not effective sample size. Provider team IDs are exact only within `selected_id`; cross-provider canonical identity and official settlement truth remain unverified.

## Main results

| Market | Comparator | N | Brier | Log loss | AUC | ECE |
|---|---|---:|---:|---:|---:|---:|
| BTTS | 730d league prior | 15,003 | 0.246222 | 0.685552 | 0.551670 | 0.013222 |
| BTTS | last-10 team form | 15,003 | 0.248002 | 0.689257 | 0.547366 | 0.029603 |
| BTTS | team + 30% H2H | 15,003 | 0.247217 | 0.687614 | 0.548799 | 0.019608 |
| Over 2.5 | 730d league prior | 15,003 | 0.245587 | 0.684236 | 0.569847 | 0.016288 |
| Over 2.5 | last-10 team form | 15,003 | 0.246498 | 0.686171 | 0.570253 | 0.025953 |
| Over 2.5 | team + 30% H2H | 15,003 | 0.245535 | 0.684136 | 0.574442 | 0.020175 |

The 30% H2H blend improves on the weaker team-form baseline in all three folds for both markets. However, it does **not** establish a robust incremental edge beyond the stronger league prior:

- **BTTS:** H2H blends have worse Brier and log loss than the league prior in all three folds.
- **Over 2.5:** the 30% blend is marginally better on Brier in the three folds, but the paired bootstrap against the league prior does not distinguish it from zero; log loss is marginally worse in the final fold.

## Paired bootstrap

A paired fixture-level bootstrap used 1,000 replicates (seed `20261031`). Negative loss deltas favour H2H.

| Market | Comparator | Brier delta vs comparator (95% CI) | Log-loss delta (95% CI) |
|---|---|---|---|
| BTTS | Team form | -0.000785 [-0.001145, -0.000433] | -0.001643 [-0.002400, -0.000916] |
| BTTS | League prior | +0.000995 [+0.000300, +0.001707] | +0.002062 [+0.000622, +0.003523] |
| Over 2.5 | Team form | -0.000963 [-0.001315, -0.000619] | -0.002035 [-0.002762, -0.001308] |
| Over 2.5 | League prior | -0.000052 [-0.000713, +0.000639] | -0.000101 [-0.001486, +0.001317] |

Conclusion: retain H2H as low-weight research context only. No production weighting change is justified.

## Integrity and archive access

- Independent brute-force reconciliation of 250 sampled primary-window fixtures passed **250/250** for prior league counts, exact-pair H2H counts and both teams' last-10 sample counts.
- Team/H2H profile coverage remains **31/50 groups** (732 team profiles; 7,188 exact pair profiles; 23,328 meetings). The other 19 groups have verified archive-ledger counts but their raw match JSON is absent from the accessible Run64 extract. They remain unavailable, not zero-filled.
- The private report-only ingestion workflow source (`cb89e5bd1c24810fe821a6b2c3c2c1c19272b381`) hard-codes **27 league codes**, not 50. It is not a complete recovery path for the remaining groups. No run/artifact ID was verified and the workflow was not dispatched.
- Score outcomes are provider-score-derived, not official settlement truth. No cross-provider canonical identity is claimed.

## Governance and outputs

- Provider/API credits used: **0**; ingestion, snapshot, runtime, backtest and bridge workflows rerun: **none**.
- Oracle V1.6 logic, probabilities and calibration changed: **no**.
- `production_eligible=false`; `betting_eligible=false`.
- Workbook: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v15_Team_H2H_PIT_Incremental_Validated.xlsx` (109 tabs; SHA-256 `948a224fa7a340ebb77a4afeef5b662d94a3764e2599f2362dab0efa78ef9fed`). All 101 v12 worksheet XML parts were preserved byte-for-byte.
- Full fixture PIT ledger, model metrics, fold comparisons, H2H coverage and bootstrap CSVs are included in the companion research bundle.

**Next priority:** obtain read-only access to the already-ingested raw match JSON for the 19 unprofiled groups. Do not dispatch ingestion or spend provider credits.