# Selected-50 Gap Investigation — 25 October 2026

## Evidence added by this review

The Run 56 artifact was inspected directly, including:
- `audit-output/extracted/private-package/league_season_mapping.csv`
- `audit-output/extracted/private-package/ingestion_manifest.csv`
- `audit-output/extracted/private-package/ingestion_errors.json`

The manifest contains the legacy ingestion's recorded seasons and statuses. The error JSON is an empty list. The mapping/ingestion manifests are finite, with 126 season rows. The `provider_league_id` field is blank in these rows.

## Findings

1. The 19 selected IDs previously listed as absent are **absent from the inspected archive mapping**. That statement is evidence-backed.
2. The empty archived error list means we cannot attribute these gaps to provider request failures from this artifact.
3. The ingestion manifest records only the season rows the legacy workflow produced. It does not provide a complete attempt ledger for all 50 selected IDs, so it cannot distinguish “not requested” from “requested but omitted before manifest creation” for every missing ID.
4. The workflow source uses a fixed alias dictionary for legacy Oracle codes. This explains why the archive package is not a selected-50 manifest-driven ingest. It is the strongest evidenced scope limitation; it does not prove the provider lacks data for any missing league.
5. Exact parent competition IDs are still unavailable in the inspected catalogue response. Season IDs must not be written into the parent competition field.

## Safe engineering decision

Do not patch the private production ingestion workflow in place. Build the selected-50 work as a separate research-only pipeline with:
- the existing 50-row selected-season manifest as the only allowed scope;
- strict unique-ID and nonblank checks;
- a dry-run plan by default with **zero API calls**;
- estimated request count reported before any live calls;
- per-ID states `IN_SCOPE_NOT_REQUESTED`, `REQUESTED_SUCCESS`, `REQUESTED_FAILED`, `ARCHIVE_MATCHED`, `ARCHIVE_ABSENT`;
- separate `provider_season_id` and `provider_competition_id` fields;
- no fuzzy mapping, silent alias substitutions, raw API keys, or raw response payloads in logs;
- a required explicit approval before live historical acquisition;
- downstream QA for match IDs, team identities, dates, status/score settlement, recent form, historical standings as of kickoff, H2H, and pre-kickoff xG/odds provenance.

## Status

- Manifest validator: PASS.
- Live schema diagnostic: PASS for season-level ID semantics.
- Archive: 31/50 exact season IDs matched; 19/50 absent from inspected mapping.
- Root cause: legacy fixed-scope ingestion is not driven by selected-50 manifest; parent league ID extraction is inconsistent with the observed schema.
- Selected-50 ingestion and end-to-end join validation: NOT COMPLETE.
- Production eligibility: NOT GRANTED.
- Provider API calls and production changes in this review: none.
