#!/usr/bin/env python3
"""Research-only Selected-50 current-feed identity quarantine; no network/API calls."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CROSSWALK = ROOT / "reports" / "oracle-50-league-provider-canonical-crosswalk-readiness-2026-10-25-r17.csv"
DEFAULT_COLLISIONS = ROOT / "reports" / "oracle-50-league-current-feed-identity-collision-audit-2026-10-25.csv"
DEFAULT_OUT = ROOT / "audit-output"

VERIFIED = {"VERIFIED", "APPROVED", "PASS", "EXACT"}

def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if r and any(str(v or "").strip() for v in r.values())]

def as_int(value):
    try:
        return int(str(value or "0").strip())
    except (TypeError, ValueError):
        raise ValueError(f"Expected integer count, received {value!r}")

def yes(value):
    return str(value or "").strip().upper() in {"YES", "TRUE", "1"}

def classify(row):
    display_rows = as_int(row.get("current_feed_display_label_rows"))
    distinct_ids = as_int(row.get("current_feed_distinct_fotmob_league_ids"))
    country_present = yes(row.get("current_feed_country_field_present"))
    id_allowlist = yes(row.get("current_feed_filter_uses_league_id_allowlist"))
    bridge = str(row.get("exact_provider_season_id_to_fotmob_league_id_bridge") or "").strip().upper()

    blockers = []
    if display_rows == 0:
        blockers.append("NO_MATCHING_CURRENT_FEED_LABEL")
    if distinct_ids > 1:
        blockers.append("AMBIGUOUS_DISPLAY_LABEL_MULTIPLE_FEED_IDS")
    if not country_present:
        blockers.append("COUNTRY_NOT_RETAINED_IN_CURRENT_FEED")
    if not id_allowlist:
        blockers.append("NO_EXACT_LEAGUE_ID_ALLOWLIST")
    if bridge not in VERIFIED:
        blockers.append("PROVIDER_SEASON_TO_FEED_BRIDGE_NOT_VERIFIED")

    if display_rows == 0:
        primary = "NO_MATCHING_CURRENT_FEED_LABEL"
    elif distinct_ids > 1:
        primary = "AMBIGUOUS_DISPLAY_LABEL_MULTIPLE_FEED_IDS"
    elif not country_present:
        primary = "COUNTRY_NOT_RETAINED_IN_CURRENT_FEED"
    elif not id_allowlist:
        primary = "NO_EXACT_LEAGUE_ID_ALLOWLIST"
    elif bridge not in VERIFIED:
        primary = "PROVIDER_SEASON_TO_FEED_BRIDGE_NOT_VERIFIED"
    else:
        primary = "FEED_BRIDGE_CANDIDATE_ONLY_CANONICAL_APPROVAL_REQUIRED"

    return {
        "current_feed_display_label_rows": display_rows,
        "current_feed_distinct_league_id_count": distinct_ids,
        "current_feed_country_field_present": "YES" if country_present else "NO",
        "current_feed_exact_league_id_allowlist": "YES" if id_allowlist else "NO",
        "provider_season_to_feed_bridge_status": str(row.get("exact_provider_season_id_to_fotmob_league_id_bridge") or "UNVERIFIED"),
        "source_collision_status": str(row.get("identity_collision_status") or "UNVERIFIED"),
        "primary_blocker": primary,
        "all_blockers": ";".join(blockers) if blockers else "CANONICAL_APPROVAL_REQUIRED",
        "current_feed_identity_candidate_only": True,
        # This audit does not prove fixture identity, team identity or result truth.
        "canonical_fixture_join_verified": "NO",
        "canonical_team_join_verified": "NO",
        "official_settlement_truth_verified": "NO",
        "production_eligibility": "NOT_GRANTED",
    }

def reconcile(crosswalk_path, collision_path, out_dir):
    crosswalk = read_csv(crosswalk_path)
    collisions = read_csv(collision_path)
    if len(crosswalk) != 50 or len(collisions) != 50:
        raise ValueError(f"Expected 50 crosswalk and collision rows; got {len(crosswalk)} and {len(collisions)}")

    cross_ids = [str(r.get("footystats_provider_id") or "").strip() for r in crosswalk]
    collision_ids = [str(r.get("footystats_selected_season_id") or "").strip() for r in collisions]
    if any(not x for x in cross_ids + collision_ids):
        raise ValueError("Blank selected season ID found")
    if len(set(cross_ids)) != 50 or len(set(collision_ids)) != 50:
        raise ValueError("Selected season IDs must be unique in both source files")
    if set(cross_ids) != set(collision_ids):
        raise ValueError("Crosswalk and current-feed collision ID sets do not match")

    by_id = {str(r["footystats_selected_season_id"]).strip(): r for r in collisions}
    out_rows = []
    for source in crosswalk:
        sid = str(source["footystats_provider_id"]).strip()
        row = by_id[sid]
        status = classify(row)
        out_rows.append({
            "selected_season_id": sid,
            "country": str(source.get("country") or ""),
            "provider_competition_name": str(source.get("provider_competition_name") or ""),
            "canonical_code_candidate": str(source.get("canonical_code_candidate") or ""),
            "source_crosswalk_status": str(source.get("crosswalk_status") or "UNVERIFIED"),
            **status,
        })

    counts = Counter(r["primary_blocker"] for r in out_rows)
    summary = {
        "status": "SELECTED50_CURRENT_FEED_IDENTITY_QUARANTINE_COMPLETE",
        "selected_groups": len(out_rows),
        "unique_selected_season_ids": len({r["selected_season_id"] for r in out_rows}),
        "groups_with_current_feed_label_rows": sum(r["current_feed_display_label_rows"] > 0 for r in out_rows),
        "groups_with_multiple_feed_league_ids": sum(r["current_feed_distinct_league_id_count"] > 1 for r in out_rows),
        "groups_with_country_field": sum(r["current_feed_country_field_present"] == "YES" for r in out_rows),
        "groups_using_exact_league_id_allowlist": sum(r["current_feed_exact_league_id_allowlist"] == "YES" for r in out_rows),
        "groups_with_verified_provider_season_to_feed_bridge": sum(r["provider_season_to_feed_bridge_status"].strip().upper() in VERIFIED for r in out_rows),
        "crosswalk_candidate_rows": sum("CANDIDATE" in r["source_crosswalk_status"].upper() for r in out_rows),
        "crosswalk_unresolved_rows": sum("UNRESOLVED" in r["source_crosswalk_status"].upper() for r in out_rows),
        "crosswalk_approved_rows": sum(r["source_crosswalk_status"].strip().upper() in {"APPROVED", "APPROVED_MAPPING", "VERIFIED"} for r in out_rows),
        "primary_blocker_counts": dict(sorted(counts.items())),
        "canonical_fixture_join_verified_rows": 0,
        "canonical_team_join_verified_rows": 0,
        "official_settlement_truth_verified_rows": 0,
        "production_eligible_rows": 0,
        "network_calls_made": 0,
        "paid_provider_calls_made": 0,
        "raw_feed_examples_exported": False,
        "interpretation": "This is a fail-closed identity-risk diagnostic. Display-label agreement or a single feed league ID is not a canonical fixture/team join. No mapping is approved by this report.",
    }

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    csv_path = out / "selected50_current_feed_identity_quarantine.csv"
    json_path = out / "selected50_current_feed_identity_quarantine_summary.json"
    md_path = out / "selected50_current_feed_identity_quarantine.md"
    fields = list(out_rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Selected-50 Current-Feed Identity Quarantine",
        "",
        "**Status:** Research-only; production eligibility NOT GRANTED.",
        "",
        f"- Selected groups: {summary['selected_groups']}",
        f"- Groups with current-feed label rows: {summary['groups_with_current_feed_label_rows']}",
        f"- Groups with multiple feed league IDs under a display label: {summary['groups_with_multiple_feed_league_ids']}",
        f"- Country field retained: {summary['groups_with_country_field']}/50",
        f"- Exact league-ID allowlist used: {summary['groups_using_exact_league_id_allowlist']}/50",
        f"- Verified provider-season-to-feed bridges: {summary['groups_with_verified_provider_season_to_feed_bridge']}/50",
        f"- Canonical fixture/team joins verified: 0/50",
        f"- Official settlement truth verified: 0/50",
        "",
        "## Primary blockers",
        "",
    ]
    lines.extend(f"- {name}: {count}" for name, count in sorted(counts.items()))
    lines += [
        "",
        "## Governance",
        "",
        "No feed examples or raw provider payloads are exported. No network/provider calls are made. All rows remain NOT_GRANTED. This diagnostic does not change canonical mappings, production logic, probabilities, calibration, thresholds or the frozen 27-league baseline.",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return summary

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crosswalk", default=str(DEFAULT_CROSSWALK))
    ap.add_argument("--collision-audit", default=str(DEFAULT_COLLISIONS))
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    args = ap.parse_args()
    print(json.dumps(reconcile(args.crosswalk, args.collision_audit, args.out_dir), sort_keys=True))

if __name__ == "__main__":
    main()
