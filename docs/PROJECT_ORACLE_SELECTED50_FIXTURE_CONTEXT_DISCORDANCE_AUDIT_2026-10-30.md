# Project Oracle — Selected-50 Fixture Context Discordance Audit

**Audit timestamp:** 2026-10-30 02:26 SAST  
**Research branch:** \`research/oracle-50-league-readiness-audit\`  
**Source runtime:** [Run #168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925)  
**Source runtime generated:** 2026-10-29 17:09:30 UTC  
**Source snapshot retrieved:** 2026-10-29 11:46:20 UTC  
**Scope:** research-only fixture-context triage. No provider/API calls, no production writes, and no access to the locked H2H paired-prediction holdout.

## Executive finding

A new fixture-context screen compared Oracle's raw Double Chance selection preference with the two teams' recent venue-specific W/D/L form, and compared raw BTTS probabilities with the displayed recent-H2H BTTS rate and scoring context.

It identified **157 of 436 fixture rows** with at least one exploratory context flag:
- 9 Double Chance preference versus recent-form disagreements;
- 58 BTTS probability versus H2H-rate gaps of at least 30 percentage points;
- 64 low-scoring H2H context flags (average total goals at or below 1.8);
- 67 high-scoring H2H context flags (average total goals at or above 3.2).

These counts are non-exclusive. They identify cases for manual research review, not model errors, traps, team exclusions, market edges or betting selections.

## 1. Source and coverage

| Measure | Result |
|---|---:|
| Fixture rows in Run #168 report | 436 |
| Raw research predictions | 411 |
| Blocked for missing required features | 25 |
| Country/league groups represented in this fixture horizon | 47 |
| Countries represented | 41 |
| Team slots | 872 |
| Distinct provider team IDs in the fixture snapshot | 779 |
| Provider team IDs associated with multiple names in this snapshot | 0 |
| Competition/team-name pairs associated with multiple provider IDs in this snapshot | 0 |

The zero collision counts are internal consistency checks only. They do **not** verify canonical Oracle team identity or competition identity.

The 25 blocked rows all had fewer than five recent home or away matches in the relevant split: 17 had home sample below five, 9 had away sample below five, and 1 was below five on both sides. No raw research prediction was emitted with either reported recent-five split below five.

## 2. H2H chronology and sample support

The displayed recent-H2H W/D/L sequence-length distribution was:

| Displayed sequence length | Fixture rows |
|---:|---:|
| 0 | 65 |
| 1 | 18 |
| 2 | 61 |
| 3 | 19 |
| 4 | 49 |
| 5 | 224 |

A recent-H2H BTTS rate was present on 371 fixture rows. For all rows where both timestamps were parseable, the last-H2H date preceded fixture kickoff: **zero date-at-or-after-kickoff violations** were detected. No row with an available H2H BTTS rate lacked the displayed last-meeting date.

The displayed W/D/L sequence length is only a proxy for the recent-H2H context sample. The exact denominator used to calculate the H2H BTTS rate is not independently exposed in this report. Consequently, the rate-gap flags below are descriptive only; no confidence interval is claimed for the H2H rate.

## 3. Double Chance preference versus recent form

A fixture was flagged when:
- the absolute difference between raw DC_HOME and DC_AWAY probabilities was at least 10 percentage points; and
- the five-match home-minus-away form-points margin (3 points per win, 1 per draw, 0 per loss) was at least 3 points in the opposite direction.

**Nine fixtures** met that rule.

| Fixture | Home recent 5 | Away recent 5 | DC_HOME − DC_AWAY | Home − away form points |
|---|---|---|---:|---:|
| Corinthians – Mirassol | LLLLD | DLWDL | +24.11 pp | −4 |
| Ajax – AZ | DLWDD | WWWLD | +19.14 pp | −4 |
| Chelsea – Manchester United | WWDWL | WLDDD | −16.79 pp | +4 |
| Barnsley – Oxford United | LWLDL | WLWWD | +14.43 pp | −6 |
| Orenburg – CSKA Moskva | LDDDW | WDWWL | +10.47 pp | −4 |
| Ceuta – Sporting Gijón | LDWLL | WWLWL | +35.00 pp | −5 |
| Bragantino – Santos | LWLDW | WWWLW | +37.27 pp | −5 |
| Watford – Lincoln City | DWLLW | WWWLD | +12.34 pp | −3 |
| Kaizer Chiefs – AmaZulu | LWDWD | WLWWW | +11.28 pp | −4 |

**Interpretation caution:** DC_HOME and DC_AWAY both include the draw outcome. Their difference is a relative selection preference, not a direct home-win versus away-win probability. Recent form is a five-match descriptive sample and may not represent opponent strength, injuries, schedule difficulty or other model inputs. These nine fixtures are a review queue, not evidence that the model is wrong.

## 4. BTTS probability versus recent-H2H context

Fifty-eight fixtures had an absolute difference of at least 30 percentage points between raw BTTS probability and the displayed recent-H2H BTTS rate, with at least three entries in the displayed H2H W/D/L sequence. Forty-two had Oracle's BTTS probability above the H2H rate; sixteen had it below.

### Largest positive gaps

| Fixture | Oracle BTTS | H2H BTTS rate | Gap | Displayed H2H n proxy |
|---|---:|---:|---:|---:|
| Aalesund – Sandefjord | 65.02% | 0% | +65.02 pp | 3 |
| Groningen – Sparta Rotterdam | 63.85% | 0% | +63.85 pp | 4 |
| Los Angeles FC – Minnesota United | 63.26% | 0% | +63.26 pp | 5 |
| Alianza Atlético – Juan Pablo II College | 60.56% | 0% | +60.56 pp | 3 |
| Atlético Bucaramanga – Atlético Nacional | 60.41% | 0% | +60.41 pp | 5 |

### Largest negative gaps

| Fixture | Oracle BTTS | H2H BTTS rate | Gap | Displayed H2H n proxy |
|---|---:|---:|---:|---:|
| CD Universidad Católica – SD Aucas | 47.79% | 100% | −52.21 pp | 5 |
| Lokomotiv Moskva – Spartak Moskva | 52.89% | 100% | −47.11 pp | 5 |
| Newcastle Jets – Wellington Phoenix | 53.14% | 100% | −46.86 pp | 5 |
| Deportivo Recoleta – Sportivo Ameliano | 54.84% | 100% | −45.16 pp | 5 |
| New England Revolution – Inter Miami | 54.85% | 100% | −45.15 pp | 5 |

These gaps may reflect a genuine model/context disagreement, small or dependent H2H samples, changing team strength, or differences between historical H2H and current team context. They are not proof of predictive failure or value. H2H is not independent across repeated meetings and must not be treated as a standalone forecast.

## 5. Scoring-context flags

Among fixture rows with at least three entries in the displayed H2H W/D/L sequence:
- 64 had average H2H total goals at or below 1.8;
- 67 had average H2H total goals at or above 3.2.

These flags can be used to prioritise BTTS and goal-market review. They do not establish a team-level low-scoring or high-scoring tendency, and they do not override model probabilities. The exact denominator and point-in-time provenance of the H2H scoring features remain unverified.

## 6. Latest independent readiness check

The latest post-change dry-run planner was [Run 40980198388](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40980198388). It completed successfully; all listed steps passed, and its artifact still reports zero network calls and zero paid-provider calls. The latest safety-contract run [40980198406](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40980198406) also passed. It compiled the new research script and ran all seven new fixture-context discordance tests successfully. The first CI attempt exposed an incorrect test import path (the test file is under tests/ while the script is under scripts/); the path was corrected in commit ed12fc187abaf38e8d5319095085aa799453281b before the passing rerun.

A successful dry-run is not a readiness approval. Its artifact reports:
- 50 selected season IDs;
- 31 exact Run 56 manifest matches and 19 selected IDs without a Run 56 manifest row, reconciled against a separate retained-package evidence layer;
- zero verified parent competition IDs;
- zero canonical fixture/team joins and zero official settlement-truth rows;
- 22 candidate crosswalk rows requiring human review and 28 unresolved rows;
- zero current governed fixture rows, with the retained schedule stale (last fixture date 2026-10-17; manifest window ended 2026-10-22);
- production eligibility false.

The dry-run's separate 14,051-row private-archive QA snapshot is explicitly pre-batch-5 and superseded by later historical ingestion; it must not be represented as the latest 200-season archive coverage. Run #168's 59,049 normalized historical rows are a different runtime archive population. Do not add or equate these counts without a reconciled archive version and identity crosswalk.

## 7. What this analysis does not establish

- No team-level out-of-sample accuracy, Brier score, log loss, calibration or ROI was computed.
- The current fixture report contains pre-fixture context and raw probabilities, not historical team-attributed prediction/outcome pairs.
- Canonical fixture/team joins and official market settlement truth remain unverified.
- Probabilities are raw and uncalibrated; odds and xG point-in-time provenance are unverified.
- The fixture artifact was generated 7h 17m before this audit; its underlying snapshot was retrieved 12h 40m before this audit. It is not a fresh live slate.
- The locked H2H paired-prediction holdout was not opened, read, ranked or used.
- No production model logic, frozen probability, calibration, threshold, registry or governance setting was changed.

## 8. Next action

1. Obtain a fresh historical-only Selected-50 research runtime artifact from the existing private archive, with current-snapshot overlay disabled and no provider refresh. A GitHub workflow dispatch is still a manual action; the connected GitHub interface used for this audit has no workflow-dispatch operation.
2. Re-run this context screen against the new artifact and compare whether the same disagreement patterns persist.
3. Build a prospective immutable prediction ledger under the existing Prospective Prediction Evaluation Protocol. It must record prediction timestamp, fixture/team IDs, model version/commit, raw probability, feature archive hash and source-as-of timestamps before kickoff.
4. Append separately verified settlement events. Only after identity and settlement validation can team-market hit rates, Brier/log loss, calibration, upset/draw risk and uncertainty/shrinkage be assessed out of sample.
5. Keep all current context flags as review-only. Do not label teams as traps or permanently exclude them from betting.

**Decision:** useful fixture-context triage has been added, but validated team-market DNA remains blocked by the missing team-attributed out-of-sample prediction/settlement ledger and unresolved canonical identity. Production and betting eligibility remain unapproved.
