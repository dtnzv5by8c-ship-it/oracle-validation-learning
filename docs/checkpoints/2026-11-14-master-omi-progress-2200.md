# Oracle Master OMI Progress Checkpoint — 2026-11-14 22:00 SAST

## Cycle objective
Advance Master OMI fixture-level evidence completeness without changing Oracle V1.6 production logic.

## Durable run consumed
- Public prospective run: 43632219913
- Result: SUCCESS
- Head: e5a4691743808e2ca821ff5654ed884cf6b1be00
- Current Team State rows verified: 13,852
- Prospective pipeline completed prediction, NO_BET diagnosis, publication, settlement, governance and evidence persistence.
- No overlapping prospective run was started.

## New finding — admission/diagnostic contract mismatch
The completed run confirms 76 NO_BET fixtures remain, but the root-cause diagnostic does **not** support treating all 76 as genuinely missing five-match Team State.

Root-cause distribution across the 76 NO_BET rows:
- 30 rows: diagnostic root_cause is blank even though production ledger status is NO_BET. For these rows, the diagnostic reports current pre-match n >= 5 on both sides, and in many cases protected pre-match rows also exist.
- 21 rows: both sides genuinely below the five-match current-state threshold and have no protected pre-match match.
- 6 rows: away side has no protected pre-match match.
- 5 rows: home side has no protected pre-match match.
- 5 rows: home current history is <5 and no protected home match.
- 5 rows: away current history is <5 and no protected away match.
- 2 rows: away current history <5 plus no protected match on both sides.
- 1 row: no protected pre-match match on both sides.
- 1 row: home current history <5 plus no protected match on both sides.

The most important new information is therefore the **30-row mismatch cohort**. Examples include Manchester City vs Fulham, Bayer Leverkusen vs Paderborn, Borussia M'gladbach vs Borussia Dortmund, Atalanta vs Inter Milan, and other fixtures where the diagnostic can see five qualifying current pre-match observations on both sides, yet the production predictor still emits NO_BET.

## Interpretation
This is no longer primarily an alias-coverage problem. It indicates a reconciliation gap between:
1. the state rows the diagnostic can resolve, and
2. the exact identity/key/path used by the production admission gate.

We must not weaken the five-match admission rule or bypass the production gate. The safe next improvement is to reconcile the exact state key, league namespace, canonical identity, state_asof selection and admission reason used by the predictor against the diagnostic for this 30-row cohort.

## Required next action
Build a read-only admission reconciliation against the completed run:
- exact fixture identity;
- production-resolved home/away state keys;
- league namespace;
- current Team State candidate rows;
- strictly pre-match qualifying rows;
- protected fallback candidates;
- state_asof result;
- final production admission reason;
- diagnostic-derived admission result.

Then classify each of the 30 mismatches as:
- state-key mismatch;
- league-namespace mismatch;
- state_asof/chronology mismatch;
- protected-fallback path mismatch;
- admission-contract/reporting mismatch;
- other proven integration defect.

Only after the exact class is proven should a targeted integration fix be made. Do **not** change Oracle V1.6 logic, thresholds or five-match governance.

## Coverage baseline
- Governed fixtures: 385
- Last authoritative governed publication baseline before this run: 362/385 = 94.03%
- The completed run's new coverage should not be promoted to a higher percentage until the persisted ledger and the 30-row reconciliation are independently verified.

## Governance
- Oracle V1.6 production logic: unchanged.
- A–CS Master OMI columns: protected.
- Chronology/leakage controls: preserved.
- H2H <5 remains non-blocking and labelled.
- Betting remains fail-closed.
- No fabricated values.

## Cycle result
Concrete blocker isolated: **30 production NO_BET records appear Team-State-eligible under the diagnostic view.**
No unsafe production change was made.
