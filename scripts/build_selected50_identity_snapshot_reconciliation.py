#!/usr/bin/env python3
"""Snapshot-scoped Selected-50 identity reconciliation; no network/API calls."""
import argparse, csv, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"reports/oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r17.csv"
MANIFEST=ROOT/"data/oracle-footystats-selected-50-season-id-manifest.csv"
EXPECTED_INGESTION="40176065362"
EXPECTED_QA="40183451811"
EXPECTED_ARTIFACT="12594568810"
EXPECTED_SHA="713ed63ed5dd6e6902a2e152367500386d5037dd6dc8bbc82fa87c831d10c375"
def read(path):
    with path.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def unique(rows,key,label):
    out={}
    for r in rows:
        v=str(r.get(key,"")).strip()
        if not v or v in out: raise ValueError(f"{label}: blank/duplicate {key}={v!r}")
        out[v]=r
    return out
def num(r,k):
    v=str(r.get(k,"")).strip()
    if not re.fullmatch(r"\d+",v): raise ValueError(f"{k}: expected integer, got {v!r}")
    return int(v)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,default=SOURCE); p.add_argument("--manifest",type=Path,default=MANIFEST); p.add_argument("--out-dir",type=Path,default=ROOT/"audit-output")
    a=p.parse_args()
    src=unique(read(a.source),"footystats_provider_id","crosswalk"); man=unique(read(a.manifest),"selected_id","manifest")
    if len(src)!=50 or len(man)!=50 or set(src)!=set(man): raise ValueError("Crosswalk and manifest must match the same 50 IDs")
    rows=[]
    for sid in sorted(man,key=lambda x:(man[x].get("country",""),man[x].get("competition_name",""),x)):
        r,m=src[sid],man[sid]
        checks={
          "provider_ingestion_run_id":EXPECTED_INGESTION,
          "provider_ingestion_run_status":"SUCCESS_50_OF_50_SEASONS_INGESTED",
          "provider_season_id_exact":sid,
          "provider_selected_id_semantics":"EXACT_PROVIDER_SEASON_ID_VERIFIED; PARENT_COMPETITION_ID_NOT_EXPOSED",
          "latest_private_archive_qa_run_id":EXPECTED_QA,
          "latest_private_archive_qa_conclusion":"success",
          "latest_private_archive_qa_artifact_id":EXPECTED_ARTIFACT,
          "latest_private_archive_qa_artifact_sha256":EXPECTED_SHA,
          "latest_private_archive_selected_id_set_match":"PASS_50_OF_50",
          "latest_private_archive_fixture_rows":"14051",
          "latest_private_archive_unique_season_fixture_pairs":"14051",
          "latest_private_archive_duplicate_pairs":"0",
          "provider_parent_competition_id_status":"NOT_EXPOSED_BY_CATALOGUE",
          "production_eligibility":"NOT_GRANTED"}
        for k,v in checks.items():
            if str(r.get(k,"")).strip()!=v: raise ValueError(f"{sid}: {k} expected {v!r}, got {r.get(k)!r}")
        latest=str(r.get("provider_selected_season_id_to_private_fixture_join_status",""))
        if not latest.startswith("EXACT_SELECTED_ID_TO_PROVIDER_SEASON_ID; PRIVATE SEASON FOLDER AND ") or EXPECTED_INGESTION not in latest:
            raise ValueError(f"{sid}: latest private-folder join not verified")
        legacy=str(r.get("selected_id_to_archive_season_fixture_join_status",""))
        legacy_rows=str(r.get("archive_primary_window_fixture_rows","")).strip()
        raw_year=str(r.get("provider_season_year_raw","")).strip()
        rows.append({
          "selected_id":sid,"country":m.get("country",""),"competition":m.get("competition_name",""),
          "selected_id_type":"PROVIDER_SEASON_ID_NOT_PARENT_COMPETITION_ID",
          "provider_season_id_exact":r.get("provider_season_id_exact",""),
          "latest_ingestion_run_id":r.get("provider_ingestion_run_id",""),
          "latest_ingestion_status":r.get("provider_ingestion_run_status",""),
          "latest_private_qa_run_id":r.get("latest_private_archive_qa_run_id",""),
          "latest_private_qa_artifact_id":r.get("latest_private_archive_qa_artifact_id",""),
          "latest_season_fixture_rows":r.get("provider_season_fixture_records",""),
          "latest_season_primary_window_rows":r.get("provider_primary_window_fixture_rows",""),
          "latest_season_recent5_both_teams_rows":r.get("provider_recent_form5_both_teams_prior_count",""),
          "legacy_run56_archive_join_status":legacy,
          "legacy_snapshot_scope":"OLDER_RUN56_SNAPSHOT_ONLY_NOT_CURRENT_PRIVATE_FOLDER_PRESENCE",
          "legacy_primary_window_rows":legacy_rows,
          "legacy_primary_window_scope":"LEGACY_ROW_VALUE_NOT_COMPARABLE_TO_LATEST_SINGLE_SEASON" if legacy_rows.isdigit() else "UNVERIFIED_IN_LEGACY_SNAPSHOT",
          "canonical_code_candidate":r.get("canonical_code_candidate",""),
          "canonical_candidate_status":r.get("crosswalk_status",""),
          "parent_competition_id_status":"NOT_EXPOSED_BY_CATALOGUE",
          "canonical_fixture_join_status":"NOT_VERIFIED",
          "canonical_team_join_status":"NOT_VERIFIED",
          "official_settlement_truth_status":"NOT_VERIFIED",
          "standings_asof_kickoff_status":"NOT_VERIFIED",
          "xg_point_in_time_status":"NOT_VERIFIED_NO_ASOF_TIMESTAMP",
          "odds_point_in_time_status":"NOT_VERIFIED_NO_ODDS_TIMESTAMP",
          "raw_season_year_token":raw_year,
          "season_year_token_status":"NONSTANDARD_8_DIGIT_TOKEN_UNVERIFIED" if re.fullmatch(r"\d{8}",raw_year) else "RAW_PROVIDER_YEAR_TOKEN",
          "production_eligible":"NO"})
    def total(k):
        return sum(num(r,k) for r in src.values())
    legacy=[r.get("selected_id_to_archive_season_fixture_join_status","") for r in src.values()]
    legacy_exact=sum(v.startswith("EXACT_SELECTED_ID_TO_ARCHIVE_SEASON_ID") for v in legacy)
    legacy_gap=sum(v.startswith("NO_EXACT_SELECTED_ID_TO_ARCHIVE_SEASON_ID_JOIN") for v in legacy)
    candidate=sum(r.get("crosswalk_status")=="CANDIDATE_REQUIRES_HUMAN_REVIEW_NOT_APPROVED" for r in src.values())
    unresolved=sum(r.get("crosswalk_status")=="UNRESOLVED_NO_EXACT_OR_EXPLICIT_ALIAS" for r in src.values())
    legacy_rows=[r for r in src.values() if str(r.get("archive_primary_window_fixture_rows","")).strip().isdigit()]
    zero=sorted(sid for sid,r in src.items() if str(r.get("provider_primary_window_fixture_rows","")).strip()=="0")
    summary={
      "status":"PASS_SELECTED50_IDENTITY_SNAPSHOT_SCOPE_RECONCILIATION_RESEARCH_ONLY","selected_groups":50,
      "latest_ingestion_run_id":EXPECTED_INGESTION,"latest_successful_season_folders":50,
      "latest_private_qa_run_id":EXPECTED_QA,"latest_private_qa_artifact_id":EXPECTED_ARTIFACT,"latest_private_qa_sha256":EXPECTED_SHA,
      "latest_private_archive_fixture_rows_global":14051,"latest_private_archive_unique_pairs_global":14051,"latest_private_archive_duplicate_pairs_global":0,
      "latest_season_fixture_rows_sum":total("provider_season_fixture_records"),
      "latest_season_primary_window_rows_sum":total("provider_primary_window_fixture_rows"),
      "latest_season_recent5_both_teams_rows_sum":total("provider_recent_form5_both_teams_prior_count"),
      "legacy_run56_exact_joins":legacy_exact,"legacy_run56_no_exact_joins":legacy_gap,
      "legacy_primary_window_rows_populated_groups":len(legacy_rows),
      "legacy_primary_window_rows_sum_populated_groups_only":sum(int(r["archive_primary_window_fixture_rows"]) for r in legacy_rows),
      "candidate_mappings_requiring_review":candidate,"unresolved_mappings":unresolved,"approved_mappings":0,
      "parent_competition_ids_verified":0,"canonical_fixture_joins_verified":0,"canonical_team_joins_verified":0,
      "official_settlement_truth_verified":0,"xg_point_in_time_verified":0,"odds_point_in_time_verified":0,
      "nonstandard_8_digit_year_tokens":sum(bool(re.fullmatch(r"\d{8}",str(r.get("provider_season_year_raw","")).strip())) for r in src.values()),
      "zero_primary_window_selected_ids":zero,"network_calls_made":0,"paid_provider_calls_made":0,
      "production_eligible":False,"betting_eligible":False,
      "interpretation":"Latest evidence confirms all 50 season folders. The older Run 56 31/19 split is retained only as a historical snapshot and does not prove 19 current folders absent. Parent competition IDs, canonical Oracle joins and settlement truth remain unverified."}
    a.out_dir.mkdir(parents=True,exist_ok=True)
    with (a.out_dir/"selected50_identity_snapshot_reconciliation.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    (a.out_dir/"selected50_identity_snapshot_reconciliation.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    md=f"""# Selected-50 Identity Snapshot Reconciliation — 2026-10-26

**Status:** {summary['status']}. Research-only; production eligibility is NOT GRANTED.

## Evidence layers

- Provider ingestion run {EXPECTED_INGESTION}: SUCCESS_50_OF_50_SEASONS_INGESTED.
- Sanitized private archive QA run {EXPECTED_QA}, artifact {EXPECTED_ARTIFACT}, SHA-256 {EXPECTED_SHA}.
- Latest QA: 50/50 selected season IDs, 14,051 fixture rows, 14,051 unique season-fixture pairs, zero duplicates.
- Legacy Run 56: {legacy_exact} exact archive joins and {legacy_gap} no-exact joins. This is a historical snapshot and does not override later private season-folder evidence.
- Latest single-season snapshot rows: {summary['latest_season_fixture_rows_sum']:,}; primary-window rows: {summary['latest_season_primary_window_rows_sum']:,}. Legacy primary-window values are populated for {len(legacy_rows)} groups only and sum to {summary['legacy_primary_window_rows_sum_populated_groups_only']:,}; the scopes are not interchangeable.

## Identity and release findings

- Selected IDs are provider season IDs, not parent competition IDs.
- Canonical candidates requiring review: {candidate}; unresolved: {unresolved}; approved: 0.
- Parent competition IDs: 0/50 verified. Canonical fixture joins: 0/50. Canonical team joins: 0/50. Official settlement truth: 0/50.
- Point-in-time xG/odds provenance: 0/50 verified.
- Nonstandard eight-digit season-year tokens: {summary['nonstandard_8_digit_year_tokens']}.
- Zero primary-window rows in latest season snapshot: {', '.join(zero)}.

## Next steps

1. Reconcile canonical fixture/team identities using approved evidence; do not infer parent IDs from season IDs, names or aliases.
2. Reconcile completed-result status and official market settlement truth.
3. Keep missing point-in-time standings, xG and odds provenance missing.
4. Keep Combo blocked until target/settlement governance is resolved; keep M-1UP blocked until its independent event-truth gate passes.
5. Keep all Selected-50 outputs research-only and production-ineligible.

No network/API calls, provider credits, private-repository Actions or raw provider payloads were used by this audit.
"""
    (a.out_dir/"selected50_identity_snapshot_reconciliation.md").write_text(md,encoding="utf-8")
    print(json.dumps(summary,sort_keys=True))
if __name__=="__main__": main()
