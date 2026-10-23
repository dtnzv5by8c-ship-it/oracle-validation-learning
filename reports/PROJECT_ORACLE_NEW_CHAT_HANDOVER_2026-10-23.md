# Project Oracle — New Chat Handover and Expedite Plan
Prepared 23 October 2026 (South Africa, UTC+02:00). Owner: Nolan. Assistant: Gem.

## Governance — mandatory
- Work ONLY in public repository https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning
- Branch: research/oracle-crosswalk-isolation-2026-10-22
- PR #20: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/20 — open, draft, unmerged. Never merge without Nolan's explicit approval.
- Do not access or change private production repository. No production model logic, version, weights, probabilities, calibration, thresholds, selection rules or production eligibility changes.
- No paid API credits, no asking for secrets, no local installation required for Nolan. Do not invent IDs or approve fuzzy matches.
- Explain in simple terms. Prefer completing tasks through tools instead of asking Nolan to edit files. Do not claim background work; execute work in the current turn and show evidence.

## User's request and monitoring idea
Nolan asks to continue autonomously to completion, research official team names/fixture dates, save progress and provide a complete prompt for a new chat because this chat is slow. He suggests a visible dummy workflow when a build takes time. Prefer a meaningful research workflow that runs tests/replay and uploads evidence; do not use sleep-only or production runs just to show activity. Give the workflow URL and explain green means the tested research checks passed, not that production is fixed.

## Verified repository and CI state (recheck before editing)
- Public repo: dtnzv5by8c-ship-it/oracle-validation-learning; branch research/oracle-crosswalk-isolation-2026-10-22.
- Base main SHA: f86eaf2586e2d2dc7df73de773a0214116f231bb.
- PR #20 head SHA last observed 23 Oct: cd7a02ccc1fe981c8b2d3887825987a39ade5b3f; fetch current head before writing.
- Research CI Run #65 / ID 39828395156 passed compile and configured synthetic tests on commit 9032542896feb0cd513e431758ecbb60fdad0bea. URL: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39828395156. This is not proof of actual data recovery.
- Run #107 artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39772347617. Artifact oracle-fixture-level-predictions, ID 12425136901, expires 5 Nov 2026, source commit f86eaf2586e2d2dc7df73de773a0214116f231bb. ZIP SHA256: 5de8e3773934e2d53aa6464df31c03ee8d7a47bda98ad19ed39e590d28cb3299.
- Local copy in original chat was /mnt/data/oracle-fixture-level-predictions.zip; it may not exist in a new chat. Re-download from GitHub if possible.

## Built research-only scripts and reports
- scripts/test_oracle_league_failure_isolation.py: date gate, fixture/league failure isolation, duplicate fixtures, empty state/fixture safeguards.
- scripts/oracle_isolated_batch_runner.py: isolated league/batch runner and fail-closed preflight prototype; not integrated into production.
- scripts/oracle_reconcile_outputs.py and scripts/test_oracle_reconcile_cli.py: fixture/market output coverage, duplicates, probability bounds, PASS/FAIL/BLOCKED.
- scripts/oracle_team_alias_audit.py and scripts/test_oracle_team_alias_audit.py: candidate audit only; does not approve aliases.
- scripts/oracle_prematch_state_replay.py and scripts/test_oracle_prematch_state_replay.py: explicit league crosswalk and explicit reviewed aliases; rejects missing evidence/ambiguous aliases and excludes state rows dated on or after fixture date.
- Workflow .github/workflows/oracle-research-isolation-tests.yml.
- Corrected audit: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/oracle-ten-fixture-corrected-role-state-audit-2026-10-22.md
- Real reconciliation: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/oracle-real-artifact-reconciliation-2026-10-22.md
- Root cause: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/oracle-team-state-root-cause-research-2026-10-22.md

