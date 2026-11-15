# Oracle Signal Validation — Cycle 12 — 2026-11-15

## Scope
Chronological, leakage-safe validation of Master OMI research fields using the public research repository `dtnzv5by8c-ship-it/oracle-validation-learning`. Oracle V1.6 production logic, probabilities, thresholds, calibration and betting eligibility are unchanged.

## Durable state
- HEAD: `6f0247f4b5d8d27447ba82ef34256881be79553e`
- Parent: `a138f51192d8c8a8534ec499b5fea1952455f5a3`
- Current source-validation run: Run 35 / 43705410134, SUCCESS.
- Prospective run: 43709067778, completed with governance/test failure; no production promotion.

## Data-integrity controls confirmed
- 50 governed leagues; 24 ready, 26 data-gated; 0 source-error leagues.
- 113 fixtures in the completed live-source validation artifact.
- Duplicate historical match IDs now hard-fail; no silent deduplication.
- PPG/GF-M/GA-M require strictly pre-kickoff historical matches, exact league/team identity and minimum five qualifying observations.
- Normalized-name matches are diagnostic only and cannot substitute for exact identity.
- No same-day/future state; missing pre-match state remains NO_BET.
- Provider percentages are not treated as Oracle probabilities.
- xG remains quarantined until point-in-time provenance is independently demonstrated.

## Prospective execution finding
Run 43709067778 successfully completed fixture refresh, protected-artifact preservation, Team State refresh, four-model prediction generation, NO_BET diagnosis, immutable publication preparation, and truth/settlement steps. The final governance/test step failed.

The failure was a research test assertion in `test_footystats_goal_market_extension.TestFootyStatsGoalMarketExtension.test_explicit_not_retrieved_and_research_only`. The assertion expected the literal serialized marker `"research_only":"TRUE"` in the extension source. The source shown in the runner instead sets `row["research_only"]="TRUE"` at runtime. This is a CI/test-contract mismatch, not evidence of data leakage or a production-model failure.

The same governance step also reported the existing test-suite leakage fixture failure `LEAKAGE_FAIL` and a data-gated empty historical match-spine message. These are test/governance controls; they are not evidence supporting promotion.

## Research signal status
No new statistical promotion is authorised from this run. Brier, log loss, AUC, ECE/reliability, probability-band and incremental-value results from prior completed experiments remain research-only and were not repeated.

| Field/signal | Status |
|---|---|
| PPG | RESEARCH / denominator-gated |
| GF/M | RESEARCH / denominator-gated |
| GA/M | RESEARCH / denominator-gated |
| BTTS | RESEARCH |
| O/U | RESEARCH |
| Average goals | RESEARCH |
| Clean sheet | RESEARCH |
| Failed to score | RESEARCH |
| xG | QUARANTINED — PIT provenance not proven |
| FootyStats goal signal | RESEARCH_ONLY |
| Prediction risk | RESEARCH / PIT provenance required |
| Goal timing | RESEARCH / PIT provenance required |
| Interactions/convergence | RESEARCH_ONLY until OOS incremental value is demonstrated |

## Decision
**NO PROMOTION.** The statistical validation program remains fail-closed until the research CI contract is repaired and the authoritative historical match spine is available for independent aggregate reconstruction. No Master OMI A:ET field or Oracle V1.6 production value is changed.

## Next controlled action
Repair the research-only CI assertion/test contract, rerun the failed governance test once, then execute the hardened PPG/GF-M/GA-M denominator audit against the authoritative historical archive and exact fixture artifact. Only after that gate passes should the chronological challenger metrics be evaluated for ET+ research admission.