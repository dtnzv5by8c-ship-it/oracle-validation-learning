# Project Oracle Validation Follow-up — Alternative Provider Gate

**Date:** 19 October 2026  
**Repository:** `oracle-validation-learning` only  
**Production governance:** No Oracle production code, predictions, probabilities, calibration, or historical database changed.

## Why this follow-up exists

The OpenFoot audit (Run #28) completed successfully but could not accept the requested data coverage. Three competitions were absent from OpenFoot's catalogue, Greece's listed season was stale, dedicated league xG was only supported for four of the ten OpenFoot-mapped competitions, and H2H quality remained partial in six mapped competitions.

## Public provider coverage discovery

API-Football's official coverage catalogue explicitly lists all three competitions that OpenFoot could not map:

- USA — MLS Next Pro
- Argentina — Copa Argentina
- Portugal — Taça de Portugal

Source: https://www.api-football.com/coverage (coverage page last updated 12 October 2026).

This establishes a **candidate alternate source**, not operational data acceptance. Public coverage listings alone do not prove that the user's API plan returns current seasons, fixtures, standings, H2H, last-five scorelines, or xG values for each target. Those must be tested using actual responses.

Sportmonks' public xG documentation lists xG-enabled competitions separately and warns that xG availability varies by league and package. Therefore broad fixture coverage must not be treated as proof of xG coverage. Source: https://docs.sportmonks.com/v3/tutorials-and-guides/tutorials/expected/coverage.

## Alternative audit added

Files:
- `scripts/audit_api_football_gap_competitions.py`
- `.github/workflows/api-football-alternative-coverage-audit.yml`

Workflow: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/workflows/api-football-alternative-coverage-audit.yml

The script is read-only and targets all 13 competitions in the OpenFoot audit. It checks exact country + normalized competition identity before accepting a mapping, current-season metadata, a finished fixture, standings, match-statistics xG, H2H response, and recent five-match scorelines/goals for both teams. Fuzzy candidates are logged for review but never probed or accepted as verified mappings.

## Actual run result and remaining dependency

Run #29: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39244855517

The workflow itself succeeded, but its sanitized artifact reports:

`BLOCKED_MISSING_API_FOOTBALL_KEY`

No API-Football API requests were made. The repository does not currently expose an `API_FOOTBALL_KEY` GitHub Actions secret to this workflow. The script was subsequently tightened to require exact competition identity before any candidate is used; that update triggers a new audit run, which will also remain blocked until the secret is configured.

## Required action to finish runtime verification

Add the API-Football key to the **public validation repository's** GitHub Actions secrets under the exact name `API_FOOTBALL_KEY`. Do not paste the key into chat, code, workflow logs, or artifacts. Then rerun the workflow above.

Once the secret is present, review the resulting artifact for:
1. Exact mapping and current-season confirmation for each target.
2. Finished fixture availability and standings rows.
3. H2H response status and meeting coverage.
4. Five scored recent matches for each team, with goals scored/conceded and form derivable.
5. Actual xG statistics for both teams.

The final acceptance gate must remain false unless the required fields are verified for all target competitions. If any competition lacks xG or another required field, document that limitation and keep that field unsupported rather than fabricating or substituting an unverified value.

## Current status by item

| Item | Status |
|---|---|
| 1. Missing competition mappings | Public alternative candidate found for all three; runtime mapping not yet verified |
| 2. Greece current season | Still requires provider response validation; OpenFoot's 2024/25 listing is stale |
| 3. H2H diagnostics | Implemented and tested on OpenFoot; alternative-provider H2H probe awaits API key |
| 4. Recent form + last-five goals | OpenFoot mapped sample coverage passes 10/10; alternative-provider test awaits API key |
| 5. Final acceptance and production governance | Acceptance remains closed; production repository remains untouched |

**Do not merge or route the alternative provider into Oracle production based on public coverage evidence alone.**
