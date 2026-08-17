#!/usr/bin/env python3
"""Update report content for 2026-07-13."""
import re

with open('/root/.openclaw/workspace/daily_report_2026-07-13.html', 'r') as f:
    html = f.read()

# === S2: Expert Consensus Update ===
s2_new = '''<div class="section-title"><span class="num">2</span> 专家共识：跨板块综合研判</div>

<div class="insight-box">
  <div class="label">当日核心判断</div>
  <div class="content">
    周末密集催化：Apple诉OpenAI窃取芯片机密、Meta Iris 9月流片、SK Hynix ADR创纪录上市。硬件层叙事强于模型层，芯片/设备股优先于应用层。Q2财报季开启，关注NVDA/AMD/META指引。
  </div>
</div>

<div class="causal-chain">
  <div class="chain-title">因果链速览</div>
  <div class="chain-item"><span class="key">触发因</span>：Meta自研Iris芯片9月流片 +  hyperscaler定制芯片俱乐部完成</div>
  <div class="chain-item"><span class="key">传导</span>：Broadcom/TSMC受益，NVDA训练份额稳固但推理面临侵蚀，AVGO设计收入倍增</div>
  <div class="chain-item"><span class="key">结论</span>：AI半导体"卖铲人"逻辑持续，但需区分训练（NVDA垄断）与推理（多元化）赛道</div>
  <div class="chain-item"><span class="key">证伪信号</span>：Iris延期/性能不及预期；Q2财报数据中心收入增速跌破30%</div>
</div>

<table class="data-table">
  <thead><tr><th>维度</th><th>置信度</th><th>关键支撑板块</th></tr></thead>
  <tbody>
    <tr><td>技术趋势</td><td>🟢🟢🟡</td><td>S5芯片/S9开源/S10端侧</td></tr>
    <tr><td>投资行为</td><td>🟢🟢🟢</td><td>S1芯片持仓/S3投资人论点</td></tr>
    <tr><td>风险预警</td><td>🟡🟡🔴</td><td>S12政策/S11地缘</td></tr>
    <tr><td>时间窗口</td><td>🟢🟢🟡</td><td>Q2财报季（7月下旬）</td></tr>
  </tbody>
</table>
'''

# Find and replace S2 content
s2_start = html.find('<div class="section-title"><span class="num">2</span>')
s2_end = html.find('<div class="section-title"><span class="num">3</span>')
if s2_start > 0 and s2_end > 0:
    html = html[:s2_start] + s2_new + html[s2_end:]
    print("S2 updated")

# === S3: Investor Opinions Update ===
s3_new = '''<div class="section-title"><span class="num">3</span> 投资人及权威机构最新论点</div>

<div class="quote-box">
  <div class="quote-text">"The hyperscaler custom-silicon club is now complete. Broadcom is designing for several of these programs simultaneously, which has quietly made it the second most important company in AI silicon after Nvidia itself."</div>
  <div class="quote-source">— BuildFastWithAI Frontier Analysis, 2026-07-11</div>
  <div class="quote-context">Context: Meta Iris, Google TPUv7, Amazon Trainium, Microsoft Maia, OpenAI Jalapeno all use Broadcom design. The playbook: move inference to in-house chips, keep Nvidia for training, use internal silicon as negotiating leverage.</div>
  <div class="play-btn">▶ 播放采访片段</div>
</div>

<div class="quote-box">
  <div class="quote-text">"Price wars at the model layer are revenue growth at the chip layer. Frontier labs compete each other's margins away with weekly price cuts, while every one of those price cuts requires buying more silicon to serve more demand."</div>
  <div class="quote-source">— BuildFastWithAI Market Intelligence, 2026-07-11</div>
  <div class="quote-context">Context: GPT-5.6 Terra at $2.50/$15, Grok 4.5 at $2/$6, Gemini 3.5 Pro rumored at $1.25/$10. Model-layer price wars compress margins but drive inference volume → silicon demand.</div>
  <div class="play-btn">▶ 播放分析</div>
</div>

<div class="insight-box">
  <div class="label">核心张力框架</div>
  <div class="content">
    <strong>模型层 vs 芯片层</strong>：OpenAI/Anthropic/xAI竞相降价 → 推理量激增 → 训练集群持续扩张 → NVDA/AVGO/SK Hynix受益。投资含义：做空模型层利润率，做多芯片层出货量。
  </div>
</div>

<div class="insight-box">
  <div class="label">观点矩阵</div>
  <div class="content">
    <ul class="signal-list">
      <li><span class="tag tag-hot">Jensen Huang</span> 未公开新言论，但NVDA重回$5T印证市场对其训练垄断的信心</li>
      <li><span class="tag tag-hot">Sam Altman</span> GPT-5.6 Sol在Cerebras上达750 tok/s，54%更高效编码。OpenAI拟9月IPO，估值$730B</li>
      <li><span class="tag tag-key">Marc Andreessen</span> SambaNova $1B F轮@$11B估值，证明推理专用芯片赛道获顶级资本认可</li>
      <li><span class="tag tag-new">Larry Fink</span> 未公开新言论，但BlackRock参投SambaNova显示机构对AI基础设施的长期配置</li>
    </ul>
  </div>
</div>
'''

