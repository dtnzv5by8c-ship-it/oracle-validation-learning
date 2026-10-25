#!/usr/bin/env python3
"""Unit tests for exact selected-50 catalogue resolution; no network access."""
import csv, json, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from resolve_selected50_catalogue import resolve

class CatalogueResolverTests(unittest.TestCase):
 def setUp(self):
  self.manifest=[{"selected_id":"1001","country":"X","competition_name":"League A"},
                 {"selected_id":"1002","country":"Y","competition_name":"League B"},
                 {"selected_id":"1003","country":"Z","competition_name":"League C"}]
 def test_exact_nested_ids_and_parent_id_only_when_explicit(self):
  leagues=[{"name":"League A","country":"X","season":[{"id":1001,"year":"2026"}]},
           {"name":"Provider B","country":"Y","competition_id":77,"season":[{"id":1002,"year":"2026"}]}]
  rows=resolve(self.manifest,leagues)
  self.assertEqual("EXACT_SEASON_ID_MATCH",rows[0]["catalogue_status"])
  self.assertEqual("1001",rows[0]["provider_season_id"])
  self.assertEqual("",rows[0]["provider_competition_id"])
  self.assertEqual("77",rows[1]["provider_competition_id"])
  self.assertEqual("EXACT_SEASON_ID_NOT_FOUND",rows[2]["catalogue_status"])
 def test_duplicate_exact_id_is_blocked(self):
  leagues=[{"name":"A","season":[{"id":"1001"}]},{"name":"B","season":[{"id":1001}]}]
  row=resolve(self.manifest,leagues)[0]
  self.assertEqual("BLOCKED_DUPLICATE_SEASON_ID",row["catalogue_status"])
  self.assertEqual("",row["provider_competition_id"])
 def test_near_name_is_not_a_match(self):
  leagues=[{"name":"League A Alt","season":[{"id":"9999"}]}]
  row=resolve(self.manifest,leagues)[0]
  self.assertEqual("EXACT_SEASON_ID_NOT_FOUND",row["catalogue_status"])
  self.assertEqual("NO_MATCH_NO_GUESS",row["mapping_method"])
 def test_no_parent_id_inferred_from_season_id(self):
  row=resolve(self.manifest,[{"name":"League A","id":55,"season":[{"id":"1001"}]}])[0]
  self.assertEqual("",row["provider_competition_id"])
  self.assertEqual("1001",row["provider_season_id"])
if __name__=="__main__": unittest.main(verbosity=2)
