# Project Oracle — autonomous research workflow readiness checklist

Date: 2026-10-21  
Scope: Research pipeline only; production governance unchanged.

## Verified in latest run

- [x] Research workflow runs on GitHub Actions using the public validation repository.
- [x] Private archive and catalogue are retrieved from previously acquired releases using the existing repository token.
- [x] Archive feature audit, integrity audit, provisional standings, season coverage matrix, candidate crosswalk, and alias classification complete in one successful run.
- [x] Parser, chronology, and archive-freshness unit-test suite passes in latest run.
- [x] Archive release freshness gate passes for the current release.
- [x] Archive checksum is recorded during the workflow run.
- [x] Current archive audit run made zero provider API calls.
- [x] Artifact is published with 30-day retention.
- [x] Research output explicitly marks production eligibility as not granted.
- [x] No production model logic, probability, weight, threshold, calibration, model version, or canonical registry was changed.

Latest verified run: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39631140733  
Artifact: https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39631140733/artifacts/12359351767  
Commit: 7d212fd30d71e3659407c23f00d76363bc99c26e

## Remaining before full autonomous operation

- [ ] Add a schedule only after archive refresh cadence and approved source process are established. The current workflow audits a previously acquired archive; it does not refresh provider data.
- [ ] Add explicit failure/stale-data notifications and coverage-change summary delivery. A failed workflow is visible in GitHub Actions, but proactive alert delivery has not been verified.
- [ ] Review token scope and rotation arrangements without exposing secrets.
- [ ] Confirm provider spend caps and avoid new paid API calls unless explicitly approved.
- [ ] Resolve the authoritative intended 44-league list and review all 43 provider competition names before canonical mapping.
- [ ] Verify pre-kickoff provenance for xG and odds; field presence is insufficient.
- [ ] Validate provisional historical standings against official tables and each competition's actual format.
- [ ] Recover immutable timestamped historical production predictions and verified settlements if available outside the inspected repository; otherwise rely on prospective evaluation.
- [ ] Continue testing source timestamps and feature-builder chronology where trustworthy point-in-time metadata exists.
- [ ] Keep research outputs isolated from production model code and canonical registry.

## Current assessment

The research archive audit is repeatable and the latest run passed its release freshness gate and all audit stages. It is not yet fully autonomous: it does not refresh the provider archive, and proactive notifications have not been implemented/verified. The intended 44-league universe and authoritative competition mapping remain unresolved. Historical production accuracy remains data-gated because verified immutable prediction/settlement pairs were not recovered. Production eligibility remains NOT_GRANTED.

No production logic or canonical registry changes are authorized by this report.
