# CMOI — Composite Match Outcome Intelligence Specification
Date: 2026-11-21
Status: RESEARCH / NOT PROMOTED

## User-locked requirements
- Separate from Oracle V1.6. No production-model logic changes.
- Append only after the current Market Intelligence contract; never alter A:ET.
- Visible output is exactly two Market Intelligence columns:
  1. CMOI_MATCH_OUTCOME = HOME / DRAW / AWAY
  2. CMOI_CONFIDENCE = calibrated probability of the selected outcome
- Venue-aware H2H is required.
- H2H uses the most recent five meetings as the initial candidate window, with heavy recency weighting. Last-3 vs Last-5 must be objectively backtested; no assumption of superiority.
- Current form uses both overall and venue-specific form.
- Last-3 and Last-5 PPG are research inputs where available, with strict pre-kickoff chronology.
- Team strength, attack/defence, league position, home/away context and goal environment may contribute where point-in-time eligible.
- Draw is the fallback outcome when the evidence does not establish a sufficiently clear Home/Away edge.
- Use the strongest empirically validated probability methodology; do not label a probability as historical accuracy.
- Historical accuracy/calibration must be established OOS before production promotion.
- No silent imputation of missing evidence; unavailable evidence reduces eligibility/evidence quality.

## H2H design
- Overall H2H and same-venue H2H are both evaluated.
- Same-venue H2H receives higher influence than non-venue H2H.
- Meeting weights decay with age; newest meeting receives the greatest weight.
- H2H must be evaluated from the current fixture's home-team perspective.
- Identity matching is exact/normalized and provenance-preserving; no silent fuzzy matching.

## Candidate signal families
1. H2H overall recency-weighted
2. H2H same-venue recency-weighted
3. Overall Last-3 / Last-5 form
4. Home-at-home / Away-away form
5. Overall PPG and venue PPG
6. GF/M and GA/M
7. Attack and defence indices
8. LTSS V1.1 / relative team strength where eligible
9. League position
10. Home advantage
11. Goal environment / approved pre-match goal signals
12. Other approved pre-match intelligence only where point-in-time provenance is proven

## Validation
- Chronological OOS validation only.
- No post-match or same-time leakage.
- Compare Last-3 vs Last-5 H2H objectively.
- Metrics: accuracy, multiclass log loss, Brier score, calibration, confidence-band accuracy, class-specific accuracy and sample size.
- A candidate is not promoted merely because it has higher raw accuracy on one small sample.
- Promotion requires stable OOS evidence and the permanent Master OMI Formula Input Release Gate.

## Current prototype evidence
Accessible historical workbook contains 316 settled fixtures suitable for this initial research test.
Initial chronological test work found the 5-meeting H2H window preferable to 3 meetings in the tested specification, but the sample is too small to declare production superiority.
A 5-H2H model with a conservative Draw fallback reached 39.2% accuracy on the final 25% OOS slice in this prototype. This is research evidence only and is not a production accuracy claim.
Therefore CMOI remains RESEARCH_ONLY until a broader historical OOS validation is completed.

## Governance
- CMOI must remain separate from Oracle V1.6 unless separately validated and explicitly promoted.
- Market Intelligence A:ET remains immutable.
- All CMOI numeric probabilities must be native Excel numeric values.
- Missing/unavailable evidence is never encoded as zero.
- Every release must pass identity, chronology, provenance, numeric-type, leakage, actual-reconciliation and formula-input QA.
