# Root-Cause Research: 10 Missing Pre-Match Team-State Fixtures

Date: 2026-10-22
Source: Oracle Completion Run #107, ID `39772347617`, source commit `f86eaf2586e2d2dc7df73de773a0214116f231bb`.
Scope: research-only diagnosis; no aliases were automatically applied and no production code was changed.

## Finding

The 10 missing predictions are all explicitly excluded as `MISSING_PREMATCH_TEAM_STATE`. Inspection of the run's historical match spine shows that many fixture names differ from the labels used in the same competition's historical records. Several names have one clear within-league candidate; two cases remain ambiguous and must not be auto-mapped.

Candidate counts below are counts of historical match rows for that team label in the fixture's competition code, with the latest observed date. They are evidence for review, not permission to rewrite production aliases.

| Fixture | Missing role(s) | Candidate historical label(s) in same competition | Evidence / decision |
|---|---|---|---|
| Pau FC vs Grenoble | Home | Pau (48 rows; latest 2026-09-18) | Candidate label for Pau FC; review alias |
| Almere City vs Roda | Home, away | Almere City FC (45; 2026-09-18); Roda JC Kerkrade (52; 2026-09-18) | Both have single label candidates; review aliases |
| Jong AZ vs Helmond | Home, away | Jong AZ Alkmaar (55; 2026-09-18); Helmond Sport (52; 2026-09-18) | Both have single label candidates; review aliases |
| Oss vs Jong Ajax | Home | TOP Oss (52; 2026-09-18) | Candidate label for Oss; review alias |
| Westerlo vs Beveren | Away | SK Beveren (7; 2026-09-20) | Unique label candidate, but short observed history; verify coverage before use |
| Brno vs Bohemians | Home | FC Zbrojovka Brno (9; 2026-09-19); Artis Brno (9; 2026-09-19) | **Ambiguous. Do not auto-map Brno.** |
| Brno vs Bohemians | Away | Bohemians 1905 (50; 2026-09-19) | Candidate label for Bohemians; review alias |
| Dordrecht vs Venlo | Home, away | FC Dordrecht (52; 2026-09-18); VVV-Venlo (54; 2026-09-18) | Both have single label candidates; review aliases |
| Wisla vs Rakow | Home, away | Wisła Płock (42; 2026-09-20) and Wisła Kraków (9; 2026-09-18); Raków Częstochowa (52; 2026-09-19) | **Wisla is ambiguous. Do not auto-map without a stable team ID or authoritative fixture-source mapping.** |
| Braunschweig vs Hannover | Home, away | Eintracht Braunschweig (48; 2026-09-19); Hannover 96 (48; 2026-09-20) | Both have single label candidates; review aliases |
| PSV vs Feyenoord | Home | PSV Eindhoven (49; 2026-09-20) | Candidate label for PSV; review alias |

## Interpretation

The evidence indicates that the exclusions are not one uniform failure:
- Most missing role histories have a plausible existing team label in the same competition, suggesting a fixture-to-history alias/canonicalization gap.
- Brno and Wisla cannot safely be resolved by fuzzy text alone.
- SK Beveren has only seven historical rows in this source window; an alias alone does not prove sufficient role-specific history or feature readiness.
- Some missing cases could still reflect incomplete source coverage, so the audit must check the actual role-state row counts after any research-only candidate join.

## Recommended fix sequence

1. Add a research-only team alias audit that proposes candidates by competition and name similarity, but never silently promotes fuzzy matches.
2. Resolve candidate aliases using stable source team IDs or documented competition-specific mappings. Mark ambiguous candidates `NEEDS_REVIEW`.
3. Recompute only a research copy of the pre-match team-state joins and report before/after readiness for the 10 fixtures.
4. Confirm every feature uses only matches strictly before kickoff and enough role-specific history.
5. Add regression tests for all 10 exclusions and ambiguous-team cases.
6. Only after evidence is reviewed, propose a separately reviewed change to the governed data preparation. Do not change model probabilities, weights, thresholds, calibration, selection rules, or production code as part of this diagnostic.

## Status

- Actual artifact reconciliation: 234/244 fixtures predicted; 10 excluded.
- Emitted rows: 5,148; all 22 markets complete for each of 234 fixtures; no duplicate fixture/market rows; all emitted probabilities are numeric and within [0, 1].
- Full fixture coverage: **not achieved**.
- Live league-level failure isolation: **not yet verified**.
- Production changes: **none**.
