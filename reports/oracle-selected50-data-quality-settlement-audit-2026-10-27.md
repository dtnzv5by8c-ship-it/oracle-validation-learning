# Selected-50 Data Quality and Settlement Audit — Run #112

**Evidence run:** GitHub Actions run 40554064150  
**Artifact:** 12757295232 — `oracle-selected50-research-runtime-report.zip`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Status:** `RESEARCH QA PASS; PRODUCTION/BETTING NOT GRANTED`

## Executive findings

The updated research runtime and its three Combo regression tests passed. The generated data-quality evidence still fails the identity, canonical-join, official-settlement, calibration, and historical-provenance gates. No production model logic or probabilities were changed.

## Historical archive settlement/status audit

Across 50 selected season groups:

| QA measure | Count | Interpretation |
|---|---:|---|
| Raw rows retained after deduplication | 59,049 | Archive rows; zero duplicate rows removed |
| Rows with missing normalized fixture ID | 0 | Internal ID presence check only |
| Rows with identical home/away team IDs | 0 | Internal team-ID consistency check only |
| Explicitly `complete` rows with numeric scores | 51,983 | Research training truth, subject to provider-source limitations |
| `incomplete` rows | 6,962 | All carry numeric 0–0 placeholders; excluded from settled truth |
| `suspended` rows | 57 | All carry numeric 0–0 placeholders; excluded from settled truth |
| `canceled` rows | 47 | All carry numeric 0–0 placeholders; excluded from settled truth |
| Non-complete rows with numeric scores | 7,066 | These scores must not be treated as settlement truth |
| Complete rows with 0–1 total goals | 13,346 | Used as regression/settlement QA cases; no predictor-ledger disagreements detected in the research contract |

The status/score cross-tab shows every incomplete, suspended, and canceled row has a 0–0 numeric score. This is a material data hazard if a downstream consumer ignores match status. The research runtime currently fails closed by training only on explicitly completed rows.

## Current fixture/report coverage

- 461 future fixture candidates in the 7-day horizon, from 47 of the 50 selected groups.
- 40 groups have prediction rows; 3 groups have no fixture in the horizon.
- 435 fixture rows have raw research probabilities; 26 are blocked for missing feature/training support.
- All 461 rows remain `production_eligible=NO`.
- All 461 canonical fixture joins are `NOT_VERIFIED`; all 461 canonical team joins are `NOT_VERIFIED`.
- All 461 settlement-truth statuses are `NOT_VERIFIED_AGAINST_PRODUCTION_MARKET_SPEC`.
- All 461 confidence scores are uncalculated because the model is uncalibrated.
- All 461 data-risk percentages are unquantified because no validated risk mapping exists.
- 363 rows show current provider team-table snapshots, not historical as-of standings; 98 have missing/unverified table positions.
- Odds/xG fields exist in named-field counts but have unverified provenance and are not used as model features.

### Three leagues with no fixture in the 7-day horizon

| Selected season ID | Country | Competition | QA disposition |
|---:|---|---|---|
| 16741 | Canada | Canadian Premier League | Check schedule freshness / season timing |
| 16789 | China | Chinese Super League | Check schedule freshness / season timing |
| 16627 | South Korea | K League 1 | Check schedule freshness / season timing |

No fixture in a 7-day horizon is not proof that the league is unsupported; it requires a schedule-freshness check.

## Identity conclusion

The provider evidence supports using each selected identifier as a **season ID** for its season-scoped match queries. It does not provide an authoritative parent competition ID or an Oracle canonical identity bridge.

- Selected IDs matched to provider `season.id`: 50/50.
- Direct parent competition IDs verified: 0/50.
- Provider-to-Oracle canonical bridges verified: 0.
- Candidate matches to the protected 27-league registry: 22 require human review.
- Selected groups with no candidate match in the current 27-league registry: 28.
- Approved canonical mappings: 0.

Do not infer parent competition IDs from season IDs, names, or year labels. The existing 27-league production registry remains protected and unchanged.

## Release decision and next actions

1. **Do not promote** this artifact or its raw probabilities to production or betting use.
2. Obtain provider clarification or documented schema evidence for stable identity semantics. The current clarification request is a draft and has not been sent.
3. Define and approve a separate identity contract for the 50 selected season IDs, including how each maps to canonical league, team, and fixture IDs. Any mapping needs evidence and human sign-off.
4. Reconcile the 7,066 non-complete 0–0 rows as status-excluded records and independently verify completed results against authoritative settlement truth.
5. Check schedule freshness for the three no-fixture groups and repair feature/training support for the 26 blocked fixture rows in research only.
6. Keep calibration, odds/ROI evaluation, and point-in-time feature provenance as separate gates. Do not call raw accuracy a betting edge.
7. Preserve the production registry, Oracle V1.6 logic, probabilities, thresholds, and governance unchanged.

## Evidence links

- [Run #112](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150)
- [Artifact #12757295232](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150/artifacts/12757295232)
- [Provider identity reconciliation](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-provider-identity-reconciliation-2026-10-27.md)
- [Canonical candidate crosswalk](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-canonical-candidate-crosswalk-2026-10-27.md)
- [FootyStats clarification request draft — not sent](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-footystats-identity-clarification-request-2026-10-27.md)
