import pandas as pd
from scripts.evaluate_settlement_evidence_gate import audit

def base(n=100):
    return pd.DataFrame({
        "fixture_id":[f"F{i}" for i in range(n)],
        "prediction_timestamp_utc":["2026-10-01T10:00:00Z"]*n,
        "kickoff_utc":["2026-10-01T12:00:00Z"]*n,
        "market":["BTTS"]*n,
        "probability":[0.6]*n,
        "settlement_status":["SETTLED_VERIFIED_PROVIDER_SCORE"]*n,
        "actual_result":["YES"]*n,
        "source_manifest_hash":["sha"]*n,
    })

def test_valid_settled_sample_is_metric_ready():
    result=audit(base())
    assert result["status"]=="READY"
    assert result["metric_calculation_permitted"] is True
    assert result["production_eligible"] is False
    assert result["betting_eligible"] is False

def test_unsettled_rows_block_metrics():
    df=base()
    df.loc[0,"settlement_status"]="UNSETTLED"
    assert audit(df)["status"]=="BLOCKED"
    assert audit(df)["metric_calculation_permitted"] is False

def test_future_prediction_blocks_metrics():
    df=base()
    df.loc[0,"prediction_timestamp_utc"]="2026-10-01T13:00:00Z"
    assert audit(df)["status"]=="BLOCKED"

def test_missing_provenance_blocks_metrics():
    df=base()
    df.loc[0,"source_manifest_hash"]=""
    assert audit(df)["status"]=="BLOCKED"

def test_small_sample_is_not_claimed_ready():
    assert audit(base(99))["status"]=="INSUFFICIENT_SAMPLE"
