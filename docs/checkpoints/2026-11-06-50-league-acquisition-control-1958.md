# Project Oracle — 50-League Acquisition Control Checkpoint — 2026-11-06 19:58 SAST

## Scope
Governed universe: **exactly 50 leagues / 182 provider seasons / 728 endpoint tasks**.
Production model: **Oracle V1.6 unchanged**.

## Private acquisition evidence
Latest persisted private checkpoint observed: **Run 42266731695**.
- completed tasks in batch: **75**
- provider requests: **100**
- production_eligible: false
- betting_eligible: false
- raw payloads public: false
- manifest file SHA-256: `58bd06ed9c5a6a09ed55eb833319ca09cd4f01e2b175e4ca9127a1b3a7f689d7`
- pinned manifest blob SHA: `57fe9e1184b5035327feaa78307750e129c54bf3`

## Reconciled control-plane state
- completed endpoint tasks: **518**
- quarantined provider-blocked tasks: **68**
- pending endpoint tasks: **142**
- successful completion: **71.15%**
- processed including quarantined: **80.49%**
- completed tasks outside manifest: **0**
- completed/blocked overlap: **0**

The private rolling ledger shows the latest reservation for Run 42266731695 as **COMPLETED**, reserved 100 and observed 100 provider requests.

## Manifest gate
The public governed manifest remains **728 rows / 50 leagues / 182 provider seasons**, with current Git blob SHA `6a916c962bfbcad1cfb429e23c26e0aef9b3a611`.
The private workflow remains pinned to the immutable plan commit `57fe9e1184b5035327feaa78307750e129c54bf3`. No manifest change was introduced.

## Next deterministic bounded batch
The private workflow's deterministic selection rule is manifest row order after excluding all completed and quarantined task IDs. The next bounded 100-task selection is:

```
FS:12446:league-matches:p1
FS:12446:league-teams:p1
FS:12446:league-tables:p1
FS:12446:league-season:p1
FS:14934:league-matches:p1
FS:14934:league-teams:p1
FS:14934:league-tables:p1
FS:14934:league-season:p1
FS:17180:league-matches:p1
FS:17180:league-teams:p1
FS:17180:league-tables:p1
FS:17180:league-season:p1
FS:9660:league-matches:p1
FS:9660:league-teams:p1
FS:9660:league-tables:p1
FS:9660:league-season:p1
FS:12325:league-matches:p1
FS:12325:league-teams:p1
FS:12325:league-tables:p1
FS:12325:league-season:p1
FS:15050:league-matches:p1
FS:15050:league-teams:p1
FS:15050:league-tables:p1
FS:15050:league-season:p1
FS:17146:league-matches:p1
FS:14956:league-season:p1
FS:17199:league-matches:p1
FS:17199:league-teams:p1
FS:17199:league-tables:p1
FS:17199:league-season:p1
FS:9675:league-matches:p1
FS:9675:league-teams:p1
FS:9675:league-tables:p1
FS:9675:league-season:p1
FS:12467:league-matches:p1
FS:12467:league-teams:p1
FS:12467:league-tables:p1
FS:12467:league-season:p1
FS:15066:league-matches:p1
FS:15066:league-teams:p1
FS:15066:league-tables:p1
FS:15066:league-season:p1
FS:17269:league-matches:p1
FS:17269:league-teams:p1
FS:17269:league-tables:p1
FS:17269:league-season:p1
FS:17350:league-matches:p1
FS:17350:league-teams:p1
FS:17350:league-tables:p1
FS:17350:league-season:p1
FS:16263:league-matches:p1
FS:16263:league-teams:p1
FS:16263:league-tables:p1
FS:16263:league-season:p1
FS:16576:league-matches:p1
FS:16576:league-teams:p1
FS:16576:league-tables:p1
FS:16576:league-season:p1
FS:9580:league-matches:p1
FS:9580:league-teams:p1
FS:9580:league-tables:p1
FS:9580:league-season:p1
FS:12326:league-matches:p1
FS:12326:league-teams:p1
FS:12326:league-tables:p1
FS:12326:league-season:p1
FS:15047:league-matches:p1
FS:15047:league-teams:p1
FS:15047:league-tables:p1
FS:15047:league-season:p1
FS:17129:league-matches:p1
FS:17129:league-teams:p1
FS:17129:league-tables:p1
FS:17129:league-season:p1
FS:9913:league-matches:p1
FS:9913:league-teams:p1
FS:9913:league-tables:p1
FS:9913:league-season:p1
FS:12641:league-matches:p1
FS:12641:league-teams:p1
FS:12641:league-tables:p1
FS:12641:league-season:p1
FS:14972:league-matches:p1
FS:14972:league-teams:p1
FS:14972:league-tables:p1
FS:14972:league-season:p1
FS:17265:league-matches:p1
FS:17265:league-teams:p1
FS:17265:league-tables:p1
FS:17265:league-season:p1
FS:10977:league-matches:p1
FS:10977:league-teams:p1
FS:10977:league-tables:p1
FS:10977:league-season:p1
FS:13973:league-matches:p1
FS:13973:league-teams:p1
FS:13973:league-tables:p1
FS:13973:league-season:p1
FS:16504:league-matches:p1
FS:16504:league-teams:p1
FS:16504:league-tables:p1
FS:16504:league-season:p1
```

This is a **prepared batch only**. No private workflow was triggered by this control-plane checkpoint.

## Validation admission
The batch is recorded for downstream validation/control-plane purposes, but no raw private payloads are admitted into OMI/backtesting/prediction until an admissible private gateway receipt and row-level validation evidence are available. No production logic, probabilities, thresholds or betting logic were modified.
