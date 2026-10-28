# Selected-50 Feature-Blocker Row Audit
**28 October 2026 — 20:21 SAST**

## Scope and source integrity

This is an independent, offline audit of the already-published Research Runtime #159 artifact. No provider API was called and no model output was regenerated.

- Runtime: [#159](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40725720521)
- Artifact: [#12831029975](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/40725720521/artifacts/12831029975)
- Artifact ZIP SHA-256: `0109f15c570aef954f4354ce84294d1c52962e73f29dc6e90bb022fc87c9335e`
- Source prediction CSV SHA-256: `3f26f220c948de0274646e567e0b2a19977cbe648fb31995515b502eedc59851`

The independent audit asserted fixture uniqueness, block counts, training support, per-side feature/history consistency, the six shared derived-feature gaps, and Combo masking. All assertions passed against the downloaded artifact.

## Findings

| Check | Result |
|---|---:|
| Runtime fixture rows | 460 |
| Unique source fixture IDs | 460 |
| Fixtures blocked by missing required features | **25** |
| Blocked fixtures with unavailable training support | **0** |
| Fixtures with supported raw research-market outputs | 435 |
| Production-eligible fixtures | **0** |
| Nonblank Combo Home probabilities | **0** |
| Nonblank Combo Away probabilities | **0** |
| Side-form feature gaps despite five or more qualifying matches | **0** |

### Venue-specific history

The missing side-form fields are consistent with the recorded venue-specific history counts:

| Missing side-form group | Blocked side cases | History count 3 | History count 4 |
|---|---:|---:|---:|
| Home side | 16 | 2 | 14 |
| Away side | 10 | 3 | 7 |

One fixture appears in both groups, so there are 25 unique blocked fixtures across 26 affected team-side histories.

Each affected side is missing the seven corresponding form features: goals for, goals against, BTTS, failed-to-score, clean sheets, shots and shots on target. No side with a reported count of five or more has its seven side-form fields missing.

### Dependent features

All 25 blocked fixtures are missing each of these six derived features:

- `pair_btts_mean`
- `pair_fts_mean`
- `pair_cs_mean`
- `score_environment`
- `shot_environment`
- `score_gap5`

These are downstream of unavailable side-form inputs in the current output. This audit does not assert that the raw historical records are absent from every archive source; it establishes only that the runtime report lacks the required feature values and reports fewer than five qualifying matches for the affected side.

## Decision

The evidence does **not** support relaxing the five-match venue-specific minimum or imputing values. Training data is available for all five research markets, so this is a feature-history support issue rather than a training-support failure.

Next useful diagnostic: for each affected team-side, trace the exact qualifying historical fixture IDs already present in the private archive and record which status, kickoff cutoff, team-ID mapping or venue-orientation rule excluded the missing fifth match. Do this offline from existing archive evidence. If no valid fifth match exists before kickoff, keep the fixture blocked.

Combo remains blocked: predictor and settlement-helper semantics still disagree. The artifact confirms both Combo probability columns are blank across all 460 rows. This report does not establish official settlement truth, canonical joins, calibrated probabilities, betting edge, or production readiness.

No provider calls, private Actions, production writes, or changes to Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, registry, ledgers or governance were made.
