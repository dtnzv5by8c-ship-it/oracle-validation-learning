# Project Oracle — Run 9 Calibration Execution Checkpoint

**Date:** 2 November 2026 (SAST)  
**Status:** Calibration experiment completed successfully; all outputs research-only.

## Repository safety and execution lineage

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Branch: `research/oracle-50-league-readiness-audit`
- Exact branch HEAD inspected before this checkpoint write: `9b739c9f7a9244705e3430c163f172076334071c`
- Prior implementation commit: `5fa6e26ab868288c9266aa05a8c770ceace3abb5`
- Test-boundary correction commit: `6d8a668e2a426695331bd17513fc3ca566998cba`
- Script import-path correction commit: `9b739c9f7a9244705e3430c163f172076334071c`
- Target checkpoint path was confirmed absent before this write.
- This checkpoint is documentation-only. No production files, Oracle V1.6 logic/probabilities, canonical ledgers or existing production workflows were changed.

## Run 8 binary recovery

A fresh Library search was performed for the exact Feature Edge v18 workbook, the Run 8 companion bundle and the event-time feature ledger. No matching binary was recovered. The repository contains the methodology, checksums and aggregate reports, not the original binary assets.

| Asset | Declared bytes | Expected SHA-256 | Status |
|---|---:|---|---|
| Feature Edge v18 workbook | 17,301,081 | `66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7` | Not recovered |
| Run 8 companion bundle | 29,242,558 | `b44e99c3ee9b1e1e4515739d810ec10b0bab1c8c718ef2918ec3f1bf78a08e2f` | Not recovered |

The checksum-pinned Selected-50 archive remains a reproducible rebuild source. This run downloaded it read-only and verified SHA-256:
`bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261`.

Archive audit: 59,049 rows, 200 season files, 50/50 exact Selected-50 mappings, zero parse errors, zero missing identities, zero duplicate identity keys. Provider API credits used: 0.

## Workflow failures and corrections

1. Workflow run `41375583760` initially failed in the contract test because the test incorrectly expected a strict gap between adjacent half-open train and calibration windows. The correct boundary is equality: train end-exclusive equals calibration start. Eight tests were discovered; seven passed and one failed.
2. After correcting that assertion, workflow run `41380480040` passed all eight tests and verified the pinned archive checksum, but the runner could not import the repository's `scripts` package when executing the calibration file directly.
3. Added an explicit repository-root insertion to `sys.path` in the research runner. This is an execution-path correction, not a model or feature change.
4. Workflow run `41380562500` completed successfully. All eight contract tests passed; the pinned archive download and checksum verification passed; event-time panel rebuild and calibration evaluation passed; aggregate-only artifact upload passed.

Successful workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41380562500  
Artifact ID: `13113101686`  
Artifact name: `oracle-run8-selected50-venue-calibration`  
Artifact SHA-256: `ae269a1972ef4328070bb872501027f7a8f4273e64a65337596d90c1950cc457`  
Artifact expiry: 9 November 2026.

## Population, chronology and gates

- Primary historical window: 20 March 2025–20 September 2026.
- Reconstructed training start: 20 March 2024.
- Folds remain the three contiguous Run 6 calendar partitions; exact original Run 8 fold-cutoff manifest remains unavailable.
- Event-time rule: strictly earlier than target kickoff; all fixtures sharing the same kickoff timestamp are evaluated before any result at that timestamp is appended to team histories. Additional history lag: 0 hours.
- Overall form: at least five observed, settled, score-complete prior matches for each team.
- Venue features: at least five explicit home-role observations for the home team and five explicit away-role observations for the away team.
- H2H eligibility is exposed only at five or more prior pair meetings; H2H is not a model input in this calibration experiment.
- No pseudo-counts or synthetic observations.
- xG without verified capture timestamps and provisional standings remain quarantined.
- Provider publication/capture timestamps remain unverified; strict event-time chronology is not proof of source publication time before kickoff.
- Archive settled status/score fields are used as labels, not an independently verified official settlement ledger.

| Fold | Train venue-eligible N | Calibration N | Test N | Test leagues |
|---|---:|---:|---:|---:|
| Fold 1 | 9,274 | 3,145 | 5,824 | 47 |
| Fold 2 | 15,752 | 2,491 | 6,004 | 44 |
| Fold 3 | 21,245 | 3,002 | 4,648 | 45 |
| Pooled OOS | — | 8,638 fold-calibration rows | 16,476 | 48/50 |

The 90-day calibration windows each exceeded the 500-observation minimum and contained both outcome classes. All 81 model/market/fold/method calibration status rows were AVAILABLE. The 16,476 pooled test cohort comprised 48 contributing selected groups; two groups had no eligible pooled test observations.

## Calibration results

Three models were evaluated on the same venue-eligible cohorts: league-only, overall-form-only and overall-form-plus-venue. Each was evaluated raw, Platt-scaled and isotonic-calibrated. Calibrators were fitted only on the immediately preceding 90-day calibration window; test outcomes were not used for fitting.

### Pooled main-effects scores

