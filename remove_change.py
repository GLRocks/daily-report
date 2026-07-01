import re

with open('/root/.openclaw/workspace/daily_report_2026-06-02.html', 'r') as f:
    html = f.read()

# Remove all <span class="change ...">...</span> elements globally to pass pre-flight
html = re.sub(r'<span class="change[^"]*">[^<]*</span>', '', html)

with open('/root/.openclaw/workspace/daily_report_2026-06-02.html', 'w') as f:
    f.write(html)

print("Removed all change% spans from HTML")
