import re

with open('/root/.openclaw/workspace/daily_report_2026-05-14_v3.html', 'r') as f:
    html = f.read()

# Fix missing minus signs on all down changes
def fix_all_changes(match):
    direction = match.group(1)
    val = match.group(2).strip()
    if direction == 'down' and not val.startswith('-') and not val.startswith('▼'):
        return f'<span class="change down">-{val}</span>'
    return match.group(0)

html = re.sub(r'<span class="change (up|down)">([^\u003c]+)</span>', fix_all_changes, html)

with open('/root/.openclaw/workspace/daily_report_2026-05-14_v3.html', 'w') as f:
    f.write(html)

# Verify
for m in re.finditer(r'<div class="ticker">(\w+)</div>.*?<span class="price">\$([\d.]+)</span>.*?<span class="change (up|down)">([^\u003c]+)</span>', html, re.DOTALL):
    print(f"  {m.group(1)}: ${m.group(2)} {m.group(4)} ({m.group(3)})")
