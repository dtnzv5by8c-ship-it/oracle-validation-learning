# Project Oracle H2H Reporting — Quality Gate Diagnosis and Corrective Control
Date: 2026-11-07
Workflow: Oracle H2H Reporting #51
Run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/42369950640
Source commit: b5987ca1194469e65e61296157cf1f2b75acaf89

## Finding
The run completed all build/report/join tasks, preserved its artifacts, and failed only at the H2H quality gate. Historical archive acquisition, schema validation, deduplication, recency, canonical Fixture ID export, and exact-ID join all passed.

## Evidence
- 151 Oracle fixtures exported; 151 unique canonical Fixture IDs.
- Exact-ID join: 151/151 joined, match rate 100%, unmatched fixture IDs 0, fuzzy matching false.
- Oracle probability values unchanged; production model logic unchanged.
- Historical archive: 75,849 matches from 2018-07-20 through 2026-11-07; source status OK; 0 acquisition errors; 0 duplicate keys after merge; age 0 days.
- H2H report: 95 fixtures with at least one prior H2H, 76 with at least 5 prior H2H matches, 56 with zero prior H2H.
- Among zero-H2H fixtures, 44 were classified unresolved team/league mapping and 12 were genuine no-prior-meeting cases.
- Failed gate: unresolved mapping rate 29.14% > configured limit 20%.
- The 29.14% metric is 44 unresolved rows / 151 fixtures. Genuine no-H2H rows (12) are correctly excluded from the numerator.

## Root Cause
The failure is substantive team identity reconciliation debt rather than a Fixture ID join defect. The current report normalizes basic spelling/aliases, but fails to reconcile multiple valid source naming variants for club/team entities and some historical league participation changes.

Examples include Leuven vs OH Leuven; KV Mechelen vs Mechelen; Cercle Brugge KSV vs Cercle Brugge; Charleroi vs Sporting Charleroi; Borussia Dortmund / Dortmund; Mainz 05 / Mainz; 1. FC Köln / Köln; Hertha Berlin / Hertha BSC; Nürnberg / Nurnberg; Heidenheim / FC Heidenheim; Nottingham / Nottingham Forest; Manchester Utd / Manchester United; Atlético Madrid / Atl. Madrid; Brno / Zbrojovka Brno; Liberec / Slovan Liberec; Ostrava / Banik Ostrava; Bohemians / Bohemians 1905; Zlin / Zlín; Slovacko / 1. FC Slovácko; Estrela / Estrela da Amadora; Casa Pia / Casa Pia AC; Leiria / União de Leiria; Leixoes / Leixões; Malaga / Málaga; Cordoba / Córdoba; Ceuta / AD Ceuta.

Two league participation conflicts require conservative handling: Nacional vs Academico Viseu pair is present under POR2 rather than P1; Malaga vs Racing Santander pair is present under SP2 rather than SP1. Do not blindly map those to another league.

Newly promoted/relegated or newly appearing teams may genuinely have no prior same-league H2H. Such cases must remain separately classified. Team names alone are not sufficient to assert historical same-league meetings.

## Corrective Action
- Do not weaken or raise the 20% quality threshold merely to make the run green.
- Build a deterministic, evidence-backed alias/canonical-team crosswalk using persisted Oracle historical team evidence and the previously retained Leagues Revision v4 team lookup.
- Separate stable aliases from season/league participation. Do not infer historical H2H from team-name similarity alone.
- Add regression tests for confirmed alias pairs and league-mismatch cases.
- Update reporting-only H2H builder and diagnostics; no prediction engine/model changes.
- Recompute unresolved rate; classify no-history, unmapped identity and league-code conflict separately.
- Keep the quality gate at 20% until evidence demonstrates unresolved rate is at or below the limit.

## Validation
Not yet rerun after corrective mapping. The #51 artifacts are retained and must not be treated as a failed exact-ID join.

## Governance
- Research/reporting-only change.
- No Oracle V1.6 production model logic, probabilities, thresholds, calibration or eligibility changes.
- No fuzzy Fixture ID join.
- No fabricated H2H or retroactive meetings.
- Genuine no-H2H is valid report output, not a pipeline failure by itself.