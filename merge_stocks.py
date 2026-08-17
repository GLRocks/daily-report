#!/usr/bin/env python3
import csv

files = [
    '/root/.openclaw/workspace/daily_report_2026-08-07_stocks.csv',
    '/root/.openclaw/workspace/stocks_batch2_2026-08-07.csv',
    '/root/.openclaw/workspace/stocks_batch3_2026-08-07.csv',
    '/root/.openclaw/workspace/stocks_batch4_2026-08-07.csv',
    '/root/.openclaw/workspace/stocks_batch5_2026-08-07.csv',
    '/root/.openclaw/workspace/stocks_batch6_2026-08-07.csv',
    '/root/.openclaw/workspace/stocks_batch7_2026-08-07.csv',
]

all_rows = []
for f in files:
    try:
        with open(f, 'r') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                all_rows.append(row)
    except Exception as e:
        print(f"Skip {f}: {e}")

outfile = '/root/.openclaw/workspace/daily_report_2026-08-07_stocks.csv'
with open(outfile, 'w', newline='') as fh:
    if all_rows:
        writer = csv.DictWriter(fh, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)
        print(f"Wrote {len(all_rows)} rows")
        for r in all_rows:
            print(f"{r.get('ts_code')}: close={r.get('close')} pct_change={r.get('pct_change')}")
