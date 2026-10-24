# Project Oracle — Actual-Artifact Replay and Coverage Audit

**Audit date:** 22 October 2026  
**Scope:** Public research repository and archived Run #107 artifact only. No production logic or probabilities changed.

## Executive result

- Archived schedule: **244 fixtures across 26 league codes**. The fixture manifest declares a 27-league universe.
- Run #107 prediction manifest: **234 eligible fixtures** and **10 excluded** for `MISSING_PREMATCH_TEAM_STATE`.
- Kickoff times populated in the schedule: **79/244**; **165 missing**.
- All **13,099/13,099** prematch-state rows were mapped to a league code using an explicit 27-code → league-name crosswalk derived from archived `matches.csv`.
- **Verified alias count: 0.** The schedule has no stable home/away team IDs. IDs attached to historical labels do not independently prove that a schedule label maps to that historical team.
- An exact-label replay of the archived schedule and prematch state, with no aliases, found **146/244** fixtures with both role states and **98/244 blocked**. This research diagnostic is stricter than the production runner and does not reproduce production eligibility: the Run #107 manifest reports 234 eligible and 10 excluded. The difference demonstrates that production canonicalization/state resolution is not yet replicated in the research harness.
- The fixture-level report must keep the manifest baseline and exact-label diagnostic separate. With no independently verified aliases, **zero excluded fixtures are declared recovered**.

## Ten excluded fixtures

| Fixture | Missing role(s) | Candidate historical role-state evidence | Decision |
|---|---|---|---|
| Ligue 2 — Pau FC vs Grenoble (23 Oct) | Home | Pau: 24 home-role rows; latest 2026-09-18. Current-match archive has ID 6355 for historical label “Pau”, but the schedule has no corresponding team ID. | Blocked; candidate only |
| Eerste Divisie — Almere City vs Roda (23 Oct) | Home + away | Almere City FC: 22 home-role rows; Roda JC Kerkrade: 26 away-role rows. Neither candidate has an exact label in the current-match ID archive. | Blocked; candidate only |
| Eerste Divisie — Jong AZ vs Helmond (23 Oct) | Home + away | Jong AZ Alkmaar: 27 home-role rows; Jong PSV: 27; Jong Ajax: 26. Helmond Sport: 25 away-role rows. | Blocked; Jong AZ identity ambiguous |
| Eerste Divisie — Oss vs Jong Ajax (23 Oct) | Home | TOP Oss: 25 home-role rows. | Blocked; candidate only |
| Belgian Pro League — Westerlo vs Beveren (24 Oct) | Away | SK Beveren: **3 usable away-role rows**; current-match archive ID 8475 exists for “SK Beveren”. Schedule still lacks a matching team ID. | Blocked; minimum-history rule not found |
| Czech First League — Brno vs Bohemians (24 Oct) | Home | Artis Brno: 4 home-role rows; FC Zbrojovka Brno: 4. Bohemians 1905: 26 away-role rows. | Blocked; ambiguous and low history |
| Eerste Divisie — Dordrecht vs Venlo (24 Oct) | Home + away | FC Dordrecht: 26 home-role rows; VVV-Venlo: 27 away-role rows. No exact candidate labels in the current-match ID archive. | Blocked; candidate only |
| Ekstraklasa — Wisla vs Rakow (24 Oct) | Home + away | Wisła Płock and Wisła Kraków are both plausible; Raków Częstochowa has 26 away-role rows. Current-match IDs exist for the two Wisła clubs and Raków, but the schedule has no source IDs to connect the labels safely. | Blocked; ambiguous Wisła identity |
| 2. Bundesliga — Braunschweig vs Hannover (25 Oct) | Home | Eintracht Braunschweig: 24 home-role rows; Hannover 96: 24 away-role rows. Current-match IDs exist for these historical labels, not for the schedule labels. | Blocked; candidate only |
| Eredivisie — PSV vs Feyenoord (25 Oct) | Home | PSV Eindhoven: 23 home-role rows; Feyenoord: 26 away-role rows. Current-match IDs exist for these historical labels, not for the schedule labels. | Blocked; candidate only |

Candidate history counts are diagnostic, not alias approvals. The replay excludes state rows dated on or after the fixture date and requires nonzero history in the appropriate role.

## Identity and minimum-history decisions

- **Jong AZ:** do not confuse Jong AZ Alkmaar with Jong Ajax or Jong PSV. Block until a stable source/team ID and competition evidence identify the scheduled club.
- **Brno:** keep blocked. Artis Brno and FC Zbrojovka Brno are competing candidates with only four usable home-role rows each.
- **Wisła:** keep blocked. Wisła Płock and Wisła Kraków are distinct clubs.
- **Beveren:** repository research documentation does not define a governed minimum-history threshold. Three usable away-role records cannot be declared sufficient or insufficient by guessing; obtain the documented policy and keep this fixture blocked meanwhile.
- Other single candidates remain unapproved until the schedule label can be tied to the candidate through source IDs or equivalent authoritative evidence plus competition/date/opponent checks.

## League coverage and kickoff times

- **Missing league code: RSA — South African Premier Division.** The fixture ingest manifest labels it `NO_FIXTURES_IN_WINDOW`. Confirm whether there truly were no fixtures in the window or whether source coverage failed; do not silently claim complete 27-league coverage.
- **165/244 fixtures lack kickoff time**; 79 have one. Time-to-kickoff, within-day chronology, and any feature requiring kickoff ordering must remain blocked for rows without verified timing evidence.
- The ingest manifest records successful official kickoff enrichment for some competitions (including the Premier League), while the final schedule still has many blanks. Available evidence does not provide complete per-fixture provenance for the 165 missing values. Do not infer times from date-only matches.

## Acceptance gates

1. Obtain source team IDs for scheduled fixtures (or an authoritative competition-specific fixture feed mapping), and tie them to historical IDs using competition, date, opponent and source provenance.
2. Obtain the governed minimum-history policy; keep SK Beveren blocked until its three away-role records are evaluated against that rule.
3. Re-run the isolated replay with only independently verified aliases; compare fixture-level role readiness and guard against future-dated state leakage.
4. Reconcile all 27 leagues, especially RSA, and produce per-fixture kickoff provenance: source, source fixture ID, UTC timestamp, timezone and exact match criteria.
5. Add regression tests for the confirmed root cause, run research CI, review real-data outputs, and only then recommend a permanent fix for review.

## Governance

- Production model logic, weights, probabilities, calibration, thresholds and selection rules: **unchanged**.
- Confirmed production recoveries: **0**.
- Research PR #20: **open, draft, unmerged**.
- Research CI Run #65 passed compilation and synthetic tests; this is not proof that real-data identity recovery works.

## Evidence

- [Run #107 artifact and completion evidence](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39772347617)
- [Research CI Run #65](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39828395156)
- [PR #20 — draft, unmerged](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/20)
- [Corrected ten-fixture role-state audit](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/oracle-ten-fixture-corrected-role-state-audit-2026-10-22.md)
