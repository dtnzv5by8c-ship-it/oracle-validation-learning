# Project Oracle — Official Fixture Cross-Check for Ten Missing Team-State Records

**Audit date:** 23 October 2026  
**Scope:** Research-only cross-check of the ten Run #107 fixtures excluded as `MISSING_PREMATCH_TEAM_STATE`. This report does not change the fixture CSV, aliases, prediction rows, or production model.

## Executive result

Public official club/league pages corroborate the scheduled dates and times for most of the ten fixtures. Two identity clarifications are especially useful:

- The Czech fixture is **FC Zbrojovka Brno vs Bohemians Praha 1905** (not enough evidence to select the historical state label solely from the short schedule label “Brno”; the official fixture identifies the current opponent, but a source team ID is still needed for a safe historical crosswalk).
- The Polish fixture is **Wisła Kraków vs Raków Częstochowa**, not Wisła Płock vs Raków. The official Ekstraklasa schedule settles which Wisła club is playing Raków on 24 October. This is strong competition-fixture identity evidence, but it must still be joined to a stable team ID before applying a state alias.

**No missing prediction fixture is declared recovered by this cross-check.** It verifies public fixture metadata, not the production runner’s internal team-state identity or minimum-history eligibility.

## Fixture evidence

Times below are published local competition/club times. Do not convert them to UTC without preserving the source timezone.

| Schedule label in Run #107 | Official fixture / local time | Source | Research decision |
|---|---|---|---|
| Pau FC vs Grenoble — 23 Oct | Pau vs Grenoble, Friday 23 Oct, 20:00 | https://www.paufc.fr/calendrier | Date/time corroborated. “Pau” remains a candidate historical label; verify stable team ID before alias. |
| Almere City vs Roda — 23 Oct | Almere City FC vs Roda JC, Friday 23 Oct, 20:00 | https://business.almerecity.nl/ | Date/time corroborated. Both historical label candidates still need identity evidence. |
| Jong AZ vs Helmond — 23 Oct | Jong AZ vs Helmond Sport, Friday 23 Oct, 20:00 | https://az.nl/wedstrijden/wedstrijden/keuken-kampioen-divisie/jong-az-helmond-sport-23-10-2026 | Date/time corroborated. Do not confuse Jong AZ with Jong Ajax/Jong PSV; identity still needs a source ID. |
| Oss vs Jong Ajax — 23 Oct | TOP Oss vs Jong Ajax, Friday 23 Oct, 20:00 | https://toposs.nl/nieuws/concept-competitieprogramma-2026-2027 | Date/time corroborated. TOP Oss is the likely historical label; verify ID before alias. |
| Westerlo vs Beveren — 24 Oct | Pro League page says 18:45; SK Beveren travel notice says 20:45 | https://www.proleague.be/wedstrijden/seizoen-2026-2027-jupiler-pro-league-9-kvc-westerlo-vs-sk-beveren-676 ; https://www.skbeveren.be/2026/10/westerlo-away-26/ | **Conflicting time evidence. Keep kickoff blocked pending authoritative timezone/schedule reconciliation.** SK Beveren has only 3 usable away-role history rows in the archive; governed minimum-history policy is also needed. |
| Brno vs Bohemians — 24 Oct | FC Zbrojovka Brno vs Bohemians Praha 1905, Saturday 24 Oct, 15:00 | https://bohemians.cz/zapasy/MUZ/ | Official fixture confirms the named current club. Keep historical alias blocked until stable ID and role-history minimum are confirmed; competing historical labels each have only 4 home-role rows. |
| Dordrecht vs Venlo — 24 Oct | FC Dordrecht vs VVV-Venlo, Saturday 24 Oct, 16:30 | https://omroepwest.voetbal.nl/ | Date/time corroborated. Historical label candidates need source ID confirmation. |
| Wisla vs Rakow — 24 Oct | Wisła Kraków vs Raków Częstochowa, Saturday 24 Oct, 20:15 | https://ekstraklasa.org/en/news/pko-bp-ekstraklasa-202627-matchweek-12-schedule/ ; https://ekstraklasa.org/en/clubs/wisa-krakow/?season=2026-2027 | Official schedule resolves the short label “Wisla” to **Wisła Kraków** for this fixture. Use as review evidence for the crosswalk; do not automatically apply alias without stable ID evidence. |
| Braunschweig vs Hannover — 25 Oct | Eintracht Braunschweig vs Hannover 96, Sunday 25 Oct, 13:30 | https://www.eintracht.com/news/artikel/vorverkaufsinfos-zum-niedersachsenderby-gegen-hannover | Date/time corroborated. Historical label candidate still needs stable ID confirmation. |
| PSV vs Feyenoord — 25 Oct | PSV vs Feyenoord, Sunday 25 Oct, 14:30 | https://www.psv.nl/en/match-center | Date/time corroborated. “PSV Eindhoven” remains a candidate historical label; verify ID before alias. |

## What this changes

1. The date-only schedule is now supported by official/public fixture evidence for these named matches.
2. “Brno” and “Wisla” should not be treated as generic fuzzy-name matches. Official fixture pages identify FC Zbrojovka Brno and Wisła Kraków respectively, but historical state mapping still needs a source-ID join or reviewed equivalent evidence.
3. The Westerlo–SK Beveren kickoff conflict is a concrete data-quality issue; the current two sources disagree by two hours. Do not guess which is correct or write either value into the production schedule until the source timezone/official schedule is reconciled.
4. The archive’s missing kickoff values remain a broader issue beyond these ten fixtures. This report does not claim to solve the other 155+ missing kickoff times across the full schedule.
5. Historical state counts remain diagnostic only. The role-history rule and governed minimum sample size must be applied consistently; three away-role rows for SK Beveren cannot be declared sufficient without that policy.

## Required next actions

1. Obtain the fixture-provider/source IDs for each scheduled team and match them to historical IDs and competition IDs.
2. Confirm the authoritative kickoff and timezone for Westerlo–SK Beveren.
3. Locate the governed minimum-history policy; keep Beveren and Brno blocked until it is satisfied.
4. Run the real archived schedule/state replay with only explicitly reviewed identity mappings and strict pre-fixture date cutoffs.
5. Save fixture-by-fixture before/after eligibility and reconcile against the 234 predicted / 10 excluded manifest baseline.
6. Add regression tests for confirmed mappings and edge cases, run research CI, and publish evidence.
7. Keep production untouched and PR #20 draft/unmerged until review and explicit approval.

## Governance

- Confirmed production recoveries from this audit: **0**.
- Approved aliases from fuzzy matching: **0**.
- Production model logic/probabilities/calibration/thresholds: **unchanged**.
- PR #20: remains draft and unmerged.
