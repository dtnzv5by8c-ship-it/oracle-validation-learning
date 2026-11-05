# FootyStats exact crosswalk human-decision queue audit — 2026-11-05

## Scope

Research-only audit of the current 49-league FootyStats catalogue-to-Oracle candidate crosswalk and its explicit human decision queue. No provider API calls were made. No private repository was accessed or modified. Oracle V1.6 production logic and governed outputs were not changed.

## Live branch checkpoint

Validated immediately before this audit:

`9a01b8f9e9453ed05928f51a68035c12308b7686`

No shared protocol file was modified.

## Exact queue status

The current catalogue contains 49 selected provider leagues. The human-decision queue contains exactly **22 candidate canonical mappings**.

- Candidate mappings: **22**
- Candidate mappings approved: **0**
- Candidate mappings rejected: **0**
- Candidate mappings still requiring human approval: **22**
- Current catalogue entries without a prior legacy-50 identity: **5**
- Candidate rows with a protected 27-league registry match: **0**
- Candidate rows with a prior protected-registry state of `CANDIDATE_MATCH_REQUIRES_HUMAN_REVIEW`: **22**

The 22 candidates are:

| Provider league | Candidate canonical ID | Candidate competition | Evidence state |
|---|---|---|---|
| Austria Bundesliga | AUT_A1 | Austrian Bundesliga | Human approval required |
| Belgium Pro League | BEL_B1 | Belgian Pro League | Human approval required |
| Croatia Prva HNL | HRV_HR1 | Croatian HNL | Human approval required |
| Czech Republic First League | CZE_CZ1 | Czech First League | Human approval required |
| England Championship | ENG_E1 | Championship | Human approval required |
| England EFL League One | ENG_E2 | League One | Human approval required |
| England Premier League | ENG_E0 | Premier League | Human approval required |
| France Ligue 1 | FRA_F1 | Ligue 1 | Human approval required |
| France Ligue 2 | FRA_F2 | Ligue 2 | Human approval required |
| Germany 2. Bundesliga | DEU_D2 | 2. Bundesliga | Human approval required |
| Germany Bundesliga | DEU_D1 | Bundesliga | Human approval required |
| Italy Serie A | ITA_I1 | Serie A | Human approval required |
| Italy Serie B | ITA_I2 | Serie B | Human approval required |
| Netherlands Eredivisie | NLD_N1 | Eredivisie | Human approval required |
| Poland Ekstraklasa | POL_P1 | Ekstraklasa | Human approval required |
| Portugal LigaPro | PRT_P2 | Liga Portugal 2 | Human approval required |
| Scotland Premiership | SCO_SC0 | Scottish Premiership | Human approval required |
| South Africa Premier Soccer League | ZAF_PSL | South African PSL | Human approval required |
| Spain La Liga | ESP_SP1 | La Liga | Human approval required |
| Spain Segunda División | ESP_SP2 | Segunda División | Human approval required |
| Turkey Süper Lig | TUR_T1 | Turkish Super Lig | Human approval required |
| Ukraine Ukrainian Premier League | UKR_UA1 | Ukrainian Premier League | Human approval required |

## Why the candidates remain unapproved

The candidate rows have prior research evidence that is useful for investigation, but the evidence is not sufficient to promote a canonical mapping.

The crosswalk records historical ledger joins based on team-pair and date evidence, but explicitly states that these joins do **not** provide kickoff proof. The current provider catalogue also does not provide a sufficiently authoritative country/competition identity for promotion in the protected registry. Therefore the candidate IDs remain hypotheses requiring independent authoritative evidence.

Observed provider competition/master fields are not treated as canonical IDs. In particular, an observed provider `comp_master_id` is retained as provider evidence only and is not promoted to an Oracle canonical or parent competition ID.

## Decision rule

No candidate may be promoted merely because:

- the provider league name resembles a known competition;
- a candidate ID exists in prior research;
- a provider `comp_master_id` is observed;
- team-pair/date joins exist;
- the league is familiar or widely known;
- the selected catalogue contains the league.

Promotion requires independent authoritative evidence establishing the competition identity and its relationship to the Oracle canonical registry.

No fuzzy joins, inferred parent IDs, name-only promotion or automatic human-decision substitution were performed.

## New-catalogue entries

The five current catalogue leagues without a legacy-50 exact identity remain outside the candidate approval queue and require separate authoritative registry assessment:

- Bulgaria First League
- Egypt Egyptian Premier League
- Portugal Liga NOS
- Qatar Stars League
- Wales Welsh Premier League

These are not treated as missing simply because they are absent from the legacy registry. They remain `NOT_ASSESSED_AGAINST_CURRENT_PROTECTED_REGISTRY`.

## Historical evidence limitation

The season plan is structurally consistent, but the underlying archive is not yet sufficient to establish full fixture-level identity continuity. Run56 evidence covers 31/49 current leagues, while 18/49 have no Run56 selected-season evidence. The aggregate Run56 evidence does not expose fixture IDs or team IDs, so it cannot establish full cross-season fixture/team identity continuity.

The separate settlement register contains only 10 fixture-level FootyStats/FotMob pairs across two seasons, with exact ordered-team-name + UTC-kickoff joins but no home/away team-ID columns. It produced zero canonical bridge approvals and zero settlement-truth approvals.

## Governance

This audit changes no production data or model logic.

- `production_eligible=false`
- `betting_eligible=false`
- Oracle V1.6 probabilities unchanged
- Oracle V1.6 thresholds unchanged
- Oracle V1.6 calibration unchanged
- ledgers unchanged
- 728-task historical ingestion remains governed and not executed
- provider API execution remains blocked by the existing safety gate

## Next evidence required

For each of the 22 candidates, the next acceptable evidence should establish, independently and reproducibly:

1. authoritative country/competition identity;
2. exact canonical competition correspondence;
3. provider-season-to-canonical-season relationship where applicable;
4. fixture-level team identity continuity;
5. fixture chronology/kickoff evidence sufficient to distinguish competitions and seasons;
6. no conflicting canonical mapping.

Until those checks are satisfied, the correct state is **candidate / human approval required**, not canonical.
