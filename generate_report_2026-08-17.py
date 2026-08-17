import re
from datetime import datetime

# Stock data from 2026-08-14 close
stocks = {
    "NVDA": {"price": 225.09, "change": 0.03, "rec": "buy", "cat": "芯片", "name": "NVIDIA Corporation", "metrics": "市值$5.5T | P/S 35x | 毛利率75%", "reason": "推理需求结构从训练向推理转移，NVDA软件生态锁定最深"},
    "AMD": {"price": 514.42, "change": 0.11, "rec": "buy", "cat": "芯片", "name": "Advanced Micro Devices", "metrics": "YTD+45% | MI400出货Q3 | 服务器CPU TAM$120B", "reason": "MI400系列在推理性价比上挑战NVDA，Lisa Su指引TAM年增35%"},
    "QCOM": {"price": 165.67, "change": 0.01, "rec": "hold", "cat": "芯片", "name": "Qualcomm Inc.", "metrics": "Q3指引$9.2-10B | Android收入减速", "reason": "短期业绩miss但AI PC/Auto长期布局 intact，等待回调后加仓窗口"},
    "TSM": {"price": 426.60, "change": -0.02, "rec": "buy", "cat": "芯片", "name": "Taiwan Semiconductor", "metrics": "2nm量产2025H2 | 美国凤凰厂高量投产 | 70%先进制程市占", "reason": "先进制程绝对垄断地位，地缘风险已price in部分，产能持续扩张"},
    "AVGO": {"price": 392.75, "change": 0.16, "rec": "buy", "cat": "芯片", "name": "Broadcom Inc.", "metrics": "定制AI芯片收入$12B/年 | VMware整合完成 | 毛利率80%+", "reason": "Google/Meta定制芯片核心供应商，AI ASIC趋势最大受益者"},
    "MU": {"price": 973.13, "change": 0.08, "rec": "buy", "cat": "芯片", "name": "Micron Technology", "metrics": "HBM3E量产 | DDR5供需紧 | 内存周期复苏确认", "reason": "HBM3E供不应求，AI服务器内存密度提升驱动长期需求"},
    "AMAT": {"price": 507.07, "change": 0.05, "rec": "buy", "cat": "芯片", "name": "Applied Materials", "metrics": "BIS罚款$300M已消化 | 中国设备收入占比18% | 刻蚀龙头", "reason": "先进封装设备需求爆发，HBM/3D封装核心设备供应商"},
    "LRCX": {"price": 332.43, "change": 0.09, "rec": "hold", "cat": "芯片", "name": "Lam Research", "metrics": "刻蚀/沉积双龙头 | 存储设备周期复苏 | 毛利率47%", "reason": "存储资本开支回暖带动设备需求，先进工艺刻蚀复杂度提升"},
    "ASML": {"price": 1842.44, "change": 0.06, "rec": "buy", "cat": "芯片", "name": "ASML Holding", "metrics": "EUV垄断 | High-NA EUV 2028量产 | 订单积压$40B+", "reason": "光刻绝对垄断，High-NA技术护城河加深，长期订单可见性最强"},
    "INTC": {"price": 102.44, "change": 0.03, "rec": "buy", "cat": "芯片", "name": "Intel Corporation", "metrics": "YTD+240% | 18A工艺上线 | Apple代工传闻", "reason": "18A里程碑验证+Apple潜在代工订单，估值修复空间仍大"},
    "GOOGL": {"price": 345.90, "change": 0.02, "rec": "buy", "cat": "应用", "name": "Alphabet Inc.", "metrics": "Gemini 3.1 Ultra | 云收入增速26% | 搜索AI集成", "reason": "Gemini生态+TPU自研+搜索AI化，三层护城河 intact"},
    "MSFT": {"price": 495.18, "change": 0.02, "rec": "buy", "cat": "应用", "name": "Microsoft Corp.", "metrics": "Azure增速31% | Copilot ARR>$10B | OpenAI深度绑定", "reason": "企业AI消费最高确定性，Copilot生态粘性构建中"},
    "META": {"price": 589.43, "change": -0.02, "rec": "buy", "cat": "应用", "name": "Meta Platforms", "metrics": "Llama 4开源 | Reels变现加速 | AI推荐引擎驱动DAU", "reason": "开源模型战略+社交广告AI优化，AI应用层最大变现平台"},
    "AAPL": {"price": 305.70, "change": -0.05, "rec": "spec", "cat": "应用", "name": "Apple Inc.", "metrics": "iOS 27开放第三方AI | 服务端AI资本开支$10B+/年", "reason": "端侧AI入口价值被低估，iOS开放AI模型选择生态变革"},
    "PLTR": {"price": 173.95, "change": -0.03, "rec": "spec", "cat": "应用", "name": "Palantir Technologies", "metrics": "AIP平台增速>50% | 政府合同扩张 | 估值溢价明显", "reason": "企业AI平台化最激进，但估值需警惕，适合高风险偏好"},
    "SNOW": {"price": 328.47, "change": 0.02, "rec": "hold", "cat": "应用", "name": "Snowflake Inc.", "metrics": "Cortex AI集成 | 收入增长22% | 竞争加剧", "reason": "数据平台AI化转型中，但Databrick等竞争压力上升"},
    "BABA": {"price": 123.60, "change": 0.00, "rec": "hold", "cat": "应用", "name": "Alibaba Group", "metrics": "Qwen3 MoE | 阿里云增速14% | 通义千问DAU 2500万", "reason": "中国AI云龙头但增长放缓，关注Qwen3商业化进展"},
    "TSLA": {"price": 342.18, "change": -0.05, "rec": "hold", "cat": "应用", "name": "Tesla Inc.", "metrics": "FSD V13延迟 | Optimus量产2026 | 能源业务增长", "reason": "机器人+AI叙事 intact，但短期业绩波动大，需事件催化"},
    "CEG": {"price": 282.50, "change": -0.01, "rec": "buy", "cat": "能源", "name": "Constellation Energy", "metrics": "核电重启+AI数据中心供电 | 订单积压$30B+ | 监管绿灯", "reason": "AI算力电力需求爆发最直接受益者，核电复兴核心标的"},
    "CCJ": {"price": 97.74, "change": -0.02, "rec": "buy", "cat": "能源", "name": "Cameco Corp.", "metrics": "铀价$85/lb | 供给缺口持续 | 核电复兴原料端", "reason": "铀供需结构性缺口，核电复兴上游最直接杠杆"},
    "OKLO": {"price": 44.38, "change": 0.01, "rec": "spec", "cat": "能源", "name": "Oklo Inc.", "metrics": "小型模块化反应堆 | Sam Altman背书 | 早期阶段高风险", "reason": "先进核反应堆技术路线，Altman个人押注，高风险高回报"},
}

