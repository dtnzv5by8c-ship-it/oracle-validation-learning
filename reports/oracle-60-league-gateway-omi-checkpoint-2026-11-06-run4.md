# Project Oracle — 60-League Gateway/OMI Checkpoint — 2026-11-06

## Scope
Governed target: Oracle-60-League, historical window 2024-current.
Branch: research/oracle-50-league-readiness-audit.

## Evidence reviewed
- Live branch contains the fail-closed private gateway receipt validator.
- The validator requires private archive evidence, 60-league scope, 2024-current history, approved transport, PASS auth/rate-limit, recent transport verification, immutable SHA-256, and non-public provider data.
- The governed private receipt locator remains required before historical ingestion.
- No public FootyStats retry or Cloudflare bypass was performed.

## Fix completed
A live-branch inspection found duplicate declarations in the Master OMI feature-join validator:
- duplicate league_count_incomplete append;
- duplicate --require-complete argparse option.

Both were removed in commit ae261ab4a195cd339cfa9a6097241f9847291cab.

## Regression execution
Added .github/workflows/oracle-master-omi-regression.yml in commit 883e3693acff30f27c0080e0634841a25c27f9d4.
GitHub currently reports no workflow run associated with that commit, so CI execution is not claimed.

The existing offline regression coverage still exercises:
- valid Master OMI row;
- missing H2H;
- blank/duplicate Fixture ID;
- missing provider season;
- invalid actual goals/result;
- invalid kickoff;
- 59-league universe with --require-complete => BLOCK.

## Admission status
Historical 2024-current ingestion remains BLOCKED until the approved private 60-league gateway/archive receipt is proven.

## Governance
No provider data or credentials were added to the public repository.
No provider request was made.
Oracle V1.6 production logic, probabilities, thresholds and governance were not modified.

## Next action
When the private receipt becomes available, validate it immediately, then admit only bounded ingestion batches and apply fixture/team identity, pagination, chronology, freshness and Master OMI feature-readiness gates before any reporting/backtesting promotion.