# Project Oracle — Selected-50 Integration & Release-Gate Register

**Evidence cutoff:** 2026-10-30 10:35 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Branch head at review:** `c06cec281da5e0d046246b13bce5a41002b20986`  
**Decision:** Research-only progress accepted. Production and betting release remain **NOT APPROVED**.

## Executive decision

The latest full Selected-50 runtime, Run #172, built its isolated research outputs but failed the final output validator because the paired-H2H chronology QA JSON was written with a literal escaped newline. The validator rejected the malformed JSON before provenance capture and artifact upload. No Run #172 performance artifact was produced.

I corrected this in the research branch by centralising chronology-QA JSON writing in a tested helper and adding a serialization regression test. The final push-triggered Safety Contract Tests #472 and Dry-Run Planner #751 both passed on the current branch head. The new JSON serialization test passed (8 paired-chronology tests total).

**Highest-value next action:** manually dispatch one new full Selected-50 Research Runtime on the current branch head, using the pinned 404474 archive and snapshot disabled. Do not repeat the identity workflow, small diagnostics, or the failed Run #172 commit.

No provider/API calls or credits were used. No production model logic, frozen probabilities, calibration, thresholds or governance were changed.

## 1. New commits integrated

The latest branch work adds two distinct evidence improvements.

### A. Canonical prediction archive / team-exposure audit

Research-only additions:
- `081021d` — canonical prediction archive exposure audit.
- `3de6044` — regression tests for prediction archive identity/sample gates.
- `501b856` — methodology and team-sample audit documentation.
- `685ee4f` — sanitized canonical archive exposure summary.
- `c5a863a` — aggregate competition coverage rollup.
- `0c51ca8` — aggregate market coverage rollup.
- `c3f6f08` — canonical archive Team DNA checkpoint.

The audit reads a separate canonical archive in `oracle-football-data`; it is not the Selected-50 archive and is not Oracle V1.6/V1.6.3 production evidence.

### B. H2H chronology JSON serialization correction

The failed Run #172 exposed a real output-writing defect. The chronology QA file ended with the literal characters `\\n`, not a newline, so Python's JSON parser raised `JSONDecodeError: Extra data`.

Research-only correction:
- `83b06db` — add a single-document chronology QA writer.
- `c04e7a3` — use the helper in the Selected-50 runtime builder.
- `c06cec2` — add a regression test that writes the artifact and parses it back as exactly one JSON document.

The helper changes serialization only; it does not alter H2H features, fitted models, probabilities, thresholds or labels.

## 2. Latest verified workflow evidence

I checked run metadata, job conclusions, job logs and artifact ZIP digests. The latest completed evidence on the current head is:

