import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MATRIX=ROOT/"reports/oracle-50-league-evidence-feature-readiness-2026-11-06.csv"

def load():
    with MATRIX.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def test_matrix_has_exactly_50_rows():
    rows=load()
    assert len(rows)==50
    assert len({r["selected_id"] for r in rows})==50
    assert len({r["league"] for r in rows})==50

def test_fail_closed_statuses():
    rows=load()
    assert all(r["overall_status"] in {"READY","PARTIAL","BLOCKED"} for r in rows)
    assert sum(r["overall_status"]=="READY" for r in rows)==0
    assert sum(r["overall_status"]=="PARTIAL" for r in rows)==44
    assert sum(r["overall_status"]=="BLOCKED" for r in rows)==6

def test_acquisition_accounting():
    rows=load()
    assert sum(int(r["planned_seasons"]) for r in rows)==182
    assert sum(int(r["acquired_seasons"]) for r in rows)==162
    assert sum(int(r["task_coverage_pct"])==100 for r in rows)==44
    assert sum(int(r["task_coverage_pct"])==0 for r in rows)==6

def test_omi_and_visual_intelligence_remain_blocked():
    rows=load()
    assert all(r["omi_eligibility"]=="BLOCKED" for r in rows)
    assert all(r["visual_intelligence_eligibility"]=="BLOCKED" for r in rows)

if __name__=="__main__":
    test_matrix_has_exactly_50_rows()
    test_fail_closed_statuses()
    test_acquisition_accounting()
    test_omi_and_visual_intelligence_remain_blocked()
    print("PASS: 50-league evidence/feature readiness matrix is structurally valid and fail-closed")
