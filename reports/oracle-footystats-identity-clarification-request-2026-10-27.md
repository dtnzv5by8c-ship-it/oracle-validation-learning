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


---

## Update — support route verified and improved email draft (2026-10-27)

**Status remains: DRAFT ONLY — NOT SENT.**

### Verified provider contact route

The official FootyStats [API Overview](https://footystats.org/api/documentations) explicitly says API questions and requests are welcome at **admin@footystats.org**. This is the recommended first route for this schema/identity question. The official [FootyStats About page](https://footystats.org/about) also directs customer support to its Contact Us page. No message has been sent, and no additional API call is requested or authorized.

### Suggested subject

**Clarification requested: stable competition ID versus season ID in Football Data API**

### Refined draft email

**To:** admin@footystats.org

Hello FootyStats API Support,

We are validating the identity fields used by the Football Data API and need to distinguish a season identifier from a stable competition/league identifier before we build a cross-season mapping.

Your [League List documentation](https://footystats.org/api/documentations/league-list) says each season of a competition has a unique ID and shows the ID nested under `season.id`. Your [League Stats / Get Season Stats and Teams documentation](https://footystats.org/api/documentations/league-season-stats-teams) describes `data.id` as the season ID, but the displayed example request uses `season_id=2012` while the sample response shows `data.id="161"` and season `2017/2018`. Separately, the [League Matches documentation](https://footystats.org/api/documentations/match-schedule-and-stats) describes the required `season_id` parameter as the league-season ID and labels the match-level `competition_id` field “Season ID of the league.” We do not interpret that field label as evidence of a stable parent competition identifier. We would appreciate clarification of the example mismatch and the intended identifier semantics.

We completed one explicitly approved, read-only diagnostic for selected season ID `16571`. It returned `data.id=16571`, name `Primera División`, country `Argentina`, and season/start/end year `2026`. We are treating this as evidence about that one season record only; we are **not** treating the value as a parent competition ID or extrapolating it to other seasons.

Could you please confirm:

1. Is there a stable competition/league identifier distinct from each `season.id`?
2. If it exists, what is the exact field name and documented endpoint that returns it?
3. Is that identifier stable across seasons of the same competition? If not, what provider-supported key should a client use to group seasons without conflating different competitions?
4. Does `league-season.data.id` always identify the requested season, or can it identify a parent competition? Please clarify the apparent mismatch in the published example.
5. The League Matches documentation labels the match-level `competition_id` field “Season ID of the league.” Is this field season-scoped, and is any distinct stable parent competition field exposed elsewhere?
6. Is there an official data dictionary or a redacted example showing the relationship between the league object, season object, match-level `competition_id`, and any parent competition identifier?
7. If a stable parent ID is exposed, can you provide a documented crosswalk for the selected season IDs in the attached manifest, including country, competition name, season ID, and parent competition ID? If no parent ID is exposed, please confirm that explicitly.

We do not need a new API call, account-specific information, or disclosure of credentials for this clarification. A link to authoritative documentation or a written explanation of the field semantics would be sufficient. We can provide the 50-row selected manifest as a separate attachment if useful.

Thank you for your help.

Regards,  
Project Oracle data validation

### Evidence attachment suggested for the account holder

Attach `reports/oracle-selected50-independent-identity-evidence-register-2026-10-27.csv` or the simpler selected manifest. The CSV is research-only and marks all mappings unapproved. Do not include API keys, raw provider payloads, or private credentials.

### Additional official-documentation finding (2026-10-28)

The public League Matches reference describes the match-level `competition_id` field as the **season ID of the league**. This is a naming ambiguity, not evidence of a stable parent competition ID. The revised questions explicitly ask FootyStats to confirm that field's semantics. The request remains **DRAFT ONLY — NOT SENT**.

### Governance after this update

- The existing one-call result remains the only approved provider call for this identity question.
- No further provider API calls are authorized without fresh explicit approval and a verified credit budget.
- Parent competition IDs remain **0/50 verified**; provider-to-canonical bridges remain **0/50 verified**.
- The email remains a draft and must not be sent by an automation or agent. Sending requires separate approval from the account holder.
- Production and betting release remain `NOT_GRANTED`.
