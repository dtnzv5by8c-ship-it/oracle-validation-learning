# Oracle Selected-50 Progress Checkpoint — 2026-10-28

**Checkpoint time:** 2026-10-28 05:10 SAST  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Latest audited code/workflow commit:** `72959792c45a2c2b153beb9612a2f826e67dd316`  
**Decision:** Research QA PASS for the validated workflows; production and betting release NOT APPROVED.

## 1. Newly verified workflow results

| Workstream | Run | Result | Artifact |
|---|---|---|---|
| FootyStats Archive Feature Audit | [#60 / 40624909115](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624909115) | PASS — 198 tests passed; archive audit steps completed | [#12788389889](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624909115/artifacts/12788389889) |
| Selected-50 Dry-Run Planner | [#468 / 40624909114](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624909114) | PASS — offline plan, identity quarantine and readiness checks passed | [#12789091929](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624909114/artifacts/12789091929) |
| Safety Contract Tests | [#162 / 40624909188](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40624909188) | PASS | No artifact |

The archive-audit failure at Run #59 was traced to missing `scikit-learn` in the test environment. The research workflow now installs its existing test dependencies before test discovery; Run #60 passed. This is a workflow/test-environment correction, not a production model change.

Run #60 archive artifact SHA-256: `cfc1fd08023a59d116e0c32acfed7ee50d13826e1118863161bed5e3af9d8db2`.  
Run #468 planner artifact SHA-256: `08565001d8ce17c629d320c194fa5400dbfec2ba4aad8f05a504dc3a6ed7e7fc`.

## 2. New research evidence

- Archive audit processed 126 archive league-season groups, 35,819 match rows, 35,819 feature rows and 35,819 provisional standings rows.
- Existing selected-50 archive scope remains 50 season IDs across two evidence layers: 31 manifest matches and 19 retained private-package QA gap reconciliations. This is archive coverage evidence, not canonical identity approval.
- Prediction-ledger staging remains fail-closed: 210 rows lack home-team IDs and 210 lack away-team IDs; verified fixture identity = 0; score-eligible rows = 0.
- Exact fixture-candidate audit: 105 competition-aligned candidates, 20 competition mismatch/crosswalk gaps, 85 without an exact kickoff/team candidate; 0 verified and 0 score-eligible.
- The broader archive name crosswalk (43 provider names; 25 review; 18 unmatched) is a different population from the selected-50 crosswalk (22 review; 28 unmatched); do not conflate them.
- No provider API requests were made in Runs #60, #468 or #162.

## 3. Release blockers — unchanged

1. Canonical identity: parent competition IDs verified 0/50; provider-to-canonical bridges approved 0/50; human-approved mappings 0.
2. Current feed: governed fixture slate is still unavailable/stale; the research/archive-derived slate must not be represented as a current production fixture feed.
3. Fixture/team joins: ledger has 0 verified fixture identities and 0 score-eligible rows in the audited adapter.
4. Settlement: all 7,066 non-complete numeric 0–0 rows remain excluded from settled truth. Official settlement truth and canonical fixture joins remain unverified.
5. Combo markets: predictor target and settlement helper disagree on 0–1-goal outcomes. Combo probabilities remain masked until the authoritative definition is approved.
6. Point-in-time feature/odds provenance and calibration/betting edge are not established. Raw walk-forward metrics are not betting-ROI evidence.

The single authorized FootyStats probe is complete and must not be repeated without fresh explicit approval and a verified credit budget. Its one Argentina Primera División season sample does not verify a parent competition ID or the other 49 leagues.

## 4. Production protection

No changes were made to the production repository, Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected canonical registry, ledgers or governance. Research and betting eligibility remain `false`.

## 5. Next actions, in order

1. Diagnose the governed current-feed freshness failure from its manifest/ingestion run records; only refresh through an already-approved safe path, without provider API calls.
2. Use official public documentation and existing archives to strengthen candidate identity evidence; leave ambiguous rows quarantined. The provider support clarification remains a draft and has not been sent.
3. Reconcile the 210 missing team-ID rows and 190 unverified fixture candidates against exact canonical IDs and kickoff evidence; do not score unverified joins.
4. Keep non-complete 0–0 exclusion and Combo masking; do not change settlement semantics without authoritative rules.
5. Publish a final 50-league go/no-go matrix. A deadline does not override failed gates.

## 6. Final decision

**Research validation for the three runs above: PASS. Overall Selected-50 production readiness: BLOCKED. Betting release: BLOCKED.** The current evidence does not justify production release, and the production model remains unchanged.
