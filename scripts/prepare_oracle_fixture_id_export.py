#!/usr/bin/env python3
"""Reporting-only adapter that exposes Oracle's canonical fixture ID.

The format deliberately mirrors scripts/prepare_prospective_four_market_publication.py
in the governed Oracle repository. It does not change predictions or model logic.
"""
import argparse, csv, json, re
from pathlib import Path

REQUIRED=("league_code","date","home_team","away_team")

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")

def canonical_fixture_id(row):
    missing=[key for key in REQUIRED if not str(row.get(key) or "").strip()]
    if missing:
        raise ValueError("Missing canonical fixture fields: "+", ".join(missing))
    return f"{row['league_code']}-{row['date']}-{slug(row['home_team'])}-{slug(row['away_team'])}"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--audit",required=True)
    args=ap.parse_args()
    with open(args.input,newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f); rows=list(reader); fields=list(reader.fieldnames or [])
    if not rows or not fields:
        raise SystemExit("Empty Oracle fixture export; refusing to publish.")
    if not set(REQUIRED).issubset(fields):
        raise SystemExit("Oracle fixture export lacks required canonical ID source fields.")
    ids=[]
    for row in rows:
        fid=canonical_fixture_id(row)
        existing=(row.get("fixture_id") or "").strip()
        if existing and existing != fid:
            raise SystemExit(f"Existing fixture_id conflicts with canonical ID for {fid}")
        ids.append(existing or fid)
    if any(not x for x in ids) or len(set(ids)) != len(ids):
        raise SystemExit("Blank or duplicate canonical fixture IDs; refusing to publish.")
    out_fields=fields if "fixture_id" in fields else ["fixture_id"]+fields
    out_rows=[]
    for row,fid in zip(rows,ids):
        out_rows.append({**row,"fixture_id":fid})
    out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=out_fields); w.writeheader(); w.writerows(out_rows)
    audit={"status":"PASS","rows":len(rows),"unique_fixture_ids":len(set(ids)),
           "id_format":"same as governed Oracle publication adapter",
           "oracle_values_changed":False,"production_model_logic_changed":False,
           "id_column":"fixture_id","id_source_fields":list(REQUIRED)}
    p=Path(args.audit); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(audit,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(audit,indent=2))

if __name__=="__main__": main()
