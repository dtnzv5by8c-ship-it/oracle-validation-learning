# Project Oracle — Selected-50 Run 170/171, H2H Evidence and Runtime QA Review

**Date:** 2026-10-30  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** Research-only. No production repository, production model logic, frozen probabilities, calibration or governance changed. No provider/API calls or provider credits used in this review.

## Executive summary

- Run **#170** completed successfully but consumed the older archive release `research-selected50-footystats-history-40375285207`, SHA-256 `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`.
- Run **#171** completed successfully and consumed the intended release `research-selected50-footystats-history-40447419806`, SHA-256 `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`. The runtime receipt confirms that exact archive was opened and hashed before feature/backtest generation; the snapshot overlay was disabled.
- The H2H paired-prediction CSV and H2H ablation-metrics JSON are byte-identical between Runs #170 and #171. The archive provenance was corrected, but the selected paired holdout predictions and reported H2H metrics did not change.
- Run #171 H2H history QA reports zero strict pre-kickoff violations, zero duplicate fixture-signature groups, zero provider fixture-ID collision groups and zero invalid completed scores. The paired CSV independently contains 99,955 rows: 19,991 fixtures × five markets, with no duplicate fixture/market keys or cross-market fixture metadata conflicts.
- A reporting gap was identified: the paired H2H CSV exposes elapsed days since the last H2H but not the actual last-H2H timestamp. The research branch now adds that timestamp and a fail-closed, independent paired-output chronology/metric contract. These new changes still require workflow execution.
- The newest dry-run and archive QA continue to block production and betting eligibility. Current-fixture evidence is stale, canonical joins and official settlement truth are unverified, and xG/odds point-in-time provenance is unverified.

## 1. Run provenance

| Run | Result | Archive tag | Archive SHA-256 | Snapshot |
|---|---|---|---|---|
| #170 | Success | `research-selected50-footystats-history-40375285207` | `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f` | Not consumed |
| #171 | Success | `research-selected50-footystats-history-40447419806` | `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875` | Not consumed |

Run #171 archive consumption receipt:
- 802 archive members.
- 66,452,206 bytes.
- `archive_open_confirmed=true`.
- `runtime_archive_consumption_status=PASS_RUNTIME_OPENED_INPUT_HASH_VERIFIED`.
- `selected_input_matches_overlay=false`.

Run #171 used commit `f35d8aeef9df8a97b26b8d88a6b7ab7f6fd94311`. A comparison from that commit to the later research branch head showed the subsequent changes were archive-QA, xG/odds diagnostic, tests and documentation work; the Selected-50 runtime builder itself was unchanged before the new paired-output audit work in this checkpoint.

**Cross-run artifact comparison:** the SHA-256 of `oracle_selected50_h2h_paired_predictions.csv` is `165be6c9465b29809afeb7c000ba0693455bd335fa0f6e21e0e226ef14187b18` in both runs. The SHA-256 of `oracle_selected50_h2h_ablation_metrics.json` is `e91c6b0152657ac3616606adabdf324b5f64a165b2cf8aa4e3f7dca582891626` in both runs. Therefore, do not describe Run #171 as an H2H performance uplift over #170; it is a corrected archive-provenance run whose paired output happened to be identical.

## 2. Run #171 runtime and H2H integrity

Run #171 runtime validation reports:
- 50 selected groups and 200 historical seasons loaded.
- 59,049 normalized historical match records.
- 51,983 explicitly finished matches.
- 420 governed fixture candidates in the seven-day report horizon.
- 395 with at least one supported research prediction; 25 blocked for missing required features.
- 2,100 raw prediction rows across five markets.
- Combo Home and Combo Away probabilities masked to zero remaining rows.
- Production and betting eligibility both false.

The embedded H2H history QA reports:
- 51,983 explicitly finished rows with valid integer scores.
- 46,323 feature rows with at least one prior H2H.
- 33,067 feature rows with cross-season prior H2H.
- 128,936 prior H2H meetings counted across feature rows.
- 0 duplicate completed fixture-signature groups.
- 0 duplicate provider fixture-ID groups and 0 conflicting provider fixture-ID groups.
- 0 completed-score rows excluded for invalid/non-integer scores.
- 0 strict kickoff-cutoff violations.
- 919 competition/team-ID groups seen across multiple seasons.
- 0 competition/team-ID groups with multiple normalized names and 0 normalized names mapped to multiple team IDs.

The zero-cutoff result is a technical chronology check against provider IDs and the runtime's selected competition-grouping scope. It does **not** establish canonical Oracle identity or official settlement truth. The 919 cross-season team-ID groups are a continuity diagnostic, not proof of canonical identity.

