# Oracle Selected-50 Noon Readiness Decision Pack — 2026-10-28

**Decision time:** 2026-10-28 08:05 SAST  
**Target deadline:** 2026-10-28 12:00 SAST  
**Repository:** `dtnzv5by8c-ship-it/oracle-validation-learning`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Decision:** **NO-GO for production predictions and betting release** until the mandatory source, identity, fixture and settlement gates pass.

## Executive summary

The research workflows and tests pass, including the offline current-feed identity contract and staging-adapter tests. The remaining blockers are not additional unit-test failures: they require verified data and approved mappings that are not present in the current evidence. Re-running green tests cannot manufacture that evidence.

### Three gates

| Gate | Status | Evidence | Exit condition |
|---|---|---|---|
| 1. Automated validation | PASS | Safety workflow run 40633801353; archive audit 40633801455; dry-run 40633801419; runtime/backtest 40633725121 | Reopen only if relevant code/data changes |
| 2. Current feed freshness | FAIL / UNVERIFIED | Accessible production-branch manifest generated 2026-10-06 07:49:26 UTC, requested through 2026-10-08; no newer authoritative feed manifest/run verified | Approved staging snapshot with timestamp, source cutoff, successful per-date requests, counts and checksum |
| 3. Canonical identity + fixture/settlement readiness | FAIL | Approved provider-season-to-FotMob bridges 0/50; verified fixture joins 0; verified team joins 0 in audited ledger | Reviewed exact-ID/country bridges, exact fixture/team IDs, and official score/status settlement evidence |

## Identity disposition across selected 50

The 50-row crosswalk has **22 candidate matches requiring human review** and **28 with no match in the current 27-league registry**. These are candidate labels/crosswalk states only. They are not 22 approved mappings. Parent competition IDs remain unverified for 50/50, and production eligibility is not granted for any league.

The current-feed collision audit separately found 12/50 groups with a display-label hit, five with ambiguous feed league IDs, 38 with no matching display label, and seven label hits lacking country evidence. The 12 label hits are not verified bridges.

No parent competition ID may be inferred from a season ID, display name, or candidate canonical code. The research allowlist intentionally remains empty until authoritative evidence is reviewed.

## Current feed and safe refresh

The checked-in `data/current_source_manifest.json` on the inspected production branch was generated at `2026-10-06T07:49:26.139704+00:00`; its requested window ended 2026-10-08. This proves that the accessible manifest is stale, but does not prove no newer artifact exists elsewhere or identify why ingestion stopped.

The old ingestion path is unsafe for refresh because it admits competitions by display name rather than approved exact IDs and omits country/category as an identity safeguard. Do not reactivate it as a shortcut. No provider API calls were made in this checkpoint; the previously approved single identity probe is not repeated.

## Data and settlement controls

- 210 staged ledger rows lack home-team IDs; 210 lack away-team IDs.
- Audited fixture candidates: 105 competition-aligned; 20 competition/crosswalk gaps; 85 without an exact kickoff/team candidate. None verified or score-eligible.
- 7,066 non-complete records with numeric 0–0 placeholders remain excluded from settled truth.
- Combo predictor/settlement disagreement for 0–1 total-goal outcomes remains unresolved; Combo probabilities stay masked.
- 25 research runtime fixtures remain blocked by minimum recent home/away history requirements; do not impute missing history.
- Point-in-time xG/odds provenance and calibrated betting edge remain unverified.

## Next actions to the noon checkpoint

1. Stop rerunning unchanged passing workflows. Gate 1 is closed for this code revision.
2. Review the 22 crosswalk candidates against authoritative provider and canonical evidence, one by one. Promote only entries with traceable evidence and human approval; leave others quarantined.
3. Locate the latest approved staging-feed artifact and its run manifest. If none exists, record the observability/source-access blocker; do not run the unsafe name-only ingestion.
4. Once a safe existing snapshot is available, run the offline adapter and verify manifest timestamp, checksums, row counts, and accepted/quarantined reasons.
5. Reconcile exact fixture/team IDs and kickoff, status, score, and settlement sources.
6. Publish the final 50-row matrix with separate archive-data coverage, current-feed freshness, identity, market readiness, and release status. Keep all unresolved rows NO-GO.

## Final governance decision

**Research QA: PASS for cited workflow runs. Production and betting release: NO-GO.**

This is a technical release gate, not a deadline preference. If authoritative mapping evidence or a safe fresh snapshot remains unavailable by 12:00 SAST, report the blocker transparently and keep release disabled. Do not bypass safeguards or mark unknown values as verified.

No production repository files, Oracle V1.6/V1.6.3 logic, probabilities, calibration, thresholds, protected canonical registry, ledgers, or governance were changed. No new provider requests were made.
