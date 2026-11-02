# Project Oracle — Market Intelligence Signal Discovery Run 6

**Status:** Research-only; no production or betting eligibility.  
**Inspected research-branch HEAD before checkpoint write:** \`f286d8446abc7add152d636a28f45b234d5aab96\`  
**Implementation commit:** \`f286d8446abc7add152d636a28f45b234d5aab96\`  
**Successful workflow run:** [41366334175](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41366334175)  
**Aggregate artifact:** \`oracle-run8-full-selected50-nested-ablations\`, artifact ID \`13107072640\`.

## 1. Run objective

Recover the original Feature Edge Run 8 event-time workbook/ledger if available; otherwise rebuild from the exact pinned Selected-50 archive without provider API calls. Test the two candidate interactions as nested ablations against the same main-effects model, with league-only comparison and a frozen Oracle V1.6 comparison where a matching historical ledger exists.

## 2. Run 8 binary recovery and exact blocker

The original v18 workbook and companion bundle remain unavailable in the 402-file Library spreadsheet/ZIP inventory and the accessible repository tree. The repository contains manifests, summary documentation and checksums only.

| Asset | Declared size | SHA-256 |
|---|---:|---|
| Feature Edge v18 workbook | 17,301,081 bytes | \`66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7\` |
| Run 8 companion bundle | 29,242,558 bytes | \`b44e99c3ee9b1e1e4515739d810ec10b0bab1c8c718ef2918ec3f1bf78a08e2f\` |

The original Run 8 methodology document records the primary window and fold sample counts, but not the exact fold cutoff timestamps or training start. Therefore this run is a transparent rebuild, not a byte-identical recovery of the missing workbook/companion bundle.

## 3. Pinned archive rebuild

The private release asset was downloaded read-only and its SHA-256 independently matched the pinned release checksum:

\`bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261\`

| Archive QA | Result |
|---|---:|
| Raw match records | 59,049 |
| Season files | 200 |
| Exact Selected-50 groups mapped | 50/50 |
| Exact season mappings | 200/200 |
| JSON parse errors | 0 |
| Date parse failures | 0 |
| Missing fixture/team identities | 0 |
| Duplicate identity keys quarantined | 0 |
| Provider API credits used | 0 |

### Home/away flag interpretation

The source \`no_home_away\` flag is not a neutral-ground indicator. A value of 1 means home/away is undistinguished; it does not prove the match was played at a neutral venue. Only explicit value 0 was used for home-role/away-role histories and for target fixture eligibility. All settled score-complete records, regardless of this flag, could contribute to overall team form. H2H goal history is pair-based and does not require home/away orientation.

Primary-window identity-complete records: 22,291; settled score-complete records: 22,256; home/away-distinguished settled targets: 17,780; home/away-undistinguished settled records: 4,476.

## 4. Event-time reconstruction and sample gates

- Primary target period: 20 March 2025–20 September 2026.
- Reconstruction training start: 20 March 2024. This is an inferred one-year pre-primary lookback consistent with the recorded Run 8 source/primary row-count difference; the original binary does not verify the exact start.
- Fold test windows used:
  - FOLD 1: 20 March 2025–30 September 2025.
  - FOLD 2: 1 October 2025–31 March 2026.
  - FOLD 3: 1 April 2026–20 September 2026.
- These are contiguous calendar partitions of the 18-month primary period. The original Run 8 document does not contain exact cutoff timestamps, so exact fold-boundary equivalence cannot be claimed.
- History cutoff is strict earlier-than-kickoff. All fixtures at an identical competition/kickoff timestamp are evaluated before any result at that timestamp enters history. No additional 24-hour lag was applied; the original Run 8 methodology describes strict pre-kickoff history, whereas a later checkpoint note mentioning 24 hours was inconsistent with that source document.
- Only actual settled, score-complete prior matches count toward sample sizes. No pseudo-counts are used.
- Overall form requires at least five observed prior matches for both teams.
- Venue features require at least five prior home-role matches for the home team and five prior away-role matches for the away team, with explicit home/away distinction.
- H2H goal-rate evidence is only exposed when at least five prior pair meetings exist.

### Fold sample counts

| Fold | Train N | Raw distinguished settled test N | Overall N>=5 | Venue N>=5 | Test league groups |
|---|---:|---:|---:|---:|---:|
| FOLD 1 | 12,419 | 6,393 | 6,078 | 5,824 | 47 |
| FOLD 2 | 18,243 | 6,229 | 6,181 | 6,004 | 44 |
| FOLD 3 | 24,247 | 5,158 | 4,844 | 4,648 | 45 |
| Pooled OOS | — | 17,780 | 17,103 | 16,476 | 48 |

All 50 groups mapped exactly. Two groups had no home/away-distinguished settled target fixtures in the primary window; 48 groups contributed to the pooled venue-eligible test population. Pooled H2H N>=5 coverage was 6,400 fixtures (36.0% of raw distinguished settled targets).

The original Run 8 reference fold sizes were train/test: 8,325/4,876; 13,201/5,828; 19,029/4,299. The current counts differ because this is the full 50-group population with an explicit home/away-distinction rule and strict five-match venue gate.

## 5. Model design

One fixed, uncalibrated logistic-regression pipeline was used for every model/fold: \`C=0.1\`, LBFGS, maximum 2,500 iterations; training-fold median imputation and standardisation for numeric features; one-hot selected-league effect. No hyperparameter tuning or post-hoc probability calibration was performed.

Models:
1. League-only baseline.
2. Overall-form-only: home/away last-five PPG, goals for and goals against.
3. Main effects: the same six overall-form variables plus home-at-home and away-away last-five PPG, goals for and goals against.
4. Main effects plus Home Strength × Away Weakness.
5. Main effects plus Home Attack × Away Defence.
6. Main effects plus both interactions.

Markets: DC_HOME, DC_AWAY and BTTS. Comparisons use identical eligible fixtures within each fold.

## 6. Principal findings

### 6.1 Venue features add incremental value for result-direction markets

Comparing main effects (overall + venue) with overall-form-only, pooled OOS results were:

| Market | Brier delta | Log-loss delta | AUC delta | ECE delta | BY q: Brier / log-loss / AUC |
|---|---:|---:|---:|---:|---|
| DC_HOME | -0.001604 | -0.004086 | +0.010703 | +0.004552 | 0.00403 / 0.00266 / 0.07474 |
| DC_AWAY | -0.002286 | -0.004828 | +0.012154 | +0.001657 | 0.00005 / 0.00005 / 0.01683 |
| BTTS | +0.000191 | +0.000379 | -0.002134 | +0.000338 | 1.00000 / 1.00000 / 1.00000 |

Negative Brier/log-loss is better; positive AUC is better; positive ECE is worse. Venue features improved pooled Brier and log loss for both double-chance markets after joint BY correction. AUC improved significantly after BY correction for DC_AWAY; the DC_HOME AUC improvement did not pass BY 5%. The direction of Brier/log-loss/AUC deltas was favourable in all three folds for both double-chance markets, although fold-level BY-adjusted tests were not individually significant. BTTS did not benefit.

This is the strongest result from this run: home-role and away-role histories appear to add information beyond overall form for result-direction markets in the reconstructed 48-group OOS population. Calibration did not improve; pooled ECE increased for both double-chance markets.

### 6.2 Candidate interactions do not add useful independent value

Nested comparisons held the main-effects model fixed and added one interaction at a time.

- Home Strength × Away Weakness: changes were effectively zero. No interaction metric passed the joint BY correction.
- Home Attack × Away Defence: worsened DC_HOME and DC_AWAY Brier/log loss/AUC; no BY-significant improvement.
- Both interactions together: worsened DC_HOME and DC_AWAY proper scores/discrimination; no BY-significant improvement.
- BTTS interaction deltas were negligible and not significant.

Constituent-controlled partial Spearman correlations, controlling for the interaction's constituent variables and selected-league fixed effects, were close to zero:

| Market | Interaction | Partial rho | p-value |
|---|---|---:|---:|
| DC_HOME | Home Strength × Away Weakness | +0.007630 | 0.3274 |
| DC_HOME | Home Attack × Away Defence | +0.007026 | 0.3671 |
| DC_AWAY | Home Strength × Away Weakness | -0.011439 | 0.1420 |
| DC_AWAY | Home Attack × Away Defence | +0.004654 | 0.5503 |
| BTTS | Home Strength × Away Weakness | -0.013677 | 0.0792 |
| BTTS | Home Attack × Away Defence | +0.001855 | 0.8119 |

No partial-Spearman test passed the joint multiplicity correction. Neither candidate interaction should be promoted.

### 6.3 Overall form versus league-only

Overall-form-only materially improved DC_HOME and DC_AWAY Brier, log loss and AUC relative to league-only, with BY-adjusted q<0.05. BTTS improvements were small; only its AUC comparison passed BY 5%, without a corresponding proper-score improvement.

### 6.4 Calibration

ECE and reliability bins were calculated, but probabilities were not post-hoc calibrated. ECE effects were mixed and no ECE comparison passed BY 5%. The result-direction discrimination improvement must not be mistaken for calibrated probability readiness.

## 7. Multiplicity and uncertainty

- Joint test family: 294 tests across paired model comparisons, all three markets, each fold and pooled OOS, plus six pooled constituent-controlled partial-Spearman tests.
- BH q<0.05: 59 tests.
- BY q<0.05: 46 tests.
- The BY-significant results were confined to overall-form/venue feature comparisons against their simpler baselines. No interaction or partial-Spearman test passed BY 5%.
- Confidence intervals are t-based intervals across per-league paired metric deltas (league-cluster mean estimand). The pooled delta is fixture-weighted and is reported separately; those two quantities can differ, particularly for ECE. They are not interchangeable.

## 8. Frozen Oracle V1.6 comparison remains blocked

The accessible canonical prediction archive contains 210 records, all marked \`FOUR_MODEL_PREDICTION_ENGINE_V1.2\` and \`CHALLENGER\`. The settlement and feature-snapshot manifests are header-only. No matching frozen Oracle V1.6 fixture-level probabilities and settled outcomes exist for these historical folds. No challenger output was substituted or labelled as V1.6.

## 9. Provenance and governance

- Provider publication/capture timestamps are not verified. Strict event-time ordering is not proof that the underlying provider data was published before kickoff.
- Official settlement truth is not independently verified; the rebuild uses the pinned archive's settled status and score fields.
- xG without verified capture timestamps was not used.
- Provisional standings were not used.
- No raw provider rows, fixture-level predictions or feature panel were exported; only aggregate metrics, reliability bins, coverage and governance metadata were uploaded.
- Provider API credits used: 0.
- Oracle V1.6 production logic and probabilities changed: no.
- Canonical ledgers changed: no.
- Existing production workflows changed or dispatched: no.
- Production/betting eligibility: false.

## 10. Execution and test record

The first implementation attempt exposed a syntax defect and was corrected before the final run. A subsequent test-discovery issue (function-style tests were not discovered by unittest) was corrected by converting the suite to \`unittest.TestCase\`.

Final successful workflow run [41366334175](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41366334175):
- 8/8 contract tests passed.
- Pinned archive download and SHA-256 verification passed.
- Full Selected-50 rebuild and nested ablations completed.
- Aggregate-only artifact uploaded.

## 11. Next steps

1. Recover the original Run 8 workbook/companion bundle or obtain its exact fold cutoff manifest to resolve the remaining fold-boundary uncertainty.
2. Obtain a matching historical frozen Oracle V1.6 probability/settlement ledger before attempting a production-baseline comparison.
3. Verify provider publication-time provenance and official score settlement before describing the features as fully point-in-time.
4. Investigate why venue features improve result-direction proper scores but worsen ECE; test calibration on a separate chronological calibration window without touching production.
5. Validate the venue signal in a separate league-held-out and later temporal window before considering any promotion.
6. Keep both candidate interactions rejected unless new independent evidence emerges.
