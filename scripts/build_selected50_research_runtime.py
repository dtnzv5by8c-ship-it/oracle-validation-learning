#!/usr/bin/env python3
"""Isolated Selected-50 research runtime. Production scripts and probabilities are untouched."""
import bisect, csv, datetime as dt, hashlib, json, math, os, re, zipfile
from collections import Counter, defaultdict
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import brier_score_loss, log_loss, accuracy_score, roc_auc_score

ARCHIVE = Path(os.environ.get("ORACLE_ARCHIVE", "private-download/oracle-selected50-footystats-private-ingestion.zip"))
MANIFEST = Path("data/oracle-footystats-selected-50-season-id-manifest.csv")
OUT = Path("selected50_runtime_output")
OUT.mkdir(exist_ok=True)
PRIMARY_START = dt.datetime(2025, 3, 20, tzinfo=dt.timezone.utc).timestamp()
PRIMARY_END = dt.datetime(2026, 9, 21, tzinfo=dt.timezone.utc).timestamp()
NOW = dt.datetime.now(dt.timezone.utc).timestamp()
FINISHED = {"complete","completed","finished","full time","full-time","ft","ended","played"}
CANCELLED = {"cancelled","canceled","abandoned","postponed","suspended","void"}
FEATURES = [
 "home_gf5","home_ga5","home_btts5","home_fts5","home_cs5","home_shots5","home_sot5",
 "away_gf5","away_ga5","away_btts5","away_fts5","away_cs5","away_shots5","away_sot5",
 "pair_btts_mean","pair_fts_mean","pair_cs_mean","score_environment","shot_environment","score_gap5"
]
MARKETS = {
 "BTTS": lambda h,a: int(h>0 and a>0),
 "DC_HOME": lambda h,a: int(h>=a),
 "DC_AWAY": lambda h,a: int(a>=h),
 "COMBO_HOME": lambda h,a: int(h>=a and 2 <= h+a <= 4),
 "COMBO_AWAY": lambda h,a: int(a>=h and 2 <= h+a <= 4),
}

def wilson_interval(successes, n, z=1.959963984540054):
    """Two-sided 95% Wilson interval for a binomial proportion; descriptive only."""
    if n <= 0:
        return None, None
    p = successes / n
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    half = z * math.sqrt((p*(1-p) + z*z/(4*n))/n) / denom
    return max(0.0, center-half), min(1.0, center+half)

def read_json(z, name):
    try: return json.loads(z.read(name).decode("utf-8"))
    except Exception: return None

def as_list(v):
    if isinstance(v,list): return v
    if isinstance(v,dict):
        for k in ("data","matches","teams","table","overall","home","away"):
            if isinstance(v.get(k),list): return v[k]
    return []

def stamp(m):
    for k in ("date_unix","kickoff_unix","timestamp","kickoff","date","datetime","match_date"):
        v=m.get(k) if isinstance(m,dict) else None
        if v in (None,""): continue
        try:
            n=float(v)
            if n > 1_000_000_000: return n
        except (TypeError,ValueError): pass
        try:
            x=dt.datetime.fromisoformat(str(v).replace("Z","+00:00"))
            if x.tzinfo is None: x=x.replace(tzinfo=dt.timezone.utc)
            return x.timestamp()
        except Exception: pass
    return None

def num(v):
    try:
        n=float(v)
        return n if math.isfinite(n) and n >= 0 else None
    except (TypeError,ValueError): return None

def get_first(row, keys):
    for k in keys:
        if row.get(k) not in (None,""): return row.get(k)
    return None

def match_score(m):
    h=num(get_first(m,("homeGoalCount","home_goals","home_score")))
    a=num(get_first(m,("awayGoalCount","away_goals","away_score")))
    return h,a

def finished(m):
    status=str(get_first(m,("status","game_status")) or "").strip().lower()
    h,a=match_score(m)
    return status in FINISHED and h is not None and a is not None

def team_ids(m):
    h=get_first(m,("homeID","home_id","home_team_id"))
    a=get_first(m,("awayID","away_id","away_team_id"))
    return (str(h) if h is not None else "", str(a) if a is not None else "")

