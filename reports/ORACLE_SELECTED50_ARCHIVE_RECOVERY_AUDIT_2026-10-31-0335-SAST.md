# Project Oracle — League DNA / Private Archive Recovery Audit

**Checkpoint:** 31 October 2026, 03:35 SAST  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Scope:** read-only evidence retrieval and reporting.

## Executive finding

The missing 19 selected-50 scoring profiles cannot currently be recovered from the named private FootyStats ingestion workflow. A read-only audit identified **70 workflow runs (run numbers 1–70, 20–27 October 2026); all 70 concluded `failure`, and the Actions artifact endpoint returned an empty artifact list for all 70 runs**. The expected artifact name is `footystats-private-historical-ingestion`. The workflow definition sets 90-day artifact retention, but no artifact was uploaded in any of the 70 checked runs.

The workflow definition is `.github/workflows/footystats-private-historical-ingestion.yml`, added by commit `cb89e5bd1c24810fe821a6b2c3c2c1c19272b381` in the private `oracle-football-data` repository. Its expected package contains season-level `matches.json`, `teams.json`, `tables.json` and `season_stats.json`, plus mapping/manifest/summary files. The workflow is report-only and has contents read permission; raw payloads are intended to exist only in the Actions artifact.

## Failure diagnostics limitation

For run `40447688046`, the `ingest` job failed. GitHub job metadata returned `logs_url=null` and `steps=null`; attempting to retrieve the job log returned `404 BlobNotFound`. The precise failure cause is therefore **unresolved**. This audit does not assume that the API secret was missing, that credits were exhausted, or that any specific provider error occurred.

## Alternative source check

The private repository's legacy `archive/` directory contains prediction, settlement, learning, feature-snapshot and team ledgers, not the missing raw selected-50 season match payloads. Its README describes a separate M-1UP/BTTS controlled data lake whose main match-results spine is Football-Data.co.uk; the historical match-spine manifest identifies FotMob and 27 active leagues. Its `major_footystats_manifest.json` records eight target pages returning HTTP 403, zero parsed/retrieved/new rows and 10,783 pre-existing controlled rows. These are not an exact-ID-mapped replacement for the governed 50 selected FootyStats season groups and were not merged.

## H2H recency cross-check (Team/H2H Run 5, 03:22 SAST)

A new exact-ID Team/H2H shrinkage checkpoint adds 732 team profiles across the 31 raw-payload groups, 7,188 exact provider-ID H2H pairings and 23,328 chronological meetings. Median H2H Kish effective sample is only 2.80 at a 365-day half-life and 2.95 at 730 days; only one pairing reaches effective N >=8 under both settings, while 6,802 remain below the recency reliability screen.

At 365 days with the unoptimized k=10 sensitivity setting, median absolute H2H shrinkage is 18.09 percentage points for Over 2.5 (p90 43.74pp) and 16.54pp for BTTS (p90 44.09pp). These are reliability corrections, not predictive improvements. The diagnostic decision is **do not increase H2H weighting**. No H2H venue split was inferred because the meeting ledger lacks the explicit `no_home_away` flag; k=10/20 are not OOS-validated.

Source note: `docs/PROJECT_ORACLE_TEAM_H2H_DNA_SHRINKAGE_RESEARCH_2026-10-31-0322-SAST.md`; checkpoint: `reports/oracle_selected50_team_h2h_shrinkage_checkpoint_2026-10-31-0322-sast.json`.

## 50-league DNA status remains unchanged

- Governed universe: 50 selected FootyStats season groups; exact season-ID mapping retained.
- Numeric score payloads: 31/50 groups available; 19/50 unavailable.
- 2024: 4 full, 27 partial, 19 unavailable.
- 2025: 31 full, 19 unavailable.
- 2026 through 20 September: 31 full, 19 unavailable.
- League-market evidence: 150 combinations; 26 strict repeatable positive-skill diagnostics across 17 leagues; 13 positive with calibration warning; 47 mixed; 60 insufficient; 4 no positive Brier skill.
- Top-50 lineage: the 02:35 League DNA baseline tabs are retained in this 46-tab audit workbook. The separate 03:02 Feature Edge Run 4 85-tab workbook is the newer ranking/team/H2H consolidation and remains the latest ranking cut. This recovery audit did not refresh or replace those lists; use the 03:02 workbook for the latest exact-ID Top 50. All probabilities remain raw, uncalibrated and research-only.

The 19 unavailable groups remain explicitly unavailable. No values were imputed, zero-filled or inferred.

## Workbook lineage

The attached 46-tab recovery-audit workbook extends the locally available 02:35 League/Market v10 baseline. It is a focused recovery addendum, **not a replacement** for the separate 03:02 Feature Edge Run 4 85-tab consolidated workbook. The 03:02 workbook remains the latest ranking/team/H2H output.

## Controls

- Provider/API credits used: **0**.
- Ingestion/snapshot/runtime/bridge workflows rerun: **0**.
- Oracle V1.6 production logic/probabilities changed: **No**.
- `production_eligible=false`; `betting_eligible=false`.

## Next step

Recover a separately retained exact copy of the raw selected-50 archive (with season IDs, fixture IDs and provenance intact). If no such copy exists, new report-only ingestion requires explicit authorization before any provider/API credit is spent. Do not rerun the failed workflow automatically.

## Files

- `oracle_selected50_private_archive_workflow_runs_2026-10-31-0335.csv` — 70 run IDs, status, artifact probes and URLs.
- `oracle_selected50_private_archive_source_gate_2026-10-31-0335.csv` — source lineage and exclusion decisions.
- `oracle_selected50_archive_recovery_manifest_2026-10-31-0335.json` — workbook hashes and audit counts.
