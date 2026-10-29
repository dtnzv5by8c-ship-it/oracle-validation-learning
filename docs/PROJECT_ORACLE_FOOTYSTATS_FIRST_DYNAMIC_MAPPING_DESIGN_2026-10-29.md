# Project Oracle — FootyStats-First Dynamic Identity and Join Design
Date: 2026-10-29
Scope: Research-only design; no production model, probability, threshold, ledger, or governance changes.

## Executive decision
Use FootyStats as the primary provider identity for the selected 50 league-season feeds, but do not treat a season ID as a permanent competition ID. FootyStats' public League List documentation explicitly says each season of a competition has a unique ID. Retain both:
- `footystats_season_id`: immutable season-scoped provider key (e.g. selected season ID in the current probe).
- `footystats_comp_master_id_observed`: provider-supplied parent/master identifier, retained as a candidate stable competition key; verify its stability across multiple seasons before treating it as stable.
- `oracle_canonical_league_code`: internal governed identity, populated only when supported by Oracle configuration or approved evidence.
- `season_start_year`, `season_end_year`, `competition_name_raw`, `country_raw`, `source_snapshot_at`, `evidence_url`, `mapping_status`, `mapping_confidence`, `reviewed_at`.

No provider-only ID should be silently promoted to an Oracle canonical ID.

## What public documentation confirms
1. FootyStats League List: each competition season has a unique ID; the endpoint returns available leagues/seasons. https://footystats.org/api/documentations/league-list
2. FootyStats API FAQ: data availability and historical coverage vary by league; coverage must be checked per competition/season. https://footystats.org/api/documentations/faq
3. FotMob's public API community documentation describes league IDs and fixture IDs, but also notes FotMob terms may restrict automated/systematic retrieval. Treat those endpoints as evidence only when access is authorized and contractually permitted. https://github.com/pseudo-r/Public-FotMob-API
4. The official EFL competition page provides a public reference for EFL League One naming and results; use the competition organizer's source to resolve naming, not to infer provider IDs. https://www.efl.com/competitions/efl-league-one/

## Dynamic join ladder
Use a deterministic, auditable ladder. Stop at the first unique match; never force a join.

### Tier A — provider-native exact ID
Join when the same provider fixture ID exists in both sources and the source system is explicitly the same. Record the ID namespace and provenance. Never compare raw IDs across providers as if they shared a namespace.

### Tier B — exact cross-provider fixture key
Require all of:
- same approved competition bridge (country + competition identity / approved provider league ID);
- normalized ordered home and away team names (or approved team-ID bridge);
- exact kickoff timestamp normalized to UTC, within a strict documented tolerance only if source timestamp precision is known;
- unique candidate in each source.
Scores and result status are validation fields, not join keys. A mismatch quarantines the row.

### Tier C — historical source-ID recovery
For the Oracle historical ledger, first test whether `source_match_id` and `source` can be recovered from the original source extract or build manifest. Existing ledger rows have synthetic-looking IDs such as `ROU-...` and blank source/source_season/source_match_id in the audited export, so they cannot be treated as provider-native IDs without provenance. If a source ID can be reconstructed from archived build outputs, retain the lineage and use it as the preferred join.

### Tier D — date-only candidate (never auto-approve)
If the ledger has date but no kickoff time, match normalized ordered teams + UTC calendar date + approved competition bridge, then produce a candidate queue. Require at least one independent corroborator (official fixture page/official match report, provider fixture ID, or an archived timestamped source). Score agreement alone is insufficient. If multiple matches remain, quarantine as ambiguous.

### Tier E — name-only or fuzzy candidates
Candidate discovery only; never production eligible without human review and independent evidence. Use aliases only when explicitly sourced and versioned.

## Canonical competition mapping
- Maintain a canonical competition table independent of any one provider.
- Map FootyStats `season_id` to canonical competition + season; map `comp_master_id` as a candidate provider family ID after cross-season stability checks.
- Maintain provider aliases by effective dates (competition renames, league restructures, promoted/relegated team aliases).
- Record the evidence source, retrieval timestamp, approval status and reviewer for each cross-provider bridge.
- Treat FotMob league ID/name as an independent source-specific mapping, not a canonical key.
- Current audit's Canada row (FootyStats Canadian Premier League vs observed FotMob label “Premier League”) remains quarantined despite four exact fixture rows; the snapshot contains a pre-kickoff row and the league label needs resolution.
- Current EFL League One row is a strong candidate, but must still be approved as a competition bridge before bulk use.

## Historical validation safeguards
- Keep finished/complete status explicit; numeric scores on suspended, postponed, cancelled or otherwise non-finished rows are not settlement truth.
- Require immutable feature observation time strictly before kickoff for every feature used in historical validation.
- Require source capture time for odds and standings-as-of time; exclude post-match xG and un-timestamped values.
- Keep outcome truth, fixture identity, feature provenance and model prediction as separate columns.
- Use walk-forward/time-split validation only after eligibility gates pass; report coverage and performance by league and market.
- Do not recalibrate frozen probabilities or modify production model logic in this research stream.

## Current evidence-backed state
- Selected-50 FootyStats probe: 50/50 season responses and country/competition name matches; all have observed `comp_master_id` values, but the current evidence is one season per competition and does not prove cross-season stability.
- Cross-provider audit: 10 exact UTC kickoff FootyStats↔FotMob fixture joins across two selected seasons; 0 exact historical-ledger kickoff joins because the exported ledger has date-only values.
- Historical ledger: 12,836 rows, 12,836 date-only, 577 candidate overlaps across 24 groups, 0 score conflicts among those candidates. These are candidates, not exact joins.
- FotMob bridge candidates: Canada/Canadian Premier League (4 exact fixture joins, 1 pre-kickoff snapshot row, label mismatch) and England/EFL League One (6 exact fixture joins, 3 known score agreements).
- Approved canonical bridges from this audit: 0. Production eligibility: false.

## Next implementation sequence
1. Add a research-only canonical competition registry seeded with the 50 FootyStats identities and explicit status/evidence columns.
2. Add a cross-season stability check for `comp_master_id` using already archived FootyStats season metadata before classifying it as stable.
3. Recover original source lineage for Oracle ledger rows; if not recoverable, keep the date-only candidate queue quarantined.
4. Add official-source evidence for the two FotMob candidate leagues and validate the Canada label anomaly without relying on unauthorized scraping.
5. Produce a machine-readable mapping review pack and exact fixture bridge report. Only after reviewed/approved bridges exist should it feed the historical validation dataset.

## References
- FootyStats League List: https://footystats.org/api/documentations/league-list
- FootyStats FAQ: https://footystats.org/api/documentations/faq
- FootyStats API overview: https://footystats.org/api/documentations
- Official EFL League One page: https://www.efl.com/competitions/efl-league-one/
- FotMob public API community notes (access/terms caution): https://github.com/pseudo-r/Public-FotMob-API
