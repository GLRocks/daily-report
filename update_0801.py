#!/usr/bin/env python3
"""Update July 31 report to August 1 with new stock prices"""
import re

# Stock data from 2026-07-31 close
stocks = {
    'NVDA': {'price': 201.86, 'change': 6.24, 'cat': '芯片', 'rec': 'BUY'},
    'AMD': {'price': 478.13, 'change': 11.31, 'cat': '芯片', 'rec': 'BUY'},
    'QCOM': {'price': 147.85, 'change': -5.03, 'cat': '芯片', 'rec': 'HOLD'},
    'TSM': {'price': 404.22, 'change': 7.89, 'cat': '芯片', 'rec': 'BUY'},
    'AVGO': {'price': 390.09, 'change': 5.34, 'cat': '芯片', 'rec': 'BUY'},
    'MU': {'price': 826.96, 'change': 11.90, 'cat': '芯片', 'rec': 'BUY'},
    'AMAT': {'price': 508.58, 'change': 16.53, 'cat': '芯片', 'rec': 'BUY'},
    'LRCX': {'price': 294.00, 'change': 16.50, 'cat': '芯片', 'rec': 'BUY'},
    'ASML': {'price': 1630.22, 'change': 5.13, 'cat': '芯片', 'rec': 'BUY'},
    'INTC': {'price': 90.44, 'change': 10.45, 'cat': '芯片', 'rec': 'BUY'},
    'GOOGL': {'price': 356.33, 'change': 5.83, 'cat': '应用', 'rec': 'BUY'},
    'MSFT': {'price': 465.10, 'change': 19.09, 'cat': '应用', 'rec': 'BUY'},
    'META': {'price': 556.50, 'change': -4.97, 'cat': '应用', 'rec': 'HOLD'},
    'AAPL': {'price': 309.03, 'change': -8.62, 'cat': '应用', 'rec': 'HOLD'},
    'PLTR': {'price': 123.24, 'change': 0.20, 'cat': '应用', 'rec': 'SPEC BUY'},
    'SNOW': {'price': 293.18, 'change': -1.65, 'cat': '应用', 'rec': 'HOLD'},
    'BABA': {'price': 122.25, 'change': 6.28, 'cat': '应用', 'rec': 'HOLD'},
    'TSLA': {'price': 311.11, 'change': 4.29, 'cat': '应用', 'rec': 'HOLD'},
    'CEG': {'price': 262.75, 'change': -0.31, 'cat': '能源', 'rec': 'BUY'},
    'CCJ': {'price': 86.38, 'change': -2.10, 'cat': '能源', 'rec': 'BUY'},
    'OKLO': {'price': 38.83, 'change': -5.50, 'cat': '能源', 'rec': 'SPEC BUY'},
}

with open('/root/.openclaw/workspace/daily_report_2026-07-31.html', 'r') as f:
    html = f.read()

# Update title and date
html = html.replace('Agentic Market Daily | 2026-07-31', 'Agentic Market Daily | 2026-08-01')
html = html.replace('2026-07-31 | Friday | Asia/Shanghai 08:07', '2026-08-01 | Saturday | Asia/Shanghai 08:07')
html = html.replace('Generated: 2026-07-31 08:07 CST', 'Generated: 2026-08-01 08:07 CST')

# Update stock prices - match each stock card and update price + change
for ticker, data in stocks.items():
    price = data['price']
    change = data['change']
    change_class = 'up' if change >= 0 else 'down'
    change_str = f'+{change:.2f}%' if change >= 0 else f'{change:.2f}%'
    
    # Find the stock card for this ticker and update its price/change
    # Pattern: ticker followed by name, then price-row with price and change
    pattern = rf'(<div class="ticker">{ticker}</div>\s*<div class="name">[^<]+</div>\s*<div class="price-row">\s*<span class="price">)\$[\d.,]+(</span>\s*<span class="change )[\w]+(">)[+-]?[\d.]+%(</span>)'
    repl = rf'\1${price:.2f}\2{change_class}\3{change_str}\4'
    html = re.sub(pattern, repl, html)
    
    # Also update in S5 table if present
    table_pattern = rf'(<td><strong>{ticker}</strong></td>.*?<td><span class="change )[\w]+(">)[+-]?[\d.]+%(</span></td>)'
    table_repl = rf'\1{change_class}\2{change_str}\3'
    html = re.sub(table_pattern, table_repl, html, flags=re.DOTALL)

# Update S2 core judgment for Saturday (weekend, no new signals)
old_judgment = 'MSFT Azure+43%业绩超预期暴涨15%，META利润miss跌9%，芯片分化AMD领涨6.8%。'
new_judgment = '周六休市无新信号，周五芯片全线反弹AMD+11%/MU+12%，MSFT财报后涨19%领跑。'
html = html.replace(old_judgment, new_judgment)

# Update S2 causal chain trigger
old_trigger = 'MSFT FY2026 Q4财报：营收$90B（+18% YoY），Azure增速+43%，EPS $4.74 vs 共识$4.24；META Q2：营收beat但EPS $6.18 vs $7.22 miss，capex指引上调'
new_trigger = '周六市场休市，沿用周五收盘数据。MSFT FY2026 Q4财报后续影响：Azure+43%验证云AI商业化，股价+19%'
html = html.replace(old_trigger, new_trigger)

# Write output
with open('/root/.openclaw/workspace/daily_report_2026-08-01.html', 'w') as f:
    f.write(html)

# Write judgment file
with open('/root/.openclaw/workspace/today_judgment.txt', 'w') as f:
    f.write(new_judgment)

print('HTML generated: /root/.openclaw/workspace/daily_report_2026-08-01.html')
print(f'Judgment: {new_judgment}')