## Actual Run #107 findings
- 244 scheduled fixtures; schedule contains 26 league codes while manifest declares 27 leagues.
- 234 predicted fixtures; 5,148 rows = 234 × 22 markets. Ten fixtures excluded as MISSING_PREMATCH_TEAM_STATE.
- Kickoff time populated for 79/244; missing for 165.
- Prematch state: 13,099 rows. Historical matches archive: 12,836 rows, 27 league codes, 21 Mar 2025–20 Sep 2026.
- Strict exact-label diagnostic replay found 146/244 with both role states and 98 blocked, but this does not reproduce production eligibility (manifest says 234/244). Keep these metrics separate.
- Verified aliases approved: 0. Confirmed production recoveries: 0. 90% accuracy is not established. The four-model OOS file is research-only and not calibrated production output.

## Ten excluded fixtures and role-specific candidate history
Candidate counts below are pre-fixture and require nonzero home_n/away_n in the appropriate role; they are not approved mappings.
1. Ligue 2 — Pau FC vs Grenoble, 23 Oct: Pau 24 home rows; Grenoble 25 away rows. Historical label Pau has current-match ID 6355, but the schedule lacks a team ID.
2. Eerste Divisie — Almere City vs Roda JC, 23 Oct: Almere City FC 22 home rows; Roda JC Kerkrade 26 away rows.
3. Eerste Divisie — Jong AZ vs Helmond Sport, 23 Oct: Jong AZ Alkmaar 27 home rows, but Jong PSV 27 and Jong Ajax 26 also exist; Helmond Sport 25 away rows. Keep Jong AZ blocked pending identity evidence.
4. Eerste Divisie — TOP Oss vs Jong Ajax, 23 Oct: TOP Oss 25 home rows.
5. Belgian Pro League — KVC Westerlo vs SK Beveren, 24 Oct: SK Beveren only 3 usable away rows. Keep blocked until minimum-history policy is confirmed.
6. Czech First League — Brno vs Bohemians Praha 1905, 24 Oct: Artis Brno and FC Zbrojovka Brno each 4 home rows; Bohemians 1905 26 away rows. Official fixture evidence points to FC Zbrojovka Brno, but verify competition and stable source IDs before alias approval.
7. Eerste Divisie — FC Dordrecht vs VVV-Venlo, 24 Oct: FC Dordrecht 26 home rows; VVV-Venlo 27 away rows.
8. Ekstraklasa — Wisla vs Rakow, 24 Oct in archive: Wisła Płock and Wisła Kraków are distinct possible clubs; Raków Częstochowa 26 away rows. Official Wisła Płock calendar says it plays Jagiellonia on 24 Oct, so investigate stale/wrong schedule or league/fixture mismatch before any mapping.
9. 2. Bundesliga — Eintracht Braunschweig vs Hannover 96, 25 Oct: Eintracht Braunschweig 24 home rows; Hannover 96 24 away rows.
10. Eredivisie — PSV vs Feyenoord, 25 Oct: PSV Eindhoven 23 home rows; Feyenoord 26 away rows.

