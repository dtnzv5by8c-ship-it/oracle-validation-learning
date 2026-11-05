import csv, json, tempfile, unittest
from pathlib import Path
import importlib.util

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts"/"validate_omi_universe_readiness.py"
s=importlib.util.spec_from_file_location("v",P); v=importlib.util.module_from_spec(s); s.loader.exec_module(v)

class TestOmiUniverseReadiness(unittest.TestCase):
    def test_manifest_requires_exact_governed_count_and_unique_ids(self):
        rows=[{"league_id":str(i),"league_name":f"L{i}","season":"2024"} for i in range(60)]
        self.assertEqual(v.validate_manifest(rows,60),[])
        rows[1]["league_id"]="0"
        self.assertTrue(v.validate_manifest(rows,60))

    def test_omi_passes_identity_temporal_and_probability_contract(self):
        row={k:"" for k in v.REQUIRED}
        row.update({
          "Fixture Date":"2026-11-05T18:00:00+00:00","League":"L1","Fixture":"A v B",
          "Fixture ID":"F1","Provider Season ID":"S1","Home Team ID":"H","Away Team ID":"A",
          "History Cutoff UTC":"2026-11-05T12:00:00+00:00","Recent Form (5)":"WDLWW",
          "League Position":"2 / 8","H2H Last-5":"2W-2D-1L",
          "Home Expected Goals Lambda":"1.6","Away Expected Goals Lambda":"1.1",
          "Research Over 1,5 %":"71.2","Research Over 2,5 %":"54.1",
          "BTTS Yes":"63.5","retrieved_utc":"2026-11-05T17:00:00+00:00",
          "Production Eligible":"FALSE","Betting Eligible":"FALSE"
        })
        e,stats=v.validate_omi([row],{"S1"})
        self.assertEqual(e,[])

    def test_future_cutoff_and_bad_probability_block(self):
        row={k:"" for k in v.REQUIRED}
        row.update({"Fixture ID":"F1","Provider Season ID":"S1","Home Team ID":"H","Away Team ID":"A",
                    "Fixture Date":"2026-11-05T18:00:00+00:00","History Cutoff UTC":"2026-11-05T19:00:00+00:00",
                    "BTTS Yes":"101","retrieved_utc":"2026-11-05T17:00:00+00:00"})
        e,_=v.validate_omi([row],{"S1"})
        self.assertTrue(any("history_cutoff" in x for x in e))
        self.assertTrue(any("bad_probability" in x for x in e))

if __name__=="__main__": unittest.main()
