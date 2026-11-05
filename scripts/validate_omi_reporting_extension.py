#!/usr/bin/env python3
"""Fail-closed validator for the append-only Master OMI reporting extension."""
from __future__ import annotations
import argparse,csv,json
from datetime import datetime
from pathlib import Path

REQUIRED = [
    "fixture_id","oracle_win_probability","oracle_draw_probability",
    "confidence_score_pct","risk_score_pct","backtest_sample_n",
    "backtest_hit_rate_pct","backtest_brier_score","backtest_log_loss",
    "backtest_scope","backtest_asof_utc"
]

def present(v): return v is not None and str(v).strip() != ""

def pct(v, field):
    try: x=float(v)
    except (TypeError,ValueError): raise ValueError(f"{field}: invalid")
    if not 0 <= x <= 100: raise ValueError(f"{field}: outside_0_100")
    return x

def nonneg_int(v, field):
    try: x=int(v)
    except (TypeError,ValueError): raise ValueError(f"{field}: invalid")
    if x < 0: raise ValueError(f"{field}: negative")
    return x

def nonneg_float(v, field):
    try: x=float(v)
    except (TypeError,ValueError): raise ValueError(f"{field}: invalid")
    if x < 0: raise ValueError(f"{field}: negative")
    return x

def validate(rows):
    errors=[]
    if not rows: return ["empty_extension"]
    missing=[h for h in REQUIRED if h not in rows[0]]
    if missing: return ["missing_headers:"+",".join(missing)]
    ids=[str(r.get("fixture_id","")).strip() for r in rows]
    if any(not x for x in ids): errors.append("blank_fixture_id")
    if len(ids)!=len(set(ids)): errors.append("duplicate_fixture_id")
    for i,r in enumerate(rows,1):
        try:
            pct(r["oracle_win_probability"],"oracle_win_probability")
            pct(r["oracle_draw_probability"],"oracle_draw_probability")
            pct(r["confidence_score_pct"],"confidence_score_pct")
            pct(r["risk_score_pct"],"risk_score_pct")
            n=nonneg_int(r["backtest_sample_n"],"backtest_sample_n")
            if n > 0:
                pct(r["backtest_hit_rate_pct"],"backtest_hit_rate_pct")
                nonneg_float(r["backtest_brier_score"],"backtest_brier_score")
                nonneg_float(r["backtest_log_loss"],"backtest_log_loss")
                if not present(r["backtest_scope"]): raise ValueError("backtest_scope: missing")
                try:
                    datetime.fromisoformat(str(r["backtest_asof_utc"]).replace("Z","+00:00"))
                except ValueError:
                    raise ValueError("backtest_asof_utc: invalid")
        except ValueError as e:
            errors.append(f"row{i}:{e}")
    return errors

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    with open(a.input,encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    errors=validate(rows)
    result={"status":"PASS" if not errors else "BLOCK","rows":len(rows),"errors":errors,
            "governance":{"oracle_v1_6_recalculation":False,"probability_mutation":False,
                          "production_eligibility":False,"betting_eligibility":False,
                          "fail_closed":True}}
    Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if not errors else 2)

if __name__=="__main__": main()