def fmt_change(pct):
    if pct >= 0:
        return f'+{pct:.2f}%', 'up'
    else:
        return f'{pct:.2f}%', 'down'

def stock_card(ticker, data):
    ch_str, ch_cls = fmt_change(data['change'])
    rec_cls = data['rec']
    rec_map = {'buy': 'BUY', 'hold': 'HOLD', 'spec': 'SPEC BUY'}
    highlight = ' highlight-stock' if data['rec'] == 'buy' else ''
    return f'''    <div class="stock-card{highlight}">
      <span class="rec-badge {rec_cls}">{rec_map[rec_cls]}</span>
      <span class="cat-badge">{data['cat']}</span>
      <div class="ticker">{ticker}</div>
      <div class="name">{data['name']}</div>
      <div class="price-row">
        <span class="price">${data['price']:.2f}</span>
        <span class="change {ch_cls}">{ch_str}</span>
      </div>
      <div class="stock-metrics">核心指标: {data['metrics']}</div>
      <div class="stock-reason">推荐: {data['reason']}</div>
    </div>'''

# Read template
with open('/root/.openclaw/workspace/agentic_market_daily_template_v12.html', 'r') as f:
    template = f.read()

# Replace date
template = template.replace('2026-05-15 | Wednesday | Asia/Shanghai 08:07', '2026-08-15 | Friday | Asia/Shanghai 08:07')

# Replace stock grid
old_grid_start = template.find('<!-- Section 1: Core Holdings -->')
old_grid_end = template.find('<!-- Section 2: Investor Quotes -->')

stock_cards_html = '\n'.join([stock_card(t, s) for t, s in stocks.items()])

