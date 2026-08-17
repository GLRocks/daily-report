#!/usr/bin/env python3
import re

stocks = {
    'NVDA': {'close': 224.14, 'pct': 3.03, 'prev_close': 217.52, 'prev_pct': -2.88},
    'AMD': {'close': 483.07, 'pct': 2.88, 'prev_close': 474.14, 'prev_pct': -1.91},
    'QCOM': {'close': 162.91, 'pct': 0.46, 'prev_close': 162.66, 'prev_pct': 0.30},
    'TSM': {'close': 428.80, 'pct': 2.47, 'prev_close': 422.56, 'prev_pct': 0.60},
    'AVGO': {'close': 416.05, 'pct': -1.50, 'prev_close': 416.22, 'prev_pct': -2.70},
    'MU': {'close': 912.32, 'pct': 5.96, 'prev_close': 868.58, 'prev_pct': -1.02},
    'AMAT': {'close': 548.66, 'pct': 5.08, 'prev_close': 525.49, 'prev_pct': -2.53},
    'LRCX': {'close': 326.37, 'pct': 6.52, 'prev_close': 311.41, 'prev_pct': 0.02},
    'ASML': {'close': 1810.06, 'pct': 4.42, 'prev_close': 1799.90, 'prev_pct': 3.38},
    'INTC': {'close': 100.95, 'pct': 3.52, 'prev_close': 97.79, 'prev_pct': -3.80},
    'GOOGL': {'close': 343.54, 'pct': -3.91, 'prev_close': 343.70, 'prev_pct': -2.99},
    'MSFT': {'close': 492.43, 'pct': -2.69, 'prev_close': 503.78, 'prev_pct': 0.76},
    'META': {'close': 578.85, 'pct': -2.70, 'prev_close': 599.21, 'prev_pct': 1.20},
    'AAPL': {'close': 301.88, 'pct': -2.07, 'prev_close': 304.78, 'prev_pct': -2.65},
    'PLTR': {'close': 171.11, 'pct': -2.35, 'prev_close': 175.04, 'prev_pct': 1.76},
    'SNOW': {'close': 333.26, 'pct': -0.26, 'prev_close': 334.27, 'prev_pct': -0.13},
    'BABA': {'close': 125.22, 'pct': -5.37, 'prev_close': 127.95, 'prev_pct': -0.36},
    'TSLA': {'close': 327.45, 'pct': -1.04, 'prev_close': 332.80, 'prev_pct': 1.28},
    'CEG': {'close': 278.68, 'pct': 3.05, 'prev_close': 278.36, 'prev_pct': 2.93},
    'CCJ': {'close': 99.03, 'pct': 0.30, 'prev_close': 98.73, 'prev_pct': 1.46},
    'OKLO': {'close': 45.11, 'pct': 1.39, 'prev_close': 47.01, 'prev_pct': 5.66},
}

with open('/root/.openclaw/workspace/daily_report_2026-08-12.html', 'r') as f:
    html = f.read()

# Update title and date
html = html.replace('Agentic Market Daily | 2026-08-12', 'Agentic Market Daily | 2026-08-13')
html = html.replace('2026-08-12 | Wednesday | Asia/Shanghai 08:07 | 数据日期: 2026-08-11',
                    '2026-08-13 | Thursday | Asia/Shanghai 08:07 | 数据日期: 2026-08-12')

# Update stock prices using regex for precise matching
for ticker, data in stocks.items():
    close = data['close']
    pct = data['pct']
    prev_close = data['prev_close']
    prev_pct = data['prev_pct']
    
    # Build old and new price strings
    old_price = "{:.2f}".format(prev_close)
    new_price = "{:.2f}".format(close)
    
    # Format pct strings
    if prev_pct >= 0:
        old_pct_str = "+{:.2f}%".format(prev_pct)
    else:
        old_pct_str = "{:.2f}%".format(prev_pct)
    
    if pct >= 0:
        new_pct_str = "+{:.2f}%".format(pct)
    else:
        new_pct_str = "{:.2f}%".format(pct)
    
    # Replace price - be careful with exact matches
    # Match the specific pattern in the stock card
    old_price_pattern = '<span class="price">{}</span>'.format(old_price)
    new_price_pattern = '<span class="price">{}</span>'.format(new_price)
    
    # Try exact match first, then fallback to simple replace
    if old_price_pattern in html:
        html = html.replace(old_price_pattern, new_price_pattern, 1)
    else:
        # Fallback: try with dollar sign
        old_price_pattern2 = '<span class="price">${}</span>'.format(old_price)
        new_price_pattern2 = '<span class="price">${}</span>'.format(new_price)
        if old_price_pattern2 in html:
            html = html.replace(old_price_pattern2, new_price_pattern2, 1)
    
    # Replace change percentage
    old_up = '<span class="change up">{}</span>'.format(old_pct_str)
    old_down = '<span class="change down">{}</span>'.format(old_pct_str)
    
    new_up = '<span class="change up">{}</span>'.format(new_pct_str)
    new_down = '<span class="change down">{}</span>'.format(new_pct_str)
    
    if old_up in html:
        html = html.replace(old_up, new_up if pct >= 0 else new_down, 1)
    elif old_down in html:
        html = html.replace(old_down, new_up if pct >= 0 else new_down, 1)

