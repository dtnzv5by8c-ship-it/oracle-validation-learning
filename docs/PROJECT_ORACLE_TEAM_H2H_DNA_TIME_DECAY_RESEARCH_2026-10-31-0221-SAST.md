# Project Oracle — Team & H2H DNA: Time-Decay Sensitivity

**Run timestamp:** 31 October 2026, 02:21 SAST  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Disposition:** research-only; `production_eligible=false`; `betting_eligible=false`

## Executive result

This incremental pass extends the verified Run 3 Team/H2H market-reliability work with exponential time-decay estimates and Kish effective sample sizes. It uses the published v7 workbook whose SHA-256 is pinned in the Run 3 manifest. No ingestion, snapshot, runtime, backtest or bridge workflow was rerun; provider/API credits used: **0**.

- **Team profiles:** 732 exact composite keys (`selected_id + provider team_id`).
- **H2H profiles:** 7,188 exact pair keys and 23,328 chronological meetings.
- **Fixture integrity:** 23,328 unique fixture IDs, zero duplicate rows and 100% raw record-hash coverage.
- **New workbook tabs:** Team Time-Decay DNA; H2H Time-Decay DNA; DNA Decay Sensitivity; H2H Decay Watch; H2H Recency-Effective Leaders; Decay Methodology; Private Archive Retrieval.

## Method

Each match receives `w = 0.5 ** (age_days / half_life_days)`, where age is measured from the fixed archive cutoff `2026-09-20T23:59:59Z`. Two sensitivity settings are reported: **365 days** and **730 days**. Effective sample size is Kish `n_eff = (sum(w)^2 / sum(w^2))`, shown separately from raw match count.

Team metrics include goals for/against, total goals, BTTS, Over 1.5/2.5/3.5, clean sheet, failed-to-score, win, draw and non-loss. H2H metrics include team-A/team-B goals, total goals, BTTS, overs, draw, team-A/team-B wins, non-loss, clean sheets and failed-to-score.

## Main finding: H2H recency is much thinner than raw meeting counts suggest

| Profile group | Median effective n, 365d half-life | Median effective n, 730d half-life | Pairs with effective n ≥8, 365d | Pairs with effective n ≥8, 730d |
|---|---:|---:|---:|---:|
| H2H pairings | 2.80 | 2.95 | 1 | 68 |
| Team profiles | 62.54 | 70.73 | 648 at n_eff ≥30 | 650 at n_eff ≥30 |

Only **1 of 7,188** H2H pairs reaches effective n≥8 with a 365-day half-life; **68 of 7,188** do so with 730 days. Median H2H effective n is only 2.80/2.95. This is a strong warning against treating historical H2H counts as equivalent to current matchup evidence. Team history is materially deeper: 648 / 732 teams reach effective n≥30 under 365 days.

Examples of the 730-day effective-sample leaders (still only 9–10 raw meetings):

| League | Team A | Team B | Raw meetings | Effective n, 730d | Weighted Over 2.5 |
|---|---|---|---:|---:|---:|
| Bundesliga | LASK Linz | Hartberg | 10 | 9.54 | 54.3% |
| Prva HNL | Lokomotiva Zagreb | Gorica | 9 | 8.65 | 68.9% |
| Premiership | Rangers | Hibernian | 9 | 8.64 | 47.0% |
| Liga I | Dinamo Bucureşti | CS U Craiova | 9 | 8.63 | 56.4% |
| Super League | Luzern | Lausanne Sport | 9 | 8.63 | 66.7% |

These examples are research diagnostics, not fixture recommendations.

## Half-life sensitivity

- Team Over 2.5: median absolute 365d-vs-730d difference **0.69 pp**, p90 **2.03 pp**; no team exceeds a 10pp difference on this metric.
- H2H Over 2.5: median absolute difference **2.13 pp**, p90 **6.61 pp**; 88 pairs exceed 10pp.
- H2H BTTS: median absolute difference **2.22 pp**, p90 **6.58 pp**; 87 pairs exceed 10pp.

