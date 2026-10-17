#!/usr/bin/env python3
"""Development-only prospective shadow settlement; never writes to Oracle ledgers."""
import argparse, csv, json, math, sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_h2h_report import team

SUPPORTED = {"BTTS_YES", "HOME_1X", "AWAY_X2", "HOME_1X_U45", "AWAY_X2_U45"}

def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def parse_dt(value):
    s = str(value or "").strip()
    if not s:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def kickoff(row):
    d = str(row.get("fixture_date") or "").strip()
    t = str(row.get("kickoff_time") or "").strip()
    if not d or not t:
        return None
    return parse_dt(d + "T" + t)

def match_key(row):
    return (
        str(row.get("league_code") or row.get("competition") or "").strip(),
        str(row.get("date") or "")[:10],
        team(row.get("home_team", "")),
        team(row.get("away_team", "")),
    )

def truth_for(market, hg, ag):
    total = hg + ag
    if market == "BTTS_YES": return int(hg > 0 and ag > 0)
    if market == "HOME_1X": return int(hg >= ag)
    if market == "AWAY_X2": return int(ag >= hg)
    if market == "HOME_1X_U45": return int(hg >= ag and total <= 4)
    if market == "AWAY_X2_U45": return int(ag >= hg and total <= 4)
    raise ValueError("Unsupported market: " + market)

def logloss(p, y):
    p = min(max(p, 1e-15), 1 - 1e-15)
    return -math.log(p) if y else -math.log(1 - p)