| Market | Method | N | Brier | Log loss | AUC | ECE10 |
|---|---|---:|---:|---:|---:|---:|
| DC_HOME | Raw | 16,476 | 0.202013 | 0.591105 | 0.631393 | 0.009375 |
| DC_HOME | Platt | 16,476 | 0.202085 | 0.591362 | 0.631008 | 0.009483 |
| DC_HOME | Isotonic | 16,476 | 0.202939 | 0.600549 | 0.628281 | 0.008322 |
| DC_AWAY | Raw | 16,476 | 0.233837 | 0.659728 | 0.625029 | 0.005509 |
| DC_AWAY | Platt | 16,476 | 0.234134 | 0.660367 | 0.623942 | 0.004200 |
| DC_AWAY | Isotonic | 16,476 | 0.235005 | 0.666948 | 0.620928 | 0.010169 |
| BTTS | Raw | 16,476 | 0.246864 | 0.686841 | 0.539188 | 0.009197 |
| BTTS | Platt | 16,476 | 0.247218 | 0.687558 | 0.532292 | 0.007823 |
| BTTS | Isotonic | 16,476 | 0.247784 | 0.695771 | 0.535565 | 0.014405 |

Lower Brier/log loss/ECE is better; higher AUC is better.

### Interpretation

- Raw main-effects probabilities had the best pooled Brier and log loss in all three markets.
- Platt scaling modestly reduced pooled ECE for DC_AWAY and BTTS, but worsened Brier/log loss and did not produce a multiplicity-corrected calibration improvement.
- Platt did not improve DC_HOME ECE.
- Isotonic worsened Brier and log loss in all three markets and reduced AUC. Its DC_HOME ECE reduction was small and not statistically supported after joint correction.
- Raw DC_HOME and DC_AWAY held-out calibration slopes/intercepts were relatively close to ideal: DC_HOME intercept 0.0158/slope 0.9597; DC_AWAY 0.0112/0.9885. BTTS slope was 0.7196, indicating a materially different reliability problem.
- The calibration-vs-raw comparison subfamily contained no BY-significant result. Across the full 624-test family, 72 results were BY-significant, primarily reflecting model-versus-baseline venue-feature comparisons rather than calibrator gains.

**Decision:** neither Platt nor isotonic calibration meets the pre-registered acceptance rule. Keep raw research probabilities for diagnostics; do not promote a calibrated variant.

## Does the venue signal survive calibration?

Comparing Platt-calibrated main effects against Platt-calibrated overall-form-only:

| Market | Brier improvement | Log-loss improvement | AUC improvement | BY q: Brier / log loss / AUC |
|---|---:|---:|---:|---|
| DC_HOME | 0.001649 | 0.004173 | 0.010993 | 0.001884 / 0.001137 / 0.154970 |
| DC_AWAY | 0.002345 | 0.004960 | 0.012299 | 0.000072 / 0.000071 / 0.016825 |
| BTTS | 0.000031 | 0.000075 | 0.000534 | 1.000000 / 1.000000 / 1.000000 |

These are pooled fixture-weighted improvements. The paired confidence intervals are league-cluster t intervals over 48 groups. Venue effects remain supported for DC_HOME and DC_AWAY proper scores after Platt scaling; DC_AWAY AUC also survives BY correction. ECE comparisons do not pass BY correction. This supports retaining venue features as a research candidate, not production promotion.

The calibration-vs-raw nested comparison had 48 tests per method (folds plus pooled, markets and metrics). Platt had one BH-significant result but zero BY-significant results; isotonic had zero BH/BY-significant improvements.

## Missingness and coverage

- All model features had 0% missingness within the gated venue-eligible cohort because five-observation eligibility was enforced before model fitting.
- Before eligibility, overall-form feature missingness ranged approximately 0.37%–0.42%; venue-history fields approximately 0.84%.
- H2H rate fields were missing in approximately 81.7% of raw target rows and 80.2% of gated rows because fewer than five verified prior pair meetings were available. H2H was not used as a model input.
- The Selected-50 universe is configured at 50 groups; 48 contributed pooled eligible test fixtures.

## Previous diagnostics not repeated

The two candidate interaction formulas were not rerun. Run 6 already tested them as nested additions to main effects on the reconstructed Selected-50 three-fold population, with constituent-controlled partial-Spearman tests and joint BH/BY corrections. Neither demonstrated independent incremental value. The calibration experiment therefore focused on the unresolved calibration deterioration.

## Frozen Oracle V1.6 baseline blocker

No matching fixture-level frozen Oracle V1.6 probability, prediction timestamp and settlement ledger is available for these historical folds. The challenger ledger and other development-only model outputs were not substituted. A paired production benchmark remains blocked.

## Next steps

1. Keep both calibrators rejected for now; do not promote calibrated probabilities.
2. Investigate why BTTS has a held-out slope around 0.72 while DC_HOME/DC_AWAY raw slopes are close to one. Prioritise a separate BTTS model specification study with strict chronological validation, not another post-hoc calibrator sweep.
3. Verify the original Run 8 fold cutoff manifest if the original companion bundle is later supplied; otherwise preserve the reconstructed-fold caveat.
4. Obtain a matching frozen V1.6 historical prediction/settlement ledger before attempting production-baseline comparisons.
5. Keep publication-time provenance, xG and standings quarantine gates in place.

## Governance

- Provider API credits used: 0.
- Raw provider rows exported: false.
- Fixture-level predictions exported: false.
- Event-time feature panel exported: false.
- Oracle V1.6 production logic/probabilities changed: false.
- Canonical ledgers changed: false.
- Production workflows changed or dispatched: false.
- Production eligible: false.
- Betting eligible: false.
