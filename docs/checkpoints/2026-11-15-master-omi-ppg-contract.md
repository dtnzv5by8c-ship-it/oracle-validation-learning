# Master OMI PPG Maintenance Contract — 2026-11-15

## Permanent requirement
The Market Intelligence layer must explicitly ingest and maintain three FootyStats provider fields for every applicable fixture/team/league record:

- PPG
- PPG Home
- PPG Away

## Controls
- Exact Fixture ID joins remain mandatory.
- Values must be pre-match and tied to the provider snapshot/as-of timestamp.
- Scope, denominator/sample, league/competition and venue scope must be preserved.
- Direct FootyStats fields are kept distinct from Oracle probabilities/signals.
- No provider field may be inferred from odds, settled results or another provider statistic.
- Missing provider fields are explicitly marked `UNAVAILABLE` / `PROVIDER_FIELD_MISSING`.
- Each field carries explicit source, provenance, status and quality metadata.
- Existing PPG/GF/M/GA/M denominator audits remain fail-closed for duplicate IDs, chronology, mapping and minimum-sample failures.
- Oracle V1.6 production logic, thresholds, calibration, betting eligibility, governance and protected Market Intelligence A:ET are unchanged.

## Implementation
Commit: 511baf7e1a2f3f07ed53637d89c13ca47e367f4c

The Master OMI Excel workflow now creates explicit fixture-level columns for both sides:
- FS Home PPG
- FS Home PPG Home
- FS Home PPG Away
- FS Away PPG
- FS Away PPG Home
- FS Away PPG Away

Each field also receives Status, Source, Provenance and Quality metadata. When FootyStats does not supply the field, the value is `UNAVAILABLE` and the status is `PROVIDER_FIELD_MISSING`.

## Maintenance interpretation
This is an ingestion/quality contract, not a production-model promotion. Direct provider values may be maintained even when a research signal has not been promoted. Research validation remains separately governed.
