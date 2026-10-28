import contextlib
import csv
import io
import json
import sys
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from scripts.audit_selected50_cross_provider_fixture_joins import main, timestamp


class CrossProviderFixtureJoinAuditTests(unittest.TestCase):
    def run_audit(self, *, ledger_exact=False, current_status="incomplete", current_finished=False,
                  current_home_goals="", current_away_goals="", footy_status="incomplete",
                  footy_home_goals="", footy_away_goals="", include_current=True):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            archive=root/"archive.zip"; manifest=root/"manifest.md"
            crosswalk=root/"crosswalk.csv"; current=root/"current_matches.csv"
            ledger=root/"historical_matches.csv"; out=root/"out"
            kickoff=datetime(2026,10,30,18,0,tzinfo=timezone.utc)
            unix=int(kickoff.timestamp())
            match={"id":"fs-1","home_name":"Home FC","away_name":"Away FC","date_unix":unix,
                   "status":footy_status,"homeGoalCount":footy_home_goals,"awayGoalCount":footy_away_goals}
            with zipfile.ZipFile(archive,"w") as zf:
                zf.writestr("private-package/seasons/1/matches.json",json.dumps([match]))
            manifest_lines=["| row | selected_season_id | country | competition |"]
            manifest_lines.extend(f"| {i} | {i} | Country {i} | League {i} |" for i in range(1,51))
            manifest.write_text("\n".join(manifest_lines)+"\n",encoding="utf-8")
            with crosswalk.open("w",encoding="utf-8",newline="") as f:
                writer=csv.DictWriter(f,fieldnames=["selected_manifest_id","provider_comp_master_id_observed"])
                writer.writeheader()
                writer.writerows({"selected_manifest_id":str(i),"provider_comp_master_id_observed":""} for i in range(1,51))
            with current.open("w",encoding="utf-8",newline="") as f:
                fields=["fotmob_match_id","date_utc","league_id","league","home_id","home_team","away_id","away_team",
                        "home_goals","away_goals","finished","started","cancelled","status"]
                writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
                if include_current:
                    writer.writerow({"fotmob_match_id":"fm-1","date_utc":kickoff.isoformat(),"league_id":"fotmob-league-1",
                                     "league":"Test League","home_id":"11","home_team":"Home FC","away_id":"22","away_team":"Away FC",
                                     "home_goals":current_home_goals,"away_goals":current_away_goals,
                                     "finished":str(current_finished).lower(),"started":"false","cancelled":"false","status":current_status})
            with ledger.open("w",encoding="utf-8",newline="") as f:
                fields=["match_id","date","date_utc","league_code","league","home_team","away_team","home_goals","away_goals","source","source_season","source_match_id"]
                writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
                writer.writerow({"match_id":"ledger-1","date":kickoff.date().isoformat(),
                                 "date_utc":kickoff.isoformat() if ledger_exact else "",
                                 "league_code":"TEST","league":"Test League","home_team":"Home FC","away_team":"Away FC",
                                 "home_goals":footy_home_goals,"away_goals":footy_away_goals,
                                 "source":"FotMob","source_season":"2025/2026","source_match_id":"fm-1"})
            argv=["audit_selected50_cross_provider_fixture_joins.py","--archive",str(archive),
                  "--current-matches",str(current),"--historical-matches",str(ledger),
                  "--manifest",str(manifest),"--identity-crosswalk",str(crosswalk),"--out",str(out)]
            with patch.object(sys,"argv",argv),contextlib.redirect_stdout(io.StringIO()):
                main()
            summary=json.loads((out/"audit_summary.json").read_text(encoding="utf-8"))
            def read_csv(name):
                with (out/name).open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
            return summary,read_csv("exact_fixture_join_rows.csv"),read_csv("date_only_ledger_candidate_rows.csv"),read_csv("canonical_code_candidates.csv"),read_csv("date_only_ledger_candidates.csv")

    def test_date_only_ledger_is_not_reported_as_exact_or_canonical_join(self):
        summary,exact,date_only,canonical,date_groups=self.run_audit(include_current=False)
        self.assertEqual(summary["exact_join_rows_total"],0)
        self.assertEqual(summary["historical_ledger_exact_join_rows"],0)
        self.assertEqual(summary["historical_ledger_date_only_join_rows"],1)
        self.assertEqual(summary["canonical_code_candidate_groups"],0)
        self.assertEqual(summary["date_only_ledger_candidate_groups"],1)
        self.assertEqual(len(exact),0)
        self.assertEqual(date_only[0]["join_precision"],"DATE_ONLY_NO_KICKOFF_PROOF")
        self.assertEqual(date_groups[0]["bridge_status"],"DATE_ONLY_OVERLAP_HUMAN_REVIEW_REQUIRED_NO_KICKOFF_PROOF")
        self.assertEqual(canonical,[])

    def test_exact_timestamp_ledger_join_is_separate_from_date_only_candidate(self):
        summary,exact,date_only,canonical,date_groups=self.run_audit(ledger_exact=True,include_current=False)
        self.assertEqual(summary["historical_ledger_exact_join_rows"],1)
        self.assertEqual(summary["historical_ledger_date_only_join_rows"],0)
        self.assertEqual(len(exact),1)
        self.assertEqual(exact[0]["join_type"],"ORACLE_HISTORICAL_LEDGER")
        self.assertEqual(date_only,[])
        self.assertEqual(len(canonical),1)
        self.assertEqual(date_groups,[])

    def test_status_conflict_is_counted_even_when_scores_are_missing(self):
        summary,exact,_,_,_=self.run_audit(current_status="complete",current_finished=True)
        self.assertEqual(summary["fotmob_exact_join_rows"],1)
        self.assertEqual(summary["source_conflict_rows"],1)
        self.assertFalse(exact[0]["score_known_both_sources"])

    def test_matching_status_and_missing_scores_are_not_a_conflict(self):
        summary,exact,_,_,_=self.run_audit()
        self.assertEqual(summary["fotmob_exact_join_rows"],1)
        self.assertEqual(summary["source_conflict_rows"],0)

    def test_date_only_timestamp_is_not_promoted_to_midnight_utc(self):
        self.assertIsNone(timestamp({"date":"2026-10-30"},("date",)))
        self.assertEqual(timestamp({"date_utc":"2026-10-30T18:00:00+00:00"},("date_utc",)),
                         int(datetime(2026,10,30,18,0,tzinfo=timezone.utc).timestamp()))

    def test_audit_script_has_no_network_client_calls(self):
        source=Path(__file__).resolve().parents[1]/"scripts"/"audit_selected50_cross_provider_fixture_joins.py"
        text=source.read_text(encoding="utf-8")
        self.assertNotIn("urlopen(",text)
        self.assertNotIn("requests.get(",text)
        self.assertNotIn("httpx.",text)


if __name__=="__main__":
    unittest.main()