s3_start = html.find('<div class="section-title"><span class="num">3</span>')
s3_end = html.find('<div class="section-title"><span class="num">4</span>')
if s3_start > 0 and s3_end > 0:
    html = html[:s3_start] + s3_new + html[s3_end:]
    print("S3 updated")

# === S4: AI Model Movements Update ===
s4_new = '''<div class="section-title"><span class="num">4</span> AI独角兽模型技术动向</div>

<div class="insight-box">
  <div class="label">本周模型市场格局（2026-07-12）</div>
  <div class="content">
    GPT-5.6家族（Terra/Sol/Luna）上线48小时后开发者共识：Terra为性价比首选，Sol性能之王，Luna为低成本工作马。Anthropic Claude Fable 5正式收费，Bun团队用64个Fable 5实例11天重写Bun runtime（Zig→Rust）。Google Gemini 3.5 Pro预计7月17日发布，2M上下文，无政府限制。
  </div>
</div>

<table class="data-table">
  <thead>
    <tr><th>公司</th><th>最新模型/动态</th><th>关键参数</th><th>推理成本</th><th>投资含义</th></tr>
  </thead>
  <tbody>
    <tr><td>OpenAI</td><td>GPT-5.6 Terra/Sol/Luna</td><td>Terra 84.3% Terminal-Bench; Sol Ultra 91.9%; Cerebras上750 tok/s</td><td>Terra $2.5/$15; Sol $5/$30; Luna $1/$6 (每百万token)</td><td>API价格战夺回份额，IPO前冲收入。利好推理芯片需求</td></tr>
    <tr><td>Anthropic</td><td>Claude Fable 5 GA; Claude Cowork发布; 64-agent Bun重写</td><td>$10/$50定价; 50%低于Mythos预览; 30天留存政策</td><td>$10/$50 per 1M tokens (intro to Aug 31)</td><td>收入年化的$47B超OpenAI; 企业安全首选定位</td></tr>
    <tr><td>Google</td><td>Gemini 3.5 Pro 7月17日GA; 2M上下文; Deep Think</td><td>TerminalBench 70.7%（低于政府限制阈值）; 无出口限制</td><td>预估$1.25/$10 per 1M tokens</td><td>唯一无政府限制的前沿模型，窗口期优势; 6周延期代价</td></tr>
    <tr><td>DeepSeek</td><td><span style="color:var(--text2)">当日无重大新信号</span></td><td>—</td><td>—</td><td>维持原评级</td></tr>
    <tr><td>Bytedance</td><td><span style="color:var(--text2)">当日无重大新信号</span></td><td>—</td><td>—</td><td>维持原评级</td></tr>
    <tr><td>Moonshot</td><td><span style="color:var(--text2)">当日无重大新信号</span></td><td>—</td><td>—</td><td>维持原评级</td></tr>
    <tr><td>Minimax</td><td><span style="color:var(--text2)">当日无重大新信号</span></td><td>—</td><td>—</td><td>维持原评级</td></tr>
  </tbody>
</table>

<div class="insight-box">
  <div class="label">权威评论</div>
  <div class="content">
    <strong>OpenAI GPT-5.6基础设施突破</strong>：Sol在Cerebras wafer-scale上达750 tok/s，对比GPU-based serving的30-80 tok/s，这是数量级变化——agent loops从分钟级变为秒级。开发者共识：OpenAI定价策略旨在夺回API市场份额。<br><br>
    <strong>Anthropic Fable 5企业级定位</strong>：Stripe压缩"数月工程为数日"，Bun 64-agent重写runtime。Fable 5 vs Mythos 5的双层信任模型预示前沿实验室将以能力分级管控方式运营。
  </div>
</div>
'''

