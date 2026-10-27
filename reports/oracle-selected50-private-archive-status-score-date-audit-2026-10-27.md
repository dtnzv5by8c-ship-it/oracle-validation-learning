# Selected-50 Private Archive Status, Score and Date Audit — 2026-10-27

## Evidence provenance

- Commit-pinned research-only QA run: [40423922693 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693)
- Sanitized QA artifact: [12698682583](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693#artifacts)
- QA artifact ZIP SHA-256: `2fd2242e46d58267f7dbbffc35fb43675c7d74dd5168446e802b45a5a7667e2b`
- Runtime validation run: [40423792877 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423792877)
- Runtime artifact: [12698452196](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423792877#artifacts), ZIP SHA-256 `ef5359a46102f87c222b80b5e1a38793d25d64f3c9f50de55e56817c24ea0f2e`
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

## Cross-check against the research runtime

The runtime's independent 50-row `oracle_selected50_settlement_truth_qa.csv` reports the same 59,049 source rows, 51,983 provider-`complete` rows with numeric scores, and 7,066 non-finished rows with numeric scores. Its per-status cross-tab shows all 7,066 non-finished score pairs are 0-0; no non-finished row has a non-zero score pair. Every row is explicitly `INTERNAL_STATUS_SCORE_QA_ONLY_OFFICIAL_SETTLEMENT_UNVERIFIED`, and every row has `production_eligible=NO`.

Runtime output contract passed: 50 selected groups, 463 governed fixture rows, 2,315 prediction rows, 250 league-market rows and 750 league-market-fold rows. It masked all 437 raw Combo Home and 437 raw Combo Away probabilities present in the governed fixture report; zero Combo probabilities remain. The runtime is research-only and does not authorize betting or production release.

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
