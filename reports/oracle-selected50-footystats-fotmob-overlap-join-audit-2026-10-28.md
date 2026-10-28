# Selected-50 FootyStats–FotMob and Historical-Ledger Join Audit — 2026-10-28

## Outcome

The read-only audit used the existing private FootyStats archive, the existing FotMob current-match snapshot, and the existing Oracle historical match ledger. It made **no provider API calls** and made no production writes.

It found:
- **10 exact FootyStats–FotMob fixture/team/UTC-kickoff joins** across two selected leagues.
- **577 FootyStats–historical-ledger team-pair + date joins** across 24 selected competitions. These have date precision only; they do not prove exact kickoff time.
- **24 strong research-only canonical league-code candidates** with 587 total joined records across the two source paths.
- **Two strong FotMob league-ID candidates**, one with a source conflict.
- **Zero approved canonical bridges**. All candidate rows remain human-review-only.

The current source manifest remains stale: generated 2026-10-06 07:49 UTC, covering requests only through 8 October.

## FotMob bridge candidates

| Selected competition | FootyStats season ID | Observed FootyStats master ID | Candidate FotMob league ID | Exact fixture joins | Completed score agreements | Source conflicts | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
| Canada — Canadian Premier League | 16741 | 524 | 1000001192 | 4 | 3 | 1 | Strong candidate; human review required |
| England — EFL League One | 17180 | 6 | 938219 | 6 | 3 | 0 | Strong candidate; human review required |

The Canadian bridge has three completed score agreements and one material score/status conflict. England has three completed score agreements and three fixtures where both sources indicate postponed/suspended status; those are not settled 0–0 results.

## Exact FootyStats–FotMob joins

| FotMob league ID | FotMob match ID | UTC kickoff | Fixture | FotMob score | FootyStats season ID | FootyStats match ID | FootyStats score/status | Result |
|---:|---:|---|---|---|---:|---:|---|---|
| 1000001192 | 1000008711 | 2026-09-30 23:00 | Atlético Ottawa vs Cavalry FC | 3–2 | 16741 | 8465230 | 3–2 / complete | Score/status agree |
| 1000001192 | 1000008713 | 2026-10-03 20:00 | Forge FC vs HFX Wanderers FC | 3–3 | 16741 | 8465240 | 3–3 / complete | Score/status agree |
| 1000001192 | 5175979 | 2026-10-04 20:00 | Supra du Québec vs Pacific FC | 5–0 | 16741 | 8465202 | 5–0 / complete | Score/status agree |
| 1000001192 | 1000008675 | 2026-10-07 23:00 | Forge FC vs Pacific FC | 0–0, unfinished | 16741 | 8465167 | 3–0 / complete | **Conflict — quarantine from settlement** |
| 938219 | 5837184 | 2026-10-03 14:00 | Barnsley vs Milton Keynes Dons | PP / postponed | 17180 | 8565639 | 0–0 / suspended | Statuses align; not a settled result |
| 938219 | 5837186 | 2026-10-03 14:00 | Bromley vs Wycombe Wanderers | PP / postponed | 17180 | 8565337 | 0–0 / suspended | Statuses align; not a settled result |
| 938219 | 5837191 | 2026-10-03 14:00 | Peterborough United vs Notts County | PP / postponed | 17180 | 8565333 | 0–0 / suspended | Statuses align; not a settled result |
| 938219 | 5837187 | 2026-10-03 14:00 | Burton Albion vs Huddersfield Town | 1–3 / FT | 17180 | 8565677 | 1–3 / complete | Score/status agree |
| 938219 | 5837192 | 2026-10-03 14:00 | Reading vs Bradford City | 1–1 / FT | 17180 | 8565598 | 1–1 / complete | Score/status agree |
| 938219 | 5837188 | 2026-10-03 14:00 | Leyton Orient vs Plymouth Argyle | 0–2 / FT | 17180 | 8565602 | 0–2 / complete | Score/status agree |

## Historical-ledger canonical-code candidates

The historical Oracle ledger uses a short `league_code` namespace (for example `E0`, `I1`, `N1`). These values are not automatically equivalent to the longer research canonical candidate IDs (for example `ENG_E0`, `ITA_I1`). Exact ordered home/away team names and UTC calendar date matched; the historical ledger does not provide kickoff precision in this file. All rows below require human review.

