# Oracle Selected-50 Execution Review — 25 October 2026

## Current verified state

- Provider diagnostic #1 succeeded: all 50 selected IDs were found as nested season IDs; none matched a direct league-level ID field.
- The Run 56 archive contains exact season-ID matches for 31 of the 50 selected IDs. Nineteen selected IDs are absent from that archive mapping.
- The historical ingestion workflow in the private repository uses a fixed alias dictionary for the legacy 27-league scope. It is not driven by the selected-50 manifest.
- The catalogue-transfer workflow reads `league.get('id')` for `provider_league_id`, but the diagnostic's sampled league objects did not expose a direct `id`. The archive mapping's provider league ID column is blank in the inspected 126 rows.

## Safe next action

Do not modify production logic or run historical ingestion automatically. First create a research-only manifest validation and coverage plan for the 50 exact season IDs; preserve `provider_season_id` separately from `provider_competition_id`. Inspect downstream consumers before changing any shared mapping schema. For the 19 absent IDs, report only evidence-backed states (present, absent from inspected archive, request failed, or not requested); do not infer a cause without the ingestion manifest or request logs.

## Gate status

Production eligibility remains NOT GRANTED. Selected-ID-to-fixture/team joins, current feed freshness, as-of-kickoff xG/odds provenance, and per-market readiness remain unverified. No production changes or provider ingestion were performed in this review.
