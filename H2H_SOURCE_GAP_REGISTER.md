# Oracle H2H Source-Gap Register

**As-of:** 2026-10-17  
**Reference audit:** [H2H workflow run #17](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39047414354)  
**Scope:** reporting/source coverage only. No production model changes.

## Audit summary

- Fixtures processed: 149
- Fixtures with H2H meetings: 107
- Unmatched source fixtures: 23
- Fixtures with no prior meeting found in the available archive: 19
- H2H audit status: `PASS_WITH_REVIEW_ITEMS`
- Unmatched rate: 15.44% (below the 20% threshold, but not evidence of complete coverage)

These categories are intentionally separate. “No prior meeting found” is bounded by archive coverage and must not be presented as proof the teams have never played.

## Unmatched records requiring source investigation

### Possible league-code/competition mismatch — do not auto-reassign

| Current league code | Fixture | Why it is flagged | Required verification |
|---|---|---|---|
| E0 | Fulham vs Hull | Same normalized pair appears in E1 history | Verify actual competition and fixture source for this date |
| SP2 | Eibar vs Mallorca | Same normalized pair appears in SP1 history | Verify actual competition and fixture source for this date |

No competition reassignment or cross-league history join is permitted until the fixture's competition is independently verified.

### Team absent from the historical archive for the reported league

| League code | Fixture |
|---|---|
| E1 | Bristol City vs Sheffield United |
| E2 | Barnsley vs Cambridge United |
| E2 | Bradford City vs Stevenage |
| E2 | Sheffield Wednesday vs AFC Wimbledon |
| E2 | AFC Wimbledon vs Mansfield Town |
| E2 | Burton Albion vs Bradford City |
| E2 | Cambridge United vs Wycombe Wanderers |
| NED2 | FC Emmen vs Almere City |
| NED2 | MVV Maastricht vs Heracles Almelo |
| NED2 | RKC Waalwijk vs FC Volendam |
| NED2 | Jong FC Utrecht vs Roda JC |
| CZE | 1. FC Slovacko vs Zbrojovka Brno |
| E0 | Leeds United vs Manchester United |
| E0 | Nottingham Forest vs Arsenal |
| POL | Zaglebie Lubin vs Jagiellonia Bialystok |
| POL | Wisla Plock vs Radomiak Radom |
| ROU | Universitatea Craiova vs Farul Constanta |
| ROU | Universitatea Cluj vs FC Arges |
| SP2 | AD Ceuta vs Real Oviedo |
| SP2 | Granada vs Cadiz |
| T1 | Kasimpasa vs Samsunspor |

This diagnosis means at least one normalized team name was not found in the archive under the fixture's current league code. It does **not** prove the team name is wrong or the league history does not exist.

## Permanent handling rules

1. Preserve each raw source team name and league code for auditability.
2. Add aliases only when verified against the provider's canonical team identity and competition/season.
3. Do not use fuzzy matching, silently reassign a fixture to another league, or promote a zero-match result as “no H2H ever.”
4. On each run, report source row counts, source/season coverage, unmatched fixtures, no-meeting fixtures, and per-league exact-ID join coverage.
5. Keep fixture identity and H2H history joins separate: canonical fixture IDs identify the upcoming fixture; H2H history is selected only from prior completed matches in the same verified competition.
6. Re-run the coverage audit after a source or alias change and retain before/after counts. A fix is accepted only if it resolves a verified root cause without creating cross-league contamination.

## What is not yet resolved

The above records are diagnosed but not all source gaps have been repaired. The available evidence does not justify automatic alias edits or competition changes. The 19 no-prior-meeting fixtures should remain explicitly marked as no meeting found in archive coverage until historical coverage is verified.

See also: [Integration and backtest status](H2H_INTEGRATION_AND_BACKTEST_STATUS.md).
