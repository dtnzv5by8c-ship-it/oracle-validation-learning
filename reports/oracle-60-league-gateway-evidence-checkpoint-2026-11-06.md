# Oracle 60-League Gateway Evidence Checkpoint — 2026-11-06

## Live evidence inspected
The connected private repository `dtnzv5by8c-ship-it/oracle-football-data` is reachable and reports `private=true`.

Its current canonical registry remains `ORACLE_MAJOR_LEAGUE_REGISTRY_V1.0` with an active universe of **27 leagues**. The registry explicitly separates league membership from data readiness and production eligibility.

## Consequence
This is useful private-repository access evidence, but it is **not** a 60-league gateway receipt and must not be promoted into one.

No verified private receipt for the governed 60-League Universe was found. In particular, there is currently no evidence that the private repository contains the governed 60-league receipt at:
`gateway/receipts/footystats-60-league-latest.json`

## Safety decision
- Public FootyStats HTTP 417/Cloudflare path remains retired.
- No provider retry or Cloudflare bypass was performed.
- No broad historical ingestion was dispatched.
- Existing selected-50/49-league evidence remains scoped to that universe.
- Oracle V1.6 production logic, probabilities, thresholds and governance remain unchanged.

## Engineering progress
A new admission workflow now checks the private repository, requires the governed 60-league receipt locator, and runs the existing fail-closed receipt validator without publishing provider payloads.

## Next action
The first genuine 60-league private receipt should be placed at the governed private locator. Once present and validated, the existing 3 x 20 bounded provider-season planner can proceed. Until then, the ingestion gate remains BLOCKED.
