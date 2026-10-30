# Project Oracle — Selected-50 Integration & Release-Gate Register

**Evidence cutoff:** 2026-10-30 12:37 SAST  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Reviewed branch head:** `460e7eca2e20ca38d122df77b3d1861cfc49f485`  
**Decision:** Continue research-only validation. Production and betting eligibility remain **NOT APPROVED**.

## Executive decision

The highest-value action is already underway: Selected-50 full historical Runtime #173 was manually dispatched at 12:35:40 SAST against commit `460e7eca2e20ca38d122df77b3d1861cfc49f485`.

At the evidence cutoff, the run is **IN PROGRESS**. Archive-access guard, private archive download/verification, archive selection, dependency installation, snapshot-disabled contract, composite-market contract, feature/training diagnostics, H2H feature/chronology contracts, paired-H2H output contracts, and input fingerprinting have passed. Snapshot overlay was skipped as intended. The full runtime builder is still running; final validation, provenance receipt, and artifact upload have not completed. No artifacts are yet listed. Do not dispatch a duplicate runtime.

Run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41041882618

## New evidence integrated

### 1. H2H paired-output validation

Research commits:
- `214945213a8ef9073b99322d85c911584621ee57` — reconcile the full chronology QA summary to the paired CSV.
- `246b0e7f114e7514f1caf042050a6783a36be8cf` — add focused regression tests for counter, market-set, per-market count, composite-fixture count, and boolean-as-integer failures.

The strengthened validator now requires:
- Exact integer row count equal to paired CSV rows.
- Exact composite `(competition_id, fixture_id)` fixture count.
- Exactly the governed five-market set.
- Per-market row counts independently matching the CSV.
- All 17 chronology failure counters present as integer zero values; booleans and missing counters fail closed.
- Explicit `production_eligible=false` and `betting_eligible=false`.

Safety Contract Tests #479 passed on commit `4b6f84e0a87f04b5b04ad9a5a052d3438036297d`; its H2H chronology and paired-output contract steps passed. The earlier focused Safety #476 also passed on the combined H2H validator/test commit. These are synthetic contract tests, not a new full-runtime result.

- Safety #479: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41039620525
- Safety #476: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41037623060

No new H2H accuracy, Brier, log-loss, AUC, significance, or fold-performance result is claimed until Runtime #173 uploads and validates its outputs.

### 2. Data quality and archive lineage

Safety #479 artifact `oracle-selected50-200-season-ingestion-audit.zip` was downloaded and inspected. Downloaded ZIP SHA-256 matches GitHub's artifact digest:

`02bd5cab4f171827b1559b03fe29f987249a6ef96a8d2c54bf10d94c388c115b`

Its sanitized ledger reports:
- 50 selected season groups.
- 200 historical season rows; 200 ingested, zero failed.
- 59,049 match rows.
- 3,366 team-season memberships (not unique canonical clubs).
- 50/50 selected season-ID matches.
- Zero parent competition IDs exposed.
- Historical source ingestion run `40375285207` used 57 provider requests; this audit itself made zero provider calls.

This artifact belongs to the **403752** lineage, SHA-256 `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`. It is not the pinned **404474** runtime archive. Do not infer equivalence from matching row counts.

The 404474 archive remains the runtime's pinned input, SHA-256 `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`. Runtime #173's private archive verification step has passed; its final runtime provenance artifact is still pending.

The earlier xG zero-rate comparison remains exploratory and unchanged: across 48 represented groups, current versus historical zero rates were 13.26% vs 3.54% for Team A prematch xG, 13.30% vs 3.52% for Team B, and 11.91% vs 3.16% for total prematch xG. No new field-level source timestamps or authoritative zero semantics were added by #479. The Belgium BTTS/DC odds gaps remain unverified for point-in-time use.

### 3. Team DNA provenance and integrity

Commits `37969d1139270159e440f344e64d55b13232107f`, `f04473e180d83b2df5bac1480c6d12da12447546`, `4b6f84e0a87f04b5b04ad9a5a052d3438036297d`, `5731fbfefad883dbb4665279d7881ed32f256a51`, and `460e7eca2e20ca38d122df77b3d1861cfc49f485` improve research-only label provenance and reproducibility:
- OOS targets are explicitly labelled score-derived research labels, not official bookmaker settlement truth.
- The ambiguous candidate-discordance field is now `exploratory_discordance_flag`, explicitly `EXPLORATORY_ONLY_NOT_SETTLEMENT_VALIDATED`.
- Team, chronological and league outputs carry label provenance and `official_settlement_verified=false`.
- Summary records zero official settlement rows.
- Run metadata captures SHA-256 hashes and row counts for the pinned OOS predictions and canonical match spine.
- A metadata CSV is included in the manual audit's sanitized artifact contract.

Team DNA OOS Integrity Tests #3 passed six synthetic tests on commit `f04473e...`; this validates the builder and output contract only. The separate read-only source audit workflow `.github/workflows/oracle-team-dna-oos-integrity-audit.yml` has not produced a source-data artifact in the reviewed run set. Its source audit remains a separate research lane; this integration pass did not dispatch it or duplicate that work.

