# FootyStats-First Source Adapter — 2026-10-28

## Purpose

This is the source-ingestion seam for the selected 50 FootyStats league seasons. It consumes the existing sanitized snapshot and writes a provider-neutral research fixture feed without calling FotMob, using secrets, fabricating FotMob IDs, or writing production files.

## Output contract

Each row preserves the FootyStats season ID, match ID, home/away team IDs, competition metadata from the selected manifest, UTC kickoff, source status, source scores and provider-native pre-match market values. The adapter also emits a deterministic research league key `FS_SEASON_<season_id>` and explicit fixture eligibility/quarantine reasons.

## Fail-closed guards

- Exactly 50 unique selected seasons must be present and each must show verified HTTP 200 plus provider success.
- Every fixture must reference one of those selected seasons and have a source-native match ID.
- Duplicate (season ID, match ID) pairs fail closed.
- Missing teams, invalid kickoff, suspended/postponed/cancelled fixtures, no-home/away rows, and non-future unsettled records are quarantined.
- Completed results are retained as historical candidates only; the adapter does not certify official settlement truth.
- Output is research-only: model predictions created = 0, production writes = 0, production eligibility = NOT GRANTED.

## Run

```bash
python scripts/oracle_selected50_footystats_adapter.py \
  --snapshot path/to/current-fixture-snapshot.json \
  --output-csv oracle-selected50-current-fixture-snapshot/footystats-neutral-fixtures.csv \
  --output-manifest oracle-selected50-current-fixture-snapshot/footystats-neutral-fixtures-manifest.json
python -m unittest discover -s tests -p 'test_oracle_selected50_footystats_adapter.py' -v
```

## Important integration boundary

The protected production staging workflow currently expects a FotMob-specific `current_matches.csv` schema, including `fotmob_match_id`, and downstream event reconciliation also depends on FotMob goal-event IDs. This adapter intentionally does not fake that identifier or silently substitute FootyStats IDs into a FotMob-named field. The next integration step is a source-neutral research execution path that consumes this adapter and preserves the existing Oracle model logic. Production is not switched by this change.