| Workflow | Run | Commit | Result | Artifact / interpretation |
|---|---:|---|---|---|
| Safety Contract Tests | [#472](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41027748808) | `c06cec2` | **PASS** | Artifact 12964068161; ZIP SHA-256 `1848cb322ce560e559f5671d0da6c6decb19c6d9d4ef5f531253b632df3a58ce`. Eight H2H paired-chronology tests passed, including the new single-JSON-document regression. |
| Dry-Run Planner | [#751](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41027748886) | `c06cec2` | **PASS** | Artifact 12964556604; ZIP SHA-256 `3e79e1874044b6b674eec4da9f344916d3e6f6f9c25d5082cfd0ad2630091ce8`. Offline plan; zero network and paid-provider calls. |
| Safety Contract Tests | [#469](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41027088775) | `0c51ca8` | **PASS** | Artifact 12964008108; confirms the sanitized 200-season ledger, but its source archive is the older 403752 release (see lineage warning below). |
| Dry-Run Planner | [#748](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41026958990) | `3de6044` | **PASS** | Artifact 12964445724; readiness only. Carries explicitly superseded 14,051-row/Run-56 evidence. |
| Identity & Settlement Evidence Tests | [#16](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41016581498) | `85a1618` | **PASS** | Artifact 12959703263; 10 sample evidence rows, six cross-provider completed-score agreements, zero approved canonical bridges. Not 50-league identity closure. |
| Selected-50 full runtime | [#172](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41025566727) | `328364d` | **FAIL — final validator** | No artifact uploaded. Runtime build step succeeded; final validation failed parsing the malformed chronology JSON. Provenance and upload steps were skipped. |
| Selected-50 full runtime baseline | [#171](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41001723054) | earlier research commit | **PASS — baseline only** | Last completed full runtime using the intended 404474 archive. Predates the latest paired-output changes. |

The downloaded #472 and #751 ZIP files were independently hashed; both matched GitHub's published artifact digests. #472's attached ingestion-ledger artifact is sourced from release 403752 and is not evidence that its private asset is byte-identical to release 404474.

## 3. H2H reconciliation

### Validated baseline

Run #171 remains the latest completed full runtime:
- 59,049 normalized historical match rows.
- 51,983 explicitly finished matches with valid integer scores.
- 99,955 paired H2H prediction rows: 19,991 fixtures × five markets.
- Zero reported strict internal pre-kickoff violations.
- Zero duplicate fixture-signature groups and zero provider fixture-ID collision groups.
- The H2H candidate and baseline use the same paired training population.

The prior paired holdout effects remain small:
- BTTS: +0.120 percentage points accuracy.
- Double Chance Home: +0.095 pp.
- Double Chance Away: -0.030 pp.
- Combo Home: -0.030 pp.
- Combo Away: +0.010 pp.

No exact paired McNemar test was significant at the unadjusted 0.05 level; Double Chance Home was closest at p=0.095673. Its accuracy direction was positive across five folds, but probability-quality gains were mixed. No candidate is approved for promotion.

### Run #172 failure and correction

Run #172 completed the isolated runtime build and generated its in-job summary, but the final validator failed at `load_json("oracle_selected50_h2h_paired_chronology_qa.json")` with `JSONDecodeError: Extra data: line 39 column 2`. The failure was serialization, not a demonstrated model-performance regression. Since validation stopped, provenance and artifact upload did not occur; the run is not a verified new performance result.

The fix is now covered by Safety #472:
- `test_chronology_qa_writer_emits_one_parseable_json_document` passed.
- All eight paired chronology tests passed.
- H2H output-contract tests also passed in the same workflow.

**Remaining:** rerun the full runtime on current head to verify the actual archive-generated paired CSV, chronology QA, five-market metric reconciliation, discordance calculations, fold outputs, provenance and artifact upload together.

## 4. Data quality and archive lineage

### 404474 baseline

Private Archive QA #39 remains the latest completed QA for the intended 404474 release. It reports:
- 50/50 selected league groups.
- 200/200 historical season folders ingested.
- 59,049 match rows.
- 22,291 records in the locked primary window (20 March 2025–20 September 2026).
- 22,256 provider-complete rows and 35 non-complete rows in that window.
- The 35 non-complete rows have numeric 0–0 placeholders and are not settlement truth.

Run #171 consumed:
- Tag: `research-selected50-footystats-history-40447419806`
- SHA-256: `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`

### Separate 403752 ingestion-ledger evidence

Safety #472's uploaded summary reconciles 50 selected season IDs, 200 seasons, 59,049 match rows and 3,366 team-season memberships, but its source archive is:
- Tag: `research-selected50-footystats-history-40375285207`
- SHA-256: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`

The row totals agree with the 404474 baseline, but the archive hashes differ. The two tag references share a checked-in manifest blob; that does not prove their attached private release assets are equivalent. Keep the archive-asset lineage gate open until the release-asset checksums are reconciled. Do not merge the two asset populations at fixture level.

### xG and odds

The current-versus-non-current archive comparison covers 48 league groups with xG observations:

| Prematch field | Current zero rate | Non-current zero rate | Difference |
|---|---:|---:|---:|
| Team A xG | 13.26% | 3.54% | +9.72 pp |
| Team B xG | 13.30% | 3.52% | +9.78 pp |
| Total xG | 11.91% | 3.16% | +8.75 pp |

Eleven group/season observations are in the exploratory high-zero subset (at least 30%). These descriptive differences do not establish that zero is a sentinel or prove a provider defect. Preserve original numeric values; do not impute or exclude leagues.

Belgium's current 63-match scope has 54 zero observations for BTTS Yes/No and Double Chance 1X/X2; Double Chance 12 is zero on all 63. This is market-specific. Source semantics, bookmaker identity and quote timestamps remain unverified, so no ROI/price benchmark is approved.

## 5. Team DNA — separate populations, no performance claim

### Canonical prediction archive audit

The new audit inspected a separate `FOUR_MODEL_PREDICTION_ENGINE_V1.2` challenger cohort:
- 210 prediction rows across 42 fixtures and nine competition codes.
- 84 team-name labels; every team appears in exactly one fixture.
- 252 team-market exposure observations, each with sample size one.
- 210 timestamps are strictly pre-kickoff, but this is not proof that the underlying feature snapshots are retrievable.
- Zero settlement-ledger rows, zero feature-snapshot-manifest rows, zero run-artifact rows, zero canonical team/fixture IDs, and no calibrated probability or odds values.

This is not Selected-50 coverage and is not Oracle V1.6/V1.6.3 production evidence. It cannot support team hit rates, calibration, team-market suitability or risk rankings. Do not merge its aggregate OOS summaries with Selected-50 without matching run, version, source-hash and row-level prediction lineage.

### Selected-50 team context

The earlier Selected-50 exposure audit remains a context inventory, not an outcome ledger. Provider team IDs/team-role profiles are not canonical club identities; short recent-form observations are not Oracle prediction outcomes. A verified prediction-to-official-settlement ledger is still absent.

## 6. Selected-50 readiness and blocker register

The latest Dry-Run #751 artifact remains an offline planning snapshot. It explicitly carries an older 14,051-row pre-batch QA snapshot and Run-56 crosswalk split (31 direct manifest matches / 19 reconciled gaps). Those are historical evidence-layer counts, not a contradiction of the later 200-season archive QA and not current 404474 coverage.

| Gate | Current evidence | Status |
|---|---|---|
| 50 selected season IDs / 200 historical folders | QA #39 on 404474; #469/#472 ledger is separate 403752 source | **PASS for archive structure; asset lineage reconciliation OPEN** |
| H2H chronology and paired-output unit contracts | Safety #472 passed, including JSON serialization regression | **PASS for tests** |
| Full runtime on latest code | #172 failed final JSON validator; no provenance/artifact upload | **BLOCKED — rerun required** |
| Canonical parent competition IDs | 0 verified | **BLOCKED** |
| Canonical team and fixture joins | 0 verified | **BLOCKED** |
| Human-reviewed identity mappings | 22 candidates; 28 unresolved; 0 approved | **BLOCKED** |
| Official settlement truth | 0 verified | **BLOCKED** |
| Point-in-time xG and odds | No verified as-of/quote timestamps | **BLOCKED** |
| Current governed fixture slate | 0 rows; last schedule fixture 17 Oct, manifest end 22 Oct | **BLOCKED — stale** |
| Combo market settlement definition | Predictor/settlement contract mismatch | **BLOCKED; probabilities remain masked** |
| M-1UP event truth | Stale/unverified | **BLOCKED** |
| Calibration and odds/ROI value | Raw probabilities; odds provenance unverified | **NOT ASSESSED / BLOCKED** |
| Production and betting release | All upstream gates not satisfied | **NOT APPROVED** |

The current-feed quarantine reports 12 groups with label rows, five with multiple feed league-ID collisions, 38 with no label rows, zero canonical joins and zero approved mappings. Display-label agreement is not canonical identity evidence.

## 7. Safe research-only improvements

Completed:
1. Fixed the malformed H2H chronology JSON writer.
2. Added an end-to-end serialization regression test.
3. Added canonical prediction archive exposure and aggregate competition/market coverage audits with explicit sample-size and provenance limits.
4. Preserved evidence-layer warnings so stale Run-56/14,051-row outputs are not represented as current 200-season coverage.

Next safe improvements after the full runtime:
- Add an explicit tag → private asset SHA-256 → archive manifest SHA-256 lineage table, keeping asset identity distinct from manifest identity.
- Refresh the 50-row identity candidate register from a single checksum-pinned evidence package, with exact candidate evidence, collisions, human-review state and no auto-approval.
- Keep settlement evidence in a separate immutable ledger and require official result/status provenance before joining it to predictions.
- Retain per-league/per-season xG and odds zero counts with source-time fields; do not rewrite zeros.

No live provider calls, credit-consuming probes, production writes or model changes are authorized by this checkpoint.

## 8. Single highest-value next action — Nolan manual dispatch

The current branch head is `c06cec281da5e0d046246b13bce5a41002b20986`. Safety #472 and Dry-Run #751 have passed on that head. The GitHub connection cannot dispatch a new `workflow_dispatch` run.

Open:
[Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)

Select branch `research/oracle-50-league-readiness-audit` and enter exactly:

| Input | Value |
|---|---|
| `confirm_private_archive_read` | `true` |
| `private_archive_release_tag` | `research-selected50-footystats-history-40447419806` |
| `include_current_snapshot` | `false` |
| `snapshot_run_id` | `0` |

Then select **Run workflow**.

This is a historical-only run against the existing private archive. It makes no provider/API calls and requires no new credits. Do not rerun #172 or dispatch on its old commit. After the new run completes, verify the archive SHA, chronology JSON, paired CSV, all five market metric/discordance reconciliations, chronological folds, provenance receipt and uploaded artifact before updating performance status.

**Production Oracle V1.6/V1.6.3: unchanged. Production eligibility: NOT APPROVED. Betting eligibility: NOT APPROVED.**
