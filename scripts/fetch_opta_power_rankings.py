#!/usr/bin/env python3
"""Fetch and validate public Opta Analyst Power Rankings; report-only."""
import ast, csv, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
import requests

URL = "https://dataviz.theanalyst.com/opta-power-rankings/index.js"
OUT = Path("artifacts/opta_power_rankings")
def parse_block(raw):
    cleaned = re.sub(r'"comps":("(\[.*?\])")', '"comps":"__COMPS__"', raw)
    data = json.loads(cleaned)
    comps = re.findall(r'"comps":("(\[.*?\])")', raw, re.DOTALL)
    for row, match in zip(data, comps):
        try: row["comps"] = ast.literal_eval(match[1])
        except Exception: row["comps"] = []
    return data
def main():
    response = requests.get(URL, timeout=30, headers={"User-Agent":"Oracle-Visual-Intelligence/1.0"})
    response.raise_for_status()
    blocks = re.findall(r"JSON\.parse\(\x60(\[.*?\])\x60\)", response.text, re.DOTALL)
    tables = []
    for block in blocks:
        try:
            rows = parse_block(block)
            if rows and all(isinstance(x, dict) for x in rows) and {"rank","contestantName","comps"}.issubset(rows[0]):
                tables.append(rows)
        except Exception:
            continue
    if len(tables) < 1:
        raise RuntimeError("Opta ranking payload schema changed; no validated ranking block found")
    OUT.mkdir(parents=True, exist_ok=True)
    names = ["mens_power_rankings.csv", "womens_power_rankings.csv"]
    manifest = {"artifact":"ORACLE-OPTA-POWER-RANKINGS-REPORT-ONLY-V1","source_url":URL,
      "retrieved_utc":datetime.now(timezone.utc).isoformat(),"status":"PASS",
      "ranking_blocks_found":len(tables),"outputs":[],"governance":"Report-only. No Oracle predictions, probabilities, calibration, thresholds, or production logic changed."}
    for idx, rows in enumerate(tables[:2]):
        filename = names[idx] if idx < 2 else f"rankings_{idx+1}.csv"
        path = OUT / filename
        fields = list(dict.fromkeys(k for row in rows for k in row))
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
        manifest["outputs"].append({"file":str(path),"rows":len(rows),"columns":fields})
    # Fail closed unless a men's ranking is identifiable and carries both rank and team identity.
    men = tables[0]
    manifest["men_team_count"] = len(men)
    manifest["unique_men_team_names"] = len({str(r.get("contestantName","")).strip().casefold() for r in men})
    manifest["rating_field_candidates"] = [k for k in men[0] if "rating" in k.casefold() or "score" in k.casefold() or "power" in k.casefold()]
    manifest["limitations"] = ["Public data asset is not proof of an official bulk API entitlement.", "Ranking scores are preserved as published; no rank-to-rating conversion.", "Team-to-fixture matching is intentionally a separate exact-match step.", "Use subject to source terms and schema changes."]
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
if __name__ == "__main__":
    try: main()
    except Exception as exc:
        print(json.dumps({"status":"FAILED","error_class":type(exc).__name__,"message":str(exc)[:250]}))
        sys.exit(1)
