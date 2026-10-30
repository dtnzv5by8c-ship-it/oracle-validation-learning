# Project Oracle — Run #172 H2H Chronology JSON Failure and Revalidation

**Date:** 2026-10-30  
**Scope:** Research branch only — `research/oracle-50-league-readiness-audit`

## Executive finding

Selected-50 Research Runtime **Run #172** (run ID `41025566727`) completed the archive download, checksum verification, offline contract tests, research runtime build, and the runtime builder's internal H2H chronology gate. It then failed in the post-build output validator while parsing `oracle_selected50_h2h_paired_chronology_qa.json`.

The failure was an artifact-serialization defect, not an observed H2H chronology violation or a model-comparison failure:

```
json.decoder.JSONDecodeError: Extra data: line 39 column 2 (char 1111)
```

Because the validator failed, the workflow skipped the derived-artifact upload. Run #172 therefore does **not** provide a retained, independently reviewable paired H2H CSV or a completed baseline-versus-H2H validation result.

## Run #172 provenance and execution

- Repository: `dtnzv5by8c-ship-it/oracle-validation-learning`
- Branch: `research/oracle-50-league-readiness-audit`
- Runtime commit: `328364d711f13792d084f8613904188367dbf126`
- Workflow: `Oracle Selected-50 Research Runtime and Backtest`
- Run: [41025566727](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41025566727)
- Archive tag observed in job log: `research-selected50-footystats-history-40447419806`
- Archive SHA-256 observed in job log: `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`
- Snapshot overlay: skipped/disabled.

The runtime build step completed. Its emitted QA summary recorded 59,049 historical feature rows, 51,983 explicitly finished score-valid rows, 46,323 rows with prior H2H history, 33,067 cross-season prior-H2H rows, zero strict kickoff-cutoff violations, and zero duplicate fixture-signature or provider fixture-ID collision groups. These are runtime-builder diagnostics, not proof of canonical identity or official settlement truth.

The paired chronology audit is called inside the builder, and the builder exits non-zero if its status is not `PASS_H2H_PAIRED_OUTPUT_CHRONOLOGY`. The builder step completed successfully. However, the post-build validator could not parse the persisted QA JSON, so no final paired chronology artifact was retained for independent inspection.

## Root cause

At Run #172's commit, the runtime wrote the chronology QA JSON using a string suffix containing a literal backslash-plus-`n` sequence rather than an actual newline. The JSON object was followed by non-JSON characters, so Python's strict `json.loads` raised `Extra data`.

This was isolated to serialization of the research QA artifact. It did not require changing feature construction, H2H history, training labels, predictions, calibration, or production logic.

## Corrective change already committed

Commit `c04e7a3b3206bff4ce136bb5fc7e38e98c8222f2` replaced the inline writer with `write_h2h_paired_chronology_qa` in `scripts/audit_selected50_h2h_paired_chronology.py`. The helper writes exactly one JSON document and a real newline using `json.dumps(summary, indent=2) + "\\n"`.

Commit `c06cec281da5e0d046246b13bce5a41002b20986` added a focused regression test, `test_chronology_qa_writer_emits_one_parseable_json_document`, which writes the QA output to a nested temporary path, confirms the trailing newline, and parses the complete file with `json.loads`.

## Post-fix automated evidence

On current research head `c06cec281da5e0d046246b13bce5a41002b20986`:

- Safety Contract Tests **#472** passed: [run 41027748808](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41027748808).
  - H2H paired chronology suite: 8 tests passed, including the new one-document JSON serialization regression.
  - H2H output-contract suite: 9 tests passed.
  - Remaining offline contract suites and compilation steps completed successfully.
- Dry-Run Planner **#751** passed: [run 41027748886](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41027748886).
  - Artifact ID: `12964556604`.
  - Artifact SHA-256: `3e79e1874044b6b674eec4da9f344916d3e6f6f9c25d5082cfd0ad2630091ce8`.
  - Dry-run artifact reports zero network calls and zero paid provider calls.

These checks validate the writer regression and offline readiness contracts. They do not substitute for a new full historical runtime.

## Current readiness blockers from Dry-Run #751

The inspected dry-run artifact still reports:

- 50 selected season IDs.
- Legacy Run 56 identity snapshot: 31 exact joins and 19 absent records; this is explicitly not current 200-season archive coverage.
- 22 crosswalk candidates requiring human review and 28 unresolved mappings.
- Zero approved mappings, canonical team joins, canonical fixture joins, official settlement-truth joins, or verified point-in-time xG/odds provenance.
- Zero governed current-fixture rows.
- Current schedule evidence stale at the 2026-10-30 audit: last fixture date 2026-10-17; schedule window end 2026-10-22.
- Combo remains blocked because predictor and settlement-helper definitions disagree; no market definition is inferred or changed.

No provider/API calls or credits were used in these checks.

## H2H comparison status

Run #171 remains the latest completed full-runtime H2H comparison with retained artifacts. Run #172 did not produce a retained paired prediction artifact because the final validator failed. Therefore:

- Do not publish new H2H accuracy, Brier, log-loss, AUC, fold, or paired-significance results from Run #172.
- Treat Run #171 as the previous benchmark only.
- Re-run the full historical runtime on the current research head before accepting any updated H2H comparison.

## Required next action

Manually dispatch **Oracle Selected-50 Research Runtime and Backtest** from the current research branch:

```
Branch: research/oracle-50-league-readiness-audit
confirm_private_archive_read: true
private_archive_release_tag: research-selected50-footystats-history-40447419806
include_current_snapshot: false
snapshot_run_id: 0
```

Workflow: [oracle-selected50-research-runtime.yml](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)

The available GitHub connector can inspect runs and artifacts but does not expose a workflow-dispatch action. Do not retry Run #172 against its old commit; dispatch a new run on the current branch head so it checks out the serialization fix and regression test.

## Governance

All changes documented here are confined to the research repository and research branch. Production repository, production model logic, frozen probabilities, calibration, thresholds, and governance were not changed. Production eligibility and betting eligibility remain **NOT APPROVED**.
