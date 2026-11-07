# H2H Reporting Run #53 — Alias Regression Correction
Date: 2026-11-07
Run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/42373095450
Source SHA: 369d466fab0b6ea4285201f81e9e97cde2d8a998

## Finding
Run #53 stopped before report generation because the newly added alias regression tests exposed two incorrect mappings. The post-failure quality step also reported a missing audit artifact because the report step was skipped.

## Evidence
- All earlier H2H reporting preparation, history extension, and backtest stages completed successfully.
- Alias test failures: `1. FC Köln` vs `Köln` normalized to `1fckoln` vs `fckoeln`; `Bohemians` vs `Bohemians 1905` normalized to `bohemians` vs `bohemians1905`.
- H2H report build and exact-ID join were skipped after the regression step failed.
- Quality-gate job then failed because `reports/h2h/h2h_audit.json` had not been generated. This is a downstream consequence, not a separate root cause.

## Root Cause
Two alias pairs asserted by the regression gate were not represented in the canonical reporting alias map.

## Fix
Reporting-only change adds `1fckoln|fckoeln|koln|cologne` and `bohemians|bohemians1905` as shared aliases. This does not touch fixture IDs, competition IDs, historical results, Oracle model logic, probabilities, calibration or eligibility.

## Validation
Fix committed as `3d699e3c975964f12193fb5ffceacec46b6faec4`. A fresh push-triggered workflow run is required to validate the alias regression suite and then proceed to H2H report, exact ID join and the unchanged 20% unresolved identity threshold.

## Governance
Do not weaken the unresolved identity gate. Keep cross-league historical matches quarantined. No production Oracle V1.6 changes.

## Run #54 follow-up
Run #54 failed the alias regression test again on `1. FC Köln` vs `Köln`. Cause: source normalizer produced `1fckoln`, but alias group did not include that exact normalized token. Added `1fckoln` to the canonical group in commit `eea3849e4712d0ccab404b693a82d89630aa5dcb`. Bohemians regression now passes in Run #54. Another push-triggered run will validate the corrected FC Köln alias. Report build and ID join remain untested in Run #54 because the alias test stopped the workflow early.

## Run #55 root cause
Run #55 still failed `1. FC Köln` vs `Köln` because the alias map contained two groups: the corrected `1fckoln|fckoeln|fckoln|koln|cologne` group was later overridden by the older `fckoeln|koln|cologne` group. This was an alias precedence/duplicate-definition defect, not a missing normalization. Removed the duplicate overriding group in commit `a2581f296fe37c89ba3898f963177425b8c44efb`. Next push-triggered run must re-execute the regression gate before H2H report generation.
