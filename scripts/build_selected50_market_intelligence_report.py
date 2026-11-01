#!/usr/bin/env python3
"""Build the Selected-50 research-only Market Intelligence workbook.

No prediction model is run here. The three supported raw Oracle probabilities are
copied from the runtime CSV without recalculation. Every archive join is exact and
fail-closed on missing or duplicate composite identities.
"""
from __future__ import annotations

import argparse
import csv
import json
import hashlib
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from bisect import bisect_left
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

HEADERS = [
    "Fixture Date", "League", "Fixture", "BTTS Yes", "Home 1X", "Away X2",
    "Over 1.5", "Over 2.5", "Under 4.5", "Home over 1.5 goals",
    "Away over 1.5 goals", "Home 1X + Over 1.5", "Away X2 + Over 1.5",
    "Home 1X + Under 4.5", "Away X2 + Under 4.5", "M-1UP Home",
    "M-1UP Away", "Draw Probability (derived)", "Goal Line Call (O/U 2.5)",
    "Most Likely Total-Goals Band (derived)", "Recent Form (5)",
    "Recent Form Points (Last 5)", "League Position",
    "Avg. Goals Scored (Last 5)", "Avg. Goals Conceded (Last 5)",
    "Avg. Points (Last 5)", "Attacking Index", "Defensive Index",
    "TOTAL Index", "H2H Last 5 Summary", "H2H Avg Total Goals",
    "Historical Accuracy Status", "Home Evidence Risk", "Away Evidence Risk",
    "Home Risk Rationale", "Away Risk Rationale", "A+ Setup Status",
    "Gem's Independent Match Analysis",
]
SUPPORTED = {
    "BTTS Yes": "BTTS_probability_pct",
    "Home 1X": "DC_HOME_probability_pct",
    "Away X2": "DC_AWAY_probability_pct",
}
UNAVAILABLE = "NOT_AVAILABLE_FROM_ORACLE_OUTPUT"
SETTLED = {"complete", "completed", "finished", "ft", "full time", "full_time",
           "played", "after extra time", "aet", "penalties"}


