# Project Oracle — Market Intelligence Signal Discovery Run 5: Archive Rebuild Preflight

**Date:** 2 November 2026 (SAST)  
**Branch:** \`research/oracle-50-league-readiness-audit\`  
**Inspected live branch HEAD before this change:** \`038ca1b3bb44de994c93a3a2911a34af052417a8\`  
**Previous checkpoint commit:** \`038ca1b3bb44de994c93a3a2911a34af052417a8\`  
**Scope:** Run 8 binary recovery and raw venue-flag preflight. Research-only.

## Work completed

- Reconfirmed that the Run 8 v18 workbook and companion bundle are absent from the Library and repository tree. The committed manifest provides names, sizes and checksums only.
- Confirmed the pinned archive release: tag \`research-selected50-footystats-history-20261025\`, asset ID \`675196963\`, 66,416,916 bytes, declared SHA-256 \`bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261\`.
- Added a separate research-only GitHub Actions workflow that reads only this exact private release asset, verifies its checksum, and performs an aggregate raw \`no_home_away\` coverage audit. It does not call FootyStats or another provider.
- Added a tri-state parser: explicit \`1/true/yes\` = neutral; explicit \`0/false/no\` = non-neutral; missing/blank = unknown; other values = invalid. Only explicit non-neutral rows can qualify for venue histories.
- Added synthetic contract tests to ensure missing/unknown venue flags are never silently counted as non-neutral.
- The workflow uploads aggregate group/season coverage and a summary only. It does not upload the archive, raw provider rows, row-level features or fixture predictions.

## Key technical finding

The existing \`scripts/build_footystats_archive_features.py\` collapses a missing \`no_home_away\` field to integer zero. That behaviour is not safe for venue-specific history gates. The new preflight reads the raw archive field directly and preserves unknown values. The existing builder was not modified.

## Existing completed analysis not repeated

Run 3 already tested both candidate interactions as nested ablations on the 31-group Run64 reconstruction and found no constituent-controlled incremental value. This run does not repeat those tests. The full 50-group Run 8 experiment remains blocked until the exact pinned archive is materialised and venue-flag coverage is verified.

## Workflow and outputs

- Workflow: \`.github/workflows/oracle-run8-pinned-archive-venue-flag-preflight.yml\`
- Script: \`scripts/audit_run8_pinned_archive_venue_flag_coverage.py\`
- Tests: \`tests/test_run8_pinned_archive_venue_flag_coverage.py\`
- Expected archive checksum: \`bc64fbad2f827dac983ae8ef1de5055be34209693b7b8057f4c00508059e7261\`
- Artifact name: \`oracle-run8-pinned-archive-venue-flag-preflight\` (aggregate outputs only; three-day retention).

The workflow was added in this commit and should run on the research-branch push. Its execution result and archive retrieval are not claimed until the Actions run completes.

## Remaining blockers and next steps

1. Inspect the workflow run. If the private token, release access or checksum fails, record the exact failure and stop; do not substitute another archive.
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
- \`production_eligible=false\`; \`betting_eligible=false\`.
