# Project Oracle — Run 8 Calibration Implementation Checkpoint

**Date:** 2 November 2026 (SAST)  
**Status:** Research-only implementation committed; execution/results not yet verified.

## Repository safety record

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Branch: `research/oracle-50-league-readiness-audit`
- Exact HEAD inspected before this checkpoint write: `5fa6e26ab868288c9266aa05a8c770ceace3abb5`
- Calibration implementation commit: `5fa6e26ab868288c9266aa05a8c770ceace3abb5`
- Parent of implementation commit: `1caf2477a3829431bfdd632307a309ac7de6d771`
- Checkpoint file was confirmed absent before writing.
- Ref update for implementation used expected-head compare-and-swap against `1caf2477a3829431bfdd632307a309ac7de6d771`; it succeeded.
- No production files, Oracle V1.6 logic/probabilities, canonical ledgers or existing production workflows were changed.

## Run 8 asset recovery

A fresh recursive Library inventory covered 495 spreadsheet/archive/data entries (xlsx, xls, zip, csv and parquet). Exact-name/title searches and repository tree inspection did not locate the original Feature Edge v18 workbook or companion bundle.

| Asset | Declared bytes | Expected SHA-256 | Status |
|---|---:|---|---|
| Feature Edge v18 workbook | 17,301,081 | `66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7` | Not recovered |
| Run 8 companion bundle | 29,242,558 | `b44e99c3ee9b1e1e4515739d810ec10b0bab1c8c718ef2918ec3f1bf78a08e2f` | Not recovered |

The original Run 8 methodology and checksums remain in the repository. The exact blocker is absence of both binary assets from the accessible Library inventory and repository tree. The pinned Selected-50 archive remains the valid rebuild source; Run 6 independently verified its SHA-256 and rebuilt the full Selected-50 event-time panel with zero provider API credits. This is a reproducible reconstruction, not recovery of the original workbook.

## Work completed

Added a separate calibration experiment:

- `scripts/calibrate_run8_selected50_venue_models.py`
- `tests/test_calibrate_run8_selected50_venue_models.py`
- `.github/workflows/oracle-run8-selected50-venue-calibration.yml`
- `docs/PROJECT_ORACLE_SIGNAL_DISCOVERY_RUN8_CALIBRATION_PLAN_2026-11-02.md`

The experiment uses the existing Run 8 event-time builder and three reconstructed expanding chronological folds. Each fold reserves the 90 calendar days immediately before its test window for calibration; the model is trained only on earlier observations. Platt and isotonic calibrators are fitted only on calibration-window predictions/outcomes, then applied to untouched test predictions.

Models are evaluated on the same venue-eligible cohort: league-only, overall-form-only and overall-form-plus-venue. The report design includes fold/pool Brier, log loss, AUC, ECE10, reliability bins, held-out calibration intercept/slope, paired league-cluster confidence intervals, joint BH/BY corrections, sample sizes, league coverage and feature missingness.

The five-observed-match overall and venue gates are inherited from the Run 8 builder. H2H is not a model input here and remains subject to N>=5. No pseudo-counts are used. xG without verified capture timestamps and provisional standings are excluded.

## Findings carried forward (not repeated)

The Run 6 nested-ablation experiment already tested both candidate interactions. Neither showed independent incremental value after constituent control and joint BH/BY correction. They were not rerun.

The venue main effects previously improved pooled Brier/log loss for DC_HOME and DC_AWAY, but ECE worsened. The calibration experiment is designed to investigate that specific trade-off.

## Execution status and blockers

- Calibration implementation commit: `5fa6e26ab868288c9266aa05a8c770ceace3abb5`.
- Branch HEAD was verified at that commit after the write.
- The new workflow file is committed and has a push trigger for this research branch.
- The available commit-status endpoint returned no status records, and the available workflow-run connector does not expose push-triggered workflow runs. Therefore this checkpoint does **not** claim that the workflow executed or that its tests/results passed.
- Frozen Oracle V1.6 comparison remains blocked by the previously documented absence of matching fixture-level frozen V1.6 probabilities and settlement truth. No challenger substitution was made.
- Provider publication/capture timestamps remain unverified; event-time ordering alone is not source-publication proof.
- No provider API credits were used.

## Next steps

1. Verify the new GitHub Actions run and inspect all eight contract tests.
2. If successful, retrieve the aggregate-only artifact and review fold/pool metrics, reliability bins, paired CIs and joint BH/BY results.
3. If the run fails, inspect the exact failing step and patch only after rechecking branch HEAD and each target file.
4. Do not repeat the Run 6 interaction diagnostics unless the full original ledger or a materially different, independently verified sample becomes available.
5. Keep all calibration outputs research-only; do not change Oracle V1.6 or promote any probabilities.
