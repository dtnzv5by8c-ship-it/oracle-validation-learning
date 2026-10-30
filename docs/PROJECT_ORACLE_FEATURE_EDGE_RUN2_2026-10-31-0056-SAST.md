# Project Oracle — Feature Edge Run 2: Lag Sensitivity & Ranking Chronology QA

**Timestamp:** 31 October 2026, 00:56 SAST  
**Branch:** research/oracle-50-league-readiness-audit  
**Scope:** research-only; existing verified artifacts only.

## Executive decision

This incremental run did not repeat ingestion, snapshot, runtime or bridge workflows. It added (1) offline 48-hour and 72-hour event-time lag sensitivities against the prior 24-hour feature experiment and (2) exact UTC kickoff reconciliation between Bridge Audit #12 and the runtime fixture report before publishing current-fixture rankings.

The ranking universe is corrected from 325 to **322 candidates per market**. All 426 runtime rows join one-to-one on selected season ID, fixture ID and ordered home/away provider team IDs. However, 21 rows have a snapshot/runtime UTC kickoff mismatch. Eighteen were already excluded by existing source/nonfuture quarantine rules. Three otherwise-rankable Saudi Professional League fixtures are now additionally excluded until their schedule chronology is reconciled.

## 1. Kickoff chronology reconciliation

| Check | Result |
|---|---:|
| Runtime fixture rows | 426 |
| Exact fixture/team ID joins | 426 / 426 |
| Snapshot/runtime UTC kickoff mismatches | 21 |
| Already excluded by source/nonfuture quarantine | 18 |
| New otherwise-rankable kickoff-mismatch exclusions | 3 |
| Candidates before kickoff equality gate | 325 per market |
| Final rankable candidates after all gates | **322 per market** |
| Selected country-league groups with candidates | **37 / 50** |
| Distinct display league labels | 33 |

The three new exclusions are fixture IDs **8620566, 8620618 and 8620625** (Saudi Professional League). Their runtime report kickoff differs from the snapshot kickoff by more than 60 minutes. They are not treated as the same scheduled event until the source schedule is reconciled. No fuzzy identity or date-only join was used.

The updated ranking rule requires all of: exact selected-season/fixture/ordered-team IDs; exact UTC kickoff equality; FUTURE_RESEARCH_CANDIDATE; source_no_home_away=0; RAW_RESEARCH_ONLY; and PASS_ALL_20_REQUIRED_FEATURES.

## 2. Corrected fixture ranking tabs

The three Top-50 sheets have been rebuilt from the complete 322-candidate universe, rather than retaining the prior top-50 lists that contained quarantined rows. They now contain 50 rows each, with zero source-quarantined rows and zero kickoff mismatches. Top-3 overall and top-3-per-selected-league-group tabs were also rebuilt under the same rule. The per-group tabs contain 111 rows: three candidates for each of 37 groups. The updated 40-tab workbook is delivered as the run artifact; its exact SHA-256 and sheet inventory are recorded in the workbook manifest.

### Top 3 overall — BTTS
| Fixture ID | League | Fixture | Kickoff UTC | Raw probability |
|---:|---|---|---|---:|
| 8411774 | Eliteserien | Brann vs Molde | 2026-11-01T13:30:00+00:00 | 68.94% |
| 8547842 | Eredivisie | Cambuur vs Go Ahead Eagles | 2026-10-31T20:00:00+00:00 | 66.61% |
| 8390942 | MLS | FC Cincinnati vs Philadelphia Union | 2026-10-31T18:00:00+00:00 | 65.89% |

### Top 3 overall — DC Home
| Fixture ID | League | Fixture | Kickoff UTC | Raw probability |
|---:|---|---|---|---:|
| 8579426 | Liga I | CS U Craiova vs Botoşani | 2026-11-01T15:30:00+00:00 | 91.83% |
| 8565837 | Bundesliga | Rapid Wien vs Wolfsberger AC | 2026-11-06T18:30:00+00:00 | 91.61% |
| 8583512 | Süper Lig | Amed vs Eyüpspor | 2026-11-01T10:30:00+00:00 | 91.55% |

### Top 3 overall — DC Away
| Fixture ID | League | Fixture | Kickoff UTC | Raw probability |
|---:|---|---|---|---:|
| 8546253 | Prva HNL | Rudeš vs Dinamo Zagreb | 2026-10-31T17:00:00+00:00 | 83.54% |
| 8553116 | J1 League | Mito Hollyhock vs Sanfrecce Hiroshima | 2026-10-31T05:00:00+00:00 | 82.50% |
| 8553096 | J1 League | Fagiano Okayama vs Tokyo | 2026-10-31T05:00:00+00:00 | 81.43% |

All probabilities are raw and uncalibrated. These rankings are not confidence scores, betting recommendations or production approvals. Canonical cross-provider identity and official settlement truth remain unverified.

## 3. Feature history-lag sensitivity

The same supplementary exact-ID archive, 31/50 league groups, fixed L2 logistic challenger, smoothed league-prevalence baseline and three expanding validation folds were used at 24h, 48h and 72h history cutoffs.

- 48h vs 24h: overall fold metrics and test counts are identical in this dataset.
- 72h: one fewer test row for recent-goals/scoring feature families and two fewer for venue families across the three folds; overall decisions remain unchanged.
- DC_HOME: RECENT_GOALS_STRENGTH and VENUE_SPLITS pass the same overall repeatability gate at 24h, 48h and 72h. At 72h the venue-split mean ECE delta improves from +0.000709 at 24/48h to -0.000019.
- BTTS: no overall feature family passes at any lag.
- DC_AWAY: discrimination and proper scores improve for some challenger feature families, but calibration/ECE still fails the combined gate at all lags.

Per-league gates show 10 market-feature-league candidates persistent across all three lags; five additional per-league gates appear only at 72h, while one 24h candidate does not persist at 72h. These remain exploratory, sample-dependent league-level signals.

**Important PIT limitation:** the 24h/48h/72h cutoffs are event-time safeguards only. The archive does not provide immutable provider publication timestamps proving each historical score was visible to the model before the target kickoff. The lag sensitivity therefore does not satisfy the strict point-in-time provenance gate and does not authorize feature promotion. The challenger is not Oracle V1.6 and does not quantify direct production uplift.

## 4. Source-family status

- Tested on lagged completed scores: recent goals for/against, goal difference, points per game, scoring/clean-sheet/failed-to-score profiles and home/away venue splits.
- H2H: existing five-fold evidence reused; no rerun and no case to increase H2H weight.
- Excluded pending PIT proof: xG for/against, shots/on-target, historical standings/strength snapshots and bookmaker odds.
- Not tested: travel; no verified venue geocodes or route-distance history.
- Rest interval remains sensitivity-only; kickoff gaps are not match-end or recovery timestamps.

## 5. Governance and next research step

- No provider/API credits used.
- No ingestion, snapshot, runtime or bridge workflow rerun.
- Oracle V1.6 production logic, probabilities and calibration unchanged.
- production_eligible=false; betting_eligible=false.

Next: resolve the three Saudi schedule mismatches through source evidence, then secure immutable publication-time provenance for xG, odds, shots and standings before any further feature inclusion. Do not change the production model.
