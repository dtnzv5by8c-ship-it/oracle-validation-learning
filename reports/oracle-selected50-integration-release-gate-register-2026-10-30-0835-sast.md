# Project Oracle — Selected-50 Integration & Release-Gate Register

**Evidence cutoff:** 2026-10-30 08:35 SAST  
**Research branch:** research/oracle-50-league-readiness-audit  
**Branch head reviewed before this register commit:** 22e7f522b8c337f02108413bba0b126a70c87e96  
**Decision:** Research baseline and offline QA strengthened; production and betting release remain **NOT APPROVED**.

## Executive decision

Keep Selected-50 Runtime #171 as the controlled historical runtime baseline for the pinned 404474 archive. Newer H2H output-contract tests and cross-scope xG/odds research checks passed their respective GitHub workflows. Private Archive QA #38 was downloaded and its ZIP SHA-256 independently matched the GitHub artifact digest.

The xG temporal-shift result must be reported in two separate populations:
- **All 48 selected groups with current-season xG QA rows:** current prematch-xG zero rates are 11.91%–13.30%, versus 3.16%–3.54% in non-current seasons.
- **The 11 threshold-selected outlier groups only:** current rates are 33.39%–37.25%. This is a selected subset, not a 50-league universe estimate.

No new provider/API calls or credits were used. No production model, frozen probabilities, calibration, thresholds or governance were changed.

## 1. Latest verified GitHub evidence

