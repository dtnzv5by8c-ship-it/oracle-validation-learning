#!/usr/bin/env python3
"""Research-only candidate classification for provider competition aliases; never approves mappings."""
import argparse, csv, json, re
from pathlib import Path

CUP_TERMS = re.compile(r"\b(cup|copa|coppa|pokal|coupe|fa cup|league cup|super cup|supercup|shield|trophy|playoff|play off)\b", re.I)
LEAGUE_TERMS = re.compile(r"\b(league|liga|ligue|bundesliga|premier|serie [ab]|division|divisie|ekstraklasa|eredivisie|super lig|premiership|championship|psl|hnl|pro league)\b", re.I)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--crosswalk",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    with Path(a.crosswalk).open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    out=[]
    for r in rows:
        name=(r.get("provider_competition_name") or "").strip()
        n=name.casefold()
        if CUP_TERMS.search(n):
            cat="LIKELY_CUP_OR_SUPERCUP_REVIEW"
            reason="Name contains cup/trophy/playoff indicator; verify official competition format."
        elif LEAGUE_TERMS.search(n):
            cat="LIKELY_LEAGUE_REVIEW"
            reason="Name resembles a league/division; verify country, season, tier, and canonical ID."
        else:
            cat="UNRESOLVED_COMPETITION_TYPE"
            reason="Name alone is insufficient to classify competition type."
        out.append({**r,"provisional_type_classification":cat,"classification_reason":reason,
                    "human_decision":"PENDING","canonical_mapping_approved":"NO",
                    "production_eligibility":"NOT_GRANTED"})
    fields=list(out[0]) if out else ["provider_competition_name","provisional_type_classification","human_decision"]
    with Path(a.out).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(out)
    counts={}
    for r in out: counts[r["provisional_type_classification"]]=counts.get(r["provisional_type_classification"],0)+1
    summary={"status":"PROVISIONAL_ALIAS_DECISION_TABLE_BUILT","provider_names":len(out),
             "classification_counts":counts,"human_decisions_pending":len(out),
             "canonical_mapping_approved":0,"production_eligibility":"NOT_GRANTED",
             "warning":"Name-based classification is triage only, not authoritative league/cup identification."}
    Path(a.out).with_suffix(".summary.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary))
if __name__=="__main__": main()
