from pathlib import Path
import importlib.util
import csv

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_selected50_historical_readiness_contract.py"

spec = importlib.util.spec_from_file_location("contract", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_selected50_contract_blocks_without_gateway_and_historical_evidence():
    manifest = mod.read_csv(mod.MANIFEST)
    crosswalk = mod.read_csv(mod.CROSSWALK)
    result = mod.validate_contract(manifest, crosswalk)
    assert result["governed_universe"] == 50
    assert result["historical_window"] == {"start_year": 2024, "end_year": 2026, "end_semantics": "CURRENT"}
    assert result["network_calls"] == 0
    assert result["provider_calls"] == 0
    assert result["production_eligible"] is False
    assert result["betting_eligible"] is False
    assert result["status"] == "BLOCKED"
    assert "NO_AUTHENTICATED_HISTORICAL_SEASON_EVIDENCE" in result["blockers"]
    assert "SIGNED_PRIVATE_ARCHIVE_RECEIPT_MISSING" in result["blockers"]

def test_pagination_and_feature_evidence_are_fail_closed():
    assert "NO_PAGINATION_COMPLETENESS_EVIDENCE" in mod.validate_contract(
        mod.read_csv(mod.MANIFEST), mod.read_csv(mod.CROSSWALK)
    )["blockers"]
    assert "NO_KICKOFF_CHRONOLOGY_EVIDENCE" in mod.validate_contract(
        mod.read_csv(mod.MANIFEST), mod.read_csv(mod.CROSSWALK)
    )["blockers"]
    assert "NO_RECENT_FORM_H2H_STANDINGS_XG_ODDS_POINT_IN_TIME_EVIDENCE" in mod.validate_contract(
        mod.read_csv(mod.MANIFEST), mod.read_csv(mod.CROSSWALK)
    )["blockers"]