def form_features(home_hist, away_hist):
    # Histories are already sorted and contain only completed fixtures strictly before target kickoff.
    def summarize(rows, side):
        last=rows[-5:]
        if len(last)<5: return {f"{side}_{k}":None for k in ("gf5","ga5","btts5","fts5","cs5","shots5","sot5")}
        gf=[]; ga=[]; btts=[]; fts=[]; cs=[]; shots=[]; sot=[]
        for m, is_home in last:
            h,a=match_score(m)
            if h is None or a is None: continue
            own,opp=(h,a) if is_home else (a,h)
            gf.append(own); ga.append(opp); btts.append(int(h>0 and a>0))
            fts.append(int(own==0)); cs.append(int(opp==0))
            sk=("team_a_shots" if is_home else "team_b_shots")
            sok=("team_a_shotsOnTarget" if is_home else "team_b_shotsOnTarget")
            shots.append(num(m.get(sk))); sot.append(num(m.get(sok)))
        if len(gf)<5: return {f"{side}_{k}":None for k in ("gf5","ga5","btts5","fts5","cs5","shots5","sot5")}
        def mean(vals):
            vals=[v for v in vals if v is not None]
            return sum(vals)/len(vals) if vals else None
        return {f"{side}_gf5":mean(gf),f"{side}_ga5":mean(ga),f"{side}_btts5":mean(btts),
                f"{side}_fts5":mean(fts),f"{side}_cs5":mean(cs),f"{side}_shots5":mean(shots),f"{side}_sot5":mean(sot)}
    x={}; x.update(summarize(home_hist,"home")); x.update(summarize(away_hist,"away"))
    h=x.get("home_"); # keep feature derivation explicit and auditable
    def avg(keys):
        vals=[x.get(k) for k in keys]
        return sum(vals)/len(vals) if all(v is not None for v in vals) else None
    x["pair_btts_mean"]=avg(["home_btts5","away_btts5"])
    x["pair_fts_mean"]=avg(["home_fts5","away_fts5"])
    x["pair_cs_mean"]=avg(["home_cs5","away_cs5"])
    x["score_environment"]=avg(["home_gf5","home_ga5","away_gf5","away_ga5"])
    x["shot_environment"]=avg(["home_sot5","away_sot5"])
    if all(x.get(k) is not None for k in ("home_gf5","home_ga5","away_gf5","away_ga5")):
        x["score_gap5"]=(x["home_gf5"]-x["home_ga5"])-(x["away_gf5"]-x["away_ga5"])
    else: x["score_gap5"]=None
    return x

def make_model(rows, market):
    valid=[r for r in rows if r["target_"+market] is not None and all(r.get(f) is not None for f in FEATURES)]
    if len(valid)<300 or len({r["target_"+market] for r in valid})<2: return None,len(valid)
    X=[[float(r[f]) for f in FEATURES] for r in valid]
    y=[int(r["target_"+market]) for r in valid]
    model=Pipeline([("scale",StandardScaler()),("lr",LogisticRegression(max_iter=2000,C=0.5,random_state=42))])
    model.fit(X,y)
    return model,len(valid)

def predict(model, feature):
    if model is None or any(feature.get(f) is None for f in FEATURES): return None
    return float(model.predict_proba([[float(feature[f]) for f in FEATURES]])[0,1])

