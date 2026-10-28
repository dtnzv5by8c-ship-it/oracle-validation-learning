# Project Oracle — 14-day reporting-window assessment

**Scope:** research-only reporting-window assessment. The runtime generation horizon remains seven days. No predictions were created outside that horizon.

## Verified source artifacts

- Snapshot run [40734991542](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40734991542), artifact [12835634404](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40734991542/artifacts/12835634404). Artifact ZIP SHA-256: `fad627dbda876f8f204b4e6c458a242b17a09312b67acaf264a84d64605a67fd`.
- Snapshot JSON SHA-256: `073723e536d4ee38c14f585f5761ac790dd90989aad380bb985bb38486255761`.
- Runtime run [40739426287](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287), artifact [12839157410](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40739426287/artifacts/12839157410). Artifact ZIP SHA-256: `5d3d0741d513da0245eddc851caace8649db7ca67b9da3451472a33b43e7666d`.
- Runtime prediction CSV SHA-256: `c190d459501a37311f7afb420ea55e700793d9295346212d6d9b83c3007670ba`.
- Snapshot retrieval: `2026-10-28T17:22:27Z`. Runtime start/as-of: `2026-10-28T17:49:57Z`. Snapshot age at runtime start: approximately 27.49 minutes.

The reconciliation uses only these saved artifacts. It makes no provider API calls.

## 14-day assessment, seven-day runtime

| Measure | Result |
|---|---:|
| Snapshot fixture rows | 2,250 |
| Future snapshot rows within 14 days at runtime start | 863 |
| Clean candidates inside the declared seven-day runtime window, after the 15-minute minimum-lead cutoff | 362 |
| Clean candidates from days 8–14, outside runtime generation | **308** |
| Quarantined future rows in the 14-day window | 188 |
| — quarantined for `no_home_away=1` | 179 |
| — quarantined for nonstandard status | 9 |
| Rows inside the 15-minute minimum-lead cutoff | 5 |
| Missing runtime rows among eligible in-window candidates | **0** |
| Ordered-team-ID mismatches among eligible in-window candidates | **0** |
| Exact UTC-kickoff mismatches among eligible in-window candidates | **0** |
| Raw runtime report rows | 460 |
| Raw runtime rows excluded from the safe joined set | 98 |
| — source flag `no_home_away=1` | 91 |
| — nonstandard source status | 7 |
| Nonblank Combo probability cells | **0** |
| Canonical fixture/team joins approved | 0 |
| Official settlement truth verified | 0 |
| Production-eligible / betting-eligible rows | 0 / 0 |

The old overlay trace labels 384 future rows as `BEYOND_7D_NOT_STAGED`. Reconciliation of the saved snapshot separates those into **308 clean out-of-runtime-window rows** and **76 rows with per-fixture quarantine conditions**. The latter must not be described as ordinary out-of-window candidates. The overlay fix now evaluates the source quarantine conditions before assigning the clean beyond-seven-day classification, and records total, quarantined and clean beyond-seven-day counts separately by league.

The raw runtime contains 26 feature-blocked rows. Of the 362 exact safe joins, 25 remain feature-gated. The remaining feature-blocked fixture, `8623482`, is suspended in the snapshot and remains quarantined. No feature, model or probability was changed.

## Research-only code changes

- The safe current-report builder now accepts a separate assessment horizon up to 14 days while keeping the runtime generation horizon capped at seven days.
- A runtime start timestamp is mandatory when assessing beyond seven days; minimum-lead filtering is explicit.
- Clean fixtures beyond the runtime horizon are classified as `OUTSIDE_RUNTIME_GENERATION_WINDOW_NOT_MISSING_JOIN`, not as missing joins.
- Exact safe joins require the same selected-season/fixture key, ordered team IDs and exact UTC kickoff.
- A per-fixture exclusions CSV records quarantine, out-of-window, minimum-lead, missing-runtime, duplicate-key, team-ID and kickoff-mismatch reasons. Every exclusion retains Combo masking and `production_eligible=NO` / `betting_eligible=NO`.
- The snapshot overlay now quarantines flagged/nonstandard rows before classifying clean rows beyond seven days and reports separate total/quarantined/clean counts.

## Validation

- Safe Current Fixture Report Contract [run #14](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40749286744): **PASS, 7 tests**, including the 14-day assessment and exact-kickoff mismatch guard. Commit: `b3e5ef6f9dd6a17fec3cf8b65d928e619c0a60cb`.
- Safety Contract Tests [run #315](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40749425980): **PASS**, all job steps successful on the later provenance checkpoint `924ce3248192583bb511d320fb86f0dca11278b1`.
- Dry-Run Planner [run #614](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40749425976): **PASS, 36 steps**, with explicit `0 network calls and 0 paid provider calls`. Artifact [12843066481](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40749425976/artifacts/12843066481), SHA-256 `0bd5c30ad6a5d7335ec2c843910cd4fe7f5eb2b217c14cc67d3b6aa0a78faf79`.
- The unchanged cross-provider audit was not rerun.
- The committed safe-report builder passed its synthetic contract suite; the actual artifact counts above come from a separate offline reconciliation of the downloaded snapshot/runtime files, not from a newly dispatched safe-report workflow.

## Decision and next safe action

**Do not expand prediction generation or publish predictions for days 8–14.** The 308 clean candidates are outside the current runtime-generation window, not missing joins. Preserve the per-fixture quarantine, exact identity/UTC-kickoff check, market gates and Combo masking.

The latest runtime trace predates the quarantine-precedence fix. A fresh trace would require the public research runtime workflow to read the governed private archive and the existing snapshot artifact. No such dispatch was started in this task. If Nolan chooses to run it manually, use:

- Workflow: [Oracle Selected-50 Research Runtime](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)
- Branch: `research/oracle-50-league-readiness-audit`
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=true`
- `snapshot_run_id=40734991542`

This workflow uses the existing archive/snapshot; do not enable provider refreshes or run the 201-call probe. After a successful run, inspect `current_snapshot_candidate_trace.csv`, `current_snapshot_overlay_qa.json` and `oracle_selected50_runtime_provenance.json`. No production repository write or merge is authorized.
