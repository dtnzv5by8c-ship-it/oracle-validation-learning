#!/usr/bin/env python3
"""Build a deterministic, no-network diagnostic of the documented Combo rule mismatch.

This is a research governance artifact only. It does not choose or change an
authoritative market definition, settlement rule, production model, or probability.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audit-output"
OUT.mkdir(parents=True, exist_ok=True)
MATRIX = OUT / "selected50_combo_settlement_mismatch_matrix.csv"
SUMMARY = OUT / "selected50_combo_settlement_mismatch_summary.json"

MAX_GOALS_PER_SIDE = 10


def evaluate(home: int, away: int) -> dict:
    total = home + away
    home_dc = home >= away
    away_dc = away >= home
    # Predictor target as documented in the selected-50 crosswalk:
    # Double Chance AND 2-4 total goals inclusive.
    pred_home = home_dc and 2 <= total <= 4
    pred_away = away_dc and 2 <= total <= 4
    # Comparator as documented for the settlement ledger:
    # Double Chance AND total goals below five (no lower bound).
    ledger_home = home_dc and total < 5
    ledger_away = away_dc and total < 5
    return {
        "home_score": home,
        "away_score": away,
        "total_goals": total,
        "home_double_chance": home_dc,
        "away_double_chance": away_dc,
        "combo_home_predictor_target": pred_home,
        "combo_home_documented_ledger_comparator": ledger_home,
        "combo_home_disagreement": pred_home != ledger_home,
        "combo_away_predictor_target": pred_away,
        "combo_away_documented_ledger_comparator": ledger_away,
        "combo_away_disagreement": pred_away != ledger_away,
        "decision_status": "BLOCKED_PENDING_GOVERNED_DEFINITION",
        "production_eligible": "NO",
    }


def main() -> None:
    rows = [evaluate(h, a) for h in range(MAX_GOALS_PER_SIDE + 1)
            for a in range(MAX_GOALS_PER_SIDE + 1)]
    fields = list(rows[0].keys())
    with MATRIX.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    home_mismatch = [r for r in rows if r["combo_home_disagreement"]]
    away_mismatch = [r for r in rows if r["combo_away_disagreement"]]
    summary = {
        "status": "DIAGNOSTIC_ONLY_NOT_A_MARKET_DEFINITION_APPROVAL",
        "score_grid": f"0-{MAX_GOALS_PER_SIDE} goals per side, inclusive",
        "scorelines_evaluated": len(rows),
        "combo_home_disagreement_scorelines": len(home_mismatch),
        "combo_away_disagreement_scorelines": len(away_mismatch),
        "combo_home_disagreement_examples": [
            f'{r["home_score"]}-{r["away_score"]}' for r in home_mismatch
        ],
        "combo_away_disagreement_examples": [
            f'{r["home_score"]}-{r["away_score"]}' for r in away_mismatch
        ],
        "predictor_comparator": "Double Chance AND 2 <= total goals <= 4",
        "documented_ledger_comparator": "Double Chance AND total goals < 5",
        "production_eligible": False,
        "decision": "Keep Combo predictions blocked until the authoritative market definition is approved and predictor/settlement labels are aligned.",
        "limitations": [
            "This enumerates scoreline logic; it is not a frequency estimate from historical matches.",
            "It does not establish the official bookmaker settlement rule.",
            "No source data, network calls, provider credits, model logic, or probabilities are used or changed.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    assert len(rows) == 121
    assert len(home_mismatch) == 2
    assert len(away_mismatch) == 2
    assert all(r["production_eligible"] == "NO" for r in rows)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
