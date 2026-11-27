# PROJECT ORACLE / MASTER OMI — FULL HANDOVER
## Handover date
2026-11-27 (SAST)

## PURPOSE
Continue Project Oracle / Master OMI from the exact live state of the public GitHub repository. The immediate business requirement is to produce the current Master OMI Excel report with the **Market Intelligence** tab for the governed rolling 50-league universe, without weakening governance, altering Oracle V1.6, or fabricating data.

## PRIMARY REPOSITORY
Public engineering / production validation repository:
- dtnzv5by8c-ship-it/oracle-validation-learning
- https://github.com/dtnzv5by8c-ship-it/oracle-validation-learning

Older engineering repository:
- dtnzv5by8c-ship-it/oracle-football-data

Prioritize oracle-validation-learning.

## LOCKED GOVERNANCE
1. Governed universe = 50 leagues.
2. Current fixture spine = the fresh rolling 50-league Fixture-ID set. Current row count is VARIABLE.
3. Never force weekly rows to 754/755/385/372.
4. Never pad/truncate or mix stale historical fixtures into the current spine.
5. Market Intelligence schema = exactly 264 columns.
6. A:ET = immutable cell-reference contract.
7. FootyStats intelligence is append-only after ET.
8. Exact Fixture-ID identity only. No fuzzy matching.
9. No estimates, guesses, zero-fill, historical fallback, timezone normalization, post-kickoff leakage, or unsupported substitution.
10. If evidence is unavailable, record explicit unavailable/unverified status and provenance/reason.
11. Missing mandatory formula inputs block release.
12. Oracle V1.6 production model logic is unchanged.
13. PIT chronology is mandatory.
14. Current prediction ledger must exactly match the governed current Fixture-ID set before certification.

## CANONICAL WORKBOOK
Locked canonical workbook:
Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx

Known ChatGPT Library copy:
- library_file_id: libfile_db76629260a08191ad7b4e08d9e6ec1a
- conversation file id: file_00000000a5e88211b627082a0fcd85b5
- size: 4,800,304 bytes
- canonical SHA required by workflow:
  9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e

IMPORTANT:
The canonical binary is in ChatGPT Library and is NOT in the public GitHub repository. It was not authorized for public publication. Do NOT upload it publicly just to unblock automation.

Canonical workbook evidence:
- 754 historical/reference Market Intelligence fixture rows.
- 264 Market Intelligence columns.
- A:ET immutable.
- Existing formulas/cell references must be preserved.
- Provider-only fields unavailable in source must remain explicitly unavailable.
- xG without verified capture timestamp/provenance must be quarantined/unverified.
- Research evidence must not overwrite Oracle V1.6 probabilities.

## ACTIVE CONTRACT FILES
- docs/master_omi/CANONICAL_V2_1_1_SCHEMA.json
  - 264 headers
  - variable_fixture_rows=true
- docs/master_omi/CANONICAL_V2_1_1_CONTRACT.json
  - market_intelligence_rows = VARIABLE_CURRENT_ROLLING_SPINE
  - governed_fixture_rows = EXACT_CURRENT_FIXTURE_ID_SET
  - immutable columns = A:ET
  - status = ACTIVE_VARIABLE_ROW_CONTRACT
  - canonical SHA = 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e
  - canonical A:ET contract SHA = b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564

## CURRENT LIVE DATA STATE
Latest known successful public Current Data run:
- Run 46066784664
- Commit 593525d781f28028cc69d953ef3a2a71da927ec4
- All 29 workflow steps passed.
- Prediction ledger: 369 rows / 16 columns; 369 unique IDs; exact 369/369 parity.
- Current Team State: 369 rows / 42 columns; exact 369/369 parity.
- Current rolling spine at the latest QA snapshot: 369 fixtures, 50 governed leagues, 41 fixture-bearing league-season IDs.
- Exact provider IDs, no duplicates, no fuzzy/historical fallback, pre_match_only.
- Latest 50-League Live Fixture Source Validation run: 46068428427, successful.
- Latest referenced 50-League MI Build run: 46054730403, successful but snapshot was stale by later QA time.
- Current-data artifact from run 46066784664 exists as GitHub Actions artifact 15232026165.
- 50-league MI artifact from run 46054730403 exists as artifact 15225488215.

## CURRENT MI COVERAGE / LIMITATIONS AT LAST QA
At QA snapshot:
- Current FootyStats MI: 369 x 139, exact parity 369/369 DIRECT_PROVIDER_PREMATCH.
- Last-5: 369/369 verified.
- Venue Last-5: 354 verified / 15 insufficient sample.
- H2H: 39 verified / 330 no authoritative history.
- Home/Away PPG: 369/369.
- xG: 369/369 but UNVERIFIED_NO_CAPTURE_TIMESTAMP.
- GF/M: unavailable for all 369.
- GA/M: unavailable for all 369.
- Direct provider BTTS: unavailable for all 369.
- No estimates/zero-fill were allowed.

