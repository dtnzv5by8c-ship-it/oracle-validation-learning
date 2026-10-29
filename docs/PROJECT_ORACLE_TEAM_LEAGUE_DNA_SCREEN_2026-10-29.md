# Project Oracle — Selected-50 Team & League DNA Analytics Checkpoint

**Date:** 29 October 2026  
**Source:** [Oracle Selected-50 Research Runtime #168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925)  
**Branch:** research/oracle-50-league-readiness-audit  
**Scope:** Research-only analytics from the existing Run #168 artifact. No provider/API calls, no additional credits, no production changes.

## Executive result

The current artifact supports a useful **league/market research screen** and an **upcoming-fixture team form-context inventory**. It does **not** yet support defensible team-level model-performance DNA or team exclusion decisions: the artifact does not contain team-attributed chronological out-of-sample predictions, and canonical fixture/team joins plus official settlement truth remain unverified. The locked primary H2H holdout was deliberately not used to rank teams.

## Archive and current fixture coverage

| Measure | Observed result | Interpretation |
|---|---:|---|
| Governed league groups with archive rows | 50 / 50 | All selected groups represented in this runtime artifact |
| Season rows seen / historical seasons loaded | 200 / 200 | Exact-label season mapping present in the current runtime |
| Normalized archive match rows retained | 59,049 | Research archive rows; not a source-completeness certification |
| Explicitly finished rows with numeric scores | 51,983 | Used as research labels; not independently verified against official market settlement truth |
| Upcoming fixtures in the seven-day report horizon | 436 | Current fixture candidates |
| Groups with at least one upcoming fixture in seven days | 47 / 50 | Three groups had no fixture in the checked horizon |
| Fixtures with raw research predictions | 411 / 436 | Research output only; not betting eligible |
| Fixtures blocked for missing required features | 25 / 436 | Keep blocked rather than impute silently |
| Unique country/league/team identities in upcoming fixture context | 779 | Context inventory, not historical prediction-performance sample size |
| Team-role form profiles | 859 | Separate home/away form context profiles |
| Profiles with 5 observed recent split-form matches | 833 / 859 | 21 profiles have 4; 5 profiles have 3 |

The runtime QA reports 40 future-fixture competitions with predictions; the broader schedule inventory has upcoming fixtures across 47 selected groups. Those counts describe different stages and must not be conflated.

## League/market chronological screen

The current readiness output has 50 leagues × 5 markets. This screen intentionally excludes both Combo markets because their authoritative settlement definition remains unresolved. For BTTS, Double Chance Home and Double Chance Away, a league is labelled **candidate for separate validation only** when its existing readiness status reports positive Brier skill versus the league-prevalence baseline in all three chronological folds and the per-fold minimum sample gate is met. This is a triage rule, not a profitability claim.

| Market | Candidate leagues for separate validation | Insufficient evidence | Mixed/non-positive diagnostic |
|---|---:|---:|---:|
| BTTS | 3 / 50 | 20 | 27 |
| Double Chance Home | 17 / 50 | 20 | 13 |
| Double Chance Away | 19 / 50 | 20 | 11 |

### Highest-priority league candidates to re-test

The min/max figures below are the observed range of fold-level Brier skill versus the league-prevalence baseline. Positive values mean better Brier score than that simple prevalence comparator for those folds. They do **not** establish a betting edge, and all scores are raw/uncalibrated.

**BTTS**

| League | Reported train n | Reported test n | Fold Brier-skill range |
|---|---:|---:|---:|
| Spain — Segunda División | 632 | 599 | +0.01603 to +0.06628 |
| Spain — La Liga | 524 | 504 | +0.00563 to +0.01407 |
| Netherlands — Eredivisie | 418 | 426 | +0.00485 to +0.02692 |

**Double Chance Home**

| League | Reported train n | Reported test n | Fold Brier-skill range |
|---|---:|---:|---:|
| Saudi Arabia — Professional League | 408 | 416 | +0.07053 to +0.21180 |
| Italy — Serie A | 535 | 500 | +0.06568 to +0.12319 |
| Spain — La Liga | 524 | 504 | +0.06097 to +0.14462 |
| Ukraine — Ukrainian Premier League | 276 | 332 | +0.05563 to +0.16660 |
| Netherlands — Eredivisie | 418 | 426 | +0.05508 to +0.20736 |

**Double Chance Away**

| League | Reported train n | Reported test n | Fold Brier-skill range |
|---|---:|---:|---:|
| Ukraine — Ukrainian Premier League | 276 | 332 | +0.16747 to +0.21073 |
| Russia — Russian Premier League | 292 | 375 | +0.11963 to +0.15791 |
| Saudi Arabia — Professional League | 408 | 416 | +0.09733 to +0.19115 |
| Spain — La Liga | 524 | 504 | +0.08476 to +0.13816 |
| Serbia — SuperLiga | 400 | 416 | +0.06936 to +0.15014 |

These are candidates for a **new untouched validation period**, not selections for bets. They are league-level pooled-model diagnostics and do not show that every team in the league is predictable. Selection bias across 50 leagues and three markets also needs to be accounted for before any league is approved.

## Team DNA: what is and is not supported

### Supported now — fixture-context inventory

The script creates a team/role context table from upcoming fixtures with each team's latest available split-form sequence, observed form count, W/D/L counts within that sequence, and upcoming fixture appearances. It labels this explicitly as context-only. The current archive feature QA says recent form uses the last five completed **home matches for a home team** and **away matches for an away team**, strictly before kickoff. This is not a model hit-rate, not an overall team-strength rating, and not evidence that a team is suitable for a particular betting market.

### Not yet supported — team-market performance DNA

The current artifact lacks a team-attributed chronological walk-forward prediction table. The existing H2H paired-prediction file belongs to the locked primary holdout; using it to discover teams to bet on or exclude would turn the holdout into a selection/tuning set. Therefore no teams are ranked as model-aligned, traps, or exclusions in this checkpoint.

The current upcoming fixture report also records:

- Canonical fixture joins verified: **0 / 436**.
- Canonical team joins verified: **0 / 436**.
- Official settlement truth verified: **0 / 436**.
- Odds/xG provenance verified: **0 / 436**.
- Calibration status: raw/un-calibrated; confidence and data-risk scores are not validated.

The runtime QA reports the provider's competition_id matches the selected identifier in all 50 sampled groups, but this identifier is documented as a **season ID**, not a verified parent competition ID or Oracle canonical league join. That distinction remains a material identity limitation.

## Next work, in priority order

1. **Generate team-attributed walk-forward predictions** from the existing chronological folds, including fixture ID, as-of cutoff, team IDs, market, raw probability, settled research outcome, fold ID and feature provenance. This must be a research-only export and must not alter production logic.
2. **Validate settlement labels and canonical bridges** before treating the team outcomes as ground truth. Preserve fail-closed behavior for missing/ambiguous identity or status.
3. **Build team/market profiles** only from those out-of-sample predictions. Report sample sizes, uncertainty intervals/shrinkage, Brier/log-loss/calibration, home/away splits, upset/draw/low-scoring rates and stability by chronological period.
4. **Control selection bias** across 50 leagues, teams and markets; require repeated out-of-sample confirmation before any risk flag or exclusion recommendation.
5. Keep Combo blocked until its settlement definition is resolved. Do not tune against the locked primary holdout.

## Governance decision

**Continue research; no promotion and no betting approval.** The most useful current signal is that Double Chance Home/Away have more league-level candidates than BTTS under the existing fold screen, while team-level performance DNA remains blocked by missing team-attributed walk-forward predictions and unverified settlement/canonical joins. Production logic and frozen probabilities remain unchanged.
