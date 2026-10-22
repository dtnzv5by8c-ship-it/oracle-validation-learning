# Ten-Fixture Root-Cause and Recovery Audit
**Date:** 2026-10-22  
**Classification:** Research-only; no production changes  
**Source run:** public repository Run #107, ID `39772347617`  
**Source commit:** `f86eaf2586e2d2dc7df73de773a0214116f231bb`  
**Artifact:** `oracle-fixture-level-predictions`, artifact ID `12425136901`  
**Manifest generated:** `2026-10-22T12:17:13.257607+00:00`  
**Historical cutoff:** `2026-09-20`

## Executive finding

The archived output contains 244 scheduled fixtures and predictions for 234 (95.90%). Ten fixtures were explicitly excluded with `MISSING_PREMATCH_TEAM_STATE`. The 5,148 emitted prediction rows form complete 22-market matrices for all 234 emitted fixtures; no duplicate fixture/market rows or invalid numeric probabilities were found.

This audit narrows the likely causes for the ten exclusions, but **does not claim any fixture has been recovered**. Team-name candidates are evidence for review, not approved aliases. No aliases were applied to production or used to generate replacement probabilities.

## Fixture-by-fixture findings

Candidate history counts below are from the archived historical match spine, scoped to the fixture's league code. Counts are appearances across home/away roles unless a role-specific count is stated. A candidate with history is not, by itself, proof that the current prematch-state builder can safely resolve it.

| # | Fixture | Missing component(s) | Evidence and candidate | Research disposition |
|---:|---|---|---|---|
| 1 | Ligue 2 — Pau FC vs Grenoble | Home-role history | Historical label **Pau**: 48 match appearances, 25 as home, latest 2026-09-18. Grenoble already has history (49 appearances; 25 home); manifest says away-role state exists. | **Strong label-mismatch candidate** for Pau FC → Pau. Validate the canonical source identity and state-builder join before accepting. |
| 2 | Eerste Divisie — Almere City vs Roda | Home- and away-role history | **Almere City FC**: 45 appearances, 22 home, latest 2026-09-18. **Roda JC Kerkrade**: 52 appearances, 26 home, latest 2026-09-18. | **Two plausible label mismatches.** Candidate mappings require confirmation against a stable source/team ID and role-state join. |
| 3 | Eerste Divisie — Jong AZ vs Helmond | Home- and away-role history | **Helmond Sport**: 52 appearances, 26 home, latest 2026-09-18. The Jong AZ search is ambiguous by string similarity: Jong AZ Alkmaar (55 appearances), Jong Ajax (54), and Jong PSV (55) are all nearby labels. | **Helmond is a plausible label mismatch. Jong AZ remains unresolved** until an authoritative identifier or trusted mapping distinguishes it from other Jong teams. |
| 4 | Eerste Divisie — Oss vs Jong Ajax | Home-role history | **TOP Oss**: 52 appearances, 25 home, latest 2026-09-18. Jong Ajax has 54 appearances and existing away-role state in the manifest. | **Strong label-mismatch candidate** for Oss → TOP Oss; verify identity before use. |
| 5 | Belgian Pro League — Westerlo vs Beveren | Away-role history | **SK Beveren**: only 7 appearances, 4 as home, latest 2026-09-20. Westerlo has 57 appearances and existing home-role state. | **Potential alias plus history-sufficiency risk.** Do not treat seven appearances as sufficient without the model's documented minimum-history requirements and team identity confirmation. |
| 6 | Czech First League — Brno vs Bohemians | Home-role history | Two competing historical labels: **Artis Brno** (9 appearances; 5 home) and **FC Zbrojovka Brno** (9 appearances; 5 home), both latest 2026-09-19. Bohemians 1905 has 50 appearances. | **Blocked — ambiguous identity.** No automatic mapping; resolve using an authoritative competition/team ID. |
| 7 | Eerste Divisie — Dordrecht vs Venlo | Home- and away-role history | **FC Dordrecht**: 52 appearances, 26 home, latest 2026-09-18. **VVV-Venlo**: 54 appearances, 27 home, latest 2026-09-18. | **Two plausible label mismatches.** Confirm IDs and test state lookup in isolation. |
| 8 | Ekstraklasa — Wisla vs Rakow | Home- and away-role history | **Raków Częstochowa** has 52 appearances, 26 home, latest 2026-09-19. The label **Wisla** is ambiguous in historical data: Wisła Płock has 42 appearances; Wisła Kraków has 9. | **Blocked — ambiguous Wisla identity.** Rakow → Raków Częstochowa is plausible but must be confirmed; do not map Wisla without a stable ID. |
| 9 | 2. Bundesliga — Braunschweig vs Hannover | Home-role history | **Eintracht Braunschweig**: 48 appearances, 24 home, latest 2026-09-19. Hannover 96 has 48 appearances and the manifest shows away-role state exists. | **Strong label-mismatch candidate** for Braunschweig → Eintracht Braunschweig. Verify canonical identity and join. |
| 10 | Eredivisie — PSV vs Feyenoord | Home-role history | **PSV Eindhoven**: 49 appearances, 24 home, latest 2026-09-20. Feyenoord has 50 appearances and the manifest shows away-role state exists. | **Strong label-mismatch candidate** for PSV → PSV Eindhoven. Verify canonical identity and join. |

## Root-cause classification

1. **Likely canonical-name / join mismatch:** Pau FC, Almere City, Roda, Helmond, Oss, Beveren, Dordrecht, Venlo, Braunschweig, PSV, and Rakow have plausible longer historical labels. These are candidates, not approved fixes.
2. **Ambiguous team identity:** Jong AZ, Brno, and Wisla cannot be safely resolved by string similarity alone. Brno has two competing candidates; Wisla may refer to different clubs. Jong AZ must be distinguished from Jong Ajax and Jong PSV.
3. **Possible insufficient history:** SK Beveren has only seven historical appearances in this artifact. Even if its identity is confirmed, minimum-history readiness must be assessed separately.
4. **Upstream mechanism still to confirm:** The manifest exposes missing role-state counts and candidate hints, but this artifact alone does not prove whether the defect is in canonicalization, team-state generation, or the final join. The next test must instrument those stages separately.

## Recovery experiment and acceptance criteria

The next research-only experiment must:
- Work on a copy of the archived inputs; do not overwrite source files.
- Apply only mappings independently confirmed by a stable source/team identifier or an authoritative competition-specific mapping.
- Rebuild/resolve prematch team-state lookup using only data available before each fixture's kickoff and the existing historical cutoff.
- Compare each fixture's home/away role-state readiness before and after, recording the exact matched team ID/name, history count, latest permissible date, and missing component.
- Keep Brno, Wisla, and unresolved Jong AZ blocked. Treat Beveren as blocked pending history-sufficiency validation.
- Never manufacture team-state rows, borrow another team's history, or emit replacement predictions as if they were production predictions.
- Add regression tests for confirmed failures and rerun the public research workflow.

**Success is not “all ten fixtures forced through.”** Success is verified eligibility restored for the subset whose identity and pre-match data are demonstrably correct, with every unresolved fixture explicitly blocked and explained.

## Governance

No production model logic, weights, probabilities, thresholds, calibration, selection rules, or production data have been changed. The research PR remains unmerged. This report is an evidence-backed root-cause assessment; the before/after state-join experiment is still outstanding and is required before calling the data issue fixed.