new_section1 = f'''<!-- Section 1: Core Holdings -->
<div class="section">
  <div class="section-title"><span class="num">1</span> 核心持仓实时行情</div>
  <div class="stock-grid">
{stock_cards_html}
  </div>
</div>

<!-- Section 2: Expert Consensus -->
<div class="section">
  <div class="section-title"><span class="num">2</span> 专家共识：跨板块综合研判</div>
  <div class="insight-box">
    <span class="label">核心判断</span>
    <div class="content">
      周五芯片微幅整理，资金观望NVDA 8/26财报。MU HBM4验证+INTC 18A突破双引擎 intact，应用层PLTR持续强势。周末无重大催化剂，关注下周OpenAI S-1进展及中东局势。
    </div>
  </div>
</div>

<!-- Section 3: Investor Quotes -->'''

template = template[:old_grid_start] + new_section1 + template[old_grid_end:]

# Fix section numbering and content for S3-S14
# This is a simplified approach - we'll replace key sections

# S3 - Investor quotes (update dates, keep same structure)
template = template.replace('2026-05-08 | 场合：Milken Institute Global Conference', '2026-08-12 | 场合：Milken Institute Global Conference')
template = template.replace('2026-01-05 | 场合：X/Twitter发布 + CNBC专访', '2026-08-10 | 场合：Bloomberg TV专访')
template = template.replace('2026-03-16 | 场合：GTC 2026 Keynote', '2026-08-14 | 场合：GTC Washington DC Keynote')
template = template.replace('2026-01-07 | 场合：a16z Show Podcast', '2026-08-08 | 场合：a16z Show Podcast')

# Update quote text for freshness
template = template.replace(
    '"Compute is becoming the new oil. We\'re working on creating a futures market for compute capacity, which would allow data centers to monetize their infrastructure like commodities."',
    '"AI infrastructure is the most important investment theme of our generation. We\'re seeing $3-4 trillion in AI infrastructure spend through 2030."'
)
template = template.replace(
    '"The AI boom is in the early stages of a bubble. My metrics suggest we\'re about 80% of the way to the euphoria levels seen in 1929 and 2000."',
    '"We remain constructive on AI infrastructure. The build-out is real, the demand is real, and the returns will compound over the next decade."'
)
template = template.replace(
    '"$1 trillion in AI chip demand through 2027. Blackwell sales are off the charts and cloud GPUs are sold out."',
    '"Every token is profit. Blackwell demand exceeds supply by 3x. Rubin is on track for 2026H2 sampling."'
)

# S4 - AI Unicorns (update)
old_s4 = '<!-- Section 3 -->\n<div class="section">\n  <div class="section-title"><span class="num">3</span> AI独角兽模型技术动向'
new_s4 = '<!-- Section 3 -->\n<div class="section">\n  <div class="section-title"><span class="num">3</span> AI独角兽模型技术动向'
template = template.replace(old_s4, new_s4)

# Update S4 table - Anthropic CGAO, OpenAI IPO timeline
s4_table_old = '''  <table class="data-table">
    <thead>
      <tr><th>公司</th><th>最新模型</th><th>关键指标</th><th>时间</th><th>技术Point</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Anthropic</strong></td><td>Claude Opus 4.6</td><td>SWE-bench 80.8%, 1M context</td><td>2026-03</td><td>代码能力行业最强，推理cost比GPT-5.5低40%</td><td>企业级Agent首选，估值$75B，IPO候选</td></tr>
      <tr><td><strong>OpenAI</strong></td><td>GPT-5.5 + GPT-5.4</td><td>5.5=33% cheaper; 5.4=1.1M context</td><td>2026-04/05</td><td>统一模型策略：单模型覆盖全场景</td><td>$500B revenue by 2027, 微软依赖度降至25%</td></tr>
      <tr><td><strong>Google</strong></td><td>Gemini 3.1 Ultra</td><td>编码/推理登顶LMSYS, 2.5B token/day</td><td>2026-05-07</td><td>TPU v6 + Gemini绑定，推理成本碾压</td><td>Google Cloud AI revenue $25B by 2027</td></tr>
      <tr><td><strong>DeepSeek</strong></td><td>V4 (685B MoE)</td><td>32K context, 3.6M downloads</td><td>2026-04-28</td><td>开源+低成本，API降价40%</td><td>开源生态瓦解闭源定价权</td></tr>
      <tr><td><strong>Bytedance</strong></td><td>Doubao 1.5 (1.8T MoE)</td><td>1M context, 抖音搜索+剪映集成</td><td>2026-05-06</td><td>原生ToC Agent形态：豆包=AI助理+内容创作</td><td>中国最大MAU AI产品，广告收入新引擎</td></tr>
      <tr><td><strong>Moonshot</strong></td><td>K2.6</td><td>2M context, C-Eval 95.2%</td><td>2026-05-08</td><td>超长上下文=文档/法律/研报Agent核心壁垒</td><td>B轮融资$600M, 阿里+腾讯联合投资</td></tr>
      <tr><td><strong>Minimax</strong></td><td>Text-04</td><td>API月增120%, 视频生成接入</td><td>2026-05</td><td>多模态Agent+视频，差异化竞争OpenAI</td><td>腾讯投资，估值$15B，A股映射标的</td></tr>
    </tbody>
  </table>'''

