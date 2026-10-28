# Selected-50 FootyStats–FotMob Overlap Join Audit — 2026-10-28

## Snapshot validation

The expanded 30-day-overlap snapshot was retrieved at `2026-10-28T06:19:09.645973+00:00` UTC and passed the offline snapshot contract validator.

- [Sanitized 30-day overlap snapshot artifact 12796207151](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12796207151)
- 50/50 season requests succeeded; 2,250 fixture/result rows in the 30-day lookback + 14-day future window.
- 871 upcoming fixtures in the next 14 days; 1,372 recent completed results in the previous 30 days.
- 19 suspended rows in the full window; 486 rows have `no_home_away=1` (181 future, 305 recent).
- No duplicate match IDs; all rows had home/away IDs, team names, kickoff timestamp, and `competition_id` matching the selected season ID.
- The snapshot contract validator returned **PASS**; production and betting eligibility remained `NOT_GRANTED`.

## Outcome

A read-only exact fixture join between the stale production FotMob staging snapshot and the fresh FootyStats 30-day overlap snapshot found **8 exact fixture/team/kickoff joins across 2 selected leagues**.

This is enough to create two strong *research-only bridge candidates*, but not to promote them to the protected canonical registry. The current FotMob source is stale, has no country/category field, and one joined Canadian fixture has a score/status conflict.

| Selected competition | FootyStats season ID | Observed FootyStats master ID | Candidate FotMob league ID | Exact fixture joins | Completed score matches | Source conflicts | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| Canada — Canadian Premier League | 16741 | 524 | 1000001192 | 4 | 3 | 1 | Strong candidate; human review required |
| England — EFL League One | 17180 | 6 | 938219 | 4 | 1 | 0 | Strong candidate; human review required |

## Exact joined evidence

| FotMob league ID | FotMob match ID | UTC kickoff | Fixture | FotMob score/status | FootyStats season ID | FootyStats match ID | FootyStats score/status | Result |
|---:|---:|---|---|---|---:|---:|---|---|
| 1000001192 | 1000008711 | 2026-09-30 23:00 | Atlético Ottawa vs Cavalry FC | 3–2 / FT | 16741 | 8465230 | 3–2 / complete | Score/status agree |
| 1000001192 | 1000008713 | 2026-10-03 20:00 | Forge FC vs HFX Wanderers FC | 3–3 / FT | 16741 | 8465240 | 3–3 / complete | Score/status agree |
| 1000001192 | 5175979 | 2026-10-04 20:00 | Supra du Québec vs Pacific FC | 5–0 / FT | 16741 | 8465202 | 5–0 / complete | Score/status agree |
| 1000001192 | 1000008675 | 2026-10-07 23:00 | Forge FC vs Pacific FC | score 0–0, unfinished flag / status blank | 16741 | 8465167 | 3–0 / complete | **Conflict — FotMob snapshot stale or inconsistent; do not use as settlement truth** |
| 938219 | 5837184 | 2026-10-03 14:00 | Barnsley vs Milton Keynes Dons | PP / postponed | 17180 | 8565639 | 0–0 / suspended | Statuses semantically align; not a settled result |
| 938219 | 5837186 | 2026-10-03 14:00 | Bromley vs Wycombe Wanderers | PP / postponed | 17180 | 8565337 | 0–0 / suspended | Statuses semantically align; not a settled result |
| 938219 | 5837187 | 2026-10-03 14:00 | Burton Albion vs Huddersfield Town | 1–3 / FT | 17180 | 8565677 | 1–3 / complete | Score/status agree |
| 938219 | 5837191 | 2026-10-03 14:00 | Peterborough United vs Notts County | PP / postponed | 17180 | 8565333 | 0–0 / suspended | Statuses semantically align; not a settled result |

## Join method

- Join key: normalized home team name + away team name + exact UTC kickoff timestamp.
- No join was accepted from display league name alone.
- FootyStats response `competition_id` matched the selected season ID in the schedule snapshot.
- The Canadian bridge has three settled score matches that agree and one material source conflict.
- The England bridge has one completed score match that agrees and three matching postponed/suspended fixtures.

## Interpretation and controls

1. **Candidate mapping only:** the observed FotMob IDs `1000001192` and `938219` are strong cross-source candidates for Canada CPL and England EFL League One, respectively. They are not yet production-approved bridges.
2. **Do not use the conflicting Canadian match as settlement truth.** The stale FotMob snapshot has an unfinished 0–0 row while FootyStats has 3–0 complete. This demonstrates why the stale feed must not be treated as current.
3. **Do not settle postponed matches as 0–0.** Both sources indicate postponement/suspension for the three England matches.
4. The existing FootyStats `comp_master_id` values (524 and 6) are source fields and must not be treated as Oracle canonical IDs.
5. The current production feed does not preserve country/category, and its ingestion logic is name-only. The identity-safe ingestion change and human review remain required.

## Gate status

- Exact overlap fixture joins: 8 across 2 selected leagues.
- Strong research-only FootyStats-to-FotMob bridge candidates: 2/50.
- Human-approved canonical bridges: 0/50.
- Official settlement truth verified for the conflicting Canadian fixture: no.
- Production/betting eligibility: NO-GO.

No production repository or model files were changed.
