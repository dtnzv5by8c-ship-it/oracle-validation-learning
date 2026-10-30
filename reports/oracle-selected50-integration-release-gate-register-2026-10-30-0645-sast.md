# Project Oracle — Selected-50 Integration & Release-Gate Register

**Evidence cutoff:** 2026-10-30 07:36 SAST  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Branch head reviewed:** `c884c6237e27feaa0b282466d6287809c2cfe13a`  
**Decision:** Historical research baseline verified; production and betting release remain **NOT APPROVED**.

## Executive decision

The exact private archive `research-selected50-footystats-history-40447419806` remains the controlled historical research source. Runtime #171 consumed its exact SHA-256 and passed its output contract. New QA #36 adds reproducible xG/odds temporal-shift diagnostics; Safety Contract Tests #440 passed the new temporal-shift and H2H paired-output contract tests; Dry-Run Planner #727 passed its offline planner and readiness checks.

These are research/test passes only. They do not close identity, settlement, current-feed, point-in-time, calibration, market-value or team-suitability gates.

## Verified workflow evidence

| Evidence | Run / artifact | Result | Scope |
|---|---|---|---|
| Selected-50 runtime baseline | [#171](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41001723054), artifact `12954131277` | PASS | Exact 404474 archive consumed; runtime predates latest H2H paired-chronology additions |
| Private archive QA + temporal shift | [#36](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41008363529), artifact `12956506568` | PASS / REVIEW REQUIRED | Exact 404474 archive; 50 groups, 200 seasons, 59,049 rows; sanitized QA only |
| Safety contract tests | [#440](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41008369534), artifact `12955952884` | PASS | Includes xG/odds temporal-shift regression tests and H2H chronology/output-contract tests |
| Dry-run planner | [#727](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41008369517), artifact `12955524632` | PASS | Offline only; zero network and paid-provider calls; readiness gates remain blocked |

Run #171 archive provenance:
- Tag: `research-selected50-footystats-history-40447419806`
- SHA-256: `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`
- 66,452,206 bytes; 802 archive members.
- Snapshot overlay disabled; snapshot run ID `0`.
- Runtime: 50 groups, 200 seasons, 59,049 normalized records; 420 report-horizon candidates; 395 with at least one supported research prediction; 25 feature-blocked; 2,100 raw prediction rows across five markets.
- Production and betting eligibility false.

QA #36 independently confirms:
- 50/50 selected season IDs present; 200/200 season rows ingested.
- 22,291 records in the primary window (2025-03-20 to 2026-09-20); 22,256 provider-status `complete`; 35 non-complete rows with 0–0 score pairs.
- Across the archive, 7,066 non-complete rows carry 0–0 scores; 4,006 `complete` rows also carry 0–0.
- Provider status is not official settlement truth. The 0–0 patterns must not be promoted into labels without independent settlement reconciliation.

## Reconciled H2H evidence

Run #170 used the older 403752 archive; Run #171 used the intended 404474 archive. The paired H2H CSV and ablation JSON were byte-identical between those two runs, so #171 is a corrected archive-provenance baseline, not an H2H performance uplift.

Paired H2H population: 19,991 fixtures, 99,955 rows (five markets per fixture), 95.75% of the baseline test population. Candidate adds four H2H features to the same 20-feature baseline and uses the same paired train/test population.

| Market | Accuracy delta (H2H minus baseline) | Brier delta | Log-loss delta |
|---|---:|---:|---:|
| BTTS | +0.120 pp | -0.00011 | -0.00022 |
| DC Home | +0.095 pp | -0.00002 | +0.00007 |
| DC Away | -0.030 pp | -0.00006 | -0.00013 |
| Combo Home | -0.030 pp | +0.00003 | +0.00006 |
| Combo Away | +0.010 pp | +0.00011 | +0.00029 |

Across five expanding folds, DC Home accuracy improved 5/5 but Brier/log-loss improved only 3/5; BTTS improved 2/5 on all three metrics. Effects are small; no H2H candidate is approved.

New research-only changes add `h2h_last_date_utc`, an independent paired-output chronology audit, fail-closed QA, and stricter market/fold/training-population validation. The related contract tests passed in Safety Contract Tests #440. **A full Selected-50 runtime has not yet exercised these latest H2H artifact changes.** No production model includes these H2H candidate features.

## Data quality and temporal-shift findings

QA #36's new current-versus-noncurrent-season pooled xG comparison is a material warning:
- Team A prematch xG zeros: 201/545 (36.88%) current vs 202/4,527 (4.46%) historical; +32.42 pp.
- Team B prematch xG zeros: 203/545 (37.25%) vs 202/4,527 (4.46%); +32.79 pp.
- Total prematch xG zeros: 182/545 (33.39%) vs 181/4,527 (4.00%); +29.39 pp.
- Eleven current-season league groups cross the exploratory 30% zero-rate screen.

This supports a cross-league current-season data-quality/ingestion-regression hypothesis, but does not prove cause. The current-season sample is partial, historical seasons are pooled, and field semantics/source timestamps are absent. Numeric zero remains unchanged; do not impute it or infer provider fault.

Belgium Pro League 2026/27 sample:
- BTTS Yes/No and Double Chance 1X/X2 each share a 54/63 (85.71%) zero mask.
- Full-time 1X2 has only 1/63 zero; Over/Under 2.5 has no zeros.
- Double Chance 12 is a distinct market field and must not be used as a 1X/X2 proxy.
- This is market-specific archive-field evidence only; bookmaker identity and quote times are unverified.

The 40-day gap between the 20 September event-window end and 30 October audit date is an event-time coverage gap, **not** a provider freshness timestamp.

## Team / league DNA reconciliation

The latest available Team & Market Exposure analysis is an exposure map, not a validated team-performance study:
- 779 provider team IDs; 859 team-role profiles; 1,718 team/market exposure records.
- 47 league groups and 41 countries represented in the current fixture horizon.
- Recent-form sample: 833 profiles with five matches, 21 with four, five with three; 26 profiles below five matches.
- 50 profiles had at least one incomplete-feature appearance.
- The exposure counts are not team-market accuracy or betting edge. There is no immutable, canonical team-attributed prediction-to-official-settlement ledger, so no team ranking or exclusion decision is justified.

## Current Selected-50 readiness and blockers

Latest dry-run #727 confirms a research-only pass, not current operational readiness:
- Legacy Run 56 / crosswalk r17 evidence still appears in some planner outputs: 31 exact selected-season manifest matches and 19 without a record in that old snapshot. This is not evidence that 19 folders are absent from the latest 404474 archive; QA #36 confirms 50/50 archive season folders.
- The planner's current-feed identity quarantine shows 22 candidate mappings requiring human review and 28 unresolved; 0 approved.
- 5 current-feed groups have multiple league-ID collisions; 7 have a single display-label ID; 38 have no matching label rows. Country is not retained in the feed identity layer.
- 0 canonical team joins, 0 canonical fixture joins, 0 verified parent competition IDs, 0 official settlement truth, 0 point-in-time xG/odds provenance.
- Current schedule evidence remains stale: last fixture date 2026-10-17; manifest window ends 2026-10-22; 0 governed current fixture rows emitted.
- BTTS and Double Chance remain NOT VERIFIED; Combo remains blocked by target/settlement mismatch; M-1UP remains blocked by stale event truth.
- Calibration and odds/ROI benchmarking remain unapproved because labels, as-of features and bookmaker quote timestamps are not verified.

Do not merge counts from Run 56/r17 with the 404474 200-season archive as though they were the same identity population. Preserve the legacy evidence labels until the planner is rebuilt against the pinned 404474 QA manifest.

## Release-gate register

| Gate | Status | Required closure evidence |
|---|---|---|
| 404474 archive integrity and runtime provenance | **PASS — research baseline only** | Preserve pinned tag/hash and artifact provenance |
| Research runtime contract | **PASS — Run #171 only** | Re-run on latest branch to exercise new H2H output contract |
| H2H chronology/output contract | **TESTS PASS; runtime pending** | Full runtime artifact with last-H2H timestamp and fail-closed chronology QA |
| Selected-50 canonical competition identity | **BLOCKED** | Authoritative parent competition mapping; no inference from season IDs |
| Canonical team and fixture joins | **BLOCKED — 0 verified** | Exact league-aware IDs, collision quarantine, source evidence and human sign-off |
| Official settlement truth | **BLOCKED — 0 verified** | Independent final status/result reconciliation per canonical fixture |
| Current fixture freshness | **BLOCKED** | Fresh snapshot, source manifest and exact Selected-50 bridge |
| Point-in-time xG/odds/standings | **BLOCKED — 0 verified** | Field semantics, source/update/quote timestamps and as-of-kickoff evidence |
| BTTS / Double Chance readiness | **NOT VERIFIED** | Identity, settlement, freshness, PIT provenance, calibration and market evaluation |
| Combo | **BLOCKED** | Authoritative market definition; align prediction target and settlement contract |
| M-1UP | **BLOCKED** | Fresh chronological goal-event truth and exact fixture joins |
| Team-market suitability / exclusions | **BLOCKED** | Immutable canonical team/fixture prediction ledger plus official settlements and minimum-sample uncertainty controls |
| Calibration / bookmaker value / ROI | **BLOCKED** | Separate chronological calibration design and timestamped odds with vig-aware evaluation |
| Production governance | **PRESERVED** | No production changes; all release gates and explicit approval required |

## PR #31 — identity resolver

[PR #31](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/31) remains **draft** and not mergeable. Its FootyStats-first resolver/adapter is research-only and reports 12 local smoke tests in the PR description; that is not a GitHub CI pass. The dedicated workflow `oracle_identity_resolver_tests.yml` exists with `workflow_dispatch`, but no completed run for that workflow was found in the reviewed Actions history. The resolver may create candidates; it does not approve canonical mappings and does not satisfy the protected production FotMob/event-truth contract.

## Safe research-only improvements

1. Refresh the planner's legacy Run 56/r17 identity/readiness evidence from the pinned 404474 QA artifact, or explicitly quarantine it as historical. Add a regression that fails if a superseded snapshot is labelled current.
2. Execute dedicated identity-resolver CI and preserve its actual artifact/test result before accepting PR #31 as a research integration.
3. Run the Selected-50 runtime once on the current branch to exercise the newly added H2H last-date and chronology artifact contract.
4. Keep team-market analysis exposure-only until canonical prediction/settlement pairs and point-in-time features exist.

No provider/API calls or credits were used in these checks. No raw provider payload was exported. No production logic, frozen probabilities, calibration, thresholds, registry or governance were changed.

## Single highest-value next action

**Manually dispatch “Oracle Identity & Settlement Evidence Tests” on branch `research/oracle-50-league-readiness-audit`.** Open [the workflow](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/.github/workflows/oracle_identity_resolver_tests.yml), select the research branch and tap **Run workflow**. It has no required inputs. This is an offline test workflow; it makes no provider/API calls. The available GitHub connection can inspect runs and artifacts but cannot dispatch Actions, so Nolan must perform this one manual click. If it passes, use the tested resolver to produce a fresh 50-row candidate register, retaining every mapping as `NOT_APPROVED` pending authoritative evidence and human review.
