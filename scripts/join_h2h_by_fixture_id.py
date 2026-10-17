#!/usr/bin/env python3
"""Reporting-only exact Oracle Fixture ID -> H2H join and coverage audit.

Never changes Oracle prediction logic or probability values. Requires canonical
fixture IDs in both inputs; intentionally refuses fuzzy/date/team fallback.
"""
import argparse, csv, json
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone

def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f)), (csv.DictReader.__name__ if False else None)

def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w=csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows: w.writerow(row)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--oracle", required=True, help="Oracle fixture-level export CSV")
    ap.add_argument("--h2h", required=True, help="H2H fixture report CSV")
    ap.add_argument("--out", required=True, help="Joined report CSV")
    ap.add_argument("--audit", required=True, help="JSON QA audit path")
    ap.add_argument("--oracle-id", default="Oracle Fixture ID")
    ap.add_argument("--h2h-id", default="fixture_id")
    ap.add_argument("--league-column", default="League")
    args=ap.parse_args()
    with open(args.oracle, newline="", encoding="utf-8-sig") as f:
        oracle_reader=csv.DictReader(f); oracle=list(oracle_reader); oracle_cols=oracle_reader.fieldnames or []
    with open(args.h2h, newline="", encoding="utf-8-sig") as f:
        h2h_reader=csv.DictReader(f); h2h=list(h2h_reader); h2h_cols=h2h_reader.fieldnames or []
    for name, cols, key in [("Oracle",oracle_cols,args.oracle_id),("H2H",h2h_cols,args.h2h_id)]:
        if key not in cols: raise SystemExit(f"Required {name} ID column '{key}' not found. No fallback matching is allowed.")
    if not oracle or not h2h: raise SystemExit("Empty input: refusing to publish an empty joined report.")
    def ids(rows,key,label):
        vals=[(r.get(key) or "").strip() for r in rows]
        missing=sum(not v for v in vals)
        counts=Counter(v for v in vals if v)
        duplicates={k:v for k,v in counts.items() if v>1}
        if missing: raise SystemExit(f"{label} has {missing} blank fixture IDs; refusing unsafe join.")
        if duplicates: raise SystemExit(f"{label} has duplicate fixture IDs (first 10): {list(duplicates.items())[:10]}")
        return {v:r for v,r in zip(vals,rows)}
    oracle_by_id=ids(oracle,args.oracle_id,"Oracle input")
    h2h_by_id=ids(h2h,args.h2h_id,"H2H input")
    # Preserve every original Oracle field/value; append H2H fields with prefix.
    h2h_extra=[c for c in h2h_cols if c != args.h2h_id]
    out_cols=list(oracle_cols)+[f"H2H | {c}" for c in h2h_extra]
    joined=[]; matched=0; leagues=Counter(); league_matched=Counter()
    for row in oracle:
        fid=row[args.oracle_id].strip()
        hist=h2h_by_id.get(fid)
        out=dict(row)
        for c in h2h_extra: out[f"H2H | {c}"]=hist.get(c,"") if hist else ""
        joined.append(out)
        league=(row.get(args.league_column) or "UNKNOWN").strip()
        leagues[league]+=1
        if hist:
            matched+=1; league_matched[league]+=1
    write_csv(Path(args.out),out_cols,joined)
    audit={
      "status":"PASS_WITH_REVIEW_ITEMS" if matched < len(oracle) else "PASS",
      "generated_utc":datetime.now(timezone.utc).isoformat(),
      "join_method":"exact canonical fixture ID only",
      "oracle_rows":len(oracle),"h2h_rows":len(h2h),"joined_rows":len(joined),
      "exact_id_matches":matched,"oracle_fixtures_without_h2h_id_match":len(oracle)-matched,
      "match_rate":round(matched/len(oracle),6),
      "oracle_probability_values_modified":False,
      "production_model_logic_changed":False,
      "fuzzy_matching_used":False,
      "league_coverage":[{"league":l,"oracle_fixtures":n,"exact_h2h_matches":league_matched[l],
                          "coverage_rate":round(league_matched[l]/n,6)} for l,n in sorted(leagues.items())],
      "unmatched_fixture_ids":[r[args.oracle_id].strip() for r in oracle if r[args.oracle_id].strip() not in h2h_by_id],
      "limitations":["A missing exact-ID match is not proof no historical meeting exists.",
                     "The H2H input must represent pre-fixture history only.",
                     "This script does not calculate market performance; use a separate chronological out-of-sample backtest."]
    }
    Path(args.audit).parent.mkdir(parents=True,exist_ok=True)
    Path(args.audit).write_text(json.dumps(audit,indent=2),encoding="utf-8")
    print(json.dumps({k:audit[k] for k in ["status","oracle_rows","h2h_rows","exact_id_matches","oracle_fixtures_without_h2h_id_match","match_rate"]},indent=2))
if __name__=="__main__": main()
