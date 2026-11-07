# Oracle Evidence & Backtest Control Checkpoint

**As-of:** 2026-11-07  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Baseline:** Selected-50 Market Intelligence Repair (successful run #360 / commit `f084491`)  
**Production/betting eligibility:** `false / false`

## Decision

The controlled acquisition queue is exhausted. This checkpoint uses existing evidence only. No provider/API acquisition was performed and no private workflow was dispatched.

The canonical production settlement ledger remains header-only, so production Oracle accuracy is **NOT TESTABLE** from canonical prediction/settlement evidence. Historical research metrics are retained only where lineage and chronology are explicitly documented.

## Evidence status

| Evidence | Status | Basis |
|---|---|---|
| Selected-50 repair | READY | Successful run #360; exact-ID/archive QA passed |
| Chronological historical-score research datasets | READY (research-only) | Date-batched construction with pre-cutoff features documented |
| Challenger shadow settlement | READY (research-only) | 210/210 rows settled, zero chronology failures |
| Canonical production prediction→settlement pairing | BLOCKED | settlement ledger header-only |
| Production Oracle accuracy | UNVERIFIED | no admissible canonical scored cohort |
| Production calibration | UNVERIFIED | no admissible canonical scored cohort |
| Confidence/risk-band performance | INSUFFICIENT SAMPLE / UNVERIFIED | no governed production cohort with immutable band + settlement provenance |
| League-level production metrics | INSUFFICIENT SAMPLE / UNVERIFIED | no canonical settled prediction cohort by league |
| H2H incremental production lift | BLOCKED | no paired immutable with/without-H2H production predictions |
| Provider-blocked population | QUARANTINED | existing blocked registry; no evidence-backed recovery without provider calls |

## Existing research metrics (not production Oracle performance)

The verified 42-fixture challenger shadow cohort contains 210 settled market rows. Descriptive metrics are:

| Market | n | Accuracy | Brier | Log loss |
|---|---:|---:|---:|---:|
| HOME_1X | 42 | 69.05% | 0.181928 | 0.543237 |
| HOME_1X_U45 | 42 | 61.90% | 0.216410 | 0.623280 |
| AWAY_X2 | 42 | 61.90% | 0.234872 | 0.662989 |
| AWAY_X2_U45 | 42 | 64.29% | 0.231525 | 0.655660 |
| BTTS_YES | 42 | 54.76% | 0.260507 | 0.715422 |

No league/risk-band ranking is promoted from this cohort: all configured league-market and team-role-market groups remain below the minimum sample threshold.

A separate August BTTS chronological research proxy has 327 held-out fixtures: raw Oracle probability accuracy 55.046%, Brier 0.244695, log loss 0.682436 and AUC 0.565797. This file lacks immutable per-row prediction timestamps/feature snapshot hashes and is therefore **research-only**.

## Gate rule

Only a dataset containing exact fixture/market identity, strictly pre-kickoff prediction timestamp, verified settlement truth, valid probability, and source-manifest provenance can be admitted to metric calculation. No inferred, future, unsettled or unverified outcome is admitted. This gate cannot grant production or betting eligibility.

## Next lane

Hand control to downstream OMI/release-readiness work. Priority is to establish an immutable fixture-level prediction→settlement evidence chain from existing records. Until that exists, do not claim production accuracy, calibration, Brier/log-loss/AUC, confidence/risk-band performance, profitability, or H2H incremental lift.

Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and governance are unchanged.