### Independent paired CSV checks

The downloaded Run #171 paired CSV was independently inspected:
- 99,955 rows.
- 19,991 unique fixture IDs.
- Exactly 19,991 rows for each of BTTS, DC Home, DC Away, Combo Home and Combo Away.
- Exactly five market rows per fixture.
- 0 duplicate fixture/market rows.
- 0 fixture metadata conflicts across market rows.
- 0 missing H2H feature values.
- 0 invalid prior counts, out-of-range BTTS rates, negative average goals, negative elapsed days or non-finite H2H values.
- Test fixture dates span 20 March 2025 through 20 September 2026.

The paired CSV did not include `h2h_last_date_utc`, so this independent file-level check could not recompute elapsed days from the source last-meeting timestamp. The embedded runtime feature QA did separately report zero strict cutoff violations. The new research changes close this observability gap for the next runtime.

## 3. Paired baseline versus H2H candidate

The ablation fits the baseline and H2H candidate on the same H2H-eligible training rows (18,913) and compares them on the same paired test population (19,991). The baseline test population is 20,878, so H2H feature coverage is 95.75%.

| Market | Baseline accuracy | H2H accuracy | Accuracy delta | Brier delta (lower better) | Log-loss delta (lower better) | AUC delta |
|---|---:|---:|---:|---:|---:|---:|
| BTTS | 53.649% | 53.769% | +0.120 pp | -0.00011 | -0.00022 | +0.00186 |
| DC Home | 69.986% | 70.082% | +0.095 pp | -0.00002 | +0.00007 | +0.00043 |
| DC Away | 60.382% | 60.352% | -0.030 pp | -0.00006 | -0.00013 | +0.00001 |
| Combo Home | 57.401% | 57.371% | -0.030 pp | +0.00003 | +0.00006 | -0.00038 |
| Combo Away | 64.939% | 64.949% | +0.010 pp | +0.00011 | +0.00029 | +0.00027 |

Positive Brier/log-loss deltas are worse. The accuracy differences are small. DC Home accuracy is higher on the paired holdout, but its log loss and ECE are worse. BTTS improves on the paired holdout's reported accuracy, Brier, log loss and AUC, but expanding-window stability is mixed.

### Five expanding-window folds

| Market | Accuracy wins | Brier wins | Log-loss wins |
|---|---:|---:|---:|
| BTTS | 2/5 | 2/5 | 2/5 |
| DC Home | 5/5 | 3/5 | 3/5 |
| DC Away | 2/5 | 1/5 | 1/5 |
| Combo Home | 3/5 | 1/5 | 1/5 |
| Combo Away | 1/5 | 1/5 | 1/5 |

**Research conclusion:** DC Home is a candidate for further diagnostic research, not a promotion recommendation. Its accuracy direction is consistent across the five folds, but probability-quality improvements are not. BTTS has a modest paired-holdout improvement but no stable fold advantage. Combo remains blocked pending an authoritative market definition. No calibration or odds/ROI benchmark was performed.

## 4. Corrected private archive QA #35

The latest private archive QA artifact independently reports:
- Release tag and SHA match the intended 404474 archive.
- 50 selected league groups and 50/50 selected IDs present in the archive manifest.
- 200 historical season rows, all marked ingested.
- 59,049 match records with IDs, dates and parseable score pairs.
- 22,291 records in the primary window; 22,291 unique provider match IDs and zero duplicate provider IDs across season rows.
- 35 primary-window non-complete-status records have parseable score pairs; all 35 are 0–0. They are not treated as completed labels.
- Across the full archive, 7,066 non-complete-status records have numeric score pairs, all 0–0.
- 0 records with missing status; 0 invalid score pairs.
- Official settlement truth remains false; production eligibility remains false.

The artifact status is `QA_COMPLETE_REVIEW_REQUIRED`, not production-ready. Selected group labels are not canonical IDs, and primary-window archive row counts are not canonical fixture counts.

## 5. New xG and odds zero-mask evidence

The offline QA #35 xG/odds audit reports:
- 20 zero-co-occurrence fields and 190 field-pair comparisons per season.
- 144 current-season prematch-xG fields screened.
- 11 current-season league groups flagged by a descriptive 30% zero-rate screen.
- Across 33 same-season prematch/postmatch xG field pairs, 586 prematch-zero rows were observed; 584 of those had non-zero postmatch xG.

This is strong evidence that many prematch zeros may represent unavailable/sentinel values, but it does not prove the provider's semantics. Numeric zeros remain unchanged and must not be silently recoded.