def main():
    selected=list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig",newline="")))
    selected_by_id={str(r.get("selected_id","")).strip():r for r in selected}
    if len(selected)!=50 or len(selected_by_id)!=50 or "" in selected_by_id: raise SystemExit("Selected-50 manifest is not exactly 50 unique IDs.")
    with zipfile.ZipFile(ARCHIVE) as z:
        names=set(z.namelist())
        mn=next((n for n in names if n.endswith("ingestion_manifest.json")),None)
        if not mn: raise SystemExit("Private ingestion manifest missing.")
        raw_manifest=read_json(z,mn)
        if not isinstance(raw_manifest,list): raise SystemExit("Unexpected private ingestion manifest shape.")
        season_rows={str(r.get("season_id","")).strip():r for r in raw_manifest if isinstance(r,dict)}
        if len(season_rows)<200: raise SystemExit(f"Expected historical archive with at least 200 season rows; got {len(season_rows)}.")
        # Canonical competition crosswalk uses exact country + competition labels already audited
        # against all 200 provider season rows. The provider catalogue does not expose a usable parent ID.
        selected_by_label={}
        for selected_sid, sel in selected_by_id.items():
            label=(str(sel.get("country","")).strip(),str(sel.get("competition_name","")).strip())
            if not all(label) or label in selected_by_label:
                raise SystemExit("Selected-50 country/competition labels are blank or non-unique; fail closed.")
            selected_by_label[label]=(selected_sid,sel)
            meta=season_rows.get(selected_sid)
            if not meta: raise SystemExit(f"Selected season ID {selected_sid} missing from private archive.")
            if (str(meta.get("selected_country","")).strip(),str(meta.get("selected_competition_name","")).strip()) != label:
                raise SystemExit(f"Selected season ID {selected_sid} label crosswalk mismatch; fail closed.")
        if len(selected_by_label)!=50: raise SystemExit(f"Expected 50 exact country/competition labels; found {len(selected_by_label)}.")
        comp_meta={selected_sid:sel for selected_sid,sel in selected_by_id.items()}
        all_matches=[]; crosswalk=[]; season_qa=[]; team_position={}; season_team_names={}
        mapped_historical_seasons=0
        for sid,meta in season_rows.items():
            label=(str(meta.get("selected_country","")).strip(),str(meta.get("selected_competition_name","")).strip())
            mapped=selected_by_label.get(label)
            if not mapped: continue
            cid,sel=mapped
            mapped_historical_seasons+=1
            base=f"seasons/{sid}/"
            mp=next((n for n in names if n.endswith(base+"matches.json")),None)
            tp=next((n for n in names if n.endswith(base+"teams.json")),None)
            tabp=next((n for n in names if n.endswith(base+"tables.json")),None)
            if not mp or not tp:
                season_qa.append({"season_id":sid,"selected_competition":sel["competition_name"],"status":"MISSING_MATCH_OR_TEAM_FILE","match_count":0})
                continue
            matches=read_json(z,mp); teams=read_json(z,tp); tables=read_json(z,tabp) if tabp else None
            if not isinstance(matches,list) or not isinstance(teams,list):
                season_qa.append({"season_id":sid,"selected_competition":sel["competition_name"],"status":"UNEXPECTED_CONTAINER_SHAPE","match_count":0})
                continue
            for t in teams:
                if not isinstance(t,dict) or t.get("id") is None: continue
                team_name = t.get("name") or t.get("english_name") or t.get("cleanName") or ""
                season_team_names[(cid,sid,str(t["id"]))] = team_name
                if sid in selected_by_id:
                    table_pos=num(t.get("table_position"))
                    team_position[(cid,str(t["id"]))]={"name":team_name,
                                                       "table_position":table_pos if table_pos is not None and table_pos > 0 else None,
                                                       "season_id":sid}
            # Table payload is not assumed to be historical; only current selected season team records are displayed.
            for m in matches:
                if not isinstance(m,dict): continue
                h,a=team_ids(m)
                home_name=str(get_first(m,("home_name","home_team_name")) or "")
                away_name=str(get_first(m,("away_name","away_team_name")) or "")
                if not home_name and h: home_name=str(season_team_names.get((cid,sid,h),team_position.get((cid,h),{}).get("name","")))
                if not away_name and a: away_name=str(season_team_names.get((cid,sid,a),team_position.get((cid,a),{}).get("name","")))
                ts=stamp(m)
                if ts is None or not h or not a: continue
                row={"fixture_id":str(m.get("id") or ""), "season_id":sid,"competition_id":cid,
                     "country":sel["country"],"league":sel["competition_name"],"home_id":h,"away_id":a,
                     "home_team":home_name,"away_team":away_name,"kickoff_unix":ts,
                     "status":str(get_first(m,("status","game_status")) or ""),
                     "home_goals":match_score(m)[0],"away_goals":match_score(m)[1],
                     "finished":finished(m),"raw_match":m}
                all_matches.append(row)
            season_qa.append({"season_id":sid,"selected_competition":sel["competition_name"],"status":"INGESTED","match_count":len(matches),"team_count":len(teams)})
        # Fail closed on unresolved competition mapping or gross archive loss.
        present_comps={r["competition_id"] for r in all_matches}
        if len(present_comps)!=50: raise SystemExit(f"Only {len(present_comps)} of 50 selected competitions yielded matches.")
        # Deduplicate by competition + fixture ID only; identical IDs across comps are distinct provider namespace.
        dedup={}
        for r in all_matches:
            key=(r["competition_id"],r["fixture_id"]) if r["fixture_id"] else (r["competition_id"],r["season_id"],r["kickoff_unix"],r["home_id"],r["away_id"])
            dedup.setdefault(key,r)
        matches=sorted(dedup.values(),key=lambda r:(r["competition_id"],r["kickoff_unix"],r["fixture_id"]))
        # Histories contain only explicit completed matches with valid scores.
        home_history=defaultdict(list); away_history=defaultdict(list); h2h_history=defaultdict(list)
        for r in matches:
            if not r["finished"]: continue
            if r["home_goals"] is None or r["away_goals"] is None: continue
            comp=r["competition_id"]; hkey=(comp,r["home_id"]); akey=(comp,r["away_id"])
            home_history[hkey].append((r["kickoff_unix"],r["raw_match"],True))
            away_history[akey].append((r["kickoff_unix"],r["raw_match"],False))
            pair=(comp,*sorted((r["home_id"],r["away_id"])))
            h2h_history[pair].append((r["kickoff_unix"],r))
        for hist in list(home_history.values())+list(away_history.values()):
            hist.sort(key=lambda x:x[0])
        for hist in h2h_history.values(): hist.sort(key=lambda x:x[0])
        def history_before(hist, ts):
            times=[x[0] for x in hist]
            return [x[1:] for x in hist[:bisect.bisect_left(times,ts)]]
        feature_rows=[]; targets_by_id={}
        for r in matches:
            comp=r["competition_id"]; ts=r["kickoff_unix"]
            hh=history_before(home_history[(comp,r["home_id"])],ts)
            ah=history_before(away_history[(comp,r["away_id"])],ts)
            f=form_features(hh,ah)
            h2h_all=h2h_history[(comp,*sorted((r["home_id"],r["away_id"])))]
            h2h_cut=bisect.bisect_left([x[0] for x in h2h_all],ts)
            h2h=h2h_all[:h2h_cut]
            last_h2h=h2h[-5:]
            h2h_btts=[]; h2h_home_results=[]; h2h_goals=[]
            for (_, old) in last_h2h:
                oh,oa=old["home_goals"],old["away_goals"]
                h2h_btts.append(int(oh>0 and oa>0)); h2h_goals.append(oh+oa)
                if old["home_id"]==r["home_id"]: rel= "W" if oh>oa else "D" if oh==oa else "L"
                else: rel= "W" if oa>oh else "D" if oa==oh else "L"
                h2h_home_results.append(rel)
            f.update({"fixture_id":r["fixture_id"],"season_id":r["season_id"],"competition_id":comp,"country":r["country"],
                      "league":r["league"],"kickoff_unix":ts,"date_utc":dt.datetime.fromtimestamp(ts,dt.timezone.utc).isoformat(),
                      "home_team":r["home_team"],"away_team":r["away_team"],"home_id":r["home_id"],"away_id":r["away_id"],
                      "status":r["status"],"finished":r["finished"],"home_goals":r["home_goals"],"away_goals":r["away_goals"],
                      "home_recent5_results":"".join("W" if match_score(m)[0]>match_score(m)[1] else "D" if match_score(m)[0]==match_score(m)[1] else "L" for m,is_home in hh[-5:]),
                      "away_recent5_results":"".join("W" if match_score(m)[1]>match_score(m)[0] else "D" if match_score(m)[1]==match_score(m)[0] else "L" for m,is_home in ah[-5:]),
                      "home_recent5_n":len(hh[-5:]),"away_recent5_n":len(ah[-5:]),
                      "h2h_prior_n":len(h2h),"h2h_last5_results_home_perspective":"".join(h2h_home_results),
                      "h2h_btts_rate_last5":sum(h2h_btts)/len(h2h_btts) if h2h_btts else None,
                      "h2h_avg_total_goals_last5":sum(h2h_goals)/len(h2h_goals) if h2h_goals else None,
                      "h2h_last_date_utc":dt.datetime.fromtimestamp(last_h2h[-1][0],dt.timezone.utc).isoformat() if last_h2h else ""})
            # Current table snapshot is display-only and never used as a historical training feature.
            f["home_table_position_current"]=team_position.get((comp,r["home_id"]),{}).get("table_position")
            f["away_table_position_current"]=team_position.get((comp,r["away_id"]),{}).get("table_position")
            f["table_position_asof_status"]="CURRENT_PROVIDER_TEAM_SNAPSHOT_NOT_HISTORICAL" if (f["home_table_position_current"] is not None and f["away_table_position_current"] is not None) else "TABLE_POSITION_MISSING_OR_UNVERIFIED"
            raw=r["raw_match"]
            f["odds_named_field_count"]=sum("odds" in k.lower() and raw.get(k) not in (None,"") for k in raw)
            f["xg_named_field_count"]=sum("xg" in k.lower() and raw.get(k) not in (None,"") for k in raw)
            f["odds_xg_provenance_status"]="UNVERIFIED_NOT_USED_IN_MODEL"
            f["model_input_coverage_pct"]=round(100*sum(f.get(k) is not None for k in FEATURES)/len(FEATURES),1)
            f["model_input_missingness_pct"]=round(100-f["model_input_coverage_pct"],1)
            # Overall confidence/risk cannot be reduced to feature completeness: probabilities are uncalibrated
            # and odds/xG provenance is unverified. Do not fabricate a confidence percentage or risk percentage.
            f["confidence_score_pct"]=None
            f["data_risk_pct"]=None
            f["risk_profile"]="HIGH_UNVALIDATED" if all(f.get(k) is not None for k in FEATURES) else "CRITICAL_INCOMPLETE_INPUTS"
            if r["finished"] and r["home_goals"] is not None and r["away_goals"] is not None:
                for market,fn in MARKETS.items(): f["target_"+market]=fn(r["home_goals"],r["away_goals"])
            else:
                for market in MARKETS: f["target_"+market]=None
            feature_rows.append(f)
        train_rows=[r for r in feature_rows if r.get("finished") and r.get("kickoff_unix",NOW)>=0]
        # Historical validation window: model is trained only before 20 March 2025.
        train_pre=[r for r in train_rows if r["kickoff_unix"]<PRIMARY_START]
        test_rows=[r for r in train_rows if PRIMARY_START<=r["kickoff_unix"]<PRIMARY_END]
        backtest=[]; backtest_preds={}
        for market in MARKETS:
            model,ntrain=make_model(train_pre,market)
            eligible=[r for r in test_rows if r.get("target_"+market) is not None and all(r.get(f) is not None for f in FEATURES)]
            if model is None or not eligible:
                backtest.append({"market":market,"status":"INSUFFICIENT_TRAIN_OR_TEST","train_n":ntrain,"test_n":len(eligible),"brier":None,"log_loss":None,"accuracy_at_0_5":None,"auc":None})
                continue
            probs=[predict(model,r) for r in eligible]; y=[r["target_"+market] for r in eligible]
            pairs=[(p,t) for p,t in zip(probs,y) if p is not None]
            probs=[p for p,t in pairs]; y=[t for p,t in pairs]
            if not probs:
                backtest.append({"market":market,"status":"NO_VALID_PREDICTIONS","train_n":ntrain,"test_n":0,"brier":None,"log_loss":None,"accuracy_at_0_5":None,"auc":None}); continue
            try: auc=roc_auc_score(y,probs) if len(set(y))==2 else None
            except Exception: auc=None
            # Leakage-safe reference baselines use training labels only, never test prevalence.
            baseline_train=[r for r in train_pre if r.get("target_"+market) is not None and all(r.get(f) is not None for f in FEATURES)]
            train_prev=(sum(int(r["target_"+market]) for r in baseline_train)/len(baseline_train)) if baseline_train else None
            majority_class=int(train_prev>=0.5) if train_prev is not None else None
            baseline_probs=[train_prev]*len(y) if train_prev is not None else []
            baseline_brier=round(brier_score_loss(y,baseline_probs),5) if baseline_probs else None
            baseline_logloss=round(log_loss(y,[min(max(p,1e-6),1-1e-6) for p in baseline_probs],labels=[0,1]),5) if baseline_probs else None
            baseline_accuracy=round(accuracy_score(y,[majority_class]*len(y)),5) if majority_class is not None else None
            # Reliability bins and ECE are diagnostics only; no calibration is applied to outputs.
            bins=[]; ece=0.0
            for bi in range(10):
                lo=bi/10; hi=(bi+1)/10
                idx=[i for i,p in enumerate(probs) if (p>=lo and (p<hi or (bi==9 and p<=hi)))]
                if not idx: continue
                mean_p=sum(probs[i] for i in idx)/len(idx)
                observed=sum(y[i] for i in idx)/len(idx)
                ece += len(idx)/len(y)*abs(mean_p-observed)
                bins.append({"bin_lower":lo,"bin_upper":hi,"n":len(idx),"mean_predicted_probability":round(mean_p,5),"observed_rate":round(observed,5)})
            per_league=[]
            league_names=sorted(set(str(r.get("league") or "UNKNOWN") for r in eligible))
            for league_name in league_names:
                inds=[i for i,r in enumerate(eligible) if str(r.get("league") or "UNKNOWN")==league_name]
                ly=[y[i] for i in inds]; lp=[probs[i] for i in inds]
                per_league.append({"league":league_name,"test_n":len(inds),
                    "positive_rate":round(sum(ly)/len(ly),5) if ly else None,
                    "accuracy_at_0_5":round(accuracy_score(ly,[int(p>=0.5) for p in lp]),5) if ly else None,
                    "brier":round(brier_score_loss(ly,lp),5) if ly else None,
                    "auc":round(roc_auc_score(ly,lp),5) if len(set(ly))==2 else None})
            backtest.append({"market":market,"status":"RAW_WALK_FORWARD_HOLDOUT_NOT_CALIBRATED","train_n":ntrain,"test_n":len(y),
                             "brier":round(brier_score_loss(y,probs),5),"log_loss":round(log_loss(y,[min(max(p,1e-6),1-1e-6) for p in probs],labels=[0,1]),5),
                             "accuracy_at_0_5":round(accuracy_score(y,[int(p>=0.5) for p in probs]),5),"auc":round(auc,5) if auc is not None else None,
                             "training_prevalence":round(train_prev,5) if train_prev is not None else None,
                             "baseline_majority_class":majority_class,"baseline_accuracy":baseline_accuracy,
                             "baseline_constant_probability_brier":baseline_brier,"baseline_constant_probability_log_loss":baseline_logloss,
                             "expected_calibration_error_10_bins":round(ece,5),"reliability_bins":bins,
                             "per_league_test_metrics":per_league})
        # Decision report horizon: next seven days only. Exclude fixtures with less than 15 minutes of lead time.
        report_start=NOW+15*60
        report_end=NOW+7*24*60*60
        future=[r for r in matches if report_start < r["kickoff_unix"] <= report_end
                and not r["finished"] and str(r["status"]).strip().lower() not in CANCELLED]
        # Explicit 50-competition schedule coverage. Absence from the seven-day window
        # is not treated as missing data; it is flagged for schedule/freshness reconciliation.
        schedule_coverage=[]
        for selected_id, sel in sorted(selected_by_id.items(), key=lambda kv: (kv[1].get("country",""),kv[1].get("competition_name",""))):
            comp_rows=[r for r in matches if str(r["competition_id"])==selected_id]
            comp_future=[r for r in future if str(r["competition_id"])==selected_id]
            future_times=sorted(r["kickoff_unix"] for r in comp_future)
            schedule_coverage.append({
                "selected_id":selected_id,"country":sel.get("country",""),"competition_name":sel.get("competition_name",""),
                "archive_match_rows":len(comp_rows),"completed_match_rows":sum(1 for r in comp_rows if r["finished"]),
                "upcoming_fixture_count_7d":len(comp_future),
                "first_upcoming_kickoff_utc":dt.datetime.fromtimestamp(future_times[0],dt.timezone.utc).isoformat() if future_times else "",
                "last_upcoming_kickoff_utc":dt.datetime.fromtimestamp(future_times[-1],dt.timezone.utc).isoformat() if future_times else "",
                "schedule_coverage_status":"FIXTURES_FOUND" if comp_future else "NO_FIXTURE_IN_7D_HORIZON_CHECK_SCHEDULE_FRESHNESS",
                "production_eligible":"NO"
            })
        # One pooled model per market, trained only on completed records before each target kickoff.
        predictions=[]
        by_date=defaultdict(list)
        for r in future: by_date[dt.datetime.fromtimestamp(r["kickoff_unix"],dt.timezone.utc).date().isoformat()].append(r)
        for date in sorted(by_date):
            targets=by_date[date]
            cutoff=min(r["kickoff_unix"] for r in targets)
            eligible_train=[r for r in train_rows if r["kickoff_unix"]<cutoff]
            models={m:make_model(eligible_train,m)[0] for m in MARKETS}
            for r in targets:
                f=next((x for x in feature_rows if x.get("fixture_id")==r["fixture_id"] and x.get("competition_id")==r["competition_id"] and x.get("kickoff_unix")==r["kickoff_unix"]),None)
                if not f: continue
                row={"fixture_id":r["fixture_id"],"date_utc":dt.datetime.fromtimestamp(r["kickoff_unix"],dt.timezone.utc).isoformat(),
                     "country":r["country"],"league":r["league"],"home_team":r["home_team"],"away_team":r["away_team"],
                     "home_recent5_results":f["home_recent5_results"],"away_recent5_results":f["away_recent5_results"],
                     "home_recent5_n":f["home_recent5_n"],"away_recent5_n":f["away_recent5_n"],
                     "h2h_prior_n":f["h2h_prior_n"],"h2h_last5_results_home_perspective":f["h2h_last5_results_home_perspective"],
                     "h2h_btts_rate_last5":f["h2h_btts_rate_last5"],"h2h_avg_total_goals_last5":f["h2h_avg_total_goals_last5"],
                     "h2h_last_date_utc":f["h2h_last_date_utc"],
                     "home_table_position_current":f["home_table_position_current"],"away_table_position_current":f["away_table_position_current"],
                     "table_position_asof_status":f["table_position_asof_status"],
                     "model_input_coverage_pct":f["model_input_coverage_pct"],
                     "model_input_missingness_pct":f["model_input_missingness_pct"],
                     "confidence_score_pct":f["confidence_score_pct"],"data_risk_pct":f["data_risk_pct"],
                     "risk_profile":f["risk_profile"],
                     "odds_named_field_count":f["odds_named_field_count"],"xg_named_field_count":f["xg_named_field_count"],
                     "odds_xg_provenance_status":"UNVERIFIED_NOT_USED_IN_MODEL","calibration_status":"RAW_ONLY_UNCALIBRATED",
                     "production_eligible":"NO"}
                for market in MARKETS: row[market+"_probability_pct"]=round(100*predict(models[market],f),2) if predict(models[market],f) is not None else None
                row["prediction_status"]="RAW_RESEARCH_ONLY" if any(row[m+"_probability_pct"] is not None for m in MARKETS) else "NO_PREDICTION_FEATURE_OR_TRAINING_GATE"
                predictions.append(row)
        # Write private normalized research package.
        normalized_path=OUT/"normalized_selected50_matches.csv"
        with normalized_path.open("w",newline="",encoding="utf-8") as f:
            cols=["fixture_id","season_id","competition_id","country","league","home_id","away_id","home_team","away_team","kickoff_unix","status","finished","home_goals","away_goals"]
            w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
            for r in matches:w.writerow({k:r.get(k) for k in cols})
        feature_path=OUT/"selected50_feature_rows.csv"
        if feature_rows:
            with feature_path.open("w",newline="",encoding="utf-8") as f:
                cols=list(feature_rows[0].keys());w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(feature_rows)
        pred_path=OUT/"oracle_selected50_prediction_report.csv"
        if predictions:
            with pred_path.open("w",newline="",encoding="utf-8") as f:
                cols=list(predictions[0].keys());w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(predictions)
        else: pred_path.write_text("prediction_status\nNO_ELIGIBLE_FUTURE_FIXTURES_OR_FEATURE_GATES_FAILED\n",encoding="utf-8")
        schedule_path=OUT/"oracle_selected50_schedule_coverage.csv"
        with schedule_path.open("w",newline="",encoding="utf-8") as sf:
            scols=["selected_id","country","competition_name","archive_match_rows","completed_match_rows","upcoming_fixture_count_7d","first_upcoming_kickoff_utc","last_upcoming_kickoff_utc","schedule_coverage_status","production_eligible"]
            sw=csv.DictWriter(sf,fieldnames=scols);sw.writeheader();sw.writerows(schedule_coverage)
        # Additional rolling-origin walk-forward diagnostics. Each fold trains only on
        # completed, fully-featured matches strictly before the fold's test start.
        # These are validation folds, not calibration or model-selection inputs.
        wf_edges = [
            ("WF1_2025-03-20_to_2025-09-20", PRIMARY_START, dt.datetime(2025, 9, 20, tzinfo=dt.timezone.utc).timestamp()),
            ("WF2_2025-09-20_to_2026-03-20", dt.datetime(2025, 9, 20, tzinfo=dt.timezone.utc).timestamp(), dt.datetime(2026, 3, 20, tzinfo=dt.timezone.utc).timestamp()),
            ("WF3_2026-03-20_to_2026-09-20", dt.datetime(2026, 3, 20, tzinfo=dt.timezone.utc).timestamp(), PRIMARY_END),
        ]
        walk_forward = []
        league_market_readiness = []
        for market in MARKETS:
            for fold_name, fold_start, fold_end in wf_edges:
                fold_train = [r for r in train_rows if r["kickoff_unix"] < fold_start
                              and r.get("target_"+market) is not None
                              and all(r.get(k) is not None for k in FEATURES)]
                fold_test = [r for r in train_rows if fold_start <= r["kickoff_unix"] < fold_end
                             and r.get("target_"+market) is not None
                             and all(r.get(k) is not None for k in FEATURES)]
                model, fold_train_n = make_model(fold_train, market)
                if model is None or not fold_test:
                    walk_forward.append({"market":market,"fold":fold_name,"status":"INSUFFICIENT_TRAIN_OR_TEST",
                                         "train_n":fold_train_n,"test_n":len(fold_test),
                                         "accuracy_at_0_5":None,"accuracy_95ci_low":None,"accuracy_95ci_high":None,"brier":None,"log_loss":None,"auc":None,
                                         "baseline_brier":None,"brier_skill_vs_prevalence":None})
                    continue
                fp = [predict(model, r) for r in fold_test]
                fy = [r["target_"+market] for r in fold_test]
                valid = [(p,y0) for p,y0 in zip(fp,fy) if p is not None]
                fp = [p for p,y0 in valid]; fy = [y0 for p,y0 in valid]
                train_prev = sum(r["target_"+market] for r in fold_train)/len(fold_train) if fold_train else None
                base_brier = brier_score_loss(fy, [train_prev]*len(fy)) if train_prev is not None and fy else None
                fold_labels = [int(p >= 0.5) for p in fp]
                fold_correct = sum(int(p) == int(y0) for p,y0 in zip(fold_labels,fy))
                acc_ci_low, acc_ci_high = wilson_interval(fold_correct, len(fy))
                walk_forward.append({"market":market,"fold":fold_name,"status":"RAW_WALK_FORWARD_NOT_CALIBRATED",
                    "train_n":fold_train_n,"test_n":len(fy),
                    "accuracy_at_0_5":round(accuracy_score(fy,fold_labels),5),
                    "accuracy_95ci_low":round(acc_ci_low,5) if acc_ci_low is not None else None,
                    "accuracy_95ci_high":round(acc_ci_high,5) if acc_ci_high is not None else None,
                    "brier":round(brier_score_loss(fy,fp),5),
                    "log_loss":round(log_loss(fy,[min(max(p,1e-6),1-1e-6) for p in fp],labels=[0,1]),5),
                    "auc":round(roc_auc_score(fy,fp),5) if len(set(fy))==2 else None,
                    "training_prevalence":round(train_prev,5) if train_prev is not None else None,
                    "baseline_brier":round(base_brier,5) if base_brier is not None else None,
                    "brier_skill_vs_prevalence":round(1-brier_score_loss(fy,fp)/base_brier,5) if base_brier else None})
            # Per-league market evidence with minimum sample gate; no unsupported league-level edge claims.
            for league_name in sorted(set(str(r.get("league") or "UNKNOWN") for r in train_rows)):
                lg_train = [r for r in train_rows if str(r.get("league") or "UNKNOWN")==league_name
                            and r["kickoff_unix"] < PRIMARY_START and r.get("target_"+market) is not None
                            and all(r.get(k) is not None for k in FEATURES)]
                lg_test = [r for r in train_rows if str(r.get("league") or "UNKNOWN")==league_name
                           and PRIMARY_START <= r["kickoff_unix"] < PRIMARY_END
                           and r.get("target_"+market) is not None and all(r.get(k) is not None for k in FEATURES)]
                if len(lg_train) < 100 or len(lg_test) < 100:
                    gate = "INSUFFICIENT_SAMPLE_MIN_100_TRAIN_AND_TEST"
                else:
                    gate = "SAMPLE_GATE_MET_REQUIRES_STABILITY_AND_ODDS_VALIDATION"
                league_market_readiness.append({"league":league_name,"market":market,
                    "train_n":len(lg_train),"test_n":len(lg_test),"sample_gate":gate,
                    "production_eligible":"NO","edge_claim":"NOT_APPROVED"})
        wf_path=OUT/"oracle_selected50_walk_forward_metrics.json"
        wf_path.write_text(json.dumps({"folds":walk_forward,
            "fold_design":"Expanding-window rolling-origin; each fold trains strictly before test interval; fixed features and model; no calibration or tuning.",
            "limitations":["This evaluates model probability quality, not betting ROI.",
                           "Historical settlement joins and provider point-in-time provenance remain unverified.",
                           "Per-league minimum samples are necessary but not sufficient for edge approval.",
                           "No production eligibility is granted."]},indent=2)+"\n",encoding="utf-8")
        # Fail the workflow if the diagnostic artifact is malformed or incomplete.
        wf_check = json.loads(wf_path.read_text(encoding="utf-8"))
        expected_fold_rows = len(MARKETS) * len(wf_edges)
        if len(wf_check.get("folds", [])) != expected_fold_rows:
            raise RuntimeError(f"Walk-forward fold count mismatch: expected {expected_fold_rows}, got {len(wf_check.get('folds', []))}")
        if len(league_market_readiness) != len(set(str(r.get("league") or "UNKNOWN") for r in train_rows)) * len(MARKETS):
            raise RuntimeError("League-market readiness row count mismatch")
        if any(r.get("production_eligible") != "NO" or r.get("edge_claim") != "NOT_APPROVED" for r in league_market_readiness):
            raise RuntimeError("Research readiness artifact attempted to grant production eligibility")
        readiness_path=OUT/"oracle_selected50_league_market_readiness.csv"
        with readiness_path.open("w",newline="",encoding="utf-8") as rf:
            cols=["league","market","train_n","test_n","sample_gate","production_eligible","edge_claim"]
            rw=csv.DictWriter(rf,fieldnames=cols);rw.writeheader();rw.writerows(league_market_readiness)
        backtest_path=OUT/"oracle_selected50_backtest_metrics.json"
        backtest_report={"primary_window":"2025-03-20 through 2026-09-20","training_cutoff_exclusive":"2025-03-20","markets":backtest, "walk_forward_metrics_file":"oracle_selected50_walk_forward_metrics.json","league_market_readiness_file":"oracle_selected50_league_market_readiness.csv",
                         "note":"Single temporal holdout baseline using the locked Oracle logistic-regression form feature set; raw probabilities, no calibration, not production-approved."}
        backtest_path.write_text(json.dumps(backtest_report,indent=2)+"\n",encoding="utf-8")
        qa={"status":"RESEARCH_RUNTIME_BUILT","selected_leagues":50,"provider_competitions_with_matches":len(present_comps),
            "report_horizon_days":7,"minimum_lead_time_minutes":15,
            "future_fixture_competitions_with_predictions":len(set(r["league"] for r in predictions)),
            "future_fixture_candidates_in_report_horizon":len(future),
            "season_rows_seen":len(season_rows),"selected_season_ids":len(selected_by_id),"historical_seasons_mapped_by_exact_labels":mapped_historical_seasons,"historical_seasons_loaded":sum(1 for r in season_qa if r["status"]=="INGESTED"),
            "raw_match_records_retained_after_dedup":len(matches),"completed_match_records":sum(r["finished"] for r in matches),
            "future_fixture_candidates":len(future),"feature_rows_with_full_20_features":sum(all(r.get(f) is not None for f in FEATURES) for r in feature_rows),
            "prediction_fixture_count":len(predictions),"prediction_rows":len(predictions)*len(MARKETS),
            "production_model_logic_changed":False,"production_probabilities_changed":False,"production_readiness":"NOT_GRANTED",
            "limitations":["This is an isolated research/challenger runtime, not the production engine.",
             "Recent form is computed from the last five completed home matches for the home team and away matches for the away team, strictly before kickoff.",
             "Historical validation includes a locked primary temporal holdout and additional expanding-window walk-forward folds; no hyperparameter selection or calibration is applied.",
             "H2H is descriptive only and not a model feature. Current team table positions are display-only snapshots, not historical standings.",
             "xG and odds are not used as model features because their semantic and point-in-time provenance is not verified.",
             "Only explicitly finished matches with numeric scores are used as training truth; unknown status values fail closed."]}
        (OUT/"oracle_selected50_feature_qa.json").write_text(json.dumps(qa,indent=2)+"\n",encoding="utf-8")
        (OUT/"season_coverage.csv").write_text("season_id,competition,status,match_count\n"+"".join(f'{r["season_id"]},{r["selected_competition"]},{r["status"]},{r["match_count"]}\n' for r in season_qa),encoding="utf-8")
        # Package the derived/private candidate. Never upload the normalized dataset as a public artifact.
        private_zip=Path("oracle-selected50-normalized-research-candidate.zip")
        with zipfile.ZipFile(private_zip,"w",zipfile.ZIP_DEFLATED) as z:
            for p in (normalized_path,feature_path,pred_path,backtest_path,wf_path,readiness_path,schedule_path,OUT/"oracle_selected50_feature_qa.json",OUT/"season_coverage.csv"):
                if p.exists(): z.write(p,p.name)
        digest=hashlib.sha256(private_zip.read_bytes()).hexdigest()
        Path("private-runtime-candidate.sha256").write_text(digest+"  oracle-selected50-normalized-research-candidate.zip\n",encoding="utf-8")
        # Only derived report, backtest and QA summaries go into public Actions artifacts.
        print(json.dumps({**qa,"backtest":backtest,"archive_sha256":hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),"private_candidate_sha256":digest},sort_keys=True))
if __name__=="__main__": main()