## Official fixture evidence found online on 23 Oct 2026
- Pau FC official calendar confirms Pau–Grenoble, 23 Oct, 20:00: https://www.paufc.fr/calendrier
- Jong AZ official page confirms Jong AZ–Helmond Sport, 23 Oct, 20:00: https://az.nl/wedstrijden/wedstrijden/keuken-kampioen-divisie/jong-az-helmond-sport-23-10-2026
- Roda JC official schedule confirms Almere City–Roda JC, 23 Oct, 20:00: https://www.rodajckerkrade.nl/wedstrijden/programma/
- KNVB official Eerste Divisie schedule confirms Almere City FC–Roda JC and TOP Oss–Jong Ajax on 23 Oct, and FC Dordrecht–VVV-Venlo on 24 Oct, 16:30: https://www.knvb.nl/node/15415
- Ajax official fixture list confirms TOP Oss–Jong Ajax, 23 Oct, 20:00: https://english.ajax.nl/games/?team=Jong+Ajax
- SK Beveren official list confirms KVC Westerlo–SK Beveren, 24 Oct, 20:45: https://www.skbeveren.be/wedstrijden?tab=binnenkort
- Bohemians Praha official fixture list confirms FC Zbrojovka Brno–Bohemians Praha 1905, 24 Oct, 15:00: https://bohemians.cz/zapasy/MUZ/
- VVV-Venlo official schedule confirms FC Dordrecht–VVV-Venlo, 24 Oct, 16:30: https://www.vvv-venlo.nl/wedstrijden/
- Eintracht Braunschweig official schedule confirms Braunschweig–Hannover 96, 25 Oct, 13:30: https://www.eintracht.com/news/artikel/drei-spiele-unter-flutlicht-die-ansetzungen-fuer-oktober-und-november-sind-da
- KNVB official Eredivisie schedule confirms PSV–Feyenoord, 25 Oct, 14:30: https://www.knvb.nl/competities/eredivisie/programma
- Official Wisła Płock schedule lists Jagiellonia–Wisła Płock on 24 Oct, not Wisła Płock–Raków: https://wisla-plock.pl/aktualnosci/ramowy-terminarz-sezonu-2026-2027/ . Resolve the source discrepancy.
- Sources establish official fixture details, not a mapping from Oracle CSV labels to historical state IDs. Capture local timezone vs UTC explicitly; sources differ on displayed kickoff time for TOP Oss–Jong Ajax, so prefer official competition/club source and document timezone.

## Immediate steps — do these autonomously
1. Re-fetch current repo head, PR #20, reports/scripts, and CI status before editing.
2. Re-download Run #107 artifact if needed and preserve hashes/source commit.
3. Build a machine-readable evidence CSV for the ten fixtures with archived label/date/league, official title/date/time/timezone/source URL, candidate historical label, role counts, identity evidence, ambiguity, disposition. Distinguish official fixture corroboration from verified Oracle alias.
4. Inspect archive ingestion manifests for source fixture IDs/team IDs and the reason abbreviated labels were written. Use stable IDs and competition/date/opponent evidence. Never invent IDs or auto-approve fuzzy aliases.
5. Resolve Wisla–Rakow discrepancy and confirm official schedule against archived league and date. Keep Jong AZ ambiguous. Verify Brno against stable ID. Keep Beveren blocked until minimum-history policy is documented.
6. Run the replay harness end-to-end against actual archive with explicit league crosswalk and only identity-evidenced aliases. Save before/after readiness CSV/JSON and blockers. Exclude state rows dated on or after each fixture date.
7. Reconcile 27-league scope; RSA/South African Premier Division was marked NO_FIXTURES_IN_WINDOW. Verify whether no matches were scheduled or source coverage failed.
8. Investigate 165 missing kickoff times; only backfill with per-fixture source evidence, provenance and timezone. Do not infer times from dates.
9. Add regression tests for confirmed root causes and a meaningful research workflow that runs tests/replay and uploads artifacts. Keep under 10 minutes if possible; no paid API/secrets. Verify workflow job status and outputs.
10. Publish final completion-gate report. If any identities/policy remain unresolved, report partial completion honestly and leave those fixtures blocked. Production fix is separate and not authorised. Keep PR #20 draft/unmerged.

## Acceptance criteria
Completion means: all ten fixture dispositions documented; aliases approved only with stable identity evidence; replay is reproducible and leak-free; before/after eligibility output saved; 27-league coverage discrepancy explained; kickoff provenance coverage quantified; regression CI green; final report states exact resolved/unresolved count. A green synthetic test alone is not completion.

## First action in new chat
Do not just repeat this handover. Verify live repo state, then begin the next concrete task: retrieve the archived artifact and inspect source IDs/manifests, while producing the evidence CSV/report. Tell Nolan briefly what is verified and proceed. Only ask him if a genuine access or policy decision cannot be resolved independently.