# Update S2 core judgment
old_judgment = """AI Agent安全事件（OpenAI Astra暂停、Anthropic沙盒逃逸、HF攻击）触发网络安全板块暴涨，资金从芯片向安全轮动。芯片板块普跌2-3%，但ASML独涨3.4%显示设备端确定性。能源股受益AI电力需求叙事持续强势。短期关注NVDA 8/26财报及OpenAI S-1披露。"""

new_judgment = """芯片板块暴力反弹，存储/设备领涨：MU+6.0% LRCX+6.5% AMAT+5.1%，资金从应用层回流算力基建。应用层普跌BABA-5.4%领跌，GOOGL/META/MSFT均跌2.7%+。能源持续强势CEG+3.1%。"""

html = html.replace(old_judgment, new_judgment)

# Update S2 causal chain
old_chain = """触发因</span>
      <span class="val">OpenAI Astra触发Critical安全阈值 + Anthropic沙盒逃逸 + HF遭AI agent攻击</span>
    </div>
    <div class="chain-item">
      <span class="key">传导</span>
      <span class="val">AI agent安全风险暴露 → 企业加速采购安全解决方案 → PANW/CRWD/PLTR受益 → 芯片资金轮动流出</span>
    </div>
    <div class="chain-item">
      <span class="key">结论</span>
      <span class="val">短期（1-2周）网络安全优于芯片；中期（1-3月）NVDA财报+OpenAI S-1将重塑估值锚</span>
    </div>
    <div class="chain-item">
      <span class="key">证伪信号</span>
      <span class="val">① 安全事件被定性为"孤立事件"而非系统性风险；② NVDA财报超预期逆转情绪；③ 美联储降息预期升温</span>"""

new_chain = """触发因</span>
      <span class="val">AI Agent安全事件后芯片板块超跌反弹，存储/设备需求预期改善</span>
    </div>
    <div class="chain-item">
      <span class="key">传导</span>
      <span class="val">芯片超跌 → 资金从应用层回流算力基建 → MU/LRCX/AMAT领涨 → 应用层BABA/GOOGL承压</span>
    </div>
    <div class="chain-item">
      <span class="key">结论</span>
      <span class="val">短期芯片优于应用层；中期NVDA 8/26财报决定方向；关注OpenAI S-1披露</span>
    </div>
    <div class="chain-item">
      <span class="key">证伪信号</span>
      <span class="val">① 芯片反弹后迅速回落；② 应用层财报超预期；③ 美联储不降息</span>"""

html = html.replace(old_chain, new_chain)

# Update S5 table prices (NVDA/AMD/INTC)
for ticker in ['NVDA', 'AMD', 'INTC']:
    data = stocks[ticker]
    old_pct = data['prev_pct']
    new_pct = data['pct']
    
    if old_pct >= 0:
        old_pct_str = "+{:.2f}%".format(old_pct)
    else:
        old_pct_str = "{:.2f}%".format(old_pct)
    
    if new_pct >= 0:
        new_pct_str = "+{:.2f}%".format(new_pct)
    else:
        new_pct_str = "{:.2f}%".format(new_pct)
    
    old_up = '<span class="change up">{}</span>'.format(old_pct_str)
    old_down = '<span class="change down">{}</span>'.format(old_pct_str)
    new_up = '<span class="change up">{}</span>'.format(new_pct_str)
    new_down = '<span class="change down">{}</span>'.format(new_pct_str)
    
    if old_up in html:
        html = html.replace(old_up, new_up if new_pct >= 0 else new_down, 1)
    elif old_down in html:
        html = html.replace(old_down, new_up if new_pct >= 0 else new_down, 1)

# Update footer
html = html.replace('数据截止: 2026-08-11 16:00 ET', '数据截止: 2026-08-12 16:00 ET')

# Write new report
with open('/root/.openclaw/workspace/daily_report_2026-08-13.html', 'w') as f:
    f.write(html)

print("Report generated successfully")

# Write today_judgment.txt
judgment = "芯片暴力反弹MU+6% LRCX+6.5%领涨，应用层普跌BABA-5.4%，资金回流算力基建。"
with open('/root/.openclaw/workspace/today_judgment.txt', 'w') as f:
    f.write(judgment)
print("Judgment written: {}".format(judgment))
print("Length: {} chars".format(len(judgment)))