Therefore the current upstream data artifact is NOT itself the final 264-column Master OMI workbook.

## LAST QA RESULT
Independent QA automation result:
- FAIL-CLOSED.
- Evidence path:
  docs/master_omi/qa/MASTER_OMI_MI_QA_AUTOMATION11_TURN11_CURRENT_2026-11-27_2312SAST.md
- Core data pipeline passed.
- Final workbook certification failed because:
  1. canonical workbook binary was not available to GitHub automation;
  2. no approved current workbook candidate XLSX/XML existed;
  3. safe canonical overlay implementation was missing;
  4. therefore A:ET equality, native Excel types, formulas, actuals, LTSS/CMOI, derived formula inputs, workbook XML integrity and final workbook hash could not be certified.

## MASTER OMI EXPORT WORKFLOW — CURRENT STATE
Workflow:
.github/workflows/oracle-master-omi-excel.yml

The workflow currently:
1. Checks rolling current-spine freshness.
2. Requires public-only current source artifacts.
3. Runs exact matching regression gate.
4. Validates active 264-column variable-row contract.
5. Installs Excel dependencies.
6. Requires authoritative canonical workbook binary at:
   runtime/canonical/Oracle_Master_OMI_CANONICAL_v2_Last3PPG_LTSS_V1_H2H_FootyStats_LOCKED.xlsx
7. Verifies canonical SHA.
8. Copies canonical to runtime/work/Master_OMI_Report_BASE.xlsx.
9. THEN FAILS CLOSED intentionally with:
   MASTER_OMI_BLOCKED_NO_SAFE_OVERLAY_IMPLEMENTATION
10. The old synthetic workbook builder has been removed.

Do NOT remove the fail-closed block unless a genuine safe overlay implementation exists.

## RECENT PERMANENT FIXES
1. Timestamp-drift gate fixed:
   commit 21d848db17ac1f05dbe71c02fe358f172686a28
   Compare exact spine SHA and Fixture-ID-set SHA, not unrelated process timestamps.

2. 50-league semantic validation fixed:
   commit 2b56ee95f9ade3f4c2307e46b4b14e929670432a
   governed_leagues must equal 50; season_ids_with_fixtures only needs to be >=1.

3. Historical/current Team State separation fixed:
   commit ca2b53b41fa4704654cbb1f1add1f9c15da6012d

4. Prediction engine repair:
   commit 7313c88a07b67fe9d762a8e0ea123415c5dc74d0

5. Exact identity regression fixed:
   commit e6169a8bc7b79eb493647db357a2a068f696d9c2

6. Current Team State production validation/deployment fix:
   private production workflow commit bb4f0d1243b8dd4c2ab7c1a84630c7f1598a64f5
   Added authoritative pre-ingestion rolling-spine gate.

7. Variable-row Master OMI contract corrected:
   docs contract/schema created and active.

8. Unsafe synthetic Master OMI builder removed:
   commit e9fdf8cf1a4773e447cbc0522034101eea5f1155

9. Explicit no-overlay fail-closed gate added:
   commit 332c1f76450f684035101236c0e7f88fb0997eaa

## AUTOMATIONS
1. Master OMI MI Remediation — Root Cause
   ID: 6b030cbf6cf481918c2ff41286bbc524
   Hourly at minute 15 SAST.
   Historical-first. Must inspect live GitHub state, workflow runs, Lessons Learned, Continuation State, latest QA/root-cause artifacts and recent commits before diagnosing.

2. Master OMI MI QA — 100% Gate
   ID: 6aff2ac2aacc819187a6fe78f8ff6d8f
   Hourly at minute 55 SAST.
   Independent 100% release gate. Fail closed until all controls pass.

Do not create duplicate automations.

## THE REAL REMAINING PROBLEM
The problem is now architectural, not another data patch:
A GitHub Action cannot access the locked canonical binary currently stored in ChatGPT Library.

A second dependency is the safe overlay/export implementation.

The final implementation MUST:
- obtain the canonical binary through an approved non-public automation-accessible mechanism OR run the final workbook build in an approved environment where the canonical binary is available;
- copy canonical binary unchanged as base;
- map current rolling Fixture IDs exactly;
- preserve A:ET cell references/values/formulas for all governed cells;
- populate only controlled intelligence fields after ET;
- handle variable current row count without introducing stale rows;
- preserve workbook native Excel types/formulas;
- validate final workbook XML;
- calculate final workbook SHA;
- run independent QA;
- publish the final XLSX artifact.

