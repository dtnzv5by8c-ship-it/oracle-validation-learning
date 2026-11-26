# Master OMI MI Root-Cause Cycle — 2026-11-27 00:57 SAST

## Release status
FAIL-CLOSED. No release workbook certified.

## Root cause resolved this cycle
The authoritative current-data reconciliation script was not consuming the rolling 50-league governed fixture spine. It was reading the obsolete local `data/fixtures/oracle_upcoming_fixtures.csv` and reconciling by normalized league/home/away strings. This violated the current weekly input contract and caused a false 429/429 unmatched result even though FootyStats ingestion had already been switched to the rolling 50-league public spine.

### Evidence
- Rolling governed spine: 372 rows / 372 unique FootyStats fixture IDs / 50 leagues.
- Fresh FootyStats manifest: 2026-11-26T21:43:55Z, no source errors.
- Reconciliation status: 429 governed rows, 0 matched, 429 unmatched.
- The mismatch was traced directly to the reconciliation implementation, not to the provider-ingestion season selection.

## Corrective action
Commit `6356d80ca4f202cadc560b88b3d0c1ca51a97b78`:
- Reconciliation now fetches `governed_50league_current.csv` from the public governed repository.
- The rolling 50-league spine is the sole current weekly fixture input.
- Exact provider Fixture ID reconciliation is used: FootyStats `source_match_id` ↔ governed `fixture_id`.
- Team-name/date normalized matching is removed from the fixture-admission gate.
- If the rolling spine cannot be retrieved, the cycle fails closed.

Commit `4a31084a4e381738220901c206e317ba94f59376`:
- Current-data workflow now triggers when `scripts/reconcile_current_data.py` changes, eliminating the prior workflow dependency gap where a reconciliation fix could remain unexecuted until the next scheduled run.

## Mandatory controls
- No fuzzy matching.
- No timezone normalization.
- No stale/frozen weekly spine substitution.
- No post-kickoff evidence.
- No fabrication, estimation, or zero-fill.
- Oracle V1.6 production logic unchanged.
- Master OMI A:ET unchanged.
- Critical enrichment remains fail-closed.

## Next gate
Execute the corrected current-data workflow, verify exact provider-ID coverage against the fresh rolling 50-league spine, then proceed to current Team State, current prediction ledger, canonical 264-column MI, exhaustive cell/type/provenance/chronology/leakage QA, and final XLSX/XML/hash certification.
