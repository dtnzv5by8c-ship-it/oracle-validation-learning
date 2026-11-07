# Project Oracle — HTTP-417 Access Root-Cause Diagnostic Prepared

Date: 2026-11-07
Governed validation branch: `research/oracle-50-league-readiness-audit`
Private diagnostic workflow commit: `75b22ecadca933a32b3477bc1265bd870c5682cb`

## Why this was added

The targeted HTTP-417 recovery attempt #1 used three transport variants and consumed 300 provider requests, with 300/300 responses returning HTTP 417 and 0/80 tasks recovered. Repeating that transport experiment is prohibited unless new evidence exists.

A materially different diagnostic is therefore prepared: determine whether the exact 20 blocked provider-season partitions are:
1. outside the account's chosen-league entitlement,
2. absent from FootyStats' API database,
3. present in chosen access and therefore indicative of an endpoint/provider transport problem, or
4. inconclusive because the diagnostic itself cannot retrieve the league list.

## Diagnostic method

Workflow:
`.github/workflows/footystats-private-access-diagnostic.yml`

It performs only two provider calls:
- `league-list?chosen_leagues_only=true`
- `league-list`

It then compares the exact 20 blocked provider-season IDs against:
- seasons visible under the account's chosen access;
- seasons present in the provider database.

No match/team/table/season recovery calls are made, and no production data is admitted.

## Manual action

The GitHub connector cannot dispatch a newly-created `workflow_dispatch` workflow. Therefore manual execution is required.

Recommended input:
- `confirm_provider_api_usage=true`

No request-cap input is needed; the workflow is hard-capped at two provider calls.

## Governance

Production/betting eligibility remains false.
Oracle V1.6 production logic, probabilities, thresholds, calibration, betting eligibility and governance are unchanged.

## Anti-repetition

Do not rerun HTTP-417 recovery attempt #1's transport matrix. This diagnostic exists specifically to determine whether the blocker is access entitlement, provider database coverage, or endpoint/transport behavior before any further recovery request is considered.