s4_start = html.find('<div class="section-title"><span class="num">4</span>')
s4_end = html.find('<div class="section-title"><span class="num">5</span>')
if s4_start > 0 and s4_end > 0:
    html = html[:s4_start] + s4_new + html[s4_end:]
    print("S4 updated")

# === S5: NVIDIA/AMD/Intel Update ===
s5_new = '''<div class="section-title"><span class="num">5</span> NVIDIA / AMD / Intel（财报级信号）</div>

<div class="insight-box">
  <div class="label">核心信号</div>
  <div class="content">
    <strong>Meta Iris芯片9月流片</strong>：Broadcom设计、TSMC制造， hyperscaler定制芯片俱乐部完成。目标：将20-30%推理成本转移至内部芯片，每年节省数十亿美元。对NVDA：训练份额稳固，推理面临长期侵蚀；对AVGO：设计服务收入倍增；对TSM：新增高端客户流片。<br><br>
    <strong>Nvidia重回$5万亿</strong>：7月10日周五涨2.3%至$210.74，市值再破$5T。芯片板块全面跑赢应用层，逻辑：模型层价格战→推理量激增→芯片层收入 growth。<br><br>
    <strong>SK Hynix ADR创纪录上市</strong>：7月10日纳斯达克SKHY首日涨13%，$26.5B募资超阿里巴巴2014年$21.8B纪录。公司占全球HBM 60%份额，Q1营收$355亿，营业利润率72%。信号：AI内存供应链定价权堪比sole-source。
  </div>
</div>

<table class="data-table">
  <thead>
    <tr><th>标的</th><th>日涨跌</th><th>催化剂</th><th>投资含义</th></tr>
  </thead>
  <tbody>
    <tr><td>NVDA</td><td>+3.24%</td><td>市值重回$5T; 训练需求持续</td><td>训练垄断地位短期不可动摇，但推理份额面临hyperscaler自研侵蚀</td></tr>
    <tr><td>AMD</td><td>+7.91%</td><td>芯片板块全面rally; 推理份额增长</td><td>推理市场多元化受益者，MI系列在hyperscaler替代方案中地位上升</td></tr>
    <tr><td>AVGO</td><td>+2.88%</td><td>Meta Iris/OpenAI Jalapeno/Microsoft Maia/Google TPUv7设计订单</td><td>AI芯片设计服务"卖铲人"，多客户订单降低单一客户风险</td></tr>
    <tr><td>TSM</td><td>-0.55%</td><td>Iris流片受益; 但地缘政治风险持续</td><td>先进制程不可替代，但需关注美国232关税对设备进口影响</td></tr>
    <tr><td>MU</td><td>+3.41%</td><td>SK Hynix ADR成功提振HBM板块情绪</td><td>HBM竞争加剧，但行业整体受益于AI内存需求爆发</td></tr>
    <tr><td>AMAT</td><td>+2.37%</td><td>芯片板块rally; 先进封装需求</td><td>设备股受益于AI chiplet和先进封装CAPEX周期</td></tr>
    <tr><td>LRCX</td><td>+5.24%</td><td>芯片板块rally; 蚀刻设备需求</td><td>AI驱动的高NA EUV和先进蚀刻设备采购周期</td></tr>
    <tr><td>ASML</td><td>+1.65%</td><td>高NA EUV订单持续; 中国设备限制风险</td><td>技术垄断但需关注BIS对华设备出口管制升级</td></tr>
    <tr><td>INTC</td><td>-0.38%</td><td><span style="color:var(--text2)">暂无新催化剂</span></td><td>维持SPEC BUY，18A制程良率仍是关键变量，需Q2财报验证</td></tr>
    <tr><td>QCOM</td><td>+1.39%</td><td>骁龙X Elite端侧AI PC; 汽车芯片</td><td>端侧AI和汽车半导体双轮驱动，但短期催化有限</td></tr>
  </tbody>
</table>

<div class="quote-box">
  <div class="quote-text">"The market is saying loudly that it currently trusts hardware margins more than model-layer margins. If you want a single stock chart that summarizes the 2026 AI economy, SKHY's first week of trading is a good candidate."</div>
  <div class="quote-source">— BuildFastWithAI Market Intelligence, 2026-07-11</div>
  <div class="quote-context">Context: SK Hynix ADR debut and Nvidia $5T revaluation in same week signal market repricing of AI infrastructure over AI software.</div>
  <div class="play-btn">▶ 播放分析</div>
</div>
'''

