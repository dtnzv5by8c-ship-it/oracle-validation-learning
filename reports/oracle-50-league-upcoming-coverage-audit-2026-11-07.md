# Oracle 50-League Upcoming Fixture Coverage Audit — 2026-11-07

## Finding
The governed historical 50-league universe is present and independently identified as 50 selected FootyStats leagues, but the live upcoming-fixture pipeline is still operating on the legacy 27-league registry and the latest persisted fixture board contains only 14 league codes.

## Evidence
- Canonical 50-league manifest: `data/footystats/selected50-full-ingestion-manifest.csv` contains 728 planned endpoint tasks across exactly 50 selected leagues.
- Private gateway receipt: `gateway/receipts/footystats-50-league-latest.json` records `universe_name=Oracle-50-League`, `expected_leagues=50`, and 8,367 received rows from the historical private archive; it remains non-production/non-betting eligible.
- Live private upcoming fixture manifest: `data/fixtures/oracle_upcoming_fixtures_manifest.json` declares `active_leagues=27`, with 27 targets.
- Of those 27 targets, 14 are `OK_FALLBACK` and 13 are `SOURCE_ERROR`.
- Persisted `data/fixtures/oracle_upcoming_fixtures.csv` currently contains only 14 unique league codes: B1, CRO, D1, D2, E1, E2, E3, F1, I1, N1, NED2, SP1, SWZ, UKR.
- The live ingestion implementation `scripts/ingest_upcoming_fixtures.py` explicitly documents and hardcodes an active 27-league `REGISTRY`; it is not a 50-league production fixture registry.
- The current fixture window is 2026-11-07 through 2026-11-21.

## Root Cause
The historical 50-league acquisition universe and the live upcoming-fixture registry are separate controls. Historical 50-league readiness was built and reconciled, but the prospective fixture-ingestion layer was never promoted from its legacy 27-league registry to a governed 50-league registry. In addition, 13 of the 27 current targets are failing their existing Football Charts/OpenFoot fallback path, including an ambiguous Premier League resolver and multiple no-usable-fixture fallback failures.

## Impact
- The current prospective prediction board cannot demonstrate 50-league fixture coverage.
- The latest governed cycle therefore cannot provide 50-league prospective evidence.
- This is separate from the already-closed 648/80 historical FootyStats acquisition accounting and must not be conflated with the HTTP-417 entitlement blocker.
- Production and betting eligibility remain fail-closed.

## Fix Required
1. Establish a canonical 50-league prospective fixture registry using the already-governed 50-league universe as the identity source.
2. Map each selected league to an explicit, verified current-season fixture source/competition identifier; do not infer ambiguous names.
3. Preserve source-specific fallback and fail-closed coverage diagnostics.
4. Require the persisted fixture board to reconcile to the governed 50-league registry before prospective prediction publication is admissible.
5. Only after genuinely new future fixtures enter the board, exercise the immutable feature-snapshot chain and settlement provenance controls.

## Validation Required
- 50/50 canonical league identities resolved.
- Current-season source/competition identifiers verified.
- No ambiguous competition resolution.
- Per-league fixture coverage status recorded as PASS, DATA_GATED, or SOURCE_ERROR.
- Fixture board coverage reconciles exactly to the governed registry for the requested window.
- No production model logic, probabilities, thresholds, calibration or betting governance changed.

## Governance
This is a research/validation finding only. No provider acquisition, private FootyStats call, production-model change, historical rewrite, or workflow rerun was performed for this audit.
