# Master OMI MI Root-Cause Cycle — 2026-11-26 04:01 SAST

## Purpose
Drive the rolling 50-league Master OMI MI layer toward release readiness without reusing a dated frozen spine or mutating A:ET / Oracle V1.6.

## Latest QA evidence
- QA artifact: MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-26_0332SAST.md
- QA blob SHA: 67fb7c07bdb3f11da9562b4913d5be9a768f7f8e
- Decision: FAIL-CLOSED
- Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

## Current rolling source
- Path: data/fixtures/governed_50league_current.csv
- Persisted blob SHA at audit: 65e8c3cc04e51c2151c4b4c9d10a3368232e5cd0
- Current manifest generated_utc: 2026-11-26T01:33:05.928823+00:00
- Fixture rows: 371
- Unique provider Fixture IDs: 371
- Provider: FootyStats
- Identity: EXACT_PROVIDER_FIXTURE_ID
- No dated frozen weekly spine accepted.
- At 04:01 SAST this artifact exceeds the 90-minute freshness gate and is therefore not accepted as the current cycle source.

## Root-cause matrix
| Field/domain | Scope | Cause | Authoritative source | Fix/status |
|---|---|---|---|---|
| Rolling fixture spine | 50 leagues | Persisted current snapshot stale for this cycle | FootyStats todays-matches | Producer workflow is hourly/dispatch-capable; fresh execution must replace stale blob. |
| Prediction ledger | 754 production fixtures | Current authoritative ledger absent from public default branch | Oracle production repository / V1.6 | BLOCKED; do not fabricate or reuse dated ledger. |
| Prematch Team State | 754 production fixtures | Current authoritative file absent from public default branch | Oracle production repository | BLOCKED; do not substitute stale state. |
| Current matches | 754 production fixtures | Current authoritative file absent | Oracle production repository | BLOCKED; do not substitute stale data. |
| Last-5 | rolling fixtures | Prior unsafe LastX dependency removed | FootyStats league-matches | FIXED in producer; strict pre-kickoff cutoff. |
| Venue Last-5 | rolling fixtures | Overall/venue mapping defect | FootyStats league-matches | FIXED; separate venue filters. |
| FootyStats PPG/GF/M/GA/M/goal intelligence | rolling fixtures | Intermediate values previously not persisted | FootyStats league-teams | FIXED; persisted with source/cutoff/status. |
| H2H | rolling fixtures | Fixture-level H2H not previously emitted | FootyStats league-matches | FIXED; exact provider IDs and pre-kickoff cutoff. |
| xG provenance | production | No capture timestamp | authoritative xG source evidence | BLOCKED/UNVERIFIED; no post-kickoff substitution. |
| Kickoff reconciliation | production | 67/754 mismatches | governed fixture spine vs authoritative source | BLOCKED; exact reconciliation only. |
| A:ET | production | Immutable production surface | canonical V2.1.1 | PRESERVE EXACTLY. |
| Oracle V1.6 | production | Production logic immutable | canonical Oracle V1.6 | PRESERVE EXACTLY. |

## Release rule
Do not build or promote a release workbook until fresh rolling input, authoritative current production inputs, fresh 754-fixture MI, exhaustive cell-level coverage/type/provenance/chronology/leakage audit, and independent candidate-binary QA all pass.
