# Project Oracle — Selected-50 Integration & Release-Gate Register

**Evidence cutoff:** 2026-10-30 06:45 SAST  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Branch head at cutoff:** `60f242dfff43acab56b08d9c6bc4a6af066d9362`  
**Decision:** Research baseline validated; production and betting release remain **NOT APPROVED**.

## Executive decision

The intended private FootyStats archive `research-selected50-footystats-history-40447419806` is now independently verified by both the full research runtime (Run #171) and private archive QA (Run #33). The runtime output contract passed and the archive QA confirms 50/50 selected groups and 200/200 ingested seasons.

This closes the archive-selection/provenance issue. It does **not** close canonical identity, official settlement, point-in-time feature, current-slate, calibration, market-value or team-suitability gates.

## Verified evidence inventory

| Evidence | Run / artifact | Result | Scope and limitation |
|---|---|---|---|
| Selected-50 runtime | [Run #171](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41001723054), artifact 12954131277 | PASS | Consumed exact 404474 archive; research output contract only |
| Private archive QA | [Run #33](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41003950016), artifact 12954144653 | PASS / REVIEW REQUIRED | 50 groups, 200 seasons, 59,049 archive rows; official settlement truth not verified |
| Dry-run planner | [Run #712](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41003949993), artifact 12954307363 | PASS | Zero network/paid-provider calls; identity/current-feed gates remain blocked |
| Safety contract tests | [Run #425](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41003950160), artifact 12954552514 | PASS | Offline contracts passed; its 200-season rollup references the older 40375285207 archive and is not current 404474 evidence |

### Archive provenance and coverage

Run #171 provenance records:

- Archive tag: `research-selected50-footystats-history-40447419806`
- SHA-256: `af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875`
- Asset size: 66,452,206 bytes; 802 archive members
- Runtime opened and consumed the exact selected archive hash; pre-runtime and at-open hashes match.
- Current-snapshot overlay was disabled and snapshot run ID was `0`.
- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`; 50 selected groups; 420 report fixture candidates; 395 with at least one supported research prediction; 25 blocked for missing required features; Combo probability fields remaining: 0.
- Production and betting eligibility are both false.

Private Archive QA #33 independently confirms:

- 50/50 selected IDs present in the archive manifest; 200/200 historical seasons marked ingested.
- 59,049 match records; 51,983 provider-status `complete` rows.
- Primary window 2025-03-20 through 2026-09-20: 22,291 records, including 22,256 provider-status `complete` and 35 non-complete rows carrying 0–0 score pairs.
- Across the full archive, all 7,066 non-complete rows carry 0–0 scores; 4,006 `complete` rows also carry 0–0. A status/score pair is still not independent official settlement proof.
- No duplicate provider match IDs were detected within or across season rows.
- 3,366 team records are team-season records, not 3,366 unique canonical clubs.
- Parent competition IDs are not exposed in the archive manifest.

### New per-season zero co-occurrence diagnostics

The new QA output contains 15,600 season/field-pair diagnostic rows. On the 48 selected current-season groups with primary-window provider-complete records, it confirms that zero values co-occur on the same fixtures in important cases:

| Selected current season | Prematch xG both zero | BTTS Yes/No odds both zero | DC 1X/X2 odds both zero |
|---|---:|---:|---:|
| Germany — Bundesliga | 18/36 (50.0%) | 0/36 | 0/36 |
| England — Premier League | 20/50 (40.0%) | 0/50 | 0/50 |
| Italy — Serie A | 18/50 (36.0%) | 0/50 | 0/50 |
| France — Ligue 1 | 16/45 (35.6%) | 0/45 | 0/45 |
| Italy — Serie B | 17/50 (34.0%) | 0/50 | 0/50 |
| Greece — Super League | 11/35 (31.4%) | 0/35 | 0/35 |
| Belgium — Pro League | 18/63 (28.6%) | 54/63 (85.7%) | 54/63 (85.7%) |

Belgium's full-time 1X and X odds were both zero on only 1/63 rows, indicating a market-specific BTTS/DC coverage issue rather than a blanket absence of odds. France, Greece and Italy also have some one-sided xG-zero rows; those must remain visible as separate missingness cases.

These are data-quality diagnostics only. They do not prove whether zero means unavailable, nor do they establish the source timestamp or pre-kickoff semantics. Do not exclude teams or leagues solely from these rates.

## H2H and raw market evidence from Run #171

H2H comparison: 19,991 paired fixtures, 95.75% of the 20,878 baseline test fixtures. Baseline and candidate used the same H2H-eligible training rows. Candidate features were the existing 20 features plus four H2H features.

| Market | Baseline accuracy | H2H accuracy | Accuracy delta | Brier delta (lower is better) | Log-loss delta (lower is better) |
|---|---:|---:|---:|---:|---:|
| BTTS | 53.649% | 53.769% | +0.120 pp | -0.00011 | -0.00022 |
| DC Home | 69.986% | 70.082% | +0.095 pp | -0.00002 | +0.00007 |
| DC Away | 60.382% | 60.352% | -0.030 pp | -0.00006 | -0.00013 |
| Combo Home | 57.401% | 57.371% | -0.030 pp | +0.00003 | +0.00006 |
| Combo Away | 64.939% | 64.949% | +0.010 pp | +0.00011 | +0.00029 |

Across five chronological H2H folds, DC Home accuracy improved 5/5, but Brier and log loss improved only 3/5. BTTS improved 2/5 on all three metrics. No H2H candidate is approved.

Raw full holdout metrics versus majority accuracy baseline:

| Market | Accuracy | Majority baseline | Difference | Interpretation |
|---|---:|---:|---:|---|
| BTTS | 53.588% | 54.143% | -0.555 pp | Does not beat majority accuracy |
| DC Home | 70.126% | 69.786% | +0.340 pp | Modest raw signal; calibration still absent |
| DC Away | 60.422% | 56.275% | +4.147 pp | Strongest raw accuracy difference; needs truth, stability and calibration checks |
| Combo Home/Away | 57.400% / 64.934% | 56.945% / 64.896% | +0.455 / +0.038 pp | Keep masked: target/settlement contract unresolved |

All raw probabilities are uncalibrated. No verified point-in-time bookmaker odds or ROI benchmark exists. The raw accuracy differences must not be interpreted as betting edge.

## Current blocker and release-gate register

| Gate | Evidence at cutoff | Status | Closure requirement |
|---|---|---|---|
| Selected-50 archive integrity | Correct 404474 tag/hash; 50/50 IDs; 200/200 seasons | **PASS — research archive only** | Preserve immutable archive/hash provenance |
| Runtime reproducibility/output contract | Run #171 success; snapshot overlay off; 25 feature-blocked fixtures | **PASS — research contract only** | Keep research and governed outputs distinct |
| Canonical league identity | 22 candidate mappings require human review; 28 unresolved; 0 approved; parent competition IDs 0 | **BLOCKED** | Authoritative competition crosswalk and human approval; never infer parent IDs from season IDs |
| Canonical team/fixture joins | 0 verified canonical team joins; 0 verified canonical fixture joins | **BLOCKED** | Exact, league-aware source-ID joins; collision/duplicate/quarantine evidence and sign-off |
| Current feed identity/freshness | Current feed has no country field; 5 groups have multiple league-ID collisions, 7 single-ID labels, 38 no label rows; source manifest 2026-10-08, reconciliation 2026-10-07, schedule ends 2026-10-17/22; 0 current governed rows | **BLOCKED** | Fresh, source-stamped current fixture snapshot and exact selected-50 bridge |
| Official settlement truth | Provider status/score diagnostics only; official settlement truth verified 0 | **BLOCKED** | Independent official final-status/result reconciliation by canonical fixture |
| Point-in-time xG/odds | Odds timestamp rows 0; verified point-in-time xG/odds rows 0; current-season zero co-occurrence outliers identified | **BLOCKED** | Field semantics, source timestamps and as-of-kickoff provenance |
| BTTS / Double Chance market readiness | All selected-50 market gates remain NOT_VERIFIED | **BLOCKED** | Exact fixture/team joins, settlement truth, feature provenance and market-specific evaluation |
| Combo markets | Predictor target is DC AND 2–4 total goals; settlement helper is DC AND total goals <5; disagreement at 0–0 and 1–0 / 0–1; Combo outputs masked | **BLOCKED** | Governed market definition and aligned target/settlement tests |
| M-1UP | Event-truth/current fixture gates remain stale/unverified | **BLOCKED** | Fresh chronological goal-event truth and exact fixture joins |
| Team-market suitability / exclusions | No validated immutable team-attributed prediction-to-settlement ledger | **BLOCKED** | Exact team/fixture mapping and verified chronological prediction/settlement pairs; use shrinkage/uncertainty and minimum samples |
| Calibration / betting value | Raw uncalibrated probabilities; odds provenance unverified; ROI benchmark not run | **BLOCKED** | Separate calibration holdout, timestamped odds, vig handling and predeclared value/ROI evaluation |
| Production governance | No production logic/probability/calibration changes; no release approval | **PASS — controls preserved** | Keep production and betting eligibility false until all gates and explicit approval pass |

## Identity resolver integration status

Draft PR #31 proposes a FootyStats-first adapter and candidate resolver with exact team/kickoff matching, fuzzy-name leads only, and quarantine for score conflicts or nonstandard home/away assignments. Its PR description reports a local smoke test (50/50 source-success seasons; 1,744 adapted rows; 681 future candidates; 370 exact season/match runtime joins; 345 raw research outputs; 25 feature-blocked; 3 with no runtime output) and 12 local unit tests. These figures are PR-description/local-smoke evidence, not a GitHub Actions CI result.

At the current branch head, the visible completed checks are contract-tests #425, private-archive QA #33 and dry-run #712. No completed dedicated identity-resolver workflow check is present on the current head. PR #31 remains draft and must not be merged into production as-is. The resolver can generate candidates, not approved canonical mappings; its source-neutral adapter also does not satisfy the production staging workflow's separate FotMob/event-truth contract.

## Evidence reconciliation warnings

1. The new 404474 QA is 50/50 and 200 seasons. The dry-run planner's legacy crosswalk/readiness summary still cites crosswalk snapshot r17 and Run 56's 14,051-row archive (31 exact season-ID matches / 19 without that old manifest record). This is a different, older evidence layer, not a contradiction to the new 404474 archive QA. Planner outputs must label that legacy source explicitly and be refreshed from the 404474 QA/crosswalk before being used as a current readiness register.
2. The Safety Contract Tests #425 artifact includes a 200-season rollup whose source run/archive hash is 40375285207 / `7c60a239...`. Do not treat that rollup as current 404474 coverage. Its contract-test success is valid; its source archive is not the current runtime baseline.
3. Run #171's 420 archive-derived fixture candidates are not the same thing as a fresh, governed current-feed slate. The dry-run's current-feed gate still emits zero governed current fixture rows.

## Safe research-only improvements

- Make the dry-run planner consume the pinned 404474 QA manifest/hash as its archive evidence source, or label its Run-56/r17 coverage as legacy and stale. Add a regression test that fails if a stale archive/crosswalk is presented as latest.
- Run the dedicated identity-resolver CI workflow against the current PR head and attach its actual GitHub result; do not infer CI success from local tests or unrelated contract workflows.
- Extend the per-season zero-co-occurrence report with explicit per-field semantics and source-timestamp availability columns, preserving row-level counts and no imputation.
- Build the next team-market analysis only from an immutable, exact-fixture, exact-team, chronological prediction/settlement ledger; do not reuse post-match features or unverified labels.

## Single highest-value next action

**Refresh the Selected-50 identity/readiness bridge from the verified 404474 archive and run the dedicated identity-resolver CI against the current research head.** First manually dispatch the existing workflow **Oracle Identity & Settlement Evidence Tests** (`.github/workflows/oracle_identity_resolver_tests.yml`) on branch `research/oracle-50-league-readiness-audit`; confirm all resolver, adapter and settlement-evidence tests pass. Then use its validated adapter/resolver to produce a new 50-row season/team/fixture candidate register, retaining every candidate as `NOT_APPROVED` until exact crosswalk evidence and human review exist. The available GitHub connection is read-only for workflow dispatch, so this dispatch requires Nolan's manual action.

No provider/API calls or credits were used for this integration pass. No production code, model logic, frozen probabilities, calibration, thresholds, registry or governance were changed.
