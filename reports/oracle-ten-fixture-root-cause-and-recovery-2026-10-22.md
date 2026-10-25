# Ten-Fixture Root-Cause and Recovery Report

**Date:** 22 October 2026  
**Classification:** Research-only diagnostic. Not a production change or model approval.  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Evidence source:** Oracle Completion Run #107 artifact, source commit `f86eaf2586e2d2dc7df73de773a0214116f231bb`, generated 2026-10-22 12:17:13 UTC. Artifact SHA-256: `5de8e3773934e2d53aa6464df31c03ee8d7a47bda98ad19ed39e590d28cb3299`.

## Executive finding

The run scheduled **244 fixtures**, emitted predictions for **234 (95.90%)**, and explicitly excluded **10** because required prematch team-state history was missing. The 5,148 emitted rows form a complete 22-market matrix for each of the 234 predicted fixtures. No duplicate fixture/market rows or nonnumeric/out-of-range probabilities were found in those emitted rows.

The ten exclusions are **not ten independent prediction-model failures**. The manifest marks all ten `MISSING_PREMATCH_TEAM_STATE`. Comparing the fixture labels with the same-league historical match spine reveals a strong team-name/canonicalization pattern for several teams. This is a credible upstream root-cause candidate, but a name similarity alone does not prove that the production team-state join can safely be repaired.

**Important limit:** this report is an evidence-backed root-cause audit, not proof that any fixture has already been recovered. No production alias was applied, no prediction was generated, and no probabilities or model logic were changed. The next validation step is an isolated, research-only role-history join experiment against these exact artifact files.

## Fixture-by-fixture findings

History counts below are from `oracle/database/matches.csv`, scoped to the fixture's competition code and counted across home/away appearances. Latest dates are observed historical dates, not forecasts. A candidate is not automatically approved.

| # | Fixture | Missing role state | Historical label evidence | Assessment |
|---:|---|---|---|---|
| 1 | Ligue 2 — Pau FC vs Grenoble | Home | Historical label **Pau**: 48 appearances (25 home, 23 away), latest 2026-09-18. Grenoble has 49 appearances and the state manifest reports 50 appearances in any role. | **Likely canonical-name mismatch** for Pau FC → Pau. Strong single-label candidate; validate role-specific state and date cutoff in the isolated join. |
| 2 | Eerste Divisie — Almere City vs Roda | Home + away | **Almere City FC**: 45 appearances (22 home, 23 away), latest 2026-09-18. **Roda JC Kerkrade**: 52 (26/26), latest 2026-09-18. | **Likely two canonical-name mismatches.** Both labels are present in the same competition's state table. Test both mappings together in the research copy. |
| 3 | Eerste Divisie — Jong AZ vs Helmond | Home + away | **Jong AZ Alkmaar**: 55 appearances (28/27), latest 2026-09-18. **Helmond Sport**: 52 (26/26), latest 2026-09-18. The competition also contains other “Jong …” clubs. | **Likely naming mismatch, with identity review required for Jong AZ.** Helmond → Helmond Sport is a strong candidate; do not choose a Jong-team mapping from string similarity alone. |
| 4 | Eerste Divisie — Oss vs Jong Ajax | Home | **TOP Oss**: 52 appearances (25/27), latest 2026-09-18. Jong Ajax has 54 appearances (27/27), latest 2026-09-18. | **Likely canonical-name mismatch** for Oss → TOP Oss. Jong Ajax's history exists under the fixture label. |
| 5 | Belgian Pro League — Westerlo vs Beveren | Away | **SK Beveren**: only 7 appearances (3 home, 4 away), latest 2026-09-20. Westerlo has 57 appearances (28/29), latest 2026-09-20. | **Mixed cause:** Beveren → SK Beveren is a plausible label mismatch, but only seven historical appearances are visible. Verify competition/team identity and the minimum history needed for reliable state before treating this as recoverable. |
| 6 | Czech First League — Brno vs Bohemians | Home | **Two Brno candidates:** FC Zbrojovka Brno and Artis Brno, each with 9 appearances (5 home, 4 away), latest 2026-09-19. Bohemians 1905 has 50 (24/26), latest 2026-09-19. | **Ambiguous identity; remain blocked.** A name-only mapping could attach the wrong club's history. Requires authoritative team ID or verified competition fixture mapping. |
| 7 | Eerste Divisie — Dordrecht vs Venlo | Home + away | **FC Dordrecht**: 52 appearances (26/26), latest 2026-09-18. **VVV-Venlo**: 54 (27/27), latest 2026-09-18. | **Likely two canonical-name mismatches.** Strong same-competition candidates; test the pair in the research copy. |
| 8 | Ekstraklasa — Wisla vs Rakow | Home + away | **Raków Częstochowa**: 52 appearances (26/26), latest 2026-09-19. “Wisla” is ambiguous in the historical spine: Wisła Płock has 42 appearances (20/22), while Wisła Kraków has 9 (5/4). | **Rakow label likely resolvable; Wisla must remain blocked.** Require stable team ID or authoritative fixture mapping before selecting either Wisła club. |
| 9 | 2. Bundesliga — Braunschweig vs Hannover | Home | **Eintracht Braunschweig**: 48 appearances (24/24), latest 2026-09-19. **Hannover 96**: 48 (24/24), latest 2026-09-20. | **Likely canonical-name mismatches** for both fixture labels. Validate exact competition-scoped mappings and role state. |
| 10 | Eredivisie — PSV vs Feyenoord | Home | **PSV Eindhoven**: 49 appearances (24/25), latest 2026-09-20. Feyenoord has 50 (25/25), latest 2026-09-20. | **Likely canonical-name mismatch** for PSV → PSV Eindhoven. Validate the home-role state join. |

