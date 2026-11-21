# Master OMI Permanent Formula Input Release Gate — Run 11 Corrected

**STATUS: FAIL-CLOSED**

Canonical A:ET baseline SHA-256: `9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e`
Corrected candidate SHA-256: `f9b6e030dbe4b9eb38da785e9bc5effcf5331395e13f841102621e3bc3516fed`

A:ET value differences: **0**. Nonblank type differences: **1,269** (float/integer serialization only). No coercion performed.

Formula QA: **387 fixtures; 0 READY; 387 BLOCKED; 0 BACKTEST_READY; 387 RELEASE FAIL.**

Remaining blockers: native numeric-type gate, missing explicit V2.1.1 certification marker, 169 sub-100% coverage fixtures, 38 kickoff/date review fixtures, 15 implausible goal-environment fixtures, and 754/754 xG rows without verified capture timestamps.

The generic identity-review status defect was corrected because exact fixture identity is PASS for 387/387 and FootyStats joins are exact. Genuine kickoff/date defects remain separate.

Missing values are never zero-filled or estimated. Oracle V1.6 and A:ET values remain unchanged.