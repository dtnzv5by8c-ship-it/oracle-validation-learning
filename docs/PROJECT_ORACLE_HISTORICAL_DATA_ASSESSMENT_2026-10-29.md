# Project Oracle — Historical Data Assessment and Model Feedback (2026-10-29)

## Executive conclusion

Oracle has useful research signals, especially in Double Chance diagnostics, but the available evidence does not establish a reliable betting edge across the selected 50-league universe. Treat all findings below as research-only, raw and uncalibrated. No production model logic, frozen probabilities, thresholds, calibration or production ledgers are changed by this assessment.

## Data scope and provenance

- Existing documented historical validation window: 20 March 2025 through 20 September 2026.
- Existing archive diagnostic: 59,049 deduplicated match records.
- This evidence does not yet establish complete coverage from 1 January 2024 through 29 October 2026. Do not claim that full range until earliest/latest timestamps and per-league season coverage have been audited.
- 51,983 records were reported with finished/complete status and numeric scores.
- 7,066 records with non-finished status also contained numeric scores. These must not be treated as settled labels merely because a score is present.
- 13,346 completed matches had 0–1 total goals; investigate this distribution by league, season and source before interpreting market behaviour.

## Historical market diagnostics currently available

| Market | Raw holdout accuracy | Majority baseline | Difference | Other reported metric | Interpretation |
|---|---:|---:|---:|---|---|
| BTTS | 53.588% | 54.143% | -0.555 percentage points | — | No demonstrated edge on accuracy; currently below the baseline |
| Double Chance Home | 70.126% | 69.786% | +0.340 percentage points | Brier 0.20081; AUC 0.63519 | Weak positive signal in discrimination/accuracy; uncalibrated and not proof of profitability |
| Double Chance Away | 60.422% | 56.275% | +4.147 percentage points | Brier 0.23298; AUC 0.63207 | Most promising raw signal of these reported accuracy metrics; needs leakage-safe validation, calibration and odds-based return testing |
| Combo | Masked | Not comparable | — | 9,335 Home and 8,017 Away predictor-versus-ledger disagreements previously reported | Do not use until target/settlement definitions and official truth are reconciled |

Accuracy alone is insufficient. Market evaluation must include Brier score, log loss, calibration/reliability curves, precision/recall where appropriate, sample size, confidence intervals, league/season stability, and odds-based ROI with a verified point-in-time price and settlement source.

## Key risks that can invalidate historical performance

1. **Point-in-time leakage is not cleared.** An earlier audit found 6,496 future-dated rows and 19,488 populated actual/post-match xG field values on future-dated rows. This does not prove the model consumed leakage, but the feature chronology is not proven safe. Exclude any feature without evidence that observed_at is earlier than kickoff.
2. **Settlement labels are not fully verified.** Numeric scores on non-finished rows are not sufficient. Use an authoritative final-status and score source with provenance.
3. **Identity mappings are incomplete.** Provider season IDs and comp_master_id values are not automatically Oracle canonical IDs. Do not silently merge leagues or teams based on names alone.
4. **Combo target conflict.** The research predictor/ledger have disagreed materially. Keep Combo masked until a single documented market definition and official settlement truth are applied to a separately labelled research diagnostic.
5. **Raw probabilities are uncalibrated.** A probability can rank outcomes reasonably but still be numerically unreliable. Do not interpret confidence as calibrated likelihood.
6. **BTTS is not currently supported by the reported accuracy comparison.** Its 53.588% accuracy is 0.555 percentage points below the 54.143% majority baseline.

## Recommended research plan

### P0 — Establish the real historical coverage window
Generate a per-league, per-season inventory showing earliest/latest kickoff, match counts, duplicate counts, source coverage, final-status completeness, feature completeness, and timestamp provenance. Explicitly test 2024, 2025 and 2026 separately. Report gaps; do not fill them with inferred data.

### P1 — Build a leakage-safe evaluation set
For every feature included in a historical row, require source identity, source timestamp, capture/observed timestamp, kickoff timestamp and proof that the observation preceded kickoff. Exclude unproven xG, standings and odds. Preserve a row-level exclusion reason.

### P2 — Re-run walk-forward diagnostics
Use chronological train/validation/test splits by kickoff date, not random splits. Keep fixtures from the same match and near-duplicate records together. Report sample size, coverage, accuracy versus baseline, Brier score, log loss, AUC where suitable, calibration bins, confidence intervals, and per-league/per-season stability.

### P3 — Test profitability only when odds provenance is valid
Join actual pre-kickoff bookmaker odds and official settlement outcomes by exact fixture/market identity. Include bookmaker margin, void/push rules and realistic bet timing. Report ROI with uncertainty and sample size; never infer profitability from accuracy alone.

### P4 — Market-specific decision
- BTTS: research only; no demonstrated edge under current accuracy comparison.
- Double Chance Home: continue validation; current raw lift is small.
- Double Chance Away: prioritize leakage-safe replication because its current raw diagnostic is the strongest of the three reported comparisons.
- Combo: remain masked until definition and settlement reconciliation pass.

### P5 — 50-league scorecard
For each league and market, show: historical rows, usable leakage-safe rows, current fixture coverage, feature completeness, canonical identity status, label provenance, calibration status, baseline comparison, uncertainty, and release status. A missing fixture or a few blocked matches should not stop other valid fixtures; however, unsupported data must remain blocked.

## Governance and release decision

- Research predictions may continue for fixtures with validated required features and source-safety checks.
- Keep the 25 missing-feature fixtures tracked in Issue #32 and do not impute their inputs.
- Maintain the 95% threshold for exact fixture-identity bridge coverage, while reporting prediction availability separately.
- Production and betting eligibility remain NOT_GRANTED until canonical joins, point-in-time integrity, official settlement truth, market-specific calibration and release review are complete.
- No production model logic, frozen probabilities, thresholds, calibration or production ledgers are modified by this assessment.
