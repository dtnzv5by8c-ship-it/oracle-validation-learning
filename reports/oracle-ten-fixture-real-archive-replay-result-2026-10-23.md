# Project Oracle — Real-Artifact Ten-Fixture Replay Result

**Audit date:** 23 October 2026  
**Input:** Archived public Run #107 fixture schedule and `current_prematch_team_state.csv`  
**Purpose:** Research-only replay of the ten fixtures excluded by the run manifest as `MISSING_PREMATCH_TEAM_STATE`. No probabilities or production data were changed.

## Result

| Outcome | Count |
|---|---:|
| Fixtures examined | 10 |
| Eligible for review only | 1 |
| Blocked pending missing identity/state or policy evidence | 9 |
| Production recoveries | 0 |

The replay used an explicit league-code-to-league-name crosswalk derived from the archived match database, required role-specific history (`home_n > 0` for home and `away_n > 0` for away), and excluded state rows dated on or after the fixture date.

## Fixture-level result

| Fixture | Replay result | Pre-fixture role-state evidence | Decision |
|---|---|---|---|
| Pau FC vs Grenoble (23 Oct) | **ELIGIBLE_FOR_REVIEW_ONLY** | Pau: 24 home-role rows, latest 18 Sep; Grenoble: 25 away-role rows, latest 11 Sep. Archived exact fixture IDs: Pau 6355, Grenoble 9855. | Strongest case for review. This is not a production recovery; the explicit mapping must be reviewed and the replay behavior reconciled with production’s resolver. |
| Almere City vs Roda (23 Oct) | BLOCKED | Exact schedule labels have no role-state rows. Candidate historical labels were found in the earlier audit, but the archived `current_matches.csv` has no matching dated fixture ID row. | Need authoritative source IDs and explicit alias evidence for both clubs. |
| Jong AZ vs Helmond (23 Oct) | BLOCKED | Exact schedule labels have no role-state rows. Jong AZ is ambiguous against Jong Ajax/Jong PSV. | Keep blocked pending stable ID evidence. |
| Oss vs Jong Ajax (23 Oct) | BLOCKED | Exact home label “Oss” has no role-state rows; Jong Ajax has 27 away-role rows. | Need source ID evidence for TOP Oss mapping. |
| Westerlo vs Beveren (24 Oct) | BLOCKED | Westerlo: 28 home-role rows; SK Beveren: only **3** usable away-role rows. Archived exact fixture IDs: Westerlo 10001, SK Beveren 8475. | Identity is supported, but minimum-history policy is unavailable. Do not assume three rows are sufficient. |
| Brno vs Bohemians (24 Oct) | BLOCKED | Exact schedule labels have no role-state rows. Two Brno candidates each have only 4 home-role rows. | Need stable IDs and governed minimum-history policy. |
| Dordrecht vs Venlo (24 Oct) | BLOCKED | Exact schedule labels have no role-state rows; no matching dated fixture ID row in archived `current_matches.csv`. | Need source IDs and explicit role-scoped aliases. |
| Wisla vs Rakow (24 Oct) | BLOCKED | Official fixture and archived IDs confirm Wisła Kraków 10265 vs Raków Częstochowa 4024. Raków: 26 away-role rows; Wisła Kraków: only **4** usable home-role rows. | Correct identity is resolved, but keep blocked pending the governed minimum-history policy. Do not substitute Wisła Płock. |
| Braunschweig vs Hannover (25 Oct) | BLOCKED | Exact schedule labels have no role-state rows; the archived `current_matches.csv` has no matching dated fixture ID row. | Need authoritative IDs and explicit aliases. |
| PSV vs Feyenoord (25 Oct) | BLOCKED | Exact home label “PSV” has no role-state rows; Feyenoord has 26 away-role rows. | Need source ID evidence for PSV Eindhoven mapping. |

## Interpretation

- This is the first real-archive replay result for the ten fixtures using the research harness logic. It does **not** reproduce production eligibility end-to-end; the production resolver has not been invoked from this research branch.
- One fixture (Pau FC vs Grenoble) has enough role-state rows to reach `ELIGIBLE_FOR_REVIEW_ONLY` under the research rule, supported by an exact dated fixture row with team IDs and official schedule evidence.
- Wisła Kraków and SK Beveren are identity-resolved in the archived fixture source, but remain blocked because their available role histories are only four and three rows respectively and the governed minimum-history rule has not been found.
- The other seven fixtures remain blocked until a source ID or equivalent authoritative identity chain can be established and supplied to the explicit alias crosswalk.
- The apparent Westerlo/SK Beveren kickoff discrepancy is timezone-related: the archive field is `date_utc`; 18:45 UTC is 20:45 in Belgium on that date.

## Completion gates

1. Obtain/verify fixture-level source IDs for the remaining seven cases and connect them to historical labels without fuzzy-only matching.
2. Locate the existing governed minimum-history policy. Do not invent a threshold.
3. Re-run the research harness with explicit reviewed mappings and retain the before/after fixture eligibility output.
4. Reconcile the replay with the actual production resolver or document precisely why the resolver’s exclusions differ.
5. Add regression tests for verified identity mappings, low-history blocks and temporal leakage; verify CI.
6. Only after evidence is reviewed, propose a permanent fix. PR #20 remains draft/unmerged; production model logic, probabilities, weights, calibration, thresholds and selection rules remain unchanged.

## Evidence

- [Official fixture cross-check and source links](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/oracle-official-fixture-crosscheck-2026-10-23.md)
- [Corrected ten-fixture role-state audit](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-crosswalk-isolation-2026-10-22/reports/oracle-ten-fixture-corrected-role-state-audit-2026-10-22.md)
- [Research CI Run #65](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39828395156)
- [PR #20 — draft and unmerged](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/20)
