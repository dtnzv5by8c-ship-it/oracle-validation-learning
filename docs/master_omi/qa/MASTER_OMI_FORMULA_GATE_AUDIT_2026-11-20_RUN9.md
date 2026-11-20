# Master OMI Formula Input Release Gate — Run 9

Date: 2026-11-20
Repository: dtnzv5by8c-ship-it/oracle-validation-learning

## Release status

**FAIL-CLOSED / NOT RELEASE-ELIGIBLE**

Run 9 re-audited the latest persisted Master OMI Formula Input Release Gate evidence and repository state after Run 8. No newer candidate workbook or governed-data repair has been committed after the Run 8 fail-closed repair. Therefore the latest auditable candidate remains the Run 8 repaired workbook and its QA evidence remains authoritative for this cycle.

## Canonical integrity

Canonical V2.1.1 SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
Run 8 repaired candidate SHA-256: 643695bc94f318fe10bbd7e47d9781db8921896dbc0c6fb7400598b8f3c3d237
A:ET semantic comparison against canonical baseline: **0 differences**.
Market Intelligence dimensions: **755 x 264**.
Heading comments: **264/264**.
Oracle V1.6: unchanged.

## Current gate result

- Formula Input Ready: **5/387 (1.29%)**
- Formula Input Blocked: **382/387 (98.71%)**
- RELEASE_DECISION PASS: **5/387 (1.29%)**
- RELEASE_DECISION FAIL: **382/387 (98.71%)**
- BACKTEST_READY: **0/387**
- Forbidden PASS + blocker combinations: **0** in the repaired candidate.
- Exact FootyStats identity only; no silent fuzzy matching.
- Missing evidence remains UNAVAILABLE/UNVERIFIED; no missing-to-zero or guessed estimates.
- xG without verified point-in-time provenance remains quarantined.
- Implausible goal-environment values remain quarantined; no divide-by-10 or guessed transformation.

## Remaining blockers

The release remains blocked by unresolved mandatory per-fixture conditions including required Market Intelligence coverage below 100%, identity review, kickoff/date reconciliation and/or invalid numeric-range evidence. Independently verified actuals plus exact governed fixture/date identity are also required for BACKTEST_READY.

## Regression decision

No newer governed workbook/data commit was found after the Run 8 release-gate repair. The current persisted state therefore has **no new evidence permitting promotion**. Release remains FAIL-CLOSED and hourly rechecks must continue.

## Governance

No Oracle V1.6 production logic was changed. No A:ET insertion, deletion, reorder or overwrite was permitted. This run does not fabricate unavailable evidence and does not alter the canonical schema.
