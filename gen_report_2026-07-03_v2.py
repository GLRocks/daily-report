#!/usr/bin/env python3
"""Generate 2026-07-03 daily report with all required modifications"""

import re

stocks_data = [
    ("NVDA", 194.97, -2.56, "芯片", "buy", "NVIDIA Corporation", "市值$4.8T | P/S 32x | 毛利率75%", "独立日假期前资金避险，短期回调不改推理需求主线，维持BUY"),
    ("AMD", 515.88, -11.20, "芯片", "buy", "Advanced Micro Devices", "YTD+48% | MI400出货Q3 | 服务器CPU TAM$120B", "单日暴跌11%，MI400出货预期受Q2财报前情绪拖累，逢低布局窗口"),
    ("QCOM", 176.37, -4.56, "芯片", "hold", "Qualcomm Inc.", "Q3指引$9.2-10B | Android收入减速 | AI PC布局", "独立日假期前跟随芯片板块回调，AI PC长期布局 intact"),
    ("TSM", 434.72, -8.97, "芯片", "buy", "Taiwan Semiconductor", "2nm量产2025H2 | 美国凤凰厂高量投产 | 70%先进制程市占", "独立日假期前获利回吐，2nm量产进度 intact，先进制程垄断未变"),
    ("AVGO", 360.22, -4.64, "芯片", "buy", "Broadcom Inc.", "定制AI芯片$12B/年 | VMware整合完成 | 毛利率80%+", "跟随板块回调，定制AI芯片收入$12B/年确定性不变"),
    ("MU", 975.76, -15.47, "芯片", "buy", "Micron Technology", "HBM3E量产 | DDR5供需紧 | 内存周期复苏", "单日暴跌15%，内存周期复苏预期受Q2财报前情绪打压，HBM3E供不应求 intact"),
    ("AMAT", 602.02, -16.73, "芯片", "buy", "Applied Materials", "BIS罚款已消化 | 中国设备收入18% | 刻蚀龙头", "单日暴跌17%，独立日假期前避险情绪集中释放，先进封装设备需求 intact"),
    ("LRCX", 350.14, -19.20, "芯片", "hold", "Lam Research", "刻蚀/沉积双龙头 | 存储设备周期复苏 | 毛利率47%", "单日暴跌19%，存储设备周期复苏 intact，短期情绪超卖"),
    ("ASML", 1768.16, -11.12, "芯片", "buy", "ASML Holding", "EUV垄断 | High-NA EUV 2028量产 | 订单$40B+", "独立日假期前跟随设备股回调，High-NA EUV订单积压$40B+未变"),
    ("INTC", 120.41, -13.76, "芯片", "buy", "Intel Corporation", "YTD+222% | 18A工艺上线 | Apple代工传闻", "单日暴跌14%，此前YTD涨幅过大，18A工艺进度 intact，获利回吐"),
    ("GOOGL", 360.40, 0.85, "应用", "buy", "Alphabet Inc.", "Gemini 3.1 Ultra | 云收入增速26% | 搜索AI集成", "独立日假期前逆势微涨，Gemini生态+搜索AI化提供防御性"),
    ("MSFT", 390.82, 4.77, "应用", "buy", "Microsoft Corp.", "Azure增速31% | Copilot ARR>$10B | OpenAI深度绑定", "独立日假期前逆势涨4.8%，Copilot ARR>$10B确定性最高，资金避风港"),
    ("META", 583.54, 3.59, "应用", "buy", "Meta Platforms", "Llama 4开源 | Reels变现加速 | AI推荐引擎", "独立日假期前逆势涨3.6%，Llama开源战略+AI推荐引擎 intact"),
    ("AAPL", 308.86, 6.74, "应用", "spec", "Apple Inc.", "iOS 27开放AI | 服务端AI资本开支$10B+/年", "独立日假期前逆势涨6.7%，iOS 27开放第三方AI预期升温"),
    ("PLTR", 129.54, 11.03, "应用", "spec", "Palantir Technologies", "AIP平台增速>50% | 政府合同扩张 | 估值溢价", "独立日假期前逆势暴涨11%，AIP平台化+政府合同扩张，资金抱团"),
    ("SNOW", 260.02, -0.45, "应用", "hold", "Snowflake Inc.", "Cortex AI集成 | 收入增长22% | 竞争加剧", "微跌0.5%，Cortex AI集成 intact，数据平台AI化转型中"),
    ("BABA", 96.22, 0.25, "应用", "hold", "Alibaba Group", "Qwen3 MoE | 阿里云增速14% | 通义千问DAU 2500万", "微涨0.3%，Qwen3商业化进展 intact，阿里云AI增速需确认"),
    ("TSLA", 394.08, -6.31, "应用", "hold", "Tesla Inc.", "FSD V13延迟 | Optimus量产2026 | 能源业务", "独立日假期前跌6.3%，FSD V13延迟+Optimus量产不确定性"),
    ("CEG", 239.53, -3.56, "能源", "buy", "Constellation Energy", "核电重启+AI供电 | 订单$30B+ | 监管绿灯", "独立日假期前跌3.6%，核电订单积压$30B+ intact，短期获利回吐"),
    ("CCJ", 96.54, -0.87, "能源", "buy", "Cameco Corp.", "铀价$85/lb | 供给缺口 | 核电复兴原料", "微跌0.9%，铀供需结构性缺口 intact，核电复兴上游杠杆未变"),
    ("OKLO", 52.37, -0.15, "能源", "spec", "Oklo Inc.", "小型模块化反应堆 | Sam Altman背书 | 早期高风险", "微跌0.2%，小型模块化反应堆技术路线 intact，Altman背书未变"),
]

