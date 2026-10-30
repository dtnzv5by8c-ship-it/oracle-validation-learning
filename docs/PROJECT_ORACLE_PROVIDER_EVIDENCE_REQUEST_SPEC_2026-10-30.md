# Project Oracle — Provider Evidence Request Specification
**Prepared:** 30 October 2026  
**Branch:** research/oracle-50-league-readiness-audit  
**Disposition:** research-only requirements document; not a provider communication and not an approval to change production.

## Purpose
Define the minimum evidence required to close the selected-50 identity, fixture chronology, point-in-time feature and market-settlement blockers. This document is a technical acceptance contract. A provider response is evidence to review, not automatic approval.

## P0 — Competition identity contract (FootyStats)
Request written answers and a versioned schema reference for:
1. The precise meaning and scope of `comp_master_id`.
2. Whether it is stable across seasons, rebrands, promotions/relegations, competition format changes and country/region changes.
3. Whether one value can map to multiple season IDs, and whether a season ID can map to multiple master IDs over time.
4. The relationship among league-catalogue `id`, match-record `competition_id`, and `comp_master_id`.
5. Deprecation, reassignment and historical backfill behaviour; effective dates and change logs.
6. Whether the field is intended as a durable competition key for third-party crosswalks.

**Acceptance evidence:** provider documentation or signed written response defining semantics and lifecycle; observed values for at least two seasons for each of the 50 selected competitions; reproducible season-to-master mapping; explicit exception list. Do not promote any field to Oracle canonical identity on name similarity or a single-season observation.

## P0 — Historical fixture and team identity
Request:
1. Stable fixture ID and its uniqueness scope (global, season, or competition).
2. Stable home-team and away-team IDs, including ID lifecycle and alias/rebrand handling.
3. Exact kickoff timestamp, timezone and precision; rescheduling history and original/current kickoff fields.
4. Status vocabulary and transition semantics, including postponed, suspended, abandoned, canceled, awarded, incomplete and complete.
5. Whether fixture IDs or team IDs can change after publication, and how corrections are exposed.

**Acceptance evidence:** historical fixture-level export for the governed validation window (2025-03-20 through 2026-09-20) with stable fixture/team IDs, UTC kickoff, status history and retrieval/observation timestamps. Reconcile a stratified sample against independent official sources. Preserve exact joins; no fuzzy or date-only join may be promoted.

## P0 — Point-in-time feature provenance
For `team_a_xg_prematch`, `team_b_xg_prematch`, `total_xg_prematch`, BTTS odds and Double Chance odds, request:
1. Definition, units, market/bookmaker identity and whether values are estimates, consensus or executable prices.
2. First-available timestamp, last-updated timestamp, source timestamp and timezone.
3. Whether historical values are point-in-time snapshots or retrospectively recomputed values.
4. Update cadence, correction/backfill policy and missing/zero/null semantics.
5. For odds, bookmaker identity, market line/selection mapping, suspension/settlement handling and whether values represent opening, closing or latest prices.

**Acceptance evidence:** immutable timestamped historical snapshots or a provider-supported point-in-time endpoint; sample payloads with observation timestamps before kickoff; documented zero/null semantics; reproducible tests proving no post-kickoff values enter a pre-match feature row. Field presence or a numeric zero is not proof of availability or validity.

## P0 — Neutral / no-home-away semantics
Request the formal definition and trigger rules for `no_home_away`, including neutral venues, tournament legs, group-stage matches, rescheduled fixtures and fixtures with reversed nominal home assignment. Confirm whether home/away IDs and statistics remain meaningful when set.

**Acceptance evidence:** provider contract plus representative fixture examples and recommended market handling. Until a reviewed feature/market contract exists, keep affected home/away-dependent markets quarantined.

## P0 — Market settlement contract (Oracle / production market owner)
Obtain the authoritative settlement rules for:
- BTTS Yes: regulation time, extra time, abandoned/postponed/awarded matches, own goals and data corrections.
- Double Chance 1X and X2: eligible match period, abandoned/postponed/awarded matches and settlement correction rules.
- Combo Home/Away: exact leg definition, order, settlement and void rules.

**Acceptance evidence:** versioned official market specification, identified settlement source of truth and approved fixture-level historical outcomes. Cross-provider score agreement and public result URLs alone do not constitute settlement truth.

## Required delivery format
Ask the provider to supply:
- Versioned field dictionary and status dictionary.
- CSV or JSONL fixture history with stable IDs and UTC timestamps.
- Point-in-time feature/odds history with observation timestamps.
- Change log for competition/team/fixture ID corrections.
- Explicit coverage and known limitations for all 50 selected competitions and each season from 2024 onward.
- A named technical contact and documentation version/date.

## Oracle-side review and release gates
1. Store raw licensed payloads only in the private archive; publish sanitized metadata/checksums only.
2. Validate schema, uniqueness, chronology, timestamp timezone, ID stability and completeness offline.
3. Reconcile competition and team identities independently; candidate mappings remain unapproved until human-reviewed.
4. Quarantine source conflicts, non-final scores, missing IDs, date-only joins, unknown status and no-home-away rows.
5. Prove feature observation time precedes kickoff for every eligible historical feature row.
6. Reconcile market outcomes against the official settlement specification.
7. Run walk-forward validation only after identity, chronology, feature and settlement gates pass.
8. Keep Oracle V1.6 production logic/probabilities unchanged; all work remains on the research branch.
9. Keep `production_eligible=false` and `betting_eligible=false` until explicit governance approval and all gates pass.

## Current known blockers this request is intended to address
- `comp_master_id` semantics and cross-season stability are undocumented.
- Historical ledger rows lack exact kickoff timestamps for canonical joins; existing historical exact-join count is zero.
- Prematch xG and odds numeric fields lack proven point-in-time provenance.
- Official settlement truth and the Combo settlement definition remain unverified.
- Existing exact cross-provider matches are candidate evidence only; no canonical bridges have been approved.

## Explicit non-goals
This request does not authorize a new model, model redesign, production code changes, probability/calibration changes, fabricated or imputed data, automatic canonical mapping, provider API calls, or production/betting release.
