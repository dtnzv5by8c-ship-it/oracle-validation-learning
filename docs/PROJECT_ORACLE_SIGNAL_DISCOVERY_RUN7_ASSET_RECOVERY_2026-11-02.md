# Project Oracle — Market Intelligence Signal Discovery Run 7
Date: 2 November 2026 (SAST)
Status: research-only; no production or betting eligibility.

## Repository guard
- Inspected branch: research/oracle-50-league-readiness-audit
- Exact branch HEAD before write: 0f0886cbd4b3b18bbeaa699f0d479a31e4032aff
- Compare result immediately before write: identical to inspected HEAD; ahead=0, behind=0.
- New checkpoint path was confirmed absent at that HEAD.
- This is a documentation-only checkpoint. No model code, canonical ledger, production workflow or probability was changed.

## Run 8 binary recovery result
A fresh recursive Library inventory of spreadsheet/archive/data files returned 497 items across XLSX, XLSM, ZIP and CSV types. The original Feature Edge Run 8 binaries were not present:
- Feature Edge v18 workbook: 17,301,081 bytes; declared SHA-256 66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7.
- Run 8 companion bundle: 29,242,558 bytes; declared SHA-256 b44e99c3ee9b1e1e4515739d810ec10b0bab1c8c718ef2918ec3f1bf78a08e2f.

The search covered exact/semantic Library title searches and a complete paginated inventory of the relevant file types. Neither binary was found. The accessible research repository contains the Run 8 methodology report, manifests/checksums and aggregate summaries, but not either binary. A read-only scan of the private oracle-football-data repository tree (11,787 entries) found no Feature Edge workbook, event-time ledger or companion bundle path. Its release inventory exposes the pinned Selected-50 source archive, not the missing Run 8 workbook/bundle. The Run 6 Actions artifact (ID 13107072640) contains aggregate-only metrics, coverage and reliability files; it intentionally excludes the original workbook, raw provider rows, feature panel and fixture-level predictions.

Primary source documentation: docs/PROJECT_ORACLE_FEATURE_EDGE_RUN8_EVENT_TIME_ABLATIONS_2026-10-31-0659-SAST.md.

## Rebuild status — already completed in Run 6; not repeated
The exact pinned archive was previously downloaded read-only and checksum-verified:
- SHA-256: bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261.
- 59,049 raw records; 200 season files; exact 50/50 selected-group mapping; zero parse errors; zero missing identities; zero duplicate identity keys.
- Provider API credits used: 0.
- Primary home/away-distinguished settled targets: 17,780.
- Five-match overall-form eligible: 17,103.
- Five-match venue eligible: 16,476 across 48/50 groups.
- Run 6 already completed the nested interaction ablations, joint BH/BY corrections, partial-Spearman controls, fold/pooled scoring metrics, reliability bins and paired league-cluster intervals. Those diagnostics were not rerun in this recovery pass.

The Run 6 result remains: venue-role features added incremental Brier/log-loss value for DC_HOME and DC_AWAY, with the DC_AWAY AUC improvement also surviving BY correction; ECE worsened for the double-chance markets. Neither candidate interaction demonstrated incremental value after constituent control and nested ablation.

## Remaining blockers
1. The original v18 workbook and companion bundle are not available in the Library or accessible repository artifacts. Exact binary recovery and byte-for-byte reproduction are therefore blocked.
2. The original Run 8 document gives fold sample counts but not exact cutoff timestamps/training start. Run 6 used transparent contiguous calendar partitions and is a full-Selected-50 reconstruction, not a byte-identical reproduction.
3. A matching historical fixture-level frozen Oracle V1.6 probability/settlement ledger is still unavailable; challenger/development outputs must not be substituted.
4. Provider publication/capture timestamps remain unverified. Event-time chronology is not proof of source-publication timing.

## Next research step
Do not repeat Run 6. The next distinct experiment should investigate the known calibration weakness using the pinned archive: fit the base model before a prespecified 90-day calibration block, fit Platt/isotonic mappings only on that earlier calibration block, and evaluate on the next untouched chronological test fold. Preserve the five-observed-match overall and venue gates, strict earlier-than-kickoff features, and aggregate-only outputs. Keep xG without verified capture timestamps and provisional standings excluded. Keep all outputs research-only.

## Governance
- Oracle V1.6 production logic/probabilities changed: no.
- Canonical ledgers changed: no.
- Production workflows changed or dispatched: no.
- Provider API credits used in this run: 0.
- Production eligible: false; betting eligible: false.
