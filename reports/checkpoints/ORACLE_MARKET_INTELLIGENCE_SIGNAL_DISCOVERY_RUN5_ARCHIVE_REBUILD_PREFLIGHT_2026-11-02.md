# Project Oracle — Market Intelligence Signal Discovery Run 5: Archive Rebuild Preflight

**Date:** 2 November 2026 (SAST)  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Inspected live branch HEAD before write:** `fe20f674cf34d4435cb3368ac6dfca31911ad899`  
**Previous checkpoint:** `fe20f674cf34d4435cb3368ac6dfca31911ad899`  
**Scope:** Run 8 asset recovery and safe offline rebuild preflight. No model rerun and no production changes.

## Work completed

- Re-read the exact Run 8 event-time report, workbook manifest, archive asset metadata, event-time checkpoint, pooled metrics and fold gate counts at the inspected HEAD.
- Re-searched the Library for the exact v18 workbook and companion bundle names and inspected the `/Project Oracle` folder's spreadsheet/archive inventory. Neither Run 8 binary is present. The repository tree contains the Run 8 note, manifests and compact summary CSVs, but not the v18 workbook, companion ZIP, full event-time feature ledger or row-level OOS predictions.
- Confirmed the pinned archive release metadata: tag `research-selected50-footystats-history-20261025`, release ID `423439954`, asset ID `675196963`, size 66,416,916 bytes, declared SHA-256 `bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261`. The binary release asset is not retrievable through the current UTF-8-only GitHub connector.
- Inspected both existing archive workflows. `.github/workflows/oracle-selected50-private-archive-qa.yml` accepts a release-tag override but hardcodes expected SHA-256 `7c60a239...`; its default tag is `research-selected50-footystats-history-40375285207`. Passing the Run 8 tag would fail the hardcoded checksum. Do not dispatch this workflow for the `bc64...` asset.
- `.github/workflows/oracle-footystats-archive-feature-audit.yml` downloads the different `footystats-all-selected-leagues-2024-2026-20261021` archive and a separate catalogue. It is not a valid substitute for the pinned Run 8 archive.
- Inspected `scripts/build_footystats_archive_features.py`. Its current `no_home_away` extraction maps missing/blank values to integer `0` (`int(value in {'1','true','yes'})`). This conflates unknown venue metadata with an explicitly non-neutral fixture. It is therefore unsafe as-is for venue-specific N>=5 feature histories. A new research-only raw-archive parser must preserve `no_home_away` as tri-state: true, false, or unknown; only explicit false may enter home/away venue histories.
- Confirmed the existing three expanding test windows from the Feature Edge fold design: `[2025-03-20, 2025-10-01)`, `[2025-10-01, 2026-04-01)`, `[2026-04-01, 2026-09-21)`. Run 8's reported train/test counts were 8,325/4,876; 13,201/5,828; and 19,029/4,299 on its 31-group source.

## Research decisions

- Do not repeat the two interaction ablations already completed on the Run64 31-group reconstruction. Those tests found no constituent-controlled incremental value; they are not a full 50-group reproduction.
- A full offline rebuild is technically possible without provider API calls once the exact pinned archive bytes are materialised. The present blocker is binary materialisation and safe venue-flag preservation, not a requirement for new provider data.
- The next safe implementation should be a separate research-only workflow that downloads only the exact pinned release asset, verifies both the checksum file and declared `bc64...` SHA, parses raw `no_home_away` without collapsing missing values, and runs the three-fold nested ablations locally in the job.
- Use a common eligible cohort for league-only, main-effects-only and each main-effects-plus-interaction model. Require five observed prior matches for both teams and five explicit non-neutral home-role/away-role observations for venue features. H2H is admissible only at five or more observed prior meetings. No pseudo-counts.
- Produce fold-level and pooled Brier, log loss, AUC, ECE and reliability bins; paired league-cluster bootstrap intervals; constituent-controlled partial-Spearman tests; one joint BH/BY correction family; sample/missingness and selected-league coverage summaries.
- Do not upload raw provider rows, raw feature panels or row-level fixture predictions from the public research repository. Only sanitized aggregate outputs may be retained as workflow artifacts. The original v18 workbook and full companion ledger remain unrecovered.
- Frozen Oracle V1.6 comparison remains blocked until an immutable fixture-level V1.6 probability ledger with matching fixture IDs and prediction timestamps is available. Do not substitute challenger predictions.

## Blockers

1. Run 8 v18 workbook (17,301,081 bytes; SHA-256 `66077dddbb3fd7857edc151c38dc626e3c1c73f58177e138553149c6f0224aa7`) and companion bundle (29,242,558 bytes; SHA-256 `b44e99c3ee9b1e1e4515739d810ec10b0bab1c8c718ef2918ec3f1bf78a08e2f`) are absent from Library and repository artifacts.
2. The exact pinned 66.4 MB archive is available only as private release metadata in this runtime; binary bytes and checksum file have not been materialised or independently verified here.
3. Existing archive workflow checksum is for a different release and cannot safely be reused for the Run 8 tag.
4. Existing feature builder does not preserve unknown `no_home_away` status, so venue-specific features must not be rebuilt from its current collapsed flag.
5. Frozen fixture-level Oracle V1.6 probabilities remain unavailable; no paired V1.6 metric can be reported.
6. Event-time chronology does not establish provider publication/capture time. xG without verified capture timestamps and provisional standings remain quarantined.

## Next steps

1. Add a dedicated research-only pinned-archive recovery workflow using the exact Run 8 tag and `bc64...` checksum; keep all production workflows untouched.
2. Add a tested tri-state event-time feature builder and nested-ablation runner; keep raw archive and row-level feature ledger inside the ephemeral job workspace.
3. Run the three existing expanding folds and publish only sanitized aggregate metrics, paired intervals, joint BH/BY results, reliability bins and league coverage.
4. Recover a legitimate frozen Oracle V1.6 fixture-level probability ledger before attempting that baseline comparison.
5. Reconcile full 50-group feature coverage and venue-flag missingness before drawing conclusions.

## Governance and change record

- This commit adds this preflight checkpoint only; no analysis code or data ledger was changed.
- Oracle V1.6 production logic, probabilities, calibration, canonical ledgers and production workflows remain untouched.
- Provider API credits used: 0. No provider ingestion or prediction workflow was run.
- No code tests were rerun because no code changed.
- `production_eligible=false`; `betting_eligible=false`.
