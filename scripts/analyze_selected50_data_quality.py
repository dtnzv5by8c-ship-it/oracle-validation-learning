#!/usr/bin/env python3
"""Research-only Selected-50 data-quality and market-screen analytics.
Reads existing runtime artifacts only; never reads the locked H2H paired-prediction
holdout, changes predictions, or makes provider/API calls.
"""
import argparse,csv,json,math
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
VALID={'BTTS','DC_HOME','DC_AWAY'}
CANDIDATE='POSITIVE_BRIER_SKILL_ALL_FOLDS_DIAGNOSTIC_ONLY'
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def writecsv(p,rows):
 rows=list(rows)
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else []);w.writeheader();w.writerows(rows)
def n(x):
 try:return int(float(x)) if x not in ('',None) else 0
 except:return 0
def f(x):
 try:
  z=float(x);return z if math.isfinite(z) else None
 except:return None
def dt(x):
 try:return datetime.fromisoformat(x.replace('Z','+00:00')).astimezone(timezone.utc) if x else None
 except:return None
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input-dir',required=True,type=Path);ap.add_argument('--output-dir',required=True,type=Path);a=ap.parse_args();d=a.input_dir;o=a.output_dir;o.mkdir(parents=True,exist_ok=True)
 j=lambda x:json.loads((d/x).read_text(encoding='utf-8'))
 feat=j('oracle_selected50_feature_qa.json');val=j('oracle_selected50_runtime_validation.json');prov=j('oracle_selected50_runtime_provenance.json')
 seasons=readcsv(d/'season_coverage.csv');py=readcsv(d/'oracle_selected50_provider_season_year_coverage.csv');cal=readcsv(d/'oracle_selected50_calendar_year_coverage.csv');settle=readcsv(d/'oracle_selected50_settlement_truth_qa.csv');ready=readcsv(d/'oracle_selected50_league_market_readiness.csv');wf=readcsv(d/'oracle_selected50_league_walk_forward_metrics.csv');fix=readcsv(d/'oracle_selected50_prediction_report.csv')
 sg,pg,cg,qg=(defaultdict(list) for _ in range(4))
 for rows,g in [(seasons,sg),(py,pg),(cal,cg),(settle,qg)]:
  for r in rows:g[r.get('selected_id','')].append(r)
 ids=sorted(set(sg)|set(pg)|set(cg)|set(qg));quality=[]
 for sid in ids:
  sr,pr,cr,qr=sg[sid],pg[sid],cg[sid],qg[sid];sample=(pr or sr or cr or qr)[0]
  archive=sum(n(x.get('normalized_match_rows_retained')) for x in sr);full=sum(n(x.get('full_20_feature_rows')) for x in pr);primary=sum(n(x.get('primary_window_match_rows')) for x in pr);primary_full=sum(n(x.get('primary_window_full_20_feature_rows')) for x in cr);completed=sum(n(x.get('explicitly_completed_match_rows')) for x in pr)
  quality.append({'selected_id':sid,'country':sample.get('country',''),'league':sample.get('competition_name',sample.get('competition','')),'season_rows':len(sr),'archive_rows':archive,'completed_rows':completed,'full_20_feature_rows':full,'full_20_feature_pct':round(100*full/archive,2) if archive else '', 'primary_window_rows':primary,'primary_window_full20_rows':primary_full,'primary_window_full20_pct':round(100*primary_full/primary,2) if primary else '', 'missing_kickoff_rows':sum(n(x.get('rejected_missing_kickoff_rows')) for x in sr),'missing_team_id_rows':sum(n(x.get('rejected_missing_home_team_id_rows'))+n(x.get('rejected_missing_away_team_id_rows')) for x in sr),'missing_fixture_id_rows':sum(n(x.get('rows_missing_normalized_fixture_id')) for x in sr),'finished_missing_score_rows':sum(n(x.get('rows_explicit_finished_status_missing_numeric_score')) for x in sr),'parent_competition_id_status':sample.get('provider_competition_id_status','NOT_RECORDED'),'settlement_truth_status':qr[0].get('settlement_truth_status','NOT_RECORDED') if qr else 'NOT_RECORDED','release_status':'RESEARCH_DIAGNOSTIC_ONLY'})
 writecsv(o/'oracle_selected50_league_data_quality.csv',quality)
 years=sorted({r.get('calendar_year_utc','') for r in cal if r.get('calendar_year_utc')});lookup={(r.get('selected_id',''),r.get('calendar_year_utc','')):r for r in cal};matrix=[]
 for sid in ids:
  sr=(sg.get(sid) or pg.get(sid) or [{}])[0]
  for y in years:
   r=lookup.get((sid,y),{});matrix.append({'selected_id':sid,'country':sr.get('country',''),'league':sr.get('competition',sr.get('competition_name','')),'calendar_year_utc':y,'archive_rows':n(r.get('archive_fixture_rows')),'completed_score_rows':n(r.get('completed_with_numeric_score_rows')),'full20_feature_rows':n(r.get('full_20_feature_rows')),'primary_window_rows':n(r.get('primary_window_fixture_rows')),'primary_window_full20_rows':n(r.get('primary_window_full_20_feature_rows')),'interpretation':r.get('coverage_interpretation','NO_ROWS_OBSERVED_NOT_SOURCE_ABSENCE_PROOF')})
 writecsv(o/'oracle_selected50_season_year_coverage_matrix.csv',matrix)
 rdy={(r.get('selected_id',''),r.get('market','')):r for r in ready if r.get('market') in VALID};wfg=defaultdict(list)
 for r in wf:
  if r.get('market') in VALID:wfg[(r.get('selected_id',''),r.get('market',''))].append(r)
 market=[]
 for key,rr in wfg.items():
  rr=sorted(rr,key=lambda x:x.get('fold',''));rd=rdy.get(key,{});skills=[f(x.get('brier_skill_vs_league_prevalence')) for x in rr];skills=[x for x in skills if x is not None];eces=[f(x.get('ece_10_bins')) for x in rr];eces=[x for x in eces if x is not None];positive=sum(x is not None and x>0 for x in [f(z.get('brier_skill_vs_league_prevalence')) for z in rr]);gate=sum(z.get('sample_gate')=='SAMPLE_GATE_MET_DIAGNOSTIC_ONLY' for z in rr);status=rd.get('fold_stability_status','NOT_RECORDED');disp='CANDIDATE_FOR_NEW_UNTOUCHED_VALIDATION_ONLY' if status==CANDIDATE and len(rr)==3 and gate==3 and positive==3 else 'INSUFFICIENT_EVIDENCE' if 'INSUFFICIENT' in status or len(rr)<3 or gate<3 else 'MIXED_OR_NONPOSITIVE_DIAGNOSTIC';z=rr[0]
  market.append({'selected_id':key[0],'country':z.get('country',''),'league':z.get('league',''),'market':key[1],'fold_count':len(rr),'folds_sample_gate_passed':gate,'folds_positive_brier_skill':positive,'min_fold_brier_skill':min(skills) if skills else '','median_fold_brier_skill':sorted(skills)[len(skills)//2] if skills else '','max_fold_brier_skill':max(skills) if skills else '','max_fold_ece10':max(eces) if eces else '','readiness_status':status,'research_disposition':disp,'warning':'50 leagues × 3 markets screened; independent validation required','betting_eligibility':'NOT_ASSESSED'})
 writecsv(o/'oracle_selected50_market_screen_robustness.csv',sorted(market,key=lambda x:(x['market'],x['research_disposition'],x['country'],x['league'])))
 status=Counter(r.get('prediction_status','') for r in fix);miss=Counter();byleague=defaultdict(list)
 for r in fix:
  for name in (r.get('missing_required_features') or '').split(';'):
   if name:miss[name]+=1
  byleague[(r.get('country',''),r.get('league',''))].append(r)
 missrows=[{'feature':k,'fixtures_missing_feature':v,'fixture_rows':len(fix),'missing_pct':round(100*v/len(fix),2),'note':'Underlying and derived feature counts overlap.'} for k,v in sorted(miss.items(),key=lambda x:(-x[1],x[0]))];writecsv(o/'oracle_selected50_fixture_feature_missingness.csv',missrows)
 blocked=[]
 for (country,league),rr in sorted(byleague.items()):
  bb=[r for r in rr if r.get('prediction_status')!='RAW_RESEARCH_ONLY']
  if not bb:continue
  hm=sum(n(r.get('home_recent5_n'))<5 for r in bb);am=sum(n(r.get('away_recent5_n'))<5 for r in bb);both=sum(n(r.get('home_recent5_n'))<5 and n(r.get('away_recent5_n'))<5 for r in bb)
  blocked.append({'country':country,'league':league,'fixture_rows':len(rr),'blocked_rows':len(bb),'blocked_home_form_short':hm,'blocked_away_form_short':am,'blocked_both_sides_short':both,'fixture_ids':';'.join(r.get('fixture_id','') for r in bb),'decision':'KEEP_BLOCKED_DO_NOT_IMPUTE'})
 writecsv(o/'oracle_selected50_blocked_fixture_diagnostics.csv',blocked)
 now=datetime.now(timezone.utc);gen=dt(prov.get('generated_utc'));snap=dt(prov.get('snapshot_retrieved_utc'));fresh={'runtime_generated_utc':gen.isoformat() if gen else None,'runtime_age_hours':round((now-gen).total_seconds()/3600,2) if gen else None,'snapshot_retrieved_utc':snap.isoformat() if snap else None,'snapshot_age_hours':round((now-snap).total_seconds()/3600,2) if snap else None,'snapshot_rows':n(prov.get('snapshot_fixture_rows')),'exact_fixture_ids_refreshed':n(prov.get('overlay_refreshed_present_exact_fixture_ids')),'candidate_rows_added':n(prov.get('overlay_candidate_rows_added')),'quarantined_or_invalid_rows':n(prov.get('overlay_quarantined_or_invalid_rows'))}
 msummary={}
 for m in sorted(VALID):
  rr=[x for x in market if x['market']==m];msummary[m]={'candidate_for_new_validation':sum(x['research_disposition']=='CANDIDATE_FOR_NEW_UNTOUCHED_VALIDATION_ONLY' for x in rr),'insufficient':sum(x['research_disposition']=='INSUFFICIENT_EVIDENCE' for x in rr),'mixed_or_nonpositive':sum(x['research_disposition']=='MIXED_OR_NONPOSITIVE_DIAGNOSTIC' for x in rr)}
 bh=sum(1 for r in fix if r.get('prediction_status')!='RAW_RESEARCH_ONLY' and n(r.get('home_recent5_n'))<5);ba=sum(1 for r in fix if r.get('prediction_status')!='RAW_RESEARCH_ONLY' and n(r.get('away_recent5_n'))<5);bb=sum(1 for r in fix if r.get('prediction_status')!='RAW_RESEARCH_ONLY' and n(r.get('home_recent5_n'))<5 and n(r.get('away_recent5_n'))<5)
 summary={'status':'RESEARCH_ONLY_DATA_QUALITY_ANALYTICS_COMPLETE_TEAM_PERFORMANCE_DNA_STILL_BLOCKED','source_run_id':prov.get('runtime_run_id'),'source_run_number':prov.get('runtime_run_number'),'source_archive_sha256':prov.get('source_archive_sha256'),'league_groups':len(ids),'season_coverage_rows':len(seasons),'calendar_year_rows':len(cal),'archive_rows':sum(x['archive_rows'] for x in quality),'completed_rows':sum(x['completed_rows'] for x in quality),'full20_feature_rows':sum(x['full_20_feature_rows'] for x in quality),'primary_window_rows':sum(x['primary_window_rows'] for x in quality),'primary_window_full20_rows':sum(x['primary_window_full20_rows'] for x in quality),'provider_parent_competition_ids_verified':n(feat.get('provider_parent_competition_ids_verified')),'provider_to_canonical_bridges_verified':n(feat.get('provider_to_canonical_bridges_verified')),'unique_provider_fixture_ids_coverage_audit':n(feat.get('provider_match_coverage_unique_fixture_ids_total')),'duplicate_fixture_id_rows_coverage_audit':n(feat.get('provider_match_coverage_duplicate_fixture_id_rows_total')),'fixture_rows':len(fix),'prediction_status_counts':dict(status),'canonical_fixture_join_counts':dict(Counter(r.get('canonical_fixture_join_status','NOT_VERIFIED') for r in fix)),'canonical_team_join_counts':dict(Counter(r.get('canonical_team_join_status','NOT_VERIFIED') for r in fix)),'home_recent5_n_distribution':dict(sorted(Counter(n(r.get('home_recent5_n')) for r in fix).items())),'away_recent5_n_distribution':dict(sorted(Counter(n(r.get('away_recent5_n')) for r in fix).items())),'blocked_home_form_short':bh,'blocked_away_form_short':ba,'blocked_both_sides_short':bb,'missing_feature_counts':dict(miss),'market_screen':msummary,'freshness':fresh,'locked_h2h_holdout_used_for_team_ranking':False,'team_performance_dna_status':'BLOCKED_NO_TEAM_ATTRIBUTED_WALK_FORWARD_PREDICTIONS_AND_VERIFIED_SETTLEMENT_TRUTH','combo_in_market_screen':False,'production_eligible':val.get('production_eligible',False),'betting_eligible':val.get('betting_eligible',False),'limitations':['Archive coverage is not proof of source completeness.','Provider competition IDs in this archive are season IDs; canonical parent competition and fixture/team bridges remain unverified.','Internal status/score QA is not official settlement truth.','League-market screening across 50 leagues and three markets has selection bias; candidates require a new untouched validation period.','Team performance ranking remains blocked; the locked H2H holdout was not used.','No production model logic, probabilities, calibration or governance was changed.']}
 (o/'oracle_selected50_data_quality_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 lines=['# Project Oracle — Selected-50 Data Quality & Market Screen','',f"**Source runtime:** #{prov.get('runtime_run_number')} (run {prov.get('runtime_run_id')})",'**Scope:** existing artifacts only; research-only; no provider/API calls; no production changes.','','## Coverage checkpoint','',f"- Groups represented: **{len(ids)}**; normalized archive rows: **{summary['archive_rows']:,}**; completed-score rows: **{summary['completed_rows']:,}.",f"- Rows with all 20 features: **{summary['full20_feature_rows']:,}**; primary-window rows: **{summary['primary_window_rows']:,}**; primary-window rows with full 20 features: **{summary['primary_window_full20_rows']:,}**.",f"- Current fixtures: **{len(fix)}**; predictions available: **{status.get('RAW_RESEARCH_ONLY',0)}**; blocked: **{status.get('BLOCKED_MISSING_REQUIRED_FEATURES',0)}**.",f"- Parent competition IDs verified: **{summary['provider_parent_competition_ids_verified']}**; provider-to-canonical bridges verified: **{summary['provider_to_canonical_bridges_verified']}**.",'','## Missing-form diagnostic','','Blocked fixtures with home split-form shorter than five matches: **%d**; away: **%d**; both: **%d**.'%(bh,ba,bb),'Missing-feature counts include underlying and derived features, so they overlap and are not unique fixture counts.','', '| Feature | Missing fixtures | % of report |','|---|---:|---:|']
 for x in missrows[:12]:lines.append(f"| {x['feature']} | {x['fixtures_missing_feature']} | {x['missing_pct']:.2f}% |")
 lines+=['','Per-league blocked fixture IDs and reasons are in oracle_selected50_blocked_fixture_diagnostics.csv. Keep these fixtures blocked; do not silently impute required pre-kickoff form.','','## League-market triage','','| Market | Candidate for new untouched validation | Insufficient | Mixed/non-positive |','|---|---:|---:|---:|']
 for m,x in sorted(msummary.items()):lines.append(f"| {m} | {x['candidate_for_new_validation']} | {x['insufficient']} | {x['mixed_or_nonpositive']} |")
 lines+=['','Candidates require an untouched validation period. The screen spans 50 leagues × 3 markets, so selection bias is material; these are not betting recommendations.','','## Freshness and overlay',f"- Runtime report age at analysis: **{fresh['runtime_age_hours']} hours**.",f"- Snapshot age at analysis: **{fresh['snapshot_age_hours']} hours**.",f"- Snapshot rows: **{fresh['snapshot_rows']:,}**; exact fixture IDs refreshed: **{fresh['exact_fixture_ids_refreshed']}**; candidate rows added: **{fresh['candidate_rows_added']}**; quarantined/invalid rows: **{fresh['quarantined_or_invalid_rows']}**.",'','The snapshot is a bounded refresh, not proof of source completeness. Quarantined rows remain excluded until identity/quality issues are resolved.','','## Team DNA and next action','','Team performance DNA remains blocked: no team-attributed chronological out-of-sample prediction artifact is available and official settlement truth/canonical bridges are unverified. Upcoming form sequences are context only. The locked H2H holdout was not used for team ranking.','','Next: produce a research-only team-attributed walk-forward export with fixture ID, as-of cutoff, team IDs, market, probability, fold, feature provenance and verified outcome; validate canonical joins and settlement truth before team hit-rate/calibration analysis. Combo stays blocked. Production and betting eligibility remain NOT GRANTED.','']
 (o/'PROJECT_ORACLE_SELECTED50_DATA_QUALITY_MARKET_SCREEN.md').write_text('\n'.join(lines),encoding='utf-8')
 print(json.dumps(summary,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
