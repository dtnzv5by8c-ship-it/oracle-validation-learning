#!/usr/bin/env python3
"""Research-only provenance gate for prospective Oracle evaluation rows.

The trusted-results input must be a separately acquired, frozen result snapshot.
This script requires exact fixture/team/kickoff/market/selection matching and an
explicit allowlist of result_source identifiers. It does not authenticate the
provider or snapshot by itself; preserve and review the acquisition manifest.
"""
import argparse, hashlib, json
from pathlib import Path

PREDICTION_KEYS = ("prediction_id", "fixture_id", "competition_id", "scheduled_kickoff_utc",
                   "home_team_id", "away_team_id", "market", "selection", "probability")
RESULT_KEYS = ("fixture_id", "competition_id", "scheduled_kickoff_utc", "home_team_id",
               "away_team_id", "market", "selection", "outcome", "result_source")
SETTLEMENT_KEYS = ("prediction_id", "fixture_id", "outcome", "result_source")

def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

def fixture_key(row):
    return tuple(str(row.get(k, "")) for k in
                 ("fixture_id", "competition_id", "scheduled_kickoff_utc", "home_team_id", "away_team_id", "market", "selection"))

def verify(predictions, settlements, trusted_results, allowed_sources):
    preds = {}
    for p in predictions:
        pid = str(p.get("prediction_id", ""))
        if not pid or pid in preds:
            raise ValueError("DUPLICATE_OR_MISSING_PREDICTION_ID")
        missing = [k for k in PREDICTION_KEYS if p.get(k) in (None, "")]
        if missing:
            raise ValueError("PREDICTION_MISSING_FIELDS:" + ",".join(missing))
        preds[pid] = p
    results = {}
    for r in trusted_results:
        missing = [k for k in RESULT_KEYS if r.get(k) in (None, "")]
        if missing:
            raise ValueError("TRUSTED_RESULT_MISSING_FIELDS:" + ",".join(missing))
        if str(r["result_source"]) not in allowed_sources:
            continue
        key = fixture_key(r)
        if key in results and results[key] != str(r["outcome"]).upper():
            raise ValueError("CONFLICTING_TRUSTED_RESULTS")
        results[key] = str(r["outcome"]).upper()
    settlement_by_pid = {}
    for s in settlements:
        missing = [k for k in SETTLEMENT_KEYS if s.get(k) in (None, "")]
        if missing:
            raise ValueError("SETTLEMENT_MISSING_FIELDS:" + ",".join(missing))
        pid = str(s["prediction_id"])
        if pid in settlement_by_pid:
            raise ValueError("DUPLICATE_SETTLEMENT_FOR_PREDICTION")
        settlement_by_pid[pid] = s
    accepted, rejected = [], []
    for pid, p in preds.items():
        s = settlement_by_pid.get(pid)
        if not s:
            rejected.append({"prediction_id": pid, "reason": "NO_SETTLEMENT"})
            continue
        if str(s["fixture_id"]) != str(p["fixture_id"]):
            rejected.append({"prediction_id": pid, "reason": "SETTLEMENT_FIXTURE_MISMATCH"})
            continue
        source = str(s["result_source"])
        if source not in allowed_sources:
            rejected.append({"prediction_id": pid, "reason": "RESULT_SOURCE_NOT_ALLOWLISTED"})
            continue
        key = fixture_key(p)
        trusted_outcome = results.get(key)
        if trusted_outcome is None:
            rejected.append({"prediction_id": pid, "reason": "NO_EXACT_TRUSTED_RESULT_MATCH"})
            continue
        outcome = str(s["outcome"]).upper()
        if outcome != trusted_outcome:
            rejected.append({"prediction_id": pid, "reason": "SETTLEMENT_OUTCOME_CONFLICTS_WITH_TRUSTED_RESULT"})
            continue
        accepted.append({"prediction_id": pid, "fixture_id": p["fixture_id"],
                         "market": p["market"], "selection": p["selection"],
                         "probability": p["probability"], "outcome": outcome,
                         "verified_fixture": True, "verified_result_source": True,
                         "verification_method": "EXACT_MATCH_TO_ALLOWLISTED_FROZEN_RESULT_SNAPSHOT"})
    return {"status": "RESEARCH_ONLY_PROVENANCE_GATE", "accepted_count": len(accepted),
            "rejected_count": len(rejected), "accepted": accepted, "rejected": rejected,
            "trusted_results_sha256": None,
            "warning": "Allowlisting and exact matching do not independently authenticate the result provider or acquisition time. Record a separately reviewed snapshot manifest and hash before using metrics."}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", required=True)
    ap.add_argument("--settlements", required=True)
    ap.add_argument("--trusted-results", required=True)
    ap.add_argument("--allowed-result-sources", required=True, help="Comma-separated exact source identifiers")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    result = verify(read_jsonl(args.predictions), read_jsonl(args.settlements),
                    read_jsonl(args.trusted_results),
                    {x.strip() for x in args.allowed_result_sources.split(",") if x.strip()})
    result["trusted_results_sha256"] = hashlib.sha256(Path(args.trusted_results).read_bytes()).hexdigest()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in ("accepted", "rejected")}, sort_keys=True))

if __name__ == "__main__":
    main()