The two half-lives are sensitivity settings only; neither was selected through backtesting. Large differences indicate sensitivity to the decay assumption, not a predictive edge.

## Critical venue limitation

The `H2H Meetings` ledger does not expose the explicit `no_home_away` flag. A `team_a_venue` label alone is not sufficient to certify venue validity. This run therefore calculates **overall team-relative time-decay profiles only** and does not infer time-decay home/away splits. Existing `Team Venue DNA` and `H2H DNA` tabs remain the source for their previously validated venue splits.

## Continuity and limitations

- Full archive ledger: 50/50 exact selected IDs, 200 seasons and 59,049 archived rows. Accessible raw score extract remains 31/50 selected groups; the other 19 remain unavailable and are not zero-filled.
- Team keys include `selected_id` because 58 provider team IDs recur across selected groups. H2H uses exact selected ID and ordered provider team IDs. No fuzzy joins.
- Primary governed validation window remains 20 March 2025–20 September 2026. These profiles use available complete history through the cutoff and do not replace primary-window OOS evaluation.
- Score-derived H2H is not official settlement truth; canonical cross-provider identity remains unverified.
- This workbook extends the verified v7 Team/H2H workbook. The separate Feature Edge Run 3 v8 binary was not present in this run's accessible file set; this v9 file does not claim to merge that separate workbook. Keep the Feature Edge v8 deliverable separate until a verified binary is available for a merge.

## Read-only archive retrieval discovery

A read-only inspection of the private archive repository's workflow definition identified the storage path for the missing raw season payloads:

- Workflow: `.github/workflows/footystats-private-historical-ingestion.yml` in `dtnzv5by8c-ship-it/oracle-football-data`, source commit `cb89e5bd1c24810fe821a6b2c3c2c1c19272b381` ([workflow source](https://github.com/dtnzv5by8c-ship-it/oracle-football-data/blob/cb89e5bd1c24810fe821a6b2c3c2c1c19272b381/.github/workflows/footystats-private-historical-ingestion.yml)).
- Artifact name: `footystats-private-historical-ingestion`; configured retention: **90 days**.
- The workflow writes per-season `matches.json`, `teams.json`, `tables.json` and `season_stats.json` into `footystats-private-historical-ingestion.zip`, and its summary explicitly says raw payloads are saved only in the private Actions artifact, not in Git.
- The exact existing workflow run ID / artifact ID is not present in the governed research evidence available to this run. No artifact download, workflow dispatch, ingestion rerun or provider/API call was made.

**Next recovery action:** obtain the exact existing run/artifact ID, download that artifact read-only, verify its archive lineage/hash, and extract only the 19 selected groups absent from the Run64 raw JSON extract. Do not rerun the ingestion workflow.

## Governance

- Provider/API credits: **0**; completed workflows rerun: **none**.
- Oracle V1.6 production logic, probabilities or calibration changed: **no**.
- `production_eligible=false`; `betting_eligible=false`.

## Output

- Workbook: `Oracle_Selected50_Final_Readiness_Visual_Intelligence_31Oct2026_v9_Team_H2H_Time_Decay.xlsx`
- Workbook SHA-256: `190d294803e479a5b97dd2c9e751153c480ac8455bf05b14d3176ff3eec0a738`
- Size: 15,745,029 bytes; sheets: 62.
- Base workbook SHA-256: `75774dcf45d8228d4a3f403a2b6a7c6200631603830a4420897dd236be808df9`.

## Next priority

Obtain the exact existing private archive workflow run/artifact ID and recover the 19 missing groups read-only. Separately, before selecting a half-life for predictive use, require a leakage-safe chronological out-of-sample sensitivity test with verified point-in-time feature availability; do not alter Oracle V1.6 based on these descriptive profiles.
