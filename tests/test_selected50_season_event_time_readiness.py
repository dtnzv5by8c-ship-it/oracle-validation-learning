import json
import unittest
from scripts.audit_selected50_season_event_time_readiness import (
    statuses, summarize, validate_report, build_rows
)

def report():
    return {
        "status":"QA_COMPLETE_REVIEW_REQUIRED","primary_window_start":"2025-03-20",
        "primary_window_end":"2026-09-20","audit_date_utc":"2026-10-30",
        "official_settlement_truth_verified":False,"production_eligible":False,
        "selected_leagues_in_manifest":50,"historical_season_manifest_rows":200,
        "primary_window_archive_match_records":98,"total_match_records":600,"total_team_records":3200,
        "primary_window_archive_unique_provider_match_ids":98,
        "primary_window_provider_status_counts":{"complete":98,"incomplete":0},
        "incomplete_status_records_with_past_kickoff":5,"complete_status_records_with_future_kickoff":0,
        "noncomplete_status_records_with_parseable_score_pair":10,
        "noncomplete_status_records_with_zero_zero_score_pair":10,
        "noncomplete_status_records_with_nonzero_score_pair":0,
        "complete_status_records_with_zero_zero_score_pair":20
    }

def seasons():
    rows=[]
    for i in range(50):
        for j in range(4):
            cur=j==0
            if cur and i==0:
                first,last,pw,sc="2026-10-10","2027-05-01",0,{"complete":1,"incomplete":2}
            elif cur:
                first,last,pw,sc="2026-01-01","2026-12-01",2,{"complete":3}
            else:
                first,last,pw,sc="2024-01-01","2024-12-01",0,{"complete":3}
            rows.append({"season_id":str(i*4+j+1),"country":f"C{i}","competition_name":f"L{i}",
                "selected_current_season":str(cur),"ingestion_status":"INGESTED","match_records":"3","team_records":"16",
                "primary_window_match_records":str(pw),"primary_window_unique_provider_match_ids":str(pw),
                "primary_window_complete_status_records":str(pw),"primary_window_noncomplete_status_records":"0",
                "duplicate_match_ids_within_season":"0","incomplete_status_records_with_past_kickoff":"1" if cur and i==1 else "0",
                "complete_status_records_with_future_kickoff":"0","suspended_status_records_with_parseable_score_pair":"0",
                "provider_status_counts_json":json.dumps(sc),"kickoff_date_min":first,"kickoff_date_max":last,
                "table_payload_present":"True","season_stats_payload_present":"True","matches_file_present":"True",
                "teams_file_present":"True","tables_file_present":"True","season_stats_file_present":"True"})
    return rows

class EventTimeTests(unittest.TestCase):
    def setUp(self):
        self.r=report(); self.start,self.end,self.audit=validate_report(self.r)
    def test_future_only_is_not_missing_archive(self):
        rows=build_rows(seasons(),self.r,self.start,self.end)
        fut=next(x for x in rows if x["country"]=="C0" and x["selected_current_season"])
        self.assertEqual(fut["coverage_bucket"],"FUTURE_ONLY_AFTER_PRIMARY_WINDOW")
        s=summarize(self.r,rows,self.start,self.end,self.audit)
        self.assertEqual(s["current_season_coverage_buckets"]["FUTURE_ONLY_AFTER_PRIMARY_WINDOW"],1)
        self.assertEqual(s["current_season_coverage_buckets"]["INTERSECTS_PRIMARY_WINDOW"],49)
    def test_duplicate_season_id_rejected(self):
        rows=seasons(); rows[1]["season_id"]=rows[0]["season_id"]
        with self.assertRaises(ValueError): build_rows(rows,self.r,self.start,self.end)
    def test_status_totals_must_reconcile(self):
        rows=seasons(); rows[0]["provider_status_counts_json"]='{"complete":2}'
        with self.assertRaises(ValueError): build_rows(rows,self.r,self.start,self.end)
    def test_primary_window_status_counts_must_reconcile(self):
        rows=seasons(); rows[1]["primary_window_noncomplete_status_records"]="1"
        with self.assertRaises(ValueError): build_rows(rows,self.r,self.start,self.end)
    def test_missing_archive_payload_rejected(self):
        rows=seasons(); rows[2]["teams_file_present"]="False"
        with self.assertRaises(ValueError): build_rows(rows,self.r,self.start,self.end)
    def test_invalid_status_counts_rejected(self):
        with self.assertRaises(ValueError): statuses('{"complete":-1}')
    def test_past_incomplete_is_not_settlement_truth(self):
        rows=build_rows(seasons(),self.r,self.start,self.end)
        s=summarize(self.r,rows,self.start,self.end,self.audit)
        self.assertEqual(s["incomplete_status_past_kickoff"]["current_selected_seasons"],1)
        self.assertFalse(s["official_settlement_truth_verified"])
        self.assertFalse(s["production_eligible"])
    def test_settlement_gate_must_remain_false(self):
        r=dict(self.r); r["official_settlement_truth_verified"]=True
        with self.assertRaises(ValueError): validate_report(r)

if __name__=="__main__": unittest.main()
