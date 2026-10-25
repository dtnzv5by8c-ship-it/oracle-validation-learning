# Oracle 50-League Follow-through Checkpoint — 2026-10-25

Status: RESEARCH ONLY. Production eligibility remains NOT_GRANTED.

## Completed in this checkpoint

1. Inspected the uploaded `footystats-selected-league-catalogue.zip` directly.
2. Independently validated the catalogue CSV:
   - 766 rows
   - 50 distinct competition names
   - 766 distinct, nonblank season IDs
3. Compared the 50 saved selected IDs with the catalogue:
   - 50/50 IDs found
   - 50/50 country + competition names match after Unicode/diacritic normalization
   - 0 missing IDs
   - 0 name mismatches
4. Added a normalized selected manifest at `data/oracle-footystats-selected-50-season-id-manifest.csv`.
5. Added a CSV-based reconciliation utility at `scripts/reconcile_footystats_selected_seasons_csv.py`. It fails closed on blank or duplicate IDs and explicitly labels mappings as not approved.
6. Saved this checkpoint on the research branch only.

## Important correction

The 50 selected IDs should be treated as **FootyStats season IDs** for this catalogue workflow. They should not be represented as verified parent-competition IDs. Keep competition name, optional parent competition ID, season year, and season ID as separate fields in any catalogue schema.

## Historical/current data status — still blocked

The existing archive feature-coverage snapshot remains a separate evidence set and has not yet been repaired by the catalogue match:

- Earlier archive snapshot: 35,819 match rows across 126 season folders; 28,491 accepted settled-status rows with complete scores.
- Exact country + competition-name archive corroboration: 31/50 selected competitions.
- No exact name match in that archive snapshot: 19/50.
- Verified selected-season-ID → historical fixture ID → canonical Oracle home/away team joins: 0/50 in the previous audit.
- Existing archive manifest provider-league-ID fields were blank; its old provider-ID join claims must not be treated as proof.
- Verified point-in-time pre-match xG provenance: 0 rows in the prior audit.
- Verified point-in-time odds provenance: 0 rows in the prior audit.
- Current reconciliation/event-truth snapshot was stale in the prior audit; four completed matches lacked chronology.
- The previous canonical settlement ledger was empty/header-only, so no defensible production accuracy/calibration/profitability claim is established by this work.

The 31 name matches are **candidate archive corroboration only**. They are not selected season-ID joins and do not justify backfilling provider IDs based on names alone. The 19 unmatched competitions need archive discovery or a documented no-data result.

## Safe next implementation

- Preserve selected season IDs in the research ingestion/catalogue layer.
- Inspect actual archived source rows and schema for a documented season-ID field before attempting joins.
- For each of the 50 entries, report archive coverage by season/year, settled-score completeness, current fixture freshness, canonical team/fixture identity, recent-form and standings coverage, H2H identity/chronology, xG provenance, odds timestamps, and each supported market.
- Keep ambiguous aliases and missing joins unresolved; do not infer parent IDs or manufacture joins.
- Do not run bulk historical ingestion or any workflow that may consume additional provider credits without explicit cost approval.
- Do not change the private production repository, 27-entry production registry, production model logic/probabilities, calibration, thresholds, ledgers, or promotion gates.

## Decision

**Identifier/catalogue checkpoint: PASS for the 50 selected season IDs.**

**Historical archive reconciliation: BLOCKED / PARTIAL.**

**Per-market readiness and production eligibility: NOT GRANTED.**

The immediate next work is a schema-backed historical archive reconciliation, not a model change and not a production expansion.