| Workstream | Run | Artifact | Result and scope |
|---|---:|---:|---|
| Selected-50 full runtime baseline | [#171](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41001723054) | 12954131277 | PASS; exact 404474 archive consumed. Predates latest paired-H2H validator changes. |
| H2H paired correctness / discordance contracts | [Safety #442](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41012430578) | 12957668040 | PASS; paired chronology and output-contract step passed, including correctness flags and exact McNemar checks. |
| H2H metric-to-CSV reconciliation | [Safety #443](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41012649069) | 12957679462 | PASS; accuracy, Brier, log loss, AUC, correctness flags and discordance are reconciled. |
| xG/odds cross-scope QA | [Private Archive QA #38](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41014563323) | 12959146668 | PASS / REVIEW REQUIRED; pinned 404474 archive and sanitized QA. Downloaded ZIP SHA-256 matched GitHub digest ca300da9ed7f887786f3b98203f7fd4352ae33ad53cae75d56dca827885148f9. |
| xG/odds cross-scope safety tests | [Safety #444](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41014563362) | 12958099719 | PASS; cross-scope regression-test step passed. Its attached ingestion rollup references legacy source 40375285207 / SHA 7c60…, not the 404474 QA source. |
| Selected-50 dry-run/readiness | [Dry-Run #731](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41014563326) | 12958643997 | PASS; offline planner and readiness contracts passed. Downloaded ZIP SHA-256 matched GitHub digest a119719838f22e600a1d6af5acd092fc2ed0167b064c6c46ff0637090ebef918. Its identity-evidence layer still contains superseded snapshots. |

Recent research-only commits:
- [918549c — paired H2H correctness discordance validation](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/918549ca77493e906b071e1940aff73fe7081203)
- [64f1b86 — paired H2H metric reconciliation](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/64f1b869edef341f2300aed2ce0d16a6707bb979)
- [cba6c3b — xG temporal-shift population-scope correction](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/cba6c3b89fbfb849446e9a3450e002d63e95cef5)
- [560c0bf — selected-50 xG/odds cross-scope reconciliation](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/560c0bfe89b00667175d8a1c262f7326e18be8ea)
- [22e7f52 — post-commit CI and QA checkpoint](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/22e7f522b8c337f02108413bba0b126a70c87e96)

## 2. Pinned archive and historical coverage

Controlled archive: research-selected50-footystats-history-40447419806  
SHA-256: af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875

- Selected season folders: 50/50.
- Historical season rows: 200/200 ingested.
- Archive match records: 59,049.
- Primary validation window: 2025-03-20 through 2026-09-20.
- Primary-window records: 22,291; 22,256 have provider status complete; 35 non-complete rows carry 0-0 score pairs.
- Across the full archive, 7,066 non-complete-status rows carry 0-0 scores; 4,006 rows marked complete also carry 0-0.

Provider status and score presence are not official settlement truth. The 50 selected group labels and provider season IDs are not canonical Oracle competition, fixture or team identities.

## 3. H2H evidence reconciliation

The paired H2H holdout remains 19,991 fixtures / 99,955 fixture-market rows, five markets per fixture, with 95.75% coverage of the 20,878 baseline test population. Baseline and candidate used the same 18,913 H2H-eligible training rows.

| Market | Accuracy delta (H2H minus baseline) | Exact paired McNemar p-value |
|---|---:|---:|
| BTTS | +0.120 pp | 0.527651 |
| Double Chance Home | +0.095 pp | 0.095673 |
| Double Chance Away | -0.030 pp | 0.755653 |
| Combo Home | -0.030 pp | 0.824126 |
| Combo Away | +0.010 pp | 0.904975 |

No market reaches an unadjusted 0.05 threshold. DC Home is closest, but evidence is not statistically conclusive for threshold correctness. These p-values are unadjusted and do not test calibration, probability superiority, bookmaker value or ROI.

The validator now recomputes accuracy, Brier score, log loss and AUC from paired CSV rows and reconciles published metrics and correctness flags. It also validates discordance counts and exact McNemar values. These are output-integrity improvements only.

**Outstanding:** the latest H2H changes have passed offline contract CI, but no full Selected-50 runtime has emitted and validated the new h2h_last_date_utc, paired chronology summary, metric-reconciliation summary and discordance summary together from the pinned archive. Runtime #171 remains the last full runtime baseline and predates these changes. Do not promote the H2H candidate.

## 4. Data-quality and xG/odds reconciliation

Private Archive QA #38 regenerated corrected cross-scope diagnostics from the pinned 404474 archive.

### All represented current-season groups

48 of the 50 selected groups have current-season xG QA rows; Australia A-League (season 17326) and India Indian Super League (season 17964) have no primary-window rows in this analysis.

| Prematch xG field | Current: 48 groups | Non-current: 78 season scopes | Change |
|---|---:|---:|---:|
| Team A | 747/5,633 = 13.26% | 577/16,318 = 3.54% | +9.72 pp |
| Team B | 749/5,633 = 13.30% | 575/16,318 = 3.52% | +9.78 pp |
| Total | 671/5,633 = 11.91% | 516/16,318 = 3.16% | +8.75 pp |

### Threshold-selected subset — not a universe estimate

Eleven groups crossed the exploratory >=30% current-season zero-rate screen:
- Team A: 201/545 (36.88%) versus 202/4,527 (4.46%) historical.
- Team B: 203/545 (37.25%) versus 202/4,527 (4.46%) historical.
- Total: 182/545 (33.39%) versus 181/4,527 (4.00%) historical.

Across the 48 represented groups, prematch-zero/postmatch-positive co-occurrence is 744/747 (99.60%) for Team A, 746/749 (99.60%) for Team B and 670/671 (99.85%) for total xG. These are field-pair observations, not unique fixtures or proof of provider semantics. They make unavailable/sentinel values a strong hypothesis, but do not justify recoding. Keep numeric zero unchanged until source semantics and timestamps are established.

### Odds-specific findings

- Belgium Pro League 2026/27: BTTS Yes/No and Double Chance 1X/X2 share an identical 54/63 zero mask (85.71%); DC 12 is zero on 63/63 rows; each full-time 1X2 field has one zero; Over/Under 2.5 has no zeros.
- Four half-specific BTTS odds fields are zero across all 59,049 archive rows.
- Current-scope DC 12, DNB and first-goal fields are overwhelmingly zero; these are distinct markets and must not be used as substitutes for DC 1X/X2 or other markets.
- Bookmaker/source IDs, quote timestamps and per-field retrieval/update timestamps are unavailable.

The 40-day difference between the 20 September event-window end and 30 October audit date is an event-time coverage gap only, not a provider freshness measurement. Keep affected fields flagged for provenance review; do not exclude entire leagues or teams from descriptive zero rates.

## 5. Team and league DNA

The latest available Team & Market Exposure map remains exposure-only:
- 779 provider team IDs; 859 team-role profiles; 1,718 team/market exposure records.
- 47 league groups and 41 countries represented in the current fixture horizon.
- 833 profiles with five recent matches; 21 with four; five with three; 26 below five matches.
- 50 profiles have at least one incomplete-feature appearance.

There is still no immutable, canonical team-attributed pre-kickoff prediction ledger joined to independently verified official settlements. These counts do not measure team-market accuracy or betting edge. Do not label teams as traps or exclude teams from raw exposure/form rates.

## 6. Selected-50 readiness and stale evidence reconciliation

Dry-Run #731 passed its offline checks, but its evidence layers are not all current:
- Its archive-evidence reconciliation retains the legacy Run 56 / crosswalk r17 split: 31 exact manifest matches and 19 without a row in that older manifest. This is not evidence that 19 selected folders are absent from the 404474 archive; QA #38 verifies 50/50 selected folders and 200/200 seasons.
- The dry-run's separate 14,051-row QA matrix is explicitly marked pre-batch-5 and superseded. Do not quote its 14,051 rows, status counts or 31/19 split as current 404474 archive coverage.
- Current-feed identity quarantine: 22 candidate mappings require human review, 28 are unresolved, zero approved. Five groups have multiple feed league-ID collisions; seven have one display-label ID; 38 have no matching label rows. Country is not retained in that feed identity layer.
- Canonical parent competition IDs: 0 verified; canonical team joins: 0; canonical fixture joins: 0; official settlement truth: 0; point-in-time xG/odds/standings provenance: 0.
- Current schedule evidence remains stale: last fixture date 2026-10-17; schedule manifest ends 2026-10-22; 0 governed current fixture rows and 0 prediction rows emitted.
- BTTS and Double Chance remain NOT VERIFIED; Combo is blocked by target/settlement mismatch; M-1UP is blocked by stale event truth.

Combo mismatch diagnostic enumerates two disagreement scorelines per side: Home (0-0, 1-0) and Away (0-0, 0-1), comparing predictor Double Chance AND 2-4 goals with documented ledger Double Chance AND fewer than five goals. This is a logic discrepancy, not an official bookmaker definition. Keep Combo masked until the authoritative settlement rule is confirmed.

## 7. Concise release-gate register

| Gate | Status | Closure evidence required |
|---|---|---|
| 404474 archive integrity and provenance | **PASS — research baseline only** | Preserve exact tag/hash and artifact provenance |
| 50 selected season folders / 200 seasons | **PASS — archive QA only** | Do not equate season IDs with canonical competitions |
| H2H paired chronology/metric/discordance tests | **PASS — offline tests** | Full runtime must emit and pass the new artifact contracts |
| Full runtime on latest research head | **PENDING** | Manual historical runtime on pinned 404474 archive |
| Identity resolver CI | **PENDING** | Dedicated workflow run and actual test artifact |
| Canonical parent competition identity | **BLOCKED — 0 verified** | Authoritative parent-ID evidence; never infer from season IDs |
| Canonical team and fixture joins | **BLOCKED — 0 verified** | Exact league-aware source IDs, collision quarantine, evidence and human sign-off |
| Official settlement truth | **BLOCKED — 0 verified** | Independent final status/result reconciliation for each canonical fixture |
| Current fixture freshness | **BLOCKED** | Fresh schedule snapshot, manifest and exact Selected-50 bridge |
| Point-in-time xG / odds / standings | **BLOCKED — 0 verified** | Field semantics, source/retrieval/quote timestamps and as-of-kickoff proof |
| BTTS / Double Chance | **NOT VERIFIED** | Identity, settlement, freshness, PIT provenance, calibration and market evaluation |
| Combo | **BLOCKED** | Authoritative definition and aligned predictor/settlement labels |
| M-1UP | **BLOCKED** | Fresh chronological goal-event truth and exact fixture joins |
| Team-market suitability / exclusions | **BLOCKED** | Immutable canonical team/fixture prediction ledger plus official settlements and sample/uncertainty controls |
| Calibration / bookmaker value / ROI | **BLOCKED** | Chronological calibration and timestamped odds with vig-aware evaluation |
| Production governance | **PRESERVED** | No production changes; formal release gates and explicit approval |

## 8. Safe research-only improvements

1. Make the dry-run planner consume a pinned 404474 QA manifest/artifact for current archive coverage, while retaining Run 56/r17 only as explicitly historical evidence. Add a regression that fails if the superseded 14,051-row snapshot is labelled current.
2. Execute the dedicated identity-resolver workflow before accepting PR #31's resolver as CI-validated. Keep all mappings unapproved pending source evidence and human review.
3. After identity CI, dispatch one full historical runtime on the latest branch to exercise the new H2H last-date, metric-reconciliation and discordance artifact contracts.
4. Review existing archive-owner documentation or stored ingestion metadata for xG semantics, odds source IDs and timestamps. If unavailable, record a manual dependency; do not call providers or incur credits.

No production code, model logic, frozen probabilities, calibration, thresholds, registry or governance were changed. No provider/API calls or credits were used.

## 9. Single highest-value next action

**Manually dispatch Oracle Identity & Settlement Evidence Tests on branch research/oracle-50-league-readiness-audit.**

Workflow: [Oracle Identity & Settlement Evidence Tests](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/.github/workflows/oracle_identity_resolver_tests.yml)

- Branch: research/oracle-50-league-readiness-audit
- Inputs: none
- Action: **Run workflow**

No matching identity-workflow run was found in the 100 most recent Actions runs reviewed. The available GitHub connection can inspect commits, runs and artifacts but cannot dispatch GitHub Actions. This one manual click is therefore required. If it passes, generate a fresh 50-row identity candidate register with evidence and collision diagnostics; every candidate remains NOT_APPROVED until authoritative identity evidence and human review exist.

**Final decision:** continue research only. Production eligibility and betting eligibility remain **NOT APPROVED**.