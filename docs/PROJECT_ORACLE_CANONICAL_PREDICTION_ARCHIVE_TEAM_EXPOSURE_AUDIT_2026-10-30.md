# Project Oracle — Canonical Prediction Archive Exposure & Team Sample Audit

**Research date:** 30 October 2026, 10:22 SAST  
**Lane:** Data Quality & Team/League DNA  
**Target branch:** `research/oracle-50-league-readiness-audit`  
**Classification:** Research-only; no production or calibration changes

## Executive finding

A read-only inspection of the canonical archive in `oracle-football-data` found **210 timestamp-valid pre-kickoff challenger forecasts across 42 fixtures, 9 competition codes and 84 team labels**. All 42 fixtures have the same five-market set and all 210 prediction IDs are unique.

This is useful prospective prediction-exposure evidence, but it does **not** establish team or market performance. The canonical settlement ledger has zero rows; the feature-snapshot manifest and run-artifact ledger are also empty. Every team label occurs in one fixture only. Therefore no team-level hit rate, calibration, market suitability or reliable risk ranking can be calculated.

The 210 rows belong to `FOUR_MODEL_PREDICTION_ENGINE_V1.2`, with `model_status=CHALLENGER`. This is a separate 9-competition cohort, not the 50-league Selected-50 archive and not Oracle V1.6/V1.6.3 production evidence.

## 1. Prediction-ledger evidence

Source: [canonical PREDICTION_LEDGER.csv](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/archive/PREDICTION_LEDGER.csv)  
Blob SHA: `10a2e8ea40d8bc7cd8eecb30fb6933f6548572b1`

| Measure | Result |
|---|---:|
| Prediction rows | 210 |
| Unique prediction IDs | 210 |
| Duplicate prediction IDs | 0 |
| Duplicate fixture/model/version observations | 0 |
| Run IDs | 1 |
| Unique fixtures | 42 |
| Fixtures with all five expected markets | 42 |
| Competition codes represented | 9 |
| Team-name labels | 84 |
| Teams with more than one fixture | 0 |
| Teams with exactly one fixture | 84 |
| Team-market exposure observations | 252, all with n=1 |
| Valid raw probabilities in [0,1] | 210 |
| Strictly pre-kickoff timestamps | 210 |
| Post/equal-kickoff timestamps | 0 |
| Unverifiable timestamps | 0 |

The five archived markets each contain 42 rows: BTTS Yes, Double Chance Home (1X), Double Chance Away (X2), Home 1X + Under 4.5 and Away X2 + Under 4.5.

### Competition coverage

| Competition code | Fixtures | Prediction rows |
|---|---:|---:|
| CRO | 5 | 25 |
| D1 | 5 | 25 |
| D2 | 2 | 10 |
| F1 | 5 | 25 |
| I1 | 5 | 25 |
| NED2 | 5 | 25 |
| RSA | 5 | 25 |
| SWZ | 5 | 25 |
| UKR | 5 | 25 |
| **Total** | **42** | **210** |

This cohort covers 9 competition codes, not the 50-league research universe.

### Timestamp and cutoff assessment

- Prediction timestamp: 4 October 2026, 17:01:24.696 UTC.
- Fixture dates: 9–17 October 2026.
- Prediction-to-kickoff lead time: 115.48 hours minimum, 142.60 hours median, 308.48 hours maximum.
- Data cutoff and event-truth cutoff: 20 September 2026 for every row.
- The cutoff was 14 calendar days before the prediction timestamp and 19–27 calendar days before kickoff.

The timestamp comparison passes, but this is not a source-freshness certification. Retrieval timestamps for the underlying feature values are unavailable.

### Model and decision status

| Field | Count |
|---|---:|
| CHALLENGER model status | 210 |
| CHALLENGER_OUTPUT decision | 110 |
| NO_BET decision | 100 |
| PASS data-quality status | 110 |
| WATCH_PARTIAL_LEAGUE data-quality status | 100 |

