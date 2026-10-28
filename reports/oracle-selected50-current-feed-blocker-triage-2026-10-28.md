# Selected-50 Current-Feed Blocker Triage — 2026-10-28

**Decision:** Current-feed release gate remains blocked. This is a research-only diagnosis and makes no provider API calls.

## What the evidence proves

The existing current-feed identity-quarantine audit was built from existing crosswalk and feed-collision snapshots. It found:

| Diagnostic | Result |
|---|---:|
| Selected season IDs in both evidence sources | 50/50 |
| Selected groups with any feed display-label rows | 12/50 |
| Groups with multiple feed league IDs under a display label | 5 |
| Groups where country is retained | 0/50 |
| Groups protected by exact league-ID allowlist | 0/50 |
| Verified provider-season-to-feed bridges | 0/50 |
| Canonical fixture joins verified | 0 |
| Canonical team joins verified | 0 |
| Production-eligible rows | 0 |

Primary blocker classification: 38 groups have no matching current-feed label, 5 have ambiguous labels matching multiple feed league IDs, and 7 have a label hit but no retained country evidence. None of the 12 display-label hits is a verified mapping.

The archive/identity audit is a no-network report based on previously acquired snapshots. It does **not** provide a current timestamped feed refresh, and it cannot prove that the feed ingestion itself has run successfully today.

## Root-cause classification

1. **Verified blocker — identity contract incomplete.** The current-feed snapshot does not retain country or exact league-ID allowlist evidence, and there is no approved bridge from provider season IDs to feed/canonical league IDs. Name-only matching is unsafe and cannot be promoted.
2. **Not yet established — ingestion freshness cause.** The available audited evidence does not identify a current feed manifest timestamp, latest ingestion run ID, source cutoff, or freshness SLA breach record. It would be inaccurate to claim that a scheduler failed, an API failed, or an old file alone is the cause without those records.
3. **Safe refresh path — not established.** The legacy provider ingestion workflows are intentionally disabled because they could write raw data to the protected production repository. Do not reactivate them or use them as a refresh workaround.

## Safe next steps

1. Locate the authoritative current-feed manifest/ingestion-run metadata and record: source, run ID, UTC creation/update time, source cutoff, row count, selected universe, and output destination. If these metadata are absent, record that as an observability gap rather than infer freshness.
2. Trace the manifest to the most recent permitted feed-ingestion workflow and confirm its destination and data classification before any run.
3. If the approved workflow is research-only and uses already-acquired data, run its validation path; do not make provider API calls, spend credits, or write raw data to the protected repository.
4. Add/retain country and exact-ID allowlist fields at the feed boundary in a research-only change; require an explicit, reviewed provider-season-to-canonical bridge before joining.
5. Keep unmatched and ambiguous rows quarantined. Do not use names, season IDs, guessed parent IDs, or a single label hit as canonical identity.
6. After a legitimate refresh and bridge approval, rerun exact kickoff/team fixture joins, official score/status settlement checks, and the Selected-50 runtime QA. Until then, keep production/betting eligibility false.

## Other gates that remain open

- Parent competition IDs verified: 0/50; approved provider-to-canonical bridges: 0/50.
- Prediction ledger adapter: 210 rows lack home-team IDs and 210 lack away-team IDs; verified fixture identities 0; score-eligible rows 0.
- The research runtime has 25 fixtures blocked by missing minimum recent home/away history. Do not impute history.
- Combo predictor and settlement helper disagree on 0–1 total-goal outcomes. Combo probabilities remain masked.
- 7,066 historical non-complete rows with numeric 0–0 remain excluded from settled truth.
- Point-in-time xG/odds provenance and calibrated betting-edge evidence remain unverified.

## Verification links

- [Current-feed identity quarantine report](oracle-50-league-current-feed-identity-quarantine-2026-10-26.md)
- [Identity snapshot reconciliation](oracle-50-league-identity-snapshot-reconciliation-2026-10-26.md)
- [Selected-50 runtime revalidation](oracle-selected50-runtime-revalidation-2026-10-28.md)
- [Selected-50 release-gate review](oracle-selected50-release-gate-review-2026-10-27.md)
- [Disabled legacy Selected-50 ingestion workflow](../.github/workflows/oracle-selected50-footystats-live-ingestion.yml)
- [Disabled legacy full selected-league ingestion workflow](../.github/workflows/footystats-full-selected-league-historical-ingestion.yml)

## Final disposition

**Research evidence and automated tests: PASS for the runs cited in the checkpoint. Current-feed freshness/identity: NOT VERIFIED. Production and betting release: BLOCKED.**

No production model logic, probabilities, calibration, thresholds, protected registry, ledgers, or governance were changed. No provider API calls were made.
