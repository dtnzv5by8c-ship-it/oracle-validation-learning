#!/usr/bin/env python3
"""Research-only audit of Selected-50 global walk-forward market stability.

Reads only the sanitized aggregate fold metrics. It never loads fixture-level
rows, settlement ledgers, the H2H paired holdout, odds, or provider APIs.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

MARKETS = {"BTTS", "DC_HOME", "DC_AWAY", "COMBO_HOME", "COMBO_AWAY"}
RAW_STATUS = "RAW_WALK_FORWARD_NOT_CALIBRATED"
FOLDS = [
    "WF1_2025-03-20_to_2025-09-20",
    "WF2_2025-09-20_to_2026-03-20",
    "WF3_2026-03-20_to_2026-09-20",
]
FOLD_RE = re.compile(r"^WF\d+_(\d{4}-\d{2}-\d{2})_to_(\d{4}-\d{2}-\d{2})$")


def number(row: dict, key: str) -> float:
    try:
        value = float(row[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Missing/non-numeric {key}") from exc
    if not math.isfinite(value):
        raise ValueError(f"Non-finite {key}")
    return value


def load(root: Path):
    folder = root / "data" / "selected50_walk_forward_snapshot"
    with (folder / "aggregate_folds.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    with (folder / "metadata.json").open(encoding="utf-8") as f:
        metadata = json.load(f)
    return rows, metadata


def validate(rows: list[dict], metadata: dict) -> dict:
    if len(rows) != 15:
        raise ValueError(f"Expected 15 market-fold rows, found {len(rows)}")
    if metadata.get("snapshot_type") != "SANITIZED_AGGREGATE_WALK_FORWARD_METRICS_ONLY_NO_RAW_PROVIDER_ROWS":
        raise ValueError("Unexpected snapshot type")
    runtime = metadata.get("runtime_validation", {})
    if runtime.get("selected_groups") != 50 or runtime.get("market_fold_rows") != 15:
        raise ValueError("Selected-50 runtime contract mismatch")
    if runtime.get("production_eligible") is not False or runtime.get("betting_eligible") is not False:
        raise ValueError("Source unexpectedly marks outputs eligible")
    qa = metadata.get("governed_fixture_qa", {})
    if qa.get("all_combo_probabilities_blocked") is not True:
        raise ValueError("Combo block is not verified")
    if qa.get("combo_home_probabilities_remaining") != 0 or qa.get("combo_away_probabilities_remaining") != 0:
        raise ValueError("Unexpected Combo outputs remain")

    grouped = defaultdict(list)
    seen = set()
    for row in rows:
        market, fold = row.get("market", ""), row.get("fold", "")
        key = (market, fold)
        if market not in MARKETS or key in seen:
            raise ValueError(f"Unexpected or duplicate market-fold key: {key}")
        seen.add(key)
        if row.get("status") != RAW_STATUS:
            raise ValueError(f"Unexpected probability status for {key}")
        if number(row, "test_n") <= 0 or number(row, "train_n") <= 0:
            raise ValueError(f"Invalid sample size for {key}")
        for col in ("accuracy_at_0_5", "brier", "ece_10_bins", "training_prevalence", "baseline_brier"):
            if not 0 <= number(row, col) <= 1:
                raise ValueError(f"Out-of-range {col} for {key}")
        if number(row, "log_loss") < 0 or number(row, "baseline_brier") <= 0:
            raise ValueError(f"Invalid loss for {key}")
        implied = 1 - number(row, "brier") / number(row, "baseline_brier")
        if abs(implied - number(row, "brier_skill_vs_prevalence")) > 0.0001:
            raise ValueError(f"Brier-skill arithmetic mismatch for {key}")
        grouped[market].append(row)

    if set(grouped) != MARKETS:
        raise ValueError("Market coverage mismatch")
    partitions = set()
    for market, group in grouped.items():
        if len(group) != 3:
            raise ValueError(f"{market}: expected three folds")
        by_fold = {r["fold"]: r for r in group}
        if set(by_fold) != set(FOLDS):
            raise ValueError(f"{market}: unexpected fold chronology")
        previous_end, previous_train = None, 0
        signature = []
        for fold in FOLDS:
            row = by_fold[fold]
            match = FOLD_RE.match(fold)
            if not match:
                raise ValueError(f"Malformed fold label: {fold}")
            start, end = match.groups()
            if previous_end is not None and start != previous_end:
                raise ValueError(f"{market}: overlapping or gapped folds")
            train_n, test_n = int(number(row, "train_n")), int(number(row, "test_n"))
            if train_n <= previous_train:
                raise ValueError(f"{market}: training window did not expand")
            previous_end, previous_train = end, train_n
            signature.append((fold, train_n, test_n))
        partitions.add(tuple(signature))
    if len(partitions) != 1:
        raise ValueError("Markets do not share identical fold partitions")
    return grouped


def analyze(rows: list[dict], metadata: dict) -> dict:
    grouped = validate(rows, metadata)
    output = {}
    for market, group in grouped.items():
        by_fold = {r["fold"]: r for r in group}
        ordered = [by_fold[f] for f in FOLDS]
        total_n = sum(int(number(r, "test_n")) for r in ordered)

        def weighted(field):
            return sum(number(r, field) * int(number(r, "test_n")) for r in ordered) / total_n

        brier, baseline = weighted("brier"), weighted("baseline_brier")
        accuracy, prevalence = weighted("accuracy_at_0_5"), weighted("training_prevalence")
        majority = max(prevalence, 1 - prevalence)
        skills = [number(r, "brier_skill_vs_prevalence") for r in ordered]
        ece = [number(r, "ece_10_bins") for r in ordered]
        output[market] = {
            "test_n_across_disjoint_folds": total_n,
            "train_n_by_fold": [int(number(r, "train_n")) for r in ordered],
            "test_n_by_fold": [int(number(r, "test_n")) for r in ordered],
            "weighted_accuracy_from_rounded_fold_rates": round(accuracy, 6),
            "weighted_training_prevalence": round(prevalence, 6),
            "majority_class_accuracy_baseline": round(majority, 6),
            "accuracy_minus_majority_baseline_pp": round(100 * (accuracy - majority), 4),
            "weighted_brier": round(brier, 6),
            "weighted_prevalence_baseline_brier": round(baseline, 6),
            "aggregate_brier_skill": round(1 - brier / baseline, 6),
            "weighted_log_loss": round(weighted("log_loss"), 6),
            "positive_skill_folds": sum(x > 0 for x in skills),
            "fold_brier_skill": [round(x, 6) for x in skills],
            "fold_ece_not_pooled": [round(x, 6) for x in ece],
            "probabilities_raw_uncalibrated": True,
            "calibration_approved": False,
            "production_eligible": False,
            "betting_eligible": False,
            "research_disposition": (
                "COMBO_BLOCKED_SEMANTIC_MISMATCH"
                if market.startswith("COMBO_")
                else "GLOBAL_BASELINE_COMPARISON_ONLY"
            ),
        }

    ranking = sorted(
        (m for m in output if not m.startswith("COMBO_")),
        key=lambda m: output[m]["aggregate_brier_skill"],
        reverse=True,
    )
    return {
        "status": "RESEARCH_ONLY_GLOBAL_MARKET_FOLD_STABILITY_AUDIT",
        "source_file": "data/selected50_walk_forward_snapshot/aggregate_folds.csv",
        "source_snapshot_type": metadata["snapshot_type"],
        "source_provenance": metadata.get("source", {}),
        "source_reported_counts": metadata.get("source_artifact_reported_counts", {}),
        "selected_league_groups": 50,
        "fold_design": metadata.get("fold_design"),
        "per_market": output,
        "non_combo_research_order_by_aggregate_brier_skill": ranking,
        "limitations": [
            "Metrics are test-size-weighted aggregates of rounded fold summaries, not exact fixture-level pooled metrics.",
            "Accuracy is reconstructed from rounded fold rates; AUC and ECE are not pooled.",
            "Raw probabilities are uncalibrated; low ECE does not approve calibration.",
            "No Brier-skill confidence intervals or multiplicity-adjusted inference are available.",
            "Global league aggregates do not establish team-level suitability, profitability, or betting eligibility.",
            "Combo remains blocked because predictor and settlement definitions disagree.",
        ],
        "governance": {
            "locked_h2h_paired_holdout_read": False,
            "provider_api_calls": 0,
            "production_logic_changed": False,
            "frozen_probabilities_changed": False,
            "calibration_changed": False,
            "betting_eligibility_approved": False,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("reports/oracle_selected50_global_market_fold_stability_summary_2026-10-30.json"))
    args = parser.parse_args()
    rows, metadata = load(args.root)
    summary = analyze(rows, metadata)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": summary["status"],
        "selected_league_groups": 50,
        "aggregate_brier_skill": {m: v["aggregate_brier_skill"] for m, v in summary["per_market"].items()},
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