The `PASS` label is the archived row's data-quality status; it is not production approval. All rows remain challenger observations.

## 2. Team DNA and market suitability

The 84 team labels each appear in exactly one fixture. Each team consequently has only one exposure for BTTS and one exposure for its relevant side-specific Double Chance and Combo markets.

This is an exposure inventory, not an outcome sample. It cannot support:
- Team-specific hit rates or confidence intervals.
- Home/away team-market accuracy.
- Team-level Brier score, Log Loss or calibration.
- Model-aligned or discordant team classifications.
- Draw, upset or low-scoring risk attribution to a team.

The ledger has team-name strings but no canonical home/away team ID fields or canonical fixture ID field. Identity remains unverified.

## 3. Settlement and feature-snapshot completeness

The canonical archive declares these ledgers in [archive/README.md](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/archive/README.md). Current read-only counts:

| Canonical artifact | Rows |
|---|---:|
| PREDICTION_LEDGER.csv | 210 |
| RUN_REGISTRY.csv | 1 |
| SETTLEMENT_LEDGER.csv | 0 |
| FEATURE_SNAPSHOT_MANIFEST.csv | 0 |
| RUN_ARTIFACTS.csv | 0 |
| TEAM_PROFILE_LEDGER.csv | 0 |
| FIXTURE_DYNAMICS_LEDGER.csv | 0 |
| MODEL_SCORECARD.csv | 0 |
| POSTMORTEM_LEDGER.csv | 0 |
| TEAM_BEHAVIOUR_LEDGER.csv | 0 |
| MISS_DNA_SUMMARY.csv | 0 |
| LEARNING_LEDGER.csv | 13 aggregate/experiment entries |
| database/matches.csv | 0 |
| database/prematch_team_state.csv | 0 |

Sources: [SETTLEMENT_LEDGER.csv](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/archive/SETTLEMENT_LEDGER.csv), [FEATURE_SNAPSHOT_MANIFEST.csv](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/archive/FEATURE_SNAPSHOT_MANIFEST.csv), [RUN_ARTIFACTS.csv](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/archive/RUN_ARTIFACTS.csv), [TEAM_PROFILE_LEDGER.csv](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/archive/TEAM_PROFILE_LEDGER.csv), [FIXTURE_DYNAMICS_LEDGER.csv](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/archive/FIXTURE_DYNAMICS_LEDGER.csv).

The prediction rows contain 210 distinct `feature_snapshot_id` values, plus populated source-manifest and pre-match-state hashes. However, no snapshot manifest rows or run artifacts resolve those IDs. The current pre-match state file is empty.

The current checked-in fixture manifest was generated on 8 October 2026, after the 4 October prediction run. It cannot be treated as the original source manifest for those predictions. The original manifest and state snapshot referenced by the prediction hashes are not recoverable from the current canonical snapshot-manifest/run-artifact ledgers.

The publication adapter [prepare_prospective_four_market_publication.py](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/scripts/prepare_prospective_four_market_publication.py) constructs its snapshot identifier from metadata including fixture, market, model version, raw probability, timestamp, cutoff and source/state hashes. The inspected implementation does not persist the underlying feature payload into the canonical snapshot manifest or run-artifact ledger. Thus the identifier is not, by itself, a retrievable record of the actual prematch feature values.

**Conclusion:** timestamp integrity passes for the 210 archived rows; feature-lineage reproducibility does not.

## 4. Calibration and market-price fields

All 210 rows have valid raw probabilities. The following fields are blank on all 210 rows:

- calibrated_probability
- market_line
- market_odds
- market_implied_probability
- model_edge

The calibration ID is `RAW_INCUMBENT`, but the calibrated probability field is empty. No calibration performance is inferred from that identifier. The market-price fields cannot support price/value or odds-suitability analysis for this cohort.

