# Master OMI Formula Gate — Automation Run 11

Status: FAIL-CLOSED

Canonical V2.1.1 baseline SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

Current candidate source SHA-256: eb6121d128027716867ca042c1dd60ac3e9d065fe8936d11674f4f1d25801021

A:ET value differences: 0. A:ET nonblank type differences: 1,269 (canonical float vs candidate int serialization; underlying values unchanged).

Market Intelligence: 755 x 264. Governed headings/comments: 264/264. Exact FootyStats fixture identity: 387/387. Governed Formula Input QA fixtures: 387.

Permanent gate outcome after re-run: FORMULA_INPUT_STATUS READY 0/387; BACKTEST_READY YES 0/387; RELEASE_DECISION PASS 0/387; RELEASE_DECISION FAIL 387/387.

Hard blockers: immutable native Excel numeric-type gate; V2.1.1 not explicitly certified by a workbook schema marker; 169/387 fixtures below 100% required MI coverage; 67/754 kickoff/date review records; 0/754 verified xG capture timestamps; 15 implausible goal-environment records quarantined as UNAVAILABLE/UNVERIFIED.

No missing value was converted to zero or estimated. No A:ET value was changed. Oracle V1.6 production logic was not changed.

The QA layer was hardened so blocker notes can never coexist with RELEASE_DECISION=PASS. The release gate remains fail-closed.