#!/usr/bin/env python3
"""Deterministic research-only metrics for verified prediction/settlement JSONL pairs."""
import argparse, json, math
from pathlib import Path

def summarize(rows):
    counts = {"total_rows": len(rows), "settled_win_loss": 0, "unsettled": 0, "void_push_excluded": 0, "invalid_or_unmatched": 0}
    scored=[]
    for row in rows:
        try:
            p=float(row["probability"]); outcome=str(row["outcome"]).upper()
            if not math.isfinite(p) or p < 0 or p > 1 or not row.get("verified_fixture") or not row.get("verified_result_source"):
                counts["invalid_or_unmatched"] += 1; continue
            if outcome == "UNSETTLED": counts["unsettled"] += 1; continue
            if outcome in {"VOID", "PUSH"}: counts["void_push_excluded"] += 1; continue
            if outcome not in {"WIN", "LOSS"}:
                counts["invalid_or_unmatched"] += 1; continue
            actual=1 if outcome=="WIN" else 0
            scored.append((p,actual))
        except (KeyError, TypeError, ValueError):
            counts["invalid_or_unmatched"] += 1
    n=len(scored); wins=sum(y for _,y in scored)
    counts["settled_win_loss"] = n
    if n:
        brier=sum((p-y)**2 for p,y in scored)/n
        eps=1e-15
        logloss=-sum(y*math.log(max(eps,min(1-eps,p)))+(1-y)*math.log(max(eps,min(1-eps,1-p))) for p,y in scored)/n
        hit=wins/n
        bands=[]
        for lo,hi in ((0,.5),(.5,.6),(.6,.7),(.7,.8),(.8,.9),(.9,1.0000001)):
            subset=[(p,y) for p,y in scored if lo <= p < hi]
            if subset:
                bands.append({"band":f"{lo:.1f}-{min(hi,1):.1f}","n":len(subset),"mean_predicted_probability":round(sum(p for p,_ in subset)/len(subset),6),"observed_rate":round(sum(y for _,y in subset)/len(subset),6)})
        metrics={"hit_rate":round(hit,6),"hit_rate_wins":wins,"hit_rate_denominator":n,"brier_score":round(brier,6),"log_loss":round(logloss,6),"calibration_bands":bands}
    else:
        metrics={"hit_rate":None,"hit_rate_wins":0,"hit_rate_denominator":0,"brier_score":None,"log_loss":None,"calibration_bands":[]}
    return {"status":"RESEARCH_ONLY_METRICS","counts":counts,"metrics":metrics,"warning":"Metrics are valid only if input rows contain genuine immutable pre-kickoff predictions and independently verified settlements. This tool does not prove those properties."}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--input",required=True); p.add_argument("--out",required=True); a=p.parse_args()
    rows=[json.loads(line) for line in Path(a.input).read_text(encoding="utf-8").splitlines() if line.strip()]
    result=summarize(rows); Path(a.out).parent.mkdir(parents=True,exist_ok=True); Path(a.out).write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8"); print(json.dumps(result))
if __name__=="__main__": main()
