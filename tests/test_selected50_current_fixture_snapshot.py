import json, tempfile, unittest
from pathlib import Path
from scripts.validate_selected50_current_fixture_snapshot import validate

class SnapshotValidatorTests(unittest.TestCase):
    def build(self):
        seasons=[{"selected_season_id":str(i),"http_status":200,"provider_success":True,"schedule_status":"ONE_PAGE_RESPONSE"} for i in range(50)]
        rows=[]
        for i in range(2):
            rows.append({"id":i+1,"selected_season_id":"1","competition_id":"1","homeID":10,"awayID":11,
                         "home_name":"Home","away_name":"Away","date_unix":100+i,"kickoff_utc":"2026-10-28T00:00:00+00:00",
                         "status":"incomplete" if i==0 else "complete","window_class":"FUTURE_14D" if i==0 else "RECENT_30D",
                         "no_home_away":0})
        return {"diagnostic":"BOUNDED_SELECTED50_CURRENT_FIXTURE_SNAPSHOT","selected_leagues":50,"requests_planned":50,
                "requests_attempted":50,"http_200_success":50,"request_failures":0,"seasons_needing_pagination":[],
                "production_eligibility":"NOT_GRANTED","betting_eligibility":"NOT_GRANTED","raw_provider_payload_persisted":False,
                "api_key_persisted":False,"production_ledger_written":False,"per_season":seasons,"fixture_rows":rows,
                "future_14d_fixture_rows":1,"recent_completed_30d_rows":1}
    def test_valid_snapshot_passes(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"snapshot.json";p.write_text(json.dumps(self.build()))
            self.assertEqual(validate(p)["status"],"PASS")
    def test_duplicate_match_id_fails(self):
        with tempfile.TemporaryDirectory() as td:
            d=self.build();d["fixture_rows"][1]["id"]=d["fixture_rows"][0]["id"]
            p=Path(td)/"snapshot.json";p.write_text(json.dumps(d))
            self.assertEqual(validate(p)["status"],"FAIL")
    def test_production_eligibility_must_remain_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            d=self.build();d["production_eligibility"]="APPROVED"
            p=Path(td)/"snapshot.json";p.write_text(json.dumps(d))
            self.assertEqual(validate(p)["status"],"FAIL")
if __name__=="__main__": unittest.main()