with open('/root/.openclaw/workspace/agentic_market_daily_template_v12.html', 'r') as f:
    html = f.read()

# 1. Fix date
html = html.replace('Agentic Market Daily | 2026-05-15', 'Agentic Market Daily | 2026-07-03')
html = html.replace('2026-05-15 | Wednesday | Asia/Shanghai 08:07', '2026-07-03 | Friday | Asia/Shanghai 08:07')

# 2. Replace all stock cards - find stock-grid and replace everything inside
# First, extract the stock-grid section
stock_grid_start = html.find('<div class="stock-grid">')
stock_grid_end = html.find('</div>\n</div>\n\n<!-- Section 2')
if stock_grid_end == -1:
    stock_grid_end = html.find('</div>\n</div>\n\n<!-- Section')

old_stock_section = html[stock_grid_start:stock_grid_end]

# Generate new stock cards
new_cards = []
for ticker, close, pct, cat, rec, name, metric, reason in stocks_data:
    change_class = "up" if pct >= 0 else "down"
    change_sign = "+" if pct >= 0 else ""
    highlight = " highlight-stock" if abs(pct) >= 5 else ""
    badge_text = {"buy": "BUY", "hold": "HOLD", "spec": "SPEC BUY"}[rec]
    new_cards.append(f'''    <div class="stock-card{highlight}">
      <span class="rec-badge {rec}">{badge_text}</span>
      <span class="cat-badge">{cat}</span>
      <div class="ticker">{ticker}</div>
      <div class="name">{name}</div>
      <div class="price-row">
        <span class="price">${close:.2f}</span>
        <span class="change {change_class}">{change_sign}{pct:.2f}%</span>
      </div>
      <div class="stock-metrics">核心指标: {metric}</div>
      <div class="stock-reason">推荐: {reason}</div>
    </div>''')

new_stock_section = '<div class="stock-grid">\n\n' + '\n\n'.join(new_cards) + '\n  </div>'
html = html.replace(old_stock_section, new_stock_section)

# 3. Fix section numbering - template has sections 2-13, we need 2-14 with S2=专家共识
# Insert expert consensus after S1, then shift all numbers
expert_consensus = '''<!-- Section 2: Expert Consensus -->
<div class="section">
  <div class="section-title"><span class="num">2</span> 专家共识：跨板块综合研判</div>

  <div class="insight-box">
    <span class="label">当日核心判断</span>
    <div class="content">
      <strong>芯片股独立日前恐慌性抛售，应用股资金避险分化；Q2财报季前情绪主导，基本面未变。</strong>设备股（AMAT-17%/LRCX-19%）和内存（MU-15%）领跌，反映市场对Q2 capex指引的焦虑。MSFT（+4.8%）和PLTR（+11%）逆势大涨，显示资金向AI应用确定性抱团。核电主题（CEG-3.6%）短期获利回吐但长期 intact。
    </div>
  </div>

  <div class="causal-chain">
    <div class="chain-title">因果链速览</div>
    <div class="chain-item"><div class="key">触发因</div><div class="val">独立日假期前流动性收缩 + Q2财报季临近焦虑</div></div>
    <div class="chain-item"><div class="key">传导机制</div><div class="val">避险资金撤离高beta芯片股 → 涌入低beta应用龙头（MSFT/PLTR）→ 板块分化加剧</div></div>
    <div class="chain-item"><div class="key">时间尺度</div><div class="val">短期（1-2周）：情绪波动主导；中期（1-3月）：Q2财报验证基本面</div></div>
    <div class="chain-item"><div class="key">投资预测</div><div class="val">芯片股暴跌提供逢低布局窗口，应用股抱团需警惕估值过热</div></div>
    <div class="chain-item"><div class="key">证伪信号</div><div class="val">Q2财报capex指引miss / 应用股抱团瓦解 / 地缘突发事件</div></div>
  </div>

  <table class="data-table">
    <thead>
      <tr><th>维度</th><th>技术趋势</th><th>投资行为</th><th>风险预警</th><th>时间窗口</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>技术趋势</strong></td><td>🟢 推理需求>训练（NVDA/AMD）</td><td>🟢 逢低加仓芯片BUY标的</td><td>🔴 Q2财报capex指引</td><td>7月15-25日</td></tr>
      <tr><td><strong>投资行为</strong></td><td>🟢 应用层资金避风港（MSFT/PLTR）</td><td>🟢 维持核心持仓</td><td>🟡 独立日假期流动性</td><td>即时</td></tr>
      <tr><td><strong>风险预警</strong></td><td>🔴 设备股情绪超卖（AMAT/LRCX）</td><td>🟡 警惕追高风险</td><td>🔴 板块分化加剧</td><td>1-2周</td></tr>
      <tr><td><strong>时间窗口</strong></td><td>🟢 Q2财报验证期</td><td>🟢 7月中旬布局窗口</td><td>🟡 8月FOMC</td><td>7-8月</td></tr>
    </tbody>
  </table>
</div>

'''

