# Project Oracle — H2H Chronology Summary Reconciliation

**Evidence cutoff:** 2026-10-30 11:58 SAST  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Code/test head reviewed:** `246b0e7f114e7514f1caf042050a6783a36be8cf`  
**Decision:** Research-only validation improvement accepted. Production and betting eligibility remain **NOT APPROVED**.

## Executive finding

The latest completed Selected-50 full historical runtime remains Run #172 (run ID `41025566727`), which failed in the final output validator while parsing `oracle_selected50_h2h_paired_chronology_qa.json`. The serialization defect was corrected and covered by tests, but no later full historical runtime has been dispatched. Run #172 therefore remains the last full-runtime attempt and does not provide a retained, independently reviewable paired H2H output artifact.

This review found a second, separate contract weakness in `validate_h2h_comparison_outputs`: the validator trusted the chronology QA `status` and checked only a subset of the failure counters. It did not reconcile the QA's market list, per-market row counts, composite fixture count, or every failure counter against the paired CSV. A malformed or inconsistent QA summary could therefore claim PASS while one of its unchecked counters was non-zero.

## Research-only correction

Commit `214945213a8ef9073b99322d85c911584621ee57` strengthens `scripts/validate_selected50_runtime_outputs.py` to require:

- Exact integer row count matching the paired CSV (booleans rejected).
- Exact composite `(competition_id, fixture_id)` unique fixture count.
- The complete five-market set with no duplicates.
- Per-market chronology row counts matching independently counted paired CSV rows.
- All 17 chronology failure counters present as integer zero values; missing, non-zero, or boolean values fail closed.
- Both production and betting eligibility explicitly false.

Commit `246b0e7f114e7514f1caf042050a6783a36be8cf` updates the synthetic fixtures and adds five focused regression tests covering non-zero failure counters, market-count reconciliation, expected-market mismatch, composite fixture-count mismatch, and rejection of boolean-as-zero counters.

This is a report-integrity validation change only. It does not alter H2H feature construction, historical labels, model fitting, predictions, calibration, production code, frozen probabilities, thresholds, or governance.

## Automated evidence

The first push-triggered Safety run (#475, run ID `41037601428`) executed on the intermediate script-only commit before the corresponding test-fixture update had landed. It failed because the old synthetic chronology fixture did not yet include the newly required QA fields. This was an expected commit-sequencing failure, not a runtime result.

The subsequent run on the combined code/test commit passed:

- Safety Contract Tests #476: [run 41037623060](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41037623060) — **PASS**.
  - H2H chronology suite: 8 tests passed.
  - H2H paired output-contract suite: 14 tests passed, including all five new reconciliation regressions.
  - Other offline safety suites and compilation checks passed.
  - Artifact 12968094416; downloaded ZIP SHA-256 `05bdf185c81af588a7d15e50c397e07bef4a52a65a66a91cfd1a17d18e399c29`, matching GitHub's published digest.
- Dry-Run Planner #755: [run 41037623589](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41037623589) — **PASS**.
  - Artifact 12968936114; downloaded ZIP SHA-256 `66c9d52ffd6c77e3cf148f16cf831c7ab0e1b761a46acb49063ee4df6370c982`, matching GitHub's published digest.
  - The plan is offline; its artifact reports zero network calls and zero paid provider calls.

These tests prove the strengthened validator contract on synthetic inputs and the dry-run readiness checks. They do not replace a full historical runtime.

## Latest full-runtime status

Run #172 [41025566727](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41025566727) remains **FAIL — final validator**. The job log shows the runtime builder completed and emitted internal H2H diagnostics, then the validator raised:

```
json.decoder.JSONDecodeError: Extra data: line 39 column 2 (char 1111)
```

The corrected single-document JSON writer and its regression test were already committed after that run. No new Selected-50 full historical runtime is present in the latest branch workflow-run list.

Run #171 remains the previous completed H2H benchmark. No new accuracy, Brier, log-loss, AUC, paired-significance, or fold result is claimed in this checkpoint.

## Archive lineage warning

Safety #476's uploaded sanitized ingestion-ledger artifact (artifact 12968094416) reports:

- Source ingestion run: `40375285207`
- Source artifact: `12674706565`
- Source archive SHA-256: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`
- 50 selected groups, 200 seasons, 59,049 rows, zero failed seasons.
- 57 provider requests belong to the historical source ingestion run; this audit made zero provider API calls.

This is a separate 403752 source lineage. It is **not** the pinned 404474 Selected-50 runtime archive and must not be used to certify the latter.

The historical runtime workflow remains pinned to:
- Tag: `research-selected50-footystats-history-40447419806`
- SHA-256: `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`

Run #172's job log recorded that pinned 404474 tag and SHA before its final-validator failure. The next full run must independently confirm the same values and retain its provenance receipt.

## Current readiness blockers from Dry-Run #755

The inspected Dry-Run #755 artifact confirms:

- 50 selected groups.
- 22 crosswalk candidates requiring human review.
- 28 unresolved identity mappings.
- Zero approved mappings, canonical team joins, canonical fixture joins, official settlement-truth joins, or verified point-in-time xG/odds provenance.
- Zero governed current-fixture rows.
- Schedule evidence remains stale: last fixture date 2026-10-17; schedule window ends 2026-10-22; audit date 2026-10-30.
- Combo remains blocked because the predictor target and settlement helper disagree; no market definition was inferred or changed.
- Network calls: 0; paid provider calls: 0.
- Production and betting eligibility: false.

The artifact's 31/19 Run-56 split is a legacy evidence-layer reconciliation and must not be represented as current archive coverage. The 403752 ledger and 404474 runtime asset remain separate.

## Separate Team DNA lane

Team DNA OOS Integrity Tests #1 [41034396710](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41034396710) passed its five synthetic tests. Its source-data audit has not been dispatched and produced no new named-team profile artifact. The 27-league development spine is separate from the Selected-50 archive and is not used as Selected-50 H2H evidence.

## Required next action

Manually dispatch **Oracle Selected-50 Research Runtime and Backtest** from the current branch head:

Workflow: [oracle-selected50-research-runtime.yml](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)

Inputs:

```
Branch: research/oracle-50-league-readiness-audit
confirm_private_archive_read: true
private_archive_release_tag: research-selected50-footystats-history-40447419806
include_current_snapshot: false
snapshot_run_id: 0
```

The available GitHub connection supports run/artifact inspection and repository file commits, but does not expose a workflow-dispatch action. Do not rerun Run #172 on its old commit. Dispatch a new run from the current branch head so it includes the full chronology-summary reconciliation and its tests.

The next runtime must retain and validate the paired prediction CSV, chronology QA JSON, five-market metric reconciliation, paired correctness/McNemar summary, all five H2H chronological folds, archive-consumption receipt, provenance JSON, and uploaded artifacts.

## Governance

No provider/API calls or credits were used in this research pass. All changes are confined to the research repository and branch. Production repository, production model logic, frozen probabilities, calibration, thresholds and governance were not changed. Production eligibility and betting eligibility remain **NOT APPROVED**.
