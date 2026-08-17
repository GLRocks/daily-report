#!/usr/bin/env python3
"""Generate 2026-07-03 daily report from template"""

import re

# Stock data: ticker, close, pct_change, category, rec_badge
stocks = [
    ("NVDA", 194.97, -2.56, "芯片", "buy"),
    ("AMD", 515.88, -11.20, "芯片", "buy"),
    ("QCOM", 176.37, -4.56, "芯片", "hold"),
    ("TSM", 434.72, -8.97, "芯片", "buy"),
    ("AVGO", 360.22, -4.64, "芯片", "buy"),
    ("MU", 975.76, -15.47, "芯片", "buy"),
    ("AMAT", 602.02, -16.73, "芯片", "buy"),
    ("LRCX", 350.14, -19.20, "芯片", "hold"),
    ("ASML", 1768.16, -11.12, "芯片", "buy"),
    ("INTC", 120.41, -13.76, "芯片", "buy"),
    ("GOOGL", 360.40, 0.85, "应用", "buy"),
    ("MSFT", 390.82, 4.77, "应用", "buy"),
    ("META", 583.54, 3.59, "应用", "buy"),
    ("AAPL", 308.86, 6.74, "应用", "spec"),
    ("PLTR", 129.54, 11.03, "应用", "spec"),
    ("SNOW", 260.02, -0.45, "应用", "hold"),
    ("BABA", 96.22, 0.25, "应用", "hold"),
    ("TSLA", 394.08, -6.31, "应用", "hold"),
    ("CEG", 239.53, -3.56, "能源", "buy"),
    ("CCJ", 96.54, -0.87, "能源", "buy"),
    ("OKLO", 52.37, -0.15, "能源", "spec"),
]

# Reasons
reasons = {
    "NVDA": "独立日假期前资金避险，短期回调不改推理需求主线，维持BUY",
    "AMD": "单日暴跌11%，MI400出货预期受Q2财报前情绪拖累，逢低布局窗口",
    "QCOM": "独立日假期前跟随芯片板块回调，AI PC长期布局 intact",
    "TSM": "独立日假期前获利回吐，2nm量产进度 intact，先进制程垄断未变",
    "AVGO": "跟随板块回调，定制AI芯片收入$12B/年确定性不变",
    "MU": "单日暴跌15%，内存周期复苏预期受Q2财报前情绪打压，HBM3E供不应求 intact",
    "AMAT": "单日暴跌17%，独立日假期前避险情绪集中释放，先进封装设备需求 intact",
    "LRCX": "单日暴跌19%，存储设备周期复苏 intact，短期情绪超卖",
    "ASML": "独立日假期前跟随设备股回调，High-NA EUV订单积压$40B+未变",
    "INTC": "单日暴跌14%，此前YTD涨幅过大，18A工艺进度 intact，获利回吐",
    "GOOGL": "独立日假期前逆势微涨，Gemini生态+搜索AI化提供防御性",
    "MSFT": "独立日假期前逆势涨4.8%，Copilot ARR>$10B确定性最高，资金避风港",
    "META": "独立日假期前逆势涨3.6%，Llama开源战略+AI推荐引擎 intact",
    "AAPL": "独立日假期前逆势涨6.7%，iOS 27开放第三方AI预期升温",
    "PLTR": "独立日假期前逆势暴涨11%，AIP平台化+政府合同扩张，资金抱团",
    "SNOW": "微跌0.5%，Cortex AI集成 intact，数据平台AI化转型中",
    "BABA": "微涨0.3%，Qwen3商业化进展 intact，阿里云AI增速需确认",
    "TSLA": "独立日假期前跌6.3%，FSD V13延迟+Optimus量产不确定性",
    "CEG": "独立日假期前跌3.6%，核电订单积压$30B+ intact，短期获利回吐",
    "CCJ": "微跌0.9%，铀供需结构性缺口 intact，核电复兴上游杠杆未变",
    "OKLO": "微跌0.2%，小型模块化反应堆技术路线 intact，Altman背书未变",
}