## 5. Separate aggregate OOS evidence — not merged

The private repository also contains a separate 27-league four-model development evidence set. Its artifacts do not reconcile to one common sample/version:

- [Four-model production report](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/data/four_model_production_report.md): n=5,847 per principal market, 12 folds.
- [Validation V0.2 report](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/research/four_model/FOUR_MODEL_VALIDATION_V0.2.md): n=6,244, 13 folds.
- [Current evidence-gate CSV](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/research/four_model/outputs/four_model_evidence_gate.csv): n=10,535 for the five non-M1UP markets, 12 folds.
- [Current row-level OOS predictions CSV](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/main/research/four_model/outputs/four_model_oos_predictions.csv): empty.

The 13-row learning ledger also contains aggregate four-model, Combo and M1UP research entries, not a team-attributed settlement ledger. Without a matching run manifest, source hashes and row-level OOS predictions, these summaries are not imported into the Selected-50 team-DNA lane and are not used to rank leagues or teams.

## 6. Archive lineage distinction

The two checked-in tag references `research-selected50-footystats-history-40447419806` and `research-selected50-footystats-history-40375285207` return the same checked-in `data/manifest.json` blob SHA `ab4e64f88f29777403c5c942d359f17e60fa91de`. That manifest was built on 1 October 2026 and describes 11,364 match rows, 6,012 goal-event rows, 2,179 one-up truth rows and 11,364 prematch-state rows.

This is a separate controlled data lake from the Selected-50 FootyStats archive previously audited at 59,049 match rows. Identical checked-in manifest content at two tag references does not reconcile their attached private release-asset checksums. Release-asset metadata remains a manual lineage dependency; no equivalence is assumed.

## 7. Existing xG and Belgium odds findings remain open

The earlier Selected-50 research findings remain exploratory:
- Current-season prematch xG zero rates increased across the 48 represented league groups versus pooled non-current seasons; the 11 high-zero league-season cases remain priority data-quality investigations.
- Belgium's current-season BTTS Yes/No and Double Chance 1X/X2 fields remain 85.71% zero-coded in the inspected 63-match scope, while other odds fields are substantially populated.

This cycle did not reinterpret those values or call providers. The original xG/odds source semantics and point-in-time timestamps remain unverified. Re-running those comparisons against a different archive release before resolving lineage would risk mixing populations.

## 8. Operational note

Selected-50 runtime Run [41025566727](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41025566727) built a research summary but failed its final validator on a malformed H2H chronology JSON file (`JSONDecodeError: Extra data`, line 39). The artifact upload did not complete. This is left to the primary H2H integrity lane; this audit did not read or modify H2H data and did not use the failed run's performance summaries as verified evidence.

## 9. Required next actions

1. Restore the original source manifest and prematch-state snapshot referenced by the 4 October run, or explicitly mark them unrecoverable; persist actual feature snapshot payloads and run artifacts in the canonical archive.
2. Populate the settlement ledger only from reconciled official outcome/event truth, linked to the immutable prediction IDs. A `SETTLED` status or a score copied from an unverified feed is not enough.
3. Add canonical fixture and team identity bridges before team attribution.
4. Reconcile the 27-league aggregate OOS artifact versions using run IDs, commit SHAs, source hashes and row-level predictions before using those metrics.
5. Resolve the Selected-50 private release-asset checksum mapping with existing release metadata/archive-owner records.
6. Re-run the xG and Belgium diagnostics only against the agreed, checksum-pinned archive and preserve point-in-time semantics.
7. Build team-market performance profiles only after verified predictions, canonical identities, retrievable prematch snapshots and official settlements are joined chronologically.

## Governance

- Research-only analytics; no provider/API calls or credits.
- No H2H files or locked holdout accessed by this audit.
- No production code, Oracle V1.6/V1.6.3 logic, frozen probabilities, calibration or governance changed.
- No team/league exclusions or betting recommendations made.
