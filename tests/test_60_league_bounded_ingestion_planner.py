#!/usr/bin/env python3
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("planner",ROOT/"scripts/plan_60_league_bounded_ingestion.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def row(i):
    return {"league_id":f"L{i}","league_name":f"League {i}",
            "provider_league_id":str(1000+i),"provider_season_id":str(2000+i),
            "season_start":"2024-01-01","season_end":"current"}

def test_sixty_rows_plan_into_three_bounded_batches():
    errors,batches=m.plan([row(i) for i in range(60)],60,20)
    assert errors==[]
    assert len(batches)==3
    assert [b["season_count"] for b in batches]==[20,20,20]
    assert sum(len(b["provider_season_ids"]) for b in batches)==60

def test_duplicate_provider_season_blocks():
    rows=[row(i) for i in range(60)]
    rows[1]["provider_season_id"]=rows[0]["provider_season_id"]
    errors,_=m.plan(rows,60,20)
    assert any("duplicate_provider_season_id" in e for e in errors)

def test_wrong_scope_blocks():
    errors,_=m.plan([row(i) for i in range(59)],60,20)
    assert any("league_count=59" in e for e in errors)

def test_missing_provider_season_blocks():
    rows=[row(i) for i in range(60)]
    rows[4]["provider_season_id"]=""
    errors,_=m.plan(rows,60,20)
    assert any("missing_fields:provider_season_id" in e for e in errors)

if __name__=="__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
