# Selected-50 Settlement Truth and Source-Provenance Review — 2026-10-27

**Disposition:** Existing artifacts support research QA and limited independent score corroboration only. They do **not** establish official settlement truth for the 50-league universe. Production and betting release remain blocked.

## Evidence lineage reviewed

- Research branch: `research/oracle-50-league-readiness-audit`
- Current identity evidence register: [CSV](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/reports/oracle-selected50-independent-identity-evidence-register-2026-10-27.csv), commit [21139591e7a7ccaedcebcebaa92411c15e201089](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/21139591e7a7ccaedcebcebaa92411c15e201089)
- Historical status/score audit: [archive QA run 40423922693](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693), artifact 12698682583.
- Research runtime: [run 40554064150](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40554064150), artifact 12757295232.
- Existing source trust policy: [research-only policy](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/docs/oracle-result-source-trust-policy-research-only-2026-10-21.md).
- Existing manual/independent score checks: [verified shadow reconciliations CSV](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/blob/research/oracle-50-league-readiness-audit/data/verified_shadow_result_reconciliations.csv).
- No provider API request was made in this review.

## Existing archive status/score evidence

The existing archive QA/runtime reports reconcile to 59,049 historical match rows across 50 selected groups / 200 seasons:

| Source status | Rows | Score pattern | Settlement disposition |
|---|---:|---|---|
| `complete` | 51,983 | Numeric score pairs; includes 4,006 0–0 rows | Candidate research truth only; still requires source provenance and exact fixture identity |
| `incomplete` | 6,962 | All 6,962 are numeric 0–0 | Exclude from settled truth |
| `suspended` | 57 | All 57 are numeric 0–0 | Exclude from settled truth |
| `canceled` | 47 | All 47 are numeric 0–0 | Exclude from settled truth |
| **Non-complete total** | **7,066** | **All 7,066 are 0–0; none has a non-zero pair** | **Never treat as settled 0–0 or a market label** |

The score/status pattern is consistent with placeholder/default values, but the artifacts do not prove the provider's internal cause. Status is the controlling exclusion: non-complete rows are not settlement truth even though score fields parse as numeric zeros. This preserves the required exclusion of non-complete 0–0 placeholders.

The research runtime and archive QA reports explicitly describe their outputs as internal status/score QA only. A green workflow or valid numeric score does not elevate a row to official truth.

## Settlement utility behavior

Code review of `scripts/settle_market_from_final_score.py` confirms it:
- requires fixture ID, competition ID, scheduled kickoff, both team IDs, both scores, match status and result source;
- requires exact fixture ID and matching competition/kickoff/team IDs between prediction and result;
- settles only explicit final statuses `FINISHED`, `FT` or `FULL_TIME`;
- returns void/unsettled outcomes for listed cancelled/postponed/abandoned/suspended statuses, and fails closed on unsupported statuses;
- rejects missing fields, invalid scores and unsupported market/selection semantics.

That is a useful structural guard, but it is not an independent source-authentication system. The settlement utility alone does not prove that a source is authoritative, that acquisition time is true, that the result snapshot was available at the claimed time, or that the result's source is independently approved. The existing source-trust policy correctly requires a separately reviewed allowlist, raw-snapshot hash, acquisition timestamp, immutable run ID, exact fixture reconciliation, chronology checks, versioned score-derived settlement, rejected-row audit and fail-closed coverage reporting.

## Independent official-score spot checks

The existing `data/verified_shadow_result_reconciliations.csv` contains two Bundesliga official-report checks:
- Borussia Dortmund 2–2 Werder Bremen, 2026-10-09 — official [Bundesliga match report](https://www.bundesliga.com/en/bundesliga/news/borussia-dortmund-werder-bremen-match-report-highlights-matchday-5-39473) shows the 2–2 score and date.
- Mainz 3–4 Bayer Leverkusen, 2026-10-10 — official [Bundesliga match report](https://www.bundesliga.com/en/bundesliga/news/mainz-bayer-leverkusen-match-report-highlights-matchday-5-39489) shows the 3–4 score and date.

These public pages independently corroborate the listed score/date. However, the two-row CSV does not contain stable fixture ID, canonical competition/team IDs, scheduled kickoff UTC, provider status, acquisition/observation timestamp, raw snapshot SHA-256, allowlist version/hash, validator version, or a reproducible exact-identity join. Therefore they are **manual score corroborations only**, not accepted rows in a production settlement ledger and not evidence that 50-league settlement truth is verified.

## Point-in-time provenance gaps

The existing evidence does not yet establish:
1. a separately pinned source allowlist and source-approval hash;
2. raw result snapshot identity/hash plus trusted UTC acquisition time for every scored result;
3. exact provider fixture → canonical fixture → canonical home/away team linkage;
4. official final status and score scope (including regulation-time/extra-time treatment);
5. documented handling for abandoned, postponed, suspended, cancelled, void and rescheduled fixtures;
6. feature and odds/xG values observed before each historical kickoff rather than after the event;
7. a complete exclusion ledger for rows rejected due to missing identity, conflicting sources, chronology, or unsupported status.

The private archive QA establishes structural completeness, not these trust properties. The latest archive evidence and legacy Run 56 evidence have different scopes; do not add their row counts or treat their discrepancies as proof of missing provider coverage.

## Required fail-closed controls

- Keep all 7,066 non-complete 0–0 records excluded from settled truth and scored metrics.
- Keep `complete` archive rows in research-only candidate truth until authoritative source provenance and exact canonical fixture/team identity are verified.
- Accept independently corroborated official scores only after the complete provenance/identity contract is satisfied; keep the current two shadow rows outside production ledgers.
- Keep all Combo predictions masked until the existing prediction/settlement semantic mismatch is resolved under governance.
- Do not claim hit rate, calibration, ROI or betting edge from status-only or source-unverified labels.
- Do not modify production ledgers, production model logic/probabilities, thresholds, calibration, registry or governance in this research pass.

## Next independent action

Continue using existing archives and public official result pages to expand a small, exact-identity shadow reconciliation set, recording the full provenance fields required by the trust policy. Do not use additional provider credits. The 50-league release remains blocked until canonical identity, settlement truth, point-in-time provenance and explicit release approval are all present.
