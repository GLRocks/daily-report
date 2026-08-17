#!/usr/bin/env python3
"""Fix remaining issues in the report."""
import shutil

# Read the report
with open('/root/.openclaw/workspace/daily_report_2026-07-07.html', 'r') as f:
    html = f.read()

# Fix 1: Add missing closing </div> for the 核心张力 insight-box in S2
# Find the pattern where </div> is missing before the next insight-box
old = '''    </div>
  
  <div class="insight-box">
    <span class="label">因果链速览</span>'''
new = '''    </div>
  </div>

  <div class="insight-box">
    <span class="label">因果链速览</span>'''
html = html.replace(old, new)

# Fix 2: Copy stock CSV to expected location
csv_src = '/root/.openclaw/workspace/all_stocks_2026-07-07.csv'
csv_dst = '/root/.openclaw/workspace/daily_report_2026-07-07_stocks.csv'
shutil.copy(csv_src, csv_dst)

# Fix 3: Fix AMAT/LRCX rating inconsistency in S1 weekly core signals
# The S1 text says BUY for AMAT/LRCX but they should be SPEC BUY
html = html.replace(
    'AMAT/LRCX=BUY（恐慌筹码）',
    'AMAT/LRCX=SPEC BUY（恐慌筹码）'
)

# Write back
with open('/root/.openclaw/workspace/daily_report_2026-07-07.html', 'w') as f:
    f.write(html)

print("Fixes applied")
print(f"Closing div fix: {'  </div>\\n\\n  <div class=\"insight-box\">' in html}")
print(f"CSV copied: {csv_dst}")
print(f"AMAT/LRCX rating fixed: {'SPEC BUY' in html}")
