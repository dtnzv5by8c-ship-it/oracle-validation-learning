# CMOI Validation Closure — 2026-11-21

## Status
RESEARCH_ONLY / NOT PROMOTED / FAIL-CLOSED

## Scope
CMOI remains separate from Oracle V1.6. The Master OMI A:ET contract is unchanged. CMOI outputs are append-only and limited to:
- CMOI_MATCH_OUTCOME
- CMOI_CONFIDENCE

## Canonical workbook validation
Source: Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_CORRECTED.xlsx
Market Intelligence rows: 754
Market Intelligence columns before CMOI: 264
CMOI columns appended: 265–266

## Chronological OOS validation
The canonical workbook contains 275 exact Fixture ID joins to Actual Results, with:
- HOME: 118
- DRAW: 68
- AWAY: 89

A chronological 70/30 split produced 83 OOS fixtures.

Candidate results:
- H2H + Last-5 form + venue context: accuracy 33.73%, log loss 1.1790
- H2H + form + venue context: accuracy 32.53%, log loss 1.1697
- form + strength: accuracy 32.53%, log loss 1.1823
- full feature model: accuracy 31.33%, log loss 1.1976
- form-only: accuracy 28.92%, log loss 1.1717

The chronological training selection process did not produce a stable test-set improvement sufficient for promotion. The best accuracy remains below the OOS majority-class benchmark of 39.76%.

## Last-3 vs Last-5
The canonical Last-3 PPG dataset contains 70 rows for the 13–17 Nov historical report, but the current canonical Actual Results sheet does not contain corresponding 13–17 Nov settlements. Therefore a clean Last-3-vs-Last-5 OOS comparison cannot be certified from this source without introducing an unsupported settlement join. This gate is explicitly left OPEN rather than guessed.

## Prototype evidence
The earlier CMOI prototype produced 39.24% accuracy on 79 OOS fixtures. This result is retained as research evidence only and is not treated as a production certification because it is not stable across the broader canonical validation.

## Release decision
CMOI is LOCKED INTO THE MASTER TEMPLATE AS A RESEARCH SCHEMA, but NOT formula-ready and NOT betting-production eligible.

Promotion requires:
1. broader chronological OOS settlement coverage;
2. clean Last-3 vs Last-5 comparison;
3. probability calibration;
4. exact identity and chronology QA;
5. Formula Input Release Gate = PASS;
6. evidence that CMOI materially improves over an appropriate benchmark out of sample.

No Oracle V1.6 logic is changed by this closure.