def summarize(rows, group_fields):
    groups = defaultdict(list)
    for r in rows:
        if r["settlement_status"] == "SETTLED":
            groups[tuple(r.get(k, "") for k in group_fields)].append(r)
    out = []
    for key, items in sorted(groups.items()):
        n = len(items)
        hits = sum(int(x["prediction_hit"]) for x in items)
        selected = [x for x in items if x["decision"] != "NO_BET"]
        out.append({
            **dict(zip(group_fields, key)),
            "settled_predictions": n,
            "classification_hits_at_50pct": hits,
            "classification_accuracy_pct": round(100 * hits / n, 2) if n else None,
            "brier_score": round(sum(float(x["brier_score"]) for x in items) / n, 6) if n else None,
            "log_loss": round(sum(float(x["log_loss"]) for x in items) / n, 6) if n else None,
            "non_no_bet_predictions": len(selected),
            "non_no_bet_hit_rate_pct": round(100 * sum(int(x["prediction_hit"]) for x in selected) / len(selected), 2) if selected else None,
        })
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--predictions", required=True)
    ap.add_argument("--matches", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    preds = read_csv(a.predictions)
    matches = read_csv(a.matches)
    outdir = Path(a.out_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    required_p = {"prediction_id","fixture_id","competition","fixture_date","kickoff_time","home_team","away_team","prediction_timestamp","raw_probability","decision","selection"}
    required_m = {"date","league_code","home_team","away_team","home_goals","away_goals"}
    if not preds or required_p - set(preds[0]):
        raise SystemExit("DATA_GATED: prediction ledger is empty or missing required immutable prediction fields")
    if not matches or required_m - set(matches[0]):
        raise SystemExit("DATA_GATED: merged historical match archive is empty or missing result fields")
    if len({r["prediction_id"] for r in preds}) != len(preds):
        raise SystemExit("DATA_GATED: duplicate prediction_id values; refusing to score ambiguous records")

    result_groups = defaultdict(list)
    for m in matches:
        try:
            hg, ag = int(float(m["home_goals"])), int(float(m["away_goals"]))
        except (ValueError, TypeError):
            continue
        if not m.get("home_team") or not m.get("away_team") or not m.get("date"):
            continue
        result_groups[match_key(m)].append((hg, ag, m.get("date","")[:10]))

    result_lookup = {}
    ambiguous = set()
    for key, vals in result_groups.items():
        distinct = {(x[0], x[1]) for x in vals}
        if len(distinct) == 1:
            result_lookup[key] = vals[0]
        else:
            ambiguous.add(key)

    settled = []
    chronology_failures = 0
    unsupported = 0
    for p in preds:
        market = str(p.get("selection") or "").strip()
        prob_text = str(p.get("raw_probability") or "").strip()
        status = "UNSETTLED"
        detail = ""
        y = hg = ag = None
        brier = ll = hit = ""
        try:
            prob = float(prob_text)
            if not 0 <= prob <= 1: raise ValueError()
        except Exception:
            prob = None
            status = "INVALID_PROBABILITY"
            detail = "raw_probability missing or outside [0,1]"
        kt = kickoff(p)
        pt = parse_dt(p.get("prediction_timestamp"))
        if status == "UNSETTLED" and (not kt or not pt or pt >= kt):
            status = "CHRONOLOGY_FAIL"
            detail = "Missing timestamp or prediction timestamp is not strictly before kickoff"
            chronology_failures += 1
        if status == "UNSETTLED" and market not in SUPPORTED:
            status = "UNSUPPORTED_MARKET"
            detail = "No governed truth formula for this market"
            unsupported += 1
        key = (str(p.get("competition") or "").strip(), str(p.get("fixture_date") or "")[:10], team(p.get("home_team","")), team(p.get("away_team","")))
        if status == "UNSETTLED":
            if key in ambiguous:
                status = "AMBIGUOUS_RESULT"
                detail = "Multiple conflicting scores found for the exact league/date/home/away key"
            elif key not in result_lookup:
                status = "RESULT_NOT_FOUND"
                detail = "No exact league/date/home/away result in merged archive"
            else:
                hg, ag, result_date = result_lookup[key]
                y = truth_for(market, hg, ag)
                hit = int((prob >= 0.5) == bool(y))
                brier = round((prob - y) ** 2, 8)
                ll = round(logloss(prob, y), 8)
                status = "SETTLED"
                detail = "Development-only shadow settlement from exact league/date/team identity; no ledger written"
        settled.append({
            "prediction_id": p.get("prediction_id",""), "run_id": p.get("run_id",""),
            "fixture_id": p.get("fixture_id",""), "competition": p.get("competition",""),
            "fixture_date": p.get("fixture_date",""), "home_team": p.get("home_team",""),
            "away_team": p.get("away_team",""), "market": market,
            "prediction_timestamp": p.get("prediction_timestamp",""), "kickoff_time": p.get("kickoff_time",""),
            "model": p.get("model",""), "model_version": p.get("model_version",""),
            "model_status": p.get("model_status",""), "decision": p.get("decision",""),
            "raw_probability": prob if prob is not None else "",
            "final_home_score": hg if hg is not None else "", "final_away_score": ag if ag is not None else "",
            "actual_truth": y if y is not None else "", "prediction_hit": hit,
            "brier_score": brier, "log_loss": ll, "settlement_status": status, "diagnostic": detail,
        })
    fields = list(settled[0].keys()) if settled else []
    with (outdir / "prospective_shadow_settlements.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(settled)
    market_summary = summarize(settled, ["market"])
    league_market_summary = summarize(settled, ["competition","market"])
    for name, data in [("prospective_shadow_market_summary.csv", market_summary), ("prospective_shadow_league_market_summary.csv", league_market_summary)]:
        with (outdir / name).open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0].keys()) if data else ["market"]); w.writeheader(); w.writerows(data)
    counts = defaultdict(int)
    for r in settled: counts[r["settlement_status"]] += 1
    n = len(settled); sn = counts["SETTLED"]
    summary = {
        "artifact": "ORACLE_PROSPECTIVE_CHALLENGER_SHADOW_SETTLEMENT_V1.0",
        "status": "PRELIMINARY_SHADOW_EVALUATION" if sn else "DATA_GATED",
        "production_model_changed": False, "canonical_ledgers_written": False,
        "prediction_rows": n, "unique_fixtures": len({r["fixture_id"] for r in settled}),
        "settled_prediction_rows": sn, "settlement_coverage_pct": round(100*sn/n,2) if n else 0,
        "unsettled_by_status": dict(counts), "chronology_failures": chronology_failures,
        "unsupported_market_rows": unsupported,
        "interpretation": "Exploratory prospective challenger evaluation only. Not a production backtest or promotion decision. A small cohort and a single historical result source cannot establish durable predictive lift; validate source coverage and accumulate more pre-kickoff observations.",
        "markets": sorted(SUPPORTED),
        "metrics": ["classification accuracy at 0.5 threshold", "Brier score", "log loss", "non-NO_BET hit rate"],
    }
    (outdir / "prospective_shadow_settlement_audit.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
