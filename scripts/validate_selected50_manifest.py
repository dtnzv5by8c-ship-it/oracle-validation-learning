import csv
from pathlib import Path

p = Path(__file__).resolve().parents[1] / 'data' / 'oracle-footystats-selected-50-season-id-manifest.csv'
with p.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
ids = [r.get('selected_id', '').strip() for r in rows]
assert len(rows) == 50, f'Expected 50 rows; found {len(rows)}'
assert all(ids), 'Blank selected_id found'
assert len(set(ids)) == 50, 'Duplicate selected_id found'
print('PASS: selected-50 manifest has exactly 50 unique, nonblank season IDs')
