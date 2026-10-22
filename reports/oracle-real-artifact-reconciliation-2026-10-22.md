# Real Oracle Artifact Reconciliation — 22 October 2026

## Scope and provenance

- Classification: research-only audit; not a production approval.
- GitHub Actions run: **39772347617** (Run #107).
- Source commit: `f86eaf2586e2d2dc7df73de773a0214116f231bb`.
- Artifact: `oracle-fixture-level-predictions` (artifact ID `12425136901`, SHA-256 `5de8e3773934e2d53aa6464df31c03ee8d7a47bda98ad19ed39e590d28cb3299`).
- Schedule: `oracle/data/fixtures/oracle_upcoming_fixtures.csv`.
- Prediction output: `oracle/research/four_model/outputs/four_model_live_predictions.csv`.
- Prediction manifest generated: `2026-10-22T12:17:13.257607+00:00`.

## Result: PARTIAL — 10 scheduled fixtures excluded

The artifact contains 244 scheduled fixtures and 5,148 prediction rows for 234 fixtures. The output manifest independently records 10 fixtures excluded due to missing pre-match team state. Comparing the schedule to output using normalized date + home-team + away-team identity produced 234 unique matches, zero ambiguous matches, and zero prediction identities without a schedule match.

| Check | Result |
|---|---:|
| Scheduled fixtures | 244 |
| Fixtures with prediction output | 234 |
| Fixtures excluded | 10 |
| Fixture coverage | 95.9016% |
| Prediction rows | 5,148 |
| Governed markets present | 22 of 22 |
| Rows per predicted fixture | 22 |
| Duplicate fixture/market rows | 0 |
| Probabilities outside [0, 1] or non-numeric | 0 |
| Fixtures with incomplete market matrix among emitted fixtures | 0 |
| Ambiguous schedule-to-output identity joins | 0 |

Every one of the 22 governed markets appears exactly 234 times. All 5,148 rows have status `PREDICTED`; no duplicate fixture/market pairs or invalid numeric probabilities were found among emitted rows.

## The 10 missing fixture outputs

The following fixtures are present in the schedule but absent from prediction rows. The source prediction manifest marks each `MISSING_PREMATCH_TEAM_STATE`; these are not silent omissions.

| League | Fixture | Missing state |
|---|---|---|
| Ligue 2 | Pau FC vs Grenoble | Home-role history |
| Eerste Divisie | Almere City vs Roda | Home- and away-role history |
| Eerste Divisie | Jong AZ vs Helmond | Home- and away-role history |
| Eerste Divisie | Oss vs Jong Ajax | Home-role history |
| Belgian Pro League | Westerlo vs Beveren | Away-role history |
| Czech First League | Brno vs Bohemians 1905 | Home-role history |
| Eerste Divisie | Dordrecht vs Venlo | Home- and away-role history |
| Ekstraklasa | Wisla vs Rakow | Home- and away-role history |
| 2. Bundesliga | Braunschweig vs Hannover 96 | Home-role history |
| Eredivisie | PSV vs Feyenoord | Home-role history |

The research reconciliation contract was applied against all 244 expected fixture identities and all 22 expected markets. It correctly returns **FAIL/PARTIAL rather than PASS** because the 10 scheduled fixtures have no prediction output. This is the intended fail-closed behavior; it does not mean the 5,148 emitted prediction rows are individually malformed.

## What this proves — and what it does not

**Verified:** the existing run's emitted prediction matrix is structurally complete for the 234 fixtures it predicted, and the 10 omissions align with the manifest's explicit missing-state exclusions.

**Not verified:** live per-league failure isolation; historical predictive accuracy; correctness of probabilities; or full coverage of all scheduled fixtures. This artifact does not establish those claims.

## Next engineering action

Fix the root cause for missing pre-match team-state coverage through a separately reviewed data/alias/state-readiness investigation. Do not fabricate team history or use post-kickoff data. Add a regression test for the 10 exclusion patterns and preserve explicit exclusion reporting. Only after the runner's actual supported input/output interface is confirmed should per-league orchestration be integrated.

No model probabilities, weights, thresholds, calibration, selection logic, or production code were changed for this audit. PR #20 remains draft and unmerged.
