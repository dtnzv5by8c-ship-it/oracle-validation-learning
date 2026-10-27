# Selected-50 Private Archive Status, Score and Date Audit — 2026-10-27

## Evidence provenance

- Research-only QA run: [40423793007 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423793007)
- Sanitized artifact: [12698323452](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423793007#artifacts)
- Artifact ZIP SHA-256: `0159f36791f668b8b1554912b4881f7e5008a10ba46b191af913f4c0dcf6f7eb`
- Private archive release tag read by the QA workflow: `research-selected50-footystats-history-40375285207`
- Private archive SHA-256 verified from the sanitized QA summary: `7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f`
- Audit date (UTC): `2026-10-27`
- Scope: aggregate and season-level QA only. Raw provider match payloads and credentials were not exported.

## Archive completeness

| Check | Result |
|---|---:|
| Selected leagues represented in manifest | 50/50 |
| Selected IDs present in archive manifest | 50/50 |
| Historical season rows | 200 |
| Seasons marked ingested | 200/200 |
| Seasons not ingested | 0 |
| Match records | 59,049 |
| Match records with an ID | 59,049 |
| Match records with a parseable kickoff date | 59,049 |
| Match records with two parseable non-negative integer scores | 59,049 |
| Team records | 3,366 |
| Duplicate match IDs within season | 0 |
| Match IDs repeated across season rows | 0 |
| Observed kickoff-date range | 2023-01-20 to 2027-06-06 |

The 50 selected-current-season folders contain 14,051 match rows, reconciling to the previously audited 14,051-row selected-season snapshot. This confirms structural agreement between that snapshot and the current archive for those selected season folders; it does not prove full primary-window coverage or canonical fixture identity.

## Provider status and score-pattern findings

### All 200 archived seasons

| Provider status | Rows | Score-pair pattern |
|---|---:|---|
| `complete` | 51,983 | 47,977 non-zero pairs; 4,006 0-0 pairs |
| `incomplete` | 6,962 | All 6,962 have a parseable 0-0 pair |
| `suspended` | 57 | All 57 have a parseable 0-0 pair |
| `canceled` | 47 | All 47 have a parseable 0-0 pair |
| **Total** | **59,049** | **7,066 non-complete-status rows have 0-0 pairs; zero have non-zero pairs** |

Additional checks:

- Missing provider status: 0.
- Rows without a kickoff date: 0.
- Invalid or negative/non-integer score pairs: 0.
- Provider-`complete` rows missing a parseable score pair: 0.
- Provider-`complete` rows with a future kickoff date relative to the audit date: 0.
- Provider-`incomplete` rows with a past kickoff date: 27 across the archive.
- Suspended rows with a parseable score pair: 57.

### Selected 50 current-season folders

| Check | Result |
|---|---:|
| Match rows | 14,051 |
| `complete` | 7,040 |
| `incomplete` | 6,958 |
| `suspended` | 53 |
| Incomplete/suspended rows with parseable 0-0 pairs | 7,011 |
| Incomplete rows with past kickoff dates | 23 |
| Suspended rows with parseable score pairs | 53 |

## Interpretation and controls

The score/status pattern is consistent with default or placeholder 0-0 values for non-complete records. This is an anomaly classification, not proof of the provider's internal mechanism. **Do not treat any incomplete, suspended or canceled row's score fields as a settled 0-0 result, training label, or official market-settlement truth.** Quarantine these rows from outcome evaluation until status and final score are independently verified against authoritative fixture identity and settlement evidence.

The audit establishes archive structure and identifies the score/status risk; it does not certify:

- Oracle canonical league, fixture or team joins;
- official settlement truth, abandonment/void/postponement handling, or regulation-time settlement scope;
- historical standings as of kickoff;
- point-in-time xG or bookmaker-odds provenance;
- completeness of the full 2025-03-20 through 2026-09-20 modelling window;
- calibrated probabilities, betting edge, ROI or production readiness.

Provider-to-canonical bridges remain 0/50 verified. All outputs remain research-only; production and betting eligibility remain false. No production model logic, probabilities, calibration, thresholds, registries or ledgers were changed.
