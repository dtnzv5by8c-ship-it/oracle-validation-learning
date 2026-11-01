# Project Oracle — Market Intelligence Signal Discovery Run 5: Archive Rebuild Preflight

**Date:** 2 November 2026 (SAST)  
**Branch:** research/oracle-50-league-readiness-audit  
**Inspected live branch HEAD before this correction:** 556ad8dd6639cbdaf6d42a3662f25ceb8742576f  
**Previous checkpoint commit:** 038ca1b3bb44de994c93a3a2911a34af052417a8  
**Scope:** Run 8 binary recovery and raw venue-flag preflight. Research-only.

## Work completed

- Reconfirmed that the Run 8 v18 workbook and companion bundle are absent from the Library and repository tree. The committed manifest provides names, sizes and checksums only.
- Confirmed the pinned archive release: tag research-selected50-footystats-history-20261025, asset ID 675196963, 66,416,916 bytes, declared SHA-256 bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261.
- Added a separate research-only workflow that reads only this exact private release asset, checks the checksum file against the pinned digest, verifies the downloaded archive bytes, and audits raw no_home_away coverage. It makes no FootyStats/provider calls.
- Added a tri-state parser and synthetic tests: explicit 1/true/yes = neutral; explicit 0/false/no = non-neutral; missing/blank = unknown; other values = invalid. Unknown values are never counted as venue-eligible.
- The workflow uploads aggregate group/season coverage and a summary only. It does not upload the archive, raw provider rows, row-level features or fixture predictions.
- Corrected two workflow-definition issues before accepting any result: GitHub expression interpolation and the exact archive filename in the release download pattern. Earlier in-flight runs reference pre-correction revisions and are not treated as valid preflight results.

## Key technical finding

The existing scripts/build_footystats_archive_features.py collapses a missing no_home_away field to integer zero. That behaviour is unsafe for venue-specific history gates. The new preflight reads the raw archive field directly and preserves unknown values. The existing builder was not modified.

## Existing completed analysis not repeated

Run 3 already tested both candidate interactions as nested ablations on the 31-group Run64 reconstruction and found no constituent-controlled incremental value. This run does not repeat those tests. The full 50-group Run 8 experiment remains blocked until the exact pinned archive is materialised and venue-flag coverage is verified.

## Workflow and outputs

- Workflow: .github/workflows/oracle-run8-pinned-archive-venue-flag-preflight.yml
- Script: scripts/audit_run8_pinned_archive_venue_flag_coverage.py
- Tests: tests/test_run8_pinned_archive_venue_flag_coverage.py
- Expected archive checksum: bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261
- Artifact name: oracle-run8-pinned-archive-venue-flag-preflight (aggregate outputs only; three-day retention).

The corrected workflow is committed in this change. Its run result and archive retrieval are not claimed until the corrected Actions run completes.

## Remaining blockers and next steps

1. Inspect the corrected workflow run. If the private token, release access or checksum fails, record the exact failure and stop; do not substitute another archive.
2. If the checksum passes, inspect tri-state venue coverage across all 50 selected groups and seasons.
3. Build the full event-time feature panel from the pinned archive with strict prior-kickoff ordering, same-kickoff isolation, five observed overall matches, five explicit non-neutral venue-role matches and H2H N>=5. Keep xG without capture timestamps and provisional standings quarantined.
4. Run the two interaction ablations using the three existing expanding folds, with league-only and main-effects baselines, paired intervals, reliability/ECE and joint BH/BY corrections.
5. Frozen Oracle V1.6 comparison remains blocked until an immutable fixture-level V1.6 probability ledger with matching fixture IDs and prediction timestamps is available.
6. Do not export raw provider data or row-level feature ledgers from the public research repository. Only aggregate research outputs may be retained as artifacts.

## Governance

- Oracle V1.6 production logic, probabilities, calibration, canonical ledgers and existing production workflows are untouched.
- No provider API credits used. The new workflow reads the already-acquired private release only.
- No pseudo-counts are used. Five-match gates are observed-match counts only.
- Event-time chronology is not source-publication-time proof.
- production_eligible=false; betting_eligible=false.

## Contract-test correction

- The first corrected-workflow contract run (commit 556ad8dd6639cbdaf6d42a3662f25ceb8742576f) found that the aggregate roll-up attempted to sum string label fields alongside numeric counts. The failing test was isolated to the summary aggregation helper; archive data was not downloaded and no provider calls occurred.
- Updated the helper to sum numeric count fields only. The next push-triggered run must pass the two synthetic tri-state tests before it attempts private archive retrieval.

## Pinned archive access result

- The corrected workflow successfully downloaded the exact 66,416,916-byte private archive and verified its SHA-256 against the declared bc64...e7261 digest. No provider API was called.
- The subsequent audit step failed before parsing the archive because direct script execution did not put the repository root on Python's import path for the shared archive helper. The contract tests themselves passed. The helper import path is corrected in this commit; no archive data was modified or exported.
- The next workflow run will repeat the checksum-verified read and complete the aggregate venue-flag audit. The archive remains ephemeral in the job workspace.

## Successful pinned-archive preflight result

- Corrected workflow run: 41360247981; conclusion SUCCESS. Both tri-state contract tests passed, the exact private release archive downloaded, and its actual SHA-256 matched the pinned digest.
- Aggregate artifact: ID 13104773485, name oracle-run8-pinned-archive-venue-flag-preflight, SHA-256 c95af0baf1e2da5af38ebe4ed9d149ae564e6232cc585aa94cd870d276ee134b. The artifact contains only summary and group/season counts; it contains no raw provider rows or fixture-level predictions.
- Exact mapping passed: 200 season folders mapped to all 50 selected groups using exact country/competition labels; no fuzzy matching, parent-competition inference, unmapped seasons or duplicate season IDs.
- Archive inventory: 59,049 match records across 200 matches.json files; zero file parse errors.
- Primary window 20 March 2025 through 20 September 2026: 22,291 records, of which 22,256 had settled status and complete score pairs.
- Primary-window no_home_away coverage: 100.0% explicit. Of the 22,291 records, 17,792 were explicitly non-neutral and 4,499 explicitly neutral; zero unknown/blank and zero invalid. Among settled-score rows, 17,780 were non-neutral and 4,476 neutral.
- Full archive season coverage independently summed from the aggregate season CSV: 52,132 explicit non-neutral records, 6,917 explicit neutral records, zero unknown/blank and zero invalid across all 59,049 records.
- The pinned archive is now proven retrievable and checksum-verifiable through the research workflow without provider API calls. It can be rebuilt in the ephemeral runner; the original Run 8 v18 workbook and companion bundle themselves remain unrecovered.
- No raw archive, full feature ledger or row-level predictions were uploaded. Only the aggregate coverage artifact was retained.

## Next research action

Use the verified pinned archive to reconstruct the full 50-group event-time panel directly from raw JSON, preserving the explicit venue flag. Match the Run 8 24-hour history lag and the three existing folds: [2025-03-20, 2025-10-01), [2025-10-01, 2026-04-01), [2026-04-01, 2026-09-21). Require five observed overall matches for both teams, five explicit non-neutral home-role/away-role matches for venue features, and H2H N>=5. Then run the nested main-effects versus each interaction ablations and the joint BH/BY, paired-bootstrap and reliability analysis. Keep the V1.6 baseline explicitly blocked until its frozen fixture-level probability ledger is available.
