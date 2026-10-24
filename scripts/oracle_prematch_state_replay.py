#!/usr/bin/env python3
"""Research-only prematch role-state replay for reviewed, competition-scoped aliases.

This utility does not predict, alter production data, or approve fuzzy matches.
Only explicit aliases supplied by a reviewer are considered. State rows dated on
or after the fixture date are excluded to prevent temporal leakage.
"""
from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"CSV_HAS_NO_HEADER:{path}")
        return list(reader)


def role_rows(history: list[dict], league: str, label: str, role: str, fixture_date: str) -> list[dict]:
    n_col = "home_n" if role == "home_team" else "away_n"
    count = []
    for row in history:
        if row.get("league_code", "").strip() != league or row.get(role, "").strip() != label:
            continue
        date = row.get("date", "").strip()
        if not date or date >= fixture_date:
            continue
        try:
            n = float(row.get(n_col, "0") or 0)
        except ValueError:
            n = 0
        if n > 0:
            count.append(row)
    return count


def replay(fixtures: list[dict], history: list[dict], aliases: list[dict], league_map: dict[str, str] | None = None) -> list[dict]:
    # Production archive's prematch state uses league names, while fixture schedule
    # uses league codes. Translate via an explicit mapping derived from archived
    # matches; never compare code strings to league-name strings directly.
    league_map = league_map or {}
    normalized_history = []
    for row in history:
        item = dict(row)
        if not item.get("league_code"):
            item["league_code"] = next((code for code, name in league_map.items()
                                        if name == item.get("league", "").strip()), "")
        normalized_history.append(item)
    history = normalized_history
    alias_map = {}
    for a in aliases:
        key = (a.get("league_code", "").strip(), a.get("fixture_label", "").strip(), a.get("role", "").strip())
        canonical = a.get("canonical_label", "").strip()
        evidence = a.get("identity_evidence", "").strip()
        if not all(key) or not canonical or not evidence:
            raise ValueError("ALIAS_REQUIRES_LEAGUE_FIXTURE_LABEL_ROLE_CANONICAL_AND_IDENTITY_EVIDENCE")
        if key in alias_map and alias_map[key] != (canonical, evidence):
            raise ValueError(f"AMBIGUOUS_ALIAS:{key}")
        alias_map[key] = (canonical, evidence)
    output = []
    for f in fixtures:
        league, date = f.get("league_code", "").strip(), f.get("date", "").strip()
        row = {"league_code": league, "date": date, "home_team": f.get("home_team", ""),
               "away_team": f.get("away_team", ""), "before_status": f.get("before_status", "MISSING_PREMATCH_TEAM_STATE")}
        role_details, blockers = {}, []
        for role in ("home_team", "away_team"):
            original = f.get(role, "").strip()
            alias = alias_map.get((league, original, role))
            canonical = alias[0] if alias else original
            evidence = alias[1] if alias else ""
            matches = role_rows(history, league, canonical, role, date)
            role_details[role] = {"fixture_label": original, "candidate_label": canonical,
                                  "explicit_alias": bool(alias), "identity_evidence": evidence,
                                  "usable_pre_fixture_role_rows": len(matches),
                                  "latest_pre_fixture_state_date": max((x.get("date","") for x in matches), default="")}
            if not matches:
                blockers.append(f"MISSING_{role.upper()}_ROLE_STATE")
            if alias and not evidence:
                blockers.append(f"UNVERIFIED_IDENTITY_{role.upper()}")
        output.append({**f, "role_state_audit": role_details,
                       "counterfactual_status": "ELIGIBLE_FOR_REVIEW_ONLY" if not blockers else "BLOCKED",
                       "blockers": blockers,
                       "note": "Research-only eligibility signal; not a production prediction."})
    return output


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fixtures", required=True, type=Path)
    p.add_argument("--history", required=True, type=Path)
    p.add_argument("--aliases", required=True, type=Path, help="Reviewed CSV: league_code,fixture_label,role,canonical_label,identity_evidence")
    p.add_argument("--league-map", type=Path, help="Optional CSV mapping league_code,league from archived matches.csv")
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    try:
        league_map = {}
        if a.league_map:
            league_map = {row["league_code"].strip(): row["league"].strip()
                          for row in read_csv(a.league_map)}
        rows = replay(read_csv(a.fixtures), read_csv(a.history), read_csv(a.aliases), league_map)
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"status":"PASS_RESEARCH_ONLY","fixtures":len(rows),
                          "eligible_for_review_only":sum(x["counterfactual_status"]=="ELIGIBLE_FOR_REVIEW_ONLY" for x in rows),
                          "blocked":sum(x["counterfactual_status"]=="BLOCKED" for x in rows),
                          "output":str(a.output)}, indent=2))
        return 0
    except (OSError, ValueError, csv.Error) as exc:
        print(json.dumps({"status":"BLOCKED_INPUT","error":str(exc)}))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
