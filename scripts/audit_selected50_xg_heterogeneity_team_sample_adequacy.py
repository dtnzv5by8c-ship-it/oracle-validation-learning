#!/usr/bin/env python3
"""Offline Selected-50 xG heterogeneity, Belgium odds and team exposure audit.

Consumes sanitized archive/runtime CSV outputs only. No provider calls, raw rows,
settlement scoring, H2H inputs, or production writes.
"""
import argparse, csv, json, math, random
from pathlib import Path

XG_FIELDS = ("team_a_xg_prematch", "team_b_xg_prematch", "total_xg_prematch")
BE_MARKETS = ("odds_btts_yes", "odds_btts_no", "odds_doublechance_1x", "odds_doublechance_x2",
              "odds_doublechance_12", "odds_ft_1", "odds_ft_x", "odds_ft_2", "odds_ft_over25", "odds_ft_under25")

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def nint(value):
    if isinstance(value, bool): raise ValueError("boolean is not a count")
    try: x = float(str(value).strip())
    except (TypeError, ValueError): raise ValueError(f"invalid count: {value!r}") from None
    if not math.isfinite(x) or x < 0 or not x.is_integer(): raise ValueError(f"invalid count: {value!r}")
    return int(x)

def flag(value):
    s = str(value).strip().lower()
    if s in ("true", "1", "yes"): return True
    if s in ("false", "0", "no", "", "none"): return False
    raise ValueError(f"invalid boolean: {value!r}")

def wilson(k, n):
    if n < 0 or k < 0 or k > n: raise ValueError("invalid binomial counts")
    if not n: return None, None
    z=1.959963984540054; p=k/n; d=1+z*z/n
    c=(p+z*z/(2*n))/d; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return 100*max(0,c-h), 100*min(1,c+h)

def quantile(values, q):
    v=sorted(values); pos=(len(v)-1)*q; lo=math.floor(pos); hi=math.ceil(pos)
    return v[lo] if lo==hi else v[lo]*(hi-pos)+v[hi]*(pos-lo)

def audit_xg(rows, reps=10000, seed=20261030):
    seen=set(); detail=[]; summary={}; rng=random.Random(seed)
    for r in rows:
        if r.get("field_name") not in XG_FIELDS: continue
        key=(r.get("country"),r.get("competition_name"),r.get("field_name"))
        if key in seen: raise ValueError(f"duplicate xG row: {key}")
        seen.add(key)
        for f in ("current_n","current_zero","historical_n","historical_zero"): r[f]=nint(r[f])
        if not r["current_n"] or not r["historical_n"] or r["current_zero"]>r["current_n"] or r["historical_zero"]>r["historical_n"]: raise ValueError(f"invalid xG counts: {key}")
    for field in XG_FIELDS:
        group=[r for r in rows if r.get("field_name")==field]; deltas=[]; shrunk=[]; cn=cz=hn=hz=0
        for r in group:
            cr=r["current_zero"]/r["current_n"]*100; hr=r["historical_zero"]/r["historical_n"]*100
            cs=(r["current_zero"]+.5)/(r["current_n"]+1)*100; hs=(r["historical_zero"]+.5)/(r["historical_n"]+1)*100
            d=cr-hr; sd=cs-hs; deltas.append(d); shrunk.append(sd)
            cn+=r["current_n"]; cz+=r["current_zero"]; hn+=r["historical_n"]; hz+=r["historical_zero"]
            cl,ch=wilson(r["current_zero"],r["current_n"]); hl,hh=wilson(r["historical_zero"],r["historical_n"])
            detail.append({"country":r["country"],"competition_name":r["competition_name"],"field_name":field,
                "current_n":r["current_n"],"current_zero":r["current_zero"],"current_zero_pct":round(cr,4),
                "current_wilson95_low_pct":round(cl,4),"current_wilson95_high_pct":round(ch,4),
                "historical_n":r["historical_n"],"historical_zero":r["historical_zero"],"historical_zero_pct":round(hr,4),
                "historical_wilson95_low_pct":round(hl,4),"historical_wilson95_high_pct":round(hh,4),
                "raw_change_pp":round(d,4),"jeffreys_shrunk_change_pp":round(sd,4),
                "current_n_ge_50":r["current_n"]>=50,"historical_n_ge_100":r["historical_n"]>=100})
        if not group: continue
        bm=[]; bmed=[]
        for _ in range(reps):
            s=[deltas[rng.randrange(len(deltas))] for _ in deltas]
            bm.append(sum(s)/len(s)); bmed.append(quantile(s,.5))
        loo=[(sum(deltas)-x)/(len(deltas)-1) for x in deltas] if len(deltas)>1 else deltas
        summary[field]={"league_groups":len(group),"positive_raw_delta_groups":sum(x>0 for x in deltas),
            "positive_shrunk_delta_groups":sum(x>0 for x in shrunk),"median_league_delta_pp":round(quantile(deltas,.5),4),
            "mean_unweighted_delta_pp":round(sum(deltas)/len(deltas),4),
            "mean_cluster_bootstrap95_pp":[round(quantile(bm,.025),4),round(quantile(bm,.975),4)],
            "median_cluster_bootstrap95_pp":[round(quantile(bmed,.025),4),round(quantile(bmed,.975),4)],
            "mean_jeffreys_shrunk_delta_pp":round(sum(shrunk)/len(shrunk),4),
            "match_weighted_pooled_delta_pp":round(100*(cz/cn-hz/hn),4),
            "leave_one_league_out_mean_range_pp":[round(min(loo),4),round(max(loo),4)],
            "current_groups_n_below_50":sum(r["current_n"]<50 for r in group),
            "bootstrap_unit":"league group, not match rows"}
    return detail, summary

