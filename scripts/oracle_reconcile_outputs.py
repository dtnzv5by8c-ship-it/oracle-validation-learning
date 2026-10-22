#!/usr/bin/env python3
"""CLI for research-only Oracle fixture/market output reconciliation.

This tool checks CSV outputs after a prediction runner has completed. It does
not invoke the predictor or modify probabilities. Exit code 0 means PASS;
exit code 1 means FAIL; exit code 2 means BLOCKED/invalid inputs.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from scripts.oracle_isolated_batch_runner import validate_market_output


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV_HAS_NO_HEADER:{path}")
        return list(reader)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-fixtures", required=True, type=Path,
                        help="Schedule CSV containing the expected fixture IDs")
    parser.add_argument("--predictions", required=True, type=Path,
                        help="Prediction CSV with fixture_id, selection, raw_probability")
    parser.add_argument("--expected-markets", required=True,
                        help="Comma-separated exact market/selection names")
    parser.add_argument("--schedule-id-column", default="fixture_id",
                        help="Fixture ID column in schedule CSV (default: fixture_id)")
    parser.add_argument("--prediction-id-column", default="fixture_id",
                        help="Fixture ID column in predictions CSV (default: fixture_id)")
    parser.add_argument("--market-column", default="selection",
                        help="Market/selection column in predictions CSV (default: selection)")
    parser.add_argument("--probability-column", default="raw_probability",
                        help="Probability column in predictions CSV (default: raw_probability)")
    parser.add_argument("--output-json", type=Path,
                        help="Optional path to write the machine-readable report")
    args = parser.parse_args()

    try:
        schedule = read_csv(args.expected_fixtures)
        predictions = read_csv(args.predictions)
        for label, rows, column in (
            ("schedule", schedule, args.schedule_id_column),
            ("predictions", predictions, args.prediction_id_column),
        ):
            if rows and column not in rows[0]:
                raise ValueError(f"MISSING_{label.upper()}_COLUMN:{column}")
        expected_ids = [str(row[args.schedule_id_column]).strip() for row in schedule]
        rows = [{
            "fixture_id": row.get(args.prediction_id_column, ""),
            "selection": row.get(args.market_column, ""),
            "raw_probability": row.get(args.probability_column, ""),
        } for row in predictions]
        markets = [part.strip() for part in args.expected_markets.split(",") if part.strip()]
        report = validate_market_output(
            rows, expected_markets=markets, expected_fixture_ids=expected_ids
        )
        report.update({
            "scope": "RESEARCH_ONLY",
            "expected_fixture_count": len(expected_ids),
            "predictions_csv": str(args.predictions),
            "schedule_csv": str(args.expected_fixtures),
        })
        exit_code = 0 if report["status"] == "PASS" else (2 if report["status"] == "BLOCKED" else 1)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        report = {"status": "BLOCKED", "errors": [f"INPUT_ERROR:{type(exc).__name__}:{exc}"],
                  "scope": "RESEARCH_ONLY"}
        exit_code = 2

    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(rendered + "\n", encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
