# Project Oracle Run 10 — BTTS Goal-Environment Diagnostics

**Status:** Pre-registered research-only experiment. No production promotion.

## Why this experiment

Run 9 found weak BTTS discrimination (pooled AUC 0.539188) and a held-out calibration slope around 0.72. Platt and isotonic scaling did not improve pooled Brier/log loss. This experiment tests model specification, not another calibrator sweep.

## Run 8 asset recovery

The original Feature Edge v18 workbook and Run 8 companion bundle remain unavailable in the Library and repository. The exact checksum-pinned Selected-50 archive is the reproducible rebuild source:

bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261

The workflow downloads this release read-only, verifies its checksum and makes no provider API calls. The original workbook and companion bundle are not represented as recovered.

## Design

Use the same three expanding chronological folds and the Run 8 event-time panel. Each target is evaluated before any result sharing its kickoff timestamp is appended to history.

All principal model comparisons use identical venue-eligible fixtures:
- At least five observed, settled, score-complete prior matches for each team.
- At least five explicit home-role matches for the home team and five explicit away-role matches for the away team.
- H2H is evaluated only on a separate cohort with at least five actual prior pair meetings.
- League goal-environment rates require at least 50 actual prior settled league matches.
- No pseudo-counts or synthetic observations.

### Model ladder

1. League-only.
2. Overall form only.
3. Main effects (overall plus venue form).
4. Main effects plus team goal environment (scoring, conceding, BTTS and O2.5 rates over five observed matches).
5. Main effects plus venue goal environment (same rates over five explicit home/away-role matches).
6. Main effects plus league goal environment (last 50 actual league matches).
7. Main effects plus all goal-environment blocks.
8. Separate H2H cohort: league-only, main effects, and main effects plus H2H rates.

The two Run 6 candidate interactions are not rerun: their nested ablations and constituent-controlled tests already failed to demonstrate independent incremental value.

## Evaluation

BTTS only. Fixed LogisticRegression(C=0.1, LBFGS, max_iter=2500), training-fold median imputation/standardisation and selected-league one-hot effects. No hyperparameter tuning and no post-hoc calibration.

Report fold-level and pooled Brier, log loss, AUC, ECE10, reliability bins, paired league-cluster confidence intervals, feature missingness and selected-league coverage. Use constituent-controlled partial Spearman tests for candidate goal-rate features, controlling for existing main effects and selected-league fixed effects. Apply one joint BH/BY correction across all fold/pooled paired comparisons and partial-correlation tests.

## Baselines and limitations

- League-only, overall-form and main-effects baselines are available.
- Frozen Oracle V1.6 remains blocked until matching fixture-level V1.6 BTTS probabilities, prediction timestamps and settlement truth are available. No challenger output may be substituted.
- Archive score/status is a research label, not independently verified official settlement.
- Provider publication/capture timestamps are not verified; event-time ordering is not proof of publication-time provenance.
- xG without verified capture timestamps and provisional standings remain quarantined.

## Governance

No raw provider rows, fixture-level predictions or feature panels are uploaded. Only aggregate metrics, reliability bins, missingness, coverage and governance metadata are exported. Oracle V1.6 production logic/probabilities, canonical ledgers and existing production workflows remain untouched. Provider API credits used: zero.
