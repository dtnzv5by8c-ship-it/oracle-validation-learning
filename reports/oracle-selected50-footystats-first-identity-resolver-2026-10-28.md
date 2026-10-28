# FootyStats-First Dynamic Identity Resolver — 2026-10-28

## Decision

FootyStats is authoritative for the user-selected 50 league seasons. This research-only resolver uses each selected FootyStats season ID as the source anchor and derives a deterministic internal key `FS_SEASON_<season_id>`. That key is explicitly a research key, not a replacement for the protected production registry.

FotMob is optional reference evidence, not a prerequisite for reading FootyStats fixtures or creating research candidates. The resolver never assumes that FootyStats team IDs equal FotMob team IDs and never treats `comp_master_id` as an Oracle canonical ID.

## What the implementation does

- Accepts the existing sanitized FootyStats snapshot JSON plus a reference fixture/ledger CSV.
- Generates exact ordered-team candidates with UTC kickoff within a configurable tolerance; if kickoff precision is unavailable but the UTC calendar date agrees, it labels the result date-only.
- Generates fuzzy team-name leads only when exact team-pair candidates are absent. Fuzzy leads are never joins or approvals.
- Uses completed scores only as corroboration; two completed records with conflicting scores are quarantined.
- Quarantines settlement comparisons when either record lacks explicit completed status and scores.
- Emits source IDs, evidence type, confidence as candidate-only, conflict status, and reason for every candidate.
- Makes no API requests, reads no API key, makes no production writes, and approves zero mappings by design.

## Run locally or in the research workflow

```bash
python scripts/oracle_selected50_footystats_identity_resolver.py \
  --snapshot path/to/current-fixture-snapshot.json \
  --reference-csv path/to/existing-reference-fixtures.csv \
  --output oracle-selected50-current-fixture-snapshot/dynamic-identity-candidates.csv
python -m unittest discover -s tests -p 'test_oracle_selected50_footystats_identity_resolver.py' -v
```

The reference CSV should expose team names and kickoff/date fields. Supported home/away aliases include `home_team`/`away_team`, `home_name`/`away_name`, and `home`/`away`. Supported kickoff fields are `kickoff_utc`, `date_unix`, `kickoff`, and `date`. Score fields include `home_goals`/`away_goals` and FootyStats-style goal-count names. Reference league identifiers are carried as evidence only.

## Current release position

This implementation is a practical bridge around the FotMob-ID bottleneck for **research joins and source validation**. It does not itself make the protected production pipeline consume FootyStats, and it does not create certified model predictions. Production/betting eligibility remains NOT GRANTED until feature completeness, identity, settlement, point-in-time data and market-specific release gates are met. The existing Oracle production model logic and probabilities remain untouched.
