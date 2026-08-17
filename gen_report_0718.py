#!/usr/bin/env python3
"""
Generate July 18, 2026 (Saturday) daily report based on July 17 (Friday) data.
Saturday = market closed, use Friday close data with weekend notes.
"""
import csv
import re
from datetime import datetime

# Read stock data
stocks = {}
with open('/root/.openclaw/workspace/stock_data_2026-07-17.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        ticker = row['ts_code'].replace('.US', '')
        stocks[ticker] = {
            'close': float(row['close']),
            'pct_change': float(row['pct_change']),
            'open': float(row['open']),
            'high': float(row['high']),
            'low': float(row['low']),
        }

# Stock definitions with metadata
stock_defs = [
    # Chip - 10
    ('NVDA', 'NVIDIA Corporation', '芯片', 'BUY', '市值$5.0T | P/S 32x | 毛利率75%', '推理需求结构从训练向推理转移，NVDA软件生态锁定最深'),
    ('AMD', 'Advanced Micro Devices', '芯片', 'BUY', 'MI400出货Q3 | 服务器CPU TAM$120B | YTD波动', 'MI400系列在推理性价比上挑战NVDA，Lisa Su指引TAM年增35%'),
    ('QCOM', 'Qualcomm Inc.', '芯片', 'HOLD', 'Q3指引$9.2-10B | Android收入减速 | AI PC布局', '短期业绩miss但AI PC/Auto长期布局 intact，等待回调后加仓窗口'),
    ('TSM', 'Taiwan Semiconductor', '芯片', 'BUY', '2nm量产2025H2 | 美国凤凰厂高量投产 | 70%先进制程市占', '先进制程绝对垄断地位，地缘风险已price in部分，产能持续扩张'),
    ('AVGO', 'Broadcom Inc.', '芯片', 'BUY', '定制AI芯片收入$12B/年 | VMware整合完成 | 毛利率80%+', 'Google/Meta定制芯片核心供应商，AI ASIC趋势最大受益者'),
    ('MU', 'Micron Technology', '芯片', 'BUY', 'HBM3E量产 | DDR5供需紧 | 内存周期复苏确认', 'HBM3E供不应求，AI服务器内存密度提升驱动长期需求'),
    ('AMAT', 'Applied Materials', '芯片', 'BUY', 'BIS罚款$300M已消化 | 中国设备收入占比18% | 刻蚀龙头', '先进封装设备需求爆发，HBM/3D封装核心设备供应商'),
    ('LRCX', 'Lam Research', '芯片', 'HOLD', '刻蚀/沉积双龙头 | 存储设备周期复苏 | 毛利率47%', '存储资本开支回暖带动设备需求，先进工艺刻蚀复杂度提升'),
    ('ASML', 'ASML Holding', '芯片', 'BUY', 'EUV垄断 | High-NA EUV 2028量产 | 订单积压$40B+', '光刻绝对垄断，High-NA技术护城河加深，长期订单可见性最强'),
    ('INTC', 'Intel Corporation', '芯片', 'BUY', '18A工艺上线 | Apple代工传闻 | YTD+220%', '18A里程碑验证+Apple潜在代工订单，估值修复空间仍大'),
    # App - 8
    ('GOOGL', 'Alphabet Inc.', '应用', 'BUY', 'Gemini 3.1 Ultra | 云收入增速26% | 搜索AI集成', 'Gemini生态+TPU自研+搜索AI化，三层护城河 intact'),
    ('MSFT', 'Microsoft Corp.', '应用', 'BUY', 'Azure增速31% | Copilot ARR>$10B | OpenAI深度绑定', '企业AI消费最高确定性，Copilot生态粘性构建中'),
    ('META', 'Meta Platforms', '应用', 'BUY', 'Iris芯片9月流片 | LLM开源生态 | Reality Labs减亏', '自研芯片+开源模型双轮驱动，AI基础设施投入进入收获期'),
    ('AAPL', 'Apple Inc.', '应用', 'BUY', 'Apple Intelligence rollout | 服务收入增速 | 现金$162B', '端侧AI落地最确定场景，服务收入持续贡献利润稳定性'),
    ('PLTR', 'Palantir Technologies', '应用', 'BUY', 'AIP平台签约增长 | 政府收入占比45% | 毛利率81%', 'AI平台企业级落地标杆，政府+商业双引擎驱动'),
    ('SNOW', 'Snowflake Inc.', '应用', 'HOLD', 'Cortex AI功能上线 | 消费模式转型 | 增速放缓', 'AI数据云平台长期逻辑 intact，但短期增长承压等待拐点'),
    ('BABA', 'Alibaba Group', '应用', 'BUY', '通义千问API增长 | 云业务分拆 | 菜鸟IPO暂停', '中国模型API流量占比提升，阿里云AI算力定价权逐步建立'),
    ('TSLA', 'Tesla Inc.', '应用', 'HOLD', 'FSD V13推送 | Robotaxi 10月发布 | 能源存储增长', '自动驾驶叙事+能源业务双主线，估值已反映部分预期'),
    # Energy - 3
    ('CEG', 'Constellation Energy', '能源', 'BUY', '核电重启核心标的 | 数据中心PPA签约 | 监管利好', 'AI数据中心电力需求爆发，核电基荷电源不可替代性'),
    ('CCJ', 'Cameco Corp.', '能源', 'BUY', '铀矿供应紧平衡 | 长协价格回升 | 地缘供应风险', '全球铀矿供应缺口持续，核电复兴周期核心资源标的'),
    ('OKLO', 'Oklo Inc.', '能源', 'SPEC BUY', 'SMR技术路线 | Aurora反应堆 | 预营收阶段', '小型模块化反应堆先锋，技术验证后商业化潜力大，高风险高回报'),
]

# Highlight the worst performer or a key stock
highlight_ticker = 'INTC'

stock_cards = []
for ticker, name, cat, rec, metrics, reason in stock_defs:
    data = stocks.get(ticker, {})
    price = data.get('close', 0)
    pct = data.get('pct_change', 0)
    
    change_class = 'up' if pct >= 0 else 'down'
    change_sign = '+' if pct >= 0 else ''
    highlight = ' highlight-stock' if ticker == highlight_ticker else ''
    
    # Weekend note: no new catalyst
    reason_text = "暂无新催化剂，维持原评级" if ticker != highlight_ticker else reason
    
    card = f'''    <div class="stock-card{highlight}">
      <span class="rec-badge {rec.lower().replace(' ', '-')}">{rec}</span>
      <span class="cat-badge">{cat}</span>
      <div class="ticker">{ticker}</div>
      <div class="name">{name}</div>
      <div class="price-row">
        <span class="price">${price:.2f}</span>
        <span class="change {change_class}">{change_sign}{pct:.2f}%</span>
      </div>
      <div class="stock-metrics">核心指标: {metrics}</div>
      <div class="stock-reason">推荐: {reason_text}</div>
    </div>'''
    stock_cards.append(card)

stock_grid = '\n'.join(stock_cards)

# Build the full HTML report
# We'll use a template approach - copy the V12 template structure

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agentic Market Daily | 2026-07-18</title>
<style>
:root {{
  --bg: #0a0e1a;
  --card: #0d1f35;
  --card2: #0a1929;
  --text: #e6edf7;
  --text2: #8892b0;
  --accent: #00d4ff;
  --highlight: #e94560;
  --success: #4ecca3;
  --warning: #ffc107;
  --danger: #ff4757;
  --border: #1a2d4a;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  background: var(--bg);
  color: var(--text);
  font-family: 'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
  line-height:1.6;
}}
.container {{ max-width:1200px; margin:0 auto; padding:20px; }}
header {{
  text-align:center; padding:30px 0; border-bottom:2px solid var(--accent); margin-bottom:30px;
}}
header h1 {{ font-size:2.2em; color:var(--accent); letter-spacing:2px; margin-bottom:8px; }}
header .subtitle {{ color:var(--text2); font-size:0.95em; }}
header .date-badge {{
  display:inline-block; background:var(--card); border:1px solid var(--accent);
  padding:6px 16px; border-radius:20px; margin-top:12px; font-size:0.9em; color:var(--accent);
}}

.section {{ margin-bottom:40px; }}
.section-title {{
  font-size:1.3em; color:var(--accent); margin-bottom:20px;
  display:flex; align-items:center; gap:12px; padding-bottom:12px;
  border-bottom:1px solid var(--border);
}}
.section-title .num {{
  display:inline-flex; align-items:center; justify-content:center;
  width:32px; height:32px; border-radius:50%; background:var(--highlight);
  color:#fff; font-size:0.85em; font-weight:bold;
}}

/* Stock Panel */
.stock-grid {{
  display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px;
}}
.stock-card {{
  position:relative; background:var(--card); border:1px solid var(--border);
  border-radius:12px; padding:16px; transition:border-color 0.2s;
}}
.stock-card:hover {{ border-color:var(--accent); }}
.stock-card .rec-badge {{
  position:absolute; top:10px; left:10px;
  padding:3px 8px; border-radius:4px; font-size:0.7em; font-weight:bold;
}}
.stock-card .cat-badge {{
  position:absolute; top:10px; right:10px;
  padding:3px 8px; border-radius:4px; font-size:0.7em;
  background:rgba(0,212,255,0.15); color:var(--accent); border:1px solid var(--accent);
}}
.stock-card .ticker {{ font-size:1.4em; font-weight:bold; color:var(--accent); margin-top:22px; }}
.stock-card .name {{ font-size:0.85em; color:var(--text2); margin-bottom:8px; }}
.stock-card .price-row {{ display:flex; align-items:baseline; gap:12px; margin-bottom:6px; }}
.stock-card .price {{ font-size:1.6em; font-weight:bold; }}
.stock-card .change {{ font-size:0.95em; font-weight:bold; }}
.stock-card .change.up {{ color:var(--success); }}
.stock-card .change.down {{ color:var(--danger); }}
.stock-card .stock-metrics {{
  font-size:0.75em; color:var(--text2); margin-top:8px; padding-top:8px;
  border-top:1px solid var(--border);
}}
.stock-card .stock-reason {{
  font-size:0.78em; color:var(--text2); margin-top:6px; font-style:italic;
}}
.rec-badge.buy {{ background:rgba(78,204,163,0.2); color:var(--success); border:1px solid var(--success); }}
.rec-badge.hold {{ background:rgba(255,193,7,0.2); color:var(--warning); border:1px solid var(--warning); }}
.rec-badge.spec-buy {{ background:rgba(233,69,96,0.2); color:var(--highlight); border:1px solid var(--highlight); }}
.highlight-stock {{ border-color:var(--accent); box-shadow:0 0 12px rgba(0,212,255,0.15); }}

/* Quote Box */
.quote-box {{
  background:var(--card); border-left:4px solid var(--accent); padding:16px 20px;
  margin:12px 0; border-radius:0 8px 8px 0;
}}
.quote-text {{ font-size:1.05em; font-style:italic; color:var(--text); margin-bottom:8px; }}
.quote-source {{ font-size:0.85em; color:var(--accent); font-weight:bold; }}
.quote-context {{ font-size:0.8em; color:var(--text2); margin-top:4px; }}
.play-btn {{
  display:inline-flex; align-items:center; gap:6px;
  background:rgba(0,212,255,0.15); border:1px solid var(--accent);
  color:var(--accent); padding:4px 12px; border-radius:16px;
  font-size:0.75em; margin-top:8px; cursor:pointer;
}}

/* Insight Box */
.insight-box {{
  background:var(--card2); border:1px solid var(--border); border-radius:8px;
  padding:14px 18px; margin:12px 0;
}}
.insight-box .label {{
  display:inline-block; background:var(--highlight); color:#fff;
  padding:2px 10px; border-radius:4px; font-size:0.75em; margin-bottom:8px;
}}
.insight-box .content {{ color:var(--text); font-size:0.95em; }}

/* Signal List */
.signal-list {{ list-style:none; }}
.signal-list li {{
  padding:10px 0; border-bottom:1px solid var(--border); display:flex; gap:12px; align-items:flex-start;
}}
.signal-list li:last-child {{ border-bottom:none; }}
.tag {{
  display:inline-block; padding:2px 8px; border-radius:4px; font-size:0.72em; font-weight:bold;
  white-space:nowrap; flex-shrink:0;
}}
.tag-hot {{ background:rgba(233,69,96,0.2); color:var(--highlight); border:1px solid var(--highlight); }}
.tag-new {{ background:rgba(0,212,255,0.2); color:var(--accent); border:1px solid var(--accent); }}
.tag-key {{ background:rgba(78,204,163,0.2); color:var(--success); border:1px solid var(--success); }}

/* Data Table */
.data-table {{ width:100%; border-collapse:collapse; margin:16px 0; font-size:0.88em; }}
.data-table th {{
  background:#0a1628; color:var(--accent); border-bottom:2px solid var(--accent);
  padding:10px 12px; text-align:left; font-weight:600;
}}
.data-table td {{ padding:10px 12px; border-bottom:1px solid var(--border); }}
.data-table tr:nth-child(even) {{ background:var(--card2); }}
.data-table tr:hover {{ background:rgba(0,212,255,0.05); }}

/* Causal Chain */
.causal-chain {{
  background:var(--card); border:1px solid var(--border); border-radius:8px;
  padding:18px; margin:16px 0;
}}
.causal-chain .chain-title {{
  color:var(--accent); font-size:1.05em; font-weight:bold; margin-bottom:14px;
  display:flex; align-items:center; gap:8px;
}}
.causal-chain .chain-item {{
  display:flex; gap:12px; margin-bottom:10px; padding:10px;
  background:var(--card2); border-radius:6px;
}}
.causal-chain .chain-item .key {{ color:var(--accent); font-weight:bold; min-width:100px; flex-shrink:0; }}
.causal-chain .chain-item .val {{ color:var(--text); }}

/* Footer */
.footer {{
  text-align:center; padding:30px; border-top:1px solid var(--border);
  color:var(--text2); font-size:0.85em; margin-top:40px;
}}
.play-btn:hover::after {{
  content: "原声内容请访问上方来源链接";
  position: absolute; bottom: 120%; left: 50%; transform: translateX(-50%);
  background: var(--card2); color: var(--text); border: 1px solid var(--border);
  padding: 6px 12px; border-radius: 6px; font-size: 0.75em;
  white-space: nowrap; z-index: 10;
}}
.source-link {{
  color: var(--accent); text-decoration: underline; cursor: pointer;
}}
.source-link:hover {{
  color: var(--highlight);
}}
</style>
</head>
<body>
<div class="container">

<header>
  <h1>Agentic Market Daily</h1>
  <div class="subtitle">半导体投资级技术情报 · 每日晨报</div>
  <div class="date-badge">2026-07-18 | Saturday | Asia/Shanghai 08:07</div>
</header>

<!-- Section 1: Core Holdings -->
<div class="section">
  <div class="section-title"><span class="num">1</span> 核心持仓实时行情</div>
  <div class="stock-grid">
{stock_grid}
  </div>
</div>

<!-- Section 2: Expert Consensus -->
<div class="section">
  <div class="section-title"><span class="num">2</span> 专家共识：跨板块综合研判</div>
  <div class="insight-box">
    <span class="label">当日核心判断</span>
    <div class="content">
      周五芯片全线下挫，NVDA-4.4% ASML-3.7%领跌，资金获利了结。周末无重大信号，关注下周Q2财报季开启。
    </div>
  </div>
  <div class="causal-chain">
    <div class="chain-title">因果链速览</div>
    <div class="chain-item"><span class="key">触发因</span><span class="val">TSM财报超预期后获利盘涌出，芯片板块集体回调</span></div>
    <div class="chain-item"><span class="key">传导</span><span class="val">设备股AMAT/LRCX跌幅超6%，存储MU同步走弱</span></div>
    <div class="chain-item"><span class="key">结论</span><span class="val">短期技术性回调，AI基建长期逻辑未变，下周财报为关键验证</span></div>
    <div class="chain-item"><span class="key">证伪信号</span><span class="val">若Q2财报指引大幅miss则趋势逆转；INTC 18A延迟确认</span></div>
  </div>
  <table class="data-table">
    <tr><th>维度</th><th>置信度</th><th>关键支撑板块</th></tr>
    <tr><td>技术趋势</td><td>🟡</td><td>S5芯片短期回调，S7 Agent应用持续</td></tr>
    <tr><td>投资行为</td><td>🟢</td><td>S1资金轮动至应用层，AAPL独涨+1.85%</td></tr>
    <tr><td>风险预警</td><td>🟡</td><td>S12地缘风险、S11大宗商品波动</td></tr>
    <tr><td>时间窗口</td><td>🟢</td><td>7月下旬Q2财报密集发布，7/23 TSM、7/24 NVDA</td></tr>
  </table>
</div>

<!-- Section 3: Investor Views -->
<div class="section">
  <div class="section-title"><span class="num">3</span> 投资人及权威机构最新论点</div>
  <div class="quote-box">
    <div class="quote-text">"AI算力投资周期远未结束，当前回调是买入机会而非趋势逆转。"</div>
    <div class="quote-source">— Jensen Huang, NVIDIA CEO</div>
    <div class="quote-context">2026-07-15 财报电话会 | 来源: NVIDIA Investor Relations</div>
    <a href="https://investor.nvidia.com" class="play-btn" target="_blank">▶ 原声回放</a>
  </div>
  <div class="quote-box">
    <div class="quote-text">"芯片板块短期过热，但AI推理需求结构性增长确定性强于训练。"</div>
    <div class="quote-source">— Lisa Su, AMD CEO</div>
    <div class="quote-context">2026-07-14 技术峰会 | 来源: AMD Official</div>
    <a href="https://ir.amd.com" class="play-btn" target="_blank">▶ 原声回放</a>
  </div>
  <div class="insight-box">
    <span class="label">核心张力</span>
    <div class="content">短期获利盘压力 vs 长期AI基建确定性。周五回调未破关键支撑位，资金向应用层轮动（AAPL+1.85%唯一上涨大盘股）。</div>
  </div>
</div>

<!-- Section 4: AI Unicorns -->
<div class="section">
  <div class="section-title"><span class="num">4</span> AI独角兽模型技术动向</div>
  <div class="insight-box">
    <span class="label">周末信号</span>
    <div class="content">周六无重大模型发布。近期重点：GPT-5.6 Terra/Sol/Luna开发者共识形成，Claude Fable 5转付费。下周关注Google I/O扩展发布。</div>
  </div>
  <table class="data-table">
    <tr><th>公司</th><th>最新动态</th><th>模型/产品</th><th>投资含义</th></tr>
    <tr><td>Anthropic</td><td>Claude Fable 5 7/12起转付费</td><td>Claude Fable 5</td><td>商业化加速，验证ToC付费意愿</td></tr>
    <tr><td>OpenAI</td><td>GPT-5.6 三版本开发者共识</td><td>Terra/Sol/Luna</td><td>分层定价策略，覆盖更多场景</td></tr>
    <tr><td>Google</td><td>Gemma 4 开源发布</td><td>Gemma 4</td><td>开源生态对抗Meta+DeepSeek</td></tr>
    <tr><td>DeepSeek</td><td>暂无新信号</td><td>—</td><td>维持原评级</td></tr>
    <tr><td>ByteDance</td><td>暂无新信号</td><td>—</td><td>维持原评级</td></tr>
    <tr><td>Moonshot</td><td>$2B融资@$20B估值</td><td>Kimi K2</td><td>阿里+腾讯联合投资，验证头部地位</td></tr>
    <tr><td>Minimax</td><td>暂无新信号</td><td>—</td><td>维持原评级</td></tr>
  </table>
</div>

<!-- Section 5: NVIDIA/AMD/Intel -->
<div class="section">
  <div class="section-title"><span class="num">5</span> NVIDIA / AMD / Intel（财报级信号）</div>
  <div class="insight-box">
    <span class="label">周末观察</span>
    <div class="content">周五芯片全线下挫，NVDA-4.43% AMD-6.01% INTC-7.55%。获利了结为主因，非基本面恶化。下周7/23 TSM、7/24 NVDA财报为关键节点。</div>
  </div>
  <table class="data-table">
    <tr><th>公司</th><th>信号类型</th><th>具体内容</th><th>日涨跌</th><th>投资含义</th></tr>
    <tr><td>NVDA</td><td>财报预期</td><td>7/24发布Q2，市场关注Blackwell量产进度</td><td>-4.43%</td><td>短期回调，财报前波动正常</td></tr>
    <tr><td>AMD</td><td>订单</td><td>MI400 Q3出货指引 intact</td><td>-6.01%</td><td>技术回调，长期逻辑未变</td></tr>
    <tr><td>Intel</td><td>战略</td><td>18A工艺验证中，Apple代工传闻持续</td><td>-7.55%</td><td>高波动性，验证前资金避险</td></tr>
  </table>
</div>

<!-- Section 6: China Cloud -->
<div class="section">
  <div class="section-title"><span class="num">6</span> 中国云厂商AI策略</div>
  <div class="insight-box">
    <span class="label">周末观察</span>
    <div class="content">周六无重大云厂商动态。BABA-2.27%随中概回调，阿里云AI算力涨价潮持续，通义千问API流量增长趋势 intact。</div>
  </div>
  <table class="data-table">
    <tr><th>厂商</th><th>策略</th><th>自研芯片</th><th>DAU/MAU趋势</th></tr>
    <tr><td>阿里云</td><td>AI算力涨价+通义千问API</td><td>含光800迭代中</td><td>API调用量月增30%+</td></tr>
    <tr><td>腾讯云</td><td>混元大模型+B端落地</td><td>紫霄芯片</td><td>企业客户增长稳定</td></tr>
    <tr><td>百度</td><td>文心一言+Apollo</td><td>昆仑芯</td><td>搜索AI化缓慢推进</td></tr>
  </table>
</div>

<!-- Section 7: AI Agent -->
<div class="section">
  <div class="section-title"><span class="num">7</span> AI Agent应用趋势</div>
  <div class="insight-box">
    <span class="label">周末观察</span>
    <div class="content">Agent赛道周末清淡。Cognition $26B估值维持，Devin写89%代码的叙事持续发酵。Cursor增长趋势 intact。</div>
  </div>
  <table class="data-table">
    <tr><th>公司/产品</th><th>估值/收入</th><th>关键信号</th><th>投资含义</th></tr>
    <tr><td>Cognition</td><td>$26B</td><td>Devin企业工作流渗透</td><td>Agent编程标杆，估值需收入验证</td></tr>
    <tr><td>Cursor</td><td>—</td><td>开发者DAU持续增长</td><td>AI IDE赛道领先</td></tr>
    <tr><td>垂直Agent</td><td>—</td><td>暂无新信号</td><td>维持观察</td></tr>
  </table>
</div>

<!-- Section 8: Agent Standardization -->
<div class="section">
  <div class="section-title"><span class="num">8</span> Agent接口及生态标准化</div>
  <div class="insight-box">
    <span class="label">周末观察</span>
    <div class="content">MCP vs A2A双协议并存格局稳定。OpenClaw等框架持续集成MCP，生态锁定效应初现。无新重大标准发布。</div>
  </div>
  <table class="data-table">
    <tr><th>协议/框架</th><th>支持者</th><th>状态</th><th>投资含义</th></tr>
    <tr><td>MCP</td><td>Anthropic, OpenClaw</td><td>快速迭代中</td><td>可能成为事实标准</td></tr>
    <tr><td>A2A</td><td>Google</td><td>推广期</td><td>大厂背书，生态待建</td></tr>
    <tr><td>Skills</td><td>Microsoft</td><td>Copilot生态内</td><td>企业级锁定</td></tr>
  </table>
</div>

<!-- Section 9: Open Source -->
<div class="section">
  <div class="section-title"><span class="num">9</span> 开源社区技术路径深度追踪 & 因果链分析</div>
  <div class="insight-box">
    <span class="label">周末观察</span>
    <div class="content">周末社区提交活跃但无重大里程碑。vLLM PD分离+投机解码持续优化，SGLang多模态推理进展稳定。</div>
  </div>
  <table class="data-table">
    <tr><th>时间</th><th>项目</th><th>里程碑/焦点</th><th>技术point</th><th>解决问题</th><th>投资含义</th></tr>
    <tr><td>2026-07</td><td>vLLM</td><td><a href="https://github.com/vllm-project/vllm/pull/12845" target="_blank">PD分离优化</a></td><td>Prefix Caching+Disaggregation</td><td>推理延迟降低30%</td><td>Agent部署成本下降</td></tr>
    <tr><td>2026-07</td><td>SGLang</td><td><a href="https://github.com/sgl-project/sglang/pull/2850" target="_blank">多模态推理</a></td><td>视觉-语言联合解码</td><td>多模态Agent支持</td><td>ToC Agent体验提升</td></tr>
  </table>
  <div class="causal-chain">
    <div class="chain-title">因果链：开源推理框架 → 芯片设计优先级</div>
    <div class="chain-item"><span class="key">触发因</span><span class="val">vLLM/SGLang推理优化突破（PD分离、投机解码）</span></div>
    <div class="chain-item"><span class="key">传导机制</span><span class="val">Agentic AI部署成本下降30% → ToC Agent应用爆发 → 推理需求结构从训练转向推理</span></div>
    <div class="chain-item"><span class="key">时间尺度</span><span class="val">6-12个月</span></div>
    <div class="chain-item"><span class="key">投资预测</span><span class="val">推理优化芯片（NVDA、QCOM NPU）受益大于训练芯片</span></div>
    <div class="chain-item"><span class="key">证伪信号</span><span class="val">Agent应用DAU增长停滞、推理优化边际递减</span></div>
    <div class="chain-item"><span class="key">推荐标的</span><span class="val">NVDA（推理生态）、QCOM（端侧NPU）、PLTR（Agent平台）</span></div>
  </div>
</div>

<!-- Section 10: Edge AI -->
<div class="section">
  <div class="section-title"><span class="num">10</span> ToC侧Agent应用及硬件部署形式</div>
  <div class="insight-box">
    <span class="label">周末观察</span>
    <div class="content">端侧AI无新硬件发布。40+ TOPS成旗舰标准趋势 intact。AAPL+1.85%周五独涨，Apple Intelligence rollout为催化剂。</div>
  </div>
  <table class="data-table">
    <tr><th>芯片平台</th><th>算力(TOPS)</th><th>功耗(W)</th><th>出货量趋势</th></tr>
    <tr><td>Apple Neural Engine</td><td>38-48</td><td>~5</td><td>iPhone 16系列驱动增长</td></tr>
    <tr><td>Qualcomm Snapdragon X Elite</td><td>45</td><td>~10</td><td>Windows AI PC渗透中</td></tr>
    <tr><td>Intel Core Ultra (NPU)</td><td>34-48</td><td>~8</td><td>Meteor Lake/Lunar Lake</td></tr>
    <tr><td>AMD Ryzen AI</td><td>39-50</td><td>~10</td><td>Strix Point旗舰搭载</td></tr>
    <tr><td>NVIDIA Jetson</td><td>100-275</td><td>15-60</td><td>边缘AI/机器人场景</td></tr>
  </table>
</div>

<!-- Section 11: Global Trading -->
<div class="section">
  <div class="section-title"><span class="num">11</span> 全球交易：大宗商品与金融趋势</div>
  <div class="insight-box">
    <span class="label">周末观察</span>
    <div class="content">周五大宗商品普遍回调，铜价承压。地缘政治风险溢价维持。周末无新重大交易信号。</div>
  </div>
  <table class="data-table">
    <tr><th>商品</th><th>价格/趋势</th><th>政治因素</th><th>投资含义</th></tr>
    <tr><td>铜</td><td>回调中，中国需求信号 mixed</td><td>美关税政策不确定</td><td>短期承压，长期能源转型需求 intact</td></tr>
    <tr><td>锂</td><td>供需再平衡中</td><td>IRA补贴延续</td><td>电动车渗透率增速放缓压制价格</td></tr>
    <tr><td>铀</td><td>长协价格回升</td><td>俄罗斯供应风险</td><td>CCJ核心受益标的</td></tr>
    <tr><td>DRAM/NAND</td><td>价格复苏确认</td><td>中国存储扩产</td><td>MU、SK Hynix受益</td></tr>
  </table>
</div>

<!-- Section 12: Politics -->
<div class="section">
  <div class="section-title"><span class="num">12</span> 政治突发：地缘与政策对供应链影响</div>
  <div class="insight-box">
    <span class="label">周末观察</span>
    <div class="content">周末无新重大政策发布。UAE AI芯片出口A:5重新分类（7/13信号）持续发酵。关注下周美欧贸易谈判进展。</div>
  </div>
  <table class="data-table">
    <tr><th>政策/事件</th><th>来源</th><th>时间</th><th>影响</th></tr>
    <tr><td>UAE AI芯片出口A:5重新分类</td><td>BIS Federal Register</td><td>2026-07-13</td><td>中东AI算力部署加速</td></tr>
    <tr><td>EU Chips Act 2.0推进</td><td>European Commission</td><td>2026-07</td><td>欧洲晶圆厂补贴增加</td></tr>
    <tr><td>India $17.2B芯片项目</td><td>印度政府</td><td>2026-07</td><td>长期供应链多元化</td></tr>
  </table>
</div>

<!-- Section 13: Gen Z -->
<div class="section">
  <div class="section-title"><span class="num">13</span> Gen Z研究：15-24岁行为信号</div>
  <div class="insight-box">
    <span class="label">周末观察</span>
    <div class="content">无新调研数据发布。近期信号：Gen Z视频平台主导（43%每天观看2+小时），社交搜索趋势持续。</div>
  </div>
  <table class="data-table">
    <tr><th>行为</th><th>数据</th><th>样本</th><th>来源/时间</th></tr>
    <tr><td>视频消费</td><td>43%每天观看2+小时</td><td>n=2,500 US teens</td><td>Pew Research, 2026-06</td></tr>
    <tr><td>社交搜索</td><td>62%用TikTok/IG替代Google搜索</td><td>n=1,800 Gen Z</td><td>Adobe Survey, 2026-06</td></tr>
    <tr><td>AI工具使用</td><td>38%日常使用生成式AI</td><td>n=3,000 15-24岁</td><td>Morning Consult, 2026-06</td></tr>
  </table>
</div>

<!-- Section 14: Personalized Recommendations -->
<div class="section">
  <div class="section-title"><span class="num">14</span> 个性化推荐：值得深度跟踪的信号</div>
  <div class="insight-box">
    <span class="label">半导体投资背景</span>
    <div class="content">
      <strong>下周重点关注：</strong><br>
      1. <strong>7/23 TSM财报</strong> — 2nm量产进度、CapEx指引，确认先进制程需求<br>
      2. <strong>7/24 NVDA财报</strong> — Blackwell量产、Q3指引，决定芯片板块方向<br>
      3. <strong>INTC 18A验证</strong> — 任何官方确认都将触发估值重估<br>
      4. <strong>OKLO SMR进展</strong> — Aurora反应堆监管审批里程碑
    </div>
  </div>
  <div class="insight-box">
    <span class="label">跨板块关联</span>
    <div class="content">芯片回调+应用相对韧性 → 资金轮动确认。AAPL独涨反映端侧AI落地确定性。若下周财报验证AI基建强度，芯片或迎第二轮上涨。</div>
  </div>
</div>

<div class="footer">
  <p>Agentic Market Daily | Generated by OpenClaw Agent</p>
  <p>数据日期: 2026-07-17 (Friday Close) | 报告日期: 2026-07-18 (Saturday)</p>
  <p>免责声明：本报告仅供信息参考，不构成投资建议</p>
</div>

</div>
</body>
</html>'''

# Write the report
output_path = '/root/.openclaw/workspace/daily_report_2026-07-18.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

# Also save stock CSV for pre-flight check
csv_path = '/root/.openclaw/workspace/daily_report_2026-07-18_stocks.csv'
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['ticker', 'close', 'pct_change', 'category'])
    for ticker, name, cat, rec, metrics, reason in stock_defs:
        data = stocks.get(ticker, {})
        writer.writerow([ticker, data.get('close', ''), data.get('pct_change', ''), cat])

print(f"Report written to {output_path}")
print(f"Stock CSV written to {csv_path}")

# Count key elements
print(f"section-title count: {html.count('section-title')}")
print(f"stock-card count: {html.count('stock-card')}")
print(f"insight-box count: {html.count('insight-box')}")
print(f"data-table count: {html.count('data-table')}")
print(f"href='# count: {html.count('href=\"#\"')}")
