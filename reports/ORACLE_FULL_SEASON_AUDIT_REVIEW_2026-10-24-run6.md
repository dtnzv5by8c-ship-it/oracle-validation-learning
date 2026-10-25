# Oracle Full-Season Audit Review — uploaded run 6

## Artifact identity
- Summary generated UTC: 2026-10-23T23:01:00.958701+00:00
- Target universe: 44
- Candidate crosswalk rows: 44
- Candidate season IDs: 41
- Pagination completed by short page: 41
- Pagination failed or not run: 3
- Fixture rows: 10,853
- Unique target-season-match keys: 10,853
- Production model logic changed: false
- Production registry changed: false
- Production predictions created: false
- Failure diagnostics CSV: empty (zero bytes)
- Page provenance: 130 rows, all HTTP 200 and api_success=True

## Comparison with earlier audit
The earlier audit contained 7,216 fixture rows across 24 retrieved target seasons, with 20 targets not retrieved. This run contains 10,853 rows across 41 candidate season IDs, and only three targets were not run. This is a material improvement in retrieval coverage. The artifact is generated at 23:01 UTC, after the request-parameter and broad-catalogue changes, but its summary does not identify a commit SHA; temporal ordering alone does not prove which code revision ran.

## Three unattempted targets
- CRO — Croatia HNL
- CO — Colombia Primera A
- EC — Ecuador Serie A

The crosswalk notes say these were selected-catalogue alias misses. Do not treat that as proof that the provider lacks the competitions. These three require alternative-name/provider catalogue review and explicit season-ID confirmation.

## Data integrity observed
- Zero duplicate match IDs in the coverage table.
- Zero missing match IDs, home/away team IDs, kickoff timestamps or statuses in the coverage table.
- xG and prematch xG non-null counts each equal 10,853.
- 1X2 odds non-null counts equal 10,853.
- All 130 page-provenance records returned HTTP 200 and API success.
- Failure diagnostics file is empty, consistent with no logged match-page failures in this run.

These are structural presence checks, not proof of semantic correctness, odds validity, odds source/time, or complete season coverage.

## Remaining release blockers
1. `cutoff_provenance` is `NOT_ESTABLISHED` for the targets. No feature/odds observation timestamps are included in the fixture audit schema.
2. Short-page termination is not independent proof that all official fixtures for the intended season are present.
3. Season identity and the 41 mappings still require evidence against provider metadata and official competition schedule.
4. CRO, CO and EC have no season ID and were not fetched.
5. No predictions were created and no historical backtest should run until point-in-time pre-kickoff feature provenance and settled outcomes are independently verified.

## Recommended next action
Do not rerun the same audit immediately. Extend the research-only audit to: (a) produce a catalogue candidate report for CRO/CO/EC using unfiltered catalogue aliases, (b) preserve source timestamps for each odds/xG field if the provider supplies them, (c) add independent expected-fixture-count comparison and explicit season date ranges, and (d) create per-target READY/PARTIAL/BLOCKED/UNVERIFIED statuses. Keep production logic and the protected 27-league registry untouched.
