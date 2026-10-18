# Oracle H2H Source-Gap Register

**As-of:** 2026-10-17  
**Latest reference audit:** [H2H workflow run #18](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39053245770)  
**Scope:** reporting/source coverage only. No production model changes or Oracle probability changes.

## Latest audit summary

- Upcoming fixtures processed: 113
- Exact canonical Fixture ID joins: 113/113 (100%); fuzzy matching: not used
- Fixtures with historical H2H meetings: 84
- Unresolved team/league archive mappings: 16
- Fixtures with no prior meeting found in the available archive: 13
- Fixtures with at least five H2H meetings: 53
- Fixtures with 1UP truth records: 24
- Historical archive: 75,104 rows; date range 2018-07-20 to 2026-10-17
- Archive merge duplicate keys: 0; source extension acquisition errors: 0
- H2H quality status: `PASS_WITH_REVIEW_ITEMS`

The successful exact-ID join confirms that each upcoming fixture has a report row. It does not mean every fixture has historical meetings or that source coverage is complete. “No prior meeting found” is bounded by the archive's available coverage and is not proof the clubs have never played.

## Current unresolved team/league mappings (16)

These are the exact current rows in `h2h_unmatched_fixtures.csv` from Run #18. The report diagnoses a team missing from the archive under the fixture's current league code; it does not establish whether the cause is an alias, a league/season coverage gap, a competition mismatch, or absent source history.

| Fixture date | League | Home team | Away team | Team(s) not found in this league archive |
|---|---|---|---|---|
| 2026-10-18 | CZE | Slovacko | Brno | Brno |
| 2026-10-18 | E0 | Leeds | Manchester Utd | Manchester Utd |
| 2026-10-18 | E0 | Nottingham | Arsenal | Nottingham |
| 2026-10-18 | NED2 | Maastricht | Heracles | Maastricht |
| 2026-10-18 | NED2 | Waalwijk | FC Volendam | Waalwijk |
| 2026-10-18 | POL | Zaglebie | Jagiellonia | Zaglebie; Jagiellonia |
| 2026-10-18 | ROU | Univ. Craiova | Farul Constanta | Farul Constanta |
| 2026-10-18 | SP2 | Ceuta | Oviedo | Ceuta |
| 2026-10-18 | SP2 | Granada CF | Cadiz CF | Granada CF; Cadiz CF |
| 2026-10-18 | T1 | Kasimpasa | Samsunspor | Kasimpasa |
| 2026-10-19 | NED2 | Jong Utrecht | Roda | Jong Utrecht; Roda |
| 2026-10-19 | POL | Wisla Plock | Radomiak Radom | Wisla Plock |
| 2026-10-19 | ROU | U. Cluj | FC Arges | U. Cluj; FC Arges |
| 2026-10-20 | E2 | AFC Wimbledon | Mansfield | AFC Wimbledon |
| 2026-10-20 | E2 | Burton | Bradford City | Bradford City |
| 2026-10-20 | E2 | Cambridge Utd | Wycombe | Cambridge Utd |

## No prior H2H found within available archive (13)

These are kept distinct from unresolved mappings because both clubs were found in the relevant league archive, but no prior meeting was found in the available coverage window.

| Fixture date | League | Home team | Away team |
|---|---|---|---|
| 2026-10-17 | ROU | FC Rapid Bucuresti | Corvinul |
| 2026-10-18 | I2 | Sampdoria | Arezzo |
| 2026-10-18 | SP1 | Malaga | Real Sociedad |
| 2026-10-18 | SP1 | Osasuna | Racing Santander |
| 2026-10-18 | SP2 | Burgos CF | Sabadell |
| 2026-10-18 | SP2 | Girona | Andorra |
| 2026-10-19 | E0 | Tottenham | Coventry |
| 2026-10-19 | UKR | FC Kharkiv | Liviy Bereh |
| 2026-10-20 | E1 | Wolves | Portsmouth |
| 2026-10-20 | E2 | Bromley | Leicester |
| 2026-10-20 | E2 | Notts County | Sheffield Wed |
| 2026-10-20 | E3 | Rotherham | Newport |
| 2026-10-20 | E3 | York City | Accrington |

## Required root-cause checks

1. **Team alias versus missing history:** inspect canonical names actually present in the same league archive before adding an alias. If the team has no rows in that league, an alias alone cannot restore missing history.
2. **Competition and season:** verify the source fixture's competition and season. Do not auto-reassign a fixture based on a same-named pair in another league.
3. **Coverage:** compare league/season match counts and dates against an independent source. Successful FotMob acquisition with zero request errors is not independent completeness validation.
4. **H2H temporal validity:** only include meetings completed before the target fixture's kickoff.
5. **Before/after audit:** any alias or source correction must be independently supported and must not create cross-league contamination.

## Permanent handling rules

- Preserve raw source team names and league codes for auditability.
- Add aliases only when the provider's canonical identity and competition/season are verified.
- Do not use fuzzy matching, silently reassign a fixture to another league, or promote a zero-match result as “no H2H ever.”
- On every run, report source row counts, league/season coverage, unresolved mappings, no-meeting cases, and exact-ID join coverage.
- Keep canonical upcoming-fixture IDs separate from H2H history selection. H2H history must be selected only from prior completed matches in the same verified competition.

## League/team audit status — 2026-10-18

See [LEAGUE_TEAM_VALIDATION_READINESS.md](LEAGUE_TEAM_VALIDATION_READINESS.md) for the detailed league × market and team alignment evidence. Production Oracle accuracy by league/team remains data-gated: the canonical settlement ledger is header-only and the 210-row prediction batch is explicitly marked CHALLENGER. The August 2026 research export has 606 rows marked PREDICTED across 27 league codes but lacks immutable per-row prediction timestamps and feature snapshot hashes; use only as descriptive research evidence. The corrected rolling and scorecard workflow is [Run #27](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39104920282).

## Predictive-value test status

**NOT TESTABLE from the currently verified canonical ledgers.** The private repository's canonical `archive/SETTLEMENT_LEDGER.csv` is header-only, and its current main prediction ledger has no verified historical prediction/outcome pairing. No hit-rate lift, Brier-score, log-loss, or calibration improvement should be claimed until immutable pre-kickoff predictions are linked to verified settled outcomes. Do not fabricate historical predictions or backfill synthetic settlements.


## Run #20 follow-up — 2026-10-17

The [successful Run #20](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39054874140) refreshed the exact-ID join to 112/112 fixtures (100%). The H2H archive remained at 75,104 rows with zero duplicate keys after merge and zero source-acquisition errors. Coverage review remains open: 16 team/league mapping cases and 13 fixtures with no prior meeting found in the available archive. The updated diagnostic CSV now records other league codes where each team appears, but those cross-league records are investigative clues only—not permission to merge cross-competition history.

The development-only challenger settlement audit scored 200/210 prediction rows (95.24%). Ten rows were left unscored because exact result records were absent for two fixture identities: Borussia Dortmund–Werder Bremen on 2026-10-09 and Mainz 05–Bayer Leverkusen on 2026-10-10 (five markets per fixture). Verify these fixtures and results independently before deciding whether the issue is a fixture-feed problem or missing result history.

The preliminary settled metrics by market are recorded in [H2H_INTEGRATION_AND_BACKTEST_STATUS.md](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/H2H_INTEGRATION_AND_BACKTEST_STATUS.md). They are descriptive challenger metrics only; no claim of H2H incremental lift, calibrated probabilities, profitability, or production readiness is supported yet.


## Verified Run #21 update — 2026-10-17

[Run #21](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39071598767) completed successfully. [Artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39071598767/artifacts/12116055163).

- Upcoming fixture window: 2026-10-18 through 2026-10-20; 92 fixtures.
- Exact canonical Fixture ID join: 92/92 (100%); no fuzzy matching; Oracle probabilities and production logic unchanged.
- Historical archive: 75,104 rows, 2018-07-20 through 2026-10-17; 62,268 extension rows added; zero rejected rows, duplicate keys, or acquisition errors.
- Current audit: 16 unresolved team/league mappings (17.39%, below the 20% workflow gate) and 12 fixtures with no prior meeting found in the available archive. These are separate states; neither should be silently remapped or described as proof of no historical meeting ever.
- Verified sourced reconciliation corrected the ten missing shadow settlement rows across Dortmund–Werder (2-2, 2026-10-09) and Mainz–Leverkusen (3-4, 2026-10-10). Shadow settlement is now 210/210 (100%) with zero chronology failures.

The 16 unresolved mappings remain open. Cross-league appearances are diagnostic clues only, not authorization to combine competitions. The archive's successful ingestion and freshness checks do not prove complete independent coverage for every league/season. H2H predictive-value testing remains blocked by the absence of verified historical outcome pairings in the canonical settlement ledger; do not claim H2H incremental lift from the challenger metrics.


## Historical validation readiness audit — 2026-10-18

See [H2H_VALIDATION_READINESS.md](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/main/H2H_VALIDATION_READINESS.md) for the verified inventory of prediction/settlement artifacts and the root cause blocking incremental H2H testing. In particular, the reporting runner is read-only against the governed private source, so repeated reporting runs do not accumulate new canonical predictions or settlements. Do not manufacture historical prediction rows from final scores or aggregate OOS metrics. Keep the with-H2H versus without-H2H comparison blocked until paired immutable pre-kickoff prediction arms and verified outcomes exist.


## Run #25 research result and next coverage requirement

Run #25 succeeded: [workflow](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39077017138), [artifact](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39077017138/artifacts/12117373764). The 27-league historical-score experiment had 74,999 valid unique matches, 71,176 training rows and 3,823 holdout rows. Best exploratory metrics: Over 2.5 logistic/all-features accuracy 57.55% (Brier 0.24241); 1X2 logistic/all-features accuracy 47.89% (balanced accuracy 41.32%); BTTS accuracy 54.17% versus 55.19% majority baseline, despite slightly improved Brier/log loss; total-goals MAE 1.3349; home-goals MAE 0.9837; away-goals MAE 0.8809.

Important limitation: these are research models built from historical results and engineered features, not fixture-level historical Oracle predictions. This run does not identify which individual teams aligned with Oracle's actual forecasts. To complete the requested team alignment audit, acquire a fixture-level historical Oracle prediction export with prediction probabilities/market selections and verified outcomes, exact fixture/team/league IDs, and prediction-before-kickoff timestamps. The current prospective shadow set has only 42 fixtures, so per-league samples of roughly 2–5 fixtures per market are too small for durable team or league rankings.
