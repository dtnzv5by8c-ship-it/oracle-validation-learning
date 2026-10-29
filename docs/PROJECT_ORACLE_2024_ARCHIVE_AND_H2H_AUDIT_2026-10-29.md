# Project Oracle — 2024 Archive Coverage and H2H Audit (2026-10-29)

## Finding: 2024 data is present in the existing research runtime archive

The runtime's existing calendar-year coverage output confirms observed archive rows for all 50 selected league groups in calendar year 2024.

| Calendar year (UTC) | Selected groups | Groups with observed rows | Archive fixture rows | Completed-like rows with numeric score | Rows with all 20 research features |
|---|---:|---:|---:|---:|---:|
| 2024 | 50 | 50 | 14,761 | 14,749 | 13,526 |
| 2025 | 50 | 50 | 15,029 | 14,987 | 14,165 |
| 2026 | 50 | 50 | 14,605 | 12,045 | 13,645 |

These are observed archive counts only. They do not prove that the provider dataset is complete or unbiased, that numeric scores are official settled truth, or that all feature values are point-in-time safe.

## Important validation-window distinction

The existing primary historical validation window remains 20 March 2025–20 September 2026. The presence of 2024 rows in the archive does not mean the reported model performance metrics have already been validated on 2024. Expanding the evaluation window must be a separate, research-only step after checking timestamped feature provenance and chronological split logic.

## Head-to-head (H2H) logic

The inspected runtime implementation constructs H2H histories from prior matches grouped by competition and unordered pair of team IDs, sorts each history by kickoff time, and cuts history at the target fixture kickoff before using prior meetings. This is the correct basic temporal direction.

Remaining H2H QA:
- verify exact competition/team identity and home/away perspective;
- report H2H sample-size distribution and fixtures with zero, 1–2, 3–5 or more than 5 prior meetings;
- verify every included historical meeting finished before the target kickoff and has valid settlement status/source;
- detect duplicate fixtures and team-ID collisions;
- compare H2H feature coverage by league and season;
- ensure H2H-derived features do not include current or future match outcomes.

The current prediction report does not export enough H2H diagnostics to certify all of these items, so a dedicated audit output is required before claiming H2H completeness.

## Decision and next steps

1. Use the existing archive; do not repeat provider API calls simply to rediscover the same 2024 rows.
2. Build a research-only per-league/per-season inventory for 2024, 2025 and 2026, including earliest/latest kickoff, fixture counts, duplicates, valid settled labels, feature coverage and source timestamp evidence.
3. Add an explicit H2H QA report with prior-match counts, last prior H2H date, exact team/competition identity status, temporal eligibility and exclusion reasons.
4. Only after the PIT gate passes, extend walk-forward validation to include eligible 2024 records. Keep train/test splits chronological.
5. Continue to exclude any feature whose pre-kickoff availability cannot be proven; do not impute or fabricate.

## Governance
Research only. No production model logic, frozen probabilities, thresholds, calibration or production ledgers changed. Production/betting eligibility remains NOT_GRANTED.
