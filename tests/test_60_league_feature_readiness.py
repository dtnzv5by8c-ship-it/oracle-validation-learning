#!/usr/bin/env python3
import csv, tempfile, json
from pathlib import Path
import importlib.util
p=Path("scripts/validate_60_league_feature_readiness.py")
spec=importlib.util.spec_from_file_location("m",p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

FEATURES=list(m.FEATURES)
def row(i, ready=True):
    r={"league_id":f"L{i}","league_name":f"League {i}",
       "provider_league_id":f"P{i}","provider_league_name":f"Provider {i}",
       "season_start":"2024","season_end":"current"}
    r.update({f:"PASS" if ready else "" for f in FEATURES})
    return r

rows=[row(i) for i in range(60)]
assert m.validate(rows)==[]
bad=[row(i) for i in range(59)]
assert any("league_count" in e for e in m.validate(bad))
bad=[row(i) for i in range(60)]; bad[1]["league_id"]=bad[0]["league_id"]
assert "duplicate_league_id" in m.validate(bad)
bad=[row(i) for i in range(60)]; bad[3]["xg_goals"]=""
assert any("xg_goals" in e for e in m.validate(bad))
bad=[row(i) for i in range(60)]; bad[4]["season_start"]="2023"
assert "season_start_before_2024" in m.validate(bad)
bad=[row(i) for i in range(60)]; bad[5]["provider_league_id"]=""
assert any("provider_league_id" in e for e in m.validate(bad))
print("PASS: 60-league feature readiness matrix regression tests")
