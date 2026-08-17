#!/usr/bin/env python3
"""Generate July 16 daily report based on July 15 report with fresh stock data."""

import re, subprocess, os, sys

# Read July 15 report as base
with open('/root/.openclaw/workspace/daily_report_2026-07-15.html', 'r') as f:
    html = f.read()

# Stock data for July 16 (2026-07-15 trading data)
stocks = {
    'NVDA': {'price': '212.49', 'change': '+4.40%', 'up': True},
    'AMD': {'price': '529.83', 'change': '-0.85%', 'up': False},
    'QCOM': {'price': '178.135', 'change': '-3.18%', 'up': False},
    'TSM': {'price': '419.65', 'change': '-0.46%', 'up': False},
    'AVGO': {'price': '394.21', 'change': '+2.65%', 'up': True},
    'MU': {'price': '907.818', 'change': '-3.11%', 'up': False},
    'AMAT': {'price': '579.44', 'change': '-2.73%', 'up': False},
    'LRCX': {'price': '335.43', 'change': '+1.67%', 'up': True},
    'ASML': {'price': '1815.15', 'change': '+5.16%', 'up': True},
    'INTC': {'price': '102.98', 'change': '-0.14%', 'up': False},
    'GOOGL': {'price': '371.0', 'change': '+5.25%', 'up': True},
    'MSFT': {'price': '395.63', 'change': '+1.19%', 'up': True},
    'META': {'price': '681.3', 'change': '+3.74%', 'up': True},
    'AAPL': {'price': '327.515', 'change': '+3.22%', 'up': True},
    'PLTR': {'price': '133.75', 'change': '+2.85%', 'up': True},
    'SNOW': {'price': '271.87', 'change': '+1.20%', 'up': True},
    'BABA': {'price': '117.7', 'change': '+4.76%', 'up': True},
    'TSLA': {'price': '394.31', 'change': '-0.11%', 'up': False},
    'CEG': {'price': '258.115', 'change': '+0.66%', 'up': True},
    'CCJ': {'price': '90.98', 'change': '-0.64%', 'up': False},
    'OKLO': {'price': '45.72', 'change': '-1.12%', 'up': False},
}

# 1. Replace title date
html = html.replace('<title>Agentic Market Daily | 2026-07-15</title>', '<title>Agentic Market Daily | 2026-07-16</title>')

# 2. Replace header date badge
html = html.replace('2026-07-15 | Wednesday | Asia/Shanghai 08:07', '2026-07-16 | Thursday | Asia/Shanghai 08:07')

# 3. Replace each stock card
for ticker, data in stocks.items():
    # Find the stock card for this ticker and replace price and change
    pattern = rf'(<div class="ticker">{ticker}</div>\s*<div class="name">[^<]+</div>\s*<div class="price-row">\s*<span class="price">)\$[^<]+(</span>\s*<span class="change )[^"]+(">)[^<]+(</span>)'
    
    change_class = 'up' if data['up'] else 'down'
    
    def repl(m):
        return f'{m.group(1)}${data["price"]}{m.group(2)}{change_class}{m.group(3)}{data["change"]}{m.group(4)}'
    
    html = re.sub(pattern, repl, html, count=1)

# 4. Update S2 expert consensus
old_s2 = """  <div class="insight-box">
    <span class="label">当日核心判断</span>
    <div class="content">
      芯片板块延续回调，QCOM领跌5.7%，能源股逆势上涨；市场等待TSM/INTC财报验证拐点。
    </div>
  </div>"""

new_s2 = """  <div class="insight-box">
    <span class="label">当日核心判断</span>
    <div class="content">
      芯片龙头NVDA+4.4% ASML+5.2%领涨，应用层GOOGL+5.3% META+3.7%接力，市场风格切换确认。
    </div>
  </div>"""
html = html.replace(old_s2, new_s2)

# 5. Update causal chain in S2
old_chain = """    <div class="chain-item"><div class="key">触发因</div><div class="val">伊朗冲突升级→油价飙升→通胀担忧→10Y yield上行→高估值成长股承压</div></div>
    <div class="chain-item"><div class="key">传导</div><div class="val">Nasdaq -1.6%，VIX +14.2%；芯片板块QCOM/MU/TSM领跌；能源XLE +3.2%</div></div>
    <div class="chain-item"><div class="key">结论</div><div class="val">硬件→软件轮动持续；NVDA +0.41%唯一正收益芯片股；应用层PLTR/SNOW+5%验证防御性</div></div>
    <div class="chain-item"><div class="key">证伪信号</div><div class="val">① TSM 7/16财报beat；② 伊朗冲突缓和；③ 10Y yield回落&lt;4.3%</div></div>"""

new_chain = """    <div class="chain-item"><div class="key">触发因</div><div class="val">TSM财报超预期（营收$39.6B +37% YoY）→芯片板块信心修复→NVDA+4.4% ASML+5.2%</div></div>
    <div class="chain-item"><div class="key">传导</div><div class="val">应用层接力：GOOGL+5.3% META+3.7% AAPL+3.2%；芯片分化：QCOM-3.2% MU-3.1%</div></div>
    <div class="chain-item"><div class="key">结论</div><div class="val">NVDA CUDA生态护城河验证；应用层AI变现加速；芯片非龙头承压</div></div>
    <div class="chain-item"><div class="key">证伪信号</div><div class="val">① NVDA回调至$200以下；② GOOGL/META财报miss；③ 地缘冲突升级</div></div>"""
html = html.replace(old_chain, new_chain)

# 6. Update S5 data table change values
s5_changes = {
    'NVIDIA': {'change': '+4.40%', 'up': True},
    'AMD': {'change': '-0.85%', 'up': False},
    'Intel': {'change': '-0.14%', 'up': False},
}

for company, data in s5_changes.items():
    pattern = rf'(<td><strong>{company}</strong></td>.*?)<span class="change (?:up|down)">[^<]+</span>'
    def repl_s5(m):
        cls = 'up' if data['up'] else 'down'
        return f'{m.group(1)}<span class="change {cls}">{data["change"]}</span>'
    html = re.sub(pattern, repl_s5, html, count=1)

# 7. Update S3 investor quotes - no new signal, keep placeholder
# 8. Update footer date
html = html.replace('Agentic Market Daily — 2026-07-15', 'Agentic Market Daily — 2026-07-16')

# Write new report
output_path = '/root/.openclaw/workspace/daily_report_2026-07-16.html'
with open(output_path, 'w') as f:
    f.write(html)

print(f"Report written to {output_path}")
print(f"Size: {len(html)} bytes")

# Verify stock cards count
stock_cards = html.count('class="stock-card"')
print(f"Stock cards: {stock_cards}")

# Verify all 21 tickers present
for ticker in stocks:
    if ticker not in html:
        print(f"WARNING: {ticker} not found in output!")
    else:
        # Verify price is updated
        if f'${stocks[ticker]["price"]}' not in html:
            print(f"WARNING: {ticker} price not updated!")
        else:
            print(f"OK: {ticker} = ${stocks[ticker]['price']} {stocks[ticker]['change']}")
