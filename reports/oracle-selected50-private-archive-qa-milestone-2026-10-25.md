# Oracle Selected-50 Archive QA Milestone — 2026-10-25

## Status

Research-only validation. Production readiness remains NOT GRANTED. Oracle production logic, production probabilities, calibration and thresholds were not changed.

## Verified workflow results

- Private archive QA: success — https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40179979282
- Regression/dry-run planner: success — https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40179979357
- QA artifact: `oracle-selected50-private-archive-qa`, sanitized-only, short retention.
- Private source release: `research-selected50-footystats-ingestion-20261025`.

## Archive QA findings

- 50/50 selected seasons have `INGESTED` manifest status and all required JSON files parse.
- 14,051 match records; 14,051 unique season/fixture-ID pairs; no duplicate fixture-ID pairs detected within seasons.
- Kickoff-like field, team-ID pair, team-name pair, and explicit score pair exist in all 14,051 records.
- Observed date range: 2026-01-16 to 2027-06-06 UTC/string date.
- Date-based preliminary split: 6,912 records have past kickoff dates; 7,004 have future kickoff dates. The remainder fall on the current UTC date or have classification edge cases.
- Provider status values: `complete` 6,916; `incomplete` 7,083; `suspended` 52.
- Non-empty odds-named values appear in 7,330 records. This is not proof of valid bookmaker, market, timestamp, or pre-kickoff odds.
- Non-empty xG-named and prematch-xG-named values appear in all 14,051 records. This is not proof that values are genuine, correctly scaled, valid for the fixture, or available as of kick-off.
- The raw archive remains private. The QA artifact contains sanitized aggregate data and observed field names only.

## Important interpretation

A populated score pair is not sufficient evidence that a match is settled: future-dated records also contain numeric score fields, and provider status/date semantics require further verification. Likewise, field presence and non-empty values do not establish point-in-time provenance. Do not use these counts as prediction-input coverage or model accuracy.

## Existing gaps

1. The ingestion ledger has blank `provider_league_id` for all selected seasons despite exact season-ID matches. The current resolver reads `league.get("id")` only; this likely reflects a catalogue schema mismatch, but the actual parent-ID field has not yet been established from a sanitized catalogue schema audit.
2. The current archive covers the selected 50 season IDs, but it is not a validated prediction feature store.
3. Recent form, H2H, standings chronology, fixture identity joins, xG provenance, odds provenance, and market-specific feature readiness have not passed dedicated tests.
4. Historical prediction accuracy and calibration improvement have not been demonstrated.
5. Earlier dry-run market gates remain conservative: BTTS Yes, Double Chance, DC + Under 4.5 are NOT VERIFIED; M-1UP is BLOCKED.

## Next actions

1. Audit the exact league-list catalogue object schema and safely resolve the parent competition ID only from an explicit provider field; do not guess IDs or spend credits on a full re-ingestion just to test this.
2. Extend QA with strict status/date/score settlement rules, numeric value distributions and sample-level consistency checks that do not publish raw provider payloads.
3. Validate standings, team identity, recent form, H2H, xG and odds separately, including as-of-kickoff availability.
4. Join selected fixture IDs to Oracle prediction outputs exactly; quantify missingness and reject ambiguous/fuzzy joins.
5. Backtest only on predictions actually recorded before kick-off, settle against verified outcomes, report hit rate by market/league and calibration metrics, and compare selection filters out-of-sample.
6. Keep production model logic and probabilities unchanged until evidence is sufficient for a separately governed approval.

## Governance

No model redesign, production code change, probability change, calibration change, or production promotion is authorized by this milestone. No accuracy or profitability claim is made.
