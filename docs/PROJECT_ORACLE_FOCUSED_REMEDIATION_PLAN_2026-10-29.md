# Project Oracle — Focused Remediation Plan (2026-10-29)

This plan replaces repeated blocker summaries with explicit closure tests. Research branch only; production model logic, frozen probabilities, thresholds, calibration, and production ledgers are not modified.

## Immediate design correction: one identity namespace per field
Oracle currently has at least three separate ID namespaces:
1. FootyStats season ID (50/50 provider responses verified)
2. FootyStats comp_master_id (50 values returned; provider field semantics captured but not promoted automatically)
3. Existing Oracle/source-specific league keys (e.g. Football-Data codes and SportMonks league IDs).

Do not overwrite or conflate them. Build a governed bridge with columns: oracle_league_code, oracle_canonical_competition_id, provider, provider_competition_id, provider_season_id, country, provider_competition_name, season, mapping_basis, evidence_uri, status, reviewed_at. Allowed statuses: VERIFIED_EXACT, VERIFIED_ALIAS_WITH_EVIDENCE, PROVIDER_ONLY_UNMAPPED, CONFLICT, NOT_IN_ORACLE_UNIVERSE. Exact fixture/team joins remain a separate gate. Never use name-only fuzzy matching to promote a mapping.

### Closure test 1 — Competition identity
- Verify all 50 rows against Oracle canonical/source registries and provider documentation.
- Automatically verify only exact IDs or aliases with documented evidence.
- Mark provider-only rows as NOT_IN_ORACLE_UNIVERSE until an approved source mapping exists.
- Pass criterion: all 50 rows have a terminal, explicit status; zero unlabelled/guessed mappings. This does not require all 50 to be production-supported.

### Closure test 2 — Combo settlement definition
Production governance documents Combo as Double Chance + Under 4.5, i.e. the DC outcome is true and total goals are 0–4. This is the governing definition for research diagnostics. The older 2–4 target is a conflicting research implementation, not a reason to change frozen production predictions. Keep existing frozen probabilities unchanged; rebuild only a separately labelled research settlement comparison under the documented definition. Settlement requires finished status plus valid final score and source provenance; numeric scores on non-finished rows are never settled.

- Pass criterion: one documented definition used by the research diagnostic; predictor/helper agreement measured; official settlement source status shown. If historical official settlement provenance cannot be established, mark settlement truth provisional and do not promote.

### Closure test 3 — Point-in-time feature provenance
- Use only fields with timestamped pre-kickoff snapshots or immutable provider snapshots demonstrably captured before kickoff.
- Exclude actual/post-match xG, standings without as-of timestamps, and odds without capture timestamps from historical backtests.
- Do not infer that fields are pre-match from their column names.
- Pass criterion: every included feature has source, observed_at, kickoff_at, and observed_at < kickoff_at. Missing proof means excluded, not imputed.

### Closure test 4 — Exact fixture/team joins and current feature coverage
- Join by provider fixture ID and provider team IDs first; aliases are an evidence-backed bridge only.
- Keep the 24 of 435 current rows that lack required features blocked; no imputation.
- Quarantine unknown/future-complete, canceled, suspended, or home/away-ambiguous rows.
- Pass criterion: every current fixture receives a join outcome and per-market readiness status; no silent row drops or inferred team matches.

## Priority order
P0: research-only Combo definition reconciliation (no provider calls required).
P1: identity bridge with explicit terminal statuses, using the already completed 50-call probe; no repeat calls unless an individual row is unresolved and a specific endpoint is justified.
P2: feature provenance exclusion rules, then rerun only historical validation on the leakage-safe subset.
P3: exact fixture/team join coverage for the current fixture slate.
P4: publish a per-league/per-market readiness matrix and release decision.

## Release rule
A workflow pass is not production readiness. The 50-league universe can be declared operationally inventoried when every league has an explicit support status. Production release remains NOT_GRANTED for any league/market that fails canonical joins, settlement truth, freshness, or point-in-time provenance. Do not change production logic to make a gate green.
