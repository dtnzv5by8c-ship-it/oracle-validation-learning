# Project Oracle — xG Temporal-Shift Scope Correction and QA #36 Review

**Evidence cutoff:** 2026-10-30 08:08 SAST  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Starting branch head:** `23a4a31543157398519ed90f59254bdef3fbb9f0`  
**Decision:** Research-only data-quality evidence; production and betting release remain **NOT APPROVED**.

## 1. Latest runtime and H2H evidence

The latest completed full Selected-50 runtime remains [Run #171](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41001723054). Run #170 is also complete, but Run #171 is the newer full runtime and is the correct archive-provenance baseline.

Run #171 artifact `12954131277` was downloaded and checked:
- ZIP SHA-256: `7c0aedb9cd9faca910a225eddd7c5649b8757de51616a5a8955534c6cf72a5db`, matching the GitHub artifact digest.
- Private archive tag: `research-selected50-footystats-history-40447419806`.
- Consumed archive SHA-256: `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`.
- Snapshot overlay disabled; snapshot run ID `0`.
- 50 selected groups, 200 historical seasons, 59,049 retained match records.
- H2H history QA: 51,983 explicit-finished rows with valid integer scores; zero duplicate fixture-signature groups; zero provider fixture-ID collision groups; zero strict kickoff-cutoff violations.

The paired H2H CSV contains 99,955 rows: 19,991 unique fixtures, exactly five markets per fixture, no duplicate fixture/market keys, no missing required prediction fields, and no negative `h2h_days_since_last` values. Independent recalculation from the CSV reproduces the published metrics to the displayed precision:

| Market | Baseline accuracy | H2H accuracy | Accuracy delta | Brier delta (lower better) | Log-loss delta (lower better) |
|---|---:|---:|---:|---:|---:|
| BTTS | 53.649% | 53.769% | +0.120 pp | -0.000110 | -0.000220 |
| DC Home | 69.987% | 70.082% | +0.095 pp | -0.000022 | +0.000066 |
| DC Away | 60.382% | 60.352% | -0.030 pp | -0.000061 | -0.000133 |
| Combo Home | 57.401% | 57.371% | -0.030 pp | +0.000034 | +0.000063 |
| Combo Away | 64.939% | 64.949% | +0.010 pp | +0.000111 | +0.000293 |

Paired population: 19,991 of 20,878 baseline test fixtures (95.75% coverage); baseline and candidate each used 18,913 training rows. Effects are small. DC Home has the strongest accuracy consistency in the five prior expanding folds, but its paired holdout log loss is slightly worse. No H2H market is promoted.

Important artifact limitation: Run #171 predates the latest paired-chronology output addition. Its CSV has `h2h_days_since_last` but not `h2h_last_date_utc`. The runtime's internal H2H QA reports zero strict cutoff violations, and the new offline contract tests pass, but the exact last-meeting timestamp has not yet been emitted and independently checked in a full runtime artifact.

## 2. Newest archive QA and temporal-shift evidence

[Private Archive QA #36](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41008363529), artifact `12956506568`, completed successfully. Its downloaded ZIP SHA-256 `7c9eb9f40c98aebd1840e1e2f75aebb255cbfb6320c47448cedc4d2e92144281` matches the GitHub artifact digest.

The QA JSON pins the same 404474 archive and SHA as Run #171 and reports:
- 50/50 selected season IDs present; 200/200 season rows ingested.
- 59,049 archive match records.
- Primary window 20 March 2025–20 September 2026: 22,291 records, of which 22,256 have provider status `complete`; 35 non-complete rows carry 0–0 score pairs.
- Current selected-season folder: 5,637 rows, including 5,633 provider-status `complete`.
- Official settlement truth remains unverified. Provider status and stored scores are not official settlement proof.

### Scope correction discovered in the temporal-shift summary

The original temporal-shift script selected only league groups that crossed a current-season >=30% xG-zero screen, then labelled the resulting pooled figures generically as current-versus-historical pooled xG. Those figures were valid for the selected outlier subset, but could be misread as a Selected-50-wide estimate.

Independent offline aggregation of the same sanitized QA CSV shows:
- 50 selected groups in the archive manifest.
- 48 groups with current-season xG QA rows; two groups have no current-season xG rows in this audit input.
- 11 of the 48 represented groups cross the exploratory >=30% current-season zero-rate screen in at least one of the three prematch xG fields.

**All 48 groups with current xG QA rows:**

| Field | Current zeros | Historical zeros | Change |
|---|---:|---:|---:|
| Team A prematch xG | 747/5,633 (13.26%) | 577/16,318 (3.54%) | +9.72 pp |
| Team B prematch xG | 749/5,633 (13.30%) | 575/16,318 (3.52%) | +9.78 pp |
| Total prematch xG | 671/5,633 (11.91%) | 516/16,318 (3.16%) | +8.75 pp |

**The 11 outlier-selected groups only** have much higher pooled current rates (36.88%, 37.25%, 33.39% respectively). Those values are conditioned on the current-season outlier screen and must not be described as a Selected-50 universe estimate.

Wilson intervals are descriptive only; they do not adjust for league/season clustering or correlation between home, away and total xG fields. The comparison is current partial-season versus pooled non-current seasons, not a matched full-season causal estimate. It is a data-quality warning, not proof of provider fault, missingness semantics, or point-in-time validity. Numeric zero is preserved and is not recoded or imputed.

### Belgium odds mask

The current Belgium Pro League sample has a market-specific zero-mask pattern: BTTS Yes/No and Double Chance 1X/X2 share a 54/63 zero mask (85.71%); Double Chance 12 is zero on 63/63 rows; full-time 1X2 has one zero on 63 rows; Over/Under 2.5 has no zeros. Bookmaker identity and quote timestamps are unavailable. Do not use 12 as a proxy for 1X/X2 or infer bookmaker/provider semantics.

## 3. Research-only code improvement

The temporal-shift audit is hardened to:
1. Parse count fields as finite, non-negative integers; reject booleans, NaN/Inf, negatives, fractions and malformed values instead of silently converting them to zero or truncating.
2. Reject zero counts greater than numeric populations.
3. Reject duplicate scope/league/field rows and conflicting scope-to-league/current-season identities.
4. Emit per-league rows for all current-selected groups with xG QA rows, marking outlier flags rather than omitting non-outlier groups.
5. Publish separate pooled summaries for all represented groups and the outlier-selected subset.
6. Report 48 represented current-xG groups against 50 archive-selected groups, keeping the two missing xG QA groups visible.

The change only affects sanitized research QA summaries. It does not alter raw xG values, H2H features, production model logic, frozen probabilities, calibration or governance.

## 4. Automated evidence and post-commit verification

The scope correction and strict-count implementation were committed as `cba6c3b89fbfb849446e9a3450e002d63e95cef5`. All three automated workflows triggered from that commit and completed successfully:

| Workflow | Run | Result | Artifact |
|---|---:|---|---|
| Safety Contract Tests | [#441](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41012121879) | PASS | `12958311313`; digest `90bac49c2b773bd645aa99f16e5e4a9013c16a001a80bc26f6629ecf3f16b106` |
| Private Archive QA | [#37](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41012121829) | PASS | `12957738691`; digest `0d05ba352295eba9fa5fc5bd12ead84e2ddb7165d85deaaa77b686b87d900b9f` |
| Dry-Run Planner | [#728](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41012121841) | PASS | `12957579196`; digest `96d00ea0d8140a027567e0f8add822a01679848fc22f148081221563d881f081` |

Safety Contract Tests #441 passed:
- 6 paired-H2H chronology tests;
- 4 H2H output-contract tests;
- 9 xG/odds temporal-shift tests, including strict count parsing, zero-count bounds, duplicate scope/field rejection, and separation of all-group versus outlier-selected pooling;
- the remaining offline safety, settlement, identity, provenance and research contract steps.

Private Archive QA #37 reran the pinned archive workflow and confirmed the temporal-shift audit executed and the sanitized QA artifact uploaded. The corrected output contains 144 league-field rows across 48 current-xG groups, 11 league groups flagged, and 30 individual field-level flags. The all-group and flagged-subset pooled summaries are now separate. The QA artifact continues to identify the exact 404474 archive tag and SHA-256.

Dry-Run Planner #728 passed. Its artifact reports zero network calls and zero paid-provider calls. Its operational readiness remains blocked; the pass is not a current-fixture or betting-readiness approval.

No provider/API calls or credits were made. These workflow passes validate the research-only QA and test changes; they do not replace the required full Selected-50 runtime.

## 5. Remaining blockers and next action

The latest dry-run artifact #727 still reports stale current-feed evidence:
- source manifest generated 8 October; reconciliation generated 7 October;
- last fixture date 17 October; manifest schedule window ends 22 October;
- zero governed current fixture rows emitted;
- 22 identity candidates need human review, 28 remain unresolved, zero are approved;
- zero verified canonical team/fixture joins, parent competition IDs, official settlement truth, or point-in-time xG/odds provenance.
- Planner still includes a legacy Run 56 / crosswalk r17 identity layer (31 matching season IDs, 19 without a record in that older snapshot). This is not a contradiction of QA #36's 50/50 current archive season folders and must not be presented as current 404474 identity coverage.

The separate 200-season ingestion rollup artifact attached to Safety Contract Tests #440 still cites source run `40375285207` and SHA `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`. It is legacy evidence, not the 404474 QA #36 archive. Keep the provenance layers separate.

After the new script/test commit passes automatic safety and private-archive QA workflows, manually dispatch [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml) on this branch with:
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=false`
- `snapshot_run_id=0`

The available GitHub connection can inspect runs/artifacts and commit research-branch files, but cannot dispatch the manual Selected-50 runtime. No provider API calls or credits are authorized or needed for this historical archive validation.

**Release decision:** Research only. Production eligibility and betting eligibility remain false.
