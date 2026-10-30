# Project Oracle — Selected-50 Team & Market Exposure Map

**Audit timestamp:** 2026-10-30 03:25 SAST  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Source runtime:** [Run #168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925)  
**Source artifact:** `oracle-selected50-research-runtime-report` (artifact `12915559785`)  
**Scope:** research-only team/market exposure and form-context indexing. No provider/API calls, no production writes, and no H2H paired-prediction/holdout file inspected or used.

## Executive result

A reproducible analysis now converts the existing Run #168 fixture report into a team-role context index and a team/market exposure matrix. It covers **779 provider team IDs**, **859 team-role profiles**, and **1,718 team/market exposure rows** across **47 league groups** represented in the fixture horizon.

This is deliberately an exposure/context map, **not a team-performance ranking**. The source report contains raw fixture probabilities and recent form, but no verified team-attributed chronological prediction/settlement pairs. Therefore this pass does not calculate team hit rate, Brier score, log loss, calibration, ROI, or market suitability.

## 1. Coverage and team sample support

| Measure | Result |
|---|---:|
| Fixture rows | 436 |
| Unique fixture IDs | 436 |
| Selected season-ID surrogates represented in fixture horizon | 47 |
| Country/league groups represented in fixture horizon | 47 |
| Countries represented | 41 |
| Distinct provider team IDs | 779 |
| Team-role profiles | 859 |
| Team/market exposure rows | 1,718 |
| Team-role profiles with one fixture exposure | 846 |
| Team-role profiles with two fixture exposures | 13 |
| Provider team IDs mapped to multiple names within this snapshot | 0 |

The archive season-coverage output contains **50 selected country/competition groups**. The fixture report contains 47. The three groups with no candidate fixture in this particular horizon are:

- Canada — Canadian Premier League
- China — Chinese Super League
- South Korea — K League 1

This is a fixture-horizon gap, not evidence that those leagues or their teams are absent from the historical archive. The sanitized `season_coverage.csv` provides per-season `team_count` aggregates but not a complete named team roster or team-by-match history for all 50 groups. Accordingly, this artifact cannot support a complete 50-league team census.

The `selected_id` field is a selected-season/competition surrogate in this report, not a verified canonical competition ID. Provider team IDs and names remain non-canonical pending the identity bridge.

## 2. Recent-form context quality

The latest fixture-as-of venue-specific W/D/L sample across the 859 team-role profiles is:

| Latest observed W/D/L sample | Profiles |
|---|---:|
| 5 matches | 833 |
| 4 matches | 21 |
| 3 matches | 5 |
| **Below five matches** | **26** |

Additional checks:

- 50 team-role profiles have at least one fixture appearance with incomplete required features; these correspond to the 25 feature-blocked fixture rows' two team slots.
- Zero reported-versus-observed recent-form sample-size mismatches were detected.
- 846 profiles have one fixture exposure; 13 have two.
- No profile has more than two fixture exposures in this snapshot.

For the latest form sample, the script reports W/D/L counts, raw win proportion, Wilson 95% interval and a Beta(1,1)-smoothed descriptive win rate. These intervals quantify uncertainty in the small recent-form sample; they are **not** predictive intervals for future results.

### League groups with the most context-support warnings

| Country | League | Team-role profiles | Profiles with latest form n < 5 | Profiles with an incomplete-feature appearance |
|---|---|---:|---:|---:|
| Germany | Bundesliga | 18 | 3 | 6 |
| Germany | 2. Bundesliga | 18 | 3 | 6 |
| South Africa | Premier Soccer League | 27 | 3 | 6 |
| England | Premier League | 20 | 2 | 4 |
| Belgium | Pro League | 20 | 2 | 4 |
| Portugal | LigaPro | 18 | 2 | 4 |
| Italy | Serie B | 20 | 2 | 4 |

These are data-support flags only. They do not indicate that the teams or leagues are poor bets or that Oracle is inaccurate there.

## 3. Market exposure — what the probabilities do and do not mean

| Market field | Fixture-level probability observations | Team exposure interpretation |
|---|---:|---|
| BTTS | 411 | The same fixture-level BTTS probability is attached to both participating teams; it is not a team-specific BTTS probability. |
| DC_HOME | 411 | Home-or-draw probability for the fixture. |
| DC_AWAY | 411 | Away-or-draw probability for the fixture. |
| COMBO_HOME | 0 | Blocked; no usable probability emitted. |
| COMBO_AWAY | 0 | Blocked; no usable probability emitted. |

The team-market exposure CSV contains:
- `BTTS_FIXTURE_EXPOSURE`: fixture-level BTTS probability shared by both teams.
- `DOUBLE_CHANCE_TEAM_SIDE`: DC_HOME probability for a team appearing at home, or DC_AWAY probability for a team appearing away. This is the probability that the team avoids defeat, **including a draw**.

The matrix reports exposure counts and probability distributions (mean, median, minimum and maximum) by provider team, selected-season surrogate, league and fixture role. These describe where the current model assigns probabilities; they do not measure whether those probabilities were correct.

## 4. Prediction, identity and settlement gates

| Gate | Run #168 report |
|---|---:|
| Raw research predictions | 411 |
| Blocked for missing required features | 25 |
| Canonical fixture joins verified | 0 / 436 |
| Canonical team joins verified | 0 / 436 |
| Official settlement truth verified | 0 / 436 |
| Invalid numeric probabilities in BTTS/DC fields | 0 |
| Production eligible | No |
| Betting eligible | No |

The 25 blocked fixtures remain blocked. This analysis does not impute missing features or manufacture probabilities.

Probabilities are marked `RAW_ONLY_UNCALIBRATED`; odds/xG provenance is unverified. No team-market accuracy, calibration or profitability metric can be honestly derived from this file.

## 5. Data freshness and provenance

At the analysis timestamp:

- Runtime generated: **2026-10-29 17:09:30 UTC**.
- Underlying snapshot retrieved: **2026-10-29 11:46:20 UTC**.
- Runtime age: **8.26 hours**.
- Snapshot age: **13.65 hours**.
- Runtime archive consumption receipt: verified.
- Runtime archive SHA-256: `e6fe86d636402e1078cdca5ae88ed211e49e78123916d3995cac4200d511d5ed`.

The snapshot is not fresh enough to treat this output as a live fixture slate. These outputs are a reproducible research index of the captured Run #168 artifact only.

## 6. Reproducibility and files

The new standard-library script reads only:
- `oracle_selected50_prediction_report.csv`
- `oracle_selected50_runtime_provenance.json`

It deliberately does not read H2H columns, H2H ablation metrics, the paired-prediction file, settlement files, or provider endpoints.

Outputs:
- `oracle_selected50_team_context_exposure.csv` — one row per team/league/selected-season/fixture-role profile (859 rows).
- `oracle_selected50_team_market_exposure.csv` — two market-exposure rows per profile (1,718 rows).
- `oracle_selected50_league_team_exposure_rollup.csv` — one summary row per represented league group (47 rows).
- `oracle_selected50_team_market_exposure_summary.json` — provenance, counts, freshness and explicit interpretation gates.

Seven regression tests pass locally, covering role attribution, market semantics, blocked fixtures, chronological latest-context selection, duplicate fixture rejection, missing provider IDs and provenance failure. This is local test evidence; no new GitHub Actions run was dispatched in this pass.

## 7. Decision and next action

**Decision:** use this matrix as a descriptive team/context index only. Do not rank teams for betting, call any team a trap, or permanently exclude teams from this output.

The next required dataset is a separate, immutable team-attributed chronological prediction/settlement ledger with canonical fixture and team IDs, prediction-before-kickoff timestamps, model version/commit, probability, feature archive hash/source-as-of timestamps, and separately verified settlement events. Only that dataset can support team-level hit rate, Brier/log loss, calibration, draw/upset/low-scoring risk and uncertainty/shrinkage by market.

A complete 50-league team census also requires a named team roster or team-by-match archive export; the current sanitized runtime provides only per-season team counts for the three groups absent from the fixture horizon.

**Governance:** no provider API calls or credits used; no H2H holdout read; no production model logic, frozen probabilities, calibration or governance changed. Production and betting eligibility remain unapproved.

## 8. Repository commits and row-level outputs

Committed to the research branch:
- `scripts/analyze_selected50_team_market_exposure.py`
- `tests/test_selected50_team_market_exposure.py`
- this audit report
- `reports/oracle_selected50_team_market_exposure_summary_2026-10-30.json`
- `reports/oracle_selected50_league_team_exposure_rollup_2026-10-30.csv`
- `reports/oracle-data-team-dna-automation-checkpoint-2026-10-30-0325-sast.md`

The full 859-row team context CSV and 1,718-row team/market exposure CSV are included in the accompanying downloadable research bundle. The committed script regenerates both from the same two approved Run #168 inputs.
