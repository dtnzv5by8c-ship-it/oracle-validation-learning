# FootyStats reporting-only pilot

This pilot processes FootyStats match and team CSVs into an Excel data-quality report. It is deliberately separate from Oracle production prediction logic.

## Governance
- Never commit FootyStats paid CSV data to this public repository.
- Run only against files the subscription holder is permitted to download and use.
- Current team-table league position is a current snapshot, not historical position at each prior kickoff.
- Actual match xG must never be substituted for prematch xG.
- Zero odds are treated as unavailable, not as odds or probabilities.
- Derived last-five form uses only completed matches before the target kickoff.
- The report does not change Oracle probabilities, thresholds, or production code.

## Run
Install Python with pandas, numpy, and openpyxl, extract your downloaded ZIP into a private working directory, then run:

```bash
python scripts/footystats_report_only_pilot.py --input-dir /path/to/private/extracted/files --output /path/to/private/FootyStats_QA.xlsx
```

If file names are unusual, pass explicit `--matches` and `--teams` paths. Keep input files and output reports private. This is a reporting utility; a later GitHub Actions integration must use a private data location and must not place licensed CSVs in this public repository.
