# Project Oracle — Run 8 Selected-50 Chronological Calibration Plan

**Research only.** This plan does not change Oracle V1.6, production probabilities, canonical ledgers or production workflows.

## Objective

Investigate whether Platt scaling or isotonic regression can reduce the calibration deterioration observed when adding home-role and away-role features to the overall-form model, while retaining any validated venue signal.

## Data and chronology

- Source: checksum-pinned Selected-50 archive; expected SHA-256 `bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261`.
- Reconstruct the event-time panel using the existing Run 8 builder and the three existing chronological test folds.
- For each fold, reserve the immediately preceding 90 calendar days as calibration data.
- Train only on rows before the calibration window; fit calibrators only on predictions and outcomes from that calibration window; evaluate only on the untouched test fold.
- The three calendar test partitions are reconstructed from Run 6 because the original Run 8 binary workbook and exact fold-cutoff manifest remain unavailable. This experiment is not an exact reproduction of the missing workbook.

## Models and methods

Fit the same fixed logistic pipeline on identical venue-eligible cohorts:
1. League-only baseline.
2. Overall-form-only.
3. Overall-form plus venue main effects.

For each model, compare raw probabilities, Platt scaling on logit scores, and isotonic regression. Calibrators are fitted separately within each fold and market. Minimum calibration sample is 500 observations with both outcome classes; otherwise the method is blocked, not imputed.

## Outcomes and inference

Report fold and pooled Brier, log loss, AUC, ECE10, held-out calibration intercept/slope, reliability bins, sample sizes, missingness and league coverage. Paired model comparisons use league-cluster confidence intervals and one-sided tests in the predeclared direction. One joint BH/BY correction family covers all markets, folds, pooled comparisons and metrics.

Primary calibration comparisons: each calibrated main-effects model versus its raw counterpart. Venue-retention comparisons: calibrated main effects versus calibrated overall-form-only and league-only baselines on identical fixtures.

## Governance and exclusions

- Five actual prior settled matches for each team; five explicit home-role matches for the home team and five explicit away-role matches for the away team.
- H2H evidence remains visible only with at least five prior meetings; it is not a model input in this calibration experiment.
- No pseudo-counts.
- xG without verified capture timestamps and provisional standings are excluded.
- Strict earlier-than-kickoff event-time construction; same-kickoff outcomes are appended only after all same-kickoff targets.
- Provider publication/capture timestamps and independent official settlement remain unverified.
- Frozen Oracle V1.6 comparison is blocked until a matching fixture-level frozen probability/settlement ledger is supplied. No challenger substitution is permitted.
- No raw provider rows, feature panels or fixture-level predictions may be exported.
- No provider API calls or credits are permitted.

## Acceptance discipline

A calibration method is a candidate only if proper-score improvements (Brier and log loss) are stable across folds and pooled, ECE/reliability improves without material deterioration, and the joint BY correction supports the prespecified comparison. AUC is reported but is not a calibration metric. No result is production-eligible or betting-eligible.
