#!/usr/bin/env python3
"""Regression test for snapshot-scoped Selected-50 identity reconciliation."""
import csv,json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts/build_selected50_identity_snapshot_reconciliation.py"
def rows(p):
    with p.open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f))
def main():
    with tempfile.TemporaryDirectory() as t:
        out=Path(t)
        subprocess.run([sys.executable,str(SCRIPT),"--out-dir",str(out)],cwd=ROOT,check=True,capture_output=True,text=True)
        rs=rows(out/"selected50_identity_snapshot_reconciliation.csv")
        s=json.loads((out/"selected50_identity_snapshot_reconciliation.json").read_text())
        assert len(rs)==50 and len({r["selected_id"] for r in rs})==50
        assert s["status"]=="PASS_SELECTED50_IDENTITY_SNAPSHOT_SCOPE_RECONCILIATION_RESEARCH_ONLY"
        assert s["latest_successful_season_folders"]==50
        assert s["latest_private_archive_fixture_rows_global"]==14051
        assert s["latest_season_fixture_rows_sum"]==14051
        assert s["latest_season_primary_window_rows_sum"]==5637
        assert s["legacy_run56_exact_joins"]==31 and s["legacy_run56_no_exact_joins"]==19
        assert s["candidate_mappings_requiring_review"]==22 and s["unresolved_mappings"]==28
        assert s["approved_mappings"]==0 and s["parent_competition_ids_verified"]==0
        assert s["canonical_fixture_joins_verified"]==s["canonical_team_joins_verified"]==0
        assert s["official_settlement_truth_verified"]==0
        assert s["xg_point_in_time_verified"]==s["odds_point_in_time_verified"]==0
        assert s["nonstandard_8_digit_year_tokens"]==33
        assert set(s["zero_primary_window_selected_ids"])=={"17326","17964"}
        assert s["network_calls_made"]==s["paid_provider_calls_made"]==0
        assert s["production_eligible"] is False and s["betting_eligible"] is False
        assert all(r["selected_id_type"]=="PROVIDER_SEASON_ID_NOT_PARENT_COMPETITION_ID" for r in rs)
        assert all(r["canonical_fixture_join_status"]=="NOT_VERIFIED" for r in rs)
        assert all(r["canonical_team_join_status"]=="NOT_VERIFIED" for r in rs)
        assert all(r["official_settlement_truth_status"]=="NOT_VERIFIED" for r in rs)
        assert all(r["production_eligible"]=="NO" for r in rs)
        assert sum(r["legacy_run56_archive_join_status"].startswith("EXACT_SELECTED_ID_TO_ARCHIVE_SEASON_ID") for r in rs)==31
        assert sum(r["legacy_run56_archive_join_status"].startswith("NO_EXACT_SELECTED_ID_TO_ARCHIVE_SEASON_ID_JOIN") for r in rs)==19
        print("PASS: 50 IDs, latest and legacy snapshot scopes separated, no parent-ID inference, production blocked.")
if __name__=="__main__": main()
