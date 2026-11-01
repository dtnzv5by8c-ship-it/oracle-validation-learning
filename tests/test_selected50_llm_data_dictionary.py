import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from openpyxl import Workbook, load_workbook

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "add_selected50_llm_data_dictionary.py"
spec = importlib.util.spec_from_file_location("selected50_dictionary", SCRIPT)
dictionary_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dictionary_module)
main = dictionary_module.main

class Selected50LLMDataDictionaryTests(unittest.TestCase):
    def test_adds_definition_for_every_heading_and_embeds_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            book=root/"report.xlsx"
            config=root/"config.json"
            wb=Workbook()
            ws=wb.active
            ws.title="Market Intelligence"
            ws.append(["Fixture","BTTS Yes","H2H N","production_eligible"])
            ws.append(["A vs B",62.5,0,"NO"])
            xg=wb.create_sheet("xG Evidence Audit")
            xg.append(["fixture_id","capture_time_utc","temporal_provenance_status"])
            xg.append(["F1","","UNVERIFIED"])
            wb.save(book)
            config.write_text(json.dumps({
                "report_name":"Test report",
                "configuration_version":"1.0.0",
                "selected_league_count":50,
                "pinned_archive_sha256":"abc",
                "weekly_workflow":"workflow.yml"
            }),encoding="utf-8")
            import sys
            old=sys.argv
            try:
                sys.argv=["add_selected50_llm_data_dictionary.py","--workbook",str(book),"--config",str(config)]
                self.assertEqual(main(),None)
            finally:
                sys.argv=old
            result=load_workbook(book,data_only=True)
            self.assertIn("LLM Data Dictionary",result.sheetnames)
            self.assertIn("Report Configuration",result.sheetnames)
            dictionary=result["LLM Data Dictionary"]
            entries={(dictionary.cell(r,1).value,dictionary.cell(r,4).value)
                     for r in range(2,dictionary.max_row+1)}
            self.assertEqual(entries,{
                ("Market Intelligence","Fixture"),
                ("Market Intelligence","BTTS Yes"),
                ("Market Intelligence","H2H N"),
                ("Market Intelligence","production_eligible"),
                ("xG Evidence Audit","fixture_id"),
                ("xG Evidence Audit","capture_time_utc"),
                ("xG Evidence Audit","temporal_provenance_status"),
            })
            cfg={result["Report Configuration"].cell(r,1).value:result["Report Configuration"].cell(r,2).value
                 for r in range(2,result["Report Configuration"].max_row+1)}
            self.assertEqual(cfg["configuration_version"],"1.0.0")
            self.assertEqual(cfg["selected_league_count"],50)
            self.assertEqual(result["Market Intelligence"]["B2"].value,62.5)
            self.assertEqual(result["Market Intelligence"]["C2"].value,0)

if __name__=="__main__":
    unittest.main()
