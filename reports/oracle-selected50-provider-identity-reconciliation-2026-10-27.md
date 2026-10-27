# Selected-50 Provider Identity Reconciliation — Initial Evidence

**Evidence source:** Oracle Selected-50 Provider ID Schema Diagnostic run #9, run ID `40548721202`  
**Artifact:** `oracle-selected50-schema-diagnostic` (SHA-256: `a993aa11e7de8aa1b4415c9a564c843cb3180bbb6754670f0f45c81426ca52c5`)  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Status:** `PARTIAL — PARENT COMPETITION IDS AND ORACLE CANONICAL IDS NOT VERIFIED`

## Findings

- Selected manifest rows: **50**; unique selected IDs: **50**.
- Provider catalogue rows examined: **50**; season objects examined: **766**.
- Selected IDs matched within provider `season.id`: **50/50**.
- Selected IDs matched within direct provider league-level ID fields: **0/50**.
- Unmatched selected IDs in the examined ID fields: **0**.
- Raw provider payload saved: **no**; API key printed/saved: **no**.
- Full match ingestion: **not performed**; production files changed: **no**.
- The provider catalogue’s league objects exposed keys `country`, `image`, `name`, `season`; season objects exposed `country`, `id`, `year`. The diagnostic found no direct ID field on the league object. Therefore the selected IDs are season-level IDs, not verified parent competition IDs.

## Mapping table interpretation

The accompanying CSV records each manifest ID and its matched provider season name/year. It deliberately leaves `provider_parent_competition_id` and `oracle_canonical_league_id` blank and labels each row `SEASON_ID_MATCH_PARENT_ID_MISSING`. Provider display names often include a country prefix (for example, manifest `Premier League` vs provider `England Premier League`); these are candidate name correspondences for review, not proof of canonical identity.

## Decision and next action

1. Keep all 50 parent competition mappings **unverified** until a provider field or authoritative source explicitly links each season ID to a stable parent competition ID.
2. Do not infer parent IDs from season IDs, names, or the `year` value.
3. The current one-call diagnostic did not return parent IDs. Before any further API request, inspect existing archive and workflow artifacts for already captured competition/season bridge fields. If absent, prepare a separately bounded, explicitly approved diagnostic that retrieves only the missing bridge data; no broad ingestion.
4. Join each verified parent competition to Oracle's canonical league registry only after both sides have stable identifiers and evidence provenance.
5. Production and betting eligibility remain **NOT GRANTED**; no production model logic or probabilities were changed.

## Artifact lineage

The evidence was derived from the sanitized schema summary only. The monthly provider credit balance is not independently verified by the artifact; the artifact explicitly records `monthly_credit_budget_verified=false`.
