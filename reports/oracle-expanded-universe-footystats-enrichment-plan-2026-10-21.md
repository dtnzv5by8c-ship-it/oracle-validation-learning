# Project Oracle — Expanded League Universe and FootyStats Enrichment Plan
Date: 2026-10-21
Status: research/reporting scope only; production registry unchanged.

## Decision
The owner has requested that FootyStats historical enrichment cover Oracle's expanded universe, currently estimated at 44 leagues, rather than treating the previous 27-league active registry as the full research scope.

## Verified repository state
- The protected production registry `config/oracle_major_league_registry_v1.json` currently declares `active_universe.league_count = 27`.
- The existing FootyStats archive was ingested from the provider's selected catalogue for season-start years 2024, 2025 and 2026.
- The archive manifest contains 42 distinct provider competition names and 126 season entries, with 35,819 match records.
- The earlier selected-catalogue audit reported 43 distinct provider competition names. The 42-vs-43 difference is unresolved.
- Provider competition names are not automatically Oracle league IDs. Cups, supercups, aliases, reserve/youth competitions, and duplicate naming variants must be classified before inclusion.
- Therefore the 44-league canonical list is not yet proven by the registry or the provider archive alone.

## Scope for the next enrichment pass
1. Preserve the current 27-league registry and production logic unchanged.
2. Treat every successfully acquired FootyStats competition as a research candidate until it is mapped to a canonical Oracle league ID and classified as league/cup/other.
3. Reconcile the provider catalogue, ingestion manifest and intended 44-league list into a versioned crosswalk with explicit states: MATCHED, ALIAS_REVIEW, CUP_OR_NONLEAGUE, NOT_INGESTED, SEASON_GAP, and DATA_GATED.
4. For every matched candidate and season, profile results/statuses, team IDs/names, goal-event arrays, xG fields, odds, tables, season stats and match counts.
5. Build chronological features only from records strictly before each target kickoff: last 3/5/10 matches, home/away form, H2H, goals for/against, BTTS and totals frequencies, and reconstructed historical table position. Respect season boundaries and competition split formats.
6. Do not use actual-match xG as a pre-match input. Do not accept fields labelled “prematch” until their point-in-time availability is evidenced. Missing features stay missing and are flagged.
7. Produce research feature tables and coverage/error reports as private artifacts. Preserve provider IDs, source season IDs, source timestamps, fixture identity, feature cutoff and provenance.
8. Evaluate feature groups separately by market using chronological out-of-sample splits and proper probability metrics. Do not call research metrics production accuracy.
9. Do not alter model weights, thresholds, production probabilities, model version, or protected registry. No PR merge or paid-plan change without explicit approval.

## Completion gates
- Canonical intended league list reconciled to exactly 44 (or owner-confirmed revised count).
- Every candidate mapped or explicitly excluded with a reason.
- Season/field coverage quantified per league-season, with no assumed completeness.
- Result status and goal-score parsing validated, including 0-0 and event-array representation.
- H2H and recent-form cutoffs verified against target kickoff; no future-data leakage.
- xG and odds provenance either verified or excluded from pre-match validation.
- Historical standings reconstructed from prior results, not final/current snapshots.
- Fixture joins exact and auditable; ambiguous rows are not silently joined.
- Walk-forward evaluation completed and reported with sample sizes, coverage, calibration and uncertainty.
- Incremental scheduled workflow runs from existing public runner, uses private archive/token, avoids repeated full downloads, and fails closed when data gates fail.
- Production promotion remains a separate approval decision.

## Current blocker
The exact 44 canonical league IDs/names have not been established by the protected 27-league registry or the 42-name provider archive manifest alone. Continue archive-wide research on the available provider competitions, but do not invent the missing league identities or silently edit the production registry.
