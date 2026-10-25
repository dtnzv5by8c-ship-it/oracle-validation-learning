# Project Oracle — Remaining Work Gate Review
Date: 2026-10-23
Branch: `research/oracle-crosswalk-isolation-2026-10-22`
Scope: research-only repository inspection; no production model or protected registry changes.

## Gate status

| Workstream | Current evidence | Status | Safe next action |
|---|---|---|---|
| 44-league target vs 27-code registry | Run #27's 44 League Universe tab has 44 target entries; 18 target leagues have fixtures, 26 have none. Run output also contains D2, E2, E3, F2, I2, NED2, POR2 outside the target universe. | BLOCKED | Maintain separate target and governed registry lists; complete a row-by-row provider competition ID crosswalk before enabling missing leagues. |
| South Africa code | Target workbook uses `ZA`; governed registry uses `RSA`; Run #27 has no ZA/RSA fixtures. | CANDIDATE ONLY | Record `ZA -> RSA` as a proposed alias, not an approved production mapping. Confirm provider competition ID, season, and teams before accepting it. |
| Form and H2H joins | Run #27 export has home recent form 144/184 (78.3%), away recent form 147/184 (79.9%), H2H 91/184 (49.5%). Existing research-only crosswalk candidates are not production-approved. | PARTIAL | Join only on verified fixture/team IDs; use date + competition/season + normalized home/away only as a candidate requiring audit. Keep unmatched fields null and log why. |
| Historical league position | 0/184 fixture rows have league-position values in the current export. | BLOCKED | Reconstruct standings from completed, dated results strictly before each fixture cutoff; account for season, points rules, deductions, and split/playoff formats. Store source row IDs and as-of timestamp. |
| Prediction-to-settlement validation | Current run export is a live prediction artifact; it does not by itself prove immutable historical predictions paired to verified final results. | BLOCKED | Build an append-only prediction ledger keyed by fixture ID, market, prediction timestamp, model/version, and probability; join to authoritative settled scores/results and retain settlement provenance. Do not report accuracy until this join passes. |
| Automated refresh | `.github/workflows/oracle-completion-run.yml` defines a weekly Monday schedule at 04:00 UTC (06:00 South Africa time), plus manual dispatch. Research recovery replay has push/manual triggers but no scheduled trigger in its workflow header. | PARTIAL | Verify actual scheduled run history, source freshness, successful artifact generation, and stale-data behaviour. A cron declaration alone is not proof of reliable operation. |
| Failure notification | The inspected production completion and research replay workflow definitions upload artifacts with `if: always()`, but the inspected files contain no explicit email/chat notification step. | NOT VERIFIED / GAP | Add a separate research-tested failure alert (e.g., GitHub issue or repository notification) with run URL, failed job/step, timestamp, and freshness status. Do not place secrets or raw provider responses in alerts. |
| Promotion governance | Run #27 reports raw, uncalibrated probabilities; historical accuracy and league position remain unverified. | BLOCKED | Keep all changes research-only. No merge/promotion until gates pass and owner explicitly approves. |

## Exact target-league rows absent from Run #27

Based on the workbook's `44 League Universe` tab: ZA (South Africa), DK (Denmark), SE (Sweden), NO (Norway), FI (Finland), GR (Greece), RS (Serbia), RU (Russia), IE (Ireland), US (USA), CA (Canada), MX (Mexico), BR (Brazil), AR (Argentina), CO (Colombia), CL (Chile), UY (Uruguay), PY (Paraguay), EC (Ecuador), PE (Peru), VE (Venezuela), AU (Australia), JP (Japan), KR (South Korea), CN (China), IN (India). These are absent from this export only; this does not prove that no provider data exists.

## Required pass criteria before declaring complete

1. A versioned 44-target-to-provider competition crosswalk, with explicit status for each target and no silent code substitutions.
2. Team and fixture join audit showing exact-ID matches, reviewed candidates, rejected ambiguous matches, and zero fabricated joins.
3. Feature lineage for form, H2H, standings, xG and odds: source, source record ID, match/feature timestamp, as-of cutoff, and freshness.
4. League-position test against independently recomputed standings for sampled historical dates in every supported competition format.
5. Immutable historical prediction-to-settlement join with duplicate checks, market-specific settlement rules, void/postponed handling, and pre-kickoff timestamp proof.
6. A demonstrated scheduled refresh run plus a deliberately induced research test failure proving alert delivery and useful diagnostics.
7. Re-run all audits and attach artifacts; leave PR #20 draft/unmerged pending owner approval.

## Disposition

**NOT COMPLETE — research-only.** The repository has a weekly schedule in the main completion workflow, but that is not sufficient evidence of reliable refresh or alerting. The target 44-league coverage, standings, historical accuracy, and failure notification gates remain open. Production logic and probabilities were not changed.