| Country | Selected competition | FootyStats season ID | Master ID observed | Historical ledger code candidate | Team/date joins | Score agreements | Conflicts |
|---|---|---:|---:|---|---:|---:|---:|
| Italy | Serie A | 17084 | 193 | I1 | 40 | 40 | 0 |
| Croatia | Prva HNL | 17087 | 82 | CRO | 8 | 8 | 0 |
| Netherlands | Eredivisie | 17097 | 234 | N1 | 22 | 22 | 0 |
| France | Ligue 1 | 17102 | 130 | F1 | 27 | 27 | 0 |
| Poland | Ekstraklasa | 17112 | 259 | POL | 69 | 69 | 0 |
| France | Ligue 2 | 17117 | 132 | F2 | 44 | 44 | 0 |
| Switzerland | Super League | 17129 | 312 | SWZ | 30 | 30 | 0 |
| England | Premier League | 17146 | 9 | E0 | 10 | 10 | 0 |
| Scotland | Premiership | 17148 | 278 | SC0 | 35 | 35 | 0 |
| Czech Republic | First League | 17157 | 88 | CZE | 33 | 33 | 0 |
| Belgium | Pro League | 17171 | 1 | B1 | 13 | 13 | 0 |
| England | EFL League One | 17180 | 6 | E2 | 10 | 10 | 0 |
| Austria | Bundesliga | 17181 | 40 | AUT | 23 | 23 | 0 |
| England | Championship | 17184 | 103 | E1 | 13 | 13 | 0 |
| Ukraine | Ukrainian Premier League | 17191 | 328 | UKR | 6 | 6 | 0 |
| Spain | La Liga | 17199 | 3 | SP1 | 13 | 13 | 0 |
| Germany | Bundesliga | 17210 | 143 | D1 | 15 | 15 | 0 |
| Germany | 2. Bundesliga | 17212 | 140 | D2 | 31 | 31 | 0 |
| Portugal | LigaPro | 17215 | 5 | POR2 | 7 | 7 | 0 |
| Romania | Liga I | 17247 | 265 | ROU | 21 | 21 | 0 |
| Turkey | Süper Lig | 17265 | 8 | T1 | 32 | 32 | 0 |
| Spain | Segunda División | 17269 | 299 | SP2 | 10 | 10 | 0 |
| Italy | Serie B | 17404 | 194 | I2 | 40 | 40 | 0 |
| South Africa | Premier Soccer League | 17444 | 290 | RSA | 25 | 25 | 0 |

**Interpretation:** 24 of 50 selected seasons have strong historical-ledger code candidates supported by 577 exact team/date joins and matching scores. This is materially stronger than display-name matching, but because the ledger match rows do not prove kickoff precision and the code namespace differs from the research candidate IDs, the candidates remain unapproved. Twenty-six selected seasons still have no supported historical-ledger code candidate in this audit.

## Join method and controls

- Current FotMob joins require normalized ordered home/away team names and exact UTC kickoff timestamp.
- Historical-ledger candidates require normalized ordered home/away team names and exact UTC calendar date; these are explicitly labelled date-only.
- No mapping is accepted from display league name alone.
- Scores are used as corroboration only when the FootyStats record is marked complete. Suspended/postponed 0–0 values are not counted as completed score agreements.
- FootyStats `comp_master_id` remains provider-side evidence, not an Oracle canonical ID.
- All candidates are marked production-ineligible pending human review.

## Current snapshot and audit artifact

- [Exact cross-provider join audit run 40644996669](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40644996669)
- [Sanitized artifact 12796818576](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40644996669/artifacts/12796818576)
- [FootyStats League Matches API documentation](https://footystats.org/api/documentations/match-schedule-and-stats)
- [FootyStats League Season API documentation](https://footystats.org/api/documentations/league-season-stats-teams)

## Gate status

- Provider identity: 50/50 season IDs and 50 distinct master IDs observed.
- Historical canonical-code candidates: 24/50 strong candidates; human approval pending.
- FotMob league-ID candidates: 2/50 strong candidates; human approval pending.
- Official settlement truth: one current Canadian source conflict unresolved; suspended fixtures excluded.
- Approved canonical bridges: 0/50.
- Production/betting eligibility: **NO-GO**.

No production repository, Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected registry, ledgers or governance were changed.
