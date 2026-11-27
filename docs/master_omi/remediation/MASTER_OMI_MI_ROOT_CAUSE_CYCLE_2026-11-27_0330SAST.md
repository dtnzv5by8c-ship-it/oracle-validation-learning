# Master OMI MI Root-Cause Cycle — 2026-11-27 03:30 SAST

## Release decision
FAIL-CLOSED / NOT RELEASED.

## Current authoritative evidence
- Rolling governed spine manifest currently persisted: 392 fixtures, 50 leagues, 392 unique provider Fixture IDs, generated 2026-11-27T00:12:17.529536Z.
- Current reconciliation status currently persisted: 372/372 exact governed upcoming identities, 100% coverage, status CURRENT, generated 2026-11-26T23:49:37.015401Z.
- Current source manifest: FootyStats primary source, no source errors, rolling public spine is the sole weekly fixture universe, pre-match-only, no fuzzy matching, no historical fallback, production model logic unchanged, A:ET unchanged.
- Latest independent QA artifact available in repository is stale relative to the newer reconciliation evidence and still records the earlier 0/429 state. It must not override the newer authoritative current reconciliation artifact.

## Root-cause matrix

| Field / scope | Fixture scope | Cause | Authoritative source | Fix | Status |
|---|---|---|---|---|---|
| Current weekly fixture universe | 50 leagues | Independent downstream reconciliation was previously consuming an obsolete frozen/upcoming fixture file instead of the rolling governed spine | `data/fixtures/governed_50league_current.csv` | Reconciliation now consumes the rolling public spine and matches exact FootyStats Fixture IDs | RESOLVED IN LIVE STATE |
| Exact fixture reconciliation | 372 governed rows in latest current reconciliation | False 0/429 result was produced by the obsolete fixture-input path, not provider identity failure | FootyStats source IDs + rolling governed spine | Exact provider-ID reconciliation enforced; latest status is 372/372 | RESOLVED |
| Rolling spine freshness | Current weekly input | Prior QA snapshot was stale while newer rolling/current artifacts existed | Rolling spine manifest + retrieval timestamps | Fresh rolling producer cycle triggered; stale snapshot not admitted | IN PROGRESS |
| Current prediction ledger | Current governed fixture set | Authoritative ledger is not yet independently certified/persisted for the newest rolling spine | Private production output `research/four_model/outputs/omi_prediction_ledger_current.csv` | Prospective workflow must consume the governed rolling spine only and fail closed if ledger absent | BLOCKED |
| 264-column Master OMI | All governed fixtures | Canonical assembly has not yet been rebuilt from the newly reconciled current set | Canonical V2.1.1 / Master OMI template | Rebuild only after current spine + ledger gates pass | BLOCKED |
| PPG/GF-M/GA-M/venue/Recent Form/H2H/BTTS/goal intelligence | Governed fixtures | Must be re-certified against the fresh rolling set with point-in-time cutoffs | FootyStats | Populate from authoritative evidence; otherwise UNAVAILABLE/UNVERIFIED | PENDING RE-CERTIFICATION |
| xG | Governed fixtures | Capture-time provenance must be independently sufficient for PIT admission | FootyStats xG + capture metadata | Admit only when cutoff chronology is proven; otherwise UNVERIFIED | BLOCKED/PENDING |
| LTSS/source IDs/sample sizes/actuals | Governed fixtures | Final canonical MI rebuild has not run | Authoritative current sources + canonical workbook | Recompute/persist with provenance and sample-size fields | BLOCKED |
| A:ET | Protected range | Release workbook not yet assembled/certified | Canonical V2.1.1 baseline | Byte-level preservation gate | UNCHANGED / NOT YET CERTIFIED |
| Oracle V1.6 | Production model | No change authorized | Oracle V1.6 production baseline | Preserve exactly; certification only | UNCHANGED / NOT YET CERTIFIED |
| Persistence/workflow dependency | Rolling-current producer | Fresh builds previously could be lost to concurrent generated-artifact writes | GitHub main + workflow | Safe latest-main refresh/overlay persistence already implemented; fresh trigger checkpoint added this cycle | RESOLVED IN CODE; EXECUTION PENDING |
| QA evidence freshness | Final gate | Latest independent QA document lags newer persisted reconciliation artifacts | Public governed evidence | Re-run final QA after fresh rolling/current cycle; never infer release from green workflow alone | BLOCKED |

## Non-negotiable controls
- No dated frozen weekly spine admitted.
- No fuzzy matching.
- No timezone normalization.
- No zero-fill, estimate, fabrication or synthetic values.
- No post-kickoff evidence.
- No stale evidence promoted.
- Critical enrichment failures fail closed.
- Oracle V1.6 unchanged.
- A:ET unchanged.

## Next gate sequence
Fresh rolling 50-league producer -> fresh current-data reconciliation -> authoritative current prediction ledger -> canonical 264-column MI -> exhaustive cell/type/provenance/chronology/leakage QA -> native XLSX/XML and A:ET certification -> exact hashes -> 100% release.
