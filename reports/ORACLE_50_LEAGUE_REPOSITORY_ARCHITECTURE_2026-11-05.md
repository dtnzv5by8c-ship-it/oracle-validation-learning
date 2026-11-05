# Oracle 50-League Repository Architecture — 2026-11-05

## Decision
- Public repository `oracle-validation-learning` performs the single low-risk FootyStats catalogue metadata call and all offline planning, QA, reconciliation, feature derivation and reporting.
- Private repository `oracle-football-data` performs the raw match/team/table/season ingestion only. Raw provider payloads never enter the public repository.
- Public standard GitHub-hosted runners are free; private GitHub-hosted runner usage consumes the account's included compute/minute allowance. This is why the heavy deterministic processing remains public while raw provider access remains private.

## Public workflow
- `.github/workflows/footystats-selected50-catalogue-resolver.yml`
- Registered on `main` and research branch.
- Exactly one provider API call: `league-list?chosen_leagues_only=false`.
- Resolves the user's canonical 50-league manifest using exact provider league names with explicit country aliases only.
- Writes only sanitized season/league IDs and the 50-league ingestion request manifest.
- Fails closed if all 50 selected leagues cannot be resolved exactly.
- Does not persist the raw provider catalogue payload.

## Private workflow
- `.github/workflows/footystats-private-historical-ingestion.yml`
- Now named `FootyStats Private Historical Ingestion (Controlled Selected-50)`.
- Reads the sanitized Selected-50 manifest from the public research branch.
- Verifies the manifest covers exactly 50 selected IDs before provider access.
- Uses raw provider calls for league-matches, league-teams, league-tables and league-season.
- Follows pagination for matches and teams when provider metadata reports additional pages.
- Keeps raw payloads private in the private Actions artifact.
- Enforces 1,500 operational requests/run and 1,800 rolling-hour ceiling.
- Final ledger handling was corrected to import the required environment module.

## Retired workflow
- `.github/workflows/footystats-global-budgeted-endpoint-preflight.yml` is now a fail-closed stub and must not be used for provider API calls.
- Prior run 41869437030 successfully made 910 preflight requests before its sanitized-output commit failed; its artifact remains valid evidence of the 49-league preflight only. It is not evidence of 50-league ingestion.

## Current gap
- The live selected provider catalogue snapshot contains 49 leagues, while the governed Oracle target contains 50. The exact missing target leagues in the 2026-11-04 selected snapshot were Finland Veikkausliiga, India Indian Super League, Republic of Ireland Premier Division, Russia Russian Premier League, South Korea K League 1, and Venezuela Primera División; the snapshot also contained five non-target extras.
- The new full-catalogue resolver is designed to determine whether those six are available in the provider database/account and to fail closed if any cannot be mapped exactly.
- Fixture-level xG point-in-time provenance remains separately quarantined; no model eligibility is changed by this architecture.

## Governance
- Oracle V1.6 production logic, probabilities, thresholds and calibration remain untouched.
- Research outputs remain `production_eligible=false` and `betting_eligible=false`.
- No fuzzy fixture/team joins, required-feature imputation or fabricated coverage claims are permitted.