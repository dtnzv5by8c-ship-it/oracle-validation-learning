#!/usr/bin/env python3
"""Offline, aggregate-only audit of canonical Oracle prediction archive evidence."""
import argparse, csv, hashlib, json
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from statistics import median

EXPECTED = {"BTTS_YES", "HOME_1X", "AWAY_X2", "HOME_1X_U45", "AWAY_X2_U45"}
LEDGERS = {
    "run_registry": "RUN_REGISTRY.csv", "team_profile": "TEAM_PROFILE_LEDGER.csv", "fixture_dynamics": "FIXTURE_DYNAMICS_LEDGER.csv",
    "model_scorecard": "MODEL_SCORECARD.csv", "postmortem": "POSTMORTEM_LEDGER.csv",
    "team_behaviour": "TEAM_BEHAVIOUR_LEDGER.csv", "learning": "LEARNING_LEDGER.csv",
    "run_artifacts": "RUN_ARTIFACTS.csv", "miss_dna": "MISS_DNA_SUMMARY.csv",
}
REQUIRED = {"prediction_id", "run_id", "fixture_id", "competition", "fixture_date", "kickoff_time",
            "home_team", "away_team", "model", "model_version", "model_status", "prediction_timestamp",
            "data_cutoff_date", "event_truth_cutoff_date", "feature_snapshot_id", "source_manifest_hash",
            "raw_probability", "display_probability", "decision", "selection", "data_quality_status",
            "pre_match_state_hash", "model_code_sha", "calibration_id"}


def read_csv(path):
    if not path.exists(): return [], []
    with path.open(encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f); return list(r.fieldnames or []), list(r)


def dt(value):
    try: x = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except (TypeError, ValueError): return None
    return x.astimezone(timezone.utc) if x.tzinfo else None


def d(value):
    try: return date.fromisoformat(str(value).strip())
    except (TypeError, ValueError): return None


def pct_summary(values):
    return {"min": round(min(values), 2), "median": round(median(values), 2), "max": round(max(values), 2)} if values else {"min": None, "median": None, "max": None}


