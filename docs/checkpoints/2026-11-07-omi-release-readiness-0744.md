# Oracle OMI / Visual Intelligence Release Readiness — 2026-11-07

## Baseline and control
- Branch: `research/oracle-50-league-readiness-audit`
- Selected-50 Market Intelligence Repair #360 remains the completed downstream baseline; it was not rerun.
- Artifact inspected: 717 runtime fixtures, 717/717 exact archive joins, 0 unmatched/quarantined joins, 0 schedule discordance rows.
- Archive index: 59,049 rows; 51,983 exact completed H2H meetings retained; zero duplicate/conflicting identity rows in the archive QA.
- Provider/API calls for the inspected OMI artifact: 0.
- Oracle V1.6 production logic, probabilities, thresholds, calibration and governance: unchanged.
- production_eligible: false
- betting_eligible: false

## Consolidated readiness matrix
The per-league matrix is published at:
`reports/oracle-omi-release-readiness-matrix-2026-11-07.csv`

It covers all 50 governed selected leagues and 24 readiness dimensions. The matrix is derived only from the successful #360 artifact and existing governed evidence; no unavailable value is inferred.

### Scope
- 50 governed leagues
- 45 leagues represented by 717 fixtures in the report horizon
- 5 leagues have no fixture rows in the horizon and are marked UNVERIFIED rather than READY:
  - Republic of Ireland Premier Division
  - South Korea K League 1
  - Uruguay Primera División
  - Canada Canadian Premier League
  - South Africa Premier Soccer League

## Feature-family results
- Fixture identity: READY for all 717 represented fixtures; exact archive join 717/717.
- Chronology: READY for the represented artifact; history cutoff is strictly before each fixture kickoff and schedule reconciliation passed.
- Recent overall form: 1,398/1,434 team-side slots have full five-match history = 97.49%; 43 active leagues are fully covered, 2 are insufficient-sample, 5 are unverified because no fixtures exist.
- Home/away venue form: 836/1,434 team-side slots have full five-match venue history = 58.30%; 15 active leagues READY, 19 PARTIAL, 11 INSUFFICIENT SAMPLE, 5 UNVERIFIED.
- Exact H2H: 604/717 fixtures have prior exact H2H history = 84.24%; 21 active leagues have H2H on every fixture, 24 are PARTIAL, 5 have no current fixtures. No H2H is inferred.
- Goal-rate / experimental goal evidence: 699/717 = 97.49%; 43 active leagues READY and 2 INSUFFICIENT SAMPLE.
- BTTS: 678/717 = 94.56%; 31 active leagues READY and 14 PARTIAL.
- Over 1.5 / Over 2.5 research probabilities: 699/717 = 97.49%; represented as PARTIAL where the 18 missing goal-research rows remain unavailable.
- Over 3.5: BLOCKED; no governed admissible evidence in the inspected baseline.
- Clean-sheet and failed-to-score historical rates: present for all 717 represented fixtures; these remain research features until the immutable prediction/settlement gate closes.
- Standings/league position: present for all 717 represented fixtures.
- xG: numeric home/away/total xG exists for 717/717, but verified capture timestamps are 0/717. xG therefore remains BLOCKED for production.
- Odds: no admissible timestamped bookmaker/market provenance is present in the OMI baseline; BLOCKED.
- Sample size: available as a diagnostic, but 18 runtime rows lack the goal-research sample/rate inputs; those rows remain unavailable for those features.
- Recency: UNVERIFIED for production because the current-feed freshness gate is not closed by this historical-only artifact.
- Confidence: UNVERIFIED for production; no immutable production confidence/settlement cohort exists.
- Risk: home/away evidence-risk and rationales are populated for all 717 represented fixtures; READY as a diagnostic only.
- Actual results: all 717 rows are `NOT_RETRIEVED_NO_CREDIT_APPROVAL`; no settlement truth was promoted.
- Leakage-safe backtesting: chronological research walk-forward evidence exists, but no immutable production prediction → feature snapshot → verified settlement chain exists.
- Production/betting: BLOCKED.

## Runtime feature blockers
The inspected runtime audit records:
- 39 blocked fixture rows
- 40 blocked team-side histories
- 22 home-side histories below five prior matches
- 18 away-side histories below five prior matches
- missing required feature counts include BTTS, clean sheets, failed-to-score, GF/GA, shots/SOT, score environment, score gap and shot environment for those blocked team sides.

The 14 affected active leagues are: Ligue 1, Ekstraklasa, Premier League, Pro League, Ukrainian Premier League, Bundesliga, 2. Bundesliga, LigaPro, Süper Lig, Segunda División, Super League (Greece), Serie B, Professional League (Saudi Arabia), Indian Super League.

## Production probability / fixture reconciliation
The #360 OMI artifact contains research market outputs, but it does not establish an admissible canonical production probability ledger joined to verified settlement truth. The canonical production settlement ledger remains header-only in the governed evidence state. Therefore:
- fixture identity is verified for the #360 research artifact;
- production probability reconciliation is UNVERIFIED;
- actual-result reconciliation is BLOCKED;
- no production probability string is replaced, recalculated or inferred.

## Exact remaining release gates
1. Canonical Oracle production probability → fixture bridge.
2. Immutable pre-kickoff feature snapshot for every admitted prediction.
3. Point-in-time xG capture/revision provenance.
4. Timestamped bookmaker/market odds provenance.
5. Verified official settlement ledger.
6. Immutable prediction → feature snapshot → settlement linkage.
7. Feature/market minimum sample gates, including blocked team-side histories.
8. Current-feed freshness/recency gate.
9. Permanent quarantine of the 80 HTTP-417 upstream tasks and all other unvalidated evidence.

## Shortest safe path
No acquisition is required for this OMI milestone. The shortest safe path is:
1. consume the canonical prediction/evidence output when its immutable bridge becomes available;
2. join it to the already-validated #360 fixture identity;
3. admit only rows passing chronology + provenance + sample gates;
4. settle only against independently verified final results;
5. calculate league/market confidence and risk performance only on the resulting immutable cohort;
6. promote production/betting eligibility only after every required gate passes.

## Governance
This checkpoint is research/reporting-only. It does not modify Oracle V1.6 logic, probabilities, thresholds, calibration or governance. No quarantined data, future/unsettled data, inferred H2H or fabricated provenance is admitted.
