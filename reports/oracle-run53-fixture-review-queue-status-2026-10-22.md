# Oracle Run #53 — Fixture Identity Review Queue
Date: 2026-10-22
Status: research-only triage; no fixture identity approved.

## Scope
The Run #53 artifact (workflow run 39662641163, artifact 12375010712) contains 210 staged market rows across 42 distinct source fixtures. A review queue was generated from the actual artifact, collapsing five market rows per fixture into one review row.

## Candidate classification (distinct fixtures)
- 21 fixtures: one provisional archive candidate in a competition-aligned folder.
- 4 fixtures: competition mismatch or crosswalk gap.
- 17 fixtures: no exact kickoff-and-team candidate.
- 0 verified identities; 0 eligible for scoring.

These counts are distinct fixtures. The workflow's fixture-candidate summary counts market-prediction rows (105 aligned, 20 mismatch/gap, 85 no candidate); do not confuse those row counts with fixture counts.

## Review queue columns
The CSV includes source fixture ID, competition code, UTC kickoff, source home/away names, number of market rows, candidate status, candidate archive fixture ID/competition/season, candidate home/away team IDs and matching status, same-pair archive row count, verification status, human review status, evidence notes, and production eligibility.

All 42 rows are initialized to:
- fixture_identity_verified=NO
- human_review_decision=PENDING
- production_eligibility=NOT_GRANTED

Candidate IDs are leads only. The queue does not approve or write any candidate ID into a canonical ledger.

## Immediate root cause
The private production repository's scripts/prepare_prospective_four_market_publication.py builds fixture IDs from league code, date, and slugified team names. The canonical publication/ledger schema retains fixture ID, competition, date/time, and team names but has no separate provider fixture ID or separate canonical home/away team IDs. The research adapter therefore fails closed.

## Safe resolution path
1. Trace each row to an authoritative provider fixture catalogue/season manifest, where available.
2. Approve only exact source-ID + competition + season + kickoff + home/away identity matches, with recorded evidence.
3. Keep normalized name matches as candidates until source identity is independently supported.
4. If upstream provider IDs were never retained, recommend a separately reviewed schema change at fixture ingestion/publication; do not infer IDs from names or silently modify production.
5. Keep unresolved rows excluded from metrics. No historical accuracy or calibration claim is supported until valid prediction/result pairs pass all evaluation gates.

## Governance
Research-only. No production model logic, probabilities, thresholds, calibration, model version, canonical registry, secrets, or provider plans changed. No paid API calls made. Production eligibility remains NOT_GRANTED.