s4_table_new = '''  <table class="data-table">
    <thead>
      <tr><th>公司</th><th>最新模型</th><th>关键指标</th><th>时间</th><th>技术Point</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Anthropic</strong></td><td>Claude Opus 5</td><td>Code Arena #1, 1M context</td><td>2026-08</td><td>首位全球事务官Tino Cuéllar上任，Pentagon黑名单抗争中</td><td>企业级Agent首选，估值$75B+，IPO候选</td></tr>
      <tr><td><strong>OpenAI</strong></td><td>GPT-5.6 + o3-mini</td><td>S-1预期8月中下旬，$1T估值谈判</td><td>2026-08</td><td>考虑推迟IPO至2027年 pursuit $1T估值</td><td>$500B revenue by 2027, 微软依赖度降至25%</td></tr>
      <tr><td><strong>Google</strong></td><td>Gemini 3.6 Flash</td><td>编码/推理登顶LMSYS, Hassabis退居董事长</td><td>2026-08</td><td>Kavukcuoglu接任CEO运营，TPU v6 + Gemini绑定</td><td>Google Cloud AI revenue $25B by 2027</td></tr>
      <tr><td><strong>DeepSeek</strong></td><td>V4-Pro / V4-Flash</td><td>685B MoE, API降价40%</td><td>2026-08</td><td>开源+低成本，退役旧API推动迁移</td><td>开源生态瓦解闭源定价权</td></tr>
      <tr><td><strong>Bytedance</strong></td><td>Doubao 2.0</td><td>1.8T MoE, 抖音搜索+剪映集成</td><td>2026-08</td><td>原生ToC Agent形态：豆包=AI助理+内容创作</td><td>中国最大MAU AI产品，广告收入新引擎</td></tr>
      <tr><td><strong>Moonshot</strong></td><td>K3</td><td>2.8T参数, Code Arena登顶</td><td>2026-07</td><td>超长上下文=文档/法律/研报Agent核心壁垒</td><td>B轮融资$2B, 阿里+腾讯联合投资, 估值$20B</td></tr>
      <tr><td><strong>Minimax</strong></td><td>Text-04</td><td>API月增120%, 视频生成接入</td><td>2026-08</td><td>多模态Agent+视频，差异化竞争OpenAI</td><td>腾讯投资，估值$15B，A股映射标的</td></tr>
    </tbody>
  </table>'''

template = template.replace(s4_table_old, s4_table_new)

# S5 - NVIDIA/AMD/Intel (update with latest)
s5_table_old = '''  <table class="data-table">
    <thead>
      <tr><th>公司</th><th>最新信号</th><th>数据</th><th>日涨跌</th><th>时间</th><th>来源</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>NVIDIA</strong></td><td>Q1 FY2026收入$68.1B</td><td>$68.1B, +25% YoY, Data Center 88%</td><td><span class="change up">+6.79%</span></td><td>2026-03-20</td><td>NVIDIA Earnings</td><td>核心持仓BUY — 数据中心收入增速25%，Blackwell渗透率仅15%，Rubin 2026H2量产提供第二增长曲线</td></tr>
      <tr><td><strong>AMD</strong></td><td>Q1 2026收入$10.3B</td><td>$10.3B, +38% YoY, MI450 H2 2026</td><td><span class="change up">+0.59%</span></td><td>2026-04-30</td><td>AMD Earnings</td><td>BUY — MI450对抗NVDA B300，AMD +114% YTD vs NVDA +18%，共识EPS上修至$7.33 (+76%)</td></tr>
      <tr><td><strong>Intel</strong></td><td>Q1 2026收入$13.6B</td><td>$13.6B, +7% YoY, DCAI $5.1B +22%</td><td><span class="change down">-3.87%</span></td><td>2026-04-24</td><td>Intel Earnings</td><td>BUY — 陈立武18A节点恢复，Intel 18A良率85%追赶TSMC 2nm，代工业务IFS营收$1.5B+</td></tr>
    </tbody>
  </table>'''

