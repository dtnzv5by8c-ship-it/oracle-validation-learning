# Project Oracle — Selected-50 Integration & Release-Gate Register

**Evidence cutoff:** 2026-10-30 09:42 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Branch head:** `19bd070850a716831b917625e5393332ae79e25e`  
**Decision:** Research-only progress accepted; production and betting release remain **NOT APPROVED**.

## Executive decision

Keep Selected-50 Runtime #171 as the pinned historical baseline for archive `research-selected50-footystats-history-40447419806` (SHA-256 `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`). The latest H2H chronology/metric safeguards and xG/team-sample audit tests now pass CI, but the full runtime has not yet emitted their integrated artifacts. Identity & Settlement Evidence Tests #16 also passed; that closes the dedicated workflow execution gap, not the identity/settlement release gates.

No provider/API calls or credits were used in this review. No production logic, frozen probabilities, calibration, thresholds or governance were changed.

## 1. Latest verified workflow evidence

Artifacts were downloaded and their ZIP SHA-256 values matched GitHub's artifact digests.

| Workflow | Run | Artifact | Result and scope |
|---|---:|---:|---|
| Private Archive QA | [#39](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41020449195) | 12961830346 | PASS / review required; pinned 404474 archive; event-time/status and xG/odds QA. ZIP SHA-256: `0e45ecbe1dcbfe2785e216a07e0987c52edc7a9c5624f85effec41d29afbdeb7`. |
| Dry-Run Planner | [#739](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41021753992) | 12962315125 | PASS; offline readiness only; 0 network/paid-provider calls. ZIP SHA-256: `09ca886f2f52ca900bb0b8c21eff0fdf90fe182b59bf7d22e6fca51e018df528`. |
| Safety Contract Tests | [#456](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41021831699) | 12961946131 | PASS; H2H chronology/output contracts, xG heterogeneity/team-sample tests and existing research safety suites passed. ZIP SHA-256: `0de94b339b6987ff2b5a8e4718fb8156171f920ef7f37f6474518c4c0c246829`. |
| Identity & Settlement Evidence Tests | [#16](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41016581498) | 12959703263 | PASS on commit `85a1618`; dedicated identity/settlement workflow and artifact verified. ZIP SHA-256: `1a71910962813c15c62fa2f6eb8ef7c707b13b113aa91ef97f2716ef23d30a8d`. |
| Selected-50 full runtime | [#171](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41001723054) | 12954131277 | PASS; exact 404474 archive consumed. This remains the last full runtime and predates the newest H2H artifact-contract changes. |

Safety #456 ran on parent commit `2c14dc2`; current branch head `19bd070` adds a documentation/checkpoint update after that test run. The latest dry-run #739 is on `ab11b03`. Do not interpret these as a full runtime on current head.

## 2. H2H reconciliation

Run #171 remains the controlled baseline: 19,991 paired fixtures, 99,955 rows across five markets, and zero reported internal strict-cutoff violations. Its paired CSV does not expose `h2h_last_date_utc`, so independent reconstruction of elapsed H2H days from that file is incomplete.

Research-only fixes now:
- emit the actual prior H2H meeting date and independently audit strict pre-kickoff chronology;
- reject timezone-naive timestamps instead of silently treating them as UTC;
- scope paired uniqueness by `(competition_id, fixture_id, market)`;
- reconcile accuracy, Brier, log loss, AUC, correctness flags, discordance counts and exact paired McNemar results.

The latest Safety #456 passed the H2H test steps, including the new safeguards. The full Selected-50 runtime has **not** yet exercised the new paired CSV and chronology/metric/discordance artifacts together.

Paired holdout effects remain small: BTTS +0.120 pp accuracy; DC Home +0.095 pp; DC Away -0.030 pp; Combo Home -0.030 pp; Combo Away +0.010 pp. No exact paired McNemar p-value is below 0.05 (DC Home is closest at 0.095673). No H2H candidate is approved for promotion; these tests establish output integrity, not betting value.

## 3. Data quality and event-time findings

QA #39 confirms the pinned archive has 50/50 selected current-season folders, 200/200 ingested season rows, 59,049 match records and 3,366 season-scoped team records.

The locked primary event window (2025-03-20 to 2026-09-20) contains 22,291 rows: 22,256 provider-status complete, 24 canceled, 6 incomplete and 5 suspended. Two current seasons have no rows inside this window because they start later: Australia A-League (season 17326; 16 Oct 2026 start) and India Indian Super League (season 17964; 10 Oct 2026 start). They are future-only relative to the historical window, not missing archive groups.

Status/score safeguards:
- 116 incomplete-status records have past kickoff dates (112 current-season, 4 historical): manual reconciliation queue only.
- All 7,066 non-complete records with parseable score pairs are 0-0; the 35 such rows in the primary window are also 0-0. Do not settle these placeholders.
- 4,006 provider-complete records are also 0-0; a 0-0 score on a complete row is not automatically invalid, but still is not independent official settlement truth.
- The 40-day difference between audit date and primary-window end is an event-time coverage gap, not provider retrieval lag. No source retrieval/update timestamps, bookmaker IDs or quote timestamps are available.

### xG heterogeneity

For the 48 league groups with current-season xG QA rows (not all 50), current vs pooled non-current zero rates are:

| Prematch xG | Current | Non-current | Difference |
|---|---:|---:|---:|
| Team A | 13.26% | 3.54% | +9.72 pp |
| Team B | 13.30% | 3.52% | +9.78 pp |
| Total | 11.91% | 3.16% | +8.75 pp |

All 48 groups have a positive current-vs-noncurrent direction for each field, including after descriptive Jeffreys shrinkage. League-cluster bootstrap mean-delta 95% intervals are +14.31 to +20.85 pp (Team A), +14.39 to +20.95 pp (Team B), and +12.86 to +19.13 pp (total). The 11 threshold-selected outlier groups have higher rates (36.88%, 37.25%, 33.39% respectively); that subset is not a 50-league estimate. Prematch-zero/postmatch-positive co-occurrence is approximately 99.6%–99.85%, but does not prove field semantics or source fault. Preserve zeros; do not impute or exclude leagues.

Belgium current scope 17171 has BTTS Yes/No and DC 1X/X2 zero on 54/63 rows (85.71%); DC12 is zero on 63/63. Two non-current scopes combined have BTTS zero on 35/385 (9.09%) and DC 1X/X2 on 41/385 (10.65%). Scope chronology is not inferred from IDs.

**Lineage limitation:** this summary uses QA #38 / archive 404474 for current xG, QA #31 / archive 403752 for Belgium season-quality rows, and Run #168 / a third runtime archive hash for team exposures. These are distinct receipts; equal row totals do not establish archive equivalence. No fixture-level cross-join is asserted.

## 4. Team DNA and sample adequacy

The Run #168 exposure artifact contains 859 team-role profiles, 779 provider team IDs and 47 league groups:
- 872 fixture exposures; 822 raw-prediction exposures; 50 blocked/incomplete exposures.
- 846 profiles have one fixture exposure; 13 have two; none have three or more.
- 833 profiles have five recent-form observations; 26 have fewer than five.
- 48 profiles have zero raw-prediction exposure.
- All 859 profiles remain canonical-join unverified, settlement-unverified and raw/uncalibrated.

These are context exposures, not repeated historical outcome samples or team-market performance samples. No team rankings, traps or exclusions are justified.

## 5. Selected-50 readiness and identity

Dry-Run #739 remains research-only. It still contains legacy Run 56 / crosswalk r17 evidence (31 direct manifest matches and 19 without a row in that old manifest). This is not evidence that 19 folders are absent from the pinned 404474 archive; QA #39 confirms all 50 current folders and 200 seasons. The planner should label the 31/19 figures as legacy snapshot evidence until rebuilt against the pinned QA manifest.

Latest readiness blockers:
- Identity crosswalk: 22 candidates require human review; 28 unresolved; 0 approved.
- Current feed: 5 groups have multiple league-ID collisions, 7 have one display-label ID, 38 have no label rows; country is not retained.
- Parent competition IDs verified: 0; canonical team joins: 0; canonical fixture joins: 0.
- Official settlement truth: 0; point-in-time xG/odds/standings: 0.
- Schedule last fixture date: 17 Oct 2026; manifest ends 22 Oct; 0 governed current fixture rows and 0 prediction rows emitted.
- BTTS / Double Chance: NOT VERIFIED; Combo: target/settlement mismatch; M-1UP: stale event truth.

Identity & Settlement Evidence Tests #16 passed and its artifact reconciled 10 evidence rows: 10 exact ordered-team/UTC-kickoff candidate joins, 6 completed cross-provider score agreements, one Canada conflict quarantined and three postponed/suspended England 0-0 placeholders excluded. Approved canonical bridges: 0; official settlement truth: 0; production/betting-eligible rows: 0. This is a small evidence-contract test, not 50-league identity closure. PR #31 remains draft; do not merge it into production.

## 6. Concise release-gate register

| Gate | Status | Closure evidence |
|---|---|---|
| Pinned 404474 archive integrity / 50 folders / 200 seasons | **PASS — research baseline** | Preserve tag, SHA and QA/runtime receipts |
| H2H chronology/metric/discordance contracts | **PASS — CI tests** | Full runtime must emit and pass integrated artifacts |
| Identity & settlement workflow execution | **PASS — #16** | Expand beyond 10 sample rows; mappings still unapproved |
| Canonical parent competition IDs | **BLOCKED — 0 verified** | Authoritative parent-ID evidence; never infer from season IDs |
| Canonical team/fixture joins | **BLOCKED — 0 verified** | League-aware source IDs, collision quarantine, evidence and human sign-off |
| Official settlement truth | **BLOCKED — 0 verified** | Independent final status/result reconciliation |
| Incomplete/past-kickoff status queue | **OPEN — 116 records** | Reconcile using existing archive-owner/internal evidence |
| Point-in-time xG/odds/standings | **BLOCKED — 0 verified** | Field semantics and source/as-of/quote timestamps |
| Current fixture freshness | **BLOCKED** | Fresh schedule, manifest and exact Selected-50 bridge |
| BTTS / Double Chance | **NOT VERIFIED** | Identity, settlement, freshness, PIT provenance and market evaluation |
| Combo | **BLOCKED** | Authoritative market definition aligned to prediction and settlement |
| M-1UP | **BLOCKED** | Fresh chronological goal-event truth and exact fixture joins |
| Team-market suitability | **BLOCKED** | Canonical pre-kickoff prediction ledger + official settlements + sample controls |
| Calibration / bookmaker value / ROI | **BLOCKED** | Separate chronological calibration and timestamped, vig-aware odds evaluation |
| Production governance | **PRESERVED** | No production changes; formal gates and explicit approval |

## 7. Safe research-only improvements

1. Run the pinned full runtime once on the latest research branch to exercise the new H2H date, chronology, metric and discordance artifact contracts.
2. Refresh the dry-run planner's identity/readiness layer from the 404474 QA manifest; retain Run 56/r17 only as historical evidence and add a stale-snapshot regression.
3. Reconcile the 116 incomplete/past-kickoff records from existing archive-owner metadata. If source semantics/timestamps are unavailable, keep the blocker explicit.
4. Preserve xG/odds values and lineage; do not impute, pool across receipts at fixture level or use exposure counts as performance evidence.

## 8. Single highest-value next action

**Nolan: manually dispatch one full “Oracle Selected-50 Research Runtime and Backtest” on the research branch.**

Workflow: [Oracle Selected-50 Research Runtime and Backtest](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/oracle-selected50-research-runtime.yml)

Inputs:
- Branch: `research/oracle-50-league-readiness-audit`
- `confirm_private_archive_read=true`
- `private_archive_release_tag=research-selected50-footystats-history-40447419806`
- `include_current_snapshot=false`
- `snapshot_run_id=0`

The available GitHub connection can inspect runs and artifacts but cannot dispatch Actions. This manual click is required. It uses the existing private archive and makes no provider/API calls or credit-consuming requests. After completion, verify the consumed archive SHA, presence of `h2h_last_date_utc`, zero invalid/naive chronology rows, strict prior-date checks, elapsed-day reconciliation, five-market metric/discordance outputs and five chronological folds.

**Final decision:** continue research only. Production and betting eligibility remain **NOT APPROVED**.
