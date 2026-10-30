# Oracle Data & Team DNA — 30 Oct 2026, 11:15 SAST

- Audited the existing 27-league Team DNA V2 and four-model chronological OOS summaries at source commit cb89e5bd1c24810fe821a6b2c3c2c1c19272b381.
- Strongest research-only Team DNA incremental signals: DC Home (+0.002112 Brier, CI excludes zero), DC Away (+0.002131, CI excludes zero), and smaller Combo Home (+0.000744, CI excludes zero). BTTS and Combo Away intervals include zero; M1UP Team DNA has only 58 scored rows in one fold and is insufficient.
- Corrected feature coverage interpretation: principal markets have 10,139 complete DNA rows from 10,362 post-warmup test fixtures (97.85%, 223 missing). M1UP has 58/58 complete after warmup; it is a sample-size limitation, not 94.5% missing.
- Found M1UP export many-to-many join: 3,300 rows/825 fixtures/four rows per fixture and 1,650 duplicate match-venue keys. The clean calibration export is 1,650 team-target rows/825 fixtures but has no venue/team IDs. Do not use the defective export for venue or baseline analysis.
- Team sample adequacy: 651 ALL-scope teams; median 48 fixtures; 169 below 30 and 73 below 8. Legacy m1up_rate is all-zero/unpopulated, not zero performance. Manifest team count 562 conflicts with 651 output labels; one older AWAY profile is missing.
- Committed a research-only team-market OOS profile builder, five tests, a push test workflow and a manual read-only audit workflow. Manual dispatch is required to generate named team profiles from the pinned source checkout.
- Selected-50 xG/Belgium odds issues remain separate and exploratory pending archive lineage and source timestamp resolution. No H2H data was read. No provider calls/credits or production changes.

Next action: manually dispatch the Oracle Team DNA OOS Integrity Audit workflow with confirm_private_source_read=true, then review team-market summaries and chronological halves with n>=30 safeguards. Reconcile team-count metadata and the M1UP export join before using venue-specific evidence.