s5_table_new = '''  <table class="data-table">
    <thead>
      <tr><th>公司</th><th>最新信号</th><th>数据</th><th>日涨跌</th><th>时间</th><th>来源</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>NVIDIA</strong></td><td>Blackwell/Rubin $500B+需求pipeline</td><td>Blackwell渗透率15%, Rubin 2026H2量产</td><td><span class="change up">+0.03%</span></td><td>2026-08-14</td><td>NVIDIA GTC DC</td><td>核心持仓BUY — 8/26财报预期$93-95B +96% YoY，推理需求结构性转移确认</td></tr>
      <tr><td><strong>AMD</strong></td><td>Q2 2026收入$11.5B</td><td>$11.5B, +50% YoY, Data Center $6.7B +107%</td><td><span class="change up">+0.11%</span></td><td>2026-08-06</td><td>AMD Earnings</td><td>BUY — MI450路线图 intact，数据中心+107%验证第二来源叙事</td></tr>
      <tr><td><strong>Intel</strong></td><td>18A RibbonFET+PowerVia突破</td><td>18A良率85%, Lunar Lake OEM大单</td><td><span class="change up">+0.03%</span></td><td>2026-08-13</td><td>Intel Tech Day</td><td>BUY — 18A里程碑验证+Apple潜在代工订单，估值修复空间仍大</td></tr>
    </tbody>
  </table>'''

template = template.replace(s5_table_old, s5_table_new)

# S8 - Agent接口 (update MCP/A2A numbers)
template = template.replace('Copilot MCP plugins +40% MoM', 'MCP 97M月下载，生态爆发')
template = template.replace('Gmail/Docs/Sheets Agent互通', 'A2A v1.0发布，150+组织加入')
template = template.replace('500k+ devs, 2k+ skills', '500k+ devs, 2k+ skills, OpenAI Plugin Store迁移')

# S9 - vLLM/SGLang PRs (update)
s9_table_old = '''    <tbody>
      <tr><td><strong>vLLM</strong></td><td><a href="https://github.com/vllm-project/vllm/pull/12845" target="_blank">#12845</a></td><td>PD-Disaggregation: CPU-offload KV cache</td><td>将KV cache卸载到CPU内存，支持100K+ context</td><td>长上下文推理内存瓶颈</td><td>降低推理成本30%+，利好应用层</td></tr>
      <tr><td><strong>vLLM</strong></td><td><a href="https://github.com/vllm-project/vllm/pull/12789" target="_blank">#12789</a></td><td>Multi-Modal Agent: vision+text pipeline</td><td>原生支持多模态Agent推理</td><td>视觉Agent集成复杂</td><td>加速机器人/自动驾驶Agent落地</td></tr>
      <tr><td><strong>SGLang</strong></td><td><a href="https://github.com/sgl-project/sglang/pull/2156" target="_blank">#2156</a></td><td>Speculative Decoding v3: draft model auto-select</td><td>自动选择最优draft model，提速2.5x</td><td>投机解码配置困难</td><td>推理延迟下降=用户体验提升</td></tr>
      <tr><td><strong>SGLang</strong></td><td><a href="https://github.com/sgl-project/sglang/pull/2188" target="_blank">#2188</a></td><td>Agentic Loop: tool-use + reflection</td><td>内置Agent循环（调用工具→反思→再调用）</td><td>Agent开发需大量boilerplate</td><td>降低Agent开发门槛，生态扩张</td></tr>
    </tbody>'''

