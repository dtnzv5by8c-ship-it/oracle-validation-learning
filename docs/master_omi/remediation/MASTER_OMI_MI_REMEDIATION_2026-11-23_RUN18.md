# Master OMI MI Remediation — Run 18 — 2026-11-23

RELEASE_DECISION=FAIL-CLOSED

Latest QA: docs/master_omi/qa/MASTER_OMI_QA_AUTOMATION11_RUN18_REAUDIT_2026-11-23_1324SAST.md
QA commit: 14795481a34a344d4f05b72c5a6268eef3ff50bc
Latest remediation reviewed: Run 17
Run 17 candidate SHA-256: e741eae321e99ded8f3e266e4e0023ed3dff5e26c8fb274a36043abd9fcf0a7c
Run 17 MI worksheet XML SHA-256: f19e5c2c06e3b3704fbd6439dd7f6ba60fb69937cf2b662d6d96565cf3dd0830

Canonical V2.1.1 baseline:
- Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
- SHA-256: 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
- MI: 755 x 264; governed fixtures: 754
- Immutable A:ET
- Canonical A:ET contract hash: b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564

Run 17 already applied the only source-backed contract-permitted remediation in the current evidence set: 21,749 type-only conversions of valid analytical numeric-looking text outside ET. 15,574 numeric-looking analytical cells remain inside immutable A:ET. 25 numeric-looking strings outside ET remain text because they are verified FootyStats provenance/source-fixture IDs in GG:GJ.

Run 18 is a controlled carry-forward of Run 17 because the latest QA evidence states no additional source-backed correction is safe without a fresh binary-level audit and authoritative evidence.

Direct Run 18 scan:
- MI dimensions: 755 x 264
- Governed fixtures: 754
- A:ET numeric-looking text: 15,574
- Outside-ET numeric-looking text: 25
- Analytical numeric-looking text outside ET: 0
- Excel errors: 0
- Formula cells: 0

Retained source-ID cells:
GI24,GJ35,GG40,GI40,GI163,GJ164,GJ165,GJ177,GH340,GI340,GG341,GJ341,GH455,GI455,GJ466,GI610,GJ610,GI611,GG612,GI612,GJ621,GH622,GJ711,GJ755

Immutable protections:
- A:ET values changed: 0
- A:ET schema changed: 0
- Oracle V1.6 changed: 0
- Source/provenance IDs changed: 0

Unresolved QA blockers:
1. 15,574 immutable A:ET numeric-type exceptions.
2. 67 kickoff/date REVIEW_REQUIRED.
3. 754/754 xG capture timestamps UNVERIFIED_NO_CAPTURE_TIMESTAMP.
4. CMOI UNAVAILABLE/UNVERIFIED.
5. 754/754 Formula Input BLOCKED.
6. 0/754 Backtest READY.
7. No fresh independent binary-level 754 x 264 QA artifact exposed after Run 17.

Candidate:
Oracle_Master_OMI_V2_1_1_REMEDIATION_RUN18_2026-11-23_EXACT_AET.xlsx
SHA-256: e741eae321e99ded8f3e266e4e0023ed3dff5e26c8fb274a36043abd9fcf0a7c

Cells changed in Run 18 relative to Run 17: 0.
Release remains FAIL-CLOSED.