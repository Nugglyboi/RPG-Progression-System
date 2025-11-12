import csv
import sys
from pathlib import Path

p = Path('data/output.csv')
if not p.exists():
    print('data/output.csv not found', file=sys.stderr)
    sys.exit(2)

with p.open(newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    try:
        header = next(reader)
    except StopIteration:
        print('empty csv')
        sys.exit(0)

    # find GearScore column (case-sensitive in header sample)
    try:
        gs_idx = header.index('GearScore')
    except ValueError:
        print('GearScore column not found in header:', header)
        sys.exit(1)

    prev = None
    prev_rownum = None
    decreases = []
    rownum = 1  # header was row 1; data starts at 2
    for row in reader:
        rownum += 1
        if gs_idx >= len(row):
            # weird row, skip
            continue
        val = row[gs_idx].strip()
        if val == '':
            continue
        try:
            cur = int(val)
        except Exception:
            # try float then int
            try:
                cur = int(float(val))
            except Exception:
                # non-numeric, skip
                continue
        if prev is not None and cur < prev:
            decreases.append((prev_rownum, prev, rownum, cur, row))
        prev = cur
        prev_rownum = rownum

    if not decreases:
        print('No GearScore decreases found in data/output.csv')
        sys.exit(0)

    print(f'Found {len(decreases)} GearScore decrease(s):')
    for pr, pv, r, cv, row in decreases:
        print(f'  row {pr} -> {r}: {pv} -> {cv}')
        # print the row for context (trim long rows)
        print('    next_row_preview:', row[:10])

    # exit non-zero so caller knows there are decreases
    sys.exit(3)