# Metrics
metrics = {
    "NVDA": "市值$4.8T | P/S 32x | 毛利率75%",
    "AMD": "YTD+48% | MI400出货Q3 | 服务器CPU TAM$120B",
    "QCOM": "Q3指引$9.2-10B | Android收入减速 | AI PC布局",
    "TSM": "2nm量产2025H2 | 美国凤凰厂高量投产 | 70%先进制程市占",
    "AVGO": "定制AI芯片$12B/年 | VMware整合完成 | 毛利率80%+",
    "MU": "HBM3E量产 | DDR5供需紧 | 内存周期复苏",
    "AMAT": "BIS罚款已消化 | 中国设备收入18% | 刻蚀龙头",
    "LRCX": "刻蚀/沉积双龙头 | 存储设备周期复苏 | 毛利率47%",
    "ASML": "EUV垄断 | High-NA EUV 2028量产 | 订单$40B+",
    "INTC": "YTD+222% | 18A工艺上线 | Apple代工传闻",
    "GOOGL": "Gemini 3.1 Ultra | 云收入增速26% | 搜索AI集成",
    "MSFT": "Azure增速31% | Copilot ARR>$10B | OpenAI深度绑定",
    "META": "Llama 4开源 | Reels变现加速 | AI推荐引擎",
    "AAPL": "iOS 27开放AI | 服务端AI资本开支$10B+/年",
    "PLTR": "AIP平台增速>50% | 政府合同扩张 | 估值溢价",
    "SNOW": "Cortex AI集成 | 收入增长22% | 竞争加剧",
    "BABA": "Qwen3 MoE | 阿里云增速14% | 通义千问DAU 2500万",
    "TSLA": "FSD V13延迟 | Optimus量产2026 | 能源业务",
    "CEG": "核电重启+AI供电 | 订单$30B+ | 监管绿灯",
    "CCJ": "铀价$85/lb | 供给缺口 | 核电复兴原料",
    "OKLO": "小型模块化反应堆 | Sam Altman背书 | 早期高风险",
}

names = {
    "NVDA": "NVIDIA Corporation", "AMD": "Advanced Micro Devices",
    "QCOM": "Qualcomm Inc.", "TSM": "Taiwan Semiconductor",
    "AVGO": "Broadcom Inc.", "MU": "Micron Technology",
    "AMAT": "Applied Materials", "LRCX": "Lam Research",
    "ASML": "ASML Holding", "INTC": "Intel Corporation",
    "GOOGL": "Alphabet Inc.", "MSFT": "Microsoft Corp.",
    "META": "Meta Platforms", "AAPL": "Apple Inc.",
    "PLTR": "Palantir Technologies", "SNOW": "Snowflake Inc.",
    "BABA": "Alibaba Group", "TSLA": "Tesla Inc.",
    "CEG": "Constellation Energy", "CCJ": "Cameco Corp.",
    "OKLO": "Oklo Inc.",
}

badge_map = {"buy": "BUY", "hold": "HOLD", "spec": "SPEC BUY"}

def generate_stock_cards():
    cards = []
    for ticker, close, pct, cat, rec in stocks:
        change_class = "up" if pct >= 0 else "down"
        change_sign = "+" if pct >= 0 else ""
        highlight = " highlight-stock" if pct >= 5 or pct <= -10 else ""
        cards.append(f'''    <div class="stock-card{highlight}">
      <span class="rec-badge {rec}">{badge_map[rec]}</span>
      <span class="cat-badge">{cat}</span>
      <div class="ticker">{ticker}</div>
      <div class="name">{names[ticker]}</div>
      <div class="price-row">
        <span class="price">${close:.2f}</span>
        <span class="change {change_class}">{change_sign}{pct:.2f}%</span>
      </div>
      <div class="stock-metrics">核心指标: {metrics[ticker]}</div>
      <div class="stock-reason">推荐: {reasons[ticker]}</div>
    </div>''')
    return "\n\n".join(cards)

# Read template
with open('/root/.openclaw/workspace/agentic_market_daily_template_v12.html', 'r') as f:
    html = f.read()

# Replace date in title
html = re.sub(r'title>Agentic Market Daily \| \d{4}-\d{2}-\d{2}', 'title>Agentic Market Daily | 2026-07-03', html)

# Replace date badge
html = re.sub(r'\d{4}-\d{2}-\d{2} \| [A-Za-z]+ \| Asia/Shanghai \d{2}:\d{2}', '2026-07-03 | Friday | Asia/Shanghai 08:07', html)

# Replace all stock cards
old_cards_pattern = r'<div class="stock-card[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>'
# Actually let's be more careful - replace the entire stock-grid content
old_grid = re.search(r'<div class="stock-grid">(.*?)</div>\s*</div>', html, re.DOTALL)
if old_grid:
    new_cards = generate_stock_cards()
    html = html.replace(old_grid.group(1), "\n\n" + new_cards + "\n  ")

# Write output
with open('/root/.openclaw/workspace/daily_report_2026-07-03.html', 'w') as f:
    f.write(html)

print("Generated daily_report_2026-07-03.html")
