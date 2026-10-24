#!/usr/bin/env python3
"""Research-only diagnostics for unresolved Oracle H2H fixture mappings.

This tool does not auto-map teams, change probabilities, or weaken quality gates.
It classifies unresolved fixture teams against the full historical archive and
emits review candidates with evidence so a human can approve only verified mappings.
"""
import argparse
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location

# Reuse the report builder canonicalizer so diagnostics and report use identical team identities.
_spec = spec_from_file_location("oracle_h2h_report_builder", Path(__file__).with_name("build_h2h_report.py"))
_builder = module_from_spec(_spec)
_spec.loader.exec_module(_builder)


def norm(value):
    return _builder.team(value)


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def diagnose(matches, unresolved, min_similarity=0.82):
    team_occurrences = defaultdict(Counter)
    team_spellings = defaultdict(Counter)
    for row in matches:
        code = (row.get("league_code") or "").strip()
        for side in ("home_team", "away_team"):
            raw = (row.get(side) or "").strip()
            key = norm(raw)
            if raw and key:
                team_occurrences[key][code] += 1
                team_spellings[key][raw] += 1

    all_keys = list(team_spellings)
    output = []
    for fixture in unresolved:
        league = (fixture.get("league") or fixture.get("league_code") or "").strip()
        date = (fixture.get("date") or "")[:10]
        home = (fixture.get("home_team") or "").strip()
        away = (fixture.get("away_team") or "").strip()
        for side, name in (("home", home), ("away", away)):
            key = norm(name)
            codes = team_occurrences.get(key, Counter())
            same_code_count = codes.get(league, 0)
            other_codes = sorted((code, count) for code, count in codes.items() if code and code != league)
            suggestions = []
            if not codes:
                for candidate_key in all_keys:
                    score = SequenceMatcher(None, key, candidate_key).ratio()
                    if score >= min_similarity:
                        for spelling, count in team_spellings[candidate_key].most_common(2):
                            suggestions.append({
                                "candidate_name": spelling,
                                "candidate_league_counts": dict(team_occurrences[candidate_key]),
                                "historical_occurrences": count,
                                "name_similarity": round(score, 3),
                                "approval_status": "UNVERIFIED_CANDIDATE_ONLY",
                            })
                suggestions.sort(key=lambda x: (-x["name_similarity"], -x["historical_occurrences"], x["candidate_name"]))
                suggestions = suggestions[:5]
            if same_code_count:
                status = "FOUND_IN_EXPECTED_LEAGUE"
            elif other_codes:
                status = "FOUND_ONLY_IN_OTHER_LEAGUE_CODES"
            elif suggestions:
                status = "POSSIBLE_NAME_ALIAS_REQUIRES_REVIEW"
            else:
                status = "NOT_FOUND_IN_ARCHIVE"
            output.append({
                "fixture_date": date,
                "league_code": league,
                "home_team": home,
                "away_team": away,
                "unresolved_team_side": side,
                "unresolved_team_name": name,
                "normalized_team_name": key,
                "diagnosis": status,
                "expected_league_occurrences": same_code_count,
                "other_league_occurrences_by_code": json.dumps(dict(other_codes), sort_keys=True),
                "review_candidates_json": json.dumps(suggestions, ensure_ascii=False, sort_keys=True),
                "mapping_approved": False,
                "scoring_eligible_from_this_diagnostic": False,
            })
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--matches", required=True)
    parser.add_argument("--unmatched", required=True)
    parser.add_argument("--out-csv", required=True)
    parser.add_argument("--out-json", required=True)
    args = parser.parse_args()
    matches = read_csv(args.matches)
    unresolved = read_csv(args.unmatched)
    rows = diagnose(matches, unresolved)
    out_csv = Path(args.out_csv)
    out_json = Path(args.out_json)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else [
            "fixture_date", "league_code", "home_team", "away_team", "unresolved_team_side",
            "unresolved_team_name", "normalized_team_name", "diagnosis", "expected_league_occurrences",
            "other_league_occurrences_by_code", "review_candidates_json", "mapping_approved",
            "scoring_eligible_from_this_diagnostic"])
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["diagnosis"] for row in rows)
    report = {
        "status": "DIAGNOSTIC_ONLY_REVIEW_REQUIRED",
        "unresolved_fixture_rows": len(unresolved),
        "unresolved_team_records": len(rows),
        "diagnosis_counts": dict(sorted(counts.items())),
        "auto_mappings_applied": 0,
        "quality_gate_changed": False,
        "production_model_changed": False,
        "probabilities_changed": False,
        "limitations": [
            "Similarity candidates are unverified and must not be used as mappings without authoritative evidence.",
            "A team appearing in another league code may reflect promotion/relegation, a code mismatch, or source coverage differences.",
            "This diagnostic does not establish season completeness, canonical fixture identity, or prediction accuracy."
        ]
    }
    out_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
