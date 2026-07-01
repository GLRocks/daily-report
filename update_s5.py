#!/usr/bin/env python3
"""更新S5表格日涨跌数据"""
with open('/root/.openclaw/workspace/daily_report_2026-06-04.html', 'r') as f:
    content = f.read()

# S5表格中的日涨跌更新
# NVDA: +6.79% → -4.26% (down)
content = content.replace(
    '<td><span class="change up">+6.79%</span></td><td>2026-03-20</td><td>NVIDIA Earnings',
    '<td><span class="change down">-4.26%</span></td><td>2026-06-03</td><td>NVIDIA Earnings'
)

# AMD: +0.59% → +6.35% (up)
content = content.replace(
    '<td><span class="change up">+0.59%</span></td><td>2026-04-30</td><td>AMD Earnings',
    '<td><span class="change up">+6.35%</span></td><td>2026-06-03</td><td>AMD Earnings'
)

# Intel: -3.87% → +2.98% (up)
content = content.replace(
    '<td><span class="change down">-3.87%</span></td><td>2026-04-24</td><td>Intel Earnings',
    '<td><span class="change up">+2.98%</span></td><td>2026-06-03</td><td>Intel Earnings'
)

with open('/root/.openclaw/workspace/daily_report_2026-06-04.html', 'w') as f:
    f.write(content)

print("S5 updated")
