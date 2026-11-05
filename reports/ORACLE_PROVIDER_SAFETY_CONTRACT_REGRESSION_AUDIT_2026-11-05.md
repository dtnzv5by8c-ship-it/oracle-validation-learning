# Project Oracle — Provider Safety Contract Regression Audit — 2026-11-05

## Scope

Offline inspection of the latest research-branch CI after the 49-vs-50 scope audit. No provider API calls were made by this audit. No private repository was modified. Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers and betting eligibility were not changed.

## Live branch state

- Branch: `research/oracle-50-league-readiness-audit`
- HEAD verified immediately before this commit: `14aaa17863d6abc71ae014c21794cbafa465d3af`
- No intervening branch movement was observed during this audit.
- Mapping-owned paths were not edited.

## CI finding

The latest Oracle Selected-50 Dry-Run Planner run `41980687165` is **FAILED**, but its failure is not a model or data-quality failure.

The planner reached the offline validation stage successfully:

- dry-run plan generation: PASS
- conservative market gates: PASS
- planner regression tests: PASS
- market gate regression tests: PASS
- exact catalogue resolver tests: PASS
- prediction input contract tests: PASS
- governed Selected-50 compatibility contract: PASS

The failure occurred in the **FootyStats identifier separation contract** test suite.

## Root cause

The public workflow `.github/workflows/footystats-selected50-catalogue-resolver.yml` still contains:

- a `FOOTYSTATS_API_KEY` secret reference;
- an environment variable populated from that secret;
- direct access to the FootyStats API endpoint;
- a one-call provider request;
- logic intended to resolve and write a Selected-50 catalogue.

This conflicts with the current public-repository safety contract, which requires provider-calling credentials and provider access to be centrally controlled and prevents the public research repository from becoming an alternative provider gateway.

The CI also reports a second contract regression: the retired global preflight workflow no longer contains the required serialized central-gateway marker expected by the existing safety contract.

This is therefore a **governance/safety-contract mismatch**, not evidence that provider data are available or that the 50-league catalogue has been validated.

## Required disposition

1. Do not rerun the failing resolver workflow.
2. Do not provide it with the FootyStats API key.
3. Do not treat its failed run as successful catalogue resolution.
4. Keep the controlled historical plan at its currently governed scope until the mapping owner explicitly resolves the 49-vs-50 discrepancy.
5. Preserve the private ingestion gate and the signed archive/budget receipt requirements.
6. Repair the public workflow/safety-contract mismatch through the owning workflow/mapping process rather than bypassing the contract in hourly completion.
7. Keep production and betting eligibility false.

## Current safety state

`production_eligible=false`

`betting_eligible=false`

No raw provider payloads or secrets were added by this audit. No Oracle V1.6 production logic or probability output was modified.
