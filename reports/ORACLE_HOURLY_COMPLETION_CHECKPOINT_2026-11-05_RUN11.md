# Project Oracle — Hourly Completion Checkpoint — 2026-11-05 Run 11

## Scope

Offline/research-only continuation from the live `research/oracle-50-league-readiness-audit` branch. No provider API requests were made by this checkpoint. No private `oracle-football-data` repository was modified. No Oracle V1.6 production logic, probabilities, thresholds, calibration, ledgers or betting eligibility were changed.

## Live branch reconciliation

Live branch HEAD was fetched immediately before this checkpoint commit:

`99b93123fa698e6e470a67f47c455a4d6051363f`

Latest commit message:

`test: align FootyStats contracts with Selected-50 resolver architecture`

The branch has advanced materially beyond the supplied 2026-11-04 checkpoint. The intervening changes were inspected at the workflow/report/test level before this checkpoint was written.

Mapping-owned paths were not edited.

## Current architecture state

The public research branch now has a Selected-50 catalogue resolver workflow and matching contract tests. The resolver has been corrected to parse season years using the intended four-digit-year pattern and the tests now assert the resolver's exact-50 and provider-season uniqueness requirements.

However, the current governed historical evidence remains **49 selected provider leagues / 756 catalogue season rows / 182 provider-season partitions / 728 planned ingestion tasks**. The resolver's 50-league contract therefore remains a separate scope-resolution mechanism, not evidence that the current 49-league catalogue has become a verified 50-league universe.

The current decision queue still records:

- 22 candidate canonical mappings requiring human approval;
- 0 approved canonical mappings;
- 5 current catalogue leagues without prior legacy-50 identity;
- 6 legacy-50 leagues absent from the current selected catalogue.

No mapping promotion was performed.

## Provider safety finding

The current public resolver still contains a direct `FOOTYSTATS_API_KEY` secret reference and direct FootyStats API access for its single catalogue metadata call. This is retained as a **mapping/workflow-owner issue** and was not modified by hourly completion.

The retired global preflight workflow is now a fail-closed stub. The hourly completion process did not attempt to bypass either contract.

The resolver must not be treated as a substitute for the controlled historical ingestion gateway, and its output must not be treated as historical fixture data.

## Historical feature admission

The following remain blocked or quarantined pending exact fixture-level source evidence:

- fixture identity;
- team identity continuity;
- kickoff chronology;
- result/score admission;
- H2H;
- recent form;
- home/away form;
- fixture-time standings;
- point-in-time xG.

The existing Run56 aggregate evidence remains insufficient for fixture-level identity because aggregate evidence does not expose the fixture IDs and ordered home/away team IDs required for admission. The existing settlement register remains only a 10-fixture research bridge with zero canonical bridge approvals and zero settlement-truth approvals.

The `no_home_away` condition remains a quarantine state; it is not interpreted as neutral venue.

## OMI / Oracle V1.6 reporting

The exact Oracle V1.6 Output schema remains the locked 68-column A:BP contract with header hash:

`4899b305eda7e156e3e1b2d398b02cac869b1df21e378fecaf991074012c22f7`

The 38-column Analyst Summary and 95-column OMI/Market Intelligence contracts remain separate. No data-backed current OMI workbook was generated.

## Eligibility and acquisition status

- Planned historical tasks: 728
- Completed controlled historical ingestion: 0
- Provider requests by this checkpoint: 0
- Production eligible: false
- Betting eligible: false
- Oracle V1.6 production logic: frozen
- Oracle V1.6 probabilities: unchanged
- Thresholds/calibration: unchanged
- Ledgers: unchanged
- Raw provider payloads/secrets added to public research repository: none
- Private repository modified by this checkpoint: no

## Safe next action

Continue offline validation only. Do not dispatch the public resolver from hourly completion, do not run provider acquisition directly, do not bypass the private controlled ingestion gate, and do not promote any 49-to-50 mapping automatically.

The next data-admission milestone remains a trusted fixture-level identity contract containing at minimum provider season ID, provider fixture ID, exact UTC kickoff, homeID, awayID, competition ID, result status and score, with duplicate/conflict rejection and provenance controls.
