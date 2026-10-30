# Project Oracle — Selected-50 Exact Calendar-Year Coverage & Feature Audit
**Audit date:** 30 October 2026 (UTC)  
**Workflow:** Private Archive QA #58 — [run 41115501513](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41115501513)  
**Artifact:** [13004648723](https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning/actions/runs/41115501513/artifacts/13004648723)  
**Artifact SHA-256:** b10eefaca601782e1083374d7f9836926a953f35f039274806149bac83cd9fc0  
**Code commit:** f2d36fafa05729ae45ccafc5398947bfa30c9ca2  
**Private archive:** research-selected50-footystats-history-40375285207  
**Private archive SHA-256:** 7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f  
**Status:** RESEARCH_ONLY_CALENDAR_YEAR_COVERAGE_COMPLETE

## Executive result
The exact calendar-year audit has now been run directly against the checksum-pinned 200-season private archive. It replaces the 27 October provisional season-overlap matrix, which did not contain exact annual fixture counts.

- 50/50 selected league groups matched by exact country + competition labels.
- 200/200 archive season folders matched: exactly four seasons per selected league group.
- 800 annual rows generated: 50 league groups × 4 calendar years (2024–2027).
- Zero unmatched/missing season folders; zero undated match rows.
- Exact historical provider-row counts are available for all 50 groups in each of 2024, 2025 and 2026 through the audit date.
- 2027 rows are future schedule records only; they are not historical outcomes.

This is exact provider archive row coverage, not canonical Oracle fixture counts or independent settlement truth.

## 1. Annual match-row coverage

| Calendar year | Archived rows | Rows on/before 30 Oct 2026 | Rows after 30 Oct 2026 | League groups with rows |
|---|---:|---:|---:|---:|
| 2024 | 14,761 | 14,761 | 0 | 50/50 |
| 2025 | 15,029 | 15,029 | 0 | 50/50 |
| 2026 | 14,605 | 12,222 | 2,383 | 50/50 |
| 2027 | 4,452 | 0 | 4,452 | 32/50 |
| **Total** | **48,847** | **42,012** | **6,835** | — |

The 2026 calendar-year archive count includes 2,383 fixtures whose kickoff is after the audit date. The 2027 calendar-year count consists entirely of future schedule rows. Do not include those future rows in historical backtests or outcome datasets.

The 42,012 rows on or before the audit date comprise 14,761 in 2024, 15,029 in 2025 and 12,222 in 2026 through 30 October. There were no duplicate provider match IDs within any league/year group in the annual audit. The wider archive QA also found no match IDs duplicated across season folders.

## 2. Provider status and settlement limitations

| Calendar year / period | Complete | Incomplete | Suspended | Canceled | Total |
|---|---:|---:|---:|---:|---:|
| 2024 | 14,749 | 0 | 1 | 11 | 14,761 |
| 2025 | 14,987 | 3 | 3 | 36 | 15,029 |
| 2026 through 30 Oct | 12,045 | 157 | 20 | 0 | 12,222 |
| 2026 after 30 Oct (future) | 0 | 2,371 | 12 | 0 | 2,383 |
| 2027 future schedule | 0 | 4,431 | 21 | 0 | 4,452 |

Historical rows on or before the audit date: 42,012. Provider-complete rows: 41,781. Non-complete rows: 231 (160 incomplete, 24 suspended and 47 canceled).

The complete provider status is a data-status indicator, not independently verified official settlement truth. Keep non-complete rows excluded from outcome scoring; keep complete rows as provider-complete candidates pending the official settlement reconciliation gate.

## 3. Complete-status feature coverage (descriptive, zero-preserving)

All seven audited fields were numeric in every provider-complete row in these annual samples (zero missing/nonnumeric values). Numeric presence is not proof of semantic validity or point-in-time availability. Zero values were retained as observed and not recoded.

| Calendar year | Complete rows | Home prematch xG zeros | Away prematch xG zeros | Total prematch xG zeros | BTTS Yes/No odds zeros | DC 1X zeros | DC X2 zeros |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2024 | 14,749 | 802 (5.44%) | 804 (5.45%) | 716 (4.85%) | 66 (0.45%) | 206 (1.40%) | 205 (1.39%) |
| 2025 | 14,987 | 772 (5.15%) | 774 (5.16%) | 692 (4.62%) | 130 (0.87%) | 515 (3.44%) | 515 (3.44%) |
| 2026 through 30 Oct | 12,045 | 781 (6.48%) | 781 (6.48%) | 693 (5.75%) | 128 (1.06%) | 134 (1.11%) | 134 (1.11%) |

Interpretation:
- Historical annual coverage is materially stronger than the old 27 October matrix suggested: every selected group has provider archive rows in each of 2024, 2025 and 2026 through the audit date.
- The annual numeric fields are populated, but zero-coded prematch xG and odds remain quality exceptions. See the Run #44 xG/odds diagnostics for current-season league-level masks, especially the 11 elevated xG groups and Belgium BTTS/DC anomaly.
- This annual roll-up does not establish per-feature retrieval timestamps, source update timestamps, bookmaker identity, quote timestamps, or the precise pre-kickoff availability of every value.
- These values must not be treated as calibration-ready or betting-grade features until those provenance gates pass.

## 4. Data and identity reconciliation

| Gate | Result |
|---|---|
| Exact selected league groups | 50/50 |
| Exact archive season folders | 200/200 |
| Season folders per selected group | 4/4 |
| League/year output rows | 200 |
| Season/year output rows | 800 |
| Unmatched or missing season folders | 0 |
| Undated match rows | 0 |
| Duplicate provider match IDs in annual group/year buckets | 0 |
| Canonical competition mappings | Not approved |
| Canonical team/fixture joins | Not verified |
| Official settlement truth | Not verified |
| Production eligibility | No |
| Betting eligibility | No |

The identity probe has a separate evidence register for the 50 returned comp_master_id values. Those are provider-returned fields only; their semantics are not approved as Oracle canonical IDs. The existing crosswalk remains 22 candidate mappings requiring human review and 28 unresolved.

## 5. Reproducibility and safeguards
- The workflow verified the private archive SHA-256 before reading it.
- It reused the existing private archive; no FootyStats provider API calls or credits were consumed by this audit.
- Raw provider payloads were not exported to the public repository. The artifact contains sanitized aggregate CSV/JSON outputs.
- The audit does not change production model logic, probabilities, calibration, thresholds, production ledgers or betting eligibility.
- Calendar-year assignment uses each fixture's parsed kickoff date in UTC where the source date is a Unix timestamp.

## 6. Required next work
1. Resolve the provider complete status against independent official outcome/settlement sources for each governed market.
2. Establish feature-level point-in-time provenance for xG, odds and standings; do not infer timestamps from the archive extraction date.
3. Investigate zero-coded xG/odds semantics by league and season; do not impute or recode without provider evidence.
4. Complete canonical competition/team/fixture identity reconciliation.
5. Run chronological held-out validation and calibration only after the above gates are satisfied.
6. Re-run the exact annual audit after any archive refresh and compare counts, status distributions and feature quality against this checkpoint.

**Decision:** Workstream 1 (exact 2024–2026 calendar-year archive coverage for the selected 50) is complete for the pinned archive. Data provenance, canonical identity, official settlement and market-validation workstreams remain open. Research-only; production and betting eligibility remain false.