## Root-cause classification

- **Strong canonicalization candidates:** fixtures 1, 2, 4, 7, 9 and 10. Their abbreviated fixture labels differ from established same-competition history labels with substantial recent records.
- **Candidate plus team-identity review:** fixture 3 (Jong AZ). The history exists as Jong AZ Alkmaar, but other “Jong” clubs make fuzzy matching an unsafe approval mechanism.
- **Candidate plus history-sufficiency review:** fixture 5 (Beveren). The candidate is SK Beveren, but only seven historical appearances are evidenced in this data window.
- **Must remain unresolved pending authoritative identity:** fixtures 6 (Brno) and 8 (Wisla). The history has multiple plausible clubs; selecting by text would risk cross-team data contamination.

This classification is a diagnosis from the historical match spine. It does **not** prove that name normalization is the only root cause. The role-state builder, competition/team ID crosswalk, and any minimum-history gates must be checked in the next isolated experiment.

## Recovery test required to close this issue

1. Reproduce the baseline against the archived artifact: 244 scheduled, 234 predicted, 10 excluded.
2. In a **research-only copy**, apply only individually verified, same-competition label mappings. Keep an explicit mapping ledger with source label, target label, evidence, approval status, and history counts. Do not write to the source files.
3. Rebuild/inspect the role-specific prematch history for each affected fixture using only records dated before that fixture's kickoff. Verify home-role history for the home team and away-role history for the away team, and preserve the existing required-feature/eligibility rules.
4. Re-run the fixture/market reconciliation. Report, for each fixture, baseline eligibility, research-copy eligibility, missing components after mapping, row counts, latest eligible history date, and whether the fixture is still blocked.
5. Do not resolve Brno or Wisla without authoritative IDs. Do not treat Beveren as adequately supported until the existing history sufficiency rule is identified and checked.
6. Add regression tests for the confirmed cause(s), run the research workflow, and attach the resulting report/artifact. Only claim recovery if the experiment actually produces a complete, valid output for that fixture.

## Acceptance criteria

- Every scheduled fixture is accounted for; no silent drops.
- No cross-competition or cross-team history joins.
- No future/post-kickoff data in prematch state.
- No synthetic/fabricated history used to make a fixture eligible.
- Existing production probabilities, weights, thresholds, selection logic and model version remain unchanged.
- Ambiguous/insufficient data remains explicitly blocked.
- PR #20 remains unmerged until the user explicitly approves.

## Current status

**Root-cause audit delivered; permanent fix not yet proven.** The best-supported explanation for a substantial subset is a mismatch between short fixture labels and canonical historical team labels. The next engineering deliverable is the research-only before/after role-history join experiment, followed by regression tests and a reconciled fixture-level result. Production remains untouched.
