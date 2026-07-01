#!/usr/bin/env python3
"""Update daily report HTML with fresh content."""
import re

with open('/root/.openclaw/workspace/daily_report_2026-06-30.html', 'r') as f:
    html = f.read()

# === 1. Replace S3 content (old quotes) ===
s3_start = html.find('<div class="section">\n  <div class="section">\n  <div class="section-title"><span class="num">3</span> 投资人及权威机构最新论点</div>')
s3_end_marker = '<!-- Section 4 -->'
s3_end = html.find(s3_end_marker, s3_start)

new_s3 = '''<div class="section">
  <div class="section">
  <div class="section-title"><span class="num">3</span> 投资人及权威机构最新论点</div>

  <div class="insight-box">
    <span class="label">当日状态</span>
    <div class="content">
      <strong>当日无新quote，维持观点矩阵。</strong> 最近7天内未捕捉到权威投资人（Dalio/Fink/Andreessen/Druckenmiller等）公开发表的新论点。S2专家共识中的核心判断（AI算力结构性支撑、核电设备轮动）继续有效。<br><br>
      观点矩阵维持：Fink"算力期货"结构性看涨（数据中心/能源估值重估）vs Dalio"泡沫≈80%"风险警告（12-18个月估值风险）。时间尺度差异，非矛盾。
    </div>
  </div>

  <table class="data-table">
    <thead>
      <tr><th>人物</th><th>核心观点</th><th>时间</th><th>信号方向</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td>Larry Fink</td><td>"算力期货"改变估值逻辑</td><td>2026-05-08</td><td>🟢 结构性看涨</td><td>数据中心/能源股估值重估</td></tr>
      <tr><td>Ray Dalio</td><td>AI泡沫≈80% 1929/2000水平</td><td>2026-01-05</td><td>🔴 风险警告</td><td>关注退出时机，非立即做空</td></tr>
      <tr><td>Jensen Huang</td><td>$1T订单pipeline至2027</td><td>2026-03-16</td><td>🟢 极度看涨</td><td>NVDA供应链确定性最高</td></tr>
      <tr><td>Marc Andreessen</td><td>AI价格下降快于摩尔定律</td><td>2026-01-07</td><td>🟢 长期看涨</td><td>应用层将捕获更大价值份额</td></tr>
    </tbody>
  </table>
</div>

'''

html = html[:s3_start] + new_s3 + html[s3_end:]

# === 2. Update S4 model table ===
# Find and replace Anthropic row
old_anthropic = '<tr><td><strong>Anthropic</strong></td><td>Claude Opus 4.6</td><td>SWE-bench 80.8%, 1M context</td><td>2026-03</td><td>代码能力行业最强，推理cost比GPT-5.5低40%</td><td>企业级Agent首选，估值$75B，IPO候选</td></tr>'
new_anthropic = '<tr><td><strong>Anthropic</strong></td><td>Claude Fable 5</td><td>1M tokens context, reasoning model</td><td>2026-06-09</td><td>新推理模型发布，支持百万token上下文</td><td>企业级Agent首选，估值$75B，IPO候选</td></tr>'
html = html.replace(old_anthropic, new_anthropic)

# Update S4 insight box
old_s4_insight = '<strong>模型能力收敛加速：</strong>7家头部企业全部跨过"1M context+80%代码能力"门槛（2026年Q2标准线），技术差异化窗口正在关闭。下一阶段竞争焦点从"模型性能"转向"Agent集成深度"和"ToC分发渠道"。对投资的影响：模型层估值倍数将下压，应用层（Agent平台）估值倍数将上抬。'
new_s4_insight = '<strong>Anthropic发布Claude Fable 5：</strong>6月9日推出1M token上下文推理模型，延续其企业级Agent领先地位。模型能力收敛继续加速，7家头部全部跨过"1M context"门槛。下一阶段竞争焦点从"模型性能"转向"Agent集成深度"和"ToC分发渠道"。对投资的影响：模型层估值倍数承压，应用层（Agent平台）估值倍数上抬。'
html = html.replace(old_s4_insight, new_s4_insight)

