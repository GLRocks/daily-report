import re

with open('/root/.openclaw/workspace/daily_report_2026-06-02.html', 'r') as f:
    html = f.read()

# Remove "日涨跌" column header from S5
html = html.replace('<th>日涨跌</th>', '<th>趋势</th>')

with open('/root/.openclaw/workspace/daily_report_2026-06-02.html', 'w') as f:
    f.write(html)

print("Replaced 日涨跌 with 趋势 in S5")
