# Project Oracle — Team & H2H DNA Research Update

**Timestamp:** 30 October 2026, 23:15 SAST  
**Research branch:** `research/oracle-50-league-readiness-audit`  
**Run scope:** Team & H2H DNA only; research/reporting lane  
**Starting branch head:** `4768ec7bc7aa1bfe636ee151f167bdc8355ed5b9`

## Executive result

This run produced a new descriptive team/H2H research layer from the existing supplementary FootyStats archive feature-audit extract. It generated:

- **732 team profiles** across **31 of the governed 50 groups**;
- **7,188 exact-ID H2H pair profiles** from **23,328 chronological completed meetings**;
- league-level score distributions for those same 31 groups;
- home/away, trailing-365-day, last-five and last-ten team splits;
- explicit sample-size warnings and repeat-window high/low scoring screens.

This is a **partial 31/50 descriptive extract**, not a complete 50-league team/H2H dataset. The remaining 19 groups have no exact selected-ID-to-source-season-ID bridge in this extract. They are marked unavailable, not treated as having zero matches. No fuzzy league or team-name joins were used.

## 1. Source and scope

Supplementary source: `oracle-footystats-archive-feature-audit-64.zip`  
SHA-256: `65aca16d0562745576f1499d25808498a560b5167cdf00bc86074f8e4c20211a`

The source audit reports 35,819 match rows across 126 season folders and 42 source league groups, with zero duplicate fixture IDs and zero records missing team IDs. This extract is separate from the complete selected-50 archive consumed by the current runtime.

Exact mapping rule: a governed `selected_id` was accepted only where it exactly matched `season_id` in the source ingestion manifest. That exact season-folder match identifies the corresponding source league folder; the other two season folders in that exact group were then included. The 11 additional source groups that did not match a governed selected ID were excluded.

| Coverage measure | Result |
|---|---:|
| Governed groups | 50 |
| Exact selected-ID / source season-ID matches | 31 |
| Groups unavailable in this extract | 19 |
| Source season folders used | 93 |
| Raw rows in the 31 matched folders | 30,257 |
| Eligible completed matches through 20 Sep 2026 | 23,328 |
| Primary validation-window matches (20 Mar 2025–20 Sep 2026) | 15,003 |
| 2024 matches | 5,715 |
| 2025 matches | 10,307 |
| 2026 matches through 20 Sep | 7,306 |

Observed match dates run from **22 February 2024 to 20 September 2026**. All 23,328 included rows have `status=complete`, parseable UTC kickoff, explicit score fields for both teams and a raw-record SHA-256. The 6,929 other raw rows in the matched folders were excluded because they were non-complete and/or outside the 20 September 2026 cutoff.

The primary governed validation window remains **20 March 2025–20 September 2026**. The 2024 matches are used as earlier descriptive history and are not represented as a change to that primary validation window.

## 2. Team DNA

The 732 profiles use the exact key `selected_id + provider_team_id`. Provider team IDs repeat across league groups (58 IDs occur in more than one group), so a team ID alone is not a safe key. Each team ID maps to one exact source team name within its selected group in this extract; no name-variant merge was required.

Metrics include:

- goals for and against, overall and by home/away venue;
- mean and median match total goals, plus 0–1, 2, 3, 4 and 5+ goal bands;
- BTTS and Over 1.5/2.5/3.5;
- clean sheets, failed to score, win/draw/loss and non-loss rates;
- all-history, primary-window and trailing-365-day samples;
- last-five and last-ten form sequences, in chronological order.

### Sample reliability

| All-history sample tier | Teams |
|---|---:|
| 50+ matches | 493 |
| 30–49 | 163 |
| 8–29 | 22 |
| Fewer than 8 | 54 |

The primary-window sample is smaller: 317 teams have 50+ matches, 247 have 30–49, 103 have 8–29 and 65 have fewer than 8.

A high/low scoring profile candidate requires at least 30 all-history and 15 primary-window team matches, plus a difference of at least 0.50 goals per match and 10 percentage points in Over 2.5 against the same league baseline in **both** windows.

| Scoring screen | Teams |
|---|---:|
| High-scoring candidates | 15 |
| Low-scoring candidates | 13 |
| No clear repeatable deviation | 554 |
| Insufficient sample for a style label | 150 |

Examples from the high-scoring screen include Inter Miami (103 matches; 3.99 mean total goals; 78.6% Over 2.5) and PSV (75; 4.29; 86.7%). Examples from the low-scoring screen include Stevenage (101; 2.07; 36.6% Over 2.5) and Getafe CF (83; 1.86; 28.9%). These are descriptive historical profiles, not forward probabilities or betting recommendations.

