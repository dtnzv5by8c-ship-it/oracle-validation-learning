#!/usr/bin/env python3
"""Fetch and validate public Opta Analyst Power Rankings; report-only."""
import ast
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
import requests

URL = "https://dataviz.theanalyst.com/opta-power-rankings/index.js"
OUT = Path("artifacts/opta_power_rankings")

def parse_block(raw):
    data = json.loads(raw)
    for row in data:
        value = row.get("comps")
        if isinstance(value, str):
            try:
                row["comps"] = json.loads(value)
            except Exception:
                try:
                    row["comps"] = ast.literal_eval(value)
                except Exception:
                    row["comps"] = []
        elif not isinstance(value, list):
            row["comps"] = []
    return data

def main():
    response = requests.get(URL, timeout=30, headers={"User-Agent": "Oracle-Visual-Intelligence/1.0"})
    response.raise_for_status()
    source = response.text
    blocks = re.findall(r"JSON\.parse\(\s*\x60(.*?)\x60\s*\)", source, re.DOTALL)
    tables, parse_errors = [], []
    for idx, block in enumerate(blocks):
        try:
            rows = parse_block(block)
            if rows and isinstance(rows, list) and isinstance(rows[0], dict) and {"rank", "contestantName"}.issubset(rows[0]):
                tables.append(rows)
        except Exception as exc:
            parse_errors.append({"block": idx, "error_class": type(exc).__name__})
    if not tables:
        diagnostic = {"status": "FAILED", "http_status": response.status_code,
          "content_length": len(source), "json_parse_occurrences": source.count("JSON.parse"),
          "backtick_count": source.count(chr(96)), "candidate_blocks": len(blocks),
          "parse_errors": parse_errors[:10], "message": "Opta ranking payload could not be parsed; no values emitted."}
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "manifest.json").write_text(json.dumps(diagnostic, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(diagnostic, indent=2))
        sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {"artifact": "ORACLE-OPTA-POWER-RANKINGS-REPORT-ONLY-V1",
      "source_url": URL, "retrieved_utc": datetime.now(timezone.utc).isoformat(),
      "status": "PASS", "ranking_blocks_found": len(tables), "outputs": [],
      "governance": "Report-only. No Oracle predictions, probabilities, calibration, thresholds, or production logic changed."}
    for idx, rows in enumerate(tables[:2]):
        filename = "mens_power_rankings.csv" if idx == 0 else "womens_power_rankings.csv"
        path = OUT / filename
        fields = list(dict.fromkeys(key for row in rows for key in row))
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        manifest["outputs"].append({"file": str(path), "rows": len(rows), "columns": fields})
    men = tables[0]
    manifest["men_team_count"] = len(men)
    manifest["unique_men_team_names"] = len({str(row.get("contestantName", "")).strip().casefold() for row in men})
    manifest["rating_field_candidates"] = [key for key in men[0] if any(word in key.casefold() for word in ("rating", "score", "power"))]
    manifest["limitations"] = ["Public data asset is not proof of an official bulk API entitlement.",
      "Published rank and rating fields are preserved as-is; no rank-to-rating conversion.",
      "Team-to-fixture matching remains a separate exact-match step.",
      "Use subject to source terms and schema changes."]
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FAILED", "error_class": type(exc).__name__, "message": str(exc)[:250]}))
        sys.exit(1)
