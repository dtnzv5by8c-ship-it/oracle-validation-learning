# Selected-50 Research Runtime Verification — 2026-10-26

## Status

**PASS — research runtime output contract only. Research-only; not approved for betting or production.**

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Branch: `research/oracle-50-league-readiness-audit`
- Runtime workflow: [Run 40238357851](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40238357851)
- Runtime code commit: `73fa4cbd459e6220b88d2fa4dbbc815b37b548de`
- Artifact ID: `12615034595`
- Artifact SHA-256: `a7d17ff2e058bcf2a8a70f7f280c8ed821f11aa8ca7d8262b45e9f74a25b877d`
- Artifact expires: 2026-11-08 22:05:41 UTC
- Output validation: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`
- `production_eligible=false`; `betting_eligible=false`.

The ZIP digest was independently recomputed from the downloaded artifact and matched the GitHub artifact digest. The run's runtime build, output-contract validator and sanitized artifact upload all completed successfully. The workflow is a research candidate run and does not promote production.

## Validated output shape

| Output | Verified count |
|---|---:|
| Selected grouping keys | 50 |
| Walk-forward aggregate market/fold rows | 15 (5 markets × 3 folds) |
| League-market readiness rows | 250 |
| League-market-fold metric rows | 750 |
| Schedule coverage rows | 50 |
| Settlement QA rows | 50 |
| UTC calendar-year coverage rows | 250 (2023–2027) |
| Provider season-start-year rows | 200 (2023–2026) |
| Governed upcoming fixture rows | 448 |
| Unique source fixture IDs in governed report | 448 |
| Fixtures retained as raw research-only output | 421 |
| Fixtures blocked by feature/training gates | 27 |
| Visible Combo Home probabilities | 0 |
| Visible Combo Away probabilities | 0 |

The validator confirms all 50 selected groups and five markets are represented; all research rows remain production-ineligible; the Combo probability columns remain blocked; and required output files are present. This is an output-contract check, not verification of canonical provider IDs, official settlement truth or point-in-time data provenance.

## Walk-forward results

Expanding-window rolling-origin folds train strictly before their test intervals. Features and model specification are fixed; no calibration or tuning is applied. Accuracy intervals are 95% Wilson intervals. The stored intervals were independently recalculated from the rounded accuracy/test counts and agree within 0.000005 absolute difference.

| Market | Mean fold accuracy | Fold accuracy range | Mean Brier | Brier skill vs training-prevalence baseline, range | AUC range | Mean 10-bin ECE |
|---|---:|---:|---:|---:|---:|---:|
| BTTS | 53.973% | 52.972%–55.422% | 0.24722 | +0.00409 to +0.00596 | 0.53448–0.54326 | 0.01799 |
| DC_HOME | 70.163% | 69.294%–70.908% | 0.20063 | +0.04690 to +0.05224 | 0.63240–0.63944 | 0.01563 |
| DC_AWAY | 60.631% | 60.203%–61.032% | 0.23281 | +0.05062 to +0.05788 | 0.63018–0.63556 | 0.01235 |
| COMBO_HOME | 57.550% | 56.922%–58.372% | 0.24157 | +0.01240 to +0.01822 | 0.56824–0.57604 | 0.01626 |
| COMBO_AWAY | 64.907% | 64.647%–65.073% | 0.22363 | +0.01429 to +0.02219 | 0.57669–0.58712 | 0.01652 |

These are aggregate research diagnostics, not betting-edge estimates. The primary holdout BTTS accuracy (53.588%) is below its majority-class accuracy baseline (54.143%), despite a slightly better Brier score than the constant-prevalence baseline. No odds-based benchmark or ROI is approved because odds provenance is unverified. ECE is diagnostic only; probabilities remain raw and uncalibrated.

## League-level stability and sample gates

| Diagnostic | Count of 250 league-market rows |
|---|---:|
| Positive Brier skill in every adequately sampled fold (diagnostic only) | 71 |
| Mixed Brier skill across folds | 75 |
| No positive Brier skill in any adequately sampled fold | 4 |
| Insufficient fold sample or metrics | 100 |
| Primary holdout fails minimum 100 train and 100 test samples | 5 |

The five primary-holdout sample failures are the five markets for the Indian Super League. The 100 fold-insufficient rows are a separate limitation: only 150 league-market combinations have adequate samples/metrics across all three folds. Positive Brier skill is not an edge approval; minimum samples alone do not establish predictive skill.

## Data and schedule QA

- Retained archive rows after deduplication: 59,049; duplicate rows removed: 0.
- Explicitly completed matches with numeric scores: 51,870.
- Full 20-feature rows: 51,056.
- Missing normalized fixture IDs in archive QA: 0; same home/away team-ID rows: 0.
- Provider parent competition IDs verified: 0; unavailable: 50.
- All 448 report rows have source fixture and source team IDs present, but canonical fixture joins are `NOT_VERIFIED` for all 448, canonical team joins are `NOT_VERIFIED` for all 448, and settlement truth is `NOT_VERIFIED_AGAINST_PRODUCTION_MARKET_SPEC` for all 448.
- Table-as-of-kickoff: 353 rows contain current snapshots that are not historical standings; 95 rows have missing/unverified positions.
- Odds/xG provenance is `UNVERIFIED_NOT_USED_IN_MODEL` for all 448; calibration status is `RAW_ONLY_UNCALIBRATED` for all 448.
- Seven-day schedule: 47 selected groups have fixtures found; 3 have no fixture in the horizon and need schedule-freshness verification. No fixture in a seven-day window is not, by itself, proof that the league lacks data.

Annual archive counts by UTC kickoff year:

| UTC year | Selected groups | Archive rows | Completed score rows | Full-20-feature rows |
|---|---:|---:|---:|---:|
| 2023 | 50 | 10,202 | 10,202 | 5,675 |
| 2024 | 50 | 14,761 | 14,749 | 13,526 |
| 2025 | 50 | 15,029 | 14,987 | 14,165 |
| 2026 | 50 | 14,605 | 11,932 | 13,633 |
| 2027 | 50 | 4,452 | 0 | 4,057 |

Provider season-start-year counts are a different grouping and must not be conflated with calendar kickoff years:

| Season-start year | Selected groups | Season rows | Archive rows | Completed score rows | Full-20-feature rows |
|---|---:|---:|---:|---:|---:|
| 2023 | 50 | 50 | 15,120 | 15,120 | 10,583 |
| 2024 | 50 | 50 | 14,854 | 14,821 | 13,621 |
| 2025 | 50 | 50 | 15,024 | 15,002 | 14,148 |
| 2026 | 50 | 50 | 14,051 | 6,927 | 12,704 |

These are observed archive counts, not proof of complete provider coverage. Future 2027 fixtures have no settled-result truth.

## Combo governance block

The research predictor target is Double Chance plus a 2–4 total-goal corridor, while the current settlement comparator accepts any total below five. Historical QA reports 9,320 Home Combo and 8,000 Away Combo predictor/ledger disagreements. In the governed upcoming report, 421 raw Combo values per side were masked and 27 additional fixtures were already blocked by feature/training gates; zero Combo probabilities remain visible. Do not choose a market rule unilaterally. Obtain an approved market definition and reconcile historical settlement truth first.

## Outstanding blockers and exact next actions

1. **Canonical competition IDs:** all 50 provider parent IDs are unavailable in the current archive manifest. Reconcile using existing private evidence first. Any live `league-teams` probe remains blocked until explicit provider-credit confirmation.
2. **Fixture/team joins:** source IDs exist, but canonical joins are unverified. Establish an authoritative, reviewed crosswalk; do not fuzzy-match names or infer competition IDs from season IDs.
3. **Settlement truth and Combo:** reconcile completed results against the approved production market/settlement specification and resolve the Combo target discrepancy through governance.
4. **Point-in-time inputs:** historical form is computed strictly before kickoff; current table snapshots are display-only. Verify historical standings, xG definitions and pre-match odds timestamps/provenance before admitting them as inputs or benchmarks.
5. **Schedules:** verify freshness for the three selected groups with no fixture in the seven-day horizon, then refresh through an approved, bounded process.
6. **Calibration and edge analysis:** only after identity, settlement and provenance gates pass; retain chronological holdouts and do not tune repeatedly against them.
7. **Production:** remain `NOT_GRANTED` until all evidence gates pass and a human explicitly approves release.

## Governance

No production model logic, probabilities, calibration, thresholds or frozen 27-league baseline were changed by this validation. No FootyStats calls or credits were used in this run; no private-repository Actions workflow was dispatched. Raw provider data remains private. All outputs are research-only; M-1UP remains blocked.
