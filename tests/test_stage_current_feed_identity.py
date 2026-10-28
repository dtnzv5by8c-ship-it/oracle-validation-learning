import json, tempfile, unittest
from pathlib import Path
from scripts.stage_current_feed_identity import run

class OfflineIdentityStagingTests(unittest.TestCase):
    def test_stages_only_exact_approved_id_country_and_writes_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); inp=root/"in.jsonl"; allow=root/"allow.json"; out=root/"out"
            rows=[
              {"canonical_competition_code":"ENG_E0","league_id":"17","country":"England","league_name":"Premier League"},
              {"canonical_competition_code":"ENG_E0","league_id":"522","country":"Ghana","league_name":"Premier League"},
              {"canonical_competition_code":"GER_D1","league_id":"35","league_name":"Bundesliga"},
              {"canonical_competition_code":"ENG_E0","league_id":"17","country":"Scotland","league_name":"Premier League"},
            ]
            inp.write_text("".join(json.dumps(x)+"\\n" for x in rows),encoding="utf-8")
            allow.write_text(json.dumps({"entries":[
              {"canonical_competition_code":"ENG_E0","status":"APPROVED","league_id":"17","country":"England"}
            ]}),encoding="utf-8")
            m=run(inp,allow,out)
            self.assertEqual((m["input_rows"],m["accepted_rows"],m["quarantined_rows"]),(4,1,3))
            self.assertEqual(m["network_calls_made"],0)
            self.assertFalse(m["production_ledger_written"])
            self.assertEqual(json.loads((out/"manifest.json").read_text())["accepted_rows"],1)
            accepted=[json.loads(x) for x in (out/"accepted.jsonl").read_text().splitlines()]
            self.assertEqual(accepted[0]["identity_audit"]["reason"],"EXACT_APPROVED_ID_AND_COUNTRY_MATCH")
    def test_duplicate_allowlist_code_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); inp=root/"in.jsonl"; allow=root/"allow.json"
            inp.write_text("",encoding="utf-8")
            allow.write_text(json.dumps({"entries":[
              {"canonical_competition_code":"ENG_E0"},{"canonical_competition_code":"ENG_E0"}
            ]}),encoding="utf-8")
            with self.assertRaises(ValueError): run(inp,allow,root/"out")
if __name__=="__main__": unittest.main()
