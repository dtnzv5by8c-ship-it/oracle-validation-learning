#!/usr/bin/env python3
"""Research-only settlement/evaluation evidence gate for Oracle.

This module does not score or promote predictions. It determines whether an
existing prediction/settlement dataset is admissible for metric calculation.
It fails closed when point-in-time provenance, exact identity, settlement
truth, or prediction timestamps are not proven.

Production/betting eligibility is never changed here.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

REQUIRED = {
    "fixture_id", "prediction_timestamp_utc", "kickoff_utc",
    "market", "probability", "settlement_status",
    "actual_result", "source_manifest_hash",
}
SETTLED = {"SETTLED_VERIFIED_PROVIDER_SCORE"}
BINARY_MARKETS = {"BTTS", "Over15", "Over25", "Under45", "HOME_WIN", "DRAW", "AWAY_WIN", "1X", "X2"}


def audit(df: pd.DataFrame) -> dict:
    missing = sorted(REQUIRED - set(df.columns))
    if missing:
        return {
            "status": "BLOCKED",
            "reason": "MISSING_REQUIRED_SETTLEMENT_EVIDENCE_COLUMNS",
            "missing_columns": missing,
            "production_eligible": False,
            "betting_eligible": False,
        }

    work = df.copy()
    work["prediction_timestamp_utc"] = pd.to_datetime(work["prediction_timestamp_utc"], utc=True, errors="coerce")
    work["kickoff_utc"] = pd.to_datetime(work["kickoff_utc"], utc=True, errors="coerce")
    work["probability"] = pd.to_numeric(work["probability"], errors="coerce")

    duplicate_identity = work.duplicated(["fixture_id", "market"], keep=False)
    pre_kickoff = work["prediction_timestamp_utc"].notna() & work["kickoff_utc"].notna() & (
        work["prediction_timestamp_utc"] < work["kickoff_utc"]
    )
    valid_probability = work["probability"].between(0, 1, inclusive="both")
    settled = work["settlement_status"].isin(SETTLED)
    verified_actual = settled & work["actual_result"].notna() & (work["actual_result"].astype(str).str.strip() != "")
    provenance = work["source_manifest_hash"].notna() & (work["source_manifest_hash"].astype(str).str.strip() != "")

    gates = {
        "exact_fixture_market_identity": not bool(duplicate_identity.any()) and work["fixture_id"].notna().all(),
        "timezone_aware_prediction_timestamp": bool(work["prediction_timestamp_utc"].notna().all()),
        "timezone_aware_kickoff": bool(work["kickoff_utc"].notna().all()),
        "strictly_pre_kickoff_prediction": bool(pre_kickoff.all()),
        "probability_in_0_1": bool(valid_probability.all()),
        "verified_settlement_truth": bool(verified_actual.all()),
        "source_manifest_provenance": bool(provenance.all()),
        "binary_market_definition": bool(work["market"].isin(BINARY_MARKETS).all()),
    }
    status = "READY" if all(gates.values()) and len(work) >= 100 else (
        "INSUFFICIENT_SAMPLE" if all(gates.values()) else "BLOCKED"
    )
    return {
        "status": status,
        "rows": int(len(work)),
        "settled_rows": int(settled.sum()),
        "verified_actual_rows": int(verified_actual.sum()),
        "gates": gates,
        "sample_gate_minimum_n": 100,
        "production_eligible": False,
        "betting_eligible": False,
        "metric_calculation_permitted": status == "READY",
        "metric_note": "Brier/log loss/AUC/calibration must be calculated only from this admissible set; no inferred, future, unsettled or unverified outcomes are allowed.",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    df = pd.read_csv(args.input)
    result = audit(df)
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