Do NOT solve this by:
- uploading the canonical workbook to the public repo;
- rebuilding the workbook from CSV;
- creating a synthetic 264-column workbook;
- forcing 754 rows;
- deleting/inserting/reordering A:ET rows without proving cell-reference safety;
- changing Oracle V1.6 logic.

## CRITICAL DESIGN QUESTION FOR THE NEW CHAT
Before implementing the overlay, inspect the canonical workbook's actual structure:
- sheet names;
- Market Intelligence header row;
- exact fixture-ID column;
- exact current formula columns;
- whether rows can be replaced/reordered safely;
- whether the canonical workbook already contains a current-report surface or hidden target range;
- whether a controlled current MI sheet can be created without modifying A:ET;
- exact append boundary after ET.

The canonical file must be inspected directly from Library if necessary. Do not infer its structure from old summaries.

## IMMEDIATE EXECUTION PLAN
### Phase 1 — Recover canonical binary safely
A. Materialize the canonical Library file locally.
B. Verify SHA = 9a02da12dd61b8cd588278c99d7ed544f8bf1a09cc3218aad2629ccbe39f106e.
C. Inspect workbook XML / openpyxl structure.
D. Identify exact Market Intelligence row/column contracts.

### Phase 2 — Build controlled overlay
A. Obtain fresh current 50-league spine.
B. Obtain current prediction ledger.
C. Obtain current Team State.
D. Obtain current FootyStats MI.
E. Exact Fixture-ID join only.
F. Write current intelligence into the approved Market Intelligence surface.
G. Preserve A:ET.
H. Explicitly classify unavailable fields.
I. No fabricated values.

### Phase 3 — Validate
Required checks:
- 50 governed leagues.
- exact current Fixture-ID parity.
- unique IDs.
- kickoff timestamps valid.
- all records pre-match where prediction inputs are used.
- 264 columns.
- A:ET unchanged.
- append-only intelligence.
- formulas intact.
- native Excel types intact.
- no stale fixture leakage.
- no duplicate fixture rows.
- no fuzzy matches.
- provenance present.
- prediction ledger exact parity.
- workbook XML opens cleanly.
- final SHA captured.

### Phase 4 — Independent certification
Run the 100% QA automation independently.
Only after PASS:
- publish XLSX as GitHub Actions artifact;
- give Nolan the file;
- record run ID, commit SHA, spine SHA, Fixture-ID SHA, workbook SHA and QA result.

## CURRENT USER REQUIREMENT
Nolan explicitly said:
“Please execute all that you need to. I need the report now.”

Therefore the next chat must NOT simply repeat the blockers. It must actively:
1. inspect the canonical workbook;
2. inspect the live repository;
3. recover/construct the safe overlay path;
4. execute the build;
5. run QA;
6. deliver the actual Master OMI report.

If a secure GitHub Actions canonical-binary path remains impossible, the fallback should be an approved local/ChatGPT-side build using the Library canonical binary, followed by independent validation. Do not publish the canonical binary publicly.

## CONTINUATION PROMPT — COPY THIS INTO THE NEW CHAT

“GEM — CONTINUE PROJECT ORACLE FROM THE LIVE GITHUB HANDOVER

Use the handover at:
docs/master_omi/MASTER_OMI_FULL_HANDOVER_2026-11-27.md

Repository:
dtnzv5by8c-ship-it/oracle-validation-learning

PRIMARY OBJECTIVE:
Finish and deliver the current Master OMI Excel report NOW. Do not restart diagnosis from scratch.

MANDATORY:
1. Read the handover first.
2. Inspect the live GitHub workflow and latest runs.
3. Inspect the canonical workbook directly from the ChatGPT Library if required.
4. Do not publish the canonical workbook publicly.
5. Do not reintroduce the synthetic workbook builder.
6. Do not remove the fail-closed gate until a safe overlay implementation exists.
7. Build the final report from the locked canonical workbook.
8. Preserve A:ET exactly.
9. Keep exactly 264 Market Intelligence columns.
10. Use the fresh rolling 50-league Fixture-ID set as the current fixture spine; row count is variable.
11. Exact Fixture-ID joins only.
12. No fuzzy matching, estimates, zero-fill, historical fallback, timezone normalization or post-kickoff leakage.
13. Populate all supported intelligence fields with provenance; explicitly classify unavailable fields.
14. Do not change Oracle V1.6.
15. Validate formulas/native types/XML.
16. Run independent Master OMI 100% QA.
17. If QA passes, publish the XLSX and give me the file/artifact.
18. If GitHub Actions cannot securely access the canonical binary, use the approved Library/local build fallback rather than delaying indefinitely, but do not expose the canonical workbook publicly.
19. Record all commits, hashes, run IDs and validation results.
20. Update this handover/Continuation State with every permanent fix.

