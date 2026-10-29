# Project Oracle — H2H Ablation Run 167 Review
**Date:** 2026-10-29  
**Workflow:** [Oracle Selected-50 Research Runtime #167](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40908822137)  
**Artifact:** [Runtime report artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40908822137/artifacts/12913366497)  
**Scope:** Research branch only. Production model logic and frozen probabilities remain unchanged.

## Execution result
- Workflow completed successfully in 5m 39s.
- Runtime output contract passed; H2H chronology/model feature contract test step passed.
- Snapshot-to-runtime archive consumption and SHA-256 verification passed.
- Production eligibility: NO. Betting eligibility: NO.
- Runtime reports 437 governed fixture rows, 25 blocked for missing required baseline features, 412 with at least one supported raw research prediction.
- H2H paired holdout contains 19,991 fixtures, or 95.75% of 20,878 baseline test fixtures; the CSV has five market rows per fixture (99,955 rows).

## Primary paired holdout
Period: 2025-03-20 through 2026-09-20. Both variants use the same H2H-eligible training rows and the same paired fixtures. The candidate adds four numeric H2H features to the existing 20 baseline features.

| Market | Baseline accuracy | H2H accuracy | Brier: baseline → H2H | Log loss: baseline → H2H | Initial interpretation |
|---|---:|---:|---:|---:|---|
| BTTS | 53.65% | 53.77% | 0.24761 → 0.24750 | 0.68833 → 0.68811 | Small numerical gain |
| Double Chance Home | 69.99% | 70.08% | 0.20150 → 0.20148 | 0.59026 → 0.59033 | Accuracy/Brier marginally better; log loss and ECE worse |
| Double Chance Away | 60.38% | 60.35% | 0.23289 → 0.23283 | 0.65769 → 0.65756 | Accuracy slightly worse; probability metrics marginally better |
| Combo Home | 57.40% | 57.37% | 0.24237 → 0.24241 | 0.67769 → 0.67775 | Not releasable; settlement definition unresolved |
| Combo Away | 64.94% | 64.95% | 0.22391 → 0.22402 | 0.63930 → 0.63960 | Not releasable; settlement definition unresolved |

H2H features are present for 19,991 paired fixtures. Median prior H2H count is 4; median time since the last meeting is 155 days; maximum observed gap is 1,302 days. These are coverage diagnostics, not proof that team identities or source history are canonical.

## Expanding-window stability
Each fold trains strictly before its start and uses the same H2H-eligible rows for baseline and candidate. Positive accuracy delta favors H2H; negative Brier/log-loss deltas favor H2H.

| Market | Accuracy improved / 5 folds | Brier improved / 5 | Log loss improved / 5 |
|---|---:|---:|---:|
| BTTS | 2 | 2 | 2 |
| Double Chance Home | 5 | 3 | 3 |
| Double Chance Away | 2 | 1 | 1 |
| Combo Home | 3 | 1 | 1 |
| Combo Away | 1 (2 ties) | 1 | 1 |

Double Chance Home is the most promising research signal so far, but probability-quality metrics are not uniformly better. Gains are small and do not establish a betting edge. Combo remains excluded pending settlement-definition reconciliation.

## H2H implementation review — current limitations
1. H2H grouping uses the research-selected competition group plus sorted provider home/away team IDs. The selected group is mapped from country/competition labels across archive seasons, so history can span seasons. However, stability of team IDs across seasons has not yet been empirically certified.
2. The implementation sorts prior completed H2H matches by kickoff and uses a strict bisect-left cutoff, excluding matches at the target kickoff timestamp and later.
3. H2H features use the last five available prior meetings for BTTS rate and mean total goals; if fewer than five exist, the available one to five are used. No-H2H cases are excluded from candidate and paired comparison, not imputed.
4. Runtime QA reports no non-integer numeric score rows in the normalized archive and no duplicate rows removed by current dedup, but this does not certify provider completeness or canonical identity.
5. H2H result-sequence data is calculated for diagnostics but is not one of the four numeric candidate model features.
6. The comparison is a reproducible research baseline versus an H2H candidate, not an exact historical production prediction replay. It is not a production-versus-research approval.
7. Official settlement truth, provider-to-canonical fixture/team/competition joins, and feature provenance remain unverified. All metrics are raw and uncalibrated.

## Next work
1. Add explicit H2H QA for cross-season team-ID/name consistency, competition grouping, valid finished status and integer scores, duplicate fixture handling, strict timestamp cutoffs, and source match counts.
2. Add focused unit tests for H2H temporal cutoff and home-perspective outcome logic; current tests validate candidate feature handling but do not fully cover history-building rules.
3. Re-run the research workflow after the QA/test update and review the resulting audit artifact.
4. Keep Combo blocked until the authoritative market settlement specification is resolved.
5. Only after data integrity passes, consider a separate validation/calibration design for Double Chance Home and BTTS. Do not tune on the locked holdout.
6. Production and betting release remain NOT GRANTED pending identity, point-in-time integrity, settlement, calibration, odds/value, market readiness and formal release review.

## Decision
**Continue research; do not promote the H2H candidate.** Double Chance Home is the first market to investigate further, but current uplift is marginal and calibration metrics are mixed. No staking recommendation is supported by this run.