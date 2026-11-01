# Project Oracle — Market Intelligence Signal Discovery Run 4: Run 8 Recovery Audit

**Date:** 1 November 2026  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Inspected live branch HEAD before write:** `6ad15b1f7bb20b6403e6d4d2d0f9dbe386dbfc19`  
**Previous checkpoint:** `6ad15b1f7bb20b6403e6d4d2d0f9dbe386dbfc19`  
**Scope:** research-only recovery audit; no model rerun or production changes.

## Work completed

- Rechecked the live branch against the Run 3 checkpoint: identical, zero commits ahead/behind.
- Inspected the Run 3 checkpoint, rebuild QA, interaction contract and tests at the inspected HEAD.
- Searched the Library recursively (12 pages / 2,400 root entries), the Project Oracle folder and current conversation attachments. The Run 8 v18 workbook and companion bundle are not present.
- Inspected the complete repository tree at the inspected HEAD (762 entries). The Run 8 note, checkpoint, workbook manifest, archive metadata and compact summary CSVs are committed; the v18 workbook, companion ZIP, full event-time feature ledger and row-level OOS prediction file are not committed.
- Confirmed that the workflow run on the Run 8 parent commit has no downloadable artifacts.
- Downloaded and inspected existing research workflow artifact 13076805703 (run 41289286811). It contains the older archive source SHA `3fea4fbc0b81595fd9fca6691f8eac66efa9ea1d5ac30460bf3646e8dad951ba`, 35,819 archive records across 126 seasons / 42 league folders / 43 provider-catalogue leagues. Its selected-50 overlap is still only 31/50. It is the Run64 source already used in Run 3, not the full Run 8 pinned archive. No provider API calls were made in this run.

## Run 8 assets recovered as metadata only

The committed Run 8 manifest records:

- Workbook: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v18_Run8_Feature_Edge_EventTime_0659SAST.xlsx`; 17,301,081 bytes; SHA-256 `66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7`; 134 sheets (18 new Run 8 tabs; 116 base-sheet XML parts byte-identical).
- Companion bundle: `Project_Oracle_Feature_Edge_Run8_EventTime_Ablations_Bundle_2026-10-31-0659SAST.zip`; 29,242,558 bytes; SHA-256 `b44e99c3ee9b1e1e4515739d810ec10b0bab1c8c718ef2918ec3f1bf78a08e2f`.
- The bundle is described as containing the full event-time feature ledger and OOS predictions. Neither binary was found in the Library, conversation attachments, or repository tree.

The exact pinned archive release is present in private GitHub release metadata:

- Tag: `research-selected50-footystats-history-20261025`; release ID `423439954`.
- Asset: `oracle-selected50-footystats-private-ingestion.zip`; asset ID `675196963`; 66,416,916 bytes.
- Declared SHA-256: `bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261`.

The current GitHub connector exposes the private release metadata but not binary release-asset bytes. The checksum and archive bytes therefore cannot be verified locally in this runtime. The available Run76 artifact is not a substitute: its source archive SHA is `3fea4fbc...`, not the pinned `bc64...` archive.

## Completed interaction work — do not repeat

Run 3 already ran the two candidate interactions as nested expanding-fold ablations on the locally available 31/50-group Run64 subset:

- Core-form cohort: 14,242 fixtures; core-plus-venue cohort: 13,682 fixtures; 31 groups.
- Compared league-only, main-effects-only, each interaction separately and both interactions together. Paired bootstrap intervals and joint BH/BY correction were calculated.
- Constituent-controlled partial Spearman correlations were near zero (absolute partial rho 0.002–0.010); all six interaction partial-correlation BY q-values were 1.0.
- Neither interaction showed repeatable positive incremental value. Adding `home_gf × away_ga` worsened DC_HOME pooled log loss by 0.000304 (BY q=0.035985); adding both interactions worsened it by 0.000385 (BY q=0.035985). No interaction is eligible for promotion.
- These tests compared against the league-only and main-effects research baselines, not frozen Oracle V1.6. They are a 31-group reconstruction, not a full Run 8 reproduction.

## Frozen Oracle V1.6 baseline blocker

The private repository's canonical `archive/PREDICTION_LEDGER.csv` contains 210 rows / 42 fixtures / five markets, all from `FOUR_MODEL_PREDICTION_ENGINE_V1.2` with `model_status=CHALLENGER`. It contains no frozen Oracle V1.6 predictions. `archive/SETTLEMENT_LEDGER.csv` is header-only. It cannot serve as the requested paired V1.6 baseline.

## Determination: can the pinned archive be rebuilt without provider API calls?

**Yes, conditionally.** The pinned 66.4 MB archive is already an ingested release asset. Once its exact bytes are made available locally, feature construction, event-time history generation and the Run 8 ablations can be rebuilt offline with zero new provider API calls. The available Run76 audit demonstrates offline processing (zero provider calls in that audit); its older source archive must not be substituted for the pinned `bc64...` package. The present blocker is binary materialization, not a need for fresh provider data.

## Blockers

1. Run 8 v18 workbook and 29.2 MB companion bundle are absent from the Library and repository artifacts.
2. Pinned full archive release asset metadata is available, but its binary bytes cannot be downloaded through the current UTF-8-only GitHub fetch connector.
3. No row-level frozen Oracle V1.6 prediction/probability ledger with matching fixture IDs and prediction timestamps is available.
4. Source publication/capture-time provenance remains absent. xG without verified capture timestamps and provisional standings remain quarantined.

## Next steps

1. Materialize the exact pinned archive asset or the original Run 8 companion bundle into the Library/runtime; verify its SHA-256 before extraction.
2. Rebuild/verify the full 50-group event-time panel against the Run 8 fold boundaries and fixture identities. Do not substitute the 31-group Run64 extract.
3. Recover the immutable fixture-level Oracle V1.6 probability ledger and matching settlements; otherwise report the V1.6 comparator as unavailable.
4. Only after those inputs are present, run the already-specified nested ablations on the full cohort and compare league-only, main-effects and frozen V1.6 baselines.
5. Preserve strict prior-kickoff construction, five observed prior matches for both teams, venue-specific N>=5, H2H N>=5, no pseudo-counts, and xG/standings quarantine.

## Governance and change record

- This commit adds this recovery checkpoint only; no analysis code or data ledger was changed.
- Oracle V1.6 production logic, probabilities, calibration, canonical ledgers and production workflows remain untouched.
- No provider API credits were used.
- No tests were rerun because no code changed; the prior Run 3 bundle records six local contract tests passing.
- `production_eligible=false`; `betting_eligible=false`.
