# Project Oracle — 50-League Readiness Classification Checkpoint

Date: 2026-11-06

## Scope

The governed target is the updated 50-League Universe for prediction/model readiness, using the existing Oracle/OMI contracts and historical window from 2024 through current.

## Changes

- Hardened the offline feature-readiness validator to emit per-league READY/PARTIAL/BLOCKED classification.
- READY requires all governed feature families.
- PARTIAL requires valid league/provider/season identity and season window plus at least one ready feature.
- BLOCKED covers invalid identity/window or zero ready feature families.
- Added deterministic missing-feature reporting and aggregate status counts.
- Added regression coverage for all three readiness states.

## Governed feature families

Recent form, H2H, league position, xG/goals, BTTS, win/draw probability, fixture/team IDs, pagination, chronology and freshness.

## Safety

- Provider calls: none.
- Gateway receipt: not fabricated.
- Oracle V1.6 production logic/probabilities: unchanged.
- Incomplete data remains inadmissible to production prediction.

## Current upstream state

The live 50-league acquisition manifest remains the source of truth: 50 leagues, 182 provider seasons and 728 planned endpoint tasks. Historical ingestion remains gated until an approved private gateway receipt is proven.

## Test note

The regression files were updated for the new classification contract. Local execution in this automation environment could not clone the public repository because outbound DNS/network access is unavailable; therefore no local test execution is claimed.
