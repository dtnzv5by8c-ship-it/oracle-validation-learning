# Corrected Ten-Fixture Prematch State Audit — 22 October 2026

**Purpose:** Corrected, row-level diagnostic based on the actual archived artifact. Research only; no production files or predictions changed.

**Source:** Oracle public Run #107 artifact `oracle-fixture-level-predictions`, artifact ID `12425136901`; manifest generated `2026-10-22T12:17:13.257607+00:00`; historical cutoff `2026-09-20`. Fixture dates and the archived `current_prematch_team_state.csv` were inspected directly.

## Important correction

The prior summary described the seven cases as promising candidates and Beveren as having limited history. This audit applies the correct role-specific history test (`home_n > 0` for home-role state, `away_n > 0` for away-role state) and excludes state rows on or after the scheduled fixture date. The usable row counts below are therefore the relevant pre-fixture counts, not total team appearances across either role.

The archived manifest reports 244 scheduled fixtures, 234 predicted fixtures, and 10 exclusions due to `MISSING_PREMATCH_TEAM_STATE`. The replay harness is a diagnostic tool only; no candidate alias has been approved from fuzzy matching.

## Fixture-by-fixture role-state diagnostic

“Candidate usable rows” means the historical label has rows dated before kickoff date with a nonzero count for the required role. It does **not** establish that the canonical identity is authoritative or that the existing production runner will accept the mapping.

| Fixture | Missing role(s) in manifest | Historical label candidates and usable role history before fixture | Finding / status |
|---|---|---|---|
| Ligue 2 — Pau FC vs Grenoble (23 Oct) | Home | Pau: 24 home-role rows; Grenoble: 25 away-role rows | Strong candidate for the home label mismatch, pending authoritative identity confirmation |
| Eerste Divisie — Almere City vs Roda (23 Oct) | Home + away | Almere City FC: 22 home-role rows; Roda JC Kerkrade: 26 away-role rows | Both labels have plausible role-state history; identity confirmation required |
| Eerste Divisie — Jong AZ vs Helmond (23 Oct) | Home + away | Jong AZ Alkmaar: 27 home-role rows; Jong PSV: 27; Jong Ajax: 26. Helmond Sport: 25 away-role rows | Helmond candidate is plausible; Jong AZ is ambiguous by name and must remain blocked pending stable ID |
| Eerste Divisie — Oss vs Jong Ajax (23 Oct) | Home | TOP Oss: 25 home-role rows; Jong Ajax: 27 away-role rows | Strong candidate for the home label mismatch, pending identity confirmation |
| Belgian Pro League — Westerlo vs Beveren (24 Oct) | Away | Westerlo: 28 home-role rows; SK Beveren: **3 away-role rows** (4 total pre-date rows, one with zero away history) | Candidate label exists, but away-role history is thin; keep blocked until model minimum-history policy is confirmed |
| Czech First League — Brno vs Bohemians (24 Oct) | Home | Artis Brno: 4 home-role rows; FC Zbrojovka Brno: 4; Bohemians 1905: 26 away-role rows | Ambiguous home identity and low role-history counts; remain blocked |
| Eerste Divisie — Dordrecht vs Venlo (24 Oct) | Home + away | FC Dordrecht: 26 home-role rows; VVV-Venlo: 27 away-role rows | Both labels have plausible role-state history; identity confirmation required |
| Ekstraklasa — Wisla vs Rakow (24 Oct) | Home + away | Wisła Płock: 20 home-role rows; Raków Częstochowa: 26 away-role rows. Wisła Kraków is another candidate label in the league data. | “Wisla” is ambiguous; remain blocked until stable identity confirms the intended club |
| 2. Bundesliga — Braunschweig vs Hannover (25 Oct) | Home | Eintracht Braunschweig: 24 home-role rows; Hannover 96: 24 away-role rows | Strong candidate for the home label mismatch, pending identity confirmation |
| Eredivisie — PSV vs Feyenoord (25 Oct) | Home | PSV Eindhoven: 23 home-role rows; Feyenoord: 26 away-role rows | Strong candidate for the home label mismatch, pending identity confirmation |

## Diagnosis

The strongest explanation for several exclusions is inconsistent team labels between the fixture schedule and historical state rows. The archived data does contain plausible role-state rows under the longer historical labels. However, fuzzy similarity alone is not proof of identity, and this report does not mark any alias as approved.

Three especially important safeguards:
- **Jong AZ:** do not confuse Jong AZ Alkmaar with Jong Ajax or Jong PSV.
- **Brno:** two candidate clubs exist and both have limited home-role history.
- **Wisla:** more than one club label is plausible; a stable source/team ID is required.
- **Beveren:** only three pre-fixture rows have nonzero away-role history; do not infer sufficiency without the governed minimum-history rule.

## Completion gate

The new replay harness and CI tests establish safe mechanics, but the artifact has not yet been replayed through the real production eligibility function. Therefore:
- Confirmed production recoveries: **0**.
- Research candidate fixtures: several, as detailed above.
- Remaining task: verify official team identities, provide an explicit league-code-to-league-name crosswalk, replay only verified aliases in an isolated copy, and compare eligibility before/after.
- Do not emit replacement probabilities or alter production model logic during this experiment.

A permanent fix is ready to recommend only after the isolated replay demonstrates a safe, reproducible recovery and regression tests pass. The research PR remains unmerged.