s5_start = html.find('<div class="section-title"><span class="num">5</span>')
s5_end = html.find('<div class="section-title"><span class="num">6</span>')
if s5_start > 0 and s5_end > 0:
    html = html[:s5_start] + s5_new + html[s5_end:]
    print("S5 updated")

# === S12: Political Update ===
s12_new = '''<div class="section-title"><span class="num">12</span> 政治突发：地缘与政策对供应链影响</div>

<div class="insight-box">
  <div class="label">重大政策信号</div>
  <div class="content">
    <strong>1. 美国商务部将阿联酋从出口管制限制国家名单中移除，重新归类为A:5，允许许可证-free出口先进AI芯片（2026-07-10）</strong><br>
    来源：US Commerce Department, Federal Register<br>
    受益方：Amazon, Apple, xAI在UAE的大规模建设。之前需case-by-case审批，现为常规商业交易。这是Gulf compute corridor正式化——UAE通过MGX和G42主权财富资本、廉价能源、快速审批，成为AI建设的"中立 ground"。<br><br>
    <strong>2. 美国诉OpenAI窃取Apple芯片机密（2026-07-11）</strong><br>
    Apple在北加州联邦法院起诉OpenAI，指控其招聘超过400名前Apple员工构成对硅片和端侧AI团队机密的"系统性提取"。诉讼发生在OpenAI计划IPO前几周，可能延迟其上市时间表。Anthropic年收入约$470亿（Fortune数据），OpenAI预计$250-330亿——Apple诉讼是IPO前的重大法律 overhang。
  </div>
</div>

<table class="data-table">
  <thead>
    <tr><th>政策/事件</th><th>来源</th><th>日期</th><th>供应链影响</th></tr>
  </thead㸾
  <tbody>
    <tr><td>UAE AI芯片出口A:5重新分类</td><td>US Commerce Dept / Federal Register</td><td>2026-07-10</td><td>Amazon/Apple/xAI在UAE建设加速；Gulf compute corridor正式化；消除case-by-case审批摩擦</td></tr>
    <tr><td>Apple诉OpenAI窃取芯片机密</td><td>Northern California Federal Court filing</td><td>2026-07-11</td><td>OpenAI IPO时间表风险；Apple silicon团队保密措施收紧；行业人才流动受阻</td></tr>
    <tr><td>Section 232半导体关税25%</td><td>White House Proclamation / Federal Register</td><td>2026-01-15生效</td><td>半导体设备进口成本上升；ASML/AMAT/LRCX面临供应链重构；中国成熟节点设备本土化加速</td></tr>
  </tbody>
</table>

<div class="insight-box">
  <div class="label">投资含义</div>
  <div class="content">
    UAE A:5重新分类是 summer 2026 AI贸易放松的一部分——对盟国和伙伴国 loosening AI trade restrictions，同时对中国保持 wall。Gulf compute corridor（阿联酋、沙特）正在成为中美之外的AI建设第三极，值得长期跟踪。对OpenAI的Apple诉讼是结构性风险信号：人才战升级为法律战，可能改变硅谷AI人才流动模式。
  </div>
</div>
'''

s12_start = html.find('<div class="section-title"><span class="num">12</span>')
s12_end = html.find('<div class="section-title"><span class="num">13</span>')
if s12_start > 0 and s12_end > 0:
    html = html[:s12_start] + s12_new + html[s12_end:]
    print("S12 updated")

# Save updated report
with open('/root/.openclaw/workspace/daily_report_2026-07-13.html', 'w') as f:
    f.write(html)

print("\nReport content updated successfully")
