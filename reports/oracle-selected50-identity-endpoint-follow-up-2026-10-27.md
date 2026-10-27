# Identity Endpoint Follow-up — Documented Candidate, Not Yet Verified (2026-10-27)

## Finding

The official FootyStats documentation exposes a potentially useful endpoint:

- [League Stats / Get Season Stats and Teams](https://footystats.org/api/documentations/league-season-stats-teams)
- Request form: `GET https://api.football-data-api.com/league-season?key=YOURKEY&season_id=X`
- The endpoint is described as returning stats and teams for the requested league season.
- Its field table describes `data.id` as “ID of the season”, while the League List docs state that each season of a competition has a unique ID.

The documentation's example request uses `season_id=2012`; its displayed sample response appears to show `data.id="161"` with season label `2017/2018`. That apparent mismatch means we must **not** assume `data.id` is a stable parent competition ID. It could reflect an example/documentation inconsistency or a different identifier semantic; the current evidence does not settle this.

Other official docs:
- [League List](https://footystats.org/api/documentations/league-list): each season of a competition has a unique ID; sample structure nests `season.id` under the league name.
- [League Matches](https://footystats.org/api/documentations/match-schedule-and-stats): the request parameter is `season_id`, and the endpoint is season-scoped.

## Controlled next step

Before any user-key API call:
1. Verify the available monthly credit balance in the FootyStats account.
2. Obtain explicit approval for a strictly bounded diagnostic budget.
3. First test **one already-selected season ID** using `league-season?season_id=<selected season id>`; capture only sanitized fields: requested season ID, returned `data.id`, `name`, `country`, `season`, `starting_year`, `ending_year`, and response success/error. Do not save the API key or raw payload.
4. Compare the returned identifier and season metadata against the same ID in `league-list` and the existing archive. Do not interpret an ID as a parent competition ID unless documentation or provider confirmation explicitly establishes that semantic.
5. Only if the one-record probe is unambiguous and the user explicitly approves, consider a bounded 50-ID identity probe; no broad ingestion.

## Current gate

- This research note does not call the provider API.
- No provider parent ID is inferred or approved.
- No production registry, Oracle V1.6 model logic, probabilities, thresholds, calibration, or governance was changed.
- Production and betting eligibility remain `NOT_GRANTED`.


## Update — one-call probe completed (2026-10-27)

The explicitly approved one-call probe has now completed successfully. See [sanitized probe result](oracle-footystats-one-call-identity-probe-result-2026-10-27.md).

- Run: [40562430790](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790)
- Artifact: [12760832880](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40562430790/artifacts/12760832880)
- One request, HTTP 200, provider success true, no retry.
- Requested season ID `16571` returned `data.id=16571`, name `Primera División`, country `Argentina`, season/start/end year `2026`.
- The sample is consistent with a season-scoped record. It does not verify a parent competition ID or establish mappings for the other 49 selected IDs.
- Parent competition IDs verified remains **0/50**; approved provider-to-canonical bridges remains **0**.
- No further provider requests are authorized by this result. Do not run a 50-ID probe without separate explicit approval and verified credit budget.
