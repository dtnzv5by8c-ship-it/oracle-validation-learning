import json
import unittest
from pathlib import Path

BUILDER = Path("scripts/build_master_omi_current.py")

class MasterOMIAETHashContractTests(unittest.TestCase):
    def test_governed_hash_serialization_includes_contract_fields(self):
        text = BUILDER.read_text(encoding="utf-8")
        self.assertIn("canonical_aet_payload", text)
        self.assertIn("cell(r, col).data_type", text)
        self.assertIn("cell(r, col).number_format", text)
        self.assertIn("cell(r, col).comment.text if", text)
        self.assertIn('expected_aet_sha256="b790145feea9a20f0d3d0070f76ace8c98c4a5f0911928a4335218beaf090564"', text)

if __name__ == "__main__":
    unittest.main()
