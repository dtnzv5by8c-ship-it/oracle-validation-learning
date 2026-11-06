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
       "provider_season_id":f"S{i}","season_start":"2024","season_end":"current"}
    r.update({f:"PASS" if ready else "" for f in FEATURES})
    return r

rows=[row(i) for i in range(50)]
assert m.validate(rows,50)==[]
bad=[row(i) for i in range(49)]
assert any("league_count" in e for e in m.validate(bad,50))
bad=[row(i) for i in range(50)]; bad[1]["league_id"]=bad[0]["league_id"]
assert "duplicate_league_id" in m.validate(bad,50)
bad=[row(i) for i in range(50)]; bad[3]["xg_goals"]=""
assert any("xg_goals" in e for e in m.validate(bad,50))
bad=[row(i) for i in range(50)]; bad[4]["season_start"]="2023"
assert "season_start_must_be_2024" in m.validate(bad,50)
bad=[row(i) for i in range(50)]; bad[5]["provider_league_id"]=""
assert any("provider_league_id" in e for e in m.validate(bad,50))
print("PASS: 50-league feature readiness matrix regression tests")

# Provider-season identity is mandatory and unique.
bad=[row(i) for i in range(50)]; bad[6]["provider_season_id"]=""
assert "blank_provider_season_id" in m.validate(bad,50)
bad=[row(i) for i in range(50)]; bad[7]["provider_season_id"]=bad[0]["provider_season_id"]
assert "duplicate_provider_season_id" in m.validate(bad,50)
bad=[row(i) for i in range(50)]; bad[8]["provider_league_id"]=bad[0]["provider_league_id"]
assert "duplicate_provider_league_id" in m.validate(bad,50)
print("PASS: provider identity hardening cases")