Existing 27-league OOS research signals remain exploratory: DC Home Brier improvement +0.002112, DC Away +0.002131, Combo Home +0.000744; BTTS and Combo Away intervals include zero. The intervals are not clustered by team/league/time. M1UP has only 58 post-warm-up observations in one fold. The team inventory reports 651 profiles (median 48 fixtures; 169 below 30; 73 below 8), but the older 562-versus-651 metadata discrepancy still needs reconciliation. The M1UP export's match-only many-to-many join remains invalid for venue attribution.

### 4. Selected-50 readiness and blocker evidence

Dry-Run Planner #758 passed on commit `4b6f84e...`; its artifact was downloaded and inspected. ZIP SHA-256 matches GitHub's digest:

`5f751c849d6149006d32e483c8f5cee523634d3e7029e5ad8e88e007da6fe`

The artifact confirms a fail-closed readiness state:
- 22 crosswalk candidates require human review; 28 are unresolved.
- Zero approved mappings, canonical team joins, canonical fixture joins, parent competition IDs, official settlement rows, or point-in-time xG/odds provenance.
- Current-feed label rows exist for 12 groups; five have multiple league-ID collisions; 38 have no matching label rows; no provider-season-to-feed bridge is verified.
- Zero current governed fixture rows. Schedule evidence is stale: last fixture date 2026-10-17; manifest window ends 2026-10-22; audit date 2026-10-30.
- The 31/19 split is a legacy Run-56/crosswalk snapshot, not current archive folder coverage.
- The 14,051-row private QA snapshot is explicitly superseded by the later 200-season ingestion evidence.
- Network calls and paid provider calls in the dry run: zero.

Market gates:
- BTTS and Double Chance: blocked by identity, settlement, freshness and point-in-time provenance.
- Combo: blocked by target/settlement mismatch. The predictor uses Double Chance AND 2–4 total goals; the documented ledger uses Double Chance AND fewer than five total goals. Do not infer or alter the official market definition.
- M1UP: blocked by stale event truth.

## Concise release-gate register

| Gate | Status | Evidence / closure condition |
|---|---|---|
| 50 selected season groups / 200-season 403752 ledger | PASS — lineage-specific | Safety #479 artifact; not interchangeable with 404474 |
| Pinned 404474 archive verification in current runtime | PASS — preflight only | Runtime #173 archive verification step passed; final provenance receipt pending |
| H2H chronology and paired-output synthetic contracts | PASS | Safety #476/#479; full runtime output validation pending |
| Full Selected-50 runtime on corrected code | IN PROGRESS | Runtime #173; wait for builder, validator and artifacts |
| Parent competition identity | BLOCKED | 0 verified; provider schema/identity evidence required |
| Canonical team/fixture joins | BLOCKED | 0 verified; evidence-backed mapping and human approval required |
| Official settlement truth | BLOCKED | 0 verified; authoritative result/status reconciliation required |
| xG/odds point-in-time provenance | BLOCKED | Field semantics and immutable as-of timestamps absent |
| Current governed fixture slate | BLOCKED | Stale schedule; zero rows emitted |
| Team-market suitability | BLOCKED | Score-derived labels only; settlement and team-level OOS joins absent |
| Combo definition | BLOCKED | Predictor/ledger disagreement requires authoritative market definition |
| M1UP event truth | BLOCKED | Fresh event-level settlement evidence absent |
| Calibration and bookmaker value | BLOCKED | No calibration approval or provenance-valid odds/ROI benchmark |
| Production and betting governance | NOT APPROVED | Preserve all current release gates |

## Safe research-only improvements identified

1. Keep the H2H validator's complete summary-to-CSV reconciliation and fail-closed integer/type checks.
2. Preserve Team DNA label provenance, source hashes, row counts and explicit non-settlement classification in every downstream artifact.
3. Add an explicit lineage key to every Selected-50 report (archive tag, source run/artifact, SHA-256, code commit, scope and generated timestamp) so 403752, 404474, Run-56 and pre-batch-5 snapshots cannot be conflated.
4. Keep current-feed identity quarantine, schedule freshness and Combo settlement diagnostics as separate gates; do not promote display-label matches into canonical joins.
5. Avoid another duplicate safety/dry-run run unless new code or evidence changes.

## Single highest-value next action

**Wait for Selected-50 Runtime #173 to finish and inspect its final job logs and uploaded artifacts.** It is already running on the latest reviewed branch head; do not dispatch another runtime or any duplicate diagnostics.

Required completion evidence:
- 404474 archive SHA-256 receipt.
- Valid single-document H2H chronology QA JSON.
- Paired CSV and exact chronology-summary reconciliation.
- Five-market metric and discordance outputs.
- Five chronological folds.
- Runtime provenance receipt and sanitized artifact upload.
- Production and betting eligibility explicitly false.

If #173 fails, diagnose the exact failing step and artifact before any rerun. No further manual action is required from Nolan while this run is active.

## Governance

No provider/API calls or credits were used in this integration pass. The 57 requests cited above belong to the historical 403752 source ingestion run, not this audit. No production model logic, frozen probabilities, calibration, thresholds, or governance were changed. All research remains isolated to the research branch. Production and betting eligibility remain **NOT APPROVED**.
