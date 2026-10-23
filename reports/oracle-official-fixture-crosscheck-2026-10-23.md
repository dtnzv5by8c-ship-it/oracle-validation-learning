# Project Oracle — Official Fixture Cross-Check for Ten Missing Team-State Records

**Audit date:** 23 October 2026  
**Scope:** Research-only cross-check of the ten Run #107 fixtures excluded as `MISSING_PREMATCH_TEAM_STATE`. This report does not change the fixture CSV, aliases, prediction rows, or production model.

## Executive result

Official club/league fixture pages corroborate the date and time for most of the ten fixtures. A cross-check against the archived `current_matches.csv` also surfaced stable team IDs for three exact fixture rows:

- **Pau vs Grenoble:** home ID `6355`, away ID `9855`, 23 October 18:00 UTC (20:00 France local).
- **Westerlo vs SK Beveren:** home ID `10001`, away ID `8475`, 24 October 18:45 UTC (20:45 Belgium local).
- **Wisła Kraków vs Raków Częstochowa:** home ID `10265`, away ID `4024`, 24 October 18:15 UTC (20:15 Poland local).

These are meaningful identity evidence in the archived fixture source. However, the original upcoming schedule CSV has no team-ID columns, and the prematch-state table also lacks team IDs. The team-ID join must be made explicit and regression-tested before using it to recover production eligibility.

**No missing prediction fixture is declared recovered by this cross-check.** It verifies public fixture metadata and identifies useful source IDs; it does not yet prove the production runner’s internal team-state identity or minimum-history eligibility.

## Fixture evidence

Times below are published local times unless explicitly marked UTC.

| Schedule label in Run #107 | Official fixture / local time | Archived `current_matches.csv` ID evidence | Research decision |
|---|---|---|---|
| Pau FC vs Grenoble — 23 Oct | Pau vs Grenoble, Friday 23 Oct, 20:00 | Exact dated Ligue 2 row: Pau ID `6355`, Grenoble ID `9855`; source timestamp 18:00 UTC | Strong evidence that schedule “Pau FC” and historical label “Pau” refer to the fixture’s home team. Add explicit ID-backed mapping only in isolated research replay, then test. |
| Almere City vs Roda — 23 Oct | Almere City FC vs Roda JC, Friday 23 Oct, 20:00 | No matching dated Eerste Divisie row found in archived `current_matches.csv` | Date/time corroborated; both historical label candidates still need ID evidence. |
| Jong AZ vs Helmond — 23 Oct | Jong AZ vs Helmond Sport, Friday 23 Oct, 20:00 | No matching dated Eerste Divisie row found in archived `current_matches.csv` | Date/time corroborated. Do not confuse Jong AZ with Jong Ajax/Jong PSV; identity still needs a source ID. |
| Oss vs Jong Ajax — 23 Oct | TOP Oss vs Jong Ajax, Friday 23 Oct, 20:00 | No matching dated Eerste Divisie row found in archived `current_matches.csv` | Date/time corroborated. TOP Oss is the likely historical label; verify ID before alias. |
| Westerlo vs Beveren — 24 Oct | KVC Westerlo vs SK Beveren, Saturday 24 Oct, 20:45 Belgium local | Exact dated Belgian Pro League row: Westerlo ID `10001`, SK Beveren ID `8475`; source timestamp 18:45 UTC = 20:45 CEST | The apparent two-hour discrepancy is explained by timezone: the archived field is explicitly `date_utc`. Local kickoff is 20:45, consistent with SK Beveren’s travel notice. Away-role history remains only 3 usable rows; minimum-history policy is still required. |
| Brno vs Bohemians — 24 Oct | FC Zbrojovka Brno vs Bohemians Praha 1905, Saturday 24 Oct, 15:00 | No matching dated Czech First League row found in archived `current_matches.csv` | Official fixture confirms current club names, but historical alias remains blocked until stable IDs and minimum-history requirements are established. Candidate Brno labels each have only 4 home-role rows. |
| Dordrecht vs Venlo — 24 Oct | FC Dordrecht vs VVV-Venlo, Saturday 24 Oct, 16:30 | No matching dated Eerste Divisie row found in archived `current_matches.csv` | Date/time corroborated. Historical label candidates need source ID confirmation. |
| Wisla vs Rakow — 24 Oct | Wisła Kraków vs Raków Częstochowa, Saturday 24 Oct, 20:15 | Exact dated Ekstraklasa row: Wisła Kraków ID `10265`, Raków Częstochowa ID `4024`; source timestamp 18:15 UTC = 20:15 CEST | Official schedule and archive settle the short label “Wisla” as **Wisła Kraków**, not Wisła Płock, for this fixture. Use as ID-backed evidence in isolated research replay; do not silently modify production mapping. |
| Braunschweig vs Hannover — 25 Oct | Eintracht Braunschweig vs Hannover 96, Sunday 25 Oct, 13:30 | No matching dated 2. Bundesliga row found in archived `current_matches.csv` | Date/time corroborated. Historical label candidate still needs fixture-level ID confirmation. |
| PSV vs Feyenoord — 25 Oct | PSV vs Feyenoord, Sunday 25 Oct, 14:30 | No matching dated Eredivisie row found in archived `current_matches.csv` | Date/time corroborated. “PSV Eindhoven” remains a candidate historical label; verify ID before alias. |

