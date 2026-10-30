# Project Oracle — Integration & Release-Gate Register

**Evidence cutoff:** 30 October 2026, 11:38 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Branch head:** `4bfbfd1cd365b28cb617108e1b207b604a810a57`  
**Decision:** Research-only progress accepted. Production and betting eligibility remain **NOT APPROVED**.

## Executive decision

New research evidence has landed in three distinct areas:

1. The H2H chronology JSON writer defect from Runtime #172 has been corrected in research code and covered by passing regression tests. The full runtime has **not** yet been rerun, so the corrected end-to-end runtime remains unverified.
2. A separate 27-league Team DNA OOS profile builder and manual read-only audit workflow have been added. Its five synthetic tests passed in GitHub Actions, but the source-data audit has not been dispatched and no new team-profile artifact exists.
3. The Selected-50 dry-run now reconciles the legacy Run-56 31/19 evidence split more explicitly. It still contains a superseded 14,051-row QA snapshot and a separate 403752 archive receipt; neither may be silently treated as the 404474 runtime asset.

**Single highest-value next action:** manually dispatch one corrected full Selected-50 historical runtime from the current research branch, pinned to the existing 404474 archive with current-snapshot overlay disabled. Do not repeat the smaller tests or identity workflow.

No provider/API calls or credits were made by this integration review. No production logic, frozen probabilities, calibration, thresholds or governance were changed.

## 1. New commits integrated

| Commit | Change | Assessment |
|---|---|---|
| `e212f5f` | Added research-only team/league market OOS profile builder, five synthetic tests, test workflow, manual audit workflow and methodology | Safe research-only addition; source audit still pending |
| `eb5a18f` | Corrected manual Team DNA audit output path to use `$RUNNER_TEMP` | Workflow configuration fix |
| `4bfbfd1` | Recorded CI validation checkpoint | Documentation only |
| `83b06db`, `c04e7a3`, `c06cec2` | Added single-document H2H chronology JSON writer, integrated it into runtime builder and added parse-back regression test | Serialization-only correction; no model logic change |
| `32b8d55` | Clarified Selected-50 archive evidence-layer lineage | Retains distinction between separate archive receipts |

The branch head is now `4bfbfd1`. The last tested code-bearing commit for the new Team DNA audit is `eb5a18f`; the later `4bfbfd1` change is a checkpoint/documentation update.

## 2. Latest workflow evidence

I checked run metadata, job steps, artifacts and downloaded ZIP contents.