def audit(pred, fields, settlements=None, snapshots=None, other_ledgers=None, matches_n=0, state_n=0,
          source_manifest=None, current_state_hash=None):
    settlements, snapshots = settlements or [], snapshots or []
    other_ledgers = other_ledgers or {}
    missing_cells = {k: sum(not str(r.get(k, "") or "").strip() for r in pred) for k in sorted(REQUIRED)}
    optional = ["calibrated_probability", "market_line", "market_odds", "market_implied_probability", "model_edge"]
    optional_missing = {k: sum(not str(r.get(k, "") or "").strip() for r in pred) for k in optional}
    fixture_markets, comp_fixtures = defaultdict(set), defaultdict(set)
    comp_rows, market_rows, decisions, quality, model_status = Counter(), Counter(), Counter(), Counter(), Counter()
    team_fixtures, team_market = defaultdict(set), Counter()
    leads, cutoff_pred, cutoff_kick = [], [], []
    pre = post = unknown = valid_prob = 0
    for r in pred:
        fid, comp, market = r.get("fixture_id", ""), r.get("competition", ""), r.get("model", "")
        fixture_markets[fid].add(market); comp_fixtures[comp].add(fid); comp_rows[comp] += 1; market_rows[market] += 1
        decisions[r.get("decision", "")] += 1; quality[r.get("data_quality_status", "")] += 1
        model_status[r.get("model_status", "")] += 1
        try: valid_prob += int(0 <= float(r.get("raw_probability", "nan")) <= 1)
        except ValueError: pass
        pt, ko = dt(r.get("prediction_timestamp", "")), dt(f"{r.get('fixture_date', '')}T{r.get('kickoff_time', '')}")
        if pt is None or ko is None: unknown += 1
        elif pt < ko: pre += 1; leads.append((ko - pt).total_seconds() / 3600)
        else: post += 1
        cutoff = d(r.get("data_cutoff_date", ""))
        if cutoff and pt: cutoff_pred.append((pt.date() - cutoff).days)
        if cutoff and ko: cutoff_kick.append((ko.date() - cutoff).days)
        home, away = r.get("home_team", "").strip(), r.get("away_team", "").strip()
        if fid and home: team_fixtures[home].add(fid)
        if fid and away: team_fixtures[away].add(fid)
        if market == "BTTS_YES":
            if home: team_market[(home, market)] += 1
            if away: team_market[(away, market)] += 1
        elif market in {"HOME_1X", "HOME_1X_U45"} and home: team_market[(home, market)] += 1
        elif market in {"AWAY_X2", "AWAY_X2_U45"} and away: team_market[(away, market)] += 1
    pred_ids = {r.get("prediction_id", "") for r in pred}
    settled = [r for r in settlements if str(r.get("settlement_status", "")).upper() == "SETTLED"]
    matched_settlements = sum(r.get("prediction_id", "") in pred_ids for r in settlements)
    verified_truth = sum(str(r.get("official_truth_verified", r.get("settlement_truth_verified", ""))).lower() in {"true", "1", "yes"} for r in settlements)
    snapshot_ids = {r.get("feature_snapshot_id", "") for r in pred if r.get("feature_snapshot_id")}
    manifest_ids = {r.get("feature_snapshot_id", "") for r in snapshots if r.get("feature_snapshot_id")}
    matched_snapshots = len(snapshot_ids & manifest_ids)
    team_ids_ok = bool(pred) and {"home_team_id", "away_team_id"} <= set(fields) and all(r.get("home_team_id") and r.get("away_team_id") for r in pred)
    fixture_ids_ok = bool(pred) and "canonical_fixture_id" in fields and all(r.get("canonical_fixture_id") for r in pred)
    src_hashes = {r.get("source_manifest_hash", "") for r in pred if r.get("source_manifest_hash")}
    state_hashes = {r.get("pre_match_state_hash", "") for r in pred if r.get("pre_match_state_hash")}
    pred_times = [dt(r.get("prediction_timestamp", "")) for r in pred]; pred_times = [x for x in pred_times if x]
    source_generated = (source_manifest or {}).get("generated_utc")
    source_generated_dt = dt(source_generated or "")
    source_after = bool(source_generated_dt and pred_times and source_generated_dt > min(pred_times))
    source_hash_match = bool(source_manifest and src_hashes and source_manifest.get("sha256") and src_hashes == {source_manifest["sha256"]})
    snapshot_retrievable = bool(snapshot_ids and snapshots and other_ledgers.get("run_artifacts", 0) > 0 and matched_snapshots == len(snapshot_ids))
    performance_measurable = bool(team_ids_ok and fixture_ids_ok and pre == len(pred) and verified_truth > 0 and matched_settlements > 0)
    team_counts = [len(v) for v in team_fixtures.values()]
    team_market_counts = list(team_market.values())
    fixtures = {k: v for k, v in fixture_markets.items() if k}
    return {
        "status": "CANONICAL_ARCHIVE_EXPOSURE_AUDIT_COMPLETE",
        "prediction_archive": {
            "prediction_rows": len(pred), "unique_prediction_ids": len(pred_ids),
            "duplicate_prediction_ids": len(pred) - len(pred_ids),
            "duplicate_fixture_model_version_observations": len(pred) - len({(r.get('fixture_id'), r.get('model'), r.get('model_version')) for r in pred}),
            "unique_runs": len({r.get("run_id") for r in pred if r.get("run_id")}),
            "fixtures": len(fixtures), "fixtures_with_all_five_expected_markets": sum(v == EXPECTED for v in fixtures.values()),
            "competition_count": len(comp_fixtures), "unique_team_labels": len(team_fixtures),
            "team_fixture_sample_distribution": dict(sorted(Counter(team_counts).items())),
            "teams_with_two_or_more_fixtures": sum(x >= 2 for x in team_counts),
            "maximum_team_fixture_exposures": max(team_counts, default=0),
            "team_market_exposure_distribution": dict(sorted(Counter(team_market_counts).items())),
            "markets": dict(sorted(market_rows.items())), "decisions": dict(sorted(decisions.items())),
            "data_quality_statuses": dict(sorted(quality.items())), "model_statuses": dict(sorted(model_status.items())),
            "valid_raw_probability_rows": valid_prob, "strictly_pre_kickoff_rows": pre,
            "post_or_equal_kickoff_rows": post, "timestamp_unverifiable_rows": unknown,
            "lead_hours": pct_summary(leads), "cutoff_age_days_at_prediction": pct_summary(cutoff_pred),
            "cutoff_age_days_at_kickoff": pct_summary(cutoff_kick),
            "data_cutoff_dates": sorted({r.get("data_cutoff_date", "") for r in pred if r.get("data_cutoff_date")}),
            "event_truth_cutoff_dates": sorted({r.get("event_truth_cutoff_date", "") for r in pred if r.get("event_truth_cutoff_date")}),
            "unique_source_manifest_hashes": len(src_hashes), "unique_pre_match_state_hashes": len(state_hashes),
            "unique_feature_snapshot_ids": len(snapshot_ids), "missing_required_columns": sorted(REQUIRED - set(fields)),
            "missing_required_cells": missing_cells, "missing_optional_cells": optional_missing,
            "competition_coverage": [{"competition": c, "fixtures": len(fs), "prediction_rows": comp_rows[c]} for c, fs in sorted(comp_fixtures.items())],
            "market_coverage": [{"market": m, "prediction_rows": n} for m, n in sorted(market_rows.items())],
        },
        "evidence_ledgers": {
            "settlement_rows": len(settlements), "settled_status_rows": len(settled),
            "settlement_rows_matching_prediction_ids": matched_settlements, "official_truth_verified_rows": verified_truth,
            "feature_snapshot_manifest_rows": len(snapshots), "feature_snapshot_ids_resolved": matched_snapshots,
            "run_registry_rows": other_ledgers.get("run_registry", 0), "other_ledger_rows": other_ledgers,
            "database_matches_rows": matches_n, "database_prematch_team_state_rows": state_n,
            "current_source_manifest_generated_utc": source_generated,
            "current_source_manifest_generated_after_predictions": source_after,
            "current_source_manifest_hash_matches_prediction_ledger": source_hash_match,
            "current_prematch_state_hash_matches_prediction_ledger": bool(current_state_hash and state_hashes == {current_state_hash}) if current_state_hash else None,
        },
        "interpretation": {
            "canonical_team_identity_verified": team_ids_ok, "canonical_fixture_identity_verified": fixture_ids_ok,
            "official_settlement_truth_available": verified_truth > 0,
            "point_in_time_feature_snapshot_retrievable": snapshot_retrievable,
            "team_market_performance_measurable": performance_measurable,
            "market_suitability_measurable": performance_measurable, "calibration_validated": False,
        },
        "limitations": [
            "Provider team labels and fixture IDs are not canonical identity joins.",
            "Prediction exposures are not outcome samples; no team hit rate or market suitability is inferred.",
            "A SETTLED status or populated source name is not independently certified official truth.",
            "Feature snapshot IDs require matching manifest and archived source artifacts to be retrievable.",
            "Current source/state files may differ from the historical files hashed at prediction time.",
            "No calibration is inferred from a calibration_id when calibrated_probability is blank.",
            "No H2H files or holdout data are read by this audit.",
        ],
        "governance": {"research_only": True, "provider_calls": 0, "provider_credits": 0,
                       "h2h_holdout_accessed": False, "production_logic_changed": False,
                       "frozen_probabilities_changed": False, "calibration_changed": False, "governance_changed": False},
    }


