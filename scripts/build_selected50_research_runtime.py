#!/usr/bin/env python3
"""Isolated Selected-50 research runtime. Production scripts and probabilities are untouched."""
import bisect, csv, datetime as dt, hashlib, json, math, os, re, zipfile
from collections import Counter, defaultdict
from pathlib import Path
import sys

# Ensure sibling research helpers import correctly when this file is loaded by tests.
SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import brier_score_loss, log_loss, accuracy_score, roc_auc_score

from record_selected50_archive_consumption import write_archive_consumption_receipt

ARCHIVE = Path(os.environ.get("ORACLE_ARCHIVE", "private-download/oracle-selected50-footystats-private-ingestion.zip"))
MANIFEST = Path("data/oracle-footystats-selected-50-season-id-manifest.csv")
PARENT_ID_PROBE = Path("reports/oracle-selected50-parent-id-probe-2026-10-26.csv")
IDENTITY_GATE_MATRIX = Path("reports/oracle-selected50-identity-and-market-gate-matrix-2026-10-26.csv")
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

def combo_predictor_vs_ledger_disagreements(home, away):
    """Return per-side predictor/settlement disagreement flags for a valid final score.

    The research predictor requires 2-4 total goals. The current settlement helper
    requires Double Chance and total goals <=4. Only the low-goal scorelines where
    the relevant Double Chance condition is true can disagree.
    """
    try:
        h, a = float(home), float(away)
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(h) or not math.isfinite(a) or h < 0 or a < 0:
        return None
    if not h.is_integer() or not a.is_integer():
        return None
    h, a = int(h), int(a)
    total = h + a
    predictor_home = bool(MARKETS["COMBO_HOME"](h, a))
    predictor_away = bool(MARKETS["COMBO_AWAY"](h, a))
    settlement_home = (h >= a) and (total <= 4)
    settlement_away = (a >= h) and (total <= 4)
    return predictor_home != settlement_home, predictor_away != settlement_away

def wilson_interval(successes, n, z=1.959963984540054):
    """Two-sided 95% Wilson interval for a binomial proportion; descriptive only."""
    if n <= 0:
        return None, None
    p = successes / n
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    half = z * math.sqrt((p*(1-p) + z*z/(4*n))/n) / denom
    return max(0.0, center-half), min(1.0, center+half)

def expected_calibration_error(y, probs, bins=10):
    """Ten-bin ECE diagnostic; never used to transform model probabilities."""
    if not y or len(y) != len(probs):
        return None
    ece = 0.0
    for bi in range(bins):
        lo = bi / bins
        hi = (bi + 1) / bins
        idx = [i for i, p in enumerate(probs) if p >= lo and (p < hi or (bi == bins - 1 and p <= hi))]
        if not idx:
            continue
        mean_p = sum(probs[i] for i in idx) / len(idx)
        observed = sum(y[i] for i in idx) / len(idx)
        ece += len(idx) / len(y) * abs(mean_p - observed)
    return round(ece, 5)

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

def valid_completed_score(home, away):
    """True only for finite, non-negative integer football scores."""
    try:
        h, a = float(home), float(away)
    except (TypeError, ValueError, OverflowError):
        return False
    return (math.isfinite(h) and math.isfinite(a) and h >= 0 and a >= 0
            and h.is_integer() and a.is_integer())