| Workflow | Run | Commit | Result | Evidence |
|---|---:|---|---|---|
| Team DNA OOS Integrity Tests | [#1](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41034396710) | `e212f5f` | **PASS** | Compile and five research-only synthetic tests passed. No artifact is expected from this test-only workflow. |
| Selected-50 Safety Contract Tests | [#473](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41034397564) | `e212f5f` | **PASS** | Artifact 12967965571; sanitized 200-season ingestion-ledger summary. |
| Selected-50 Dry-Run Planner | [#752](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41034396741) | `e212f5f` | **PASS** | Offline planner and readiness artifact. |
| Selected-50 Safety Contract Tests | [#474](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41034448098) | `eb5a18f` | **PASS** | Artifact 12966903832; same 200-season source-ledger values as #473. |
| Selected-50 Dry-Run Planner | [#753](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41034448210) | `eb5a18f` | **PASS** | Artifact 12967251761; 25 sanitized files covering archive evidence reconciliation, identity quarantine, governed readiness, walk-forward integrity and market gates. |
| Selected-50 Full Historical Runtime | [#172](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41025566727) | `328364d` | **FAIL — final validator** | Runtime build step succeeded; final validator failed parsing H2H chronology JSON. No artifact was uploaded. |
| Selected-50 Full Historical Runtime baseline | [#171](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41001723054) | earlier commit | **PASS — baseline only** | Last completed full runtime; predates the latest paired-output and serialization changes. |

### Artifact integrity

- Dry-Run #753 ZIP SHA-256: `7e7327b3c052c393a575cc7423cf3eb4d158859f60e239b5d2a95e2125d7e714` — matches GitHub's published digest.
- Safety #474 ZIP SHA-256: `77c5d6cdd827cc4735a325bdf1cf578bea8f6a97b4c290cfe89492759374320e` — matches GitHub's published digest.
- Safety #473 ZIP SHA-256: `254396719e4603c164ddc9c9df9ec583c2f7cf56f6bd10df806ffb0f82f1c04e` — matches GitHub's published digest.
- The #473 and #474 ingestion-summary JSON contents are identical, although their enclosing ZIP digests differ.

The #474/#473 ingestion summary describes source ingestion Run 40375285207 and archive SHA `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`. It reports 50 selected IDs, 200 seasons, 59,049 match rows and 3,366 team-season memberships. Its 57 provider requests belong to that historical ingestion run; the audits themselves made zero provider calls. The reported remaining request window is explicitly not monthly credit proof.

### Runtime #172 failure confirmed from job log

The actual failing step was `Validate walk-forward metrics, league gates and governed report outputs`. The validator raised:

`JSONDecodeError: Extra data: line 39 column 2`

The failed file was `oracle_selected50_h2h_paired_chronology_qa.json`. The runtime build itself completed, but provenance capture and artifact upload were skipped. Therefore #172 is not a completed performance result.

The correction in `83b06db`/`c04e7a3` and regression test in `c06cec2` have since been exercised by Safety #472 and the later Safety #473/#474 suites. This establishes the focused code/test correction, **not** end-to-end runtime success.

## 3. H2H reconciliation

Run #171 remains the last verified full-runtime baseline:

- 59,049 normalized historical rows.
- 51,983 completed matches with valid integer scores.
- 19,991 paired fixtures across five markets (99,955 paired prediction rows).
- Zero reported strict pre-kickoff violations.
- Zero duplicate fixture-signature groups and zero provider fixture-ID collision groups.

Previously reconciled candidate-minus-baseline accuracy changes remain:

| Market | Accuracy change |
|---|---:|
| BTTS | +0.120 percentage points |
| Double Chance Home | +0.095 pp |
| Double Chance Away | -0.030 pp |
| Combo Home | -0.030 pp |
| Combo Away | +0.010 pp |

None of the five paired McNemar tests reached the unadjusted 0.05 significance threshold; Double Chance Home was closest at p=0.095673. Probability-quality changes were mixed. No H2H candidate is approved for promotion.

**Gate:** focused chronology/output tests pass; full runtime on the corrected code remains pending.

## 4. Selected-50 archive and readiness reconciliation

### Separate archive receipts — do not merge by row count

| Evidence | Receipt | What it establishes |
|---|---|---|
| Last completed full runtime baseline | 404474 release tag; SHA `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875` | Run #171 consumed this pinned archive; prior QA reported 50 groups, 200 seasons and 59,049 rows. |
| Sanitized 200-season ingestion ledger in Safety #473/#474 | Source Run 40375285207; SHA `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f` | 50/50 selected season IDs, 200 seasons, 59,049 rows, 3,366 team-season memberships. |
| Dry-Run #753 legacy/private-coverage matrix | Pre-batch-5 QA snapshot, 14,051 rows | Explicitly marked superseded for current 200-season coverage; not a current archive receipt. |

The 404474 and 403752 private archive SHA-256 values differ. Equal row counts and shared checked-in manifest references do not prove private release assets are byte-identical. Keep asset lineage open until tag → asset SHA-256 → manifest SHA-256 → source-run provenance is reconciled.

The #753 evidence-layer reconciliation correctly distinguishes 31 exact Run-56 manifest matches from 19 selected IDs with no exact Run-56 manifest record, with separate retained private-package gap evidence. A missing Run-56 manifest row does not prove that a provider request failed or was never attempted. Do not sum the two row-count populations as a deduplicated archive total.

### Current-feed identity quarantine and freshness

Dry-Run #753 reports:

- 50 selected season IDs.
- 22 candidate crosswalk rows requiring human review.
- 28 unresolved mappings.
- Zero approved mappings.
- Zero verified parent competition IDs.
- Zero canonical team joins and zero canonical fixture joins.
- Zero verified provider-season-to-current-feed bridges.
- Zero official settlement-truth rows.
- Zero point-in-time xG/odds provenance rows.
- 12 groups with current-feed label rows; five groups have multiple feed league-ID collisions; 38 have no label rows.
- No current-feed country field and no exact league-ID allowlist groups.

The governed fixture gate emits zero rows. Its schedule evidence is stale: last fixture date 17 October 2026, schedule window ends 22 October, and the audit date is 30 October. The gate remains fail-closed; no unsupported predictions are emitted.

Market gates remain:
- BTTS and Double Chance: blocked on identity, settlement and feature provenance.
- Combo: blocked on target/settlement definition mismatch.
- M-1UP: blocked on stale event truth.

The Combo diagnostic compares `Double Chance AND 2 <= total goals <= 4` against `Double Chance AND total goals < 5`. The 121-scoreline grid finds two disagreement examples for each side (home: 0-0 and 1-0; away: 0-0 and 0-1). This is a logic diagnostic only, not bookmaker settlement approval.

### Aggregate walk-forward audit

The #753 artifact contains a research-only aggregate integrity audit of 15 market-fold records across three folds. It reports raw, uncalibrated probabilities; no calibration was performed and no odds/ROI benchmark was run because odds provenance is unverified. Its 250 league-market rows and 750 league-market-fold rows are reported from the source artifact, not independently rebuilt in this compact audit. This is not a new full runtime or a production performance approval.

## 5. Team DNA reconciliation — separate source populations

### New 27-league Team DNA OOS work

The new builder reads a pinned existing `oracle-football-data` source snapshot at commit `cb89e5bd1c24810fe821a6b2c3c2c1c19272b381`. This is a separate 27-league controlled spine, not the Selected-50 FootyStats archive and not Oracle V1.6/V1.6.3 production evidence.

Existing source summary:
- 12,836 canonical fixtures and 25,672 team-fixture rows.
- 651 Team DNA V2 team labels and 1,302 team-venue profiles.
- 10,139 complete Team DNA rows from 10,362 post-warm-up test fixtures: 97.85% feature completeness, 223 incomplete-feature rows.
- Team DNA score is a 0–150 evidence index, not a probability; 75 is neutral.
- The source artifacts end on 20 September 2026 and were generated 4–6 October; no per-feature retrieval timestamps are available.

Paired development-model OOS summaries report:

| Market | n | Brier improvement | Existing 95% interval | Interpretation |
|---|---:|---:|---:|---|
| DC Home | 10,139 | +0.002112 | +0.001355 to +0.002870 | Positive screening signal |
| DC Away | 10,139 | +0.002131 | +0.001433 to +0.002830 | Positive screening signal |
| Combo Home | 10,139 | +0.000744 | +0.000186 to +0.001302 | Smaller positive screening signal |
| BTTS | 10,139 | +0.000485 | -0.000038 to +0.001007 | Interval includes zero |
| Combo Away | 10,139 | +0.000463 | -0.000053 to +0.000980 | Interval includes zero |
| M1UP Home/Away | 58 each | +0.017049 / +0.007312 | Both intervals include zero | Insufficient sample; one fold, five-league scope |

These are exploratory development-model comparisons. The intervals are row-level normal approximations, not clustered for repeated teams/leagues/time dependence; the league comparisons are multiple exploratory comparisons. They do not support production promotion.

### M1UP export defect and metadata discrepancies

- The M1UP OOS export has 3,300 rows for 825 fixtures, four rows per match and 1,650 duplicate `(match_id, venue)` keys. It is invalid for venue-specific or baseline comparison.
- The clean w250 calibration export has 1,650 team-target rows across 825 fixtures but no venue/team identifiers; aggregate-only.
- The Team Fixture Intelligence manifest reports 562 teams while the generated summary and Team DNA V2 manifest report 651.
- An older report pack has 651 HOME profiles and 650 AWAY profiles; the missing older AWAY profile is Inhulets Petrove (UKR).
- The older `m1up_rate` field is all-zero/unpopulated, not evidence of zero performance.

The new profile builder uses exact `match_id` joins, market-based home/away role assignment, Wilson intervals, Beta(1,1) shrinkage, a minimum n=30 for exploratory discordance flags, and chronological halves only when each half has at least eight rows. BTTS is explicitly treated as a shared fixture outcome duplicated across team exposures, not independent team trials.

Team DNA OOS Integrity Tests #1 passed compile and five synthetic tests. No source-data audit artifact exists yet. The separate manual audit workflow was fixed in `eb5a18f` to use `$RUNNER_TEMP`, but it has not been dispatched. It is pinned to the existing private source commit, performs a read-only sparse checkout, and uploads aggregate outputs only; it does not call a football-data provider.

### Separate 9-competition challenger archive

The canonical prediction archive checkpoint reports 210 archived challenger predictions across 42 fixtures and nine competition codes, 84 team labels with one fixture exposure each, zero settlement rows, zero feature snapshot manifest rows, zero run artifacts and no canonical team/fixture IDs. This is exposure inventory only, not team performance and not Selected-50 or production evidence.

## 6. Concise blocker and release-gate register

| Gate | Current evidence | Status |
|---|---|---|
| Selected-50 historical structure | 50 selected groups / 200 seasons / 59,049 rows in separate receipts | **Structural PASS; asset lineage OPEN** |
| H2H chronology/serialization tests | Safety #472/#473/#474 passed after fix | **PASS — tests only** |
| Full runtime on corrected code | #172 failed final validator; no artifact; no rerun yet | **BLOCKED — rerun required** |
| Parent competition identity | 0 verified | **BLOCKED** |
| Canonical team/fixture joins | 0 verified | **BLOCKED** |
| Human-reviewed identity mappings | 22 candidates; 28 unresolved; 0 approved | **BLOCKED** |
| Official settlement truth | 0 verified | **BLOCKED** |
| Point-in-time xG/odds | No verified as-of/quote timestamps | **BLOCKED** |
| Current governed fixture slate | 0 rows; stale schedule | **BLOCKED** |
| Team DNA named-profile audit | Synthetic tests pass; manual source audit not dispatched | **PENDING** |
| Team-market suitability | No verified prediction-to-official-settlement ledger | **BLOCKED** |
| Combo definition | Predictor/settlement mismatch | **BLOCKED; probabilities remain masked** |
| M-1UP event truth | Stale/unverified | **BLOCKED** |
| Calibration and odds/ROI value | Raw probabilities; no valid price provenance | **NOT ASSESSED / BLOCKED** |
| Production/betting release | Upstream gates not satisfied | **NOT APPROVED** |

## 7. Safe research-only improvements

Completed:
1. H2H chronology JSON writer corrected and covered by parse-back regression test.
2. Team-market OOS profile builder added with exact joins, sample safeguards, shrinkage and chronological halves.
3. Manual Team DNA audit runner path corrected.
4. Selected-50 evidence-layer reconciliation now distinguishes Run-56 manifest absence from retained private-package evidence and warns against treating old 14,051-row QA as current coverage.

Recommended next improvements, without touching production:
- Add a machine-readable archive lineage table separating release tag, private asset SHA-256, package checksum, checked-in manifest SHA and source run ID.
- Make every readiness artifact carry its evidence snapshot/source IDs and an explicit superseded flag; prevent the 14,051-row snapshot from being rendered as current 200-season coverage.
- Refresh the 50-row identity candidate register only from a single checksum-pinned evidence package; retain exact candidate evidence, collisions and human-review status, with no automatic approval.
- Keep official settlements in a separate immutable ledger; require canonical fixture/team joins and official result/status evidence before joining predictions.
- For Team DNA, persist fold-level predictions/metrics and use team/league/time-clustered uncertainty before stronger suitability claims. Keep the M1UP export excluded from venue analysis until its source-side join defect is corrected and independently retested.

## 8. Single highest-value next action — Nolan manual dispatch

The highest-value next action is one corrected full Selected-50 historical runtime. It exercises the fixed H2H JSON writer and the actual pinned archive through final validation, provenance capture and artifact upload.

Open:

[Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)

Select branch:
`research/oracle-50-league-readiness-audit`

Enter exactly:

| Input | Value |
|---|---|
| `confirm_private_archive_read` | `true` |
| `private_archive_release_tag` | `research-selected50-footystats-history-40447419806` |
| `include_current_snapshot` | `false` |
| `snapshot_run_id` | `0` |

Then select **Run workflow**. The available GitHub connection cannot manually dispatch Actions. This historical-only run reads the existing pinned archive; it does not require provider/API calls or credits.

After completion, verify the exact 404474 archive SHA, valid single-document H2H chronology JSON, `h2h_last_date_utc`, zero pre-kickoff violations, all five paired market reconciliations, fold outputs, exact input-to-runtime provenance and uploaded artifacts. Do not approve production or betting eligibility from a green workflow alone.

## Governance

Research-only changes and tests only. No provider/API calls or credits in this review. No production model logic, frozen probabilities, calibration, thresholds or governance changed. Production and betting eligibility remain **NOT APPROVED**.
