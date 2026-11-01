# Project Oracle — Market Intelligence Signal Discovery Run 3 checkpoint

**Inspected branch HEAD at start of run:** `5e30876b83633adae29c761ca167fec3060a7537`  
**Research implementation commit:** `c212a2cfa4651a8bd1f82370e50abcc6fb8a405f`  
**Branch:** `research/oracle-50-league-readiness-audit`  
**Run date:** 1 November 2026

## Work completed
- Recovered the locally available Run64 FootyStats audit archive from the user's Library; no provider API calls or credits used.
- Rebuilt a strict event-time panel of 23,328 settled matches across the 31 selected groups available locally; 15,003 target fixtures in 20 Mar 2025–20 Sep 2026.
- Reproduced the Run 8 test fold sizes exactly: 4,876 / 5,828 / 4,299. H2H N≥5 count 1,048; last-20 vs prior-20 regime coverage 8,378.
- Enforced prior kickoff < target kickoff, excluded same-kickoff matches, preserved observed N≥5 for both teams and role splits, and used no pseudo-counts.
- Independent brute-force audit: 250 fixtures, zero history-count discrepancies. Rebuilt last-five PPG/GF/GA matched the available chronological feature file on 21,508 non-null comparisons.
- Ran expanding-fold nested logistic ablations for BTTS, DC_HOME and DC_AWAY; computed Brier, log loss, fold-weighted AUC, ECE10, reliability bins, paired league-cluster bootstrap CIs and a joint 252-test BH/BY correction.
- Added research-only eligibility/interaction contract and six tests. All six tests passed locally; derived-bundle validator passed.

## Findings
- **Venue-role features are the strongest new candidate.** On the same 13,682-fixture cohort, adding home-role/away-role features to core form improves DC_HOME and DC_AWAY Brier and log loss in all three folds. Both improvements survive global BY correction (q_BY=0.035985). Fold-weighted AUC improves in all folds but does not survive BY (q_BY=0.070635). ECE improvement is inconclusive.
- The two proposed interactions add no positive incremental value. Home GF × away GA slightly worsens DC_HOME/DC_AWAY; selected adverse core DC_HOME Brier/log-loss effects survive the joint BY correction (q_BY=0.035985).
- Momentum regime features add no reliable value; only folds 2 and 3 have adequate training history.
- H2H N≥5 coverage is only 1,048 fixtures; fold 1 has 12, so a defensible three-fold H2H model is not supported.
- Goal-environment association with BTTS is small and does not beat the league-only baseline.
- No scoreline model was fitted in this run.

## Blockers and limitations
- Original Run 8 v18 workbook and 29.2 MB companion bundle are not in the Library or accessible repository tree. Their committed manifests record checksums, but the binary assets were not retrieved.
- The pinned full Selected-50 archive release binary was not retrieved. Run64 is a different, smaller audit extract covering 31/50 selected groups; the 19 missing groups remain unavailable locally. Population counts match Run 8, but exact fixture-ID equivalence to its missing workbook cannot be certified.
- Local reconstructed core-form coverage (14,242) and role-based venue coverage (13,682) differ from Run 8 published counts (14,105 and 12,268). The original workbook is required to reconcile these differences.
- The source lacks a `no_home_away` flag; venue variables are home-role/away-role proxies, not verified actual-venue-only histories.
- Source publication/capture timestamps are unavailable. Event-time chronology is verified, source availability at kickoff is not.
- No row-level frozen Oracle V1.6 probabilities exist for the same 15,003-fixture cohort in the accessible archive. No paired V1.6 comparison is claimed.
- xG and provisional standings remain quarantined.

## Next steps
1. Recover the original Run 8 workbook/companion bundle or a verified row-level extract; reconcile the feature-coverage differences.
2. Obtain the immutable fixture-level Oracle V1.6 probability ledger for paired benchmarking.
3. Obtain verified venue and source-capture provenance before further promotion testing.
4. Repeat the venue ablation on an independent historical window and league holdout.
5. Build a hierarchical Poisson/Dixon–Coles scoreline model with chronological calibration.

## Governance
Research-only. Oracle V1.6 production logic, probabilities, canonical ledgers and production workflows were not changed. `production_eligible=false`; `betting_eligible=false`.
Detailed outputs: `ORACLE_MARKET_INTELLIGENCE_SIGNAL_DISCOVERY_RUN3_2026-11-01.zip` in the conversation attachments.
