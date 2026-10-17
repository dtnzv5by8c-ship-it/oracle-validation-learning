# Project Oracle — H2H Historical Validation Readiness

**As-of:** 2026-10-18  
**Scope:** reporting/research only. This document does not authorize production model, probability, threshold, calibration, or canonical-ledger changes.

## Decision

**A defensible matched chronological H2H incremental-value test is not yet executable from the currently verified artifacts.** This is a data-lineage and pairing limitation, not evidence that H2H has or has not predictive value.

## Verified inputs and what each can support

| Input | Verified shape / evidence | Usable for H2H incremental-value test? | Limitation |
|---|---|---|---|
| `archive/PREDICTION_LEDGER.csv` on governed source branch | 210 prospective challenger rows across 42 fixtures, with prediction IDs, fixture IDs, timestamps, markets, and probabilities | Only as a small prospective shadow cohort when paired to verified results | Only one current prediction batch; not a historical paired archive |
| `archive/SETTLEMENT_LEDGER.csv` on governed source branch | Header only; zero settled rows | No | No canonical prediction-to-settlement pairings |
| `research/BTTS_OOS_PREDICTIONS_001.csv` | 10,365 rows with synthetic-style `match_id` values, date, target, model probability and base probability | Not for H2H joining as-is | No league/team/fixture identity or H2H feature snapshot in this file |
| `research/august_2026_backtest/august_2026_predictions.csv` | 782 rows with fixture/team identity, outcomes and probabilities for multiple markets | Potential research cohort after provenance checks | August-only; no per-row immutable prediction timestamp or H2H feature snapshot in this CSV |
| `research/four_model/outputs/four_model_backtest_audit.json` | Aggregate historical replay metrics for 20 March 2025–20 September 2026 | Context only | Aggregate metrics are not fixture-level paired predictions and do not isolate H2H lift |
| Run #21 shadow settlement artifact | 210/210 rows settled with verified results; 42 fixtures | Prospective descriptive evaluation | One small cohort; the reporting job reads the source branch read-only and does not persist new predictions or settlements back to the governed source |

## Root cause

The canonical settlement ledger is empty. The prediction ledger has a single finite batch. Existing historical OOS assets either lack fixture/team identifiers, lack a timestamped H2H feature snapshot, or provide aggregate rather than fixture-level paired predictions. Therefore they cannot be safely joined into a valid with-H2H versus without-H2H comparison.

A reporting workflow that clones the private repository read-only cannot, by itself, make the prediction ledger grow between runs. Re-running the report only re-evaluates rows already present in the source snapshot; it does not create new independent prediction observations.

## Required data contract before the test can run

Each prediction row must preserve, at minimum:

- immutable `prediction_id`, canonical `fixture_id`, league/competition, fixture date, home/away team identities;
- prediction timestamp and kickoff timestamp/timezone, proving prediction precedes kickoff;
- market, raw probability and calibrated probability if applicable, decision/selection, model and version/code hash;
- data cutoff, feature snapshot identifier/hash, and H2H feature values computed strictly from matches completed before the prediction cutoff;
- paired verified result/settlement with final score, market truth, result source and source URL, settlement timestamp, and reconciliation status.

For an incremental H2H test, the same chronological fixtures and markets must have baseline probabilities and H2H-augmented challenger probabilities generated without future leakage. Compare paired Brier score, log loss, calibration, classification and selection hit rate, by market and league, with sample sizes and uncertainty intervals. Report selection returns only when trustworthy odds and a governed staking rule are present.

## Safe next steps

1. Preserve the current source ledger as read-only; do not backfill synthetic historic predictions or write shadow settlements into canonical ledgers.
2. Add or enable a governed append-only prediction capture in the existing prediction-producing workflow so each new run saves immutable pre-kickoff predictions with stable IDs and feature provenance. This must be a separate approved change in the source repository; the reporting repository cannot persist into the private source by design.
3. Keep shadow settlements in reporting artifacts until independently verified and reviewed.
4. Build the paired H2H/no-H2H evaluation only after both arms exist for the same out-of-sample fixtures and markets.
5. Until then, keep H2H predictive lift marked **NOT TESTABLE**, and do not promote the challenger or claim profitability.

## Latest completed reporting run

- [Run #21](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39071598767) — success.
- [Run #21 artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39071598767/artifacts/12116055163).
- Exact fixture-ID join: 92/92 (100%); no fuzzy matching.
- Shadow settlement: 210/210 (100%), zero chronology failures.
- H2H source audit: 16 unresolved mappings and 12 no-prior-meeting-found fixtures; review remains open.
- Production logic/probabilities unchanged; canonical ledgers untouched.
