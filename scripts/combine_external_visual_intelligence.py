#!/usr/bin/env python3
"""Combine report-only Opta and xG layers by exact Oracle fixture_id."""
import csv, json, sys
from datetime import datetime, timezone
from pathlib import Path

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def unique_by_fixture(rows, label):
    out = {}
    for row in rows:
        fid = str(row.get("fixture_id") or "").strip()
        if not fid:
            raise ValueError(label + " contains a blank fixture_id")
        if fid in out:
            raise ValueError(label + " contains duplicate fixture_id: " + fid)
        out[fid] = row
    return out

def main():
    if len(sys.argv) != 4:
        raise SystemExit("Usage: combine_external_visual_intelligence.py <fixture_csv> <opta_fixture_csv> <xg_fixture_csv>")
    schedule, opta, xg = map(read_csv, sys.argv[1:])
    schedule_map = unique_by_fixture(schedule, "Oracle schedule")
    opta_map = unique_by_fixture(opta, "Opta layer")
    xg_map = unique_by_fixture(xg, "xG layer")
    if set(schedule_map) != set(opta_map) or set(schedule_map) != set(xg_map):
        raise ValueError("Fixture ID sets differ: schedule=%d opta=%d xg=%d" % (len(schedule_map),len(opta_map),len(xg_map)))
    core = {"league_code","date","home_team","away_team","kickoff_time","fixture_id"}
    combined = []
    for fid, base in schedule_map.items():
        row = dict(base)
        for source in (opta_map[fid], xg_map[fid]):
            for key, value in source.items():
                if key not in core:
                    if key in row and row[key] != value:
                        raise ValueError("Unexpected overlapping enrichment field: " + key)
                    row[key] = value
        combined.append(row)
    outdir = Path("artifacts/external_visual_intelligence")
    outdir.mkdir(parents=True, exist_ok=True)
    out_csv = outdir / "oracle_fixture_external_visual_intelligence.csv"
    fields = list(dict.fromkeys(k for row in combined for k in row))
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(combined)
    opta_both = sum(r.get("opta_home_match_status") == "MATCHED_EXACT_NORMALIZED" and r.get("opta_away_match_status") == "MATCHED_EXACT_NORMALIZED" for r in combined)
    xg_both = sum(r.get("home_xg_status") == "MATCHED_EXACT_NORMALIZED" and r.get("away_xg_status") == "MATCHED_EXACT_NORMALIZED" for r in combined)
    manifest = {
      "artifact": "ORACLE-EXTERNAL-VISUAL-INTELLIGENCE-V1",
      "status": "PASS",
      "mode": "REPORT_ONLY_NOT_PRODUCTION_INPUT",
      "generated_utc": datetime.now(timezone.utc).isoformat(),
      "fixture_count": len(combined),
      "unique_fixture_ids": len({r["fixture_id"] for r in combined}),
      "opta_both_team_matches": opta_both,
      "opta_both_team_coverage": opta_both/len(combined) if combined else 0,
      "xg_both_team_matches": xg_both,
      "xg_both_team_coverage": xg_both/len(combined) if combined else 0,
      "xg_feature_definition": "Current-season aggregate xG only; not last-3/last-5 form.",
      "governance": [
        "Exact fixture_id join; one row per fixture.",
        "Missing and ambiguous source matches remain explicitly unavailable.",
        "No model probabilities or production logic included or modified.",
        "No fuzzy team matching, no goals-as-xG fallback, no calibration or promotion changes."
      ],
      "output_csv": str(out_csv)
    }
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
