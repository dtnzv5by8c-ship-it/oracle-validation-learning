# Oracle 50-League Evidence & Feature Readiness Matrix — 2026-11-06

## Gate result

**RED / NOT READY — but the evidence gate has materially advanced.**

The exact governed **50-league / 182-season / 728-task** roster has now been reconciled from the pinned Selected-50 manifest and the completed private archive checkpoints.

### Acquisition reconciliation

- Governed leagues: **50/50**
- Provider seasons: **182/182**
- Endpoint tasks: **728/728 accounted for**
- Completed endpoint tasks: **648**
- Quarantined HTTP-417 tasks: **80**
- Pending tasks: **0**
- Fully acquired leagues at task level: **44/50**
- Fully blocked leagues: **6/50**
- Acquired provider seasons: **162/182**
- Blocked provider seasons: **20/182**
- Production eligible: **false**
- Betting eligible: **false**

The 80 blocked tasks map exactly to the 20 seasons belonging to:
- Finland Veikkausliiga
- India Indian Super League
- Republic of Ireland Premier Division
- Russia Russian Premier League
- South Korea K League 1
- Venezuela Primera División

No further private acquisition was triggered.

## Historical fixture evidence recovered from existing private artifacts

The existing private artifacts were reconciled read-only; no new provider calls were made.

For the 648 completed endpoint tasks:

- Unique fixture IDs: **49,949**
- Completed/settled-status fixtures: **43,618**
- Completed-status coverage: **87.33%**
- Kickoff timestamp present/valid: **100%**
- Provider fixture/team IDs present: **100%**
- Completed-match score fields valid: **100%**
- 1X2 odds non-zero coverage: **99.74%**
- BTTS odds non-zero coverage: **99.34%**
- O/U 2.5 odds non-zero coverage: **99.85%**
- Prematch-labelled xG values non-zero for both teams: **93.28%**
- Explicit home/away flag: **86.64%**
- Strict chronological 5-match form available for both teams: **92.60%**
- Strict chronological 8-match form available for both teams: **88.23%**
- Strict pre-kickoff H2H prior meeting available: **75.33%**

These are **evidence/availability measurements only**. They are not production eligibility or betting accuracy claims.

### Archive deduplication control

The downloaded private artifacts contain overlapping copies of some payloads from repeated/continued runs. Across raw artifact observations there were 56,407 match rows, resolving to **49,949 unique provider fixture IDs**. The 6,458 repeated observations had no conflicting core fixture identity/score fields.

Therefore the readiness matrix uses **unique fixture IDs**, not duplicated archive observations.

## Feature gate

| Feature | Evidence status | Production admission |
|---|---|---|
| Exact provider fixture/team/league identity | GREEN at provider-ID level | BLOCKED pending canonical Oracle bridge |
| Kickoff chronology | GREEN structurally | BLOCKED pending full historical admission |
| Final result / score | GREEN for completed rows | BLOCKED pending settlement contract admission |
| Recent form 3/5/8 | STRONG coverage | BLOCKED pending full point-in-time admission |
| Home/Away form | PARTIAL — 86.64% explicit orientation | BLOCKED |
| H2H | STRONG research coverage — 75.33% have prior meeting | BLOCKED pending canonical/chronology admission |
| Goals / BTTS / Over markets | GREEN structurally for settled rows | BLOCKED pending admission |
| Fixture-time standings | NOT YET PROVEN | BLOCKED |
| xG values | 93.28% non-zero prematch-labelled | BLOCKED — point-in-time provenance not proven |
| 1X2 / BTTS / O/U odds | >99% structural coverage | BLOCKED — point-in-time provenance not proven |
| Sample size | Available for acquired spine | BLOCKED until feature eligibility is gated |
| Freshness | Retrieval evidence exists | BLOCKED for historical pre-kickoff admission |
| Source/provenance | Strong private source lineage | PARTIAL |
| OMI eligibility | NOT_GRANTED | BLOCKED |
| Visual Intelligence eligibility | NOT_GRANTED | BLOCKED |

## League classification

- **READY: 0**
- **PARTIAL: 44**
- **BLOCKED: 6**

The 44 PARTIAL leagues have complete endpoint-task acquisition and substantial fixture/feature coverage, but cannot be promoted to READY because the remaining governance gates are feature provenance and point-in-time admission, not raw data availability.

The 6 BLOCKED leagues have no admitted historical provider payloads because all 80 associated endpoint tasks are quarantined HTTP-417.

## Major blockers remaining

1. **Fixture-time standings** — historical as-of-kickoff table truth still needs certification.
2. **xG provenance** — the prematch fields are populated, but the provider response does not prove that those values were frozen before kickoff.
3. **Odds provenance** — high structural coverage, but point-in-time capture/effective-time evidence is not yet certified.
4. **Canonical Oracle identity bridge** — provider IDs are exact, but the remaining canonical mapping decisions must remain fail-closed.
5. **Settlement admission** — completed status and scores are present, but the final prediction-to-settlement contract must be applied before backtesting.
6. **Home/away orientation** — 86.64% explicit coverage; the remainder cannot be imputed.
7. **Six HTTP-417 leagues** — remain quarantined and must not be silently promoted.

## OMI / Visual Intelligence decision

**OMI: NOT READY.**

The underlying data is now demonstrably much stronger than the previous metadata-only state, but OMI cannot consume it as production/historical truth until the point-in-time and identity gates above are closed.

**Visual Intelligence: NOT READY for production admission.**

The feature framework can now be populated from the admitted research spine, but production-grade Visual Intelligence must remain fail-closed until the same provenance gates pass.

## Governance

- Oracle V1.6 production logic: **UNCHANGED**
- Oracle probabilities: **UNCHANGED**
- Calibration: **UNCHANGED**
- Thresholds: **UNCHANGED**
- Production ledger: **UNCHANGED**
- Private provider budget: **no new acquisition run**
- Raw provider payloads: **remain private**
- Public branch contains only sanitized evidence/matrix outputs
- Betting eligibility: **NOT_GRANTED**

## Next single target

**POINT-IN-TIME FEATURE ADMISSION GATE.**

Focus only on proving, from the already-acquired private evidence:

**fixture-time standings + xG chronology/provenance + odds chronology/provenance + exact canonical identity + settlement eligibility.**

Do not acquire more data. Do not redesign Oracle. Do not change production logic.

Once this gate is closed, move directly to **OMI admission → Visual Intelligence → historical backtest → risk profiles**.
