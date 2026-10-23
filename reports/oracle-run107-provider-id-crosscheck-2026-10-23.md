# Oracle Run #107 — Provider-ID Crosscheck (23 October 2026)

## Scope and governance
Research-only inspection of the archived public Run #107 artifact. No alias has been approved, no production prediction was generated, and no production logic or eligibility rule was changed. PR #20 remains draft/open/unmerged.

## Source schemas
The archive's `current_matches.csv` includes provider identifiers (`fotmob_match_id`, `league_id`, `home_id`, `away_id`) for current fixtures/results. However:
- `oracle_upcoming_fixtures.csv` has only `league_code,date,home_team,away_team,kickoff_time`; no fixture ID or team IDs.
- `current_prematch_team_state.csv` has team names and state counts but no home/away team IDs.
- Historical `matches.csv` has `source_match_id` but no home/away team IDs. Its historical source-match IDs did not overlap the 448 current-match IDs in this archive, so those records do not provide a direct ID bridge for historical team-state labels.
This is a structural limitation: name variants can be identified as candidates, but cannot be safely joined to historical state by a stable ID when the state/history tables do not preserve IDs.

## Direct provider fixture records found
| Target schedule label | Current provider record | Provider identifiers | Interpretation |
|---|---|---|---|
| Pau FC–Grenoble, Ligue 2, 23 Oct | Pau–Grenoble at 2026-10-23T18:00:00Z | FotMob match 5803296; home ID 6355; away ID 9855 | Direct provider record supports this fixture pairing. Historical state still uses label `Pau`, not `Pau FC`; because the historical state row has no team ID, the alias cannot be certified from this artifact alone. |
| Westerlo–Beveren, Belgian Pro League, 24 Oct | Westerlo–SK Beveren at 2026-10-24T18:45:00Z | FotMob match 5811790; home ID 10001; away ID 8475 | Direct provider record supports the current fixture and canonical provider label `SK Beveren`. The archived state has three SK Beveren away-role rows, but the governed minimum-history rule must be verified before eligibility. |
| Wisla–Rakow, Ekstraklasa, 24 Oct | Current provider record is Wisła Kraków–Raków Częstochowa at 2026-10-24T18:15:00Z | FotMob match 5804021; home ID 10265; away ID 4024 | Conflict, not a safe alias: the target schedule only says `Wisla`; official Wisła Płock calendar lists another opponent. The identity/competition mismatch remains unresolved and must stay blocked. |

## Team IDs seen in other current records
The artifact also shows these provider IDs in nearby records, but those records are not the exact target fixture and do not by themselves prove the schedule-to-history join:
- Eintracht Braunschweig: 9776; Hannover 96: 9904.
- PSV Eindhoven: 8640; Feyenoord: 10235.
- Wisła Płock: 8243, distinct from Wisła Kraków: 10265.
- Raków Częstochowa: 4024.
No corresponding exact current provider fixture record was found in this artifact for Almere City–Roda, Jong AZ–Helmond, Oss–Jong Ajax, Brno–Bohemians, or Dordrecht–Venlo. Do not invent IDs or promote fuzzy aliases for these fixtures.

## Research conclusion and permanent-fix direction
1. Preserve provider fixture/team IDs in the schedule and in the prematch-state/history records, not only in `current_matches.csv`.
2. Build an auditable crosswalk by provider team ID + league/competition + season; keep names as display fields.
3. Require direct fixture/competition evidence for the Wisła case and an approved minimum-history policy for SK Beveren.
4. Until stable identity evidence exists, leave all ten named fixtures blocked in the research replay. The successful Run #17 only validates the replay process; it does not restore these ten production predictions.

## Reproducible sources
- Archived Run #107: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39772347617
- Successful research replay Run #17: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39910882943
- Replay diagnostics artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39910882943/artifacts/12482807263
