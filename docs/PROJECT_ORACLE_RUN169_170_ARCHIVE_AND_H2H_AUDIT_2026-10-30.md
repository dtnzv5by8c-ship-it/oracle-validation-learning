# Project Oracle — Run 169/170 Archive Provenance and H2H Audit
Date: 2026-10-30

## Executive outcome

Runs #169 and #170 both completed successfully, but they are duplicate executions of the same research commit and the same archive input. They are not independent validation samples. Both consumed archive release `research-selected50-footystats-history-40375285207`, not the intended `research-selected50-footystats-history-40447419806`.

This provenance discrepancy is material. The run success must not be described as validation of the intended 40447419806 archive.

## Run evidence

| Item | Run #169 | Run #170 |
|---|---:|---:|
| GitHub run ID | 40995652102 | 40995653217 |
| Conclusion | success | success |
| Commit | `c9d8f793317ad0b55a15225c69d1c00f29b6c875` | same |
| Artifact ID | 12950664148 | 12951506425 |
| Archive tag actually consumed | `research-selected50-footystats-history-40375285207` | same |
| Archive SHA-256 | `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f` | same |
| Snapshot overlay | disabled | disabled |

The job logs explicitly show `PRIVATE_ARCHIVE_RELEASE_TAG=research-selected50-footystats-history-40375285207`. The provenance JSON independently records the same tag and archive SHA.

The paired-prediction CSV, H2H ablation metrics JSON, H2H expanding-window metrics JSON and prediction report CSV are byte-identical between the two artifacts. The second run therefore adds execution redundancy, not new historical evidence.

## Intended archive release and corrective control

The intended release `research-selected50-footystats-history-40447419806` was published 2026-10-27. Its private archive asset is 66,452,206 bytes and GitHub reports SHA-256:

`af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`

The earlier 40375285207 asset is 66,451,830 bytes and has a different SHA-256. These releases must not be treated as interchangeable.

### Research-only correction committed

The runtime workflow now:
- defaults to and falls back to `research-selected50-footystats-history-40447419806`;
- pins the expected archive asset SHA-256 to the verified GitHub release digest;
- fails closed if the downloaded archive SHA does not match that pinned digest.

A workflow-contract regression test asserts the intended tag, digest and fail-closed comparison.

Commits:
- Workflow archive pin: `549d333388e0533f806939ea0e2f41f46d2e413c`
- Contract test: `50cf8dd4cf10f4afc41dd48f70d769920d41cc34`

This change affects only the research runtime workflow. It does not alter the production repository, production model, frozen probabilities, calibration or governance.

## H2H integrity evidence from Run #170

The feature QA artifact reports:
- 59,049 source history rows retained after archive deduplication;
- 51,983 explicitly finished rows with valid integer scores;
- 0 explicitly finished rows excluded for invalid/non-integer scores;
- 0 completed score rows excluded for missing or identical team IDs;
- 0 duplicate fixture-signature groups (same competition, kickoff and unordered team pair);
- 0 conflicting duplicate-signature groups;
- 0 provider fixture-ID collision groups;
- 0 strict pre-kickoff H2H cutoff violations;
- 46,323 rows with prior H2H history;
- 33,067 rows with cross-season prior H2H history;
- 128,936 summed cross-season prior meetings.

These are archive/runtime diagnostics on the 40375285207 input. They do not certify canonical team/fixture identity or official settlement truth. The H2H feature unit-test step passed in both runtime jobs, but the corrected 404474 archive has not yet been exercised.

## Independent paired-artifact audit

The paired CSV was independently parsed and metrics recomputed from the same rows.

Structural checks:
- 99,955 rows = 19,991 fixtures × 5 markets;
- exactly 19,991 unique fixture IDs;
- exactly one row per fixture/market key (zero duplicate fixture/market keys);
- every fixture has all five markets;
- date, competition, home team and away team are consistent across each fixture's five market rows;
- all four H2H feature fields are populated in every paired row;
- baseline and H2H candidate are evaluated against the same outcome labels on the paired fixture subset.

The recomputed accuracy, Brier score, log loss and AUC match the reported H2H ablation metrics to the report's rounding precision. This confirms the summary metrics are reproducible from the paired CSV; it does not validate the source settlement labels.

### Paired holdout results

Primary window: 2025-03-20 through 2026-09-20.

Baseline test set: 20,878. H2H-eligible paired test fixtures: 19,991 (95.75% coverage). Baseline and candidate training sizes are both 18,913.

| Market | Baseline accuracy | H2H accuracy | Accuracy delta | Brier delta (lower better) | Log-loss delta (lower better) |
|---|---:|---:|---:|---:|---:|
| BTTS | 53.649% | 53.769% | +0.120 pp | -0.000110 | -0.000220 |
| DC Home | 69.986% | 70.082% | +0.095 pp | -0.000022 | +0.000070 |
| DC Away | 60.382% | 60.352% | -0.030 pp | -0.000064 | -0.000133 |
| Combo Home | 57.401% | 57.371% | -0.030 pp | +0.000034 | +0.000063 |
| Combo Away | 64.939% | 64.949% | +0.010 pp | +0.000111 | +0.000294 |

Positive Brier/log-loss deltas indicate worse probability quality. The small accuracy changes do not establish a betting edge.

### Chronological expanding-window stability

Across five chronological folds, candidate improvements versus baseline were:

| Market | Accuracy improved | Brier improved | Log loss improved |
|---|---:|---:|---:|
| BTTS | 2/5 | 2/5 | 2/5 |
| DC Home | 5/5 | 3/5 | 3/5 |
| DC Away | 2/5 | 1/5 | 1/5 |
| Combo Home | 3/5 | 1/5 | 1/5 |
| Combo Away | 1/5 (2 ties) | 1/5 (1 tie) | 1/5 |

DC Home remains a candidate for further research, but its paired holdout log loss and ECE worsen despite small gains in accuracy, Brier and AUC. BTTS improves slightly on the paired holdout but is inconsistent across the chronological folds. No H2H candidate is approved.

## Runtime output and release gates

Run #170 output contract:
- 50 selected groups;
- 426 future fixture candidates;
- 401 research predictions;
- 25 fixtures blocked for missing required features;
- 2,130 prediction rows (401 × 5 markets plus the report's market structure);
- Combo probabilities fully masked;
- production eligibility false;
- betting eligibility false.

Canonical fixture joins, canonical team joins, official settlement truth and point-in-time xG/odds provenance remain unverified. Combo target/settlement semantics remain unresolved.

## Next action

Manually dispatch **Oracle Selected-50 Research Runtime and Backtest** on branch `research/oracle-50-league-readiness-audit` with:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=false`
- `snapshot_run_id=0`

The updated workflow now pins the expected 404474 archive digest and will fail closed if another archive is supplied. Verify the runtime provenance records tag 40447419806 and SHA-256 `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875` before interpreting any refreshed metrics.

No new provider API calls or provider credits were used for this audit or workflow correction.

## Governance

Research-only work. Production model logic, frozen probabilities, calibration and governance are unchanged. Production and betting eligibility remain NOT APPROVED.
