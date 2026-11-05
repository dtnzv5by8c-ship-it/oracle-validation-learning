import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"scripts"/"validate_gateway_receipt.py"
s=importlib.util.spec_from_file_location("g",P); g=importlib.util.module_from_spec(s); s.loader.exec_module(g)

class TestGatewayReceipt(unittest.TestCase):
    def receipt(self):
        return {"gateway_repo":"dtnzv5by8c-ship-it/oracle-football-data","workflow_run_id":"123456789",
        "governed_manifest_sha":"a"*40,"archive_release_tag":"research-60league-footystats-history-123456789",
        "archive_sha256":"a"*64,"provider":"FootyStats","provider_request_count":120,
        "governed_league_count":60,"history_start":"2024-01-01","history_end":"2026-11-05",
        "raw_payloads_private_only":True,"production_eligible":False,"betting_eligible":False,
        "status":"GATEWAY_RECEIPT_VERIFIED"}
    def test_valid_receipt_passes(self): self.assertEqual(g.validate_receipt(self.receipt(),60),[])
    def test_wrong_universe_blocks(self):
        r=self.receipt(); r["governed_league_count"]=49
        self.assertTrue(any("governed_league_count" in x for x in g.validate_receipt(r,60)))
    def test_public_or_production_receipt_blocks(self):
        r=self.receipt(); r["raw_payloads_private_only"]=False
        self.assertIn("raw_payloads_not_private_only",g.validate_receipt(r,60))
        r=self.receipt(); r["production_eligible"]=True
        self.assertIn("production_must_remain_false",g.validate_receipt(r,60))
if __name__=="__main__": unittest.main()