# Find position to insert - after S1 closing </div>
s1_end = html.find('</div>\n</div>\n\n<!-- Section 2')
if s1_end != -1:
    # Insert expert consensus and change the following section to be Section 3
    html = html[:s1_end + len('</div>\n</div>\n\n')] + expert_consensus + html[s1_end + len('</div>\n</div>\n\n'):]

# Now renumber sections 2-13 to 3-14
# Section 2 (investor quotes) -> Section 3
# Section 3 (AI unicorns) -> Section 4
# etc.
for old_num in range(13, 1, -1):
    new_num = old_num + 1
    # Replace section titles
    html = html.replace(f'<span class="num">{old_num}</span>', f'<span class="num">{new_num}</span>', 1)
    # Also fix the comment
    html = html.replace(f'<!-- Section {old_num} -->', f'<!-- Section {new_num} -->')

# Fix the investor quotes section title to be Section 3
html = html.replace('<!-- Section 2: Investor Quotes -->', '<!-- Section 3: Investor Quotes -->')
html = html.replace('<span class="num">2</span> 投资人及权威机构最新论点', '<span class="num">3</span> 投资人及权威机构最新论点', 1)

# 4. Update investor quotes - mark old quotes as historical since they're >7 days old
# Keep the quotes but add context that they're historical
# Larry Fink 5/8 > 7 days (6/26), Ray Dalio 1/5 > 7 days, etc.
# All existing quotes are >7 days old, so mark section as historical

# Find the investor quotes section and add a note
inv_section = re.search(r'(<span class="num">3</span> 投资人及权威机构最新论点.*?</div>\s*</div>)', html, re.DOTALL)
if inv_section:
    old_inv = inv_section.group(1)
    # Add note before the first quote-box
    new_inv = old_inv.replace(
        '<div class="quote-box">',
        '<div class="insight-box">\n    <span class="label">信号状态</span>\n    <div class="content">当日无新投资人quote（>7天），以下为历史观点矩阵供参考。独立日假期前市场言论清淡。</div>\n  </div>\n\n  <div class="quote-box">',
        1
    )
    html = html.replace(old_inv, new_inv)

# 5. Update S4 (AI Unicorns) - add note about no new signals
s4_section = re.search(r'(<span class="num">4</span> AI独角兽模型技术动向.*?</div>\s*</div>)', html, re.DOTALL)
if s4_section:
    old_s4 = s4_section.group(1)
    new_s4 = old_s4.replace(
        '<table class="data-table">',
        '<div class="insight-box">\n    <span class="label">信号状态</span>\n    <div class="content">当日无重大模型发布信号，以下为7家覆盖框架历史数据。等待Llama-4.1等下一代模型发布。</div>\n  </div>\n\n  <table class="data-table">',
        1
    )
    html = html.replace(old_s4, new_s4)

# 6. Update S5 (NVIDIA/AMD/Intel) - update prices and add note
s5_section = re.search(r'(<span class="num">5</span> NVIDIA / AMD / Intel.*?</div>\s*</div>)', html, re.DOTALL)
if s5_section:
    old_s5 = s5_section.group(1)
    # Update prices in the table
    new_s5 = old_s5.replace('+6.79%', '<span class="change down">-2.56%</span>')
    new_s5 = new_s5.replace('+0.59%', '<span class="change down">-11.20%</span>')
    new_s5 = new_s5.replace('-3.87%', '<span class="change down">-13.76%</span>')
    # Add note
    new_s5 = new_s5.replace(
        '<table class="data-table">',
        '<div class="insight-box">\n    <span class="label">信号状态</span>\n    <div class="content">年中财报前静默期，Q2财报将于7月中旬发布。以下为历史财报数据，股价为2026-07-02收盘。</div>\n  </div>\n\n  <table class="data-table">',
        1
    )
    html = html.replace(old_s5, new_s5)

