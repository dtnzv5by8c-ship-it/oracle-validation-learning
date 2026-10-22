# Ten-Fixture Prematch State Recovery Experiment — 22 October 2026

**Classification:** Research-only counterfactual; no production inputs or outputs modified.  
**Input provenance:** Public Oracle Run #107 artifact `oracle-fixture-level-predictions`, artifact ID `12425136901`; source commit `f86eaf2586e2d2dc7df73de773a0214116f231bb`.  
**Schedule:** 244 fixtures; prediction manifest excludes 10 for `MISSING_PREMATCH_TEAM_STATE`.  
**Method:** Compare the archived upcoming fixture labels with exact historical team labels in the archived prematch team-state table. For a counterfactual candidate, count rows where the proposed team appears in its required role and that role's history count is greater than zero, using only rows dated before that fixture's scheduled date. This is a diagnostic join experiment, not a run of the production prediction engine.

## Result summary

- **7 fixtures:** both roles have plausible same-league label candidates with role-state rows before the fixture date. These are promising for a controlled research replay after identity confirmation.
- **1 fixture (Westerlo–Beveren):** Westerlo's home role is present, but the candidate SK Beveren has only **3** away-role state rows with nonzero away history before the scheduled date. This remains blocked until the model's minimum role-history requirement is confirmed and met.
- **2 fixtures (Brno–Bohemians and Wisla–Rakow):** keep blocked because the home-team identity is ambiguous. Do not choose a team by fuzzy name matching.
- These are **counterfactual eligibility signals only**. No prediction was generated, and no fixture is claimed to have been recovered in production.

## Fixture-by-fixture counterfactual

Role-state row counts below are calculated from the archived state table with `date < fixture date`. They count rows for the exact role and where the role's `*_n > 0`. “Candidate rows” are not a claim that the production engine will accept the alias; authoritative identity validation is still required.

| Fixture | Required role(s) missing in source manifest | Counterfactual candidate | Home-role rows before fixture | Away-role rows before fixture | Disposition |
|---|---|---|---:|---:|---|
| Ligue 2 — Pau FC vs Grenoble (23 Oct) | Home | Pau / Grenoble | Pau: 24 usable; Grenoble: 25 | 25 | Candidate ready for identity-checked research replay |
| Eerste Divisie — Almere City vs Roda (23 Oct) | Home + away | Almere City FC / Roda JC Kerkrade | 26 | 26 | Candidate ready for identity-checked research replay |
| Eerste Divisie — Jong AZ vs Helmond (23 Oct) | Home + away | Jong AZ Alkmaar / Helmond Sport | 27 | 25 | Candidate ready only after verifying Jong AZ's source identity |
| Eerste Divisie — Oss vs Jong Ajax (23 Oct) | Home | TOP Oss / Jong Ajax | 25 | 27 | Candidate ready for identity-checked research replay |
| Belgian Pro League — Westerlo vs Beveren (24 Oct) | Away | Westerlo / SK Beveren | 28 | 3 | Remains blocked pending history sufficiency and identity validation |
| Czech First League — Brno vs Bohemians (24 Oct) | Home | Ambiguous: Artis Brno or FC Zbrojovka Brno / Bohemians 1905 | Not assigned | 26 | Blocked; stable team ID required |
| Eerste Divisie — Dordrecht vs Venlo (24 Oct) | Home + away | FC Dordrecht / VVV-Venlo | 26 | 27 | Candidate ready for identity-checked research replay |
| Ekstraklasa — Wisla vs Rakow (24 Oct) | Home + away | Ambiguous Wisla / Raków Częstochowa | Not assigned | 26 | Blocked; stable team ID required |
| 2. Bundesliga — Braunschweig vs Hannover (25 Oct) | Home | Eintracht Braunschweig / Hannover 96 | 24 | 24 | Candidate ready for identity-checked research replay |
| Eredivisie — PSV vs Feyenoord (25 Oct) | Home | PSV Eindhoven / Feyenoord | 23 | 26 | Candidate ready for identity-checked research replay |

## Root cause conclusion

The strongest current evidence is **team-label mismatch between the scheduled fixture feed and the historical/prematch state table**. The counterfactual demonstrates that role-specific state records exist for seven fixtures under plausible historical labels, where the exact scheduled labels have zero matching role rows. This makes canonicalisation / join-key alignment the leading hypothesis for those seven.

Two cases cannot be safely fixed by a name-only alias: Brno has two distinct historical candidates; Wisla has multiple clubs. Jong AZ should also be checked against a stable competition-specific team ID because several “Jong” teams exist. Beveren's candidate has only three usable away-role state rows in the prematch state table, so aliasing alone does not establish adequate data.

## Required next implementation step

Build a **research-only replay harness** that:
1. accepts a small, explicit, reviewed alias map scoped by league/competition;
2. rejects ambiguous aliases and refuses any match lacking stable identity evidence;
3. joins to pre-kickoff state rows only and records selected team label/ID, role history count, latest state date, and missing component;
4. re-runs the existing eligibility/reconciliation checks without changing model calculations;
5. emits before/after status for all ten fixtures and regression tests for each confirmed root cause.

Only after that replay passes should a separate recommendation be made about a permanent upstream canonicalisation fix. Do not modify production aliases or emit replacement predictions as part of this experiment.

## Governance and limitations

No production model logic, probabilities, thresholds, weights, calibration, selection rules, or live output files were changed. The research PR remains unmerged. This report improves the diagnosis but does not itself repair production. The seven candidate fixtures are not yet formally recovered; authoritative identity confirmation and replay through the real eligibility path are still required.
