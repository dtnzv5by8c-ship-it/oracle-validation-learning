import importlib.util, unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"scripts"/"validate_60_league_registry_admission.py"
s=importlib.util.spec_from_file_location("v60",P); v=importlib.util.module_from_spec(s); s.loader.exec_module(v)

def registry(n=60):
    seasons=[]
    for i in range(n):
        seasons.append({"provider_league_name":f"L{i}","provider_season_label":"2024","provider_season_id":str(1000+i)})
    return {"provider_league_count":n,"seasons":seasons}

class Test60LeagueRegistryAdmission(unittest.TestCase):
    def test_exact_60_passes(self):
        self.assertEqual(v.validate_registry(registry(60),60),[])
    def test_49_cannot_be_promoted_to_60(self):
        errors=v.validate_registry(registry(49),60)
        self.assertTrue(any("provider_league_count" in e for e in errors))
        self.assertTrue(any("unique_provider_leagues" in e for e in errors))
    def test_duplicate_season_ids_block(self):
        x=registry(60); x["seasons"][1]["provider_season_id"]=x["seasons"][0]["provider_season_id"]
        self.assertTrue(any("duplicate_or_blank_provider_season_id" in e for e in v.validate_registry(x,60)))

if __name__=="__main__": unittest.main()
