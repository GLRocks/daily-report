#!/usr/bin/env python3
"""Generate V12 daily report for 2026-07-04 using template replacement."""
import re
from datetime import datetime

# Stock data: close from API 2026-07-02, change% from Yahoo Finance where available
STOCKS = [
    ("NVDA", "NVIDIA Corporation", "BUY", "芯片", 194.97, -1.39),
    ("AMD", "Advanced Micro Devices", "HOLD", "芯片", 515.88, -4.26),
    ("QCOM", "Qualcomm Inc.", "HOLD", "芯片", 176.37, -3.12),
    ("TSM", "Taiwan Semiconductor", "BUY", "芯片", 434.72, -2.27),
    ("AVGO", "Broadcom Inc.", "BUY", "芯片", 360.22, -2.41),
    ("MU", "Micron Technology", "HOLD", "芯片", 975.76, -5.49),
    ("AMAT", "Applied Materials", "HOLD", "芯片", 602.02, 0.0),
    ("LRCX", "Lam Research", "HOLD", "芯片", 350.14, 0.0),
    ("ASML", "ASML Holding", "BUY", "芯片", 1768.16, 0.0),
    ("INTC", "Intel Corporation", "SPEC BUY", "芯片", 120.41, -5.25),
    ("GOOGL", "Alphabet Inc.", "BUY", "应用", 360.40, -0.36),
    ("MSFT", "Microsoft Corp.", "BUY", "应用", 390.82, 1.62),
    ("META", "Meta Platforms", "BUY", "应用", 583.54, -4.90),
    ("AAPL", "Apple Inc.", "BUY", "应用", 308.86, 4.84),
    ("PLTR", "Palantir Technologies", "SPEC BUY", "应用", 129.54, 2.84),
    ("SNOW", "Snowflake Inc.", "HOLD", "应用", 260.02, -2.45),
    ("BABA", "Alibaba Group", "HOLD", "应用", 96.22, 0.0),
    ("TSLA", "Tesla Inc.", "HOLD", "应用", 394.08, -7.49),
    ("CEG", "Constellation Energy", "BUY", "能源", 239.53, 0.0),
    ("CCJ", "Cameco Corp.", "SPEC BUY", "能源", 96.54, 0.0),
    ("OKLO", "Oklo Inc.", "SPEC BUY", "能源", 52.37, 0.0),
]

with open('/root/.openclaw/workspace/agentic_market_daily_template_v12.html') as f:
    template = f.read()

# 1. Update title and date
report = template.replace('Agentic Market Daily | 2026-05-15', 'Agentic Market Daily | 2026-07-04')
report = report.replace('2026-05-15 | Wednesday | Asia/Shanghai 08:07', '2026-07-04 | Saturday | Asia/Shanghai 08:07')

# 2. Generate stock cards and replace between <div class="stock-grid"> and </div> before Section 2
cards_html = []
for ticker, name, badge, cat, close, change in STOCKS:
    change_str = f"{change:+.2f}%"
    change_class = "up" if change >= 0 else "down"
    price_str = f"${close:.2f}"
    badge_class = badge.lower().replace(" ", "")
    
    card = f'''    <div class="stock-card{' highlight-stock' if ticker == 'NVDA' else ''}">
      <span class="rec-badge {badge_class}">{badge}</span>
      <span class="cat-badge">{cat}</span>
      <div class="ticker">{ticker}</div>
      <div class="name">{name}</div>
      <div class="price-row">
        <span class="price">{price_str}</span>
        <span class="change {change_class}">{change_str}</span>
      </div>
    </div>'''
    cards_html.append(card)

# Find and replace stock grid content
stock_grid_pattern = r'(<div class="stock-grid">)(.*?)(\s+</div>\s+</div>\s+<!-- Section 2)'
stock_grid_replacement = r'\1\n' + '\n'.join(cards_html) + r'\n  </div>\n</div>\n<!-- Section 2'

report = re.sub(stock_grid_pattern, stock_grid_replacement, report, flags=re.DOTALL)

# 3. Insert S2 专家共识 section after S1 and before current S2 (which will become S3)
# The current S2 is "投资人及权威机构最新论点" which should be S3
s2_expert_section = '''
<!-- Section 2: Expert Consensus -->
<div class="section">
  <div class="section-title"><span class="num">2</span> 专家共识（跨领域）</div>
  
  <div class="insight-box">
    <span class="label">当日核心判断</span>
    <div class="content">
      <p>假期清淡，AI双巨头（Anthropic/OpenAI）密集申报IPO，芯片板块短期承压但中期AI基建逻辑不变。</p>
    </div>
  </div>
  
  <div class="causal-chain">
    <div class="chain-title">因果链速览</div>
    <div class="chain-item">
      <span class="key">触发因：</span>
      <span class="val">Anthropic $965B/OpenAI $852B IPO申报，H1全球风投43%集中AI</span>
    </div>
    <div class="chain-item">
      <span class="key">传导：</span>
      <span class="val">流动性预期→估值锚定→芯片需求再确认</span>
    </div>
    <div class="chain-item">
      <span class="key">结论：</span>
      <span class="val">中期看好AI基建链，短期关注流动性拐点</span>
    </div>
    <div class="chain-item">
      <span class="key">证伪信号：</span>
      <span class="val">IPO定价低于区间下限或延迟上市</span>
    </div>
  </div>
  
  <div class="data-table">
    <table>
      <thead><tr><th>维度</th><th>判断</th><th>置信度</th><th>关键支撑板块</th></tr></thead>
      <tbody>
        <tr><td>技术趋势</td><td>AI infra需求持续</td><td>🟢</td><td>S4/S5</td></tr>
        <tr><td>投资行为</td><td>避险情绪升温</td><td>🟡</td><td>S1/S11</td></tr>
        <tr><td>风险预警</td><td>IPO窗口收窄</td><td>🔴</td><td>S2/S12</td></tr>
        <tr><td>时间窗口</td><td>7月中旬前观察</td><td>🟡</td><td>S1/S5</td></tr>
      </tbody>
    </table>
  </div>
</div>
'''

# Insert after S1 closing </div>
report = report.replace(
    '<!-- Section 2: Investor Quotes -->',
    s2_expert_section + '\n<!-- Section 3: Investor Quotes -->'
)

# 4. Update section numbers: current S2->S3, S3->S4, etc.
# First, fix the S2 title since we renamed it
# The template's S2 already exists but we renamed it to S3 in the comment, now update the actual title
# Actually we need to renumber all sections after the insertion

# Renumber sections: S3->S4, S4->S5, etc.
# Current S2 (Investor Quotes) should become S3
for i in range(13, 1, -1):  # From 13 down to 2
    old_num = f'<span class="num">{i}</span>'
    new_num = f'<span class="num">{i+1}</span>'
    report = report.replace(old_num, new_num, 1)  # Replace only first occurrence (the section title)

# 5. Write judgment file
with open('/root/.openclaw/workspace/today_judgment.txt', 'w') as f:
    f.write('假期清淡，IPO密集申报，芯片短期承压但中期逻辑不变')

# 6. Write report
output_path = '/root/.openclaw/workspace/daily_report_2026-07-04.html'
with open(output_path, 'w') as f:
    f.write(report)

print(f"Report generated: {output_path}")
print(f"Size: {len(report)} bytes")
print(f"Stock cards: {len(cards_html)}")
