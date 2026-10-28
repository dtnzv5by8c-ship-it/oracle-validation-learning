#!/usr/bin/env python3
"""Offline research-only adapter: apply reviewed identity allowlist to acquired JSONL rows.

No network access, provider calls, canonical ledger writes, or mapping inference.
"""
import argparse, csv, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from scripts.validate_current_feed_identity_contract import classify_match

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def run(input_path, allowlist_path, output_dir):
    inp, allow_path, out = Path(input_path), Path(allowlist_path), Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    config=json.loads(allow_path.read_text(encoding="utf-8"))
    entries=config.get("entries", [])
    if not isinstance(entries,list):
        raise ValueError("allowlist entries must be a list")
    allow={}
    for e in entries:
        code=str(e.get("canonical_competition_code") or "").strip()
        if not code or code in allow:
            raise ValueError("allowlist contains missing or duplicate canonical competition code")
        allow[code]=e
    accepted=out/"accepted.jsonl"
    quarantined=out/"quarantined.jsonl"
    counts={"input_rows":0,"accepted_rows":0,"quarantined_rows":0,"reasons":{}}
    with inp.open(encoding="utf-8") as src, accepted.open("w",encoding="utf-8") as ok, quarantined.open("w",encoding="utf-8") as q:
        for line_no,line in enumerate(src,1):
            if not line.strip(): continue
            row=json.loads(line); counts["input_rows"]+=1
            result=classify_match(row,allow)
            record={"source_line":line_no,"source_row":row,"identity_audit":result}
            if result["admitted"]:
                ok.write(json.dumps(record,ensure_ascii=False,sort_keys=True)+"\n")
                counts["accepted_rows"]+=1
            else:
                q.write(json.dumps(record,ensure_ascii=False,sort_keys=True)+"\n")
                counts["quarantined_rows"]+=1
                reason=result["reason"]; counts["reasons"][reason]=counts["reasons"].get(reason,0)+1
    manifest={
      "schema_version":1,"generated_utc":datetime.now(timezone.utc).isoformat(),
      "mode":"OFFLINE_RESEARCH_ONLY","network_calls_made":0,"provider_calls_made":0,
      "production_ledger_written":False,"production_eligibility":"NOT_GRANTED",
      "allowlist_entry_count":len(entries),"input_sha256":sha256(inp),"allowlist_sha256":sha256(allow_path),
      **counts,
      "accepted_sha256":sha256(accepted),"quarantined_sha256":sha256(quarantined),
      "release_policy":"Accepted rows are staging candidates only; this manifest does not approve production eligibility or official settlement truth."
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return manifest

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input-jsonl",required=True)
    p.add_argument("--allowlist-json",required=True)
    p.add_argument("--output-dir",required=True)
    a=p.parse_args()
    print(json.dumps(run(a.input_jsonl,a.allowlist_json,a.output_dir),indent=2,sort_keys=True))
if __name__=="__main__": main()