CURRENT KNOWN BLOCKER:
The public GitHub exporter has the canonical-base gate and then intentionally fails with MASTER_OMI_BLOCKED_NO_SAFE_OVERLAY_IMPLEMENTATION. The old synthetic builder was removed permanently. The next task is to implement the safe overlay against the actual canonical workbook structure and then certify the resulting workbook.

DO NOT GIVE ME ANOTHER STATUS-ONLY RESPONSE. EXECUTE THE RECOVERY, BUILD, QA AND DELIVERY.”

## SUCCESS CONDITION
The task is complete only when Nolan has an actual current Master OMI XLSX with the Market Intelligence tab and an independent QA PASS, or when a hard technical impossibility is demonstrated with exact evidence.


## IMMEDIATE WORKING REPORT CREATED — 27 NOV 2026
A local working export was successfully created from the locked canonical binary plus the latest public rolling intelligence snapshot.

File:
Oracle_Master_OMI_CURRENT_WORKING_2026-11-27.xlsx

Working export SHA256:
8e6841adbc8a7a5177ce5a6905864993db62ee88afd99114b88e438f2b85e

Important status:
- This is a WORKING intelligence export, not the final certified production Master OMI.
- The original locked `Market Intelligence` sheet remains untouched at 755 x 264.
- A separate `Market Intelligence CURRENT` sheet contains the current 369-fixture rolling intelligence surface at exactly 264 columns.
- `CURRENT REPORT STATUS` records the release state and known data gates.
- Canonical Market Intelligence A:ET was programmatically compared before/after and verified unchanged.
- Current source snapshot used the successful 50-League MI artifact (run 46054730403 / artifact 15225488215) and current Team State artifact (run 46066784664 / artifact 15232026165).
- This working export intentionally does NOT claim independent 100% production certification.
- The production GitHub workflow remains fail-closed until the safe canonical overlay is implemented.
- The working export provides an immediate view of the current intelligence while preserving the locked canonical workbook.

Canonical workbook inspection completed:
- Market Intelligence = 755 rows x 264 columns.
- Fixture ID = column 39.
- ET = column 150; EU = column 151.
- Existing Market Intelligence header/formula surface remains intact.

---
END HANDOVER


## 2026-11-28 — Permanent exporter architecture fix applied
The previous variable-row exporter was corrected so it can no longer delete/rebuild the locked canonical `Market Intelligence` sheet. The locked canonical sheet remains the immutable A:ET reference surface; the variable rolling 50-league current data is now materialised in a separate `Market Intelligence CURRENT` sheet.

Commits:
- `dbdad0e3fde2c474808cd2477e25fd967b4043f5` — safe non-destructive current-surface builder.
- `6af5a4b32311af09e4b4ef93c7dd541f1c653394` — workflow validates `Market Intelligence CURRENT` and retains locked canonical surface.
- `d72bd58aad25ee8bd4ea32a4520b6c513c268bfb` — derived eligibility outputs removed from mandatory-input gate.
- `3460cca37f254589aa8e0786c13ca1725d12b407` — lessons-learned record.

Provider-specific FootyStats Last-5 GF/M and GA/M mappings were corrected to their provider fields. Exact Fixture-ID/PIT controls remain active.

Current runtime remains fail-closed until the public current prediction ledger and Team State are regenerated against the same fresh rolling 50-league spine. At the latest inspected state, the rolling spine is 359 rows while persisted current Team State/ledger remain 369 rows; this mismatch is correctly blocking release.


## 2026-11-28 — kickoff-level PIT rebuild verified
- Public current-data run: `46076862247` completed SUCCESS.
- Fresh governed rolling spine: 359 fixtures.
- Current pre-match Team State: 359/359 exact Fixture-ID parity.
- Prediction Team-State compatibility: 359/359 exact parity.
- Current prediction ledger: 359/359 exact parity.
- Kickoff-level PIT: 0 violations; all home/away state cutoffs are strictly before governed kickoff.
- Ledger status after permanent PIT fix: CONTROLLED 203, WATCH 140, NO_BET 16.
- The prior widespread false missing-Team-State classification is therefore cleared at the source integration layer; Oracle V1.6 model logic remains unchanged.

## 2026-11-28 — permanent canonical automation path
- The public Master OMI exporter remains fail-closed and must not contain the canonical workbook binary.
- Commit `ebac68ae567a0300e94bcfc3b9726a91b55896f7` changes the exporter to checkout the private `oracle-football-data` repository using the existing `ORACLE_PRIVATE_REPO_TOKEN`, locate the locked canonical workbook by exact filename, materialise it into the runner, and then enforce the canonical SHA before export.
- This permanently separates public governed evidence from the private canonical workbook base.
- Current blocker: the locked canonical binary is not yet present in the private production repository, so the exporter cannot reach production certification until that one-time binary placement is completed.