def write_csv(path, rows):
    if not rows: path.write_text("\n", encoding="utf-8"); return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def main():
    p = argparse.ArgumentParser(); p.add_argument("--archive-dir", required=True); p.add_argument("--database-dir", required=True)
    p.add_argument("--output-dir", required=True); p.add_argument("--source-manifest", default=""); a = p.parse_args()
    arch, db, out = Path(a.archive_dir), Path(a.database_dir), Path(a.output_dir)
    fields, pred = read_csv(arch / "PREDICTION_LEDGER.csv")
    _, settlements = read_csv(arch / "SETTLEMENT_LEDGER.csv"); _, snapshots = read_csv(arch / "FEATURE_SNAPSHOT_MANIFEST.csv")
    other = {}
    for key, name in LEDGERS.items(): other[key] = len(read_csv(arch / name)[1])
    _, matches = read_csv(db / "matches.csv"); _, states = read_csv(db / "prematch_team_state.csv")
    source = None
    if a.source_manifest and Path(a.source_manifest).exists():
        raw = Path(a.source_manifest).read_bytes()
        try: source = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError): source = {}
        source["sha256"] = hashlib.sha256(raw).hexdigest()
    state_path = db / "prematch_team_state.csv"
    state_hash = hashlib.sha256(state_path.read_bytes()).hexdigest() if state_path.exists() else None
    summary = audit(pred, fields, settlements, snapshots, other, len(matches), len(states), source, state_hash)
    out.mkdir(parents=True, exist_ok=True)
    (out / "oracle_canonical_prediction_archive_team_exposure_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_csv(out / "oracle_canonical_archive_competition_coverage.csv", summary["prediction_archive"]["competition_coverage"])
    write_csv(out / "oracle_canonical_archive_market_coverage.csv", summary["prediction_archive"]["market_coverage"])
    print(json.dumps({"status": summary["status"], "prediction_rows": summary["prediction_archive"]["prediction_rows"],
                      "fixtures": summary["prediction_archive"]["fixtures"], "settlements": summary["evidence_ledgers"]["settlement_rows"],
                      "snapshot_manifest_rows": summary["evidence_ledgers"]["feature_snapshot_manifest_rows"]}, sort_keys=True))


if __name__ == "__main__": main()
