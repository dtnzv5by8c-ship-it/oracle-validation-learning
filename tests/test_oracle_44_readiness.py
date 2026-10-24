import csv
import tempfile
import unittest
from pathlib import Path
from scripts.build_oracle_44_readiness import build


class ReadinessTests(unittest.TestCase):
    def test_verified_identity_is_partial_not_prediction_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fields = ["target_code","country","target_competition","provider_name","provider_season_id","season_label","catalogue_status","match_fetch_status","fixture_rows","duplicate_match_ids","cutoff_provenance"]
            with (root/"oracle_44_league_full_season_coverage.csv").open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
                for i in range(44):
                    w.writerow(dict(target_code=f"L{i}",country="X",target_competition="C",provider_name="P",provider_season_id="S",season_label="2026",catalogue_status="CANDIDATE_ONLY",match_fetch_status="PAGINATION_STOPPED_SHORT_PAGE",fixture_rows="1",duplicate_match_ids="0",cutoff_provenance="NOT_ESTABLISHED"))
            with (root/"oracle_44_league_candidate_crosswalk.csv").open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=["target_code","provider_name","provider_season_id","season_label"]); w.writeheader()
                for i in range(44): w.writerow(dict(target_code=f"L{i}",provider_name="P",provider_season_id="S",season_label="2026"))
            with (root/"oracle_44_league_sanitized_fixture_audit.csv").open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=["target_code","match_id","homeID","awayID","date_unix","status"]); w.writeheader()
                for i in range(44): w.writerow(dict(target_code=f"L{i}",match_id=f"M{i}",homeID="1",awayID="2",date_unix="1790000000",status="complete"))
            rows=build(root)
            self.assertEqual(len(rows),44)
            self.assertTrue(all(r["readiness_status"]=="PARTIAL" for r in rows))
            self.assertTrue(all(r["prediction_ready"]=="NO" for r in rows))

    def test_unmatched_alias_is_parked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            fields=["target_code","country","target_competition","provider_name","provider_season_id","season_label","catalogue_status","match_fetch_status","fixture_rows","duplicate_match_ids","cutoff_provenance"]
            with (root/"oracle_44_league_full_season_coverage.csv").open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
                for i in range(44):
                    w.writerow(dict(target_code=f"L{i}",country="X",target_competition="C",catalogue_status="NO_EXACT_ALIAS_MATCH" if i==0 else "CANDIDATE_ONLY",match_fetch_status="NOT_RUN" if i==0 else "PAGINATION_STOPPED_SHORT_PAGE",fixture_rows="0" if i==0 else "1",duplicate_match_ids="0",cutoff_provenance="NOT_ESTABLISHED"))
            with (root/"oracle_44_league_candidate_crosswalk.csv").open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=["target_code"]); w.writeheader()
                for i in range(44): w.writerow(dict(target_code=f"L{i}"))
            with (root/"oracle_44_league_sanitized_fixture_audit.csv").open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=["target_code","match_id","homeID","awayID","date_unix","status"]); w.writeheader()
                for i in range(1,44): w.writerow(dict(target_code=f"L{i}",match_id=f"M{i}",homeID="1",awayID="2",date_unix="1790000000",status="complete"))
            rows=build(root)
            self.assertEqual(rows[0]["readiness_status"],"PARKED_UNVERIFIED")
            self.assertEqual(rows[0]["prediction_ready"],"NO")


if __name__ == "__main__":
    unittest.main()