def completed_fixture_signature_key(row):
    """Canonical research signature for a completed score row; None if identity is incomplete."""
    if not row.get("finished") or not valid_completed_score(row.get("home_goals"), row.get("away_goals")):
        return None
    home_id = str(row.get("home_id") or "").strip()
    away_id = str(row.get("away_id") or "").strip()
    if not home_id or not away_id or home_id == away_id:
        return None
    try:
        kickoff = float(row["kickoff_unix"])
    except (KeyError, TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(kickoff):
        return None
    return (str(row.get("competition_id") or ""), kickoff, tuple(sorted((home_id, away_id))))


def market_targets_for_match(match, excluded_signatures=None):
    """Return labels only for valid completed fixtures not quarantined as duplicate signatures."""
    markets = MARKETS
    signature = completed_fixture_signature_key(match)
    home_id = str(match.get("home_id") or "").strip()
    away_id = str(match.get("away_id") or "").strip()
    if not (match.get("finished")
            and valid_completed_score(match.get("home_goals"), match.get("away_goals"))
            and home_id and away_id and home_id != away_id
            and not (signature is not None and signature in (excluded_signatures or set()))):
        return {f"target_{market}": None for market in markets}
    home_goals = int(float(match["home_goals"]))
    away_goals = int(float(match["away_goals"]))
    return {f"target_{market}": fn(home_goals, away_goals) for market, fn in markets.items()}


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

def make_model_for_features(rows, market, feature_names, min_train=300):
    """Research-only model helper for a separately specified feature set."""
    valid=[r for r in rows if r.get("target_"+market) is not None
           and all(r.get(f) is not None and math.isfinite(float(r[f])) for f in feature_names)]
    if len(valid)<min_train or len({r["target_"+market] for r in valid})<2:
        return None,len(valid)
    X=[[float(r[f]) for f in feature_names] for r in valid]
    y=[int(r["target_"+market]) for r in valid]
    model=Pipeline([("scale",StandardScaler()),("lr",LogisticRegression(max_iter=2000,C=0.5,random_state=42))])
    model.fit(X,y)
    return model,len(valid)

def predict_for_features(model, feature, feature_names):
    if model is None or any(feature.get(f) is None for f in feature_names):
        return None
    values=[float(feature[f]) for f in feature_names]
    if not all(math.isfinite(v) for v in values):
        return None
    return float(model.predict_proba([values])[0,1])


def h2h_prior_meetings(history, target_kickoff):
    """Return only prior meetings; ties at the target kickoff are excluded."""
    times = [item[0] for item in history]
    return history[:bisect.bisect_left(times, target_kickoff)]


def h2h_result_from_target_home_perspective(old_match, target_home_id):
    """W/D/L from the target fixture's home team's perspective."""
    old_home, old_away = old_match["home_goals"], old_match["away_goals"]
    if old_match["home_id"] == target_home_id:
        return "W" if old_home > old_away else "D" if old_home == old_away else "L"
    if old_match["away_id"] == target_home_id:
        return "W" if old_away > old_home else "D" if old_away == old_home else "L"
    raise ValueError("Target home team is not present in the historical H2H fixture")


def h2h_duplicate_signature_diagnostics(matches):
    """Detect duplicate completed fixture signatures and return keys for quarantine."""
    groups = defaultdict(list)
    for row in matches:
        key = completed_fixture_signature_key(row)
        if key is None:
            continue
        _, _, pair = key
        home_id = str(row.get("home_id") or "").strip()
        # Normalize score orientation to the lexicographically first team ID.
        score = ((int(row["home_goals"]), int(row["away_goals"])) if home_id == pair[0]
                 else (int(row["away_goals"]), int(row["home_goals"])))
        groups[key].append({"fixture_id": str(row.get("fixture_id") or ""), "canonical_score": score})
    duplicate_groups = [(key, rows) for key, rows in groups.items() if len(rows) > 1]
    return {
        "valid_completed_signature_groups": len(groups),
        "duplicate_signature_groups": len(duplicate_groups),
        "duplicate_extra_rows": sum(len(rows) - 1 for _, rows in duplicate_groups),
        "conflicting_score_groups": sum(
            1 for _, rows in duplicate_groups if len({row["canonical_score"] for row in rows}) > 1
        ),
        "duplicate_signature_keys": [key for key, _ in duplicate_groups],
    }


def prediction_support_diagnostics(feature, model_fits, any_probability_available=False):
    """Expose why a fixture did or did not pass feature/training support gates.

    This is reporting-only. It never fills missing features or changes a model fit.
    model_fits maps each market to the (model, eligible_training_row_count) returned
    by make_model().
    """
    missing = [name for name in FEATURES if feature.get(name) is None]
    unavailable = [market for market, fit in model_fits.items() if fit[0] is None]
    if not missing:
        feature_status = "PASS_ALL_20_REQUIRED_FEATURES"
    else:
        feature_status = "BLOCKED_MISSING_REQUIRED_FEATURES"
    if not unavailable:
        training_status = "PASS_ALL_MARKET_MODELS"
    elif len(unavailable) == len(model_fits):
        training_status = "BLOCKED_ALL_MARKET_MODELS_UNAVAILABLE"
    else:
        training_status = "PARTIAL_MARKET_MODEL_TRAINING_GATE"
    if any_probability_available:
        block_reason = "RESEARCH_PREDICTION_AVAILABLE"
    elif missing and unavailable:
        block_reason = "BLOCKED_MISSING_FEATURES_AND_TRAINING_GATE"
    elif missing:
        block_reason = "BLOCKED_MISSING_REQUIRED_FEATURES"
    elif unavailable:
        block_reason = "BLOCKED_MODEL_TRAINING_GATE"
    else:
        block_reason = "BLOCKED_UNCLASSIFIED_NO_PREDICTION"
    return {
        "feature_support_status": feature_status,
        "missing_required_features": ";".join(missing),
        "training_support_status": training_status,
        "unavailable_training_markets": ";".join(unavailable),
        "training_eligible_rows_by_market": ";".join(
            f"{market}:{int(fit[1])}" for market, fit in model_fits.items()
        ),
        "prediction_block_reason": block_reason,
        "prediction_status": (
            "RAW_RESEARCH_ONLY" if any_probability_available else {
                "BLOCKED_MISSING_REQUIRED_FEATURES": "BLOCKED_MISSING_REQUIRED_FEATURES",
                "BLOCKED_MODEL_TRAINING_GATE": "BLOCKED_MODEL_TRAINING_GATE",
                "BLOCKED_MISSING_FEATURES_AND_TRAINING_GATE": "BLOCKED_MISSING_FEATURES_AND_TRAINING_GATE",
            }.get(block_reason, "BLOCKED_UNCLASSIFIED_NO_PREDICTION")
        ),
    }


def mask_combo_probabilities_for_export(rows):
    """Return export-safe copies with Combo probabilities masked until governed release gates pass."""
    masked = []
    for source in rows:
        row = dict(source)
        row["COMBO_HOME_probability_pct"] = None
        row["COMBO_AWAY_probability_pct"] = None
        row["combo_probability_status"] = "BLOCKED_SETTLEMENT_SPEC_MISMATCH"
        masked.append(row)
    return masked

def season_coverage_row(sid, meta, selected_id, selected, status, match_count, team_count=None):
    # Preserve only source-provided season metadata. Missing years remain unverified.
    def source_value(keys):
        for key in keys:
            value = meta.get(key)
            if value not in (None, ""):
                return str(value)
        return ""
    provider_competition_id = source_value(("provider_league_id", "provider_competition_id"))
    provider_competition_name = source_value(("provider_league_name", "provider_competition_name"))
    provider_season_year = source_value(("provider_season_year", "season_year", "year"))
    season_label = source_value(("season_name", "season_label", "season")) or provider_season_year
    season_start = source_value(("season_start", "start_date", "start", "starting_at", "season_start_date"))
    season_end = source_value(("season_end", "end_date", "end", "ending_at", "season_end_date"))
    date_year_match = re.match(r"^(\d{4})", season_start)
    season_start_year = date_year_match.group(1) if date_year_match else ""
    provider_year_match = re.match(r"^(\d{4})", provider_season_year)
    provider_season_start_year = provider_year_match.group(1) if provider_year_match else ""
    provider_id_ok = bool(provider_competition_id and provider_competition_id != "NOT_EXPOSED_BY_CATALOGUE")
    return {
        "season_id": str(sid), "selected_id": str(selected_id),
        "selected_id_type": "SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
        "provider_competition_id": provider_competition_id if provider_id_ok else "",
        "provider_competition_id_status": "FROM_PROVIDER_CATALOGUE_INGESTION_MANIFEST" if provider_id_ok else "UNAVAILABLE_IN_ARCHIVE_MANIFEST",
        "provider_competition_name_source": provider_competition_name,
        "provider_season_year_source": provider_season_year,
        "provider_season_start_year_from_source_label": provider_season_start_year,
        "country": str(selected.get("country", "")),
        "competition": str(selected.get("competition_name", "")),
        "season_label_source": season_label, "season_start_source": season_start,
        "season_end_source": season_end,
        "season_start_year_derived_from_source_date": season_start_year,
        "season_year_mapping_status": "PROVIDER_SEASON_YEAR_AVAILABLE" if provider_season_start_year else ("SOURCE_DATE_YEAR_AVAILABLE" if season_start_year else "UNVERIFIED_NO_SOURCE_YEAR"),
        "status": status, "match_count": int(match_count),
        "team_count": "" if team_count is None else int(team_count),
    }

def main():
    selected=list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig",newline="")))
    selected_by_id={str(r.get("selected_id","")).strip():r for r in selected}
    if len(selected)!=50 or len(selected_by_id)!=50 or "" in selected_by_id: raise SystemExit("Selected-50 manifest is not exactly 50 unique IDs.")

    # Separate provider match-record probe evidence from the older archive-catalogue metadata.
    # Official docs define match-record competition_id as the league season ID, not the parent competition ID.
    # This does not establish Oracle canonical IDs or settlement truth.
    parent_probe_rows=[]
    parent_probe_by_id={}
    parent_probe_status="PROBE_EVIDENCE_NOT_AVAILABLE"
    if PARENT_ID_PROBE.is_file():
        with PARENT_ID_PROBE.open(encoding="utf-8-sig",newline="") as probe_file:
            parent_probe_rows=list(csv.DictReader(probe_file))
        parent_probe_by_id={str(r.get("selected_id","")).strip():r for r in parent_probe_rows}
        if len(parent_probe_rows)!=50 or len(parent_probe_by_id)!=50 or "" in parent_probe_by_id:
            raise SystemExit("Parent-ID probe evidence must contain exactly 50 unique selected IDs; fail closed.")
        if set(parent_probe_by_id)!=set(selected_by_id):
            raise SystemExit("Parent-ID probe evidence IDs do not match the selected-50 manifest; fail closed.")
        if any(str(r.get("provider_competition_id","")).strip()!=sid for sid,r in parent_probe_by_id.items()):
            raise SystemExit("Parent-ID probe provider competition ID mismatch; fail closed.")
        if len({str(r.get("provider_match_id","")).strip() for r in parent_probe_rows})!=50:
            raise SystemExit("Parent-ID probe source match IDs are not unique; fail closed.")
        if any(not str(r.get("home_team_id","")).strip() or not str(r.get("away_team_id","")).strip() for r in parent_probe_rows):
            raise SystemExit("Parent-ID probe lacks one or more source team IDs; fail closed.")
        parent_probe_status="MATCH_RECORD_COMPETITION_ID_DOCUMENTED_AS_SEASON_ID_50_OF_50_PARENT_ID_NOT_PROVIDED"

    # Validate the persisted first-page coverage audit while keeping identity and settlement gates closed.
    if not IDENTITY_GATE_MATRIX.is_file():
        raise SystemExit("Selected-50 identity/market gate matrix missing; fail closed.")
    with IDENTITY_GATE_MATRIX.open(encoding="utf-8-sig", newline="") as matrix_file:
        identity_gate_rows = list(csv.DictReader(matrix_file))
    identity_gate_by_id = {str(r.get("selected_season_id", "")).strip(): r for r in identity_gate_rows}
    if len(identity_gate_rows) != 50 or len(identity_gate_by_id) != 50 or "" in identity_gate_by_id:
        raise SystemExit("Selected-50 identity/market gate matrix must contain exactly 50 unique IDs; fail closed.")
    if set(identity_gate_by_id) != set(selected_by_id):
        raise SystemExit("Identity/market gate matrix IDs do not match the selected-50 manifest; fail closed.")
    coverage_status_counts = Counter()
    for sid, row in identity_gate_by_id.items():
        row_count = int(row.get("provider_match_coverage_rows_first_page") or 0)
        if row.get("production_eligible") != "NO":
            raise SystemExit("Identity/market matrix contains a production-eligible row; fail closed.")
        if row.get("provider_to_canonical_bridge") != "UNVERIFIED" or row.get("official_settlement_truth") != "UNVERIFIED":
            raise SystemExit("Identity/market matrix promotes an unverified bridge or settlement truth; fail closed.")
        if row.get("provider_competition_id_observation_status") != "PROVIDER_DOCS_DEFINE_COMPETITION_ID_AS_SEASON_ID_NOT_PARENT_ID":
            raise SystemExit("Provider match competition_id must remain explicitly typed as season ID, not parent ID; fail closed.")
        if "Official FootyStats docs define league-matches competition_id as the league season ID" not in row.get("provider_competition_id_evidence_scope", ""):
            raise SystemExit("Official provider field-semantics evidence missing from identity matrix; fail closed.")
        if row.get("provider_competition_id_observed_value") != sid or row.get("provider_match_coverage_competition_id_matches_selected_id") != "YES":
            raise SystemExit("Observed provider competition-ID relationship mismatch; fail closed.")
        if row.get("provider_match_coverage_audit_run") != "40391540391":
            raise SystemExit("Unexpected or missing match-coverage evidence run; fail closed.")
        if row.get("provider_match_coverage_rows_first_page") != row.get("provider_match_coverage_unique_fixture_ids_first_page"):
            raise SystemExit("First-page fixture ID uniqueness contract failed; fail closed.")
        if row.get("provider_match_coverage_duplicate_fixture_rows_first_page") != "0" or row.get("provider_match_coverage_pager_max_page") != "1":
            raise SystemExit("First-page duplicate or pagination gate failed; fail closed.")
        for field in ("provider_match_coverage_rows_with_status", "provider_match_coverage_rows_with_both_team_ids",
                      "provider_match_coverage_rows_with_both_score_fields", "provider_match_coverage_rows_with_unix_kickoff"):
            if row.get(field) != str(row_count):
                raise SystemExit(f"First-page coverage field {field} is inconsistent; fail closed.")
        if row.get("provider_match_coverage_nonempty_season_id_field_rows") != "0":
            raise SystemExit("Unexpected explicit season_id values; review provider identity semantics; fail closed.")
        counts = json.loads(row.get("provider_match_coverage_status_counts_json") or "{}")
        if sum(int(v) for v in counts.values()) != row_count:
            raise SystemExit("Provider status counts do not reconcile to page row count; fail closed.")
        coverage_status_counts.update({str(k): int(v) for k, v in counts.items()})
    provider_match_coverage_status = "PASS_PROVIDER_MATCH_COVERAGE_CONTRACT_50_OF_50"

    with zipfile.ZipFile(ARCHIVE) as z:
        write_archive_consumption_receipt(
            ARCHIVE, z, OUT / "oracle_selected50_archive_consumption_receipt.json"
        )
        names=set(z.namelist())
        mn=next((n for n in names if n.endswith("ingestion_manifest.json")),None)
        if not mn: raise SystemExit("Private ingestion manifest missing.")
        raw_manifest=read_json(z,mn)
        if not isinstance(raw_manifest,list): raise SystemExit("Unexpected private ingestion manifest shape.")
        season_rows={str(r.get("season_id","")).strip():r for r in raw_manifest if isinstance(r,dict)}
        if len(season_rows)<200: raise SystemExit(f"Expected historical archive with at least 200 season rows; got {len(season_rows)}.")
        # Country + competition labels group historical seasons; exact parent provider IDs and provider season years
        # are preserved separately from the selected-season surrogate used for research grouping.
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
        # Parent provider IDs come from exact league-list season matches in the private ingestion manifest.
        provider_ids_by_label = defaultdict(set)
        for meta in season_rows.values():
            label = (str(meta.get("selected_country", "")).strip(), str(meta.get("selected_competition_name", "")).strip())
            if label not in selected_by_label: continue
            pid = str(meta.get("provider_league_id", "")).strip()
            if pid and pid != "NOT_EXPOSED_BY_CATALOGUE": provider_ids_by_label[label].add(pid)
        provider_parent_id_by_selected = {}
        for label, (selected_sid, _sel) in selected_by_label.items():
            ids = provider_ids_by_label.get(label, set())
            if len(ids) == 1:
                provider_parent_id_by_selected[selected_sid] = (next(iter(ids)), "VERIFIED_FROM_PROVIDER_CATALOGUE_MANIFEST")
            elif len(ids) > 1:
                provider_parent_id_by_selected[selected_sid] = ("", "AMBIGUOUS_PROVIDER_PARENT_ID_ACROSS_SEASONS")
            else:
                provider_parent_id_by_selected[selected_sid] = ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST")
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
                season_qa.append(season_coverage_row(sid,meta,cid,sel,"MISSING_MATCH_OR_TEAM_FILE",0))
                continue
            matches=read_json(z,mp); teams=read_json(z,tp); tables=read_json(z,tabp) if tabp else None
            if not isinstance(matches,list) or not isinstance(teams,list):
                season_qa.append(season_coverage_row(sid,meta,cid,sel,"UNEXPECTED_CONTAINER_SHAPE",0))
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
            raw_rows_seen = len(matches)
            retained_before_season = len(all_matches)
            rejected_non_object_rows = 0
            rejected_missing_kickoff_rows = 0
            rejected_missing_home_team_id_rows = 0
            rejected_missing_away_team_id_rows = 0
            rows_missing_normalized_fixture_id = 0
            rows_explicit_finished_status_missing_numeric_score = 0
            for m in matches:
                if not isinstance(m,dict):
                    rejected_non_object_rows += 1
                    continue
                h,a=team_ids(m)
                if m.get("id") in (None, ""):
                    rows_missing_normalized_fixture_id += 1
                source_status = str(get_first(m,("status","game_status")) or "").strip().lower()
                score_h, score_a = match_score(m)
                if source_status in FINISHED and (score_h is None or score_a is None):
                    rows_explicit_finished_status_missing_numeric_score += 1
                home_name=str(get_first(m,("home_name","home_team_name")) or "")
                away_name=str(get_first(m,("away_name","away_team_name")) or "")
                if not home_name and h: home_name=str(season_team_names.get((cid,sid,h),team_position.get((cid,h),{}).get("name","")))
                if not away_name and a: away_name=str(season_team_names.get((cid,sid,a),team_position.get((cid,a),{}).get("name","")))
                ts=stamp(m)
                if ts is None: rejected_missing_kickoff_rows += 1
                if not h: rejected_missing_home_team_id_rows += 1
                if not a: rejected_missing_away_team_id_rows += 1
                if ts is None or not h or not a: continue
                row={"fixture_id":str(m.get("id") or ""), "season_id":sid,"competition_id":cid,
                     "country":sel["country"],"league":sel["competition_name"],"home_id":h,"away_id":a,
                     "home_team":home_name,"away_team":away_name,"kickoff_unix":ts,
                     "status":str(get_first(m,("status","game_status")) or ""),
                     "home_goals":match_score(m)[0],"away_goals":match_score(m)[1],
                     "finished":finished(m),"raw_match":m}
                all_matches.append(row)
            season_row = season_coverage_row(sid,meta,cid,sel,"INGESTED",len(matches),len(teams))
            season_row.update({"raw_match_rows_seen": raw_rows_seen,
                "normalized_match_rows_retained": len(all_matches) - retained_before_season,
                "rejected_non_object_rows": rejected_non_object_rows,
                "rejected_missing_kickoff_rows": rejected_missing_kickoff_rows,
                "rejected_missing_home_team_id_rows": rejected_missing_home_team_id_rows,
                "rejected_missing_away_team_id_rows": rejected_missing_away_team_id_rows,
                "rows_missing_normalized_fixture_id": rows_missing_normalized_fixture_id,
                "rows_explicit_finished_status_missing_numeric_score": rows_explicit_finished_status_missing_numeric_score})
            season_qa.append(season_row)
        # Fail closed on unresolved competition mapping or gross archive loss.
        present_comps={r["competition_id"] for r in all_matches}
        if len(present_comps)!=50: raise SystemExit(f"Only {len(present_comps)} of 50 selected grouping keys yielded matches.")
        # Deduplicate by competition + fixture ID only; identical IDs across comps are distinct provider namespace.
        dedup={}
        for r in all_matches:
            key=(r["competition_id"],r["fixture_id"]) if r["fixture_id"] else (r["competition_id"],r["season_id"],r["kickoff_unix"],r["home_id"],r["away_id"])
            dedup.setdefault(key,r)
        matches=sorted(dedup.values(),key=lambda r:(r["competition_id"],r["kickoff_unix"],r["fixture_id"]))
        # Internal status/score/ID consistency audit; this is not official settlement verification.
        settlement_truth_qa = []
        for cid, sel in sorted(selected_by_id.items(), key=lambda kv: (kv[1].get("country", ""), kv[1].get("competition_name", ""))):
            raw_comp = [r for r in all_matches if str(r.get("competition_id")) == str(cid)]
            normalized_comp = [r for r in matches if str(r.get("competition_id")) == str(cid)]
            status_counts = Counter(str(r.get("status") or "UNKNOWN").strip() or "UNKNOWN" for r in raw_comp)
            status_score_counts = defaultdict(lambda: {"rows":0,"numeric_score_rows":0,"zero_zero_score_rows":0,"nonzero_score_rows":0,"missing_score_rows":0})
            final_status_missing_score = 0
            nonfinal_status_with_score = 0
            noninteger_score_rows = 0
            completed_total_goals_0_1_rows = 0
            combo_home_predictor_vs_ledger_disagreement_rows = 0
            combo_away_predictor_vs_ledger_disagreement_rows = 0
            for r in raw_comp:
                m = r.get("raw_match") or {}
                st = str(get_first(m, ("status", "game_status")) or "UNKNOWN").strip().lower() or "unknown"
                gh, ga = match_score(m)
                has_score = gh is not None and ga is not None
                status_score_counts[st]["rows"] += 1
                if has_score:
                    status_score_counts[st]["numeric_score_rows"] += 1
                    if float(gh) == 0 and float(ga) == 0:
                        status_score_counts[st]["zero_zero_score_rows"] += 1
                    else:
                        status_score_counts[st]["nonzero_score_rows"] += 1
                else:
                    status_score_counts[st]["missing_score_rows"] += 1
                if st in FINISHED and not has_score:
                    final_status_missing_score += 1
                if st in FINISHED and has_score and (gh + ga) <= 1:
                    completed_total_goals_0_1_rows += 1
                if st not in FINISHED and has_score:
                    nonfinal_status_with_score += 1
                if has_score and (not float(gh).is_integer() or not float(ga).is_integer()):
                    noninteger_score_rows += 1
            # Count actual predictor-vs-settlement disagreements on deduplicated,
            # explicitly finished records only. Numeric placeholders on nonfinal
            # rows are never treated as settled outcomes.
            for r in normalized_comp:
                m = r.get("raw_match") or {}
                st = str(get_first(m, ("status", "game_status")) or "UNKNOWN").strip().lower() or "unknown"
                gh, ga = match_score(m)
                if st not in FINISHED or gh is None or ga is None:
                    continue
                disagreements = combo_predictor_vs_ledger_disagreements(gh, ga)
                if disagreements is None:
                    continue
                combo_home_predictor_vs_ledger_disagreement_rows += int(disagreements[0])
                combo_away_predictor_vs_ledger_disagreement_rows += int(disagreements[1])
            settlement_truth_qa.append({
                "selected_id": str(cid), "selected_id_type": "SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
                "provider_competition_id": provider_parent_id_by_selected.get(str(cid), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[0],
                 "provider_competition_id_status": provider_parent_id_by_selected.get(str(cid), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[1],
                "country": sel.get("country", ""), "competition_name": sel.get("competition_name", ""),
                "source_rows_retained_for_id_time_validation": len(raw_comp), "normalized_rows_after_dedup": len(normalized_comp),
                "duplicate_rows_removed_by_dedup": len(raw_comp) - len(normalized_comp),
                "rows_missing_fixture_id": sum(1 for r in raw_comp if not r.get("fixture_id")),
                "rows_with_same_home_away_team_id": sum(1 for r in raw_comp if r.get("home_id") and r.get("home_id") == r.get("away_id")),
                "finished_status_with_numeric_score_rows": sum(1 for r in raw_comp if r.get("finished")),
                "finished_status_missing_numeric_score_rows": final_status_missing_score,
                "nonfinished_status_with_numeric_score_rows": nonfinal_status_with_score,
                "noninteger_numeric_score_rows": noninteger_score_rows,
                "completed_total_goals_0_1_rows": completed_total_goals_0_1_rows,
                "combo_home_predictor_vs_ledger_disagreement_rows": combo_home_predictor_vs_ledger_disagreement_rows,
                "combo_away_predictor_vs_ledger_disagreement_rows": combo_away_predictor_vs_ledger_disagreement_rows,
                "source_status_counts_json": json.dumps(dict(sorted(status_counts.items())), ensure_ascii=False, separators=(",", ":")),
                "status_score_cross_tab_json": json.dumps(dict(sorted(status_score_counts.items())), ensure_ascii=False, separators=(",", ":")),
                "settlement_truth_status": "INTERNAL_STATUS_SCORE_QA_ONLY_OFFICIAL_SETTLEMENT_UNVERIFIED",
                "production_eligible": "NO"
            })
        # Research-only score/identity gate: malformed completed scores and self-fixtures
        # are retained for QA but cannot become historical features or training labels.
        completed_status_rows=[r for r in matches if r["finished"]]
        invalid_completed_score_rows=[r for r in completed_status_rows
            if not valid_completed_score(r.get("home_goals"),r.get("away_goals"))]
        invalid_completed_team_identity_rows=[r for r in completed_status_rows
            if valid_completed_score(r.get("home_goals"),r.get("away_goals"))
            and (not str(r.get("home_id") or "").strip() or not str(r.get("away_id") or "").strip()
                 or str(r.get("home_id")) == str(r.get("away_id")))]
        h2h_duplicate_qa=h2h_duplicate_signature_diagnostics(matches)
        duplicate_signature_keys=set(h2h_duplicate_qa["duplicate_signature_keys"])
        duplicate_rows_quarantined=sum(
            1 for r in matches if completed_fixture_signature_key(r) in duplicate_signature_keys
        )
        # Duplicate-signature rows are excluded from history and labels, not merely counted.
        # Histories otherwise contain only explicit completed matches with valid integer scores and distinct team IDs.
        home_history=defaultdict(list); away_history=defaultdict(list); h2h_history=defaultdict(list)
        for r in matches:
            if completed_fixture_signature_key(r) in duplicate_signature_keys: continue
            if not r["finished"]: continue
            if not valid_completed_score(r.get("home_goals"),r.get("away_goals")): continue
            if not str(r.get("home_id") or "").strip() or not str(r.get("away_id") or "").strip(): continue
            if str(r.get("home_id")) == str(r.get("away_id")): continue
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
            h2h=h2h_prior_meetings(h2h_all,ts)
            last_h2h=h2h[-5:]
            h2h_btts=[]; h2h_home_results=[]; h2h_goals=[]
            for (_, old) in last_h2h:
                oh,oa=old["home_goals"],old["away_goals"]
                h2h_btts.append(int(oh>0 and oa>0)); h2h_goals.append(oh+oa)
                rel=h2h_result_from_target_home_perspective(old,r["home_id"])
                h2h_home_results.append(rel)
            f.update({"fixture_id":r["fixture_id"],"season_id":r["season_id"],"competition_id":comp,"country":r["country"],
                      "league":r["league"],"kickoff_unix":ts,"date_utc":dt.datetime.fromtimestamp(ts,dt.timezone.utc).isoformat(),
                      "home_team":r["home_team"],"away_team":r["away_team"],"home_id":r["home_id"],"away_id":r["away_id"],
                      "status":r["status"],"finished":r["finished"],"home_goals":r["home_goals"],"away_goals":r["away_goals"],
                      "home_recent5_results":"".join("W" if match_score(m)[0]>match_score(m)[1] else "D" if match_score(m)[0]==match_score(m)[1] else "L" for m,is_home in hh[-5:]),
                      "away_recent5_results":"".join("W" if match_score(m)[1]>match_score(m)[0] else "D" if match_score(m)[1]==match_score(m)[0] else "L" for m,is_home in ah[-5:]),
                      "home_recent5_n":len(hh[-5:]),"away_recent5_n":len(ah[-5:]),
                      "h2h_prior_n":len(h2h),"h2h_cross_season_prior_n":sum(1 for _, old in h2h if str(old.get("season_id")) != str(r["season_id"])),
                      "h2h_last5_results_home_perspective":"".join(h2h_home_results),
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
            f["confidence_score_status"]="NOT_CALCULATED_UNCALIBRATED_MODEL"
            f["data_risk_pct"]=None
            f["data_risk_status"]="NOT_QUANTIFIED_NO_VALIDATED_RISK_MAPPING"
            f["risk_profile"]="HIGH_UNVALIDATED" if all(f.get(k) is not None for k in FEATURES) else "CRITICAL_INCOMPLETE_INPUTS"
            f.update(market_targets_for_match(r, duplicate_signature_keys))
            feature_rows.append(f)
        # Research-only H2H integrity diagnostics. These do not change model inputs or eligibility.
        team_id_names=defaultdict(set); team_id_seasons=defaultdict(set); normalized_name_ids=defaultdict(set)
        for match in matches:
            for side in ("home","away"):
                tid=str(match.get(side+"_id") or "").strip()
                name=" ".join(str(match.get(side+"_team") or "").casefold().split())
                if not tid or not name: continue
                key=(str(match.get("competition_id") or ""),tid)
                team_id_names[key].add(name)
                team_id_seasons[key].add(str(match.get("season_id") or ""))
                normalized_name_ids[(str(match.get("competition_id") or ""),name)].add(tid)
        h2h_rows_with_prior=[r for r in feature_rows if int(r.get("h2h_prior_n") or 0)>0]
        h2h_rows_cross_season=[r for r in feature_rows if int(r.get("h2h_cross_season_prior_n") or 0)>0]
        h2h_cutoff_violations=0
        for row in feature_rows:
            last_date=row.get("h2h_last_date_utc")
            if not last_date: continue
            try:
                last_ts=dt.datetime.fromisoformat(str(last_date).replace("Z","+00:00")).timestamp()
                if last_ts >= float(row["kickoff_unix"]): h2h_cutoff_violations += 1
            except (ValueError,TypeError,OverflowError,KeyError):
                h2h_cutoff_violations += 1
        h2h_history_qa={
            "status":"RESEARCH_ONLY_H2H_HISTORY_DIAGNOSTICS",
            "history_source_rows":len(matches),
            "explicit_finished_status_rows":len(completed_status_rows),
            "explicit_finished_with_valid_integer_scores":len(completed_status_rows)-len(invalid_completed_score_rows),
            "explicit_finished_with_invalid_or_noninteger_scores_excluded":len(invalid_completed_score_rows),
            "valid_score_rows_excluded_from_history_for_missing_or_same_team_ids":len(invalid_completed_team_identity_rows),
            "feature_rows_checked":len(feature_rows),
            "duplicate_fixture_signature_groups_same_competition_kickoff_team_pair":h2h_duplicate_qa["duplicate_signature_groups"],
            "duplicate_fixture_signature_extra_rows":h2h_duplicate_qa["duplicate_extra_rows"],
            "duplicate_fixture_signature_conflicting_score_groups":h2h_duplicate_qa["conflicting_score_groups"],
            "duplicate_fixture_rows_quarantined_from_history_and_labels":duplicate_rows_quarantined,
            "research_label_integrity_status":("BLOCKED_DUPLICATE_FIXTURE_SIGNATURES_QUARANTINED_FROM_HISTORY_AND_LABELS" if h2h_duplicate_qa["duplicate_signature_groups"] else "TECHNICAL_SCORE_AND_DUPLICATE_CHECKS_PASS_CANONICAL_SETTLEMENT_UNVERIFIED"),
            "rows_with_any_prior_h2h":len(h2h_rows_with_prior),
            "rows_with_cross_season_prior_h2h":len(h2h_rows_cross_season),
            "cross_season_prior_meeting_count_sum":sum(int(r.get("h2h_cross_season_prior_n") or 0) for r in feature_rows),
            "strict_kickoff_cutoff_violations":h2h_cutoff_violations,
            "competition_team_ids_with_multiple_normalized_names":sum(1 for names in team_id_names.values() if len(names)>1),
            "competition_team_ids_seen_across_multiple_seasons":sum(1 for seasons in team_id_seasons.values() if len(seasons-{""})>1),
            "competition_normalized_names_mapped_to_multiple_team_ids":sum(1 for ids in normalized_name_ids.values() if len(ids)>1),
            "limitations":["Name variation counts are diagnostics, not proof of a wrong identity; manual canonical review remains required.",
                           "Provider team IDs and source completeness are not certified by these counts.",
                           "H2H rows are scoped to the research-selected competition group and provider team IDs; ambiguous IDs are not automatically reconciled."]
        }
        if h2h_cutoff_violations:
            raise SystemExit("H2H strict pre-kickoff cutoff audit failed; fail closed.")
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
        # Paired research-only ablation: frozen 20-feature baseline vs the same baseline plus numeric H2H features.
        # The existing production/research baseline fit and probabilities above remain untouched.
        h2h_feature_names = ["h2h_prior_n", "h2h_btts_rate_last5", "h2h_avg_total_goals_last5", "h2h_days_since_last"]
        for row in feature_rows:
            last_date = row.get("h2h_last_date_utc")
            days_since = None
            if last_date:
                try:
                    last_ts = dt.datetime.fromisoformat(str(last_date).replace("Z","+00:00")).timestamp()
                    days_since = max(0.0, (float(row["kickoff_unix"]) - last_ts) / 86400.0)
                except (ValueError, TypeError, OverflowError):
                    days_since = None
            row["h2h_days_since_last"] = days_since
        h2h_comparison = []
        h2h_fixture_rows = []
        h2h_common_train = [r for r in train_pre if
            all(r.get(k) is not None and math.isfinite(float(r[k])) for k in FEATURES + h2h_feature_names)]
        for market in MARKETS:
            # Train both sides of the ablation on the exact same historical rows to isolate H2H feature value.
            base_model, base_train_n = make_model_for_features(h2h_common_train, market, FEATURES)
            candidate_features = FEATURES + h2h_feature_names
            candidate_model, candidate_train_n = make_model_for_features(h2h_common_train, market, candidate_features)
            base_test = [r for r in test_rows if r.get("target_"+market) is not None and
                         all(r.get(k) is not None and math.isfinite(float(r[k])) for k in FEATURES)]
            paired_test = [r for r in base_test if all(r.get(k) is not None and math.isfinite(float(r[k])) for k in h2h_feature_names)]
            base_probs = [predict_for_features(base_model, r, FEATURES) for r in paired_test]
            cand_probs = [predict_for_features(candidate_model, r, candidate_features) for r in paired_test]
            paired = [(r, bp, cp, int(r["target_"+market])) for r,bp,cp in zip(paired_test,base_probs,cand_probs)
                      if bp is not None and cp is not None]
            if paired:
                labels=[x[3] for x in paired]; bp=[x[1] for x in paired]; cp=[x[2] for x in paired]
                base_brier=brier_score_loss(labels,bp); cand_brier=brier_score_loss(labels,cp)
                base_ll=log_loss(labels,[min(max(p,1e-6),1-1e-6) for p in bp],labels=[0,1])
                cand_ll=log_loss(labels,[min(max(p,1e-6),1-1e-6) for p in cp],labels=[0,1])
                base_acc=accuracy_score(labels,[int(p>=0.5) for p in bp])
                cand_acc=accuracy_score(labels,[int(p>=0.5) for p in cp])
                auc_base=roc_auc_score(labels,bp) if len(set(labels))==2 else None
                auc_cand=roc_auc_score(labels,cp) if len(set(labels))==2 else None
                result_status="PAIRED_RESEARCH_ONLY_NOT_CALIBRATED"
                for r, bprob, cprob, label in paired:
                    h2h_fixture_rows.append({"fixture_id":r.get("fixture_id",""),"date_utc":r.get("date_utc",""),
                        "competition_id":r.get("competition_id",""),"league":r.get("league",""),
                        "home_team":r.get("home_team",""),"away_team":r.get("away_team",""),
                        "market":market,"actual":label,"baseline_probability":round(bprob,8),
                        "h2h_candidate_probability":round(cprob,8),"h2h_prior_n":r.get("h2h_prior_n"),
                        "h2h_btts_rate_last5":r.get("h2h_btts_rate_last5"),
                        "h2h_avg_total_goals_last5":r.get("h2h_avg_total_goals_last5"),
                        "h2h_days_since_last":r.get("h2h_days_since_last"),
                        "baseline_correct":int((bprob>=0.5)==bool(label)),
                        "h2h_candidate_correct":int((cprob>=0.5)==bool(label))})
            else:
                base_brier=cand_brier=base_ll=cand_ll=base_acc=cand_acc=auc_base=auc_cand=None
                result_status="NO_PAIRED_TEST_PREDICTIONS"
            h2h_comparison.append({"market":market,"status":result_status,
                "test_window":"2025-03-20 through 2026-09-20",
                "baseline_features":"EXISTING_20_FEATURES",
                "candidate_features":"EXISTING_20_PLUS_4_H2H_FEATURES",
                "baseline_train_n":base_train_n,"candidate_train_n":candidate_train_n,
                "baseline_test_n":len(base_test),"h2h_available_test_n":len(paired_test),
                "paired_test_n":len(paired),
                "h2h_test_coverage_pct":round(100*len(paired_test)/len(base_test),2) if base_test else None,
                "baseline_accuracy_at_0_5":round(float(base_acc),5) if base_acc is not None else None,
                "candidate_accuracy_at_0_5":round(float(cand_acc),5) if cand_acc is not None else None,
                "accuracy_delta_candidate_minus_baseline":round(float(cand_acc-base_acc),5) if cand_acc is not None and base_acc is not None else None,
                "baseline_brier":round(float(base_brier),5) if base_brier is not None else None,
                "candidate_brier":round(float(cand_brier),5) if cand_brier is not None else None,
                "brier_delta_candidate_minus_baseline":round(float(cand_brier-base_brier),5) if cand_brier is not None and base_brier is not None else None,
                "baseline_log_loss":round(float(base_ll),5) if base_ll is not None else None,
                "candidate_log_loss":round(float(cand_ll),5) if cand_ll is not None else None,
                "log_loss_delta_candidate_minus_baseline":round(float(cand_ll-base_ll),5) if cand_ll is not None and base_ll is not None else None,
                "baseline_auc":round(float(auc_base),5) if auc_base is not None else None,
                "candidate_auc":round(float(auc_cand),5) if auc_cand is not None else None,
                "baseline_ece_10_bins":expected_calibration_error(labels,bp) if paired else None,
                "candidate_ece_10_bins":expected_calibration_error(labels,cp) if paired else None,
                "production_eligible":"NO","betting_eligible":"NO"})
        # Additional chronological folds deliberately include 2024 as a test period and as training history
        # for later folds. Every fold trains strictly before its test start; this does not replace the primary holdout.
        h2h_fold_edges = [
            ("H2H_WF1_2024H1", dt.datetime(2024,1,1,tzinfo=dt.timezone.utc).timestamp(), dt.datetime(2024,7,1,tzinfo=dt.timezone.utc).timestamp()),
            ("H2H_WF2_2024H2", dt.datetime(2024,7,1,tzinfo=dt.timezone.utc).timestamp(), dt.datetime(2025,1,1,tzinfo=dt.timezone.utc).timestamp()),
            ("H2H_WF3_2025H1", dt.datetime(2025,1,1,tzinfo=dt.timezone.utc).timestamp(), dt.datetime(2025,7,1,tzinfo=dt.timezone.utc).timestamp()),
            ("H2H_WF4_2025H2", dt.datetime(2025,7,1,tzinfo=dt.timezone.utc).timestamp(), dt.datetime(2026,1,1,tzinfo=dt.timezone.utc).timestamp()),
            ("H2H_WF5_2026H1", dt.datetime(2026,1,1,tzinfo=dt.timezone.utc).timestamp(), dt.datetime(2026,7,1,tzinfo=dt.timezone.utc).timestamp()),
        ]
        h2h_expanding_rows=[]
        for fold_name, fold_start, fold_end in h2h_fold_edges:
            fold_train=[r for r in train_rows if r.get("kickoff_unix",0)<fold_start]
            fold_test=[r for r in train_rows if fold_start<=r.get("kickoff_unix",0)<fold_end]
            common_train=[r for r in fold_train if
                all(r.get(k) is not None and math.isfinite(float(r[k])) for k in FEATURES+h2h_feature_names)]
            for market in MARKETS:
                candidate_features=FEATURES+h2h_feature_names
                base_model,base_n=make_model_for_features(common_train,market,FEATURES)
                cand_model,cand_n=make_model_for_features(common_train,market,candidate_features)
                eligible=[r for r in fold_test if r.get("target_"+market) is not None and
                    all(r.get(k) is not None and math.isfinite(float(r[k])) for k in FEATURES+h2h_feature_names)]
                bprob=[predict_for_features(base_model,r,FEATURES) for r in eligible]
                cprob=[predict_for_features(cand_model,r,candidate_features) for r in eligible]
                paired=[(r,b,c,int(r["target_"+market])) for r,b,c in zip(eligible,bprob,cprob) if b is not None and c is not None]
                if paired:
                    yy=[x[3] for x in paired]; bp0=[x[1] for x in paired]; cp0=[x[2] for x in paired]
                    ba=accuracy_score(yy,[int(p>=0.5) for p in bp0]); ca=accuracy_score(yy,[int(p>=0.5) for p in cp0])
                    bb=brier_score_loss(yy,bp0); cb=brier_score_loss(yy,cp0)
                    bl=log_loss(yy,[min(max(p,1e-6),1-1e-6) for p in bp0],labels=[0,1])
                    cl=log_loss(yy,[min(max(p,1e-6),1-1e-6) for p in cp0],labels=[0,1])
                    aucb=roc_auc_score(yy,bp0) if len(set(yy))==2 else None
                    aucc=roc_auc_score(yy,cp0) if len(set(yy))==2 else None
                    status="EXPANDING_WINDOW_RESEARCH_ONLY_NOT_CALIBRATED"
                else:
                    ba=ca=bb=cb=bl=cl=aucb=aucc=None
                    status="INSUFFICIENT_PAIRED_TEST_PREDICTIONS"
                h2h_expanding_rows.append({"fold":fold_name,"test_start_utc":dt.datetime.fromtimestamp(fold_start,dt.timezone.utc).isoformat(),
                    "test_end_exclusive_utc":dt.datetime.fromtimestamp(fold_end,dt.timezone.utc).isoformat(),"market":market,
                    "training_cutoff_exclusive_utc":dt.datetime.fromtimestamp(fold_start,dt.timezone.utc).isoformat(),
                    "baseline_train_n":base_n,"candidate_train_n":cand_n,"test_n_h2h_available":len(eligible),
                    "paired_test_n":len(paired),"status":status,
                    "baseline_accuracy_at_0_5":round(float(ba),5) if ba is not None else None,
                    "candidate_accuracy_at_0_5":round(float(ca),5) if ca is not None else None,
                    "accuracy_delta_candidate_minus_baseline":round(float(ca-ba),5) if ca is not None and ba is not None else None,
                    "baseline_brier":round(float(bb),5) if bb is not None else None,
                    "candidate_brier":round(float(cb),5) if cb is not None else None,
                    "brier_delta_candidate_minus_baseline":round(float(cb-bb),5) if cb is not None and bb is not None else None,
                    "baseline_log_loss":round(float(bl),5) if bl is not None else None,
                    "candidate_log_loss":round(float(cl),5) if cl is not None else None,
                    "log_loss_delta_candidate_minus_baseline":round(float(cl-bl),5) if cl is not None and bl is not None else None,
                    "baseline_auc":round(float(aucb),5) if aucb is not None else None,
                    "candidate_auc":round(float(aucc),5) if aucc is not None else None,
                    "production_eligible":"NO","betting_eligible":"NO"})
        h2h_expanding_path=OUT/"oracle_selected50_h2h_expanding_window_metrics.json"
        h2h_expanding_path.write_text(json.dumps({"status":"RESEARCH_ONLY_CHRONOLOGICAL_FOLDS_NOT_CALIBRATED",
            "fold_policy":"Expanding history strictly before each fold start; H2H and baseline trained on the same H2H-eligible training rows.",
            "feature_set":"EXISTING_20_PLUS_4_H2H_FEATURES_FOR_CANDIDATE",
            "folds":h2h_expanding_rows},indent=2)+"\n",encoding="utf-8")
        h2h_json_path=OUT/"oracle_selected50_h2h_ablation_metrics.json"
        h2h_json_path.write_text(json.dumps({"status":"RESEARCH_ONLY_ABLATION_NOT_CALIBRATED",
            "primary_window":"2025-03-20 through 2026-09-20",
            "h2h_feature_names":h2h_feature_names,
            "interpretation":"Paired holdout comparison only. A positive delta means the candidate metric is numerically higher; for Brier/log loss lower is better. No betting or production approval.",
            "markets":h2h_comparison},indent=2)+"\n",encoding="utf-8")
        h2h_csv_path=OUT/"oracle_selected50_h2h_paired_predictions.csv"
        h2h_columns=["fixture_id","date_utc","competition_id","league","home_team","away_team","market","actual",
            "baseline_probability","h2h_candidate_probability","h2h_prior_n","h2h_btts_rate_last5",
            "h2h_avg_total_goals_last5","h2h_days_since_last","baseline_correct","h2h_candidate_correct"]
        with h2h_csv_path.open("w",newline="",encoding="utf-8") as h2h_file:
            writer=csv.DictWriter(h2h_file,fieldnames=h2h_columns);writer.writeheader();writer.writerows(h2h_fixture_rows)
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
                "selected_id":selected_id,"selected_id_type":"SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
                "provider_competition_id":provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[0],
                 "provider_competition_id_status":provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[1],
                "country":sel.get("country",""),"competition_name":sel.get("competition_name",""),
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
            model_fits={m:make_model(eligible_train,m) for m in MARKETS}
            models={m:fit[0] for m,fit in model_fits.items()}
            for r in targets:
                f=next((x for x in feature_rows if x.get("fixture_id")==r["fixture_id"] and x.get("competition_id")==r["competition_id"] and x.get("kickoff_unix")==r["kickoff_unix"]),None)
                if not f: continue
                row={"fixture_id":r["fixture_id"],"date_utc":dt.datetime.fromtimestamp(r["kickoff_unix"],dt.timezone.utc).isoformat(),
                     "selected_id":str(r["competition_id"]),
                     "selected_id_type":"SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
                     "provider_competition_id":provider_parent_id_by_selected.get(str(r["competition_id"]), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[0],
                     "provider_competition_id_status":provider_parent_id_by_selected.get(str(r["competition_id"]), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[1],
                     "provider_competition_name_source":str(season_rows.get(str(r["season_id"]), {}).get("provider_league_name", "")),
                     "provider_season_year_source":str(season_rows.get(str(r["season_id"]), {}).get("provider_season_year", "")),
                     "provider_season_id":str(r["season_id"]),
                     "home_team_provider_id":str(r.get("home_id") or ""),"away_team_provider_id":str(r.get("away_id") or ""),
                     "source_fixture_id_status":"PRESENT" if r.get("fixture_id") else "MISSING",
                     "source_team_ids_status":"PRESENT" if r.get("home_id") and r.get("away_id") else "MISSING",
                     "canonical_fixture_join_status":"NOT_VERIFIED",
                     "canonical_team_join_status":"NOT_VERIFIED",
                     "settlement_truth_status":"NOT_VERIFIED_AGAINST_PRODUCTION_MARKET_SPEC",
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
                     "confidence_score_pct":f["confidence_score_pct"],"confidence_score_status":f["confidence_score_status"],"data_risk_pct":f["data_risk_pct"],"data_risk_status":f["data_risk_status"],
                     "risk_profile":f["risk_profile"],
                     "odds_named_field_count":f["odds_named_field_count"],"xg_named_field_count":f["xg_named_field_count"],
                     "odds_xg_provenance_status":"UNVERIFIED_NOT_USED_IN_MODEL","calibration_status":"RAW_ONLY_UNCALIBRATED",
                     "production_eligible":"NO"}
                for market in MARKETS: row[market+"_probability_pct"]=round(100*predict(models[market],f),2) if predict(models[market],f) is not None else None
                has_probability=any(row[m+"_probability_pct"] is not None for m in MARKETS)
                row.update(prediction_support_diagnostics(f, model_fits, has_probability))
                predictions.append(row)
        # Write private normalized research package.
        normalized_path=OUT/"normalized_selected50_matches.csv"
        with normalized_path.open("w",newline="",encoding="utf-8") as f:
            cols=["fixture_id","season_id","selected_id","selected_id_type","provider_competition_id","provider_competition_id_status","provider_competition_name_source","provider_season_year_source","country","league","home_id","away_id","home_team","away_team","kickoff_unix","status","finished","home_goals","away_goals"]
            w=csv.DictWriter(f,fieldnames=cols);w.writeheader()
            for r in matches:
                out_row={k:r.get(k) for k in cols if k in r}
                provider_id, provider_id_status = provider_parent_id_by_selected.get(str(r.get("competition_id") or ""), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))
                season_meta = season_rows.get(str(r.get("season_id") or ""), {})
                out_row.update({"selected_id":str(r.get("competition_id") or ""),
                    "selected_id_type":"SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
                    "provider_competition_id":provider_id,
                    "provider_competition_id_status":provider_id_status,
                    "provider_competition_name_source":str(season_meta.get("provider_league_name", "")),
                    "provider_season_year_source":str(season_meta.get("provider_season_year", ""))})
                w.writerow(out_row)
        feature_path=OUT/"selected50_feature_rows.csv"
        if feature_rows:
            with feature_path.open("w",newline="",encoding="utf-8") as f:
                cols=[("selected_id" if k=="competition_id" else k) for k in feature_rows[0].keys()]
                cols += ["selected_id_type","provider_competition_id","provider_competition_id_status","provider_competition_name_source","provider_season_year_source"]
                w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader()
                for row in feature_rows:
                    out_row={("selected_id" if k=="competition_id" else k):v for k,v in row.items()}
                    provider_id, provider_id_status = provider_parent_id_by_selected.get(str(row.get("competition_id") or ""), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))
                    season_meta = season_rows.get(str(row.get("season_id") or ""), {})
                    out_row.update({"selected_id_type":"SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
                        "provider_competition_id":provider_id,"provider_competition_id_status":provider_id_status,
                        "provider_competition_name_source":str(season_meta.get("provider_league_name", "")),
                        "provider_season_year_source":str(season_meta.get("provider_season_year", ""))})
                    w.writerow(out_row)
        pred_path=OUT/"oracle_selected50_prediction_report.csv"
        export_predictions = mask_combo_probabilities_for_export(predictions)
        if export_predictions:
            with pred_path.open("w",newline="",encoding="utf-8") as f:
                cols=list(export_predictions[0].keys());w=csv.DictWriter(f,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(export_predictions)
        else: pred_path.write_text("prediction_status,combo_probability_status\nNO_ELIGIBLE_FUTURE_FIXTURES_OR_FEATURE_GATES_FAILED,BLOCKED_SETTLEMENT_SPEC_MISMATCH\n",encoding="utf-8")
        # Produce a separate governed view: retain supported non-Combo research values for analysis,
        # but never present any market as betting-approved. Mask Combo probabilities until predictor
        # target and settlement-ledger definitions are reconciled.
        combo_block_reason = ("Research-only block: the existing predictor target is Double Chance AND total goals "
                              "between 2 and 4 inclusive, while the current settlement helper uses Double Chance AND "
                              "total goals < 5, including 0-1 goals. The authoritative market definition is unresolved; "
                              "do not reconcile these rules by silently changing either definition. Probabilities remain "
                              "masked pending an approved market definition, canonical fixture/team joins, and official "
                              "settlement truth.")
        noncombo_block_reason = ("Research-only: canonical fixture/team joins and production settlement truth "
                                 "remain unverified; raw probabilities are uncalibrated and not approved for betting.")
        governed_predictions = []
        for source_row in predictions:
            governed_row = dict(source_row)
            governed_row["governed_prediction_status"] = "RESEARCH_ONLY_NOT_FOR_BETTING"
            governed_row["governed_block_reason"] = noncombo_block_reason
            governed_row["production_eligible"] = "NO"
            for market in MARKETS:
                probability_key = market + "_probability_pct"
                if market in ("COMBO_HOME", "COMBO_AWAY"):
                    governed_row[probability_key] = None
                    governed_row[market + "_governed_status"] = "BLOCKED_SETTLEMENT_SPEC_MISMATCH"
                    governed_row[market + "_block_reason"] = combo_block_reason
                elif source_row.get(probability_key) is None:
                    governed_row[market + "_governed_status"] = "BLOCKED_INPUT_OR_TRAINING_GATE"
                    governed_row[market + "_block_reason"] = "No raw research probability was produced by the feature/training gate."
                else:
                    governed_row[market + "_governed_status"] = "RESEARCH_ONLY_NOT_FOR_BETTING"
                    governed_row[market + "_block_reason"] = noncombo_block_reason
            if not any(source_row.get(market + "_probability_pct") is not None for market in MARKETS):
                governed_row["governed_prediction_status"] = "BLOCKED_NO_SUPPORTED_PREDICTION"
            governed_predictions.append(governed_row)
        governed_path = OUT / "oracle_selected50_governed_fixture_report.csv"
        if governed_predictions:
            with governed_path.open("w", newline="", encoding="utf-8") as governed_file:
                governed_columns = list(governed_predictions[0].keys())
                governed_writer = csv.DictWriter(governed_file, fieldnames=governed_columns, extrasaction="ignore")
                governed_writer.writeheader()
                governed_writer.writerows(governed_predictions)
        else:
            governed_path.write_text("governed_prediction_status\nNO_FIXTURES\n", encoding="utf-8")
        governed_report_qa = {
            "status": "RESEARCH_ONLY_COMBO_BLOCKED",
            "fixture_rows": len(governed_predictions),
            "unique_source_fixture_ids": len({str(r.get("fixture_id") or "") for r in governed_predictions if r.get("fixture_id")}),
            "raw_combo_home_probabilities_masked": sum(1 for r in predictions if r.get("COMBO_HOME_probability_pct") is not None),
            "raw_combo_away_probabilities_masked": sum(1 for r in predictions if r.get("COMBO_AWAY_probability_pct") is not None),
            "combo_home_probabilities_remaining": sum(1 for r in governed_predictions if r.get("COMBO_HOME_probability_pct") is not None),
            "combo_away_probabilities_remaining": sum(1 for r in governed_predictions if r.get("COMBO_AWAY_probability_pct") is not None),
            "all_rows_production_ineligible": all(r.get("production_eligible") == "NO" for r in governed_predictions),
            "all_combo_probabilities_blocked": all(r.get("COMBO_HOME_probability_pct") is None and r.get("COMBO_AWAY_probability_pct") is None for r in governed_predictions),
            "all_combo_probabilities_masked_in_prediction_report": all(r.get("COMBO_HOME_probability_pct") is None and r.get("COMBO_AWAY_probability_pct") is None and r.get("combo_probability_status") == "BLOCKED_SETTLEMENT_SPEC_MISMATCH" for r in export_predictions),
            "combo_block_reason": combo_block_reason,
            "other_market_probabilities": "Retained only as raw research outputs; each is explicitly NOT_FOR_BETTING while canonical joins, settlement truth and calibration remain unverified."
        }
        if len(governed_predictions) != len(predictions):
            raise RuntimeError("Governed fixture report changed the source prediction row count")
        if not governed_report_qa["all_rows_production_ineligible"] or not governed_report_qa["all_combo_probabilities_blocked"]:
            raise RuntimeError("Governed fixture report failed its fail-closed market/production gate")
        governed_qa_path = OUT / "oracle_selected50_governed_fixture_report_qa.json"
        governed_qa_path.write_text(json.dumps(governed_report_qa, indent=2) + "\n", encoding="utf-8")
        schedule_path=OUT/"oracle_selected50_schedule_coverage.csv"
        with schedule_path.open("w",newline="",encoding="utf-8") as sf:
            scols=["selected_id","selected_id_type","provider_competition_id","provider_competition_id_status","country","competition_name","archive_match_rows","completed_match_rows","upcoming_fixture_count_7d","first_upcoming_kickoff_utc","last_upcoming_kickoff_utc","schedule_coverage_status","production_eligible"]
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
        league_walk_forward_metrics = []
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
                                         "accuracy_at_0_5":None,"accuracy_95ci_low":None,"accuracy_95ci_high":None,
                                         "brier":None,"log_loss":None,"auc":None,"ece_10_bins":None,
                                         "baseline_brier":None,"brier_skill_vs_prevalence":None})
                    for selected_id, sel in selected_by_id.items():
                        lg_train = [r for r in fold_train if str(r["competition_id"]) == str(selected_id)]
                        lg_test = [r for r in fold_test if str(r["competition_id"]) == str(selected_id)]
                        league_walk_forward_metrics.append({
                            "selected_id":str(selected_id),"selected_id_type":"SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
                            "provider_competition_id":provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[0],
                         "provider_competition_id_status":provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[1],"country":sel.get("country",""),
                            "league":sel.get("competition_name",""),"market":market,"fold":fold_name,
                            "train_n":len(lg_train),"test_n":len(lg_test),
                            "sample_gate":"INSUFFICIENT_SAMPLE_MIN_100_TRAIN_AND_TEST" if len(lg_train)<100 or len(lg_test)<100 else "SAMPLE_GATE_MET",
                            "status":"INSUFFICIENT_TRAIN_OR_TEST","accuracy_at_0_5":None,
                            "accuracy_95ci_low":None,"accuracy_95ci_high":None,"brier":None,
                            "log_loss":None,"auc":None,"ece_10_bins":None,
                            "training_prevalence_league":None,"baseline_majority_accuracy_league":None,
                            "baseline_brier_league_prevalence":None,"brier_skill_vs_league_prevalence":None,
                            "production_eligible":"NO","edge_claim":"NOT_APPROVED"})
                    continue
                fp_all = [predict(model, r) for r in fold_test]
                valid = [(r, p) for r, p in zip(fold_test, fp_all) if p is not None]
                fold_test_eval = [r for r, p in valid]
                fp = [p for r, p in valid]
                fy = [int(r["target_"+market]) for r in fold_test_eval]
                train_prev = sum(int(r["target_"+market]) for r in fold_train)/len(fold_train) if fold_train else None
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
                    "ece_10_bins":expected_calibration_error(fy,fp),
                    "training_prevalence":round(train_prev,5) if train_prev is not None else None,
                    "baseline_brier":round(base_brier,5) if base_brier is not None else None,
                    "brier_skill_vs_prevalence":round(1-brier_score_loss(fy,fp)/base_brier,5) if base_brier else None})
                # Per-competition metrics use the pooled fold model, evaluated only on that
                # competition's test rows; baselines use that competition's training labels only.
                for selected_id, sel in selected_by_id.items():
                    lg_train = [r for r in fold_train if str(r["competition_id"]) == str(selected_id)]
                    lg_indices = [idx for idx, r in enumerate(fold_test_eval) if str(r["competition_id"]) == str(selected_id)]
                    ly = [fy[idx] for idx in lg_indices]
                    lp = [fp[idx] for idx in lg_indices]
                    lg_train_n = len(lg_train)
                    lg_test_n = len(ly)
                    lg_prev = (sum(int(r["target_"+market]) for r in lg_train)/lg_train_n) if lg_train_n else None
                    lg_baseline_probs = [lg_prev]*lg_test_n if lg_prev is not None and lg_test_n else []
                    lg_baseline_brier = brier_score_loss(ly, lg_baseline_probs) if lg_baseline_probs else None
                    lg_brier = brier_score_loss(ly, lp) if lp else None
                    lg_majority = int(lg_prev >= 0.5) if lg_prev is not None else None
                    lg_baseline_accuracy = accuracy_score(ly, [lg_majority]*lg_test_n) if lg_test_n and lg_majority is not None else None
                    lg_labels = [int(p >= 0.5) for p in lp]
                    lg_correct = sum(int(p) == int(y0) for p,y0 in zip(lg_labels,ly))
                    lg_ci_low, lg_ci_high = wilson_interval(lg_correct, lg_test_n)
                    lg_gate = "INSUFFICIENT_SAMPLE_MIN_100_TRAIN_AND_TEST" if lg_train_n < 100 or lg_test_n < 100 else "SAMPLE_GATE_MET_DIAGNOSTIC_ONLY"
                    league_walk_forward_metrics.append({
                        "selected_id":str(selected_id),"selected_id_type":"SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
                        "provider_competition_id":provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[0],
                         "provider_competition_id_status":provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[1],"country":sel.get("country",""),
                        "league":sel.get("competition_name",""),"market":market,"fold":fold_name,
                        "train_n":lg_train_n,"test_n":lg_test_n,"sample_gate":lg_gate,
                        "status":"NO_TEST_ROWS" if not lg_test_n else "RAW_POOLED_MODEL_LEAGUE_SUBSET_NOT_CALIBRATED",
                        "accuracy_at_0_5":round(accuracy_score(ly,lg_labels),5) if ly else None,
                        "accuracy_95ci_low":round(lg_ci_low,5) if lg_ci_low is not None else None,
                        "accuracy_95ci_high":round(lg_ci_high,5) if lg_ci_high is not None else None,
                        "brier":round(lg_brier,5) if lg_brier is not None else None,
                        "log_loss":round(log_loss(ly,[min(max(p,1e-6),1-1e-6) for p in lp],labels=[0,1]),5) if lp else None,
                        "auc":round(roc_auc_score(ly,lp),5) if len(set(ly))==2 else None,
                        "ece_10_bins":expected_calibration_error(ly,lp),
                        "training_prevalence_league":round(lg_prev,5) if lg_prev is not None else None,
                        "baseline_majority_accuracy_league":round(lg_baseline_accuracy,5) if lg_baseline_accuracy is not None else None,
                        "baseline_brier_league_prevalence":round(lg_baseline_brier,5) if lg_baseline_brier is not None else None,
                        "brier_skill_vs_league_prevalence":round(1-lg_brier/lg_baseline_brier,5) if lg_brier is not None and lg_baseline_brier is not None and lg_baseline_brier > 0 else None,
                        "production_eligible":"NO","edge_claim":"NOT_APPROVED"})
        # Readiness is keyed by selected-season surrogate, not provider competition ID or league label; names can collide.
        for selected_id, sel in selected_by_id.items():
            for market in MARKETS:
                lg_train = [r for r in train_rows if str(r["competition_id"]) == str(selected_id)
                            and r["kickoff_unix"] < PRIMARY_START and r.get("target_"+market) is not None
                            and all(r.get(k) is not None for k in FEATURES)]
                lg_test = [r for r in train_rows if str(r["competition_id"]) == str(selected_id)
                           and PRIMARY_START <= r["kickoff_unix"] < PRIMARY_END
                           and r.get("target_"+market) is not None and all(r.get(k) is not None for k in FEATURES)]
                gate = "INSUFFICIENT_SAMPLE_MIN_100_TRAIN_AND_TEST" if len(lg_train) < 100 or len(lg_test) < 100 else "SAMPLE_GATE_MET_REQUIRES_STABILITY_AND_ODDS_VALIDATION"
                folds = [x for x in league_walk_forward_metrics if x["selected_id"] == str(selected_id) and x["market"] == market]
                adequate = [x for x in folds if x["train_n"] >= 100 and x["test_n"] >= 100 and x.get("brier_skill_vs_league_prevalence") is not None]
                skills = [x["brier_skill_vs_league_prevalence"] for x in adequate]
                if len(adequate) < len(wf_edges):
                    stability = "INSUFFICIENT_FOLD_SAMPLE_OR_METRIC"
                elif all(v > 0 for v in skills):
                    stability = "POSITIVE_BRIER_SKILL_ALL_FOLDS_DIAGNOSTIC_ONLY"
                elif all(v <= 0 for v in skills):
                    stability = "NO_POSITIVE_BRIER_SKILL_ALL_FOLDS"
                else:
                    stability = "MIXED_BRIER_SKILL_ACROSS_FOLDS"
                league_market_readiness.append({
                    "selected_id":str(selected_id),"selected_id_type":"SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
                        "provider_competition_id":provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[0],
                         "provider_competition_id_status":provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[1],"country":sel.get("country",""),
                    "league":sel.get("competition_name",""),"market":market,
                    "train_n":len(lg_train),"test_n":len(lg_test),"sample_gate":gate,
                    "walk_forward_folds_with_test_data":sum(1 for x in folds if x["test_n"] > 0),
                    "folds_meeting_min_100_train_and_test":len(adequate),
                    "folds_positive_brier_skill_vs_league_prevalence":sum(1 for v in skills if v > 0),
                    "fold_brier_skill_min":round(min(skills),5) if skills else None,
                    "fold_brier_skill_max":round(max(skills),5) if skills else None,
                    "fold_stability_status":stability,
                    "production_eligible":"NO","edge_claim":"NOT_APPROVED"})
        wf_path=OUT/"oracle_selected50_walk_forward_metrics.json"
        wf_path.write_text(json.dumps({"folds":walk_forward,
            "fold_design":"Expanding-window rolling-origin; each fold trains strictly before test interval; fixed features and model; no calibration or tuning.",
            "league_walk_forward_metrics_file":"oracle_selected50_league_walk_forward_metrics.csv",
            "limitations":["This evaluates model probability quality, not betting ROI.",
                           "Historical settlement joins and provider point-in-time provenance remain unverified.",
                           "Per-league minimum samples are necessary but not sufficient for edge approval.",
                           "No production eligibility is granted."]},indent=2)+"\n",encoding="utf-8")
        # Fail the workflow if the diagnostic artifact is malformed or incomplete.
        wf_check = json.loads(wf_path.read_text(encoding="utf-8"))
        expected_fold_rows = len(MARKETS) * len(wf_edges)
        if len(wf_check.get("folds", [])) != expected_fold_rows:
            raise RuntimeError(f"Walk-forward fold count mismatch: expected {expected_fold_rows}, got {len(wf_check.get('folds', []))}")
        if len(league_market_readiness) != len(selected_by_id) * len(MARKETS):
            raise RuntimeError(f"League-market readiness row count mismatch: expected {len(selected_by_id) * len(MARKETS)}, got {len(league_market_readiness)}")
        if len(league_walk_forward_metrics) != len(selected_by_id) * len(MARKETS) * len(wf_edges):
            raise RuntimeError(f"League walk-forward row count mismatch: expected {len(selected_by_id) * len(MARKETS) * len(wf_edges)}, got {len(league_walk_forward_metrics)}")
        if any(r.get("production_eligible") != "NO" or r.get("edge_claim") != "NOT_APPROVED" for r in league_market_readiness):
            raise RuntimeError("Research readiness artifact attempted to grant production eligibility")
        readiness_path=OUT/"oracle_selected50_league_market_readiness.csv"
        with readiness_path.open("w",newline="",encoding="utf-8") as rf:
            cols=["selected_id","selected_id_type","provider_competition_id","provider_competition_id_status","country","league","market","train_n","test_n","sample_gate",
                  "walk_forward_folds_with_test_data","folds_meeting_min_100_train_and_test",
                  "folds_positive_brier_skill_vs_league_prevalence","fold_brier_skill_min","fold_brier_skill_max",
                  "fold_stability_status","production_eligible","edge_claim"]
            rw=csv.DictWriter(rf,fieldnames=cols);rw.writeheader();rw.writerows(league_market_readiness)
        league_walk_forward_path=OUT/"oracle_selected50_league_walk_forward_metrics.csv"
        with league_walk_forward_path.open("w",newline="",encoding="utf-8") as lwf:
            fold_cols=["selected_id","selected_id_type","provider_competition_id","provider_competition_id_status","country","league","market","fold","train_n","test_n","sample_gate","status",
                       "accuracy_at_0_5","accuracy_95ci_low","accuracy_95ci_high","brier","log_loss","auc","ece_10_bins",
                       "training_prevalence_league","baseline_majority_accuracy_league",
                       "baseline_brier_league_prevalence","brier_skill_vs_league_prevalence",
                       "production_eligible","edge_claim"]
            lw=csv.DictWriter(lwf,fieldnames=fold_cols);lw.writeheader();lw.writerows(league_walk_forward_metrics)
        backtest_path=OUT/"oracle_selected50_backtest_metrics.json"
        backtest_report={"primary_window":"2025-03-20 through 2026-09-20","training_cutoff_exclusive":"2025-03-20","markets":backtest, "walk_forward_metrics_file":"oracle_selected50_walk_forward_metrics.json","league_market_readiness_file":"oracle_selected50_league_market_readiness.csv",
                         "note":"Single temporal holdout baseline using the locked Oracle logistic-regression form feature set; raw probabilities, no calibration, not production-approved."}
        backtest_path.write_text(json.dumps(backtest_report,indent=2)+"\n",encoding="utf-8")
        # Calendar-year coverage is derived from each match's source kickoff timestamp.
        # It is deliberately not used to infer provider season-year labels.
        feature_by_match_key = {
            (str(x.get("competition_id") or ""), str(x.get("fixture_id") or ""),
             float(x.get("kickoff_unix") or 0), str(x.get("home_id") or ""), str(x.get("away_id") or "")): x
            for x in feature_rows
        }
        matches_by_comp_year = defaultdict(list)
        observed_years = sorted({dt.datetime.fromtimestamp(r["kickoff_unix"], dt.timezone.utc).year for r in matches})
        if not observed_years:
            raise RuntimeError("Cannot build calendar-year coverage: no source kickoff timestamps were observed.")
        for r in matches:
            year = dt.datetime.fromtimestamp(r["kickoff_unix"], dt.timezone.utc).year
            matches_by_comp_year[(str(r["competition_id"]), year)].append(r)
        calendar_year_rows = []
        for selected_id, sel in sorted(selected_by_id.items(), key=lambda kv: (kv[1].get("country", ""), kv[1].get("competition_name", ""))):
            for year in range(min(observed_years), max(observed_years) + 1):
                year_rows = matches_by_comp_year.get((str(selected_id), year), [])
                completed_rows = [r for r in year_rows if r["finished"] and r["home_goals"] is not None and r["away_goals"] is not None]
                feature_matches = []
                for r in year_rows:
                    key = (str(r["competition_id"]), str(r.get("fixture_id") or ""), float(r["kickoff_unix"]),
                           str(r.get("home_id") or ""), str(r.get("away_id") or ""))
                    feature_matches.append(feature_by_match_key.get(key))
                full_feature_rows = sum(1 for x in feature_matches if x and all(x.get(k) is not None for k in FEATURES))
                primary_rows = [r for r in year_rows if PRIMARY_START <= r["kickoff_unix"] < PRIMARY_END]
                primary_completed = [r for r in primary_rows if r["finished"] and r["home_goals"] is not None and r["away_goals"] is not None]
                status_counts = Counter(str(r.get("status") or "UNKNOWN") for r in year_rows)
                calendar_year_rows.append({
                    "selected_id": str(selected_id), "selected_id_type": "SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
                    "provider_competition_id": provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[0],
                     "provider_competition_id_status": provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))[1], "country": sel.get("country", ""),
                    "competition_name": sel.get("competition_name", ""), "calendar_year_utc": year,
                    "archive_fixture_rows": len(year_rows),
                    "completed_with_numeric_score_rows": len(completed_rows),
                    "completed_rows_with_fixture_id": sum(1 for r in completed_rows if r.get("fixture_id")),
                    "completed_rows_with_both_team_ids": sum(1 for r in completed_rows if r.get("home_id") and r.get("away_id")),
                    "full_20_feature_rows": full_feature_rows,
                    "primary_window_fixture_rows": len(primary_rows),
                    "primary_window_completed_score_rows": len(primary_completed),
                    "primary_window_full_20_feature_rows": sum(1 for r in primary_rows for x in [feature_by_match_key.get((str(r["competition_id"]), str(r.get("fixture_id") or ""), float(r["kickoff_unix"]), str(r.get("home_id") or ""), str(r.get("away_id") or "")))] if x and all(x.get(k) is not None for k in FEATURES)),
                    "source_status_counts_json": json.dumps(dict(sorted(status_counts.items())), ensure_ascii=False, separators=(",", ":")),
                    "coverage_interpretation": "OBSERVED_ARCHIVE_ROWS_ONLY_NOT_PROVIDER_COMPLETENESS_PROOF" if year_rows else "NO_ROWS_OBSERVED_NOT_PROOF_OF_PROVIDER_ABSENCE",
                    "season_year_mapping_status": "NOT_INFERRED_FROM_MATCH_CALENDAR_YEAR",
                    "production_eligible": "NO"
                })
        calendar_year_path = OUT / "oracle_selected50_calendar_year_coverage.csv"
        with calendar_year_path.open("w", newline="", encoding="utf-8") as year_file:
            year_columns = ["selected_id", "selected_id_type", "provider_competition_id", "provider_competition_id_status", "country", "competition_name", "calendar_year_utc",
                            "archive_fixture_rows", "completed_with_numeric_score_rows",
                            "completed_rows_with_fixture_id", "completed_rows_with_both_team_ids",
                            "full_20_feature_rows", "primary_window_fixture_rows",
                            "primary_window_completed_score_rows", "primary_window_full_20_feature_rows",
                            "source_status_counts_json", "coverage_interpretation",
                            "season_year_mapping_status", "production_eligible"]
            year_writer = csv.DictWriter(year_file, fieldnames=year_columns)
            year_writer.writeheader()
            year_writer.writerows(calendar_year_rows)
        expected_calendar_rows = len(selected_by_id) * (max(observed_years) - min(observed_years) + 1)
        if len(calendar_year_rows) != expected_calendar_rows:
            raise RuntimeError(f"Calendar-year coverage row count mismatch: expected {expected_calendar_rows}, got {len(calendar_year_rows)}")
        if any(r["production_eligible"] != "NO" for r in calendar_year_rows):
            raise RuntimeError("Calendar-year coverage attempted to grant production eligibility")
        # Provider season-year matrix: use the source catalogue's season-year label, never kickoff-year inference.
        provider_season_years = sorted({int(r["provider_season_start_year_from_source_label"])
            for r in season_qa if str(r.get("provider_season_start_year_from_source_label", "")).isdigit()})
        if not provider_season_years:
            raise RuntimeError("Provider season-year coverage cannot be built: no source season-year labels parsed.")
        has_unmapped_seasons = any(not str(r.get("provider_season_start_year_from_source_label", "")).isdigit() for r in season_qa)
        provider_season_year_buckets = [str(y) for y in provider_season_years] + (["UNMAPPED"] if has_unmapped_seasons else [])
        matches_by_season = defaultdict(list)
        features_by_season = defaultdict(list)
        for match_row in matches: matches_by_season[str(match_row.get("season_id") or "")].append(match_row)
        for feature_row in feature_rows: features_by_season[str(feature_row.get("season_id") or "")].append(feature_row)
        provider_season_year_rows = []
        for selected_id, sel in sorted(selected_by_id.items(), key=lambda kv: (kv[1].get("country", ""), kv[1].get("competition_name", ""))):
            selected_seasons = [r for r in season_qa if str(r.get("selected_id")) == str(selected_id)]
            for year_bucket in provider_season_year_buckets:
                season_group = [r for r in selected_seasons if
                    (str(r.get("provider_season_start_year_from_source_label", "")) == year_bucket if year_bucket != "UNMAPPED"
                     else not str(r.get("provider_season_start_year_from_source_label", "")).isdigit())]
                season_ids = [str(r.get("season_id") or "") for r in season_group]
                group_matches = [m for sid in season_ids for m in matches_by_season.get(sid, [])]
                group_features = [f for sid in season_ids for f in features_by_season.get(sid, [])]
                group_completed = [m for m in group_matches if m.get("finished") and m.get("home_goals") is not None and m.get("away_goals") is not None]
                group_primary = [m for m in group_matches if PRIMARY_START <= m["kickoff_unix"] < PRIMARY_END]
                group_primary_completed = [m for m in group_primary if m.get("finished") and m.get("home_goals") is not None and m.get("away_goals") is not None]
                parent_id, parent_status = provider_parent_id_by_selected.get(str(selected_id), ("", "UNAVAILABLE_IN_ARCHIVE_MANIFEST"))
                provider_season_year_rows.append({
                    "selected_id":str(selected_id),"selected_id_type":"SELECTED_SEASON_ID_SURROGATE_FOR_COMPETITION_GROUPING",
                    "provider_competition_id":parent_id,"provider_competition_id_status":parent_status,
                    "country":sel.get("country", ""),"competition_name":sel.get("competition_name", ""),
                    "provider_season_start_year":year_bucket,
                    "provider_season_year_source_labels":";".join(sorted({str(r.get("provider_season_year_source", "")) for r in season_group if r.get("provider_season_year_source")})),
                    "source_season_rows":len(season_group),
                    "archive_match_rows_seen":sum(int(r.get("match_count") or 0) for r in season_group),
                    "normalized_match_rows_retained":sum(int(r.get("normalized_match_rows_retained") or 0) for r in season_group),
                    "explicitly_completed_match_rows":len(group_completed),
                    "full_20_feature_rows":sum(1 for r in group_features if all(r.get(k) is not None for k in FEATURES)),
                    "primary_window_match_rows":len(group_primary),
                    "primary_window_completed_match_rows":len(group_primary_completed),
                    "research_markets":";".join(MARKETS),
                    "provider_season_year_mapping_status":"VERIFIED_FROM_PROVIDER_SEASON_YEAR_SOURCE_LABEL" if season_group and year_bucket != "UNMAPPED" else "UNMAPPED_SOURCE_SEASON_YEAR",
                    "outstanding_gates":"Provider parent competition ID unavailable; canonical fixture/team joins unverified; Combo prediction/settlement mismatch; historical standings-as-of and odds/xG provenance unverified",
                    "production_eligible":"NO"
                })
        provider_season_year_path = OUT / "oracle_selected50_provider_season_year_coverage.csv"
        with provider_season_year_path.open("w", newline="", encoding="utf-8") as season_year_file:
            season_year_columns = ["selected_id","selected_id_type","provider_competition_id","provider_competition_id_status","country","competition_name","provider_season_start_year","provider_season_year_source_labels","source_season_rows","archive_match_rows_seen","normalized_match_rows_retained","explicitly_completed_match_rows","full_20_feature_rows","primary_window_match_rows","primary_window_completed_match_rows","research_markets","provider_season_year_mapping_status","outstanding_gates","production_eligible"]
            season_year_writer = csv.DictWriter(season_year_file, fieldnames=season_year_columns)
            season_year_writer.writeheader()
            season_year_writer.writerows(provider_season_year_rows)
        expected_provider_season_year_rows = len(selected_by_id) * len(provider_season_year_buckets)
        if len(provider_season_year_rows) != expected_provider_season_year_rows:
            raise RuntimeError(f"Provider season-year coverage row count mismatch: expected {expected_provider_season_year_rows}, got {len(provider_season_year_rows)}")
        if any(r["production_eligible"] != "NO" for r in provider_season_year_rows):
            raise RuntimeError("Provider season-year coverage attempted to grant production eligibility")
        qa={"status":"RESEARCH_RUNTIME_BUILT","selected_leagues":50,"selected_groups_with_match_rows":len(present_comps),
            "report_horizon_days":7,"minimum_lead_time_minutes":15,
            "future_fixture_competitions_with_predictions":len(set(r["league"] for r in predictions)),
            "future_fixture_candidates_in_report_horizon":len(future),
            "season_rows_seen":len(season_rows),"selected_season_ids":len(selected_by_id),"historical_seasons_mapped_by_exact_labels":mapped_historical_seasons,"historical_seasons_loaded":sum(1 for r in season_qa if r["status"]=="INGESTED"),
            "raw_match_records_retained_after_dedup":len(matches),"completed_match_records":sum(r["finished"] for r in matches),"h2h_history_qa":h2h_history_qa,
            "raw_rows_missing_normalized_fixture_id":sum(int(r.get("rows_missing_normalized_fixture_id") or 0) for r in season_qa),
            "finished_status_missing_numeric_score_rows":sum(int(r.get("rows_explicit_finished_status_missing_numeric_score") or 0) for r in season_qa),
            "completed_total_goals_0_1_rows":sum(int(r.get("completed_total_goals_0_1_rows") or 0) for r in settlement_truth_qa),
            "combo_home_predictor_vs_ledger_disagreement_rows":sum(int(r.get("combo_home_predictor_vs_ledger_disagreement_rows") or 0) for r in settlement_truth_qa),
            "combo_away_predictor_vs_ledger_disagreement_rows":sum(int(r.get("combo_away_predictor_vs_ledger_disagreement_rows") or 0) for r in settlement_truth_qa),
            "future_fixture_candidates":len(future),"feature_rows_with_full_20_features":sum(all(r.get(f) is not None for f in FEATURES) for r in feature_rows),
            "prediction_fixture_count":len(predictions),"prediction_rows":len(predictions)*len(MARKETS),
            "production_model_logic_changed":False,"production_probabilities_changed":False,"production_readiness":"NOT_GRANTED",
            "governed_fixture_report_status":governed_report_qa["status"],"governed_fixture_report_rows":governed_report_qa["fixture_rows"],"governed_combo_home_probabilities_masked":governed_report_qa["raw_combo_home_probabilities_masked"],"governed_combo_away_probabilities_masked":governed_report_qa["raw_combo_away_probabilities_masked"],
            "calendar_year_coverage_rows":len(calendar_year_rows),"league_market_readiness_rows":len(league_market_readiness),"league_walk_forward_metrics_rows":len(league_walk_forward_metrics),"observed_calendar_year_min":min(observed_years),"observed_calendar_year_max":max(observed_years),
            # These three legacy counters are specifically about the private archive catalogue manifest.
            "provider_parent_competition_ids_verified":sum(1 for _, status in provider_parent_id_by_selected.values() if status == "VERIFIED_FROM_PROVIDER_CATALOGUE_MANIFEST"),
            "provider_parent_competition_ids_ambiguous":sum(1 for _, status in provider_parent_id_by_selected.values() if status == "AMBIGUOUS_PROVIDER_PARENT_ID_ACROSS_SEASONS"),
            "provider_parent_competition_ids_unavailable":sum(1 for _, status in provider_parent_id_by_selected.values() if status == "UNAVAILABLE_IN_ARCHIVE_MANIFEST"),
            "provider_competition_id_field_matches_selected_id_in_match_probe":sum(1 for r in parent_probe_rows if str(r.get("provider_competition_id","")).strip()==str(r.get("selected_id","")).strip()),
            "provider_competition_id_match_probe_status":parent_probe_status,
            "provider_competition_id_match_probe_rows":len(parent_probe_rows),
            "provider_competition_id_match_probe_evidence_run":"40382835076" if parent_probe_status=="MATCH_RECORD_COMPETITION_ID_DOCUMENTED_AS_SEASON_ID_50_OF_50_PARENT_ID_NOT_PROVIDED" else "",
            "provider_competition_id_field_semantics_documented_as_season_id":True,
            "provider_competition_id_field_semantics_source":"Official FootyStats API docs define league-matches competition_id as the league season ID; league-list says each season of a competition has a unique ID.",
            "provider_competition_id_field_semantics_source_urls":"https://footystats.org/api/documentations/match-schedule-and-stats;https://footystats.org/api/documentations/league-list",
            "provider_competition_id_parent_semantics_verified":False,
            "provider_match_coverage_matrix_status":provider_match_coverage_status,
            "provider_match_coverage_audit_run":"40391540391",
            "provider_match_coverage_leagues":len(identity_gate_rows),
            "provider_match_coverage_first_page_total_rows":sum(int(r.get("provider_match_coverage_rows_first_page") or 0) for r in identity_gate_rows),
            "provider_match_coverage_unique_fixture_ids_total":sum(int(r.get("provider_match_coverage_unique_fixture_ids_first_page") or 0) for r in identity_gate_rows),
            "provider_match_coverage_duplicate_fixture_id_rows_total":sum(int(r.get("provider_match_coverage_duplicate_fixture_rows_first_page") or 0) for r in identity_gate_rows),
            "provider_match_coverage_truncated_leagues":sum(int(r.get("provider_match_coverage_pager_max_page") or 0)>1 for r in identity_gate_rows),
            "provider_match_coverage_rows_with_status_total":sum(int(r.get("provider_match_coverage_rows_with_status") or 0) for r in identity_gate_rows),
            "provider_match_coverage_rows_with_both_team_ids_total":sum(int(r.get("provider_match_coverage_rows_with_both_team_ids") or 0) for r in identity_gate_rows),
            "provider_match_coverage_rows_with_both_score_fields_total":sum(int(r.get("provider_match_coverage_rows_with_both_score_fields") or 0) for r in identity_gate_rows),
            "provider_match_coverage_rows_with_unix_kickoff_total":sum(int(r.get("provider_match_coverage_rows_with_unix_kickoff") or 0) for r in identity_gate_rows),
            "provider_match_coverage_status_counts_json":json.dumps(dict(sorted(coverage_status_counts.items())), sort_keys=True),
            "provider_match_coverage_groups_matching_selected_id":sum(r.get("provider_match_coverage_competition_id_matches_selected_id")=="YES" for r in identity_gate_rows),
            "provider_explicit_season_id_field_nonempty_rows":sum(int(r.get("provider_match_coverage_nonempty_season_id_field_rows") or 0) for r in identity_gate_rows),
            "provider_sample_fixture_ids_observed":sum(1 for r in parent_probe_rows if str(r.get("provider_match_id","")).strip()),
            "provider_sample_home_away_team_id_pairs_observed":sum(1 for r in parent_probe_rows if str(r.get("home_team_id","")).strip() and str(r.get("away_team_id","")).strip()),
            "provider_sample_complete_status_count":sum(1 for r in parent_probe_rows if str(r.get("provider_match_status","")).strip()=="complete"),
            "provider_sample_incomplete_status_count":sum(1 for r in parent_probe_rows if str(r.get("provider_match_status","")).strip()=="incomplete"),
            "provider_to_canonical_bridges_verified":0,
            "provider_sample_scores_are_settlement_truth":False,
            "provider_season_year_metadata_rows":sum(1 for r in season_qa if r.get("provider_season_year_source")),
            "provider_season_year_coverage_rows":len(provider_season_year_rows),
            "provider_season_start_year_min":min(provider_season_years),
            "provider_season_start_year_max":max(provider_season_years),
            "provider_season_year_buckets":provider_season_year_buckets,
            "limitations":["This is an isolated research/challenger runtime, not the production engine.",
             "Recent form is computed from the last five completed home matches for the home team and away matches for the away team, strictly before kickoff.",
             "Historical validation includes a locked primary temporal holdout and additional expanding-window walk-forward folds; no hyperparameter selection or calibration is applied.",
             "H2H is descriptive only and not a model feature. Current team table positions are display-only snapshots, not historical standings.",
             "xG and odds are not used as model features because their semantic and point-in-time provenance is not verified.",
             "Official FootyStats API docs define the match-record competition_id field as the league season ID and the league-list endpoint documents a unique ID per season. The 50/50 live match-record equality therefore confirms a season-ID relationship, not a parent competition ID or Oracle canonical league/fixture/team join.",
             "The 14,051-row first-page audit measures provider fixture-ID uniqueness and status/field presence only; score fields on incomplete/suspended rows are not settlement truth.",
             "Only explicitly finished matches with numeric scores are used as training truth; unknown status values fail closed."]}
        (OUT/"oracle_selected50_feature_qa.json").write_text(json.dumps(qa,indent=2)+"\n",encoding="utf-8")
        settlement_path = OUT / "oracle_selected50_settlement_truth_qa.csv"
        with settlement_path.open("w", newline="", encoding="utf-8") as settlement_file:
            settlement_columns = ["selected_id","selected_id_type","provider_competition_id","provider_competition_id_status","country","competition_name","source_rows_retained_for_id_time_validation","normalized_rows_after_dedup","duplicate_rows_removed_by_dedup","rows_missing_fixture_id","rows_with_same_home_away_team_id","finished_status_with_numeric_score_rows","finished_status_missing_numeric_score_rows","nonfinished_status_with_numeric_score_rows","noninteger_numeric_score_rows","completed_total_goals_0_1_rows","combo_home_predictor_vs_ledger_disagreement_rows","combo_away_predictor_vs_ledger_disagreement_rows","source_status_counts_json","status_score_cross_tab_json","settlement_truth_status","production_eligible"]
            settlement_writer = csv.DictWriter(settlement_file, fieldnames=settlement_columns)
            settlement_writer.writeheader(); settlement_writer.writerows(settlement_truth_qa)
        with (OUT/"season_coverage.csv").open("w",encoding="utf-8",newline="") as season_file:
            season_columns=["season_id","selected_id","selected_id_type","provider_competition_id","provider_competition_id_status","provider_competition_name_source","provider_season_year_source","provider_season_start_year_from_source_label","country","competition","season_label_source","season_start_source","season_end_source","season_start_year_derived_from_source_date","season_year_mapping_status","status","match_count","team_count","raw_match_rows_seen","normalized_match_rows_retained","rejected_non_object_rows","rejected_missing_kickoff_rows","rejected_missing_home_team_id_rows","rejected_missing_away_team_id_rows","rows_missing_normalized_fixture_id","rows_explicit_finished_status_missing_numeric_score"]
            writer=csv.DictWriter(season_file,fieldnames=season_columns,extrasaction="ignore")
            writer.writeheader()
            writer.writerows(season_qa)
        # Package the derived/private candidate. Never upload the normalized dataset as a public artifact.
        private_zip=Path("oracle-selected50-normalized-research-candidate.zip")
        with zipfile.ZipFile(private_zip,"w",zipfile.ZIP_DEFLATED) as z:
            for p in (normalized_path,feature_path,pred_path,governed_path,governed_qa_path,backtest_path,wf_path,readiness_path,league_walk_forward_path,schedule_path,OUT/"oracle_selected50_feature_qa.json",OUT/"season_coverage.csv",calendar_year_path,provider_season_year_path,settlement_path):
                if p.exists(): z.write(p,p.name)
        digest=hashlib.sha256(private_zip.read_bytes()).hexdigest()
        Path("private-runtime-candidate.sha256").write_text(digest+"  oracle-selected50-normalized-research-candidate.zip\n",encoding="utf-8")
        # Only derived report, backtest and QA summaries go into public Actions artifacts.
        print(json.dumps({**qa,"governed_fixture_report_qa":governed_report_qa,"backtest":backtest,"archive_sha256":hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),"private_candidate_sha256":digest},sort_keys=True))
if __name__=="__main__": main()