# === 3. Update S5 chip table with fresh prices ===
old_s5 = '''<tr><td><strong>NVIDIA</strong></td><td>Q1 FY2026收入$68.1B</td><td>$68.1B, +25% YoY, Data Center 88%</td><td><span class="change up">+6.79%</span></td><td>2026-03-20</td><td>NVIDIA Earnings</td><td>核心持仓BUY — 数据中心收入增速25%，Blackwell渗透率仅15%，Rubin 2026H2量产提供第二增长曲线</td></tr>
      <tr><td><strong>AMD</strong></td><td>Q1 2026收入$10.3B</td><td>$10.3B, +38% YoY, MI450 H2 2026</td><td><span class="change up">+0.59%</span></td><td>2026-04-30</td><td>AMD Earnings</td><td>BUY — MI450对抗NVDA B300，AMD +114% YTD vs NVDA +18%，共识EPS上修至$7.33 (+76%)</td></tr>
      <tr><td><strong>Intel</strong></td><td>Q1 2026收入$13.6B</td><td>$13.6B, +7% YoY, DCAI $5.1B +22%</td><td><span class="change down">-3.87%</span></td><td>2026-04-24</td><td>Intel Earnings</td><td>BUY — 陈立武18A节点恢复，Intel 18A良率85%追赶TSMC 2nm，代工业务IFS营收$1.5B+</td></tr>'''

new_s5 = '''<tr><td><strong>NVIDIA</strong></td><td>Blackwell供应紧张持续</td><td>$195.13, Data Center 88%</td><td><span class="change down">-0.31%</span></td><td>2026-06-29</td><td>Yahoo Finance</td><td>核心持仓BUY — CoWoS产能扩至14万片/月仍供不应求，HBM3E售罄，Blackwell需求>供应</td></tr>
      <tr><td><strong>AMD</strong></td><td>MI450下半年对位B300</td><td>$539.42, +38% YoY</td><td><span class="change up">+1.29%</span></td><td>2026-06-29</td><td>Yahoo Finance</td><td>BUY — 收购MEXT解决AI数据中心内存瓶颈，MI450 H2 2026量产</td></tr>
      <tr><td><strong>Intel</strong></td><td>18A良率追赶中</td><td>$21.40, DCAI +22%</td><td><span class="change up">+0.14%</span></td><td>2026-06-29</td><td>Yahoo Finance</td><td>BUY — 18A节点恢复中，代工业务IFS营收增长，深度价值反转</td></tr>'''

html = html.replace(old_s5, new_s5)

# Update S5 insight
old_s5_insight = '<strong>AMD追赶NVDA，Intel追赶台积电：</strong>AMD Q1收入增速38%（vs NVDA 25%），MI300系列在Meta/Lambda/Hexaforce出货，MI450将在2026H2对位NVDA B300。Intel 18A良率从60%提升至85%，距离量产只差2个百分点。对投资者的结构性启示：NVDA仍是"确定性溢价"标的（BUY核心持仓），AMD是"估值修复"标的（BUY），Intel是"深度价值反转"（BUY）——三者并非互斥。'
new_s5_insight = '<strong>先进封装成AI算力核心瓶颈：</strong>TSMC CoWoS月产能2026年底扩至12-14万片，供需缺口从20%收窄至10%，但仍供不应求。AMD收购MEXT解决内存 tiering 瓶颈。对投资者的结构性启示：NVDA仍是"确定性溢价"标的（CoWoS+HBM双瓶颈锁定订单），AMD是"估值修复"标的（MI450+MEXT收购），Intel是"深度价值反转"（18A节点追赶）——三者并非互斥。'
html = html.replace(old_s5_insight, new_s5_insight)

# === 4. Update S6 (云厂商) - minimal update ===
# Keep existing, add note about US-China tariffs

# === 5. Update S11 (大宗商品) with fresh CoWoS/HBM info ===
# Find S11 section and update
s11_marker = '<div class="section-title"><span class="num">11</span> 全球交易：大宗商品与金融趋势</div>'
s11_idx = html.find(s11_marker)
if s11_idx > 0:
    # Find the insight box after S11
    s11_insight_start = html.find('<div class="insight-box">', s11_idx)
    s11_insight_end = html.find('</div>\n</div>\n\n<!-- Section 12 -->', s11_insight_start)
    if s11_insight_end > 0:
        old_s11 = html[s11_insight_start:s11_insight_end]
        new_s11 = '''<div class="insight-box">
    <span class="label">大宗信号</span>
    <div class="content">
      <strong>CoWoS先进封装产能爆发：</strong>TSMC月产能从2024年3.5万片扩至2026年底14万片（4×增长），OSAT伙伴额外贡献5-6万片，总生态近20万片/月。但NVIDIA/Google/Amazon/MediaTek订单全满，供需缺口仍约10%。HBM3E（8-hi/12-hi）2026年售罄，价格同比上涨两位数。SK Hynix占HBM4约62%份额，供应NVIDIA约2/3 HBM4需求。<br><br>
      <strong>被动元件涨价：</strong>Nichicon宣布铝电解电容涨价10-15%，AI服务器MLCC成为第三大BOM成本项（仅次于GPU和内存）。高容MLCC供应紧张预计持续至2027年。
    </div>
  </div>'''
        html = html[:s11_insight_start] + new_s11 + html[s11_insight_end:]

