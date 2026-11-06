import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MATRIX=ROOT/"reports/oracle-50-league-evidence-feature-readiness-2026-11-06.csv"
def load():
    with MATRIX.open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f))
def test_matrix_has_exactly_50_rows():
    rows=load(); assert len(rows)==50; assert {int(r["league_index"]) for r in rows}==set(range(1,51))
def test_fail_closed_statuses():
    rows=load(); assert all(r["overall_status"] in {"READY","PARTIAL","BLOCKED"} for r in rows); assert sum(r["overall_status"]=="READY" for r in rows)==0; assert sum(r["overall_status"]=="PARTIAL" for r in rows)==0; assert sum(r["overall_status"]=="BLOCKED" for r in rows)==50
def test_feature_gates_are_not_promoted():
    rows=load(); gated=["league_identity","kickoff_chronology","result_settlement","recent_form_3_5_8","home_away_form","h2h_pre_kickoff","goals_btts_overs","fixture_time_standings","xg_point_in_time","odds_point_in_time","omi_eligibility","visual_intelligence_eligibility"]
    for r in rows: assert all(r[c]=="BLOCKED" for c in gated)
if __name__=="__main__":
    test_matrix_has_exactly_50_rows(); test_fail_closed_statuses(); test_feature_gates_are_not_promoted(); print("PASS: 50-league evidence/feature readiness matrix is fail-closed and structurally valid")
