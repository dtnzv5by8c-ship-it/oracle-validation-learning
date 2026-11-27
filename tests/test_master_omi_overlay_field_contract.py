import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_master_omi_current.py"

class MasterOMIOverlayFieldContractTest(unittest.TestCase):
    def test_overlay_runtime_symbols_are_defined_before_use(self):
        source = SCRIPT.read_text(encoding="utf-8")
        tree = ast.parse(source)
        assigned = set()
        referenced = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = []
                if isinstance(node, ast.AugAssign):
                    targets = [node.target]
                elif isinstance(node, ast.Assign):
                    targets = node.targets
                else:
                    targets = [node.target]
                for target in targets:
                    if isinstance(target, ast.Name):
                        assigned.add(target.id)
                    elif isinstance(target, (ast.Tuple, ast.List)):
                        assigned.update(x.id for x in target.elts if isinstance(x, ast.Name))
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                referenced.append(node.id)
        undefined = sorted(
            name for name in set(referenced)
            if name in {"alias", "mandatory", "blocked_fields"} and name not in assigned
        )
        self.assertEqual(undefined, [], f"overlay runtime symbols undefined: {undefined}")

    def test_required_contracts_exist(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("alias = {", source)
        self.assertIn("mandatory = {", source)
        self.assertIn("blocked_fields = []", source)
        self.assertIn("MASTER_OMI_BLOCKED_MANDATORY_INPUTS_MISSING", source)

if __name__ == "__main__":
    unittest.main()