def audit_belgium(rows):
    out=[]; seen=set()
    for r in rows:
        if r.get("country")!="Belgium" or r.get("competition_name")!="Pro League" or r.get("field_name") not in BE_MARKETS: continue
        key=(r.get("scope_id"),r.get("field_name"))
        if key in seen: raise ValueError(f"duplicate Belgium scope/field: {key}")
        seen.add(key); n=nint(r.get("sample_rows")); z=nint(r.get("zero_rows"))
        if z>n: raise ValueError(f"zero count exceeds sample: {key}")
        lo,hi=wilson(z,n)
        out.append({"season_scope_id":r["scope_id"],"selected_current_season":flag(r.get("selected_current_season")),
            "market_field":r["field_name"],"sample_n":n,"zero_n":z,"positive_n":n-z,
            "zero_pct":round(100*z/n,4) if n else None,"wilson95_low_pct":round(lo,4) if lo is not None else None,
            "wilson95_high_pct":round(hi,4) if hi is not None else None,
            "season_order":"NOT_INFERRED; DATES ABSENT FROM SANITIZED INPUT"})
    return out

def audit_team(rows):
    if not rows: return [], {"status":"NO_TEAM_CONTEXT_ROWS"}
    groups={}
    for r in rows: groups.setdefault((r["country"],r["league"]),[]).append(r)
    def c(r,k): return nint(r.get(k))
    by=[]
    for (country,league),g in sorted(groups.items()):
        by.append({"country":country,"league":league,"team_role_profiles":len(g),
            "distinct_provider_team_ids":len({r["provider_team_id"] for r in g}),
            "fixture_exposures":sum(c(r,"fixture_appearances") for r in g),
            "raw_prediction_exposures":sum(c(r,"raw_prediction_appearances") for r in g),
            "blocked_exposures":sum(c(r,"blocked_appearances") for r in g),
            "profiles_with_form_below5":sum(c(r,"latest_form_n_observed")<5 for r in g),
            "profiles_with_ge3_fixture_exposures":sum(c(r,"fixture_appearances")>=3 for r in g)})
    fc=[c(r,"fixture_appearances") for r in rows]; pc=[c(r,"raw_prediction_appearances") for r in rows]
    form=[c(r,"latest_form_n_observed") for r in rows]
    def vc(k):
        d={}
        for r in rows: d[r.get(k,"")]=d.get(r.get(k,""),0)+1
        return d
    summary={"team_role_profiles":len(rows),"distinct_provider_team_ids":len({r["provider_team_id"] for r in rows}),
        "league_groups":len(groups),"fixture_exposures":sum(fc),"raw_prediction_exposures":sum(pc),
        "blocked_exposures":sum(c(r,"blocked_appearances") for r in rows),
        "feature_complete_exposures":sum(c(r,"feature_complete_appearances") for r in rows),
        "feature_incomplete_exposures":sum(c(r,"feature_incomplete_appearances") for r in rows),
        "profiles_one_fixture":sum(x==1 for x in fc),"profiles_two_fixtures":sum(x==2 for x in fc),
        "profiles_ge3_fixtures":sum(x>=3 for x in fc),"profiles_zero_raw_predictions":sum(x==0 for x in pc),
        "form_n5_profiles":sum(x==5 for x in form),"form_below5_profiles":sum(x<5 for x in form),
        "form_size_mismatches":sum(flag(r.get("latest_form_n_mismatch")) for r in rows),
        "btts_probability_exposures":sum(c(r,"btts_fixture_probability_exposures") for r in rows),
        "dc_probability_exposures":sum(c(r,"dc_team_side_probability_exposures") for r in rows),
        "canonical_join_status_counts":vc("canonical_team_join_statuses"),
        "settlement_truth_status_counts":vc("settlement_truth_statuses"),
        "calibration_status_counts":vc("calibration_statuses"),
        "interpretation":"EXPOSURES ARE NOT HISTORICAL OUTCOME SAMPLES OR TEAM-MARKET PERFORMANCE SAMPLES"}
    return by,summary

