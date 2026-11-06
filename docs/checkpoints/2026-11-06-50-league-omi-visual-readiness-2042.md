# Oracle 50-League OMI / Visual Intelligence Readiness Checkpoint

**As-of:** 2026-11-06 20:42 SAST
**Branch:** `research/oracle-50-league-readiness-audit`
**Head:** `198b9476e7e3fd96135da3b9bec095e04076e472`
**Scope:** governed 50-league universe only. Research/reporting validation only.

## Upstream admission rule

The acquisition queue is treated as exhausted for downstream research. Only upstream evidence with deterministic READY, provenance, chronology, freshness and settlement gates may be consumed. Acquisition success alone is not feature readiness.

## Current evidence

- Governed acquisition plan: 50 leagues, 182 provider seasons, 728 endpoint tasks.
- Latest recorded validation coverage checkpoint: 648/728 tasks.
- Provider-417 quarantine/blocked-task registry is explicitly recorded; blocked tasks are not promoted.
- The public Master OMI exact-ID join workflow is restored.
- Latest public contract test run on this branch: run 1215, conclusion SUCCESS, head `198b9476e7e3fd96135da3b9bec095e04076e472`.
- H2H reporting integration has an exact-ID contract and rejects missing/blank/duplicate IDs.
- H2H history remains review-gated: unresolved mappings and no-history cases are kept distinct; fuzzy matching and cross-league reassignment are prohibited.
- Canonical settlement evidence for production accuracy remains insufficient: the historical H2H status records the canonical settlement ledger as header-only, while challenger/shadow results are research-only.

## Downstream readiness matrix

| Feature family | Status | Admission rule / blocker |
|---|---|---|
| Fixture identity | READY when exact canonical IDs and source identity agree | Exact-ID join; no fuzzy matching |
| Chronology | READY only with pre-kickoff cutoff evidence | Reject leakage/future rows |
| Recent form | PARTIAL until required windows are present and timestamp-valid | No fabricated windows |
| Home/away splits | PARTIAL until role-specific history meets window/sample gate | Preserve home/away role |
| H2H | PARTIAL | Exact history only; unresolved mappings/no-history remain separate |
| Goals for/against | PARTIAL pending complete validated match spine | No inferred values |
| Total-goal distributions | PARTIAL pending validated historical sample | Derived only from admitted matches |
| BTTS | PARTIAL pending validated goals/sample | No proxy substitution |
| Over 1.5/2.5/3.5 | PARTIAL pending validated goals/sample | No fabricated labels |
| Clean sheets | PARTIAL pending settled score history | Derived only |
| Failed-to-score | PARTIAL pending settled score history | Derived only |
| xG for/against | BLOCKED where provider xG evidence is absent/unvalidated | No synthetic xG |
| Standings/strength | PARTIAL pending exact league/season chronology | No cross-season substitution |
| Timestamped odds | BLOCKED unless timestamped pre-kickoff odds are verified | No closing-odds substitution |
| Sample size | READY as a diagnostic once source rows are admitted | Must be explicit per feature |
| Recency | READY as a diagnostic once timestamps are valid | Must be calculated from source dates |
| Confidence | GATED | Must reflect validated feature coverage |
| Data-quality/risk flags | READY as a reporting layer | Must expose missingness/provenance |
| Actual results | PARTIAL | Only exact settled fixtures admitted |
| Backtesting | BLOCKED for production claims until immutable prediction→settlement pairs exist | Research-only evidence remains labelled |
| Team risk | PARTIAL | Requires sufficient repeated pre-kickoff samples |
| League risk | PARTIAL | Requires sufficient validated samples |

## Highest-value blockers

1. **Validated feature-ready upstream batch coverage**: 648/728 is a recorded validation-coverage checkpoint, but blocked/provider-417 tasks must remain excluded and the remaining 80 tasks must not be silently treated as READY.
2. **Feature completeness**: identity/chronology are structurally supported; form, splits, goals, derived markets, xG, standings and odds require field-level admission evidence.
3. **H2H completeness**: exact-ID reporting works, but unresolved mappings/no-history cases remain separate and H2H predictive value is not production-proven.
4. **Settlement provenance**: production accuracy/backtesting requires immutable pre-kickoff prediction timestamps/probabilities linked to exact settled outcomes.
5. **Odds provenance**: timestamped pre-kickoff odds are required; no unverified odds substitution.

## Minimum evidence to resolve blockers

For each admitted fixture/team-season feature:
- canonical fixture ID
- provider league/season identity
- exact home/away team identity
- kickoff timestamp and source timestamp
- pre-kickoff feature cutoff
- source provenance and immutable batch reference
- required window/sample count
- raw goals/score evidence for derived goal markets
- xG source evidence when xG is used
- exact standings snapshot for the applicable league/season
- timestamped odds captured before kickoff when odds are requested
- settlement result only after fixture completion
- deterministic READY/PARTIAL/BLOCKED classification

## Production protection

No Oracle V1.6 production probability, threshold, decision rule, calibration or governance has been changed. This checkpoint is research/reporting only. Production and betting admission remain fail-closed.
