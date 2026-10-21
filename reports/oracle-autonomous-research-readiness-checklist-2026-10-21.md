# Project Oracle — autonomous research workflow readiness checklist

Date: 2026-10-21  
Scope: Research pipeline only; production governance unchanged.

## Verified

- [x] Research workflow can run on GitHub Actions using the public validation repository.
- [x] Private archive and catalogue are retrieved from previously acquired releases using the existing repository token.
- [x] Archive feature audit, integrity audit, provisional standings, season coverage matrix, and candidate crosswalk complete in one successful run.
- [x] Six parser/status unit tests pass.
- [x] Current archive audit run made zero provider API calls.
- [x] Artifact is published with 30-day retention.
- [x] Research output explicitly marks production readiness/eligibility as not assessed/not granted.

## Still required before calling the workflow autonomous/production-ready

- [ ] Confirm an approved cadence and add a scheduled trigger only after deciding how often the data archive itself should be refreshed. The current archive audit is manual/push-triggered; it does not refresh provider data.
- [ ] Add a freshness gate based on archive release date, manifest dates and expected update cadence; fail visibly when stale.
- [ ] Add alerting/summary on failed runs, stale inputs, incomplete seasons and changed coverage.
- [ ] Review token scope and rotation arrangements without printing or exposing secrets.
- [ ] Confirm provider spend caps and avoid new paid API calls unless explicitly approved.
- [ ] Resolve the authoritative intended 44-league list and review all 43 provider competition names before any canonical mapping.
- [ ] Verify pre-kickoff provenance for xG and odds; field presence is insufficient.
- [ ] Validate historical standings against official historical tables and each competition's actual format.
- [ ] Establish immutable timestamped prediction snapshots and verified settlements to support prospective and historical accuracy reporting.
- [ ] Add separate chronology/leakage tests that exercise the actual feature builder, including same-kickoff events, postponed/unknown status, and point-in-time source timestamps.
- [ ] Keep research outputs isolated from production model code and canonical registry.

## Current assessment

The research audit pipeline is repeatable in a successful manual/push-triggered run, but full autonomous weekly operation is NOT yet demonstrated. It currently audits a previously acquired archive; it does not independently refresh provider data or verify prediction accuracy. No production logic or canonical registry changes are authorized by this report.