Belgium current-season Pro League sample:
- 63 rows.
- BTTS Yes odds zero rate: 85.714%.
- Double Chance 1X odds zero rate: 85.714%.
- Double Chance 12 odds zero rate: 100%.
- Full-time home odds zero rate: 1.587%.
- Over 2.5 odds zero rate: 0%.

This is market-specific coverage, not evidence that all odds are missing. No bookmaker timestamps or point-in-time odds provenance were verified.

## 6. Latest dry-run readiness blockers

Dry-run #714 remains a research-only pass with zero network/provider calls. Its governed readiness summary reports:
- 50/50 current-fixture coverage groups classified stale/inconsistent with no Selected-50 join.
- Latest recorded fixture date 17 October 2026; schedule manifest ends 22 October 2026.
- Current reconciliation generated 7 October and source manifest generated 8 October.
- 22 identity candidates require human review; 28 remain unresolved; 0 approved.
- 0 canonical fixture joins and 0 canonical team joins.
- 0 official settlement truth.
- 0 point-in-time xG provenance and 0 point-in-time odds provenance.
- 0 governed current fixture rows emitted.

The Combo diagnostic finds two disagreement scorelines per side: Home 0–0 and 1–0; Away 0–0 and 0–1. The predictor uses Double Chance AND 2–4 total goals; the settlement helper uses Double Chance AND total goals below five. This is a logic discrepancy, not an authoritative bookmaker settlement rule. Combo remains blocked.

## 7. Research-only code improvements in this checkpoint

A new gap was identified: the paired H2H prediction CSV carried `h2h_days_since_last` but not the underlying `h2h_last_date_utc`. That made independent file-level verification of the strict pre-kickoff cutoff incomplete.

The research branch now:
1. Adds `h2h_last_date_utc` to each paired H2H prediction row.
2. Adds `scripts/audit_selected50_h2h_paired_chronology.py`, which checks competition-scoped fixture/market uniqueness, complete market coverage, valid H2H features/probabilities, strict prior-date ordering and elapsed-days reconciliation.
3. Adds a fail-closed chronology QA JSON to the runtime outputs.
4. Extends `validate_selected50_runtime_outputs.py` to validate paired market counts, same baseline/candidate training populations, coverage arithmetic, five chronological folds, probabilities and research-only eligibility.
5. Adds focused unit tests and wires them into both the manual runtime workflow and push-triggered safety contract workflow.
6. Clarifies the runtime limitation text: H2H is not part of the baseline/production model; the four H2H features are used only in the isolated research ablation.

Commits:
- `569c214012e6b851770f9c36eba17be0f13d7caa` — independent paired chronology audit helper.
- `1f15881acf08be645af68e2c4ba7f6e649d4fef1` — focused chronology tests.
- `57e7dfa913236aad37bb55557e63991ad4996087` — paired CSV last-H2H timestamp and fail-closed QA output.
- `61553176f4db11e227c6a33565ed90b90d881c7c` — paired H2H metrics/fold validation.
- `b865d47a6fc8f9971fb39fd4b1f230170c936cdc` — avoid imposing an artificial upper bound on log loss.
- `b36abf241a5ca70a779c0cf99752b476a1f59f3b` — paired H2H output-contract tests.
- `e2f3dc09f855a2f37124f5ab2e6195aa2fdee844` — publish chronology QA artifact and run tests in runtime workflow.
- `0bfa815d2fe7a7603d35033b1102f343561d7c52` — run new H2H tests in push-triggered safety workflow.
- `6cb00aeaf54bb520dab4efc67800569e65cc58d4` — scope paired artifact keys by competition and fixture ID.

These commits are research-only. At the time this report was written, the final safety run on the latest commit was still in progress; the new H2H runtime artifact contract has not yet been validated by a complete Selected-50 runtime.

## 8. Next action

Run the manual workflow once on the latest branch head after the safety run completes:

`Oracle Selected-50 Research Runtime and Backtest`

Inputs:
- Branch: `research/oracle-50-league-readiness-audit`
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=false`
- `snapshot_run_id=0`

This uses the existing private archive only; no provider/API call or credit is required. The run must verify the new unit tests, emit the paired chronology QA, pass the strengthened output validator, and recalculate the H2H metrics. Compare the resulting metrics to Run #171; do not assume an uplift.

**Release decision:** keep production and betting eligibility unapproved. Canonical identity, official settlement truth, fresh current fixtures, point-in-time xG/odds, calibration and betting-value validation remain open.