## 3. Exact H2H DNA

The H2H pair key is `selected_id + lower_provider_team_id + higher_provider_team_id`. Team A/B ordering is by provider ID, not by home/away. The workbook includes both an aggregate pair profile and a separate chronological meeting ledger with fixture IDs, score, venue perspective and raw-record hashes.

| H2H sample tier | Pair profiles |
|---|---:|
| 1–2 meetings (very low) | 3,273 |
| 3–4 (low) | 2,513 |
| 5–7 (developing) | 1,243 |
| 8+ (repeated history; not predictive proof) | 159 |

Only 159 of 7,188 pairings have eight or more observed meetings. A high/low H2H scoring screen is therefore applied only to those 159 pairings and still remains exploratory:

- 22 high-scoring H2H screens;
- 30 low-scoring H2H screens;
- 107 with no clear deviation from the league baseline;
- 7,029 pairings excluded from style labelling for insufficient H2H sample.

Examples include Inter Miami–Nashville SC (9 observed meetings; 4.11 mean total goals; 88.9% BTTS; 100% Over 2.5) and Istra 1961–Varaždin (9; 1.22 mean total goals; 22.2% BTTS; 22.2% Over 2.5). The H2H history starts at the available extract boundary in February 2024; earlier meetings are not present.

## 4. Existing runtime H2H feature evidence

The existing Run **#176** runtime H2H ablation uses four features: `h2h_prior_n`, `h2h_btts_rate_last5`, `h2h_avg_total_goals_last5` and `h2h_days_since_last`.

- Paired holdout: **19,991 fixtures**, or **95.75%** of the 20,878-fixture test window.
- Paired chronology QA: **PASS**, 99,955 market rows / 19,991 fixtures, with zero duplicate fixture-market keys, invalid prior dates or chronology violations.
- Five expanding chronological folds were available for each of five markets.

The H2H effect is small and mixed. In the five folds, Brier improved in 2/5 BTTS folds, 3/5 DC Home folds and only 1/5 DC Away folds. Combo Home and Combo Away improved in only 1/5 folds each. The primary holdout shows small numerical changes, but not a consistent cross-market, cross-fold improvement. **No H2H weighting or production change is recommended.**

The runtime H2H model evidence is kept separate from the 31-group descriptive pair profiles; no cross-archive team-name or team-ID join was made.

## 5. Snapshot/runtime bridge and governance

The existing snapshot-to-runtime bridge artifact reports:

- snapshot consumption and runtime archive-open hash verification: **PASS**;
- 426 runtime report rows exactly reconciled to source rows;
- 99.14% exact join coverage within seven days;
- three within-seven-day fixtures remain unmatched;
- bridge status: `PASS_BRIDGE_AUDIT_WITH_RELEASE_BLOCKERS`.

This is a provenance pass, not a release approval. `production_eligible=false` and `betting_eligible=false` remain in force.

No provider/API credits were used. No ingestion, snapshot, runtime or bridge workflow was rerun. Oracle V1.6 production logic and frozen probabilities were not modified.

## 6. Deliverables

Detailed workbook: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_30Oct2026_v3_Team_H2H_DNA.xlsx`  
Workbook SHA-256: `470ad084dc03f2d8afc5a5d4bc9415e47fcabd379b5d4c39f0190b23e2551fac`  
Workbook size: 6,344,909 bytes

New workbook tabs:

1. `League Match DNA`
2. `Team DNA`
3. `Team Venue DNA`
4. `Team Recency DNA`
5. `H2H DNA`
6. `H2H Meetings`
7. `DNA Coverage`
8. `H2H Model Evidence`

Compact companion CSV exports are also prepared:

- `team_scoring_candidates.csv`
- `h2h_scoring_candidates.csv`
- `dna_coverage_50_leagues.csv`
- `h2h_model_evidence.csv`
- `oracle_selected50_team_h2h_dna_summary_2026-10-30.json`

The workbook and companion CSVs are delivered as conversation artifacts. The dated Markdown note and compact JSON checkpoint are the branch-persisted continuation record; the JSON records the companion CSV hashes.

## 7. Next action

Continue from the already verified full selected-50 archive and seek an exact, read-only member-level bridge for the 19 groups missing from this supplementary extract. Do not spend provider credits or infer missing league/team identities from names. Keep all current team/H2H outputs partial and research-only until that exact coverage is available.
