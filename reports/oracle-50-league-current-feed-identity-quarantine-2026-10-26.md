# Selected-50 Current-Feed Identity Quarantine — 2026-10-26

**Status:** Research-only diagnostic; production eligibility NOT GRANTED.

## Build verification

- Branch: `research/oracle-50-league-readiness-audit`
- Commit: [2d349ae6b1803710cadc0ed7920861cfe94cd9c5](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/commit/2d349ae6b1803710cadc0ed7920861cfe94cd9c5)
- Workflow: [40257455170 — SUCCESS](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40257455170)
- Artifact: [12622932928](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40257455170/artifacts/12622932928)
- Artifact SHA-256: `99d8b6d7911e7fde973f094f0b186a4ce10a45857fbec5a7b2e5daff55c172f3`
- Artifact ZIP checksum was independently recomputed and matched the GitHub digest.
- The run completed all 28 steps successfully; the new identity-quarantine builder, regression test and artifact upload passed.

## Inputs and method

The no-network diagnostic joins the existing 50-row crosswalk revision r17 (blob `2c23ac9d42f0b8cf85111ea5e431b234cc164ab4`) to the current-feed identity-collision audit (blob `16e277b6659b6a4a0110fecee0e5d6f1c492950d`) by exact selected season ID. It classifies missing labels, multi-ID label collisions, absent country retention, absent exact league-ID allowlists and unverified provider-season-to-feed bridges. It does not export current-feed examples or raw provider payloads.

## Verified results

| Measure | Result |
|---|---:|
| Selected season IDs | 50 |
| Unique IDs in both sources | 50 / 50 |
| Groups with any current-feed display-label rows | 12 |
| Groups with multiple feed league IDs under a label | 5 |
| Groups with country field retained | 0 / 50 |
| Groups filtered by exact league-ID allowlist | 0 / 50 |
| Verified provider-season-to-feed bridges | 0 / 50 |
| Candidate crosswalk rows requiring review | 22 |
| Unresolved crosswalk rows | 28 |
| Approved crosswalk rows | 0 |
| Canonical fixture joins verified | 0 |
| Canonical team joins verified | 0 |
| Official settlement truth verified | 0 |
| Production-eligible rows | 0 |
| Network / paid-provider calls | 0 / 0 |

### Primary blocker distribution

| Primary blocker | Groups |
|---|---:|
| No matching current-feed label | 38 |
| Ambiguous display label matching multiple feed league IDs | 5 |
| Country not retained in current feed | 7 |

The 12 groups with a display-label hit are not verified matches. Five are ambiguous; the other seven still lack country retention, an exact allowlist and a verified bridge. A single feed league ID is not proof of canonical competition identity.

## Interpretation and remediation

1. Do not use display-name-only current-feed rows for Selected-50 canonical joins.
2. Do not infer parent competition IDs or provider-to-FotMob mappings from selected season IDs, labels or candidate canonical codes.
3. Reconcile only from approved existing evidence. If no authoritative bridge is available, use the existing bounded provider-probe gate after explicit provider-credit confirmation.
4. Keep official settlement truth, historical standings-as-of-kickoff, xG/odds chronology and canonical fixture/team joins unverified until independently evidenced.
5. Combo remains blocked by its predictor/settlement definition mismatch; M-1UP remains blocked by its independent event-truth gate.

## Governance

This is a research-only reporting/quarantine change. Production model logic, probabilities, calibration, thresholds and the frozen 27-league baseline are unchanged. No private-repository Actions, provider API calls or extra spend occurred. All Selected-50 rows remain production-ineligible.