def write_csv(path, rows):
    if not rows: Path(path).write_text("\n",encoding="utf-8"); return
    with Path(path).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
    p=argparse.ArgumentParser(); p.add_argument("--xg-csv",required=True); p.add_argument("--season-csv",required=True)
    p.add_argument("--team-csv",required=True); p.add_argument("--output-dir",required=True)
    p.add_argument("--bootstrap-reps",type=int,default=10000); p.add_argument("--seed",type=int,default=20261030); a=p.parse_args()
    if a.bootstrap_reps<100: p.error("--bootstrap-reps must be >=100")
    xd,xs=audit_xg(read_csv(a.xg_csv),a.bootstrap_reps,a.seed); be=audit_belgium(read_csv(a.season_csv)); tl,ts=audit_team(read_csv(a.team_csv))
    bes={}
    for field in BE_MARKETS:
        g=[r for r in be if r["market_field"]==field]; cur=[r for r in g if r["selected_current_season"]]; old=[r for r in g if not r["selected_current_season"]]
        cn=sum(r["sample_n"] for r in cur); cz=sum(r["zero_n"] for r in cur); hn=sum(r["sample_n"] for r in old); hz=sum(r["zero_n"] for r in old)
        if cn or hn:
            cl=wilson(cz,cn); hl=wilson(hz,hn)
            bes[field]={"current_n":cn,"current_zero_n":cz,"current_zero_pct":round(100*cz/cn,4) if cn else None,
                "current_wilson95":[round(cl[0],4),round(cl[1],4)] if cn else None,
                "noncurrent_n":hn,"noncurrent_zero_n":hz,"noncurrent_zero_pct":round(100*hz/hn,4) if hn else None,
                "noncurrent_wilson95":[round(hl[0],4),round(hl[1],4)] if hn else None,
                "change_pp":round(100*(cz/cn-hz/hn),4) if cn and hn else None,
                "current_scope_ids":[r["season_scope_id"] for r in cur],"noncurrent_scope_ids":[r["season_scope_id"] for r in old]}
    summary={"status":"RESEARCH_ONLY_XG_HETEROGENEITY_AND_TEAM_SAMPLE_ADEQUACY_COMPLETE",
        "source_provenance":{
            "xg_qa38":{"run_id":41014563323,"artifact_id":12959146668,"archive_tag":"research-selected50-footystats-history-40447419806","archive_sha256":"af1d88a79f3af8019938b979bcf74869730a07bbef19a2b86df276d42226a875"},
            "season_quality_qa31":{"run_id":40995121333,"artifact_id":12951360252,"archive_tag":"research-selected50-footystats-history-40375285207","archive_sha256":"7c60a239f16dcee318cd04b031c68c07505760cb1063c1c34f368bef86844f2f"},
            "team_runtime168":{"run_id":40917698925,"artifact_id":12915559785,"runtime_archive_sha256":"e6fe86d636402e1078cdca5ae88ed211e49e78123916d3995cac4200d511d5ed"},
            "lineage_warning":"Distinct receipts; no fixture-level cross-join or archive-equivalence assumption."},
        "xg_league_heterogeneity":xs,"belgium_market_by_scope":bes,"team_sample_adequacy":ts,
        "limits":["Current and pooled non-current seasons are not matched cohorts.","Bootstrap resamples league groups, not matches; 48 clusters only.","Jeffreys shrinkage is descriptive, not feature validation.","Belgium season scope IDs are not chronologically ordered because dates are absent.","Numeric zero and positive odds are not proven valid point-in-time values.","Team fixture exposures are not historical outcome samples; canonical joins and settlement truth are unverified.","No H2H, market scoring, accuracy, calibration, ROI or betting suitability is inferred."],
        "governance":{"research_only":True,"provider_calls":0,"provider_credits":0,"h2h_holdout_accessed":False,"production_logic_changed":False,"frozen_probabilities_changed":False,"calibration_changed":False,"governance_changed":False}}
    summary["analysis_parameters"]={"bootstrap_reps":a.bootstrap_reps,"seed":a.seed,"shrinkage_prior":"Jeffreys Beta(0.5, 0.5)"}
    out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True)
    (out/"oracle_selected50_xg_league_heterogeneity_summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    write_csv(out/"oracle_selected50_xg_league_paired_deltas.csv",xd); write_csv(out/"oracle_selected50_belgium_season_scope_market_quality.csv",be); write_csv(out/"oracle_selected50_team_sample_adequacy_by_league.csv",tl)
    print(json.dumps({"status":summary["status"],"xg_fields":len(xs),"belgium_fields":len(bes),"team_role_profiles":ts.get("team_role_profiles")},sort_keys=True))

if __name__=="__main__": main()
