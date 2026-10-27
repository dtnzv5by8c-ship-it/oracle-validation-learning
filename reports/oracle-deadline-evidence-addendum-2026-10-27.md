# Project Oracle — Deadline Evidence Addendum
Date: 2026-10-27
Branch: `research/oracle-50-league-readiness-audit`
Status: research-only; production and betting eligibility NOT GRANTED.

## New executive finding
The archive has strong structural integrity evidence, but that is not the same as historical coverage completeness or settled-result truth.

## Latest available archive QA evidence
Source report: [Selected-50 Private Archive Status, Score and Date Audit — 2026-10-27](oracle-selected50-private-archive-status-score-date-audit-2026-10-27.md)
Source QA run: [40423922693 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423922693)
Runtime verification run: [40423792877 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40423792877)

| Audit item | Verified result | Interpretation |
|---|---:|---|
| Selected leagues in manifest/archive | 50/50 | Structural universe check passes |
| Historical season rows | 200 | Four season folders per selected league on average; not a guarantee of equal history |
| Seasons ingested | 200/200 | Ingestion presence check passes |
| Archived match records | 59,049 | Raw records, not all valid settled labels |
| Records with IDs and parseable kickoff dates | 59,049 / 59,049 | Field/parseability check passes; canonical identity not established |
| Records with two parseable non-negative integer scores | 59,049 / 59,049 | Score fields present; not sufficient for settlement truth |
| Duplicate match IDs within season | 0 | Structural duplicate check passes |
| Repeated match IDs across season rows | 0 | Structural duplicate check passes |
| Provider status = complete | 51,983 | Candidate settled-status population only; still needs authoritative identity/truth verification |
| Incomplete/suspended/canceled with score pair | 7,066 | All are 0-0; must not be treated as settled 0-0 |
| Provider complete rows with future kickoff | 0 | Date/status consistency check passes for this rule |
| Incomplete rows with past kickoff | 27 | Requires investigation/quarantine |
| Observed kickoff range | 2023-01-20 to 2027-06-06 | Wider than the modelling window; does not prove full window coverage |

## Per-league/per-year coverage limitation
The existing `oracle-selected50-year-by-year-data-and-market-readiness-2026-10-25.csv` and `oracle-selected50-annual-coverage-reconciliation-2026-10-25.csv` are based on the older Run 9 feature snapshot. They must not be presented as the current 200-season archive's authoritative per-year coverage totals. Current runtime `season_coverage.csv` was reported to contain 200 season rows but not explicit country/year columns, so mapping rows to season years without the source season start/end dates would be unsafe.

**Required next technical action:** generate a refreshed, sanitized coverage matrix directly from the exact batch-5 archive, keyed by selected season ID and source season start/end dates, with record counts by calendar/season year, primary-window counts, completed/incomplete/suspended/canceled counts, score-status exceptions, feature availability and a clear evidence timestamp. Do not reuse the stale Run 9 totals as current.

## Market / model implications
- BTTS primary holdout accuracy 53.588% versus 54.143% majority baseline; below baseline.
- Double Chance Home 70.126% versus 69.786% baseline; Double Chance Away 60.422% versus 56.275% baseline. These are raw uncalibrated diagnostics, not production approval.
- Combo Home/Away probabilities remain masked because target and settlement definitions differ.
- Odds have no verified point-in-time timestamps; no ROI/profitability claim is supportable.
- xG-like fields and standings snapshots lack sufficient as-of provenance for safe historical modelling.
- Canonical provider-to-Oracle bridges: 0/50 verified. Canonical fixture/team joins and official settlement truth remain unverified.

## Executive disposition
1. Keep the research pipeline and its current contracts intact.
2. Do not run more paid provider requests; the bounded audit is already consumed.
3. Do not promote candidate mappings by name similarity.
4. Do not modify the production repository/model to meet the deadline.
5. At the deadline, deliver this as an evidence-backed research readiness pack unless all identity, settlement, validation and operational gates are independently evidenced and approved. Current evidence does not meet production-release conditions.
