#!/usr/bin/env python3
"""Build a sanitized Selected-50 identity, freshness and market-gate matrix."""
from __future__ import annotations
import csv,json
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"audit-output"; OUT.mkdir(parents=True,exist_ok=True)
CROSSWALK=ROOT/"reports"/"oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r17.csv"
AUDIT_DATE=datetime.now(timezone.utc).date()
def read_csv(path):
    if not path.is_file(): raise AssertionError(f"Missing evidence table: {path}")
    with path.open(encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
def build_matrix(coverage,quarantine,crosswalk,audit_date=AUDIT_DATE):
    assert len(coverage)==len(quarantine)==len(crosswalk)==50
    def index(rows,key):
        out={}
        for r in rows:
            k=str(r.get(key,"")).strip()
            assert k and k not in out, f"Blank/duplicate key {key}: {k}"
            out[k]=r
        return out
    cov=index(coverage,"selected_id"); qua=index(quarantine,"selected_season_id")
    # This legacy field is used only as the selected-ID row reference, never as a parent competition ID.
    xw=index(crosswalk,"footystats_provider_id")
    assert set(cov)==set(qua)==set(xw),"Selected-ID sets do not match across evidence layers"
    result=[]
    for sid in sorted(cov,key=int):
        c,q,x=cov[sid],qua[sid],xw[sid]
        assert c["crosswalk_status"]==x["crosswalk_status"]==q["source_crosswalk_status"],f"Crosswalk mismatch {sid}"
        assert c["provider_parent_competition_id_status"]==x["provider_parent_competition_id_status"]
        last=str(x.get("current_upcoming_fixture_schedule_last_date","")).strip()
        end=str(x.get("upcoming_fixture_window_end","")).strip()
        days_last=(audit_date-date.fromisoformat(last)).days if last else ""
        days_end=(audit_date-date.fromisoformat(end)).days if end else ""
        parent=x.get("provider_parent_competition_id_status","")
        fixture=c.get("canonical_fixture_join_status",""); team=c.get("canonical_team_join_status",""); truth=c.get("official_settlement_truth_status","")
        assert parent=="NOT_EXPOSED_BY_CATALOGUE"
        assert fixture==team==truth=="NOT_VERIFIED"
        result.append({
          "selected_season_id":sid,"audit_date":audit_date.isoformat(),"country":c.get("country",""),"competition":c.get("competition",""),
          "canonical_code_candidate":c.get("crosswalk_candidate_code",""),"crosswalk_status":c.get("crosswalk_status",""),
          "crosswalk_candidate_basis":x.get("candidate_basis",""),"latest_selected_id_semantics":c.get("selected_id_semantics_status",""),
          "historical_crosswalk_semantics_snapshot":x.get("selected_id_semantics_status",""),
          "historical_archive_season_id_match":x.get("selected_id_exact_archive_season_id_match",""),
          "parent_competition_id_status":parent,"parent_id_schema_evidence":x.get("provider_parent_competition_id_schema_evidence",""),
          "private_season_fixture_rows":c.get("provider_season_fixture_records",""),"private_season_team_rows":c.get("provider_season_team_records",""),
          "latest_private_archive_selected_id_set_match":x.get("latest_private_archive_selected_id_set_match",""),
          "latest_private_archive_seasons_global":x.get("latest_private_archive_seasons_audited",""),
          "latest_private_archive_fixture_rows_global":x.get("latest_private_archive_fixture_rows",""),
          "latest_private_archive_unique_pairs_global":x.get("latest_private_archive_unique_season_fixture_pairs",""),
          "latest_private_archive_duplicate_pairs_global":x.get("latest_private_archive_duplicate_pairs",""),
          "latest_private_archive_parent_competition_ids_global":x.get("latest_private_archive_parent_competition_id_rows",""),
          "canonical_fixture_join_status":fixture,"canonical_team_join_status":team,"official_settlement_truth_status":truth,
          "current_feed_label_rows":q.get("current_feed_display_label_rows",""),"current_feed_distinct_league_ids":q.get("current_feed_distinct_league_id_count",""),
          "current_feed_country_field_present":q.get("current_feed_country_field_present",""),"current_feed_exact_league_id_allowlist":q.get("current_feed_exact_league_id_allowlist",""),
          "provider_season_to_feed_bridge_status":q.get("provider_season_to_feed_bridge_status",""),
          "current_fixture_coverage_status":x.get("current_fixture_coverage_status",""),"freshness_status":x.get("freshness_status",""),
          "current_source_manifest_generated_utc":x.get("current_source_manifest_generated_utc",""),
          "current_reconciliation_generated_utc":x.get("current_reconciliation_generated_utc",""),
          "current_data_snapshot_consistency_status":x.get("current_data_snapshot_consistency_status",""),
          "immutable_feature_snapshot_manifest_rows":x.get("immutable_feature_snapshot_manifest_row_count",""),
          "schedule_rows_global":x.get("current_upcoming_fixture_schedule_rows",""),"schedule_last_fixture_date":last,
          "schedule_manifest_window_end":end,"days_since_last_fixture_date":days_last,"days_since_schedule_window_end":days_end,
          "recent_form_both_teams_prior_rows":c.get("provider_recent_form5_both_teams_prior_count",""),
          "standings_status":c.get("provider_standings_payload_status",""),
          "xg_point_in_time_provenance":c.get("provider_xg_point_in_time_provenance",""),
          "odds_point_in_time_provenance":c.get("provider_odds_point_in_time_provenance",""),
          "latest_archive_odds_timestamp_rows_global":x.get("latest_private_archive_odds_timestamp_rows",""),
          "latest_archive_xg_provenance_global":x.get("latest_private_archive_xg_pit_provenance",""),
          "latest_archive_odds_provenance_global":x.get("latest_private_archive_odds_pit_provenance",""),
          "BTTS_YES_readiness":c.get("BTTS_YES_readiness",""),"DOUBLE_CHANCE_readiness":c.get("DOUBLE_CHANCE_readiness",""),
          "COMBO_readiness":"BLOCKED_TARGET_SETTLEMENT_DEFINITION_MISMATCH","M1UP_readiness":c.get("M1UP_readiness",""),
          "governed_fixture_report_status":"STALE_SCHEDULE_AND_IDENTITY_GATES; DO NOT ISSUE NEW SLATE",
          "production_eligible":"NO","research_only":"YES","raw_feed_examples_exported":"NO"})
    return result
def build_fixture_gate(summary):
    return {
      "status":"BLOCKED_NO_CURRENT_GOVERNED_FIXTURE_SLATE","audit_date":summary.get("audit_date", AUDIT_DATE.isoformat()),"selected_groups":50,
      "schedule_rows_snapshot":summary["schedule_rows_global"],"schedule_last_fixture_date":summary["schedule_last_fixture_date"],
      "schedule_manifest_window_end":summary["schedule_manifest_window_end"],"days_since_last_fixture_date":summary["days_since_last_fixture_date"],
      "days_since_schedule_window_end":summary["days_since_schedule_window_end"],"current_fixture_rows_emitted":0,
      "prediction_rows_emitted":0,"unsupported_predictions_emitted":0,"missing_fields_filled":0,
      "production_eligible":False,"research_only":True,
      "reason_codes":["STALE_SCHEDULE","CURRENT_FEED_IDENTITY_UNVERIFIED","CANONICAL_FIXTURE_TEAM_JOINS_UNVERIFIED","OFFICIAL_SETTLEMENT_TRUTH_UNVERIFIED","POINT_IN_TIME_STANDINGS_XG_ODDS_UNVERIFIED"],
      "market_gates":{"BTTS":"BLOCKED_IDENTITY_SETTLEMENT_AND_FEATURE_PROVENANCE","DOUBLE_CHANCE":"BLOCKED_IDENTITY_SETTLEMENT_AND_FEATURE_PROVENANCE",
        "COMBO":"BLOCKED_TARGET_SETTLEMENT_DEFINITION_MISMATCH","M1UP":"BLOCKED_EVENT_TRUTH_STALE"},
      "no_staking_or_betting_recommendation":True}
def main():
    coverage=read_csv(OUT/"selected50_latest_private_archive_coverage_matrix.csv")
    quarantine=read_csv(OUT/"selected50_current_feed_identity_quarantine.csv")
    crosswalk=read_csv(CROSSWALK); rows=build_matrix(coverage,quarantine,crosswalk)
    assert len({r["selected_season_id"] for r in rows})==50 and all(r["production_eligible"]=="NO" and r["raw_feed_examples_exported"]=="NO" for r in rows)
    statuses=Counter(r["crosswalk_status"] for r in rows); archive=Counter(r["historical_archive_season_id_match"] for r in rows)
    hits=sum(int(r["current_feed_label_rows"] or 0)>0 for r in rows)
    ambiguous=sum(int(r["current_feed_distinct_league_ids"] or 0)>1 for r in rows)
    single=sum(int(r["current_feed_label_rows"] or 0)>0 and int(r["current_feed_distinct_league_ids"] or 0)==1 for r in rows)
    none=sum(int(r["current_feed_label_rows"] or 0)==0 for r in rows)
    verified=lambda v:"VERIFIED" in str(v) and "NOT_VERIFIED" not in str(v) and "UNVERIFIED" not in str(v)
    s={"status":"PASS_SANITIZED_SELECTED50_GOVERNED_READINESS_MATRIX_RESEARCH_ONLY","audit_date":AUDIT_DATE.isoformat(),"selected_groups":50,
      "crosswalk_status_counts":dict(statuses),"historical_archive_season_id_match_counts":dict(archive),
      "current_feed_groups_with_label_rows":hits,"current_feed_groups_with_multiple_league_id_collisions":ambiguous,
      "current_feed_groups_with_single_label_id":single,"current_feed_groups_with_no_label_rows":none,
      "current_feed_country_field_present_groups":sum(r["current_feed_country_field_present"]=="YES" for r in rows),
      "current_feed_exact_league_id_allowlist_groups":sum(r["current_feed_exact_league_id_allowlist"]=="YES" for r in rows),
      "provider_season_to_feed_bridge_verified_groups":sum(verified(r["provider_season_to_feed_bridge_status"]) for r in rows),
      "parent_competition_ids_verified":sum(r["parent_competition_id_status"]=="VERIFIED" for r in rows),
      "latest_private_archive_seasons_global":rows[0]["latest_private_archive_seasons_global"],
      "latest_private_archive_fixture_rows_global":rows[0]["latest_private_archive_fixture_rows_global"],
      "latest_private_archive_unique_pairs_global":rows[0]["latest_private_archive_unique_pairs_global"],
      "latest_private_archive_duplicate_pairs_global":rows[0]["latest_private_archive_duplicate_pairs_global"],
      "latest_private_archive_parent_competition_ids_global":rows[0]["latest_private_archive_parent_competition_ids_global"],
      "canonical_fixture_joins_verified":sum(r["canonical_fixture_join_status"]=="VERIFIED" for r in rows),
      "canonical_team_joins_verified":sum(r["canonical_team_join_status"]=="VERIFIED" for r in rows),
      "official_settlement_truth_verified":sum(r["official_settlement_truth_status"]=="VERIFIED" for r in rows),
      "current_fixture_coverage_status_counts":dict(Counter(r["current_fixture_coverage_status"] for r in rows)),
      "freshness_status_counts":dict(Counter(r["freshness_status"] for r in rows)),
      "schedule_rows_global":rows[0]["schedule_rows_global"],"schedule_last_fixture_date":rows[0]["schedule_last_fixture_date"],
      "schedule_manifest_window_end":rows[0]["schedule_manifest_window_end"],"days_since_last_fixture_date":rows[0]["days_since_last_fixture_date"],
      "days_since_schedule_window_end":rows[0]["days_since_schedule_window_end"],
      "current_source_manifest_generated_utc":rows[0]["current_source_manifest_generated_utc"],
      "current_reconciliation_generated_utc":rows[0]["current_reconciliation_generated_utc"],
      "immutable_feature_snapshot_manifest_rows":rows[0]["immutable_feature_snapshot_manifest_rows"],
      "latest_archive_odds_timestamp_rows_global":rows[0]["latest_archive_odds_timestamp_rows_global"],
      "xg_point_in_time_provenance_verified":sum(verified(r["xg_point_in_time_provenance"]) for r in rows),
      "odds_point_in_time_provenance_verified":sum(verified(r["odds_point_in_time_provenance"]) for r in rows),
      "production_eligible_rows":0,"raw_feed_examples_exported":False,"network_calls_made":0,"paid_provider_calls_made":0,
      "limitations":["The 31/19 historical archive season-ID split is from crosswalk snapshot r17 and is separate from latest private archive QA, which reports all 50 selected season folders.",
      "The catalogue does not expose a parent competition ID; selected/season IDs are not promoted to parent IDs.",
      f"Current schedule evidence is stale: last fixture date {rows[0]['schedule_last_fixture_date']} and manifest window end {rows[0]['schedule_manifest_window_end']}, both before the {s['audit_date']} audit date.",
      "Canonical fixture/team joins and official settlement truth remain unverified; xG/odds point-in-time provenance is unverified and no ROI benchmark is approved.",
      "Combo remains blocked by target/settlement mismatch; M-1UP remains blocked by its independent event-truth gate."]}
    fixture_gate=build_fixture_gate(s); s["governed_fixture_report_gate_status"]=fixture_gate["status"]; s["governed_fixture_rows_emitted"]=0
    with (OUT/"selected50_governed_readiness_matrix.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (OUT/"selected50_governed_readiness_summary.json").write_text(json.dumps(s,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    (OUT/"selected50_governed_fixture_report_gate.json").write_text(json.dumps(fixture_gate,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    gate_lines=[f"# Governed Fixture Report Gate — {s['audit_date']}","","Status: BLOCKED_NO_CURRENT_GOVERNED_FIXTURE_SLATE.",
      "No fixture or prediction rows were emitted because the schedule snapshot is stale and identity, settlement and point-in-time feature gates remain unresolved.","",
      f"- Schedule rows in snapshot: {fixture_gate['schedule_rows_snapshot']}",
      f"- Last fixture date in snapshot: {fixture_gate['schedule_last_fixture_date']}",
      f"- Schedule manifest window end: {fixture_gate['schedule_manifest_window_end']}",
      f"- Days since last fixture date: {fixture_gate['days_since_last_fixture_date']}; days since manifest window end: {fixture_gate['days_since_schedule_window_end']}.",
      "- Fixture rows emitted: 0; prediction rows emitted: 0; unsupported predictions emitted: 0; missing fields filled: 0.",
      "- BTTS and Double Chance blocked pending identity/settlement/point-in-time evidence; Combo blocked by target/settlement mismatch; M-1UP blocked by stale event truth.",
      "- Production eligibility: NO. Research-only gate report, not a betting recommendation."]
    (OUT/"selected50_governed_fixture_report_gate.md").write_text("\n".join(gate_lines)+"\n",encoding="utf-8")
    lines=[f"# Selected-50 Governed Readiness Matrix — {s['audit_date']}","","Status: PASS_SANITIZED_SELECTED50_GOVERNED_READINESS_MATRIX_RESEARCH_ONLY.",
      "No-network reconciliation of existing sanitized evidence. Raw feed examples are excluded and no production eligibility is granted.","","## Identity and archive scope","",
      f"- Selected IDs: {len(rows)}; crosswalk review candidates: {statuses.get('CANDIDATE_REQUIRES_HUMAN_REVIEW_NOT_APPROVED',0)}; unresolved: {statuses.get('UNRESOLVED_NO_EXACT_OR_EXPLICIT_ALIAS',0)}; approved: {sum(r['crosswalk_status']=='APPROVED' for r in rows)}.",
      f"- Historical r17 archive-ID snapshot: {archive.get('YES',0)} exact season-ID matches and {archive.get('NO',0)} no exact match. Latest private archive QA separately reports {s['latest_private_archive_seasons_global']} seasons and {s['latest_private_archive_fixture_rows_global']} fixture rows.",
      f"- Parent competition IDs exposed: {s['parent_competition_ids_verified']}; canonical fixture joins verified: {s['canonical_fixture_joins_verified']}; team joins verified: {s['canonical_team_joins_verified']}; official settlement truth verified: {s['official_settlement_truth_verified']}.","","## Current feed and schedule","",
      f"- Feed labels found for {hits} groups; {ambiguous} have multiple league-ID collisions; {single} have a single label/ID; {none} have no label rows.",
      f"- Country retained: {s['current_feed_country_field_present_groups']}/50; exact league-ID allowlist: {s['current_feed_exact_league_id_allowlist_groups']}/50; provider-season-to-feed bridges verified: {s['provider_season_to_feed_bridge_verified_groups']}/50.",
      f"- Schedule snapshot: {s['schedule_rows_global']} rows; last fixture date {s['schedule_last_fixture_date']}; manifest window end {s['schedule_manifest_window_end']}; {s['days_since_last_fixture_date']} days since last fixture date and {s['days_since_schedule_window_end']} days since window end at audit date. This is stale, not a current slate.",
      f"- Source manifest: {s['current_source_manifest_generated_utc']}; reconciliation: {s['current_reconciliation_generated_utc']}; immutable feature snapshot rows: {s['immutable_feature_snapshot_manifest_rows']}.","","## Feature and market gates","",
      "- Recent-form counts are archive field-presence evidence, not proof of canonical team joins or fully point-in-time correctness.",
      "- Standings are not verified as of kickoff; xG lacks as-of timestamps; odds lacks odds timestamps. No odds/ROI benchmark is approved.",
      "- BTTS and Double Chance remain research-only; Combo and M-1UP remain blocked. All 50 rows have production_eligible=NO.",
      "- No network/API calls or provider credits were used; no raw feed examples were exported.","","## Next action","",
      "Review the 22 candidate canonical mappings against approved authoritative evidence; keep 28 unresolved mappings unresolved. Repair/refresh current feed and immutable feature snapshot evidence, then reconcile official settlement truth and point-in-time inputs before producing a new governed slate.","","Production remains NOT_GRANTED. Research-only; not approved for betting."]
    (OUT/"selected50_governed_readiness_report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({k:s[k] for k in ["status","selected_groups","crosswalk_status_counts","historical_archive_season_id_match_counts","current_feed_groups_with_label_rows","current_feed_groups_with_multiple_league_id_collisions","current_feed_groups_with_no_label_rows","parent_competition_ids_verified","canonical_fixture_joins_verified","canonical_team_joins_verified","official_settlement_truth_verified","schedule_last_fixture_date","days_since_last_fixture_date","xg_point_in_time_provenance_verified","odds_point_in_time_provenance_verified","governed_fixture_report_gate_status","governed_fixture_rows_emitted","production_eligible_rows","network_calls_made","paid_provider_calls_made"]},sort_keys=True))
if __name__=="__main__": main()
