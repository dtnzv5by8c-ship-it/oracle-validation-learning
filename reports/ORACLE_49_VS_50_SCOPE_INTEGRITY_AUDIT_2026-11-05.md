# Project Oracle — 49-vs-50 Scope Integrity Audit — 2026-11-05

## Scope

Offline governance audit of the live research branch. No provider API calls, no private-repository writes, no Oracle V1.6 production changes.

## Live HEAD

- Branch: `research/oracle-50-league-readiness-audit`
- HEAD verified immediately before this commit: `ab6a4d1f5dcc01458afa726f90a0dec4616ba533`
- Supplied checkpoint base: `4c859c5f2bdfa29fcfc70e601836e2c7e95aeba0`
- Intervening commits: 19
- Mapping-owned paths were not modified by this audit.

## Finding

The governed historical research scope currently reconciles to **49 selected provider leagues**, not 50:

- selected catalogue: 49 leagues
- catalogue season rows: 756
- historical provider-season partitions: 182
- planned controlled ingestion tasks: 728
- approved canonical mappings: 0

However, the newly committed public workflow `.github/workflows/footystats-selected50-catalogue-resolver.yml` is labelled and implemented as a **Selected-50** resolver and contains an internal assertion requiring:

`len(set(resolved selected_id)) == 50`

It also constructs a registry with `selected_league_count: 50`.

This creates a governance mismatch between the current **49-league governed catalogue** and the workflow's **50-league resolver contract**.

## Why this matters

The mismatch must not be resolved by silently adding a 50th league, promoting one of the 22 unresolved canonical candidates, or treating the legacy 50-league universe as identical to the current 49-league catalogue.

The mapping audit currently records:

- 5 current catalogue leagues are new relative to the legacy-50 reconciliation.
- 6 legacy-50 leagues are absent from the current selected catalogue.
- 22 candidate canonical mappings remain unapproved.
- 0 canonical mappings have been promoted.

Therefore the number 50 cannot be used as evidence that the current 49-league catalogue has been fully resolved.

## Required disposition

Until the scope is explicitly governed by the appropriate owner:

1. Treat the **49-league catalogue** as the authoritative current research scope.
2. Treat the Selected-50 resolver as **non-authoritative research infrastructure** and do not dispatch it as a substitute for the controlled historical ingestion plan.
3. Do not create a 50th current league by inference.
4. Do not promote any canonical mapping solely to make the count equal 50.
5. Keep the 728-task historical plan and its existing eligibility gates unchanged.
6. Preserve the private ingestion safety gate and do not execute provider requests from this audit.

## Governance

`production_eligible=false`

`betting_eligible=false`

Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility remain unchanged.

No raw provider payloads or secrets were added.
