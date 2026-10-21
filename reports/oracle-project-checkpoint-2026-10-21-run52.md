# Project Oracle research checkpoint — 21 October 2026 — Run #52

## Executive status

**Research archive audit: PASS. Prediction evaluation: BLOCKED. Production readiness: NOT GRANTED.**

Run #52 verifies that the research-only changes merged to the validation repository's `main` branch execute successfully. This is not an Oracle production release and does not establish historical prediction accuracy. No production model logic, weights, probabilities, thresholds, calibration, model version, or canonical league registry were changed.

- Workflow: [Run #52](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39658148278)
- Result: `success`
- Commit: `96bc5d800a0e1cafb53ec795b248fa17a5f7ba15`
- Artifact: `oracle-footystats-archive-feature-audit`, ID `12371679825`
- Artifact SHA-256: `80a354dcd2b183c1a25416fb5ebfc05d8a32900b7d0c35076abf228d79132fab`
- Archive release hash recorded by the audit: `3fea4fbc0b81595fd9fca6691f8eac66efa9ea1d5ac30460bf3646e8dad951ba`
- Archive freshness: `FRESH` (release age 0.599 days at the workflow check)
- The workflow reused the acquired archive/catalogue and made no provider API calls in this audit run.

## Run #52 results

| Check | Verified result |
|---|---:|
| Archive match records | 35,819 |
| Season folders/groups | 126 |
| Parse errors | 0 |
| Rows with parseable kickoff | 35,819 |
| Rows with archive team IDs | 35,819 |
| Rows with final score and settled status | 28,491 |
| Input prediction rows | 210 |
| Research-staged prediction rows | 210 |
| Quarantined prediction rows | 0 |
| Prediction rows blocked from evaluation | 210 |
| Rows with unique name candidates for both teams | 150 |
| Rows with unresolved team identity | 60 |
| Provisional competition-hint-aligned fixture candidates | 105 |
| Competition mismatch/crosswalk-gap candidates | 20 |
| No exact kickoff/team candidate | 85 |
| Verified fixture identities | 0 |
| Rows eligible for scoring | 0 |

**Important interpretation:** zero quarantined rows means the adapter can represent the supported composite market labels in research staging. It does not mean the 210 predictions have passed identity, result-source, timestamp or evaluation gates.

All 210 staged rows still lack canonical home and away team IDs. The team-name audit proposes candidates only; it does not write IDs into the prediction ledger. The fixture candidate audit deliberately marks every row `fixture_identity_verified=false` and `eligible_for_scoring=false`.

## Competition and feature-data audit

- Provider competition names in the acquired catalogue: 43.
- Provisional crosswalk candidates requiring review: 25.
- Unmatched provider competition names: 18.
- Approved canonical mappings: 0.
- Canonical registry universe: 27 leagues.
- Intended 44-league universe reconciled to the canonical registry: no.
- Pre-match xG point-in-time provenance verified: no.
- Pre-match odds point-in-time provenance verified: no.
- Historical league standings: still provisional; season formats and official tie-break rules are not fully validated.

The archive contains xG and odds fields, but field presence is not proof those values were available before kickoff. These fields must not be treated as verified pre-match model inputs until source timestamps and snapshots establish point-in-time provenance.

## Root cause and why evaluation cannot finish from this archive alone

The immediate evaluation blocker is not archive parsing: the archive integrity checks pass. The missing link is a **trusted, exact identity chain from each immutable Oracle prediction to the correct historical fixture and result**.

1. The 210 staged prediction rows do not carry canonical home/away team IDs.
2. Team-name normalization improves candidate discovery but cannot prove the competition, season, kickoff and fixture are identical.
3. Competition hints remain provisional and the crosswalk has no approved mappings.
4. A valid evaluation also needs immutable prediction timestamps strictly before kickoff and independently trusted frozen result snapshots with source provenance.
5. The canonical production settlement ledger and scorecard remain empty/header-only in the evidence previously audited. Therefore no defensible production hit rate, Brier score, log loss, calibration result or profitability result is currently available.

A successful workflow, a populated historical-results archive, or a unique name match does not substitute for these controls. No performance metric should be inferred or fabricated.

## Research-only correction now verified

Research PR [#14](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/14) was merged to the **validation/research repository only**. Run #52 on the resulting `main` commit passed all workflow steps, including tests, archive integrity, feature coverage, crosswalk, prediction adapter, team identity audit, fixture candidate audit and artifact upload.

The research changes:
- align conservative team-name normalization and add regression tests;
- explicitly represent the confirmed `HOME_1X_U45` and `AWAY_X2_U45` composite market semantics for research settlement;
- preserve candidate-only and fail-closed evaluation rules.

No changes were made to the private production repository's model logic or probabilities.

## Next actions, in safe order

1. **Produce a reviewable identity/crosswalk decision table** from the existing candidate audit. Keep exact matches, normalized matches, mismatches, ambiguous cases and unmatched names separate; include source evidence and never auto-approve.
2. **Resolve authoritative competition and team identities** using existing provider identifiers and the canonical registry, with explicit review for season and competition. Do not invent mappings from names alone.
3. **Verify prediction provenance**: each prediction needs a stable ID, timezone-aware prediction timestamp before kickoff, original probability, model/version identifiers and an immutable feature/source snapshot reference.
4. **Establish trusted result provenance**: a separately reviewed source allowlist, acquisition manifest and frozen raw result snapshot whose hashes are independently pinned. A hash proves file identity, not provider authenticity.
5. **Run the exact-ID result join only on rows passing every gate.** Publish included/excluded counts and reasons before computing market, league or team metrics.
6. **Keep weekly autonomous prediction/settlement readiness unapproved** until the full prospective capture → exact identity → trusted settlement → scorecard cycle is demonstrated end-to-end.

## Completion decision

The Run #52 research audit milestone is complete. The broader Project Oracle historical validation and autonomous evaluation workflow is **not complete** because the identity and trusted-provenance gates are still blocked by evidence not present in the current audited rows. The overall project estimate remains at the previously recorded 78%; no increase is justified by a successful archive audit alone.

No paid API plan was purchased, no production integration was changed, and no production prediction logic or canonical data was modified.
