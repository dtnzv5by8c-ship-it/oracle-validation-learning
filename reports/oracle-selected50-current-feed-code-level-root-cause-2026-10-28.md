# Selected-50 Current-Feed Code-Level Root Cause — 2026-10-28

**Disposition:** Root cause of identity contamination is confirmed in the current-ingestion implementation. This is a read-only code review; no production files changed and no API calls were made.

## Exact source reviewed

- Production repository: `dtnzv5by8c-ship-it/oracle-football-data`
- Branch inspected: `fix/epl-btts-team-state-aliases`
- `scripts/ingest_current_fotmob.py`, blob `cdde6c9d0d583626b9a993d6f59aac67cb41c4c9`
- `config/data_config.json`, blob `60b74f53222ec69853d303066beb5f27053f1edc`
- Research evidence: `reports/oracle-50-league-current-feed-identity-collision-audit-2026-10-25.csv`

## Root cause confirmed

The current ingestion script creates `TARGET_LEAGUES` from the values of `season_leagues` and `extra_all_seasons` in `config/data_config.json`. For every date, it fetches FotMob `matches` data and admits a league solely when:

```python
league_name = league.get("name", "")
if league_name not in TARGET_LEAGUES:
    continue
```

It then writes the match's `league_id` to `current_matches.csv`, but the admission decision has already been made on display name alone. The row does not retain the league country/category, and the code does not enforce an exact approved league-ID allowlist for the selected competition. Thus `league_id` is recorded as data but is not used to guard admission. Repeated names such as “Premier League”, “Bundesliga”, “Serie A” and “Ligue 1” can admit fixtures from unrelated competitions.

The script does produce `data/current_source_manifest.json` with `generated_utc`, requested dates, per-request SHA-256 values, errors and row counts. However, the reviewed public research repository does not contain the live production copy of that manifest or the latest private `current_matches.csv`; therefore this review cannot establish the live feed's last ingestion time or whether its scheduler succeeded today.

## Exact corrective design — proposed, not applied

1. Add an explicit, reviewed `current_feed_league_allowlist` keyed by canonical competition code, with the exact provider/FotMob league ID and country/category expected for each entry. Populate it only from authoritative, human-approved evidence; do not derive IDs from display names or provider season IDs.
2. At ingestion, require the incoming league ID to match the allowlist entry. Where the source supplies country/category, require that value to match too. If ID or country/category is missing, unknown, conflicting or ambiguous, quarantine the row and record a structured rejection reason.
3. Persist `league_id`, `league_name`, `country/category`, `canonical_competition_code`, `allowlist_version`, and an explicit `identity_status` in the staging output. Preserve source match ID, UTC kickoff, status and source provenance.
4. Generate the feed manifest with per-date request status, timestamps, counts, error totals, source cutoff and output checksum. Fail the freshness gate if required dates fail, the source window is stale, or manifest/output checksums disagree.
5. Add regression tests proving that (a) same-name competitions with different IDs cannot cross-admit; (b) wrong country/category is quarantined; (c) unknown IDs are rejected; (d) exact approved IDs are admitted; (e) failed date requests make completeness/freshness fail closed; and (f) the legacy name-only path is not accepted.
6. Run in research/staging first against fixtures covering known collisions. Compare admitted/rejected counts and verify no cross-competition contamination before a separately reviewed production PR.

## What this fixes and what it does not

This design fixes the confirmed **identity admission** defect when approved IDs are available. It does not by itself verify that the 50 FootyStats season IDs map to 50 parent competitions, refresh the live feed, verify fixture/team joins, or settle official market outcomes. Those remain separate gates.

## Current evidence

The existing 50-row collision audit found 38 groups with no matching display label, 5 ambiguous label groups and 7 label hits lacking country evidence. Approved provider-season-to-FotMob bridges remain 0/50. No league ID is being promoted to canonical based on this review.

## Governance and next action

No production code/configuration, Oracle model logic/probabilities, thresholds, calibration, protected registry or ledgers were changed. No provider requests were made. The production patch should be a narrowly scoped ingestion identity-contract change only after the allowlist is sourced and reviewed; do not reactivate legacy ingestion or bypass the protected-repository guard.

**Release decision remains NO-GO** until the allowlist/bridges are approved, the live manifest is checked, and exact fixture/team/settlement joins pass.
