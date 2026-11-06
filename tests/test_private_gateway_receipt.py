#!/usr/bin/env python3
import hashlib, json, tempfile
from pathlib import Path
import importlib.util
from datetime import datetime, timezone, timedelta
p=Path("scripts/validate_private_gateway_receipt.py")
spec=importlib.util.spec_from_file_location("gateway",p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def base():
    recent=(datetime.now(timezone.utc)-timedelta(minutes=5)).isoformat().replace("+00:00","Z")
    return {
      "schema_version":1,"gateway_id":"approved-private-gateway-v1",
      "provider":"FootyStats","archive_ref":"private://oracle/60/batch-001.zip",
      "archive_sha256":"0"*64,"universe_name":"Oracle-60-League",
      "expected_leagues":60,"historical_start":"2024-01-01","historical_end":"current",
      "batch_id":"batch-001","requested_rows":10,"received_rows":10,"request_count":1,
      "raw_provider_payload_persisted_publicly":False,"credentials_persisted_publicly":False,
      "production_eligible":False,"betting_eligible":False,"transport_status":"PASS",
      "auth_status":"PASS","rate_limit_status":"PASS","receipt_status":"VERIFIED_PRIVATE_ARCHIVE","transport_mode":"private_archive",
      "transport_evidence_ref":"private://oracle/gateway/transport-evidence-001",
      "transport_verified_at_utc":recent
    }

with tempfile.TemporaryDirectory() as td:
    a=Path(td)/"archive.bin"; a.write_bytes(b"oracle-private-batch")
    r=base(); r["archive_sha256"]=hashlib.sha256(a.read_bytes()).hexdigest()
    assert m.validate(r,a)==[]
    bad=dict(r); bad["expected_leagues"]=49
    assert "expected_leagues_not_60" in m.validate(bad,a)
    bad=dict(r); bad["transport_status"]="BLOCKED_417"
    assert "transport_not_pass" in m.validate(bad,a)
    bad=dict(r); bad["raw_provider_payload_persisted_publicly"]=True
    assert "raw_provider_payload_public_visibility_not_false" in m.validate(bad,a)
    bad=dict(r); bad["archive_sha256"]="1"*64
    assert "archive_sha256_mismatch" in m.validate(bad,a)
    bad=dict(r); bad["archive_ref"]="https://public.example/archive.zip"
    assert "archive_ref_not_private" in m.validate(bad,a)
    bad=dict(r); bad["gateway_id"]="public-gateway-v1"
    assert "gateway_id_not_approved" in m.validate(bad,a)
    bad=dict(r); bad["request_count"]=101
    assert "request_count_exceeds_bounded_limit" in m.validate(bad,a)
    bad=dict(r); bad["request_count"]="not-a-number"
    assert "request_count_invalid" in m.validate(bad,a)
    bad=dict(r); bad["requested_rows"]="NaN"
    assert "requested_rows_invalid" in m.validate(bad,a)
    bad=dict(r); bad["received_rows"]="NaN"
    assert "received_rows_invalid" in m.validate(bad,a)
    bad=dict(r); bad["transport_mode"]="public_http"
    assert "transport_mode_not_approved" in m.validate(bad,a)
    bad=dict(r); bad["transport_evidence_ref"]="https://public.example/evidence"
    assert "transport_evidence_ref_not_private" in m.validate(bad,a)
    bad=dict(r); bad["historical_end"]="2027-01-01"
    assert "historical_end_out_of_range" in m.validate(bad,a)
    bad=dict(r); bad["transport_verified_at_utc"]=(datetime.now(timezone.utc)-timedelta(days=2)).isoformat().replace("+00:00","Z")
    assert "transport_proof_stale" in m.validate(bad,a)
    bad=dict(r); bad["transport_verified_at_utc"]=(datetime.now(timezone.utc)+timedelta(hours=1)).isoformat().replace("+00:00","Z")
    assert "transport_verified_timestamp_in_future" in m.validate(bad,a)
print("PASS: private gateway receipt contract regression tests")
