# Selected-50 Identity Snapshot Reconciliation — 2026-10-26

**Status:** Research-only evidence reconciliation; production eligibility is NOT GRANTED.

## Build verification

- Dry-run [40252186906 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40252186906) on commit ee6aeaf3779dbb39e6fb34652e54be6792e46141.
- Artifact [12620986710](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40252186906/artifacts/12620986710), SHA-256 df3b28a2ae1e759317982d678d137a53b2b0b30787038084c87298b18c13b458.
- Snapshot-scope builder and regression test both passed. This is a no-network evidence/reporting check, not a new prediction run.

## Verified source layers

- Provider ingestion run 40176065362: SUCCESS_50_OF_50_SEASONS_INGESTED.
- Latest sanitized private-archive QA: run 40183451811, artifact 12594568810, SHA-256 713ed63ed5dd6e6902a2e152367500386d5037dd6dc8bbc82fa87c831d10c375.
- Latest private archive QA reports 50/50 selected season IDs, 14,051 fixture rows, 14,051 unique season-fixture pairs and zero duplicate pairs.
- The older Run 56 crosswalk snapshot records 31 exact selected-ID archive joins and 19 no-exact-join rows. These are historical snapshot fields; they do not override later private season-folder evidence.

## Evidence scope

| Evidence item | Latest verified scope | Legacy Run 56 scope |
|---|---:|---:|
| Selected season IDs / folders | 50/50 | 31 exact joins; 19 gaps in that snapshot |
| Season fixture rows | 14,051 | Different row-level snapshot; not directly comparable |
| Latest season-snapshot primary-window rows | 5,637 | Legacy values populated only for some rows |
| Duplicate season-fixture pairs | 0 | Not used to certify latest package |
| Parent competition IDs verified | 0 | 0 |
| Approved canonical mappings | 0 | 0 |

Do not add latest single-season-snapshot primary-window rows to legacy crosswalk primary-window counts. Their scope and row-level evidence differ.

## Canonical identity and data gates

- Selected IDs are verified provider season IDs, not parent competition IDs.
- Candidate canonical mappings needing human review: 22. Unresolved: 28. Approved mappings: 0.
- Parent competition IDs verified: 0/50.
- Canonical Oracle fixture joins verified: 0/50.
- Canonical team joins verified: 0/50.
- Official settlement truth verified: 0/50.
- Historical standings as of kickoff: not verified.
- xG and odds point-in-time provenance: not verified; neither is approved for ROI benchmarking.
- 33 raw season-year tokens remain the unverified eight-digit value 20262027.
- Australia A-League (17326) and India Indian Super League (17964) have zero primary-window rows in the latest selected-season snapshot.

## Next actions

1. Inspect the generated 50-row identity-scope matrix and regression test after the dry-run.
2. Reconcile canonical fixture/team IDs using approved existing evidence; do not infer parent IDs from season IDs, aliases or names.
3. Reconcile finished-status/date discrepancies and official market settlement truth.
4. Keep missing historical standings, xG and odds provenance missing. Do not benchmark ROI without verified pre-match bookmaker, market, price and timestamp data.
5. Keep Combo blocked until target/settlement governance is resolved; keep M-1UP blocked until its independent event-truth gate passes.

No provider API calls/credits, private-repository Actions, or raw provider payloads are used by this reconciliation. All Selected-50 outputs remain research-only and production-ineligible.