def read_csv(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def parse_dt(value):
    try:
        d = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def valid_score(row):
    try:
        h, a = float(row.get("home_goals", "")), float(row.get("away_goals", ""))
        return (math.isfinite(h) and math.isfinite(a) and h >= 0 and a >= 0
                and h.is_integer() and a.is_integer())
    except (TypeError, ValueError, OverflowError):
        return False


def h2h_average_total_goals(trace_row):
    """Mean goals across exact, strictly pre-cutoff H2H meetings already in trace."""
    try:
        meetings = json.loads(trace_row.get("h2h_meetings_detail") or "[]")
    except (TypeError, ValueError):
        meetings = []
    totals = []
    for meeting in meetings:
        try:
            total = float(meeting.get("home_goals")) + float(meeting.get("away_goals"))
            if math.isfinite(total) and total >= 0:
                totals.append(total)
        except (TypeError, ValueError, OverflowError):
            continue
    return round(sum(totals) / len(totals), 2) if totals else "NO_VERIFIED_PRIOR_H2H"

def archive_key(row):
    return (
        str(row.get("provider_season_id") or "").strip(),
        str(row.get("fixture_id") or "").strip(),
        str(row.get("home_team_id") or "").strip(),
        str(row.get("away_team_id") or "").strip(),
    )


def runtime_key(row):
    return (
        str(row.get("provider_season_id") or "").strip(),
        str(row.get("fixture_id") or "").strip(),
        str(row.get("home_team_provider_id") or "").strip(),
        str(row.get("away_team_provider_id") or "").strip(),
    )


def build_indexes(matches):
    """Create strictly chronological archive indexes from exact provider identities."""
    by_team = defaultdict(list)
    by_season = defaultdict(list)
    by_pair = defaultdict(list)
    seen = set()
    duplicates = 0
    for row in matches:
        dt = parse_dt(row.get("kickoff_utc"))
        if not dt or not row.get("home_team_id") or not row.get("away_team_id"):
            continue
        season_id = str(row.get("provider_season_id") or "").strip()
        league = season_id
        season = season_id
        # Cross-season H2H requires a stable provider competition ID; otherwise use exact season only.
        competition = str(row.get("provider_league_id") or "").strip() or season_id
        h, a = str(row["home_team_id"]), str(row["away_team_id"])
        if not league or not season or h == a:
            continue
        identity = (str(row.get("provider_season_id") or ""), str(row.get("fixture_id") or ""), h, a)
        if all(identity) and identity in seen:
            duplicates += 1
        elif all(identity):
            seen.add(identity)
        item = dict(row)
        item["_dt"] = dt
        item["_league"] = league
        item["_season"] = season
        item["_competition"] = competition
        item["_home"] = h
        item["_away"] = a
        by_team[(competition, h)].append(item)
        by_team[(competition, a)].append(item)
        by_season[(league, season)].append(item)
        by_pair[(competition, tuple(sorted((h, a))))].append(item)
    for index in (by_team, by_season, by_pair):
        for key in index:
            index[key].sort(key=lambda x: (x["_dt"], str(x.get("fixture_id") or "")))
    return by_team, by_season, by_pair, duplicates


def before(rows, cutoff):
    times = [r["_dt"] for r in rows]
    return rows[:bisect_left(times, cutoff)]


def team_form(rows, team_id, venue=None):
    """Latest-five completed form; venue optionally restricts the team's match role."""
    usable = [r for r in rows if str(r.get("status_raw") or "").lower() in SETTLED
              and valid_score(r)
              and (venue is None or
                   (venue == "home" and str(r.get("home_team_id")) == team_id) or
                   (venue == "away" and str(r.get("away_team_id")) == team_id))]
    sample = usable[-5:]
    results, gf, ga, pts = [], [], [], []
    for r in sample:
        home = str(r.get("home_team_id")) == team_id
        own = int(float(r["home_goals"] if home else r["away_goals"]))
        opp = int(float(r["away_goals"] if home else r["home_goals"]))
        gf.append(own); ga.append(opp)
        points = 3 if own > opp else 1 if own == opp else 0
        pts.append(points)
        results.append("W" if points == 3 else "D" if points == 1 else "L")
    n = len(sample)
    btts = [int(int(float(r["home_goals"])) > 0 and int(float(r["away_goals"])) > 0) for r in sample]
    over15 = [int(int(float(r["home_goals"])) + int(float(r["away_goals"])) > 1) for r in sample]
    over25 = [int(int(float(r["home_goals"])) + int(float(r["away_goals"])) > 2) for r in sample]
    under45 = [int(int(float(r["home_goals"])) + int(float(r["away_goals"])) < 5) for r in sample]
    team_over15 = [int(x > 1) for x in gf]
    clean_sheet = [int(x == 0) for x in ga]
    failed_to_score = [int(x == 0) for x in gf]
    rate = lambda values: round(sum(values) / n, 4) if n else None
    return {
        "n": n, "form": "".join(results),
        "gf": sum(gf) / n if n else None,
        "ga": sum(ga) / n if n else None,
        "ppg": sum(pts) / n if n else None,
        "points": sum(pts) if n else None,
        "btts_rate": rate(btts), "over15_rate": rate(over15),
        "over25_rate": rate(over25), "under45_rate": rate(under45),
        "team_over15_rate": rate(team_over15), "clean_sheet_rate": rate(clean_sheet),
        "failed_to_score_rate": rate(failed_to_score),
        "sample": sample,
    }


def league_table(rows, cutoff):
    stats = {}
    for r in rows:
        if r["_dt"] >= cutoff:
            break
        if str(r.get("status_raw") or "").lower() not in SETTLED or not valid_score(r):
            continue
        h, a = str(r["_home"]), str(r["_away"])
        hg, ag = int(float(r["home_goals"])), int(float(r["away_goals"]))
        for tid, gf, ga in ((h, hg, ag), (a, ag, hg)):
            team_name = str((r.get("home_team") if tid == h else r.get("away_team")) or "").strip()
            s = stats.setdefault(tid, {"played": 0, "points": 0, "gf": 0, "ga": 0, "team_name": team_name})
            if team_name and not s.get("team_name"):
                s["team_name"] = team_name
            s["played"] += 1; s["gf"] += gf; s["ga"] += ga
            s["points"] += 3 if gf > ga else 1 if gf == ga else 0
    ordered = sorted(stats.items(), key=lambda kv: (
        -kv[1]["points"], -(kv[1]["gf"] - kv[1]["ga"]), -kv[1]["gf"],
        str(kv[1].get("team_name") or "").casefold(), kv[0]
    ))
    return {tid: {"position": i + 1, **s} for i, (tid, s) in enumerate(ordered)}


def pct(value):
    if value in (None, ""):
        return ""
    return round(float(value), 2)


def index_value(team_gf, team_ga, league_goals_per_team):
    if team_gf is None or team_ga is None or league_goals_per_team is None:
        return None, None
    attack = min(100.0, max(0.0, 50.0 * team_gf / league_goals_per_team))
    defence = None if team_ga == 0 else min(100.0, max(0.0, 50.0 * league_goals_per_team / team_ga))
    return attack, defence


def exact_join(runtime_rows, archive_rows):
    index = defaultdict(list)
    for row in archive_rows:
        key = archive_key(row)
        if all(key):
            index[key].append(row)
    duplicates = {k: len(v) for k, v in index.items() if len(v) != 1}
    joined, missing = {}, []
    for row in runtime_rows:
        key = runtime_key(row)
        if not all(key):
            missing.append((row, "MISSING_COMPOSITE_IDENTITY"))
        elif len(index.get(key, [])) != 1:
            missing.append((row, "NO_EXACT_ARCHIVE_MATCH" if not index.get(key) else "DUPLICATE_ARCHIVE_MATCH"))
        else:
            archive_row = index[key][0]
            runtime_kickoff = parse_dt(row.get("date_utc"))
            archive_kickoff = parse_dt(archive_row.get("kickoff_utc"))
            if runtime_kickoff is None or archive_kickoff is None:
                missing.append((row, "KICKOFF_UNPARSEABLE", archive_row))
            else:
                # Fixture identity is exact. A schedule discrepancy is a separate QA condition:
                # use runtime kickoff as the pre-match cutoff, retain the archived time as evidence,
                # and exclude this target fixture from every historical feature pool.
                joined[key] = archive_row
                if runtime_kickoff != archive_kickoff:
                    missing.append((row, "SCHEDULE_KICKOFF_MISMATCH", archive_row))
    return joined, missing, duplicates


def build_report(runtime_rows, archive_rows):
    joined, missing, duplicate_archive_keys = exact_join(runtime_rows, archive_rows)
    schedule_conflict_keys = {
        archive_key(archive_row)
        for row, reason, *extras in missing
        if reason == "SCHEDULE_KICKOFF_MISMATCH"
        for archive_row in extras[:1]
    }
    # Never let schedule-discordant target records contribute to any fixture's historical
    # form, table, scoring baseline or H2H until their event time is reconciled.
    history_archive_rows = [
        row for row in archive_rows
        if archive_key(row) not in schedule_conflict_keys
    ]
    by_team, by_season, by_pair, history_duplicates = build_indexes(history_archive_rows)
    output, trace = [], []
    leagues = set()
    seen_runtime = set()
    for runtime in runtime_rows:
        key = runtime_key(runtime)
        selected = str(runtime.get("selected_id") or "").strip()
        league_name = str(runtime.get("league") or runtime.get("provider_competition_name_source") or "")
        fixture_text = f"{runtime.get('home_team','')} vs {runtime.get('away_team','')}"
        leagues.add(selected)
        if key in seen_runtime:
            raise ValueError(f"Duplicate runtime exact key: {key}")
        seen_runtime.add(key)
        target = joined.get(key)
        cutoff = parse_dt(runtime.get("date_utc"))
        schedule_entry = next((entry for entry in missing
                               if entry[0] is runtime and entry[1] == "SCHEDULE_KICKOFF_MISMATCH"), None)
        if target is None or cutoff is None:
            failure_entry = next((entry for entry in missing if entry[0] is runtime), None)
            reason = failure_entry[1] if failure_entry else "MISSING_ARCHIVE_JOIN_OR_KICKOFF"
            archive_match = failure_entry[2] if failure_entry and len(failure_entry) > 2 else {}
            outrow = base_row(runtime, league_name, reason)
            output.append(outrow)
            trace.append({"fixture_id": runtime.get("fixture_id", ""), "selected_id": selected,
                          "join_status": reason, "home_form_n": 0, "away_form_n": 0,
                          "home_table_status": "UNAVAILABLE", "away_table_status": "UNAVAILABLE",
                          "fixture_date": runtime.get("date_utc", ""),
                          "runtime_league": league_name, "runtime_fixture": fixture_text,
                          "fixture_identity": "|".join(key) if all(key) else "",
                          "runtime_provider_season_id": runtime.get("provider_season_id", ""),
                          "runtime_home_team_id": runtime.get("home_team_provider_id", ""),
                          "runtime_away_team_id": runtime.get("away_team_provider_id", ""),
                          "runtime_kickoff_utc": runtime.get("date_utc", ""),
                          "archive_kickoff_utc": archive_match.get("kickoff_utc", ""),
                          "schedule_reconciliation_status": "NOT_EVALUATED",
                          "schedule_reconciliation_reason": reason,
                          "schedule_delta_minutes_archive_minus_runtime": "",
                          "archive_source_file": archive_match.get("source_file", ""),
                          "archive_source_row": archive_match.get("source_row", ""),
                          "runtime_home_team": runtime.get("home_team", ""),
                          "runtime_away_team": runtime.get("away_team", ""),
                          "history_cutoff_utc": runtime.get("date_utc", ""), "production_eligible": "NO", "betting_eligible": "NO"})
            continue
        league = key[0]
        season = key[0]
        home, away = key[2], key[3]
        competition_id = str(target.get("provider_league_id") or "").strip() or season
        home_rows = before(by_team[(competition_id, home)], cutoff)
        away_rows = before(by_team[(competition_id, away)], cutoff)
        hf, af = team_form(home_rows, home), team_form(away_rows, away)
        home_venue_form = team_form(home_rows, home, venue="home")
        away_venue_form = team_form(away_rows, away, venue="away")
        table = league_table(by_season[(league, season)], cutoff)
        hpos, apos = table.get(home, {}).get("position"), table.get(away, {}).get("position")
        league_completed = [r for r in before(by_season[(league, season)], cutoff)
                            if str(r.get("status_raw") or "").lower() in SETTLED and valid_score(r)]
        total_goals = sum(int(float(r["home_goals"])) + int(float(r["away_goals"])) for r in league_completed)
        league_goals_per_team = (total_goals / (2 * len(league_completed))) if league_completed else None
        h_attack, h_defence = index_value(hf["gf"] if hf["n"] >= 3 else None,
                                           hf["ga"] if hf["n"] >= 3 else None, league_goals_per_team)
        a_attack, a_defence = index_value(af["gf"] if af["n"] >= 3 else None,
                                           af["ga"] if af["n"] >= 3 else None, league_goals_per_team)
        h2h_scope = competition_id
        pair_rows = before(by_pair[(h2h_scope, tuple(sorted((home, away))))], cutoff)
        h2h = [r for r in pair_rows if str(r.get("status_raw") or "").lower() in SETTLED and valid_score(r)][-5:]
        h2h_results = []
        for r in h2h:
            home_was_home = str(r.get("home_team_id")) == home
            own = int(float(r["home_goals"] if home_was_home else r["away_goals"]))
            opp = int(float(r["away_goals"] if home_was_home else r["home_goals"]))
            h2h_results.append("W" if own > opp else "D" if own == opp else "L")
        h2h_avg = (sum(int(float(r["home_goals"])) + int(float(r["away_goals"])) for r in h2h) / len(h2h)) if h2h else None
        h_risk, h_reasons = evidence_risk(hf["n"], hpos is not None, len(h2h), all(key))
        a_risk, a_reasons = evidence_risk(af["n"], apos is not None, len(h2h), all(key))
        h_attack_text, h_def_text = fmt(h_attack), fmt(h_defence)
        a_attack_text, a_def_text = fmt(a_attack), fmt(a_defence)
        h_total = h_attack + h_defence if h_attack is not None and h_defence is not None else None
        a_total = a_attack + a_defence if a_attack is not None and a_defence is not None else None
        def pairfmt(x, y):
            return f"Home {fmt(x)} | Away {fmt(y)}" if x is not None or y is not None else "INSUFFICIENT_DATA"
        form_text = f"Home {hf['form'] or 'INSUFFICIENT'} | Away {af['form'] or 'INSUFFICIENT'}"
        points_text = (f"Home {hf['points']}/{hf['n'] * 3} (n={hf['n']})" if hf["points"] is not None else "Home N/A") + " | " + (f"Away {af['points']}/{af['n'] * 3} (n={af['n']})" if af["points"] is not None else "Away N/A")
        position_text = f"Home {hpos if hpos else 'N/A'} | Away {apos if apos else 'N/A'} (PROVISIONAL)"
        avg_gf = pairfmt(hf["gf"] if hf["n"] >= 3 else None, af["gf"] if af["n"] >= 3 else None)
        avg_ga = pairfmt(hf["ga"] if hf["n"] >= 3 else None, af["ga"] if af["n"] >= 3 else None)
        avg_pts = pairfmt(hf["ppg"] if hf["n"] >= 3 else None, af["ppg"] if af["n"] >= 3 else None)
        attack_text = pairfmt(h_attack, a_attack)
        defence_text = pairfmt(h_defence, a_defence)
        total_text = pairfmt(h_total, a_total)
        h2h_text = "".join(h2h_results) if h2h_results else "NO_VERIFIED_PRIOR_H2H"
        analysis = independent_analysis(hf, af, h_attack, a_attack, h_defence, a_defence)
        row = base_row(runtime, league_name, "EXACT_ARCHIVE_JOIN")
        row.update({
            "Recent Form (5)": form_text,
            "Recent Form Points (Last 5)": points_text,
            "League Position": position_text,
            "Avg. Goals Scored (Last 5)": avg_gf,
            "Avg. Goals Conceded (Last 5)": avg_ga,
            "Avg. Points (Last 5)": avg_pts,
            "Attacking Index": attack_text,
            "Defensive Index": defence_text,
            "TOTAL Index": total_text,
            "H2H Last 5 Summary": h2h_text,
            "H2H Avg Total Goals": fmt(h2h_avg),
            "Historical Accuracy Status": "NOT_VALIDATED_NO_EXACT_PREMATCH_LEDGER_AND_OFFICIAL_SETTLEMENT_JOIN",
            "Home Evidence Risk": f"{h_risk:.1f}%",
            "Away Evidence Risk": f"{a_risk:.1f}%",
            "Home Risk Rationale": h_reasons,
            "Away Risk Rationale": a_reasons,
            "A+ Setup Status": "NOT_GRADED_CALIBRATION_SETTLEMENT_AND_ODDS_GATES_NOT_PASSED",
            "Gem's Independent Match Analysis": analysis,
        })
        output.append(row)
        trace.append({
            "fixture_id": runtime.get("fixture_id", ""), "selected_id": selected,
            "join_status": "PASS_EXACT_SEASON_FIXTURE_ORDERED_TEAM_IDS",
            "fixture_date": runtime.get("date_utc", ""),
            "runtime_league": league_name, "runtime_fixture": fixture_text,
            "fixture_identity": "|".join(key) if all(key) else "",
            "runtime_provider_season_id": runtime.get("provider_season_id", ""),
            "runtime_home_team_id": runtime.get("home_team_provider_id", ""),
            "runtime_away_team_id": runtime.get("away_team_provider_id", ""),
            "schedule_reconciliation_status": "REVIEW_REQUIRED" if schedule_entry else "MATCH",
            "schedule_reconciliation_reason": "KICKOFF_MISMATCH" if schedule_entry else "",
            "runtime_kickoff_utc": runtime.get("date_utc", ""),
            "runtime_home_team": runtime.get("home_team", ""),
            "runtime_away_team": runtime.get("away_team", ""),
            "archive_kickoff_utc": target.get("kickoff_utc", ""),
            "schedule_delta_minutes_archive_minus_runtime": (
                int((parse_dt(target.get("kickoff_utc")) - cutoff).total_seconds() / 60)
                if schedule_entry and parse_dt(target.get("kickoff_utc")) and cutoff else ""
            ),
            "schedule_discordance_minutes": (
                int((parse_dt(target.get("kickoff_utc")) - cutoff).total_seconds() / 60)
                if schedule_entry and parse_dt(target.get("kickoff_utc")) and cutoff else ""
            ),
            "home_form_n": hf["n"], "away_form_n": af["n"], "h2h_n": len(h2h),
            "home_form": hf["form"], "away_form": af["form"],
            "home_form_gf_avg": fmt(hf["gf"]), "home_form_ga_avg": fmt(hf["ga"]),
            "home_form_ppg": fmt(hf["ppg"]), "away_form_gf_avg": fmt(af["gf"]),
            "away_form_ga_avg": fmt(af["ga"]), "away_form_ppg": fmt(af["ppg"]),
            "home_form_btts_rate": fmt(hf["btts_rate"] * 100 if hf["btts_rate"] is not None else None), "away_form_btts_rate": fmt(af["btts_rate"] * 100 if af["btts_rate"] is not None else None),
            "home_form_over15_rate": fmt(hf["over15_rate"] * 100 if hf["over15_rate"] is not None else None), "away_form_over15_rate": fmt(af["over15_rate"] * 100 if af["over15_rate"] is not None else None),
            "home_form_over25_rate": fmt(hf["over25_rate"] * 100 if hf["over25_rate"] is not None else None), "away_form_over25_rate": fmt(af["over25_rate"] * 100 if af["over25_rate"] is not None else None),
            "home_form_under45_rate": fmt(hf["under45_rate"] * 100 if hf["under45_rate"] is not None else None), "away_form_under45_rate": fmt(af["under45_rate"] * 100 if af["under45_rate"] is not None else None),
            "home_team_over15_rate": fmt(hf["team_over15_rate"] * 100 if hf["team_over15_rate"] is not None else None), "away_team_over15_rate": fmt(af["team_over15_rate"] * 100 if af["team_over15_rate"] is not None else None),
            "home_clean_sheet_rate": fmt(hf["clean_sheet_rate"] * 100 if hf["clean_sheet_rate"] is not None else None), "away_clean_sheet_rate": fmt(af["clean_sheet_rate"] * 100 if af["clean_sheet_rate"] is not None else None),
            "home_failed_to_score_rate": fmt(hf["failed_to_score_rate"] * 100 if hf["failed_to_score_rate"] is not None else None), "away_failed_to_score_rate": fmt(af["failed_to_score_rate"] * 100 if af["failed_to_score_rate"] is not None else None),
            "home_form_source_fixture_ids": ";".join(str(r.get("fixture_id") or "") for r in hf["sample"]),
            "away_form_source_fixture_ids": ";".join(str(r.get("fixture_id") or "") for r in af["sample"]),
            "home_at_home_form_n": home_venue_form["n"],
            "home_at_home_form": home_venue_form["form"],
            "home_at_home_avg_goals_for": fmt(home_venue_form["gf"]) if home_venue_form["n"] >= 3 else "INSUFFICIENT_DATA",
            "home_at_home_avg_goals_against": fmt(home_venue_form["ga"]) if home_venue_form["n"] >= 3 else "INSUFFICIENT_DATA",
            "home_at_home_avg_points": fmt(home_venue_form["ppg"]) if home_venue_form["n"] >= 3 else "INSUFFICIENT_DATA",
            "home_at_home_source_fixture_ids": ";".join(str(r.get("fixture_id") or "") for r in home_venue_form["sample"]),
            "away_away_form_n": away_venue_form["n"],
            "away_away_form": away_venue_form["form"],
            "away_away_avg_goals_for": fmt(away_venue_form["gf"]) if away_venue_form["n"] >= 3 else "INSUFFICIENT_DATA",
            "away_away_avg_goals_against": fmt(away_venue_form["ga"]) if away_venue_form["n"] >= 3 else "INSUFFICIENT_DATA",
            "away_away_avg_points": fmt(away_venue_form["ppg"]) if away_venue_form["n"] >= 3 else "INSUFFICIENT_DATA",
            "away_away_source_fixture_ids": ";".join(str(r.get("fixture_id") or "") for r in away_venue_form["sample"]),
            "home_league_position": hpos or "", "away_league_position": apos or "",
            "league_table_status": "PROVISIONAL_CONVENTIONAL_TABLE" if hpos and apos else "TABLE_POSITION_INSUFFICIENT_OR_UNAVAILABLE",
            "history_cutoff_utc": cutoff.isoformat(),
            "history_cutoff_rule": "STRICTLY_BEFORE_FIXTURE_KICKOFF",
            "home_risk_pct": h_risk, "away_risk_pct": a_risk,
            "archive_provider_season_id": key[0], "archive_provider_season_id_source": target.get("provider_season_id_source", "ARCHIVE_SEASON_FOLDER_ID"),
            "archive_provider_competition_id": target.get("provider_league_id", ""),
            "h2h_scope": "EXPLICIT_PROVIDER_COMPETITION_ID_SCOPE" if competition_id else "EXACT_SEASON_FALLBACK",
            "h2h_meetings_detail": json.dumps([{
                "fixture_id": r.get("fixture_id", ""), "kickoff_utc": r.get("kickoff_utc", ""),
                "provider_season_id": r.get("provider_season_id", ""),
                "home_team_id": r.get("home_team_id", ""), "away_team_id": r.get("away_team_id", ""),
                "home_goals": r.get("home_goals", ""), "away_goals": r.get("away_goals", ""),
                "result_current_home_perspective": h2h_results[i],
                "total_goals": int(float(r["home_goals"])) + int(float(r["away_goals"]))
            } for i, r in enumerate(h2h)], ensure_ascii=False),
            "archive_fixture_id": key[1], "archive_home_team_id": key[2], "archive_away_team_id": key[3],
            "archive_source_file": target.get("source_file", ""), "archive_source_row": target.get("source_row", ""),
            "archive_raw_record_sha256": target.get("raw_record_sha256", ""),
            "home_form_source_fixture_ids": ";".join(str(r.get("fixture_id") or "") for r in hf["sample"]),
            "away_form_source_fixture_ids": ";".join(str(r.get("fixture_id") or "") for r in af["sample"]),
            "h2h_source_fixture_ids": ";".join(str(r.get("fixture_id") or "") for r in h2h),
            "home_table_sample_n": len([r for r in league_completed if home in (str(r.get("home_team_id")), str(r.get("away_team_id")))]),
            "away_table_sample_n": len([r for r in league_completed if away in (str(r.get("home_team_id")), str(r.get("away_team_id")))]),
            "league_baseline_match_n": len(league_completed),
            "production_eligible": "NO", "betting_eligible": "NO",
        })
    if len(output) != len(runtime_rows):
        raise AssertionError("Output row count does not reconcile to runtime fixture rows")
    return output, trace, {
        "runtime_rows": len(runtime_rows), "report_rows": len(output),
        "exact_archive_joins": sum(r.get("join_status") == "PASS_EXACT_SEASON_FIXTURE_ORDERED_TEAM_IDS" for r in trace),
        "unmatched_or_quarantined_rows": sum(r.get("join_status") != "PASS_EXACT_SEASON_FIXTURE_ORDERED_TEAM_IDS" for r in trace),
        "selected_league_groups": len(leagues), "selected_ids": sorted(leagues),
        "duplicate_archive_composite_keys": len(duplicate_archive_keys),
        "duplicate_archive_history_rows": history_duplicates,
        "duplicate_runtime_keys": len(runtime_rows) - len(seen_runtime),
        "schedule_discordance_rows": len(schedule_conflict_keys),
        "schedule_discordance_fixture_keys": [list(k) for k in sorted(schedule_conflict_keys)],
        "schedule_reconciliation_gate": "REVIEW_REQUIRED" if schedule_conflict_keys else "PASS",
        "schedule_reconciliation_queue": build_schedule_reconciliation_queue(trace),
        "schedule_reconciliation_queue_rows": len(build_schedule_reconciliation_queue(trace)),
        "join_failure_reason_counts": {reason: sum(1 for entry in missing if entry[1] == reason) for reason in sorted({entry[1] for entry in missing})},
        "join_failure_examples": [
            {"reason": reason,
             "status": "REVIEW_REQUIRED" if reason == "SCHEDULE_KICKOFF_MISMATCH" else "BLOCKED",
             "schedule_reconciliation_status": "REVIEW_REQUIRED" if reason == "SCHEDULE_KICKOFF_MISMATCH" else "NOT_APPLICABLE",
             "runtime_key": list(runtime_key(row)),
             "fixture_identity": "|".join(runtime_key(row)) if all(runtime_key(row)) else "",
             "fixture_date": row.get("date_utc", ""),
             "league": row.get("league") or row.get("provider_competition_name_source") or "",
             "fixture": f"{row.get('home_team','')} vs {row.get('away_team','')}",
             "runtime_kickoff_utc": row.get("date_utc", ""),
             "archive_kickoff_utc": archive_row.get("kickoff_utc", "") if len(entry) > 2 else "",
             "delta_minutes_archive_minus_runtime": (
                 int((parse_dt(archive_row.get("kickoff_utc")) - parse_dt(row.get("date_utc"))).total_seconds() / 60)
                 if len(entry) > 2 and parse_dt(archive_row.get("kickoff_utc")) and parse_dt(row.get("date_utc")) else ""
             ),
             "archive_source_file": archive_row.get("source_file", "") if len(entry) > 2 else "",
             "archive_source_row": archive_row.get("source_row", "") if len(entry) > 2 else "",
             "home_team": row.get("home_team", ""), "away_team": row.get("away_team", "")}
            for entry in missing[:25]
            for row, reason, *extras in [entry]
            for archive_row in [extras[0] if extras else {}]
        ],
    }


def build_schedule_reconciliation_queue(trace_rows):
    """Return explicit manual-review records for schedule conflicts; never correct source times."""
    queue = []
    for item in trace_rows or []:
        if item.get("schedule_reconciliation_status") != "REVIEW_REQUIRED":
            continue
        season_id = str(item.get("runtime_provider_season_id") or item.get("archive_provider_season_id") or "").strip()
        fixture_id = str(item.get("fixture_id") or "").strip()
        home_id = str(item.get("runtime_home_team_id") or item.get("archive_home_team_id") or "").strip()
        away_id = str(item.get("runtime_away_team_id") or item.get("archive_away_team_id") or "").strip()
        identity_parts = (season_id, fixture_id, home_id, away_id)
        queue.append({
            "status": "REVIEW_REQUIRED",
            "schedule_reconciliation_status": "REVIEW_REQUIRED",
            "reason": item.get("schedule_reconciliation_reason") or "KICKOFF_MISMATCH",
            "fixture_date": item.get("fixture_date") or item.get("runtime_kickoff_utc") or "",
            "league": item.get("runtime_league", ""),
            "fixture": item.get("runtime_fixture", ""),
            "fixture_id": fixture_id,
            "selected_id": item.get("selected_id", ""),
            "provider_season_id": season_id,
            "home_team_id": home_id,
            "away_team_id": away_id,
            "fixture_identity": "|".join(identity_parts) if all(identity_parts) else "",
            "runtime_kickoff_utc": item.get("runtime_kickoff_utc", ""),
            "archive_kickoff_utc": item.get("archive_kickoff_utc", ""),
            "delta_minutes_archive_minus_runtime": item.get("schedule_delta_minutes_archive_minus_runtime", ""),
            "archive_source_file": item.get("archive_source_file", ""),
            "archive_source_row": item.get("archive_source_row", ""),
            "exact_join_status": item.get("join_status", ""),
            "resolution_action": "MANUAL_AUTHORITATIVE_EVENT_TIME_REVIEW_ONLY_NO_AUTO_CORRECTION",
        })
    return queue


SCHEDULE_RECONCILIATION_HEADERS = [
    "status", "schedule_reconciliation_status", "reason", "fixture_date", "league", "fixture",
    "fixture_id", "selected_id", "provider_season_id", "home_team_id", "away_team_id",
    "fixture_identity", "runtime_kickoff_utc", "archive_kickoff_utc",
    "delta_minutes_archive_minus_runtime", "archive_source_file", "archive_source_row",
    "exact_join_status", "resolution_action"
]



def build_xg_audit(runtime_rows, archive_rows, trace_rows=None):
    """Exact-identity xG evidence inventory. This output is never a prediction input."""
    index = defaultdict(list)
    for row in archive_rows:
        key = archive_key(row)
        if all(key):
            index[key].append(row)
    trace_by_key = {}
    for item in (trace_rows or []):
        key = (
            str(item.get("runtime_provider_season_id") or item.get("archive_provider_season_id") or "").strip(),
            str(item.get("fixture_id") or "").strip(),
            str(item.get("runtime_home_team_id") or item.get("archive_home_team_id") or "").strip(),
            str(item.get("runtime_away_team_id") or item.get("archive_away_team_id") or "").strip(),
        )
        if all(key):
            trace_by_key[key] = item
    output = []
    for runtime in runtime_rows:
        key = runtime_key(runtime)
        matches = index.get(key, []) if all(key) else []
        trace = trace_by_key.get(key, {})
        if not all(key):
            join_status, source = "BLOCKED_MISSING_RUNTIME_COMPOSITE_IDENTITY", {}
        elif len(matches) == 0:
            join_status, source = "BLOCKED_NO_EXACT_ARCHIVE_MATCH", {}
        elif len(matches) > 1:
            join_status, source = "QUARANTINED_DUPLICATE_ARCHIVE_IDENTITY", {}
        else:
            join_status, source = "PASS_EXACT_COMPOSITE_IDENTITY", matches[0]
        output.append({
            "Fixture Date": runtime.get("date_utc", ""),
            "League": runtime.get("league") or runtime.get("provider_competition_name_source") or "",
            "Fixture": f"{runtime.get('home_team','')} vs {runtime.get('away_team','')}",
            "fixture_id": runtime.get("fixture_id", ""),
            "selected_id": runtime.get("selected_id", ""),
            "provider_season_id": key[0] if all(key) else "",
            "home_team_id": key[2] if all(key) else "",
            "away_team_id": key[3] if all(key) else "",
            "fixture": f"{runtime.get('home_team','')} vs {runtime.get('away_team','')}",
            "runtime_kickoff_utc": runtime.get("date_utc", ""),
            "archive_kickoff_utc": source.get("kickoff_utc", ""),
            "history_cutoff_utc": runtime.get("date_utc", ""),
            "join_status": join_status,
            "schedule_reconciliation_status": trace.get("schedule_reconciliation_status", "NOT_VERIFIED"),
            "home_xg_source_field": source.get("home_xg_prematch_source_field", "") or "NOT_AVAILABLE",
            "home_xg_raw": source.get("home_xg_prematch_raw", "") if source else "NOT_AVAILABLE",
            "home_xg_numeric": source.get("home_xg_prematch_value", "") if source else "NOT_AVAILABLE",
            "away_xg_source_field": source.get("away_xg_prematch_source_field", "") or "NOT_AVAILABLE",
            "away_xg_raw": source.get("away_xg_prematch_raw", "") if source else "NOT_AVAILABLE",
            "away_xg_numeric": source.get("away_xg_prematch_value", "") if source else "NOT_AVAILABLE",
            "total_xg_source_field": source.get("total_xg_prematch_source_field", "") or "NOT_AVAILABLE",
            "total_xg_raw": source.get("total_xg_prematch_raw", "") if source else "NOT_AVAILABLE",
            "total_xg_numeric": source.get("total_xg_prematch_value", "") if source else "NOT_AVAILABLE",
            "capture_time_utc": source.get("xg_capture_time_utc", "") if source else "NOT_AVAILABLE",
            "temporal_provenance_status": source.get("xg_temporal_provenance_status", "NOT_AVAILABLE"),
            "prediction_use_status": "QUARANTINED_RESEARCH_AUDIT_ONLY",
            "prediction_eligible": "NO",
            "betting_eligible": "NO",
            "archive_source_file": source.get("source_file", ""),
            "archive_source_row": source.get("source_row", ""),
            "archive_raw_record_sha256": source.get("raw_record_sha256", ""),
            "remediation": "Obtain provider point-in-time snapshot/capture timestamp and revision policy; exclude from all forecasts until verified."
        })
    return output


def snapshot_identity(row):
    return (
        str(row.get("selected_season_id") or "").strip(),
        str(row.get("fixture_id") or "").strip(),
        str(row.get("home_team_provider_id") or "").strip(),
        str(row.get("away_team_provider_id") or "").strip(),
    )


def _optional_count(value):
    try:
        if value in (None, ""):
            return None
        number = float(value)
        return int(number) if math.isfinite(number) else None
    except (TypeError, ValueError, OverflowError):
        return None


def build_snapshot_orientation_map(runtime_rows, snapshot_rows, runtime_provenance, archive_summary):
    """Join no_home_away only through the verified ordered snapshot composite identity."""
    if not snapshot_rows:
        raise ValueError("Snapshot candidate trace is required for the v1.4 orientation audit.")
    expected_snapshot_sha = str(runtime_provenance.get("snapshot_file_sha256") or "").strip()
    expected_archive_sha = str(archive_summary.get("archive_sha256") or "").strip()
    expected_retrieved = str(runtime_provenance.get("snapshot_retrieved_utc") or "").strip()
    expected_artifact_id = str(runtime_provenance.get("snapshot_artifact_id") or "").strip()
    expected_run_id = str(runtime_provenance.get("snapshot_run_id") or "").strip()
    expected_trace_rows = _optional_count(runtime_provenance.get("snapshot_fixture_rows"))
    if not all((expected_snapshot_sha, expected_archive_sha, expected_retrieved,
                expected_artifact_id, expected_run_id, expected_trace_rows is not None)):
        raise ValueError("Runtime provenance is missing verified snapshot artifact metadata.")
    if len(snapshot_rows) != expected_trace_rows:
        raise ValueError("Snapshot candidate trace row count does not match runtime provenance.")

    index = defaultdict(list)
    for row in snapshot_rows:
        if str(row.get("snapshot_file_sha256") or "").strip() != expected_snapshot_sha:
            raise ValueError("Snapshot trace file hash does not match runtime provenance.")
        if str(row.get("source_archive_sha256") or "").strip() != expected_archive_sha:
            raise ValueError("Snapshot trace archive hash does not match the pinned archive.")
        if str(row.get("snapshot_retrieved_utc") or "").strip() != expected_retrieved:
            raise ValueError("Snapshot trace retrieval time does not match runtime provenance.")
        key = snapshot_identity(row)
        if all(key):
            index[key].append(row)

    orientation_by_key = {}
    exact_matches = flagged = distinction_present = unknown = 0
    duplicate_keys = sum(1 for values in index.values() if len(values) > 1)
    incomplete_snapshot_identity_rows = sum(1 for row in snapshot_rows if not all(snapshot_identity(row)))
    for runtime in runtime_rows:
        key = runtime_key(runtime)
        matches = index.get(key, []) if all(key) else []
        source = matches[0] if len(matches) == 1 else {}
        flag = str(source.get("no_home_away") or "").strip() if source else ""
        if not all(key):
            orientation_status = "ORIENTATION_UNKNOWN"
            review_status = "REVIEW_REQUIRED_RUNTIME_IDENTITY_MISSING"
        elif not matches:
            orientation_status = "ORIENTATION_UNKNOWN"
            review_status = "REVIEW_REQUIRED_NO_EXACT_SNAPSHOT_MATCH"
        elif len(matches) > 1:
            orientation_status = "ORIENTATION_UNKNOWN"
            review_status = "REVIEW_REQUIRED_DUPLICATE_SNAPSHOT_MATCH"
        elif flag == "1":
            orientation_status = "NO_HOME_AWAY_DISTINCTION"
            review_status = "REVIEW_REQUIRED_NO_HOME_AWAY_DISTINCTION"
            exact_matches += 1
            flagged += 1
        elif flag == "0":
            orientation_status = "HOME_AWAY_DISTINCTION_PRESENT"
            review_status = "NO_ORIENTATION_REVIEW_FLAG"
            exact_matches += 1
            distinction_present += 1
        else:
            orientation_status = "ORIENTATION_UNKNOWN"
            review_status = "REVIEW_REQUIRED_UNKNOWN_NO_HOME_AWAY_FLAG"
        if orientation_status == "ORIENTATION_UNKNOWN":
            unknown += 1
        orientation_by_key[key] = {
            "snapshot_no_home_away_flag": flag or "NOT_AVAILABLE",
            "fixture_orientation_status": orientation_status,
            "home_away_market_review_status": review_status,
            "snapshot_row_number": source.get("snapshot_row_number", "NOT_AVAILABLE"),
            "snapshot_retrieved_utc": source.get("snapshot_retrieved_utc", "NOT_AVAILABLE"),
            "snapshot_file_sha256": source.get("snapshot_file_sha256", "NOT_AVAILABLE"),
        }

    qa = {
        "status": "PASS_EXACT_SNAPSHOT_TRACE_JOIN" if exact_matches == len(runtime_rows) and unknown == 0 and duplicate_keys == 0 and incomplete_snapshot_identity_rows == 0 else "REVIEW_REQUIRED",
        "runtime_fixture_rows": len(runtime_rows),
        "snapshot_trace_rows": len(snapshot_rows),
        "snapshot_trace_rows_expected": expected_trace_rows,
        "snapshot_trace_row_count_match": len(snapshot_rows) == expected_trace_rows,
        "incomplete_snapshot_identity_rows": incomplete_snapshot_identity_rows,
        "exact_snapshot_matches": exact_matches,
        "no_home_away_flagged": flagged,
        "home_away_distinction_present": distinction_present,
        "orientation_unknown_rows": unknown,
        "duplicate_snapshot_keys": duplicate_keys,
        "snapshot_artifact_id": expected_artifact_id,
        "snapshot_run_id": expected_run_id,
        "snapshot_file_sha256": expected_snapshot_sha,
        "snapshot_retrieved_utc": expected_retrieved,
        "production_eligible": False,
        "betting_eligible": False,
    }
    return orientation_by_key, qa



def require_snapshot_orientation_qa(qa):
    """Fail the candidate report if any runtime fixture lacks an exact binary orientation flag."""
    expected = int(qa.get("runtime_fixture_rows", -1))
    exact = int(qa.get("exact_snapshot_matches", -1))
    flagged = int(qa.get("no_home_away_flagged", -1))
    distinction = int(qa.get("home_away_distinction_present", -1))
    unknown = int(qa.get("orientation_unknown_rows", -1))
    duplicates = int(qa.get("duplicate_snapshot_keys", -1))
    incomplete = int(qa.get("incomplete_snapshot_identity_rows", -1))
    if (
        qa.get("status") != "PASS_EXACT_SNAPSHOT_TRACE_JOIN"
        or expected < 0
        or exact != expected
        or flagged + distinction != expected
        or unknown != 0
        or duplicates != 0
        or incomplete != 0
        or qa.get("snapshot_trace_row_count_match") is not True
        or qa.get("production_eligible") is not False
        or qa.get("betting_eligible") is not False
    ):
        raise ValueError(
            "SNAPSHOT_ORIENTATION_QA_BLOCKED: "
            f"status={qa.get('status')}; runtime={expected}; exact={exact}; "
            f"flagged={flagged}; distinction={distinction}; unknown={unknown}; "
            f"duplicates={duplicates}; incomplete={incomplete}"
        )
    return True


def require_runtime_feature_block_audit(rows, qa):
    """Reconcile source-runtime blocked fixtures and side rows without relaxing any feature gate."""
    expected_sides = int(qa.get("blocked_team_side_histories", -1))
    home_sides = int(qa.get("home_side_histories_below_5", -1))
    away_sides = int(qa.get("away_side_histories_below_5", -1))
    if expected_sides < 0 or len(rows) != expected_sides or home_sides + away_sides != expected_sides:
        raise ValueError(
            "RUNTIME_FEATURE_BLOCK_AUDIT_RECONCILIATION_FAILED: "
            f"rows={len(rows)}; expected={expected_sides}; home={home_sides}; away={away_sides}"
        )
    keys = []
    for row in rows:
        try:
            count = int(row.get("recent5_feature_complete_n"))
        except (TypeError, ValueError):
            raise ValueError("RUNTIME_FEATURE_BLOCK_AUDIT_HAS_INVALID_SIDE_SAMPLE_COUNT")
        if count >= 5 or row.get("team_side") not in {"HOME", "AWAY"}:
            raise ValueError("RUNTIME_FEATURE_BLOCK_AUDIT_CONTAINS_NON_BLOCKED_SIDE")
        if row.get("production_eligible") != "NO" or row.get("betting_eligible") != "NO":
            raise ValueError("RUNTIME_FEATURE_BLOCK_AUDIT_ELIGIBILITY_MUST_REMAIN_NO")
        keys.append((
            str(row.get("provider_season_id") or ""),
            str(row.get("fixture_id") or ""),
            str(row.get("team_side") or ""),
            str(row.get("team_provider_id") or ""),
        ))
    if len(keys) != len(set(keys)):
        raise ValueError("RUNTIME_FEATURE_BLOCK_AUDIT_HAS_DUPLICATE_EXACT_SIDE_KEYS")
    return True

def build_runtime_feature_block_audit(runtime_rows):
    """Expose the runtime's actual 20-feature gate; do not substitute score-only form counts."""
    blocked = [
        row for row in runtime_rows
        if str(row.get("feature_support_status") or row.get("prediction_status") or "").startswith("BLOCKED")
    ]
    output = []
    feature_counts = {}
    sample_counts = {}
    home_sides = 0
    away_sides = 0
    for row in blocked:
        missing = str(row.get("missing_required_features") or "").strip()
        for feature in [item for item in missing.split(";") if item]:
            feature_counts[feature] = feature_counts.get(feature, 0) + 1
        for side in ("home", "away"):
            count = _optional_count(row.get(f"{side}_recent5_n"))
            if count is None or count >= 5:
                continue
            if side == "home":
                home_sides += 1
            else:
                away_sides += 1
            sample_counts[str(count)] = sample_counts.get(str(count), 0) + 1
            output.append({
                "Fixture Date": row.get("date_utc", ""),
                "League": row.get("league", ""),
                "Fixture": f"{row.get('home_team', '')} vs {row.get('away_team', '')}",
                "fixture_id": row.get("fixture_id", ""),
                "selected_id": row.get("selected_id", ""),
                "provider_season_id": row.get("provider_season_id", ""),
                "team_side": side.upper(),
                "team_provider_id": row.get(f"{side}_team_provider_id", ""),
                "recent5_feature_complete_n": count,
                "team_side_history_gate": "BLOCKED_LT_5_FEATURE_COMPLETE_PRIOR_MATCHES",
                "missing_required_features": missing,
                "feature_support_status": row.get("feature_support_status", ""),
                "prediction_block_reason": row.get("prediction_block_reason", ""),
                "production_eligible": "NO",
                "betting_eligible": "NO",
            })
    qa = {
        "status": "RESEARCH_ONLY_RUNTIME_FEATURE_BLOCK_AUDIT",
        "blocked_fixture_rows": len(blocked),
        "blocked_team_side_histories": len(output),
        "home_side_histories_below_5": home_sides,
        "away_side_histories_below_5": away_sides,
        "side_history_sample_n_counts": dict(sorted(sample_counts.items())),
        "missing_required_feature_counts": dict(sorted(feature_counts.items())),
        "production_eligible": False,
        "betting_eligible": False,
    }
    return output, qa


XG_AUDIT_HEADERS = [
    "Fixture Date", "League", "Fixture",
    "fixture_id", "selected_id", "provider_season_id", "home_team_id", "away_team_id",
    "fixture", "runtime_kickoff_utc", "archive_kickoff_utc", "history_cutoff_utc",
    "join_status", "schedule_reconciliation_status",
    "home_xg_source_field", "home_xg_raw", "home_xg_numeric",
    "away_xg_source_field", "away_xg_raw", "away_xg_numeric",
    "total_xg_source_field", "total_xg_raw", "total_xg_numeric",
    "capture_time_utc", "temporal_provenance_status", "prediction_use_status",
    "prediction_eligible", "betting_eligible", "archive_source_file",
    "archive_source_row", "archive_raw_record_sha256", "remediation"
]


COVERAGE_HEADERS = [
    "Selected Season ID", "Country", "League", "Upcoming Fixtures (7d)",
    "Exact Archive Joins", "Kickoff Matches", "Kickoff Mismatches Requiring Review",
    "BTTS Raw Research Predictions", "Home 1X Raw Research Predictions",
    "Away X2 Raw Research Predictions", "Feature-blocked Fixtures",
    "Blocked Team-side Histories", "Experimental Goal Forecasts",
    "Experimental Goal Forecasts Blocked", "Team Form Side Rows",
    "Overall Form Full-5 Samples", "Overall Form >=3 Samples", "Overall Form <5 Samples",
    "Venue Form Full-5 Samples", "Venue Form >=3 Samples", "Venue Form <3 Samples",
    "Fixtures with Prior H2H", "Individual H2H Meeting Rows", "Provisional Table Rows",
    "Pre-match-labelled xG Rows", "Verified xG Capture Timestamps",
    "Historical Accuracy Graded", "Production Eligible YES", "Betting Eligible YES",
    "Fixture Coverage Status", "Raw Oracle Prediction Status", "Production / Betting Status"
]


def _coverage_int(value):
    try:
        number = float(value)
        return int(number) if math.isfinite(number) else 0
    except (TypeError, ValueError, OverflowError):
        return 0


def _coverage_available(value):
    text = str(value or "").strip()
    return bool(text) and text not in ("None", UNAVAILABLE, "N/A") and not text.startswith("NOT_")


def _coverage_numeric(value):
    try:
        number = float(value)
        return math.isfinite(number)
    except (TypeError, ValueError, OverflowError):
        return False


def build_50_league_coverage_rows(schedule_rows, runtime_rows, report_rows, trace_rows,
                                  xg_audit_rows=None, goal_market_rows=None):
    """Build one auditable row per governed Selected-50 season, including no-fixture groups."""
    if not (len(runtime_rows) == len(report_rows) == len(trace_rows)):
        raise ValueError("Runtime, report and evidence-trace rows must align exactly.")
    groups = defaultdict(lambda: {
        "runtime": [], "report": [], "trace": [], "xg": [], "goal": []
    })
    for runtime, report, trace in zip(runtime_rows, report_rows, trace_rows):
        selected_id = str(trace.get("selected_id") or runtime.get("selected_id") or "").strip()
        if selected_id:
            group = groups[selected_id]
            group["runtime"].append(runtime)
            group["report"].append(report)
            group["trace"].append(trace)
    for item in (xg_audit_rows or []):
        selected_id = str(item.get("selected_id") or "").strip()
        if selected_id:
            groups[selected_id]["xg"].append(item)
    for item in (goal_market_rows or []):
        selected_id = str(item.get("provider_season_id") or item.get("selected_id") or "").strip()
        if selected_id:
            groups[selected_id]["goal"].append(item)

    output = []
    seen = set()
    for schedule in sorted(schedule_rows, key=lambda item: str(item.get("selected_id") or "")):
        sid = str(schedule.get("selected_id") or "").strip()
        if not sid or sid in seen:
            raise ValueError("Selected-50 schedule contains a blank or duplicate selected_id.")
        seen.add(sid)
        group = groups.get(sid, {"runtime": [], "report": [], "trace": [], "xg": [], "goal": []})
        runtime = group["runtime"]
        report = group["report"]
        trace = group["trace"]
        xg = group["xg"]
        goals = group["goal"]
        fixture_count = len(runtime)

        exact_joins = sum(str(item.get("join_status") or "").startswith("PASS_EXACT") for item in trace)
        kickoff_matches = sum(str(item.get("schedule_reconciliation_status") or "").upper() in ("MATCH", "PASS") for item in trace)
        kickoff_mismatches = sum(str(item.get("schedule_reconciliation_status") or "").upper() == "REVIEW_REQUIRED" for item in trace)
        btts = sum(_coverage_available(item.get("BTTS Yes")) for item in report)
        home_1x = sum(_coverage_available(item.get("Home 1X")) for item in report)
        away_x2 = sum(_coverage_available(item.get("Away X2")) for item in report)

        blocked_runtime = [
            item for item in runtime
            if str(item.get("feature_support_status") or item.get("prediction_status") or "").startswith("BLOCKED")
        ]
        feature_blocked = len(blocked_runtime)
        blocked_sides = sum(_coverage_int(item.get("home_recent5_n")) < 5 for item in blocked_runtime)
        blocked_sides += sum(_coverage_int(item.get("away_recent5_n")) < 5 for item in blocked_runtime)

        home_n = [_coverage_int(item.get("home_form_n")) for item in trace]
        away_n = [_coverage_int(item.get("away_form_n")) for item in trace]
        overall_ns = home_n + away_n
        home_venue_n = [_coverage_int(item.get("home_at_home_form_n")) for item in trace]
        away_venue_n = [_coverage_int(item.get("away_away_form_n")) for item in trace]
        venue_ns = home_venue_n + away_venue_n

        goal_forecasts = sum(
            str(item.get("forecast_status") or item.get("status") or "") == "EXPERIMENTAL_UNCALIBRATED"
            for item in goals
        )
        goal_blocked = sum(
            str(item.get("forecast_status") or item.get("status") or "").startswith("BLOCKED")
            or _coverage_available(item.get("blocked_reason"))
            for item in goals
        )
        xg_numeric_rows = sum(
            all(_coverage_numeric(item.get(field)) for field in
                ("home_xg_numeric", "away_xg_numeric", "total_xg_numeric"))
            for item in xg
        )
        xg_verified_rows = sum(
            _coverage_available(item.get("capture_time_utc"))
            and str(item.get("temporal_provenance_status") or "").startswith("VERIFIED")
            for item in xg
        )
        accuracy_graded = sum(
            _coverage_available(item.get("Historical Accuracy Status"))
            and not str(item.get("Historical Accuracy Status") or "").startswith(("NOT_VALIDATED", "NOT_GRADED"))
            for item in report
        )
        production_yes = sum(str(item.get("production_eligible") or "").upper() == "YES" for item in trace)
        betting_yes = sum(str(item.get("betting_eligible") or "").upper() == "YES" for item in trace)
        h2h_fixtures = sum(_coverage_int(item.get("h2h_n")) > 0 for item in trace)
        h2h_meetings = sum(_coverage_int(item.get("h2h_n")) for item in trace)
        provisional_tables = sum(
            str(item.get("league_table_status") or "") == "PROVISIONAL_CONVENTIONAL_TABLE"
            for item in trace
        )

        if fixture_count == 0:
            fixture_status = "NO_FIXTURE_IN_7D_HORIZON"
            prediction_status = "NO_FIXTURES_TO_SCORE"
        else:
            fixture_status = str(schedule.get("schedule_coverage_status") or "FIXTURES_FOUND")
            if not (btts + home_1x + away_x2):
                prediction_status = "NO_RAW_MARKET_OUTPUTS"
            elif min(btts, home_1x, away_x2) < fixture_count:
                prediction_status = "PARTIAL_PREDICTIONS_WITH_FEATURE_BLOCKS"
            else:
                prediction_status = "RAW_RESEARCH_PREDICTIONS_PRESENT"
        eligibility_status = "ELIGIBILITY_REVIEW_REQUIRED" if production_yes or betting_yes else "NOT_ELIGIBLE"

        row = {
            "Selected Season ID": sid,
            "Country": schedule.get("country", ""),
            "League": schedule.get("competition_name", ""),
            "Upcoming Fixtures (7d)": fixture_count,
            "Exact Archive Joins": exact_joins,
            "Kickoff Matches": kickoff_matches,
            "Kickoff Mismatches Requiring Review": kickoff_mismatches,
            "BTTS Raw Research Predictions": btts,
            "Home 1X Raw Research Predictions": home_1x,
            "Away X2 Raw Research Predictions": away_x2,
            "Feature-blocked Fixtures": feature_blocked,
            "Blocked Team-side Histories": blocked_sides,
            "Experimental Goal Forecasts": goal_forecasts,
            "Experimental Goal Forecasts Blocked": goal_blocked,
            "Team Form Side Rows": 2 * fixture_count,
            "Overall Form Full-5 Samples": sum(value >= 5 for value in overall_ns),
            "Overall Form >=3 Samples": sum(value >= 3 for value in overall_ns),
            "Overall Form <5 Samples": sum(value < 5 for value in overall_ns),
            "Venue Form Full-5 Samples": sum(value >= 5 for value in venue_ns),
            "Venue Form >=3 Samples": sum(value >= 3 for value in venue_ns),
            "Venue Form <3 Samples": sum(value < 3 for value in venue_ns),
            "Fixtures with Prior H2H": h2h_fixtures,
            "Individual H2H Meeting Rows": h2h_meetings,
            "Provisional Table Rows": provisional_tables,
            "Pre-match-labelled xG Rows": xg_numeric_rows,
            "Verified xG Capture Timestamps": xg_verified_rows,
            "Historical Accuracy Graded": accuracy_graded,
            "Production Eligible YES": production_yes,
            "Betting Eligible YES": betting_yes,
            "Fixture Coverage Status": fixture_status,
            "Raw Oracle Prediction Status": prediction_status,
            "Production / Betting Status": eligibility_status,
        }
        output.append(row)
    return output


def build_coverage_summary_rows(coverage_rows, runtime_rows=None, report_rows=None,
                               trace_rows=None, runtime_provenance=None,
                               archive_summary=None, report_summary=None,
                               xg_audit_rows=None, runtime_artifact_id=""):
    """Create a provenance-led summary with the same field-level gates as the 50-row matrix."""
    runtime_rows = runtime_rows or []
    report_rows = report_rows or []
    trace_rows = trace_rows or []
    runtime_provenance = runtime_provenance or {}
    archive_summary = archive_summary or {}
    report_summary = report_summary or {}
    xg_audit_rows = xg_audit_rows or []
    total = lambda field: sum(_coverage_int(item.get(field)) for item in coverage_rows)
    fixture_groups = sum(_coverage_int(item.get("Upcoming Fixtures (7d)")) > 0 for item in coverage_rows)
    no_fixture_groups = len(coverage_rows) - fixture_groups
    blocked_runtime = [
        item for item in runtime_rows
        if str(item.get("feature_support_status") or item.get("prediction_status") or "").startswith("BLOCKED")
    ]
    blocked_four = sum(_coverage_int(item.get("home_recent5_n")) == 4 for item in blocked_runtime)
    blocked_four += sum(_coverage_int(item.get("away_recent5_n")) == 4 for item in blocked_runtime)
    blocked_three = sum(_coverage_int(item.get("home_recent5_n")) == 3 for item in blocked_runtime)
    blocked_three += sum(_coverage_int(item.get("away_recent5_n")) == 3 for item in blocked_runtime)

    def verified(value):
        return str(value or "").upper().startswith(("PASS", "VERIFIED"))

    provider_parent_ids = {
        str(item.get("selected_id") or "").strip()
        for item in runtime_rows
        if str(item.get("provider_competition_id_status") or "").upper().startswith("VERIFIED_PARENT")
        and str(item.get("selected_id") or "").strip()
    }
    canonical_fixture_rows = sum(verified(item.get("canonical_fixture_join_status")) for item in runtime_rows)
    canonical_team_rows = sum(verified(item.get("canonical_team_join_status")) for item in runtime_rows)
    canonical_bridges = {
        str(item.get("selected_id") or "").strip()
        for item in runtime_rows
        if verified(item.get("canonical_fixture_join_status"))
        and verified(item.get("canonical_team_join_status"))
        and str(item.get("selected_id") or "").strip()
    }
    accuracy_graded = sum(
        _coverage_available(item.get("Historical Accuracy Status"))
        and not str(item.get("Historical Accuracy Status") or "").startswith(("NOT_VALIDATED", "NOT_GRADED"))
        for item in report_rows
    )
    aplus_graded = sum(
        _coverage_available(item.get("A+ Setup Status"))
        and not str(item.get("A+ Setup Status") or "").startswith("NOT_GRADED")
        for item in report_rows
    )
    xg_prediction_eligible = sum(str(item.get("prediction_eligible") or "").upper() == "YES"
                                 for item in xg_audit_rows)
    evidence_date = str(runtime_provenance.get("generated_utc") or "UNKNOWN").split("T")[0]
    run_number = runtime_provenance.get("runtime_run_number")
    evidence_label = f"{evidence_date}; Selected-50 Run #{run_number}" if run_number else evidence_date

    metrics = [
        ("Evidence cutoff", evidence_label, None),
        ("Runtime run ID", runtime_provenance.get("runtime_run_id", "NOT_RECORDED"), None),
        ("Runtime artifact ID", runtime_artifact_id or runtime_provenance.get("runtime_artifact_id") or "NOT_PROVIDED_TO_REPORT_BUILDER", None),
        ("Runtime commit", runtime_provenance.get("runtime_commit_sha", "NOT_RECORDED"), None),
        ("Runtime prediction report SHA-256", runtime_provenance.get("runtime_report_sha256", "NOT_RECORDED"), None),
        ("Pinned archive SHA-256", archive_summary.get("archive_sha256", "NOT_RECORDED"), None),
        ("Pinned archive match records", archive_summary.get("archive_match_records", 0), None),
        ("Pinned archive season folders", archive_summary.get("season_folders", 0), None),
        ("Pinned archive completed match records", archive_summary.get("settled_status_and_score_complete_records", 0), None),
        ("Provider API calls for archive analysis", archive_summary.get("provider_api_calls", 0), None),
        ("Selected league-season groups", len(coverage_rows), "Governed selected season IDs; each appears once."),
        ("Groups with 7-day fixtures", fixture_groups, None),
        ("Groups with no 7-day fixtures", no_fixture_groups, "Not necessarily data failure; no fixture rows in the seven-day report horizon."),
        ("Upcoming fixture rows", total("Upcoming Fixtures (7d)"), None),
        ("Exact archive fixture joins", total("Exact Archive Joins"), None),
        ("Kickoff matches", total("Kickoff Matches"), None),
        ("Kickoff mismatches requiring manual review", total("Kickoff Mismatches Requiring Review"), "Manual authoritative event-time review; no automatic correction."),
        ("League groups with kickoff mismatches", sum(_coverage_int(item.get("Kickoff Mismatches Requiring Review")) > 0 for item in coverage_rows), None),
        ("Raw Oracle BTTS predictions", total("BTTS Raw Research Predictions"), None),
        ("Raw Oracle DC_HOME predictions", total("Home 1X Raw Research Predictions"), None),
        ("Raw Oracle DC_AWAY predictions", total("Away X2 Raw Research Predictions"), None),
        ("Feature-blocked Oracle research fixtures", total("Feature-blocked Fixtures"), "Required-feature gate retained; no imputation or threshold relaxation."),
        ("Feature-blocked team-side histories", total("Blocked Team-side Histories"), None),
        ("Feature-blocked sides with 4 prior oriented matches", blocked_four, None),
        ("Feature-blocked sides with 3 prior oriented matches", blocked_three, None),
        ("Experimental goal-market forecasts", total("Experimental Goal Forecasts"), "Uncalibrated research estimates only."),
        ("Experimental goal-market blocked fixtures", total("Experimental Goal Forecasts Blocked"), "Blocked by insufficient league baseline."),
        ("Fixtures with at least one prior meeting", total("Fixtures with Prior H2H"), None),
        ("Individual H2H meeting rows", total("Individual H2H Meeting Rows"), None),
        ("H2H cross-season meetings verified", report_summary.get("h2h_cross_season_meetings_verified", 0), None),
        ("Team form sides with full 5 overall matches", total("Overall Form Full-5 Samples"), None),
        ("Team form sides with >=3 overall matches", total("Overall Form >=3 Samples"), None),
        ("Venue-split sides with full 5 matches", total("Venue Form Full-5 Samples"), None),
        ("Venue-split sides with >=3 matches", total("Venue Form >=3 Samples"), None),
        ("Provisional league table rows", total("Provisional Table Rows"), "Reconstructed conventional table; not independently verified historical official standings."),
        ("Historical accuracy graded fixtures", accuracy_graded, "Requires exact pre-match prediction ledger and official settlement join."),
        ("A+ setup graded fixtures", aplus_graded, "Calibration, settlement and contemporaneous odds gates have not passed."),
        ("Prematch-labelled xG candidate rows", total("Pre-match-labelled xG Rows"), "Field presence only; not proof of point-in-time availability."),
        ("Prematch-labelled xG rows with capture timestamp", total("Verified xG Capture Timestamps"), "Unverified xG remains quarantined research audit only."),
        ("Prematch-labelled xG prediction eligible rows", xg_prediction_eligible, None),
        ("Production eligible fixtures", total("Production Eligible YES"), "No production eligibility is granted by this report."),
        ("Betting eligible fixtures", total("Betting Eligible YES"), "No betting eligibility is granted by this report."),
        ("Provider parent competition IDs verified", len(provider_parent_ids), "Provider season IDs are not automatically promoted to parent competition IDs."),
        ("Provider-to-canonical bridges verified", len(canonical_bridges), "Canonical cross-provider identity requires explicit approved bridges."),
        ("Canonical fixture joins verified", canonical_fixture_rows, None),
        ("Canonical team joins verified", canonical_team_rows, None),
        ("Overall report status", report_summary.get("report_status", "PARTIAL_RESEARCH_ONLY"), "Research-only; not production-ready or betting-ready."),
        ("League group gate", report_summary.get("league_group_gate", "NOT_VERIFIED"), None),
        ("Required exact join gate", report_summary.get("required_join_gate", "NOT_VERIFIED"), None),
        ("Schedule reconciliation gate", report_summary.get("schedule_reconciliation_gate", "NOT_VERIFIED"), None),
        ("Production readiness", archive_summary.get("production_readiness", "NOT_GRANTED"), None),
    ]
    orientation = report_summary.get("fixture_orientation", {})
    runtime_blocks = report_summary.get("runtime_feature_block_audit", {})
    metrics.extend([
        ("Runtime fixtures with no home/away distinction", orientation.get("no_home_away_flagged", 0),
         "Exact ordered-ID snapshot join; review home/away-oriented markets only; no probability changes."),
        ("Runtime fixtures with home/away distinction", orientation.get("home_away_distinction_present", 0), None),
        ("Runtime fixtures with unresolved orientation", orientation.get("orientation_unknown_rows", 0),
         "Unknown orientation remains review-required; never infer a flag."),
        ("Exact snapshot trace matches", orientation.get("exact_snapshot_matches", 0), None),
        ("Runtime feature-blocked fixtures", runtime_blocks.get("blocked_fixture_rows", 0),
         "Copied from the source runtime's 20-feature gate; not recalculated by the report builder."),
        ("Runtime blocked team-side histories", runtime_blocks.get("blocked_team_side_histories", 0),
         "Counts home/away sides with fewer than five feature-complete prior matches."),
        ("Home team-side histories below five", runtime_blocks.get("home_side_histories_below_5", 0), None),
        ("Away team-side histories below five", runtime_blocks.get("away_side_histories_below_5", 0), None),
    ])
    return [{"Metric": metric, "Value": value, "Interpretation": interpretation}
            for metric, value, interpretation in metrics]


def build_xg_provenance_rows(coverage_rows):
    total = lambda field: sum(_coverage_int(item.get(field)) for item in coverage_rows)
    candidates = total("Pre-match-labelled xG Rows")
    verified = total("Verified xG Capture Timestamps")
    return [
        {"Control": "Selected-50 xG candidates",
         "Finding": f"{candidates} numeric pre-match-labelled fixture rows in the current report horizon.",
         "Decision / implication": "Field presence does not establish when values were first available."},
        {"Control": "Point-in-time capture timestamps",
         "Finding": f"{verified}/{candidates} rows have a verified capture timestamp.",
         "Decision / implication": "Keep all unverified xG quarantined from historical backtests, forecasts and betting."},
        {"Control": "Provider documentation",
         "Finding": "Reviewed FootyStats documentation describes an as-of max_time query for league/team statistics; it does not establish an immutable per-fixture historical xG snapshot or revision history.",
         "Decision / implication": "Do not infer historical pre-kickoff availability from the *_xg_prematch field names."},
        {"Control": "API activity in this report build",
         "Finding": "No authenticated provider API request is made by the report builder.",
         "Decision / implication": "No provider credits are consumed; account validity and credit balance remain unverified."},
        {"Control": "Eligibility",
         "Finding": f"{total('Production Eligible YES')} production-eligible and {total('Betting Eligible YES')} betting-eligible fixtures.",
         "Decision / implication": "All report outputs remain research-only; xG prediction_eligible=NO and betting_eligible=NO until provenance is demonstrated."},
    ]



def fmt(value):
    return "N/A" if value is None else f"{value:.2f}"


def evidence_risk(form_n, has_position, h2h_n, identity_ok):
    # Evidence coverage score only; not a probability of losing or match outcome.
    components = {
        "form_gap": max(0.0, (5 - min(form_n, 5)) / 5) * 40,
        "standings_gap": 0.0 if has_position else 30.0,
        "h2h_gap": max(0.0, (5 - min(h2h_n, 5)) / 5) * 20,
        "identity_gap": 0.0 if identity_ok else 10.0,
    }
    risk = round(sum(components.values()), 1)
    rationale = ("Evidence coverage gap: " + ", ".join(
        f"{k}={v:.0f}/" + str({"form_gap":40,"standings_gap":30,"h2h_gap":20,"identity_gap":10}[k])
        for k, v in components.items() if v > 0
    )) if risk else "Required evidence coverage present; standings remain provisional."
    return risk, rationale


def independent_analysis(hf, af, ha, aa, hd, ad):
    if hf["n"] < 3 or af["n"] < 3:
        return "Insufficient recent five-match evidence for a balanced comparison; no independent match conclusion assigned."
    parts = []
    if hf["ppg"] > af["ppg"]:
        parts.append("Home side has the stronger recent points rate")
    elif hf["ppg"] < af["ppg"]:
        parts.append("Away side has the stronger recent points rate")
    else:
        parts.append("Recent points rates are level")
    if ha is not None and aa is not None:
        parts.append("home attacking index is higher" if ha > aa else "away attacking index is higher" if aa > ha else "attacking indices are level")
    if hd is not None and ad is not None:
        parts.append("home defensive index is higher" if hd > ad else "away defensive index is higher" if ad > hd else "defensive indices are level")
    return "; ".join(parts) + ". Evidence summary only; not a calibrated prediction or betting recommendation."


def base_row(runtime, league_name, join_status):
    row = {h: "" for h in HEADERS}
    row["Fixture Date"] = runtime.get("date_utc", "")
    row["League"] = league_name
    row["Fixture"] = f"{runtime.get('home_team','')} vs {runtime.get('away_team','')}"
    for header, source in SUPPORTED.items():
        value = runtime.get(source, "")
        row[header] = value if value not in (None, "") else "NOT_AVAILABLE_FROM_ORACLE_OUTPUT"
    for header in HEADERS[6:20]:
        row[header] = UNAVAILABLE
    row["Historical Accuracy Status"] = "NOT_VALIDATED"
    row["A+ Setup Status"] = "NOT_GRADED"
    if join_status != "EXACT_ARCHIVE_JOIN":
        row["Recent Form (5)"] = join_status
        row["Recent Form Points (Last 5)"] = join_status
        row["League Position"] = join_status
        row["Avg. Goals Scored (Last 5)"] = join_status
        row["Avg. Goals Conceded (Last 5)"] = join_status
        row["Avg. Points (Last 5)"] = join_status
        row["Attacking Index"] = join_status
        row["Defensive Index"] = join_status
        row["TOTAL Index"] = join_status
        row["H2H Last 5 Summary"] = join_status
        row["H2H Avg Total Goals"] = join_status
        row["Home Evidence Risk"] = "UNQUANTIFIED_IDENTITY_OR_ARCHIVE_JOIN_FAILURE"
        row["Away Evidence Risk"] = "UNQUANTIFIED_IDENTITY_OR_ARCHIVE_JOIN_FAILURE"
        row["Home Risk Rationale"] = join_status
        row["Away Risk Rationale"] = join_status
        row["A+ Setup Status"] = "NOT_GRADED"
        row["Gem's Independent Match Analysis"] = "No analysis: exact archive identity join failed."
    return row


def write_xlsx(path, rows, trace=None, archive_summary=None, goal_market_rows=None, xg_audit_rows=None, league_coverage_rows=None, coverage_summary_rows=None, xg_provenance_rows=None, runtime_rows=None, snapshot_orientation_by_key=None):
    wb = Workbook()
    ws = wb.active
    ws.title = "Oracle V1.6 Output"
    ws.append(HEADERS)
    for row in rows:
        ws.append([row.get(h, "") for h in HEADERS])
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = ws.dimensions
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="333366")
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[1].height = 42
    widths = [14, 20, 34] + [18] * 17 + [32] * 18
    for i, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = width
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    # Supporting evidence tabs expand visibility without changing the locked 38-column summary.
    trace = trace or []
    def add_sheet(name, headers, data):
        sh = wb.create_sheet(name)
        sh.append(headers)
        for item in data:
            sh.append([item.get(h, "") for h in headers])
        sh.freeze_panes = "A2"
        sh.auto_filter.ref = sh.dimensions
        for cell in sh[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="333366")
            cell.alignment = Alignment(wrap_text=True, vertical="center")
        for col in range(1, len(headers) + 1):
            sh.column_dimensions[get_column_letter(col)].width = min(42, max(14, len(str(headers[col-1])) + 3))
        for cells in sh.iter_rows(min_row=2):
            for cell in cells:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
        return sh

    # Consolidated analyst view. Production output remains separately preserved.
    trace = trace or []
    def trace_identity(item):
        return (
            str(item.get("runtime_provider_season_id") or item.get("archive_provider_season_id") or "").strip(),
            str(item.get("fixture_id") or "").strip(),
            str(item.get("runtime_home_team_id") or item.get("archive_home_team_id") or "").strip(),
            str(item.get("runtime_away_team_id") or item.get("archive_away_team_id") or "").strip(),
        )

    def fixture_context(item):
        return {
            "Fixture Date": item.get("fixture_date") or item.get("runtime_kickoff_utc") or "",
            "League": item.get("runtime_league", ""),
            "Fixture": item.get("runtime_fixture") or (
                str(item.get("runtime_home_team") or "") + " vs " + str(item.get("runtime_away_team") or "")
            ),
        }

    trace_by_exact_key = {}
    for item in trace:
        key = trace_identity(item)
        if all(key):
            trace_by_exact_key[key] = item
    runtime_by_exact_key = {}
    for item in (runtime_rows or []):
        key = runtime_key(item)
        if all(key):
            if key in runtime_by_exact_key:
                raise ValueError(f"Duplicate runtime row for supporting-tab identity: {key}")
            runtime_by_exact_key[key] = item
    snapshot_orientation_by_key = snapshot_orientation_by_key or {}
    goal_by_key_candidates = defaultdict(list)
    for item in (goal_market_rows or []):
        key = (
            str(item.get("provider_season_id") or "").strip(),
            str(item.get("fixture_id") or "").strip(),
            str(item.get("home_team_id") or "").strip(),
            str(item.get("away_team_id") or "").strip(),
        )
        if all(key):
            goal_by_key_candidates[key].append(item)
    goal_by_exact_key = {key: values[0] for key, values in goal_by_key_candidates.items() if len(values) == 1}
    decision_headers = HEADERS + [
        "Fixture ID", "Provider Season ID", "Home Team ID", "Away Team ID",
        "Schedule Reconciliation", "History Cutoff UTC",
        "Home Last-5 Form", "Home Last-5 N", "Home Goals For Avg", "Home Goals Against Avg",
        "Home Points Per Game", "Home-at-Home N", "Home-at-Home Form",
        "Away Last-5 Form", "Away Last-5 N", "Away Goals For Avg", "Away Goals Against Avg",
        "Away Points Per Game", "Away-Away N", "Away-Away Form",
        "Home League Position", "Away League Position", "League Table Status",
        "H2H Last-5", "H2H N", "H2H Avg Total Goals",
        "Goal Research Status", "Goal Research Model ID",
        "Research Over 1.5 %", "Research Over 2.5 %", "Research Under 4.5 %",
        "Research Home Over 1.5 %", "Research Away Over 1.5 %",
        "Home Expected Goals Lambda", "Away Expected Goals Lambda",
        "Goal Research Home/Away Sample N", "Goal Research League Prior N",
        "Goal Research Source", "Goal Research Block Reason",
        "Historical Accuracy Status", "A+ Setup Status",
        "Evidence / Schedule Gate", "Production Eligible", "Betting Eligible",
        "History Source Fixture IDs"
    ]
    decision_rows = []
    for row_index, base_row_data in enumerate(rows):
        t = trace[row_index] if row_index < len(trace) else {}
        fid = str(t.get("fixture_id") or "").strip()
        g = goal_by_exact_key.get(trace_identity(t), {})
        extra = {
            "Fixture ID": fid,
            "Provider Season ID": t.get("archive_provider_season_id", g.get("provider_season_id", "")),
            "Home Team ID": t.get("archive_home_team_id", g.get("home_team_id", "")),
            "Away Team ID": t.get("archive_away_team_id", g.get("away_team_id", "")),
            "Schedule Reconciliation": t.get("schedule_reconciliation_status", "UNAVAILABLE"),
            "History Cutoff UTC": t.get("history_cutoff_utc", ""),
            "Home Last-5 Form": t.get("home_form", ""),
            "Home Last-5 N": t.get("home_form_n", ""),
            "Home Goals For Avg": t.get("home_form_gf_avg", ""),
            "Home Goals Against Avg": t.get("home_form_ga_avg", ""),
            "Home Points Per Game": t.get("home_form_ppg", ""),
            "Home-at-Home N": t.get("home_at_home_form_n", ""),
            "Home-at-Home Form": t.get("home_at_home_form") or "NOT_AVAILABLE_INSUFFICIENT_VENUE_SAMPLE",
            "Away Last-5 Form": t.get("away_form", ""),
            "Away Last-5 N": t.get("away_form_n", ""),
            "Away Goals For Avg": t.get("away_form_gf_avg", ""),
            "Away Goals Against Avg": t.get("away_form_ga_avg", ""),
            "Away Points Per Game": t.get("away_form_ppg", ""),
            "Away-Away N": t.get("away_away_form_n", ""),
            "Away-Away Form": t.get("away_away_form") or "NOT_AVAILABLE_INSUFFICIENT_VENUE_SAMPLE",
            "Home League Position": t.get("home_league_position", ""),
            "Away League Position": t.get("away_league_position", ""),
            "League Table Status": t.get("league_table_status", ""),
            "H2H Last-5": base_row_data.get("H2H Last 5 Summary", ""),
            "H2H N": t.get("h2h_n", ""),
            "H2H Avg Total Goals": h2h_average_total_goals(t),
            "Goal Research Status": g.get("forecast_status", g.get("status", "NOT_AVAILABLE")),
            "Goal Research Model ID": g.get("model_id", ""),
            "Research Over 1.5 %": g.get("over15_probability_pct", "NOT_AVAILABLE"),
            "Research Over 2.5 %": g.get("over25_probability_pct", "NOT_AVAILABLE"),
            "Research Under 4.5 %": g.get("under45_probability_pct", "NOT_AVAILABLE"),
            "Research Home Over 1.5 %": g.get("home_over15_probability_pct", "NOT_AVAILABLE"),
            "Research Away Over 1.5 %": g.get("away_over15_probability_pct", "NOT_AVAILABLE"),
            "Home Expected Goals Lambda": g.get("home_lambda", ""),
            "Away Expected Goals Lambda": g.get("away_lambda", ""),
            "Goal Research Home/Away Sample N": str(g.get("home_overall_n", "")) + "/" + str(g.get("away_overall_n", "")),
            "Goal Research League Prior N": g.get("league_prior_n", ""),
            "Goal Research Source": "Home:" + str(g.get("home_lambda_source", "")) + "; Away:" + str(g.get("away_lambda_source", "")),
            "Goal Research Block Reason": g.get("blocked_reason") or ("NONE_FORECASTABLE_RESEARCH_ONLY" if g.get("forecast_status") == "EXPERIMENTAL_UNCALIBRATED" else "NOT_AVAILABLE_REASON_NOT_RETURNED"),
            "Historical Accuracy Status": base_row_data.get("Historical Accuracy Status", "NOT_VALIDATED"),
            "A+ Setup Status": base_row_data.get("A+ Setup Status", "NOT_GRADED"),
            "Evidence / Schedule Gate": (
                "REVIEW_REQUIRED_SCHEDULE_DISCORDANCE" if t.get("schedule_reconciliation_status") == "REVIEW_REQUIRED"
                else "EXACT_JOIN_EVIDENCE_AVAILABLE" if str(t.get("join_status", "")).startswith("PASS")
                else "BLOCKED_OR_UNAVAILABLE"
            ),
            "Production Eligible": "NO",
            "Betting Eligible": "NO",
            "History Source Fixture IDs": ";".join(x for x in (
                str(t.get("home_form_source_fixture_ids") or ""),
                str(t.get("away_form_source_fixture_ids") or "")
            ) if x)
        }
        decision_rows.append({**base_row_data, **extra})
    decision_sheet = add_sheet("Market Intelligence", decision_headers, decision_rows)
    decision_sheet.freeze_panes = "D2"
    decision_sheet.row_dimensions[1].height = 54

    h2h_rows = []
    team_rows = []
    quality_rows = []
    for item in trace:
        base = {**fixture_context(item),
                "fixture_id": item.get("fixture_id", ""), "selected_id": item.get("selected_id", ""),
                "history_cutoff_utc": item.get("history_cutoff_utc", ""),
                "h2h_scope": item.get("h2h_scope", ""),
                "provider_competition_id": item.get("archive_provider_competition_id", "")}
        try:
            meetings = json.loads(item.get("h2h_meetings_detail") or "[]")
        except (TypeError, ValueError):
            meetings = []
        for rank, meeting in enumerate(meetings, 1):
            meeting = dict(meeting)
            meeting["meeting_fixture_id"] = meeting.pop("fixture_id", "")
            h2h_rows.append({**base, "meeting_rank_latest_first": rank, **meeting})
        for side in ("home", "away"):
            venue = "home_at_home" if side == "home" else "away_away"
            team_rows.append({
                **base, "side": side, "team_id": item.get(f"archive_{side}_team_id", ""),
                "overall_last5_n": item.get(f"{side}_form_n", ""),
                "overall_last5_form": item.get(f"{side}_form", ""),
                "overall_last5_gf_avg": item.get(f"{side}_form_gf_avg", ""),
                "overall_last5_ga_avg": item.get(f"{side}_form_ga_avg", ""),
                "overall_last5_points_per_game": item.get(f"{side}_form_ppg", ""),
                "historical_btts_rate_pct": item.get(f"{side}_form_btts_rate", ""),
                "historical_over15_rate_pct": item.get(f"{side}_form_over15_rate", ""),
                "historical_over25_rate_pct": item.get(f"{side}_form_over25_rate", ""),
                "historical_under45_rate_pct": item.get(f"{side}_form_under45_rate", ""),
                "team_over15_rate_pct": item.get(f"{side}_team_over15_rate", ""),
                "clean_sheet_rate_pct": item.get(f"{side}_clean_sheet_rate", ""),
                "failed_to_score_rate_pct": item.get(f"{side}_failed_to_score_rate", ""),
                "overall_source_fixture_ids": item.get(f"{side}_form_source_fixture_ids", ""),
                "venue_split": venue, "venue_last5_n": item.get(f"{venue}_form_n", ""),
                "venue_last5_form": item.get(f"{venue}_form", ""),
                "venue_avg_goals_for": item.get(f"{venue}_avg_goals_for", ""),
                "venue_avg_goals_against": item.get(f"{venue}_avg_goals_against", ""),
                "venue_avg_points": item.get(f"{venue}_avg_points", ""),
                "venue_source_fixture_ids": item.get(f"{venue}_source_fixture_ids", ""),
                "league_position": item.get(f"{side}_league_position", ""),
                "table_status": item.get("league_table_status", ""),
                "table_sample_n": item.get(f"{side}_table_sample_n", "")
            })
        exact_key = trace_identity(item)
        runtime_item = runtime_by_exact_key.get(exact_key, {})
        orientation_item = snapshot_orientation_by_key.get(exact_key, {})
        home_n = _optional_count(runtime_item.get("home_recent5_n"))
        away_n = _optional_count(runtime_item.get("away_recent5_n"))
        blocked_sides = [
            side for side, count in (("HOME", home_n), ("AWAY", away_n))
            if count is not None and count < 5
        ]
        quality_rows.append({
            **fixture_context(item),
            "fixture_identity": item.get("fixture_identity", ""),
            "fixture_id": item.get("fixture_id", ""), "selected_id": item.get("selected_id", ""),
            "join_status": item.get("join_status", ""),
            "schedule_status": item.get("schedule_reconciliation_status", ""),
            "schedule_reconciliation_status": item.get("schedule_reconciliation_status", ""),
            "schedule_reconciliation_reason": item.get("schedule_reconciliation_reason", ""),
            "runtime_kickoff_utc": item.get("runtime_kickoff_utc", ""),
            "archive_kickoff_utc": item.get("archive_kickoff_utc", ""),
            "schedule_delta_minutes_archive_minus_runtime": item.get("schedule_delta_minutes_archive_minus_runtime", ""),
            "history_cutoff_utc": item.get("history_cutoff_utc", ""),
            "home_evidence_risk_pct": item.get("home_risk_pct", ""),
            "away_evidence_risk_pct": item.get("away_risk_pct", ""),
            "home_form_n": item.get("home_form_n", ""), "away_form_n": item.get("away_form_n", ""),
            "h2h_n": item.get("h2h_n", ""), "h2h_scope": item.get("h2h_scope", ""),
            "archive_source_file": item.get("archive_source_file", ""),
            "archive_source_row": item.get("archive_source_row", ""),
            "archive_raw_record_sha256": item.get("archive_raw_record_sha256", ""),
            "production_eligible": item.get("production_eligible", ""),
            "betting_eligible": item.get("betting_eligible", ""),
            "snapshot_no_home_away_flag": orientation_item.get("snapshot_no_home_away_flag", "NOT_AVAILABLE_SNAPSHOT_TRACE_NOT_SUPPLIED"),
            "fixture_orientation_status": orientation_item.get("fixture_orientation_status", "ORIENTATION_UNKNOWN"),
            "home_away_market_review_status": orientation_item.get("home_away_market_review_status", "REVIEW_REQUIRED_ORIENTATION_UNVERIFIED"),
            "snapshot_row_number": orientation_item.get("snapshot_row_number", "NOT_AVAILABLE"),
            "snapshot_retrieved_utc": orientation_item.get("snapshot_retrieved_utc", "NOT_AVAILABLE"),
            "snapshot_file_sha256": orientation_item.get("snapshot_file_sha256", "NOT_AVAILABLE"),
            "runtime_feature_support_status": runtime_item.get("feature_support_status", "NOT_AVAILABLE_RUNTIME_FEATURE_STATUS"),
            "runtime_prediction_block_reason": runtime_item.get("prediction_block_reason", "NOT_AVAILABLE_RUNTIME_BLOCK_REASON"),
            "runtime_missing_required_features": (
                runtime_item.get("missing_required_features") or "NONE"
                if runtime_item else "NOT_AVAILABLE_RUNTIME_FEATURES"
            ),
            "runtime_home_recent5_n": runtime_item.get("home_recent5_n", "NOT_AVAILABLE"),
            "runtime_away_recent5_n": runtime_item.get("away_recent5_n", "NOT_AVAILABLE"),
            "runtime_home_history_gate": "NOT_AVAILABLE" if home_n is None else ("PASS_5_OR_MORE" if home_n >= 5 else "BLOCKED_LT_5"),
            "runtime_away_history_gate": "NOT_AVAILABLE" if away_n is None else ("PASS_5_OR_MORE" if away_n >= 5 else "BLOCKED_LT_5"),
            "runtime_blocked_team_sides": ";".join(blocked_sides) if blocked_sides else "NONE",
            "runtime_blocked_team_side_count": len(blocked_sides)
        })
    add_sheet("xG Evidence Audit", XG_AUDIT_HEADERS, xg_audit_rows or [])
    add_sheet("H2H Intelligence",
        ["Fixture Date", "League", "Fixture", "fixture_id", "selected_id", "history_cutoff_utc", "h2h_scope", "provider_competition_id",
         "meeting_rank_latest_first", "meeting_fixture_id", "kickoff_utc", "provider_season_id",
         "home_team_id", "away_team_id", "home_goals", "away_goals",
         "result_current_home_perspective", "total_goals"], h2h_rows)
    add_sheet("Team Form Evidence",
        ["Fixture Date", "League", "Fixture", "fixture_id", "selected_id", "history_cutoff_utc", "side", "team_id",
         "overall_last5_n", "overall_last5_form", "overall_last5_gf_avg", "overall_last5_ga_avg",
         "overall_last5_points_per_game", "historical_btts_rate_pct", "historical_over15_rate_pct",
         "historical_over25_rate_pct", "historical_under45_rate_pct", "team_over15_rate_pct",
         "clean_sheet_rate_pct", "failed_to_score_rate_pct", "overall_source_fixture_ids", "venue_split",
         "venue_last5_n", "venue_last5_form", "venue_avg_goals_for", "venue_avg_goals_against",
         "venue_avg_points", "venue_source_fixture_ids", "league_position", "table_status",
         "table_sample_n"], team_rows)
    add_sheet("Data Quality & Risk",
        ["Fixture Date", "League", "Fixture", "fixture_identity", "fixture_id", "selected_id",
         "join_status", "schedule_status", "schedule_reconciliation_status", "schedule_reconciliation_reason",
         "runtime_kickoff_utc", "archive_kickoff_utc", "schedule_delta_minutes_archive_minus_runtime",
         "history_cutoff_utc", "home_evidence_risk_pct", "away_evidence_risk_pct",
         "home_form_n", "away_form_n", "h2h_n", "h2h_scope", "archive_source_file", "archive_source_row",
         "archive_raw_record_sha256", "production_eligible", "betting_eligible",
         "snapshot_no_home_away_flag", "fixture_orientation_status", "home_away_market_review_status",
         "snapshot_row_number", "snapshot_retrieved_utc", "snapshot_file_sha256",
         "runtime_feature_support_status", "runtime_prediction_block_reason", "runtime_missing_required_features",
         "runtime_home_recent5_n", "runtime_away_recent5_n", "runtime_home_history_gate",
         "runtime_away_history_gate", "runtime_blocked_team_sides", "runtime_blocked_team_side_count"], quality_rows)
    schedule_queue = build_schedule_reconciliation_queue(trace)
    schedule_sheet_rows = [{
        "Fixture Date": q["fixture_date"], "League": q["league"], "Fixture": q["fixture"],
        "status": q["status"], "reason": q["reason"], "fixture_identity": q["fixture_identity"],
        "fixture_id": q["fixture_id"], "selected_id": q["selected_id"],
        "provider_season_id": q["provider_season_id"], "home_team_id": q["home_team_id"],
        "away_team_id": q["away_team_id"], "runtime_kickoff_utc": q["runtime_kickoff_utc"],
        "archive_kickoff_utc": q["archive_kickoff_utc"],
        "delta_minutes_archive_minus_runtime": q["delta_minutes_archive_minus_runtime"],
        "archive_source_file": q["archive_source_file"], "archive_source_row": q["archive_source_row"],
        "exact_join_status": q["exact_join_status"], "resolution_action": q["resolution_action"],
    } for q in schedule_queue]
    add_sheet("Schedule Reconciliation",
        ["Fixture Date", "League", "Fixture", "status", "reason", "fixture_identity", "fixture_id",
         "selected_id", "provider_season_id", "home_team_id", "away_team_id", "runtime_kickoff_utc",
         "archive_kickoff_utc", "delta_minutes_archive_minus_runtime", "archive_source_file",
         "archive_source_row", "exact_join_status", "resolution_action"], schedule_sheet_rows)
    coverage = []
    for header in HEADERS:
        vals = [str(row.get(header, "")) for row in rows]
        coverage.append({"field": header, "fixture_rows": len(rows),
                         "populated_rows": sum(v not in ("", "None", UNAVAILABLE) and not v.startswith("NOT_") for v in vals),
                         "not_available_from_oracle_output": sum(v == UNAVAILABLE for v in vals),
                         "not_validated_or_not_graded": sum(v.startswith(("NOT_VALIDATED", "NOT_GRADED")) for v in vals),
                         "coverage_pct": round(100 * sum(v not in ("", "None", UNAVAILABLE) and not v.startswith("NOT_") for v in vals) / len(rows), 2) if rows else 0})
    goal_rows = []
    for item in trace:
        goal_rows.append({
            **fixture_context(item),
            "fixture_id": item.get("fixture_id", ""), "selected_id": item.get("selected_id", ""),
            "home_team_id": item.get("archive_home_team_id", ""),
            "away_team_id": item.get("archive_away_team_id", ""),
            "home_last5_n": item.get("home_form_n", ""), "away_last5_n": item.get("away_form_n", ""),
            "home_last5_form": item.get("home_form", ""), "away_last5_form": item.get("away_form", ""),
            "home_last5_goals_scored_avg": item.get("home_form_gf_avg", ""),
            "home_last5_goals_conceded_avg": item.get("home_form_ga_avg", ""),
            "home_last5_total_goals_avg": round(float(item.get("home_form_gf_avg") or 0) + float(item.get("home_form_ga_avg") or 0), 2) if item.get("home_form_gf_avg") not in ("", None) and item.get("home_form_ga_avg") not in ("", None) else "",
            "away_last5_goals_scored_avg": item.get("away_form_gf_avg", ""),
            "away_last5_goals_conceded_avg": item.get("away_form_ga_avg", ""),
            "away_last5_total_goals_avg": round(float(item.get("away_form_gf_avg") or 0) + float(item.get("away_form_ga_avg") or 0), 2) if item.get("away_form_gf_avg") not in ("", None) and item.get("away_form_ga_avg") not in ("", None) else "",
            "home_at_home_sample_n": item.get("home_at_home_form_n", ""),
            "home_at_home_form": item.get("home_at_home_form", ""),
            "home_at_home_goals_scored_avg": item.get("home_at_home_avg_goals_for", ""),
            "home_at_home_goals_conceded_avg": item.get("home_at_home_avg_goals_against", ""),
            "away_away_sample_n": item.get("away_away_form_n", ""),
            "away_away_form": item.get("away_away_form", ""),
            "away_away_goals_scored_avg": item.get("away_away_avg_goals_for", ""),
            "away_away_goals_conceded_avg": item.get("away_away_avg_goals_against", ""),
            "home_overall_form_source_fixture_ids": item.get("home_form_source_fixture_ids", ""),
            "away_overall_form_source_fixture_ids": item.get("away_form_source_fixture_ids", ""),
            "home_venue_form_source_fixture_ids": item.get("home_at_home_source_fixture_ids", ""),
            "away_venue_form_source_fixture_ids": item.get("away_away_source_fixture_ids", ""),
            "home_btts_historical_rate_pct": item.get("home_form_btts_rate", ""),
            "away_btts_historical_rate_pct": item.get("away_form_btts_rate", ""),
            "home_over15_historical_rate_pct": item.get("home_form_over15_rate", ""),
            "away_over15_historical_rate_pct": item.get("away_form_over15_rate", ""),
            "home_over25_historical_rate_pct": item.get("home_form_over25_rate", ""),
            "away_over25_historical_rate_pct": item.get("away_form_over25_rate", ""),
            "home_under45_historical_rate_pct": item.get("home_form_under45_rate", ""),
            "away_under45_historical_rate_pct": item.get("away_form_under45_rate", ""),
            "home_team_over15_historical_rate_pct": item.get("home_team_over15_rate", ""),
            "away_team_over15_historical_rate_pct": item.get("away_team_over15_rate", ""),
            "home_clean_sheet_rate_pct": item.get("home_clean_sheet_rate", ""),
            "away_clean_sheet_rate_pct": item.get("away_clean_sheet_rate", ""),
            "home_failed_to_score_rate_pct": item.get("home_failed_to_score_rate", ""),
            "away_failed_to_score_rate_pct": item.get("away_failed_to_score_rate", ""),
            "h2h_n": item.get("h2h_n", ""), "h2h_scope": item.get("h2h_scope", ""),
            "h2h_meetings_detail": item.get("h2h_meetings_detail", ""),
            "evidence_label": "HISTORICAL_EMPIRICAL_RATE_NOT_PREDICTION_PROBABILITY",
            "history_cutoff_utc": item.get("history_cutoff_utc", "")
        })
    add_sheet("Goal Intelligence",
        ["Fixture Date", "League", "Fixture", "fixture_id", "selected_id", "home_team_id", "away_team_id", "home_last5_n", "away_last5_n",
         "home_last5_form", "away_last5_form",
         "home_last5_goals_scored_avg", "home_last5_goals_conceded_avg", "home_last5_total_goals_avg",
         "away_last5_goals_scored_avg", "away_last5_goals_conceded_avg", "away_last5_total_goals_avg",
         "home_at_home_sample_n", "home_at_home_form", "home_at_home_goals_scored_avg", "home_at_home_goals_conceded_avg",
         "away_away_sample_n", "away_away_form", "away_away_goals_scored_avg", "away_away_goals_conceded_avg",
         "home_overall_form_source_fixture_ids", "away_overall_form_source_fixture_ids",
         "home_venue_form_source_fixture_ids", "away_venue_form_source_fixture_ids",
         "home_btts_historical_rate_pct", "away_btts_historical_rate_pct",
         "home_over15_historical_rate_pct", "away_over15_historical_rate_pct",
         "home_over25_historical_rate_pct", "away_over25_historical_rate_pct",
         "home_under45_historical_rate_pct", "away_under45_historical_rate_pct",
         "home_team_over15_historical_rate_pct", "away_team_over15_historical_rate_pct",
         "home_clean_sheet_rate_pct", "away_clean_sheet_rate_pct",
         "home_failed_to_score_rate_pct", "away_failed_to_score_rate_pct",
         "h2h_n", "h2h_scope", "h2h_meetings_detail", "evidence_label", "history_cutoff_utc"], goal_rows)
    goal_market_rows = [dict(item) for item in (goal_market_rows or [])]
    for item in goal_market_rows:
        key = (
            str(item.get("provider_season_id") or "").strip(),
            str(item.get("fixture_id") or "").strip(),
            str(item.get("home_team_id") or "").strip(),
            str(item.get("away_team_id") or "").strip(),
        )
        context = fixture_context(trace_by_exact_key[key]) if all(key) and key in trace_by_exact_key else {
            "Fixture Date": "NOT_AVAILABLE_EXACT_IDENTITY_CONTEXT_JOIN",
            "League": "NOT_AVAILABLE_EXACT_IDENTITY_CONTEXT_JOIN",
            "Fixture": "NOT_AVAILABLE_EXACT_IDENTITY_CONTEXT_JOIN",
        }
        for field, value in context.items():
            if item.get(field) in (None, ""):
                item[field] = value
    goal_market_headers = list(dict.fromkeys(
        ["Fixture Date", "League", "Fixture"] + (
            list(dict.fromkeys(k for r in goal_market_rows for k in r)) or
            ["fixture_id", "forecast_status", "forecast_label", "model_id",
             "production_eligible", "betting_eligible"]
        )
    ))
    add_sheet("Goal Market Research", goal_market_headers, goal_market_rows)
    add_sheet("Market Data Coverage",
        ["field", "fixture_rows", "populated_rows", "not_available_from_oracle_output",
         "not_validated_or_not_graded", "coverage_pct"], coverage)
    archive_summary = archive_summary or {}
    raw_counts = archive_summary.get("field_nonempty_counts", {})
    archive_total = archive_summary.get("archive_match_records", 0)
    archive_coverage = [{
        "raw_source_field": field, "records_with_value": count,
        "archive_match_records": archive_total,
        "coverage_pct": round(100 * count / archive_total, 2) if archive_total else 0,
        "interpretation": "Field presence only; not proof of pre-kickoff availability or valid semantics."
    } for field, count in sorted(raw_counts.items(), key=lambda item: item[0].casefold())]
    add_sheet("Archive Field Coverage",
        ["raw_source_field", "records_with_value", "archive_match_records", "coverage_pct", "interpretation"],
        archive_coverage)
    definitions = [
        {"term": "Market probability", "definition": "Only raw supported Oracle runtime probabilities are predictions. Unsupported markets remain unavailable; empirical rates are not forecasts."},
        {"term": "Historical H2H", "definition": "Prior completed meetings for the exact stable team-ID pair within the same explicit provider competition ID, strictly before fixture kickoff. Falls back to exact season when competition ID is absent."},
        {"term": "Team form", "definition": "Latest completed fixtures for the exact stable team ID within the same explicit provider competition; strict pre-kickoff cutoff. Venue splits are home-at-home and away-away."},
        {"term": "League position", "definition": "Reconstructed within exact provider season using conventional 3-1-0 points and provisional tie-break order; not official where competition rules are unverified."},
        {"term": "Evidence risk", "definition": "Coverage and provenance gaps only; not probability of losing or match outcome."},
        {"term": "Fixture orientation", "definition": "The exact current-snapshot no_home_away flag is displayed as received. Flag 1 means no home/away distinction; it is not automatically a neutral-venue label. Affected home/away-oriented markets are review-required; probabilities are not changed."},
        {"term": "Runtime feature support", "definition": "The source runtime's 20-feature support status and recent-five feature-complete side counts are shown separately from score-complete form recomputed for descriptive reporting. The report must never use score-only counts to override a runtime block."},
        {"term": "Eligibility", "definition": "All Selected-50 report rows remain production_eligible=false and betting_eligible=false."}
    ]
    add_sheet("Definitions & Governance", ["term", "definition"], definitions)
    if league_coverage_rows is not None:
        add_sheet("50-League Coverage", COVERAGE_HEADERS, league_coverage_rows)
    if coverage_summary_rows is not None:
        add_sheet("Coverage Audit Summary", ["Metric", "Value", "Interpretation"], coverage_summary_rows)
    if xg_provenance_rows is not None:
        add_sheet("xG Provenance Decision", ["Control", "Finding", "Decision / implication"], xg_provenance_rows)
    wb.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runtime-report", required=True)
    ap.add_argument("--archive-audit", required=True, help="Directory containing match_field_audit.csv")
    ap.add_argument("--schedule-coverage", required=True, help="Runtime schedule coverage CSV proving the full governed league universe")
    ap.add_argument("--runtime-provenance", required=True)
    ap.add_argument("--snapshot-candidate-trace", required=True,
                    help="Exact snapshot candidate trace included in the verified runtime artifact")
    ap.add_argument("--archive-summary", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--expected-league-groups", type=int, default=50)
    ap.add_argument("--runtime-artifact-id", default="", help="Verified GitHub Actions artifact ID for the runtime report")
    ap.add_argument("--goal-market-research", required=False, help="Experimental goal-market research CSV; never production probabilities")
    args = ap.parse_args()
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    runtime_rows = read_csv(args.runtime_report)
    archive_rows = read_csv(Path(args.archive_audit) / "match_field_audit.csv")
    schedule_rows = read_csv(args.schedule_coverage)
    runtime_provenance = json.loads(Path(args.runtime_provenance).read_text(encoding="utf-8"))
    archive_summary = json.loads(Path(args.archive_summary).read_text(encoding="utf-8"))
    snapshot_rows = read_csv(args.snapshot_candidate_trace)
    goal_market_rows = read_csv(args.goal_market_research) if args.goal_market_research else []
    snapshot_orientation_by_key, snapshot_orientation_qa = build_snapshot_orientation_map(
        runtime_rows, snapshot_rows, runtime_provenance, archive_summary
    )
    runtime_feature_block_rows, runtime_feature_block_qa = build_runtime_feature_block_audit(runtime_rows)

    # Persist diagnostics before enforcing the candidate release gates so failed
    # runs still upload exact orientation and feature-block evidence.
    (out_dir / "oracle_selected50_snapshot_orientation_qa.json").write_text(
        json.dumps(snapshot_orientation_qa, indent=2) + "\\n", encoding="utf-8"
    )
    (out_dir / "oracle_selected50_runtime_feature_block_audit_qa.json").write_text(
        json.dumps(runtime_feature_block_qa, indent=2) + "\\n", encoding="utf-8"
    )
    write_csv(out_dir / "oracle_selected50_runtime_feature_block_audit.csv",
              runtime_feature_block_rows,
              ["Fixture Date", "League", "Fixture", "fixture_id", "selected_id",
               "provider_season_id", "team_side", "team_provider_id",
               "recent5_feature_complete_n", "team_side_history_gate",
               "missing_required_features", "feature_support_status",
               "prediction_block_reason", "production_eligible", "betting_eligible"])
    orientation_rows = []
    for item in runtime_rows:
        key = runtime_key(item)
        orientation = snapshot_orientation_by_key.get(key, {})
        orientation_rows.append({
            "Fixture Date": item.get("date_utc", ""),
            "League": item.get("league", ""),
            "Fixture": f"{item.get('home_team', '')} vs {item.get('away_team', '')}",
            "fixture_id": item.get("fixture_id", ""),
            "selected_id": item.get("selected_id", ""),
            "provider_season_id": item.get("provider_season_id", ""),
            "home_team_id": item.get("home_team_provider_id", ""),
            "away_team_id": item.get("away_team_provider_id", ""),
            **orientation,
            "production_eligible": "NO",
            "betting_eligible": "NO",
        })
    write_csv(out_dir / "oracle_selected50_fixture_orientation_audit.csv", orientation_rows,
              ["Fixture Date", "League", "Fixture", "fixture_id", "selected_id",
               "provider_season_id", "home_team_id", "away_team_id",
               "snapshot_no_home_away_flag", "fixture_orientation_status",
               "home_away_market_review_status", "snapshot_row_number",
               "snapshot_retrieved_utc", "snapshot_file_sha256",
               "production_eligible", "betting_eligible"])
    require_snapshot_orientation_qa(snapshot_orientation_qa)
    require_runtime_feature_block_audit(runtime_feature_block_rows, runtime_feature_block_qa)

    runtime_report_sha256 = hashlib.sha256(Path(args.runtime_report).read_bytes()).hexdigest()
    if runtime_provenance.get("runtime_report_sha256") != runtime_report_sha256:
        raise SystemExit("FAIL: runtime report does not match its provenance SHA-256")
    if runtime_provenance.get("source_archive_sha256") != archive_summary.get("archive_sha256"):
        raise SystemExit("FAIL: runtime provenance and archive feature audit refer to different archives")
    governed_ids = {str(r.get("selected_id") or "").strip() for r in schedule_rows if str(r.get("selected_id") or "").strip()}
    report_ids = {str(r.get("selected_id") or "").strip() for r in runtime_rows if str(r.get("selected_id") or "").strip()}
    if len(schedule_rows) != args.expected_league_groups or len(governed_ids) != args.expected_league_groups:
        raise SystemExit(f"FAIL: governed schedule coverage must contain exactly {args.expected_league_groups} unique selected IDs")
    if not report_ids.issubset(governed_ids):
        raise SystemExit("FAIL: runtime report contains selected IDs outside the governed 50-league schedule")
    report, trace, summary = build_report(runtime_rows, archive_rows)
    xg_audit_rows = build_xg_audit(runtime_rows, archive_rows, trace)
    xg_audit_counts = {
        "fixture_rows": len(xg_audit_rows),
        "exact_identity_rows": sum(r["join_status"] == "PASS_EXACT_COMPOSITE_IDENTITY" for r in xg_audit_rows),
        "blocked_or_quarantined_identity_rows": sum(r["join_status"] != "PASS_EXACT_COMPOSITE_IDENTITY" for r in xg_audit_rows),
        "rows_with_home_xg_numeric": sum(r["home_xg_numeric"] not in ("", "NOT_AVAILABLE", None) for r in xg_audit_rows),
        "rows_with_away_xg_numeric": sum(r["away_xg_numeric"] not in ("", "NOT_AVAILABLE", None) for r in xg_audit_rows),
        "rows_with_total_xg_numeric": sum(r["total_xg_numeric"] not in ("", "NOT_AVAILABLE", None) for r in xg_audit_rows),
        "rows_with_verified_capture_time": sum(bool(r["capture_time_utc"]) and r["capture_time_utc"] != "NOT_AVAILABLE" for r in xg_audit_rows),
        "prediction_eligible_rows": sum(r["prediction_eligible"] == "YES" for r in xg_audit_rows),
        "policy": "AUDIT_ONLY_UNTIL_POINT_IN_TIME_CAPTURE_AND_REVISION_PROVENANCE_VERIFIED"
    }
    fixture_league_groups = summary["selected_league_groups"]
    summary["fixture_league_groups"] = fixture_league_groups
    summary["selected_league_groups"] = len(governed_ids)
    summary["selected_ids_without_fixture_rows_in_runtime_horizon"] = sorted(governed_ids - report_ids)
    summary["selected_ids_with_fixture_rows_in_runtime_horizon"] = sorted(report_ids)
    trace_by_id = defaultdict(list)
    for item in trace:
        trace_by_id[str(item.get("selected_id") or "")].append(item)
    league_fixture_coverage = []
    for item in sorted(schedule_rows, key=lambda x: str(x.get("selected_id") or "")):
        sid = str(item.get("selected_id") or "").strip()
        league_trace = trace_by_id.get(sid, [])
        league_fixture_coverage.append({
            "selected_id": sid,
            "country": item.get("country", ""),
            "competition_name": item.get("competition_name", ""),
            "runtime_fixture_rows": sum(1 for r in runtime_rows if str(r.get("selected_id") or "").strip() == sid),
            "exact_archive_joins": sum(1 for r in league_trace if r.get("join_status") == "PASS_EXACT_SEASON_FIXTURE_ORDERED_TEAM_IDS"),
            "quarantined_rows": sum(1 for r in league_trace if r.get("join_status") != "PASS_EXACT_SEASON_FIXTURE_ORDERED_TEAM_IDS" or r.get("schedule_reconciliation_status") == "REVIEW_REQUIRED"),
            "schedule_discordance_rows": sum(1 for r in league_trace if r.get("schedule_reconciliation_status") == "REVIEW_REQUIRED"),
            "schedule_coverage_status": item.get("schedule_coverage_status", ""),
        })
    column_status_counts = {}
    for header in HEADERS:
        values = [str(r.get(header, "")) for r in report]
        column_status_counts[header] = {
            "nonempty": sum(v not in ("", "None") for v in values),
            "empty": sum(v in ("", "None") for v in values),
            "not_available_from_oracle_output": sum(v == UNAVAILABLE for v in values),
            "not_validated": sum(v.startswith("NOT_VALIDATED") for v in values),
            "not_graded": sum(v.startswith("NOT_GRADED") for v in values),
        }
    fixture_dates = sorted(r.get("date_utc", "") for r in runtime_rows if r.get("date_utc"))
    summary.update({
        "runtime_run_id": runtime_provenance.get("runtime_run_id"),
        "runtime_commit_sha": runtime_provenance.get("runtime_commit_sha"),
        "runtime_ref": runtime_provenance.get("runtime_ref"),
        "runtime_report_sha256": runtime_report_sha256,
        "source_archive_sha256": archive_summary.get("archive_sha256"),
        "archive_match_records": archive_summary.get("archive_match_records"),
        "archive_season_folders": archive_summary.get("season_folders"),
        "provider_api_calls": archive_summary.get("provider_api_calls"),
        "fixture_cutoff_range_utc": {"first": fixture_dates[0] if fixture_dates else None, "last": fixture_dates[-1] if fixture_dates else None},
        "history_cutoff_rule": "STRICTLY_BEFORE_EACH_FIXTURE_KICKOFF_UTC",
        "league_fixture_coverage": league_fixture_coverage,
        "column_status_counts": column_status_counts,
        "schema_status": "PASS_38_COLUMNS" if len(HEADERS) == 38 else "FAIL_SCHEMA",
        "headers": HEADERS,
        "production_eligible": False, "betting_eligible": False,
        "production_model_logic_changed": False, "production_probabilities_changed": False,
        "probability_policy": "BTTS, DC_HOME and DC_AWAY copied unchanged from runtime CSV; all other probability/market fields explicitly unavailable.",
        "combo_policy": "Combo probabilities remain masked; no combo output is synthesized.",
        "historical_accuracy_status": "NOT_VALIDATED",
        "standings_policy": "Provisional conventional 3-1-0 table within exact provider season ID; special competition tie-breaks/formats not verified.",
        "history_scope": "Team form and H2H use explicit provider_competition_id where present with exact stable team IDs and strict pre-kickoff cutoffs; tables remain exact provider-season scoped. Provider competition IDs may themselves be season-scoped; cross-season coverage is measured from actual source and target season IDs, not inferred from the scope label.",
        "risk_policy": "Evidence coverage gap score only; not outcome risk or probability of losing.",
        "minimum_expected_league_groups": args.expected_league_groups,
        "league_group_gate": "PASS" if summary["selected_league_groups"] == args.expected_league_groups and report_ids.issubset(governed_ids) else "FAIL",
        "column_nonempty_counts": {h: sum(1 for r in report if r.get(h) not in ("", None)) for h in HEADERS},
        "required_join_gate": "PASS" if summary["unmatched_or_quarantined_rows"] == 0 and summary["duplicate_archive_composite_keys"] == 0 else "BLOCKED",
        "schedule_reconciliation_gate": "REVIEW_REQUIRED" if summary.get("schedule_discordance_rows", 0) else "PASS",
        "all_rows_research_only": True,
        "report_status": "PASS_RESEARCH_ONLY" if summary["unmatched_or_quarantined_rows"] == 0 and summary["selected_league_groups"] == args.expected_league_groups and report_ids.issubset(governed_ids) and summary.get("schedule_discordance_rows", 0) == 0 else "PARTIAL_RESEARCH_ONLY",
    })
    # Measure actual season span from H2H source records, not from the scope label.
    h2h_meetings_total = 0
    h2h_cross_season_meetings = 0
    for item in trace:
        target_season = str(item.get("archive_provider_season_id") or "")
        try:
            meetings = json.loads(item.get("h2h_meetings_detail") or "[]")
        except (TypeError, ValueError):
            meetings = []
        for meeting in meetings:
            h2h_meetings_total += 1
            if str(meeting.get("provider_season_id") or "") != target_season:
                h2h_cross_season_meetings += 1
    summary["h2h_meetings_total"] = h2h_meetings_total
    summary["h2h_cross_season_meetings_verified"] = h2h_cross_season_meetings
    summary["h2h_cross_season_verified"] = h2h_cross_season_meetings > 0
    summary["h2h_scope_policy"] = "Explicit provider competition ID; cross-season coverage only where source meeting season differs from target season."
    summary["xg_audit"] = xg_audit_counts
    summary["fixture_orientation"] = snapshot_orientation_qa
    summary["runtime_feature_block_audit"] = runtime_feature_block_qa
    summary["report_template_candidate"] = "V1.4_REPORT_ONLY_EXTENSION_PENDING_FULL_WORKFLOW_QA"
    schedule_queue = build_schedule_reconciliation_queue(trace)
    summary["schedule_reconciliation_queue_rows"] = len(schedule_queue)
    summary["schedule_reconciliation_queue_status"] = "REVIEW_REQUIRED" if schedule_queue else "PASS"
    coverage_rows = build_50_league_coverage_rows(
        schedule_rows, runtime_rows, report, trace, xg_audit_rows, goal_market_rows
    )
    if len(coverage_rows) != args.expected_league_groups:
        raise SystemExit(
            f"FAIL: 50-league coverage sheet must contain {args.expected_league_groups} unique groups; "
            f"found {len(coverage_rows)}"
        )
    coverage_ids = {str(item["Selected Season ID"]) for item in coverage_rows}
    if len(coverage_ids) != args.expected_league_groups:
        raise SystemExit("FAIL: 50-league coverage sheet has duplicate selected season IDs")
    coverage_summary_rows = build_coverage_summary_rows(
        coverage_rows, runtime_rows, report, trace, runtime_provenance,
        archive_summary, summary, xg_audit_rows, args.runtime_artifact_id
    )
    xg_provenance_rows = build_xg_provenance_rows(coverage_rows)
    summary["coverage_sheet_rows"] = len(coverage_rows)
    summary["coverage_sheet_unique_selected_ids"] = len(coverage_ids)
    summary["coverage_sheet_status"] = "PASS_50_UNIQUE_SELECTED_SEASON_IDS"

    write_csv(out_dir / "oracle_selected50_50_league_coverage.csv", coverage_rows, COVERAGE_HEADERS)
    write_csv(out_dir / "oracle_selected50_market_intelligence.csv", report, HEADERS)
    write_csv(out_dir / "oracle_selected50_market_intelligence_evidence_trace.csv", trace,
              list(dict.fromkeys(k for r in trace for k in r)))
    quarantined = [r for r in trace if r.get("join_status") != "PASS_EXACT_SEASON_FIXTURE_ORDERED_TEAM_IDS" or r.get("schedule_reconciliation_status") == "REVIEW_REQUIRED"]
    write_csv(out_dir / "oracle_selected50_market_intelligence_join_quarantine.csv", quarantined,
              list(dict.fromkeys(k for r in quarantined for k in r)) or ["fixture_id", "join_status"])
    write_csv(out_dir / "oracle_selected50_xg_evidence_audit.csv", xg_audit_rows, XG_AUDIT_HEADERS)
    write_csv(out_dir / "oracle_selected50_schedule_reconciliation_queue.csv",
              schedule_queue, SCHEDULE_RECONCILIATION_HEADERS)
    (out_dir / "oracle_selected50_xg_evidence_audit_qa.json").write_text(
        json.dumps(xg_audit_counts, indent=2) + "\n", encoding="utf-8"
    )
    write_xlsx(out_dir / "oracle_selected50_market_intelligence.xlsx", report, trace,
               archive_summary, goal_market_rows, xg_audit_rows, coverage_rows,
               coverage_summary_rows, xg_provenance_rows,
               runtime_rows=runtime_rows,
               snapshot_orientation_by_key=snapshot_orientation_by_key)
    (out_dir / "oracle_selected50_market_intelligence_qa.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: summary[k] for k in (
        "runtime_rows", "report_rows", "exact_archive_joins", "unmatched_or_quarantined_rows",
        "selected_league_groups", "duplicate_archive_composite_keys", "schema_status",
        "league_group_gate", "required_join_gate", "production_eligible", "betting_eligible"
    )}, indent=2))
    if summary["schema_status"] != "PASS_38_COLUMNS":
        raise SystemExit("FAIL: report schema contract")
    if summary["league_group_gate"] != "PASS":
        raise SystemExit("FAIL: selected 50-league completeness gate")
    if summary["required_join_gate"] != "PASS":
        raise SystemExit("FAIL: exact archive join or duplicate-key gate")


if __name__ == "__main__":
    main()