## Source pages

- Pau FC official calendar: https://www.paufc.fr/calendrier
- Almere City ticketing / fixture page: https://business.almerecity.nl/
- AZ official fixture page: https://az.nl/wedstrijden/wedstrijden/keuken-kampioen-divisie/jong-az-helmond-sport-23-10-2026
- TOP Oss fixture calendar: https://toposs.nl/nieuws/concept-competitieprogramma-2026-2027
- Pro League match page: https://www.proleague.be/wedstrijden/seizoen-2026-2027-jupiler-pro-league-9-kvc-westerlo-vs-sk-beveren-676
- SK Beveren travel notice: https://www.skbeveren.be/2026/10/westerlo-away-26/
- Bohemians Praha 1905 official fixtures: https://bohemians.cz/zapasy/MUZ/
- Eerste Divisie schedule: https://omroepwest.voetbal.nl/
- Official Ekstraklasa schedule: https://ekstraklasa.org/en/news/pko-bp-ekstraklasa-202627-matchweek-12-schedule/
- Official Eintracht Braunschweig notice: https://www.eintracht.com/news/artikel/vorverkaufsinfos-zum-niedersachsenderby-gegen-hannover
- Official PSV match centre: https://www.psv.nl/en/match-center

## What this changes

1. Public fixture dates and local kickoff times are now corroborated for the named fixtures.
2. The Westerlo–SK Beveren time conflict is explained by timezone: archived `date_utc` is UTC, while the club notice uses Belgian local time. Use the UTC timestamp with timezone provenance, not an unlabelled local time.
3. The archived match source provides stable IDs for Pau/Grenoble, Westerlo/SK Beveren and Wisła Kraków/Raków. Those ID-backed rows can support an isolated crosswalk experiment, provided the alias is explicit and the prematch role history is checked before fixture date.
4. The other seven fixtures still need fixture-level source IDs or an equivalent reviewable identity chain. Do not use fuzzy name matching as a substitute.
5. Historical state counts remain diagnostic only. Three away-role rows for SK Beveren cannot be declared sufficient without the governed minimum-history policy.

## Required next actions

1. Implement a **research-only** explicit identity crosswalk for the three ID-backed fixture rows and replay against the archived state using strict pre-fixture cutoffs.
2. Keep the remaining seven fixtures blocked until stable source IDs or equivalent authoritative evidence are available.
3. Locate the governed minimum-history policy; keep Beveren blocked until the policy is applied.
4. Save fixture-by-fixture before/after eligibility and reconcile against the 234 predicted / 10 excluded manifest baseline.
5. Add regression tests for ID-backed mapping, unresolved identity, role-history minimums and temporal leakage; run research CI.
6. Keep production untouched and PR #20 draft/unmerged until review and explicit approval.

## Governance

- Confirmed production recoveries from this audit: **0**.
- Approved production aliases: **0**.
- Production model logic/probabilities/calibration/thresholds: **unchanged**.
- PR #20: remains draft and unmerged.
