# Oracle 50-League Downstream Code Reconciliation Audit

Date: 2026-11-07

## Finding
The governed 50-league source registry uses canonical source codes such as ARG1, EPL, FR1, DE1, IT1 and NED1, while the current private prediction engine uses a legacy 27-code allow-list such as E0, E1, F1, D1, I1 and N1.

A direct code-set comparison is therefore unsafe: the canonical 50 source codes must not simply be substituted into the production engine until an exact league-identity mapping is independently evidenced.

## Evidence
- Private production file: `scripts/oracle_four_model_predict.py`
- Current engine allow-list contains 27 legacy codes:
  `E0,E1,E2,E3,SP1,SP2,D1,D2,I1,I2,F1,F2,N1,P1,T1,B1,SC0,AUT,SWZ,POL,ROU,NED2,POR2,CZE,CRO,UKR,RSA`
- Canonical 50-league source registry contains 50 governed source codes.
- Direct string intersection between the 50 canonical source codes and the 27 legacy engine codes is only **CRO**.
- Therefore 49/50 governed source codes require an explicit identity mapping before downstream prediction scope can be safely advanced.

## Root Cause
The historical/provider source identity namespace and the legacy prediction-engine league-code namespace evolved separately. The existing engine's 27-league allow-list is not a canonical governed-universe registry.

## Impact
A blind replacement of the legacy allow-list could mis-route fixtures into the wrong league model or silently exclude valid fixtures. This is a data/universe configuration risk, not a reason to alter Oracle V1.6 model logic.

## Fix Direction
Build an evidence-backed league identity bridge using existing fixture/database metadata and the governed 50-league registry. Each mapping must be one-to-one and independently validated before it can feed production scope.

The bridge must explicitly represent:
- governed league identity
- canonical FootyStats league ID
- canonical source code
- OpenFoot competition ID
- production/internal league code, if one exists
- mapping evidence
- mapping status
- fail-closed status when no exact mapping exists

## Validation Rule
No production downstream scope change is admissible until:
1. all 50 governed identities are represented;
2. every production/internal code mapping is exact and one-to-one;
3. unmapped identities remain explicitly DATA_GATED rather than dropped;
4. the live 50-league fixture board has independently passed source validation and exact identity reconciliation;
5. Oracle V1.6 production logic/probabilities/calibration/thresholds/governance remain unchanged.

## Current Status
**BLOCKED — mapping evidence required.**

This audit is research/control-plane only and does not modify production prediction logic.
