#!/usr/bin/env python3
"""Workflow entrypoint retained for compatibility; runs the bounded current-fixture probe.

The prior 50-call season-identity reconciliation is already recorded in the report and
crosswalk. This entrypoint now performs only one league-matches request per selected season.
"""
import runpy
runpy.run_path("scripts/oracle_selected50_current_fixture_probe.py", run_name="__main__")
