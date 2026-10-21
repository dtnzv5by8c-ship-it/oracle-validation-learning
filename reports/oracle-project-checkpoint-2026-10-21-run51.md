# Project Oracle research checkpoint — 21 October 2026

## Status

Research-only validation is progressing. Production readiness remains **NOT GRANTED**. No production prediction logic, probabilities, thresholds, calibration, model version, or canonical league registry was changed.

## Verified workflow evidence

### Run #48 — baseline
- Workflow run: [39656048444](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39656048444)
- Conclusion: `success`
- Commit: `197c33a9e14a57a93af9f50195a88f25dc4ec4f2`
- Job: `archive-feature-audit`, completed successfully.
- Artifact: `oracle-footystats-archive-feature-audit`
- Artifact SHA-256: `533725690dde6111c4d87084edae9d3da29bfe467533b02c4526de4a2f354add`
- Artifact ID: `12370903255`

### Run #50 — team-name normalization correction
- Workflow run: [39657422914](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39657422914)
- Conclusion: `success`
- Commit: `4e96164e7cfe1d6ce47e6a524c48341aed10154e`
- Artifact SHA-256: `292ac860e40adf7a384bf8721e66aba53930965290f022ca62e236f6296051e2`
- Team identity improved from 84 to 90 rows with both names uniquely matched in the 126-row staged sample; unresolved rows fell from 42 to 36. Fixture identities verified remained 0.

### Run #51 — composite-market settlement and full archive audit
- Workflow run: [39657795166](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/39657795166)
- Conclusion: `success`
- Commit: `d13c4a9f9e01617e93b9a86dc2825c549a801418`
- Artifact ID: `12371974107`
- Artifact SHA-256: `91be78bf7d04f569477c80c7ad5c3c211773acd4692da90fad4a3d0da13f92be`
- Full workflow steps completed, including tests, archive feature build, integrity audit, standings reconstruction, coverage matrix, competition crosswalk, prediction adapter, team identity audit, fixture candidate audit, and artifact upload.

## Run #51 findings

| Measure | Result |
|---|---:|
| Archive match records | 35,819 |
| Archive season groups | 126 |
| Archive parse errors | 0 |
| Rows with parseable kickoff | 35,819 |
| Rows with score and settled status | 28,491 |
| Input prediction rows | 210 |
| Research-staged rows | 210 |
| Quarantined rows | 0 |
| Rows blocked from evaluation by missing home/away team IDs | 210 |
| Rows where both team names have unique name candidates | 150 |
| Rows with unresolved team identity | 60 |
| Provisional competition-hint-aligned fixture candidates | 105 |
| Competition mismatch/crosswalk-gap candidates | 20 |
| No exact kickoff/team candidate | 85 |
| Verified fixture identities | 0 |
| Eligible-for-scoring rows | 0 |

The zero quarantined rows reflect that the two composite market labels are now structurally understood and research-staged; this is not evidence that any prediction is eligible for evaluation. All 210 rows remain blocked by missing canonical home and away team IDs.

## Code correction and settlement semantics

The research-only team identity normalizer now strips a conservative set of leading club prefixes (including HNK, NK, FK, SK and AFC) and common FC/AFC/CF/SC suffixes. Regression tests preserve the rule that normalized name matches are candidates, not verified identities.

The composite market definitions were checked against existing Oracle truth-building code:
- `HOME_1X_U45`: home win or draw AND total goals no greater than four.
- `AWAY_X2_U45`: away win or draw AND total goals no greater than four.

The research adapter maps these to an explicit `COMPOSITE` market and preserves the original composite selection. Settlement logic and tests cover draws, 0–0, home/away outcomes, and four-versus-five-goal boundaries. These changes are in draft PR [#14](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/pull/14), not merged to main or production.

## Outstanding blockers

1. **Canonical team identity:** all 210 staged rows lack canonical home and away team IDs. Name matching alone cannot fill these IDs safely.
2. **Fixture identity:** no row is verified. Candidate matching must also establish competition, season, kickoff and unique fixture identity.
3. **Competition mapping:** the current provisional crosswalk has 43 provider competition names, 25 candidate mappings requiring review, and 18 unmatched. The intended 44-league universe is not reconciled. No mappings are approved.
4. **Trusted historical results:** the result-source trust policy requires an independently reviewed allowlist, acquisition evidence and frozen raw result snapshots. Synthetic test fixtures are not evidence of genuine historical results.
5. **Point-in-time feature provenance:** xG and odds fields are present, but their availability before kickoff is unverified. They cannot yet be treated as valid historical pre-match features.
6. **Historical evaluation:** no verified prediction-to-result join exists; therefore no current hit rate, Brier score, log loss, calibration or profitability claim is supported.
7. **Autonomous production readiness:** not granted. Archive workflow success does not establish a safe weekly prediction-to-settlement workflow.

## Next safe actions

1. Review Run #51's artifact and the draft PR #14 checks before any merge decision.
2. Build a reviewable team mapping report constrained by approved competition and season, preserving unresolved/ambiguous records.
3. Reconcile the provisional competition crosswalk against the canonical registry using explicit human-review states; do not auto-approve mappings.
4. Establish a separately pinned, independently reviewed result-source allowlist and acquire a genuine frozen result snapshot with provenance.
5. Run the exact-ID verified evaluation join only after fixture identities, timestamps, source provenance and settlement rules pass.
6. Report coverage and rejection reasons before computing metrics. Keep all changes research-only until separately approved.

## Cost and governance

Run #51's workflow uses the previously acquired archive and provider catalogue; the artifact indicates zero provider API calls in the archive audit summary. No paid plan was purchased and no production integration or provider was changed.
