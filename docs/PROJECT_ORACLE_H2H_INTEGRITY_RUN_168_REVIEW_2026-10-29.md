# Project Oracle — H2H Integrity Run 168 Review
**Date:** 2026-10-29  
**Workflow:** [Oracle Selected-50 Research Runtime #168](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925)  
**Artifact:** [Research runtime report](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40917698925/artifacts/12915559785)  
**Scope:** Research-only branch; production model logic and probabilities unchanged.

## Run outcome
- Workflow success in 5m 33s; all listed steps passed.
- H2H chronology/model feature contract tests passed.
- Runtime output contract: `PASS_RESEARCH_RUNTIME_OUTPUT_CONTRACT`.
- Production eligible: `false`; betting eligible: `false`.
- Exact snapshot-to-runtime archive hash verification passed.

## H2H history QA
| Diagnostic | Result | Interpretation |
|---|---:|---|
| Normalized archive history rows | 59,049 | Research archive rows, not a completeness guarantee |
| Explicitly finished with numeric scores | 51,983 | Score/status intersection only; not official settlement certification |
| Feature rows with any prior H2H | 46,323 | Historical H2H exists for these rows |
| Rows with cross-season prior H2H | 33,067 | Cross-season history is contributing to H2H features |
| Cross-season prior-meeting count sum | 128,936 | Aggregate across target feature rows; not unique match count |
| Strict pre-kickoff cutoff violations | 0 | No last-H2H-date cutoff violations detected |
| Competition/team IDs with multiple normalized names | 0 | Reassuring diagnostic, not canonical identity proof |
| Competition/team IDs seen across multiple seasons | 919 | Provider team IDs recur across seasons in archive |
| Competition/name pairs mapped to multiple team IDs | 0 | No split IDs detected by this normalized-name diagnostic |

## Important limitation
The H2H history builder uses selected competition group plus provider team IDs. These diagnostics do not certify that the selected competition grouping is canonical, that team IDs retain stable semantics across all seasons, or that the provider archive is complete. The 7,066 records that are not in the explicit finished+numeric-score intersection must not be treated as settled merely because some may contain scores. Official settlement truth and provider-to-canonical fixture/team/competition bridges remain unverified.

## Paired model comparison
The paired holdout and five chronological-fold metrics are generated successfully and remain as documented in `docs/PROJECT_ORACLE_H2H_ABLATION_RUN_167_REVIEW_2026-10-29.md`. The main conclusion is unchanged: H2H gains are small and mixed; Double Chance Home merits further research, but is not approved. Combo remains blocked due to unresolved settlement semantics. Metrics are raw and uncalibrated.

## Decision and next steps
**Continue research; do not promote or stake on the H2H candidate based on these results.**
1. Retain the zero strict-cutoff violation gate and tests.
2. Add deeper QA for provider competition mapping and team identity, with manual review of ambiguous mappings rather than automatic inference.
3. Establish authoritative market settlement truth and audit target labels before calibration.
4. Use a separate calibration/validation period; do not tune against the locked holdout.
5. Only consider betting eligibility after point-in-time provenance, canonical joins, settlement, calibration, odds/value analysis and formal release review pass.
Production code and frozen probabilities remain unchanged.