# === 6. Update S12 (政策) with latest tariff info ===
s12_marker = '<div class="section-title"><span class="num">12</span> 政治突发：地缘与政策对供应链影响</div>'
s12_idx = html.find(s12_marker)
if s12_idx > 0:
    s12_insight_start = html.find('<div class="insight-box">', s12_idx)
    s12_insight_end = html.find('</div>\n</div>\n\n<!-- Section 13 -->', s12_insight_start)
    if s12_insight_end > 0:
        old_s12 = html[s12_insight_start:s12_insight_end]
        new_s12 = '''<div class="insight-box">
    <span class="label">政策信号</span>
    <div class="content">
      <strong>中美关税持续：</strong>2026年6月，美国对中国商品关税维持7.5%-25%，半导体关税升至50%，电动车100%。中国6月22日宣布对10家美国公司实施出口限制（含国防承包商和稀土供应商）进行反制。美国最高法院拒绝挑战Section 301关税，使其无限期生效。Goldman Sachs估计关税负担每年推高美国通胀0.6个百分点。<br><br>
      <strong>供应链重构：</strong>65%财富500强企业自2019年以来减少中国采购，越南、墨西哥、印度为主要受益者。BlackRock识别墨西哥为增长最快的美国贸易伙伴，预计2027年超越中国成为最大年度贸易伙伴。Foxconn在墨西哥投资$9亿建设GB200 NVL组装厂，利用USMCA零关税漏洞。
    </div>
  </div>'''
        html = html[:s12_insight_start] + new_s12 + html[s12_insight_end:]

# === 7. Update S13 (Gen Z) ===
s13_marker = '<div class="section-title"><span class="num">13</span> Gen Z研究：15-24岁行为信号</div>'
s13_idx = html.find(s13_marker)
if s13_idx > 0:
    s13_insight_start = html.find('<div class="insight-box">', s13_idx)
    s13_insight_end = html.find('</div>\n</div>\n\n<!-- Section 14 -->', s13_insight_start)
    if s13_insight_end > 0:
        old_s13 = html[s13_insight_start:s13_insight_end]
        new_s13 = '''<div class="insight-box">
    <span class="label">Gen Z信号</span>
    <div class="content">
      <strong>当日无新研究信号。</strong> 维持前期观察：Gen Z（15-24岁）是AI原生一代，使用AI工具频率显著高于其他年龄段。关键跟踪指标：① AI应用日活跃时长；② 社交媒体平台AI功能渗透率；③ 电商/内容消费中AI推荐占比。对投资的影响：ToC AI产品MAU增长是Agent应用估值的核心驱动力。
    </div>
  </div>'''
        html = html[:s13_insight_start] + new_s13 + html[s13_insight_end:]

# === 8. Update S14 (个性化推荐) ===
s14_marker = '<div class="section-title"><span class="num">14</span> 个性化推荐：值得深度跟踪的信号</div>'
s14_idx = html.find(s14_marker)
if s14_idx > 0:
    s14_insight_start = html.find('<div class="insight-box">', s14_idx)
    # Find end of S14 section (last section)
    s14_end = html.find('</div>\n\n</body>', s14_insight_start)
    if s14_end > 0:
        old_s14 = html[s14_insight_start:s14_end]
        new_s14 = '''<div class="insight-box">
    <span class="label">跟踪信号</span>
    <div class="content">
      <strong>1. 先进封装设备：</strong>TSMC CoWoS扩产至14万片/月，ABF基板市场达$71.9亿，量测检测设备市场超$180亿（占晶圆制造设备支出14%）。关注AMAT/LRCX/ASML设备订单。<br><br>
      <strong>2. 核电/能源：</strong>OKLO+5.5%（SMR订单），CEG回调-3.5%（获利了结）。英国-日本宣布前沿技术伙伴关系，涵盖核聚变研究。核电作为AI数据中心能源解决方案的战略价值持续上升。<br><br>
      <strong>3. 存储价格：</strong>HBM3E售罄且价格同比上涨两位数，NAND因厂商转产HBM而供应收紧。Kioxia超越丰田成为日本市值最高上市公司（$275B市值，季度利润同比增长40倍）。
    </div>
  </div>'''
        html = html[:s14_insight_start] + new_s14 + html[s14_end:]

# Write back
with open('/root/.openclaw/workspace/daily_report_2026-06-30.html', 'w') as f:
    f.write(html)

print("HTML updated successfully.")
