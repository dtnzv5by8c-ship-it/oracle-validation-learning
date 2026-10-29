# Project Oracle — Team Form and Fixture Context Uncertainty Audit

**Date:** 2026-10-30  
**Source:** Existing Run #168 artifact, generated 2026-10-29 17:09:30 UTC  
**Scope:** Research-only context analytics; no provider/API calls; no production changes.

## What was executed

A reproducible standard-library Python script was tested and run against the existing runtime artifact. It emits:
- one latest-as-of team/role form profile per team, league and home/away role, with W/D/L counts, raw rates, Wilson 95% intervals and Beta(1,1)-smoothed descriptive rates;
- one fixture-context row per upcoming candidate, with form uncertainty, H2H BTTS sample consistency and explicit data-quality flags;
- a machine-readable summary.

The script's self-tests passed. The locked H2H paired-prediction holdout was not loaded.

## Verified results

| Measure | Result |
|---|---:|
| Fixture candidates in the source report | 436 |
| Rows with raw research predictions | 411 |
| Rows blocked for missing required features | 25 |
| Team/league/role context profiles | 859 |
| Distinct team/league identities in the fixture context | 779 |
| Profiles with 5 observed W/D/L symbols | 833 |
| Profiles with 4 symbols | 21 |
| Profiles with 3 symbols | 5 |
| Fixtures with a recent H2H BTTS rate | 371 |
| Fixtures without a recent H2H BTTS rate | 65 |
| Fixtures with fewer than 3 prior H2H meetings | 144 |

The W/D/L sequence-length distribution is 833/859 (96.97%) at five results, 21 at four, and 5 at three. This is contextual coverage only; it does not prove the feature values are canonical or predictively useful.

## Why the uncertainty matters

For a five-match form sample, the two-sided Wilson 95% interval for a win proportion is:
- 0 wins out of 5: 0.0%–43.45%;
- 5 wins out of 5: 56.55%–100.0%.

Even an apparently perfect 5/5 recent run is therefore highly uncertain as an estimate of a team's underlying rate. Raw form percentages must not be used alone to rank teams or select markets.

The H2H BTTS interval uses the explicit length of the displayed recent H2H sequence and checks that the reported rate is compatible with an integer event count. The interval is approximate context only: historical meetings are not independent samples, and it is not a calibrated probability interval for the model.

## Blocking evidence

All 436 fixture rows currently have:
- unverified canonical fixture joins;
- unverified canonical team joins;
- settlement truth not verified against the production market specification;
- raw, uncalibrated probabilities;
- odds/xG provenance unverified.

In addition, 25 fixtures are blocked for missing required features, and 144 have fewer than three prior H2H meetings. These are data-quality and context flags, not team-performance judgments.

The source runtime was 5.41 hours old at the time of this analysis; the underlying snapshot was retrieved at 11:46 UTC, about 10.77 hours before the analysis checkpoint. Freshness should be rechecked before using these fixtures operationally.

## Decision

**Do not produce team-market rankings or permanent exclusions from this artifact.** The current report does not contain fixture-level, team-attributed chronological out-of-sample predictions with verified settlement outcomes. The locked H2H holdout remains untouched.

## Next action

1. Use a fresh governed snapshot when available and rerun this script.
2. Resolve canonical fixture/team/competition joins and official settlement labels.
3. Obtain a separate team-attributed walk-forward prediction output that is not the locked primary holdout.
4. Then calculate per-team market accuracy, Brier score, log loss, calibration and risk intervals with minimum-sample and shrinkage rules.
5. Keep all outputs research-only until independent validation and formal governance review pass.

**Production model logic and frozen probabilities remain unchanged; production and betting eligibility remain unapproved.**