# 7. Add no-signal notes to sections without fresh data
sections_to_mark = [
    (6, "中国云厂商AI策略", "当日无重大云厂商信号，维持阿里/腾讯/百度策略跟踪。年中财报季临近。"),
    (7, "AI Agent应用趋势", "当日无重大Agent商业化信号，维持PLTR/SNOW/Cursor跟踪。独立日假期前市场活动减少。"),
    (8, "Agent接口及生态标准化", "当日无重大协议标准进展，维持MCP/A2A跟踪。Cognition Windsurf品牌已更名为Devin Desktop（6/2）。"),
    (10, "ToC侧Agent应用及硬件部署形式", "当日无重大端侧AI硬件发布，维持N1X/骁龙X Elite跟踪。独立日假期前硬件发布清淡。"),
    (11, "全球交易：大宗商品与金融趋势", "当日无重大大宗商品价格异动，维持铜/锂/稀土跟踪。年中淡季+独立日假期。"),
    (12, "政治突发：地缘与政策对供应链影响", "当日无重大政策变动，维持BIS/EU/国务院跟踪。年中静默期。"),
    (13, "Gen Z研究：15-24岁行为信号", "当日无重大Gen Z调研发布，维持Gartner/Deloitte跟踪。调研淡季。"),
]

for num, title, note in sections_to_mark:
    pattern = f'<span class="num">{num}</span> {title}'
    if pattern in html:
        # Find the section and add note after title
        section_match = re.search(rf'(<span class="num">{num}</span> {re.escape(title)}.*?</div>\s*</div>)', html, re.DOTALL)
        if section_match:
            old_sec = section_match.group(1)
            new_sec = old_sec.replace(
                f'<span class="num">{num}</span> {title}</div>',
                f'<span class="num">{num}</span> {title}</div>\n\n  <div class="insight-box">\n    <span class="label">信号状态</span>\n    <div class="content">{note}</div>\n  </div>',
                1
            )
            html = html.replace(old_sec, new_sec)

# 8. Update S9 (Open Source) - add note
s9_section = re.search(r'(<span class="num">9</span> 开源社区技术路径深度追踪.*?</div>\s*</div>)', html, re.DOTALL)
if s9_section:
    old_s9 = s9_section.group(1)
    new_s9 = old_s9.replace(
        '<h3 style="color:var(--accent);margin:15px 0 10px;">vLLM / SGLang PR追踪（近7日）</h3>',
        '<div class="insight-box">\n    <span class="label">信号状态</span>\n    <div class="content">当日无重大开源PR发布，以下为历史PR追踪数据。vLLM/SGLang社区持续活跃。</div>\n  </div>\n\n  <h3 style="color:var(--accent);margin:15px 0 10px;">vLLM / SGLang PR追踪（近期）</h3>',
        1
    )
    html = html.replace(old_s9, new_s9)

# 9. Update S14 (Personalized) - update with today's signals
s14_section = re.search(r'(<span class="num">14</span> 个性化推荐.*?</div>\s*</div>)', html, re.DOTALL)
if s14_section:
    old_s14 = s14_section.group(1)
    new_s14 = old_s14.replace(
        '<div class="highlight-content">',
        '<div class="highlight-content">\n      <strong>🔥 2026-07-03 核心信号</strong><br>\n      <strong>1. 芯片股独立日前恐慌抛售</strong> — AMAT-17%/LRCX-19%/MU-15%领跌，反映Q2财报前焦虑。Q2财报将于7月中旬发布，capex指引是关键变量。评级：芯片BUY标的逢低布局窗口。<br><br>\n      <strong>2. 资金抱团应用确定性</strong> — MSFT+4.8%/PLTR+11%逆势大涨，显示避险情绪下资金向AI应用龙头集中。需警惕抱团估值过热风险。<br><br>\n      <strong>3. 独立日假期流动性收缩</strong> — 7月3日美股提前收盘，7月4日休市。假期后关注Q2财报季（7月15-25日）和8月FOMC。',
        1
    )
    # Remove old highlight content partially
    html = html.replace(old_s14, new_s14)

# Write output
with open('/root/.openclaw/workspace/daily_report_2026-07-03.html', 'w') as f:
    f.write(html)

print("Generated: /root/.openclaw/workspace/daily_report_2026-07-03.html")
