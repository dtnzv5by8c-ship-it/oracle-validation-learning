# FootyStats Identity Clarification — Request Draft (2026-10-27)

**Purpose:** obtain authoritative clarification without making another API request or changing Oracle production.

## Context

Oracle is reconciling a governed set of 50 selected FootyStats league/season identifiers. A read-only `league-list?chosen_leagues_only=true` schema diagnostic (workflow run `40548721202`) found:
- 50/50 selected identifiers matched a `season.id` field.
- 0/50 selected identifiers matched a direct ID field on the league object.
- The inspected league objects exposed `country`, `image`, `name`, and `season`; season objects exposed `country`, `id`, and `year`.
- The sanitized summary did not expose a documented stable parent competition identifier.

The published [League List documentation](https://footystats.org/api/documentations/league-list) describes unique IDs per season. We do not want to infer a parent competition identifier from a season ID.

## Questions for FootyStats support

1. Does the League List API expose a stable competition/league identifier distinct from each `season.id`?
2. If yes, what is the exact response field name and which endpoint/version returns it?
3. If no, what is the recommended stable identifier for mapping a season across years to the same competition?
4. Are `season.id` values intentionally unique per season, and should clients treat them strictly as season identifiers?
5. Is there an official data dictionary or schema reference that documents the relationship between a league object and its nested season objects?

## Minimal evidence requested

Please provide a documentation link or a redacted sample response showing the relevant fields and their semantics. No API key or customer-specific information is required.

## Oracle controls

- This request draft does not call the API.
- No provider IDs are inferred or promoted.
- No production registry, model logic, probability, calibration, threshold, or prediction gate is changed.
- Parent competition IDs remain blank until supported by explicit provider evidence.
- Production/betting eligibility remains `NOT_GRANTED`.

## Closure criteria

Identity blocker can be closed only when the response provides either:
- an explicit, documented stable parent competition field and a verifiable mapping for the selected seasons; or
- explicit provider confirmation that no parent identifier is exposed, plus a formally approved alternative identity contract that preserves season IDs as season IDs and does not fabricate parent IDs.

**Status:** `DRAFT — NOT SENT`. Sending requires the account holder to submit this text through the provider's support channel.
