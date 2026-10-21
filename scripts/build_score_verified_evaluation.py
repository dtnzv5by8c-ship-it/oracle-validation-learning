#!/usr/bin/env python3
"""Research-only evaluation join: immutable pre-kickoff predictions + frozen score results."""
import argparse, hashlib, json
from datetime import datetime
from pathlib import Path
from scripts.settle_market_from_final_score import settle
from scripts.summarize_prospective_evaluation import summarize

PREDICTION_KEYS = ("prediction_id", "fixture_id", "competition_id", "scheduled_kickoff_utc",
                   "prediction_timestamp_utc", "home_team_id", "away_team_id", "market", "selection", "probability")
RESULT_KEYS = ("fixture_id", "competition_id", "scheduled_kickoff_utc", "home_team_id", "away_team_id",
               "home_score", "away_score", "match_status", "result_source", "result_observed_at_utc")

def utc(value):
    if not isinstance(value, str) or not value:
        raise ValueError("MISSING_TIMESTAMP")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("INVALID_TIMESTAMP")
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("TIMEZONE_REQUIRED")
    return dt

def fixture_key(row):
    return tuple(str(row.get(k, "")) for k in
        ("fixture_id", "competition_id", "scheduled_kickoff_utc", "home_team_id", "away_team_id"))

def build_rows(predictions, results, manifest, results_sha256):
    if manifest.get("results_sha256") != results_sha256:
        raise ValueError("RESULT_SNAPSHOT_HASH_MISMATCH")
    sources = manifest.get("sources", {})
    if not sources:
        raise ValueError("SOURCE_MANIFEST_EMPTY")
    by_fixture = {}
    for r in results:
        missing = [k for k in RESULT_KEYS if r.get(k) in (None, "")]
        if missing:
            raise ValueError("RESULT_MISSING_FIELDS:" + ",".join(missing))
        src = str(r["result_source"])
        spec = sources.get(src)
        if not spec or spec.get("approved_for_evaluation") is not True or not spec.get("source_uri"):
            continue
        utc(r["result_observed_at_utc"])
        key = fixture_key(r)
        if key in by_fixture and by_fixture[key] != r:
            raise ValueError("CONFLICTING_RESULT_SNAPSHOTS")
        by_fixture[key] = r
    seen = set()
    rows, rejected = [], []
    for p in predictions:
        pid = str(p.get("prediction_id", ""))
        if not pid or pid in seen:
            raise ValueError("DUPLICATE_OR_MISSING_PREDICTION_ID")
        seen.add(pid)
        missing = [k for k in PREDICTION_KEYS if p.get(k) in (None, "")]
        if missing:
            rejected.append({"prediction_id":pid,"reason":"PREDICTION_MISSING_FIELDS:" + ",".join(missing)})
            continue
        try:
            pred_time, kickoff = utc(p["prediction_timestamp_utc"]), utc(p["scheduled_kickoff_utc"])
            prob = float(p["probability"])
            if not 0 <= prob <= 1:
                raise ValueError("PROBABILITY_OUT_OF_RANGE")
            if pred_time >= kickoff:
                raise ValueError("PREDICTION_NOT_STRICTLY_PRE_KICKOFF")
        except (ValueError, TypeError) as e:
            rejected.append({"prediction_id":pid,"reason":str(e)})
            continue
        result = by_fixture.get(fixture_key(p))
        if not result:
            rejected.append({"prediction_id":pid,"reason":"NO_APPROVED_EXACT_FIXTURE_RESULT"})
            continue
        try:
            outcome = settle(p, result)["outcome"]
        except ValueError as e:
            rejected.append({"prediction_id":pid,"reason":"SETTLEMENT_REJECTED:" + str(e)})
            continue
        rows.append({"prediction_id":pid,"fixture_id":p["fixture_id"],"market":p["market"],
                     "selection":p["selection"],"probability":prob,"outcome":outcome,
                     "verified_fixture":True,"verified_result_source":True,
                     "result_source":result["result_source"],"result_snapshot_sha256":results_sha256,
                     "settlement_rule_version":"oracle-score-settlement-v1"})
    return {"status":"RESEARCH_ONLY_EVALUATION_JOIN","accepted_count":len(rows),"rejected_count":len(rejected),
            "rows":rows,"rejected":rejected,"metrics":summarize(rows),
            "warning":"Research-only. Review the source manifest and preserve the exact result snapshot before interpreting metrics. A hash proves file identity, not source authenticity."}

def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--predictions",required=True); ap.add_argument("--results",required=True)
    ap.add_argument("--source-manifest",required=True); ap.add_argument("--expected-manifest-sha256",required=True)
    ap.add_argument("--out",required=True); args=ap.parse_args()
    manifest_bytes=Path(args.source_manifest).read_bytes()
    manifest_hash=hashlib.sha256(manifest_bytes).hexdigest()
    if manifest_hash != args.expected_manifest_sha256:
        raise SystemExit("SOURCE_MANIFEST_HASH_MISMATCH")
    result_bytes=Path(args.results).read_bytes()
    result=build_rows(read_jsonl(args.predictions),read_jsonl(args.results),
                      json.loads(manifest_bytes),hashlib.sha256(result_bytes).hexdigest())
    result["source_manifest_sha256"]=manifest_hash
    out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"accepted_count":result["accepted_count"],
                      "rejected_count":result["rejected_count"],"metrics":result["metrics"]["metrics"]},sort_keys=True))
if __name__=="__main__": main()