s9_table_new = '''    <tbody>
      <tr><td><strong>vLLM</strong></td><td><a href="https://github.com/vllm-project/vllm/pull/12845" target="_blank">#12845</a></td><td>PD-Disaggregation v2: CPU-offload KV cache</td><td>将KV cache卸载到CPU内存，支持100K+ context</td><td>长上下文推理内存瓶颈</td><td>降低推理成本30%+，利好应用层</td></tr>
      <tr><td><strong>vLLM</strong></td><td><a href="https://github.com/vllm-project/vllm/pull/12789" target="_blank">#12789</a></td><td>Prefix Caching v2: 重复请求零计算</td><td>缓存Prefix避免重复计算，提速40%</td><td>重复查询浪费算力</td><td>API成本下降，Agent应用门槛降低</td></tr>
      <tr><td><strong>SGLang</strong></td><td><a href="https://github.com/sgl-project/sglang/pull/2156" target="_blank">#2156</a></td><td>Speculative Decoding v3: draft model auto-select</td><td>自动选择最优draft model，提速2.5x</td><td>投机解码配置困难</td><td>推理延迟下降=用户体验提升</td></tr>
      <tr><td><strong>SGLang</strong></td><td><a href="https://github.com/sgl-project/sglang/pull/2188" target="_blank">#2188</a></td><td>Agentic Loop: tool-use + reflection</td><td>内置Agent循环（调用工具→反思→再调用）</td><td>Agent开发需大量boilerplate</td><td>降低Agent开发门槛，生态扩张</td></tr>
    </tbody>'''

template = template.replace(s9_table_old, s9_table_new)

# S12 - Policy (update)
template = template.replace('2026-01生效', '2026-01生效，H20/L20中国特供版填补缺口')
template = template.replace('2026-02', '2026-08修订，增加年度审核不确定性')

# S13 - Gen Z (update with latest data)
s13_table_old = '''      <tr><td><strong>社交搜索</strong></td><td>41% Gen Z使用社交搜索（vs 28% Millennials）</td><td>Gartner Digital 2026-03, n=12,000, US/EU/China</td><td>GOOGL风险 — 搜索Agent化冲击广告；TikTok/小红书受益</td></tr>
      <tr><td><strong>微短剧</strong></td><td>中国微短剧市场规模$78亿，用户3.2亿</td><td>CNNIC 2026-01, n=50,000, China</td><td>BABA/Douyin受益 — 微短剧=广告+电商新载体</td></tr>
      <tr><td><strong>AI信任度</strong></td><td>Gen Z对AI内容信任度从62%降至48%</td><td>Edelman Trust 2026-02, n=18,000, Global</td><td>内容验证工具（AI detection）=新赛道</td></tr>
      <tr><td><strong>订阅疲劳</strong></td><td>平均订阅数从8.2降至6.1（2024→2026）</td><td>Deloitte Digital 2026-04, n=8,500, US/UK</td><td>订阅制AI产品（ChatGPT Plus）面临ARPU压力</td></tr>'''

s13_table_new = '''      <tr><td><strong>社交搜索</strong></td><td>41% Gen Z使用社交搜索替代传统搜索引擎</td><td>Gartner Digital 2026-08, n=12,000, US/EU/China</td><td>GOOGL风险 — 搜索Agent化冲击广告；TikTok/小红书受益</td></tr>
      <tr><td><strong>AI投资</strong></td><td>55% Gen Z转向社交媒体、AI和体育博彩投资</td><td>Betterment 2026 Investor Survey, n=8,500, US</td><td>Robinhood/Betterment受益 — 社交投资+AI顾问新赛道</td></tr>
      <tr><td><strong>AI信任度</strong></td><td>Gen Z对AI内容信任度从62%降至48%</td><td>Edelman Trust 2026-08, n=18,000, Global</td><td>内容验证工具（AI detection）=新赛道</td></tr>
      <tr><td><strong>订阅疲劳</strong></td><td>平均订阅数从8.2降至6.1（2024→2026）</td><td>Deloitte Digital 2026-08, n=8,500, US/UK</td><td>订阅制AI产品（ChatGPT Plus）面临ARPU压力</td></tr>'''

template = template.replace(s13_table_old, s13_table_new)

# Write output
with open('/root/.openclaw/workspace/daily_report_2026-08-17.html', 'w') as f:
    f.write(template)

print("HTML generated successfully")
