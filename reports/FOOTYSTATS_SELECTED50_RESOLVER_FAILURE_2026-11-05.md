# FootyStats Selected-50 Resolver Failure — 2026-11-05

Run: 41994920103
Job: 127135685829

## Root cause

The resolver executed successfully through the single FootyStats `league-list?chosen_leagues_only=false` API call, but its season-year parser used the incorrect regular expression `r'20\\\\d{2}'` in the workflow source. That pattern searches for a literal backslash sequence rather than four-digit years, so valid season labels produced no year matches and therefore no resolved season groups.

The run consequently failed closed with:

`Exact Selected-50 resolution failed: 1 league failures; resolved groups=0.`

The visible '1 league failure' is a separate catalogue-name reconciliation issue; the zero resolved groups was caused by the parser defect.

## Correction

The resolver was corrected on both `main` and `research/oracle-50-league-readiness-audit` to use:

`re.findall(r'20\\d{2}', label)`

Commits:
- main: `b76f243357cddef63bc4abc34305208d53e1aa6d`
- research: `0ee61127fe365e50610d5742b50d198a82c88b86`

## Next gate

Re-run the public Selected-50 Catalogue Resolver from `main`. This is still a single catalogue API call. Do not start private historical ingestion until the resolver reports exactly 50 selected leagues and a non-zero, complete season registry.

Oracle V1.6 production logic is unchanged.