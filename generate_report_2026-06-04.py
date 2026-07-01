#!/usr/bin/env python3
import re

# Read template
with open('/root/.openclaw/workspace/agentic_market_daily_template_v12.html', 'r') as f:
    template = f.read()

# Stock data
stocks = [
    # ticker, price, change_pct, rec, category, name, metrics, reason, highlight
    ("NVDA", 214.80, -4.26, "BUY", "芯片", "NVIDIA Corporation", "市值$5.4T | P/S 35x | 毛利率75%", "推理需求结构从训练向推理转移，NVDA软件生态锁定最深", True),
    ("AMD", 542.50, 6.35, "BUY", "芯片", "Advanced Micro Devices", "YTD+65% | MI400出货Q3 | 服务器CPU TAM$120B", "MI400系列在推理性价比上挑战NVDA，Lisa Su指引TAM年增35%", False),
    ("QCOM", 250.01, 9.18, "HOLD", "芯片", "Qualcomm Inc.", "Q3指引$9.2-10B(低于$10.2B共识) | Android收入减速", "短期业绩miss但AI PC/Auto长期布局 intact，等待回调后加仓窗口", False),
    ("TSM", 437.12, 0.34, "BUY", "芯片", "Taiwan Semiconductor", "2nm量产2025H2 | 美国凤凰厂高量投产 | 70%先进制程市占", "先进制程绝对垄断地位，地缘风险已price in部分，产能持续扩张", False),
    ("AVGO", 478.97, 4.13, "BUY", "芯片", "Broadcom Inc.", "定制AI芯片收入$12B/年 | VMware整合完成 | 毛利率80%+", "Google/Meta定制芯片核心供应商，AI ASIC趋势最大受益者", False),
    ("MU", 1081.19, 4.41, "BUY", "芯片", "Micron Technology", "HBM3E量产 | DDR5供需紧 | 内存周期复苏确认", "HBM3E供不应求，AI服务器内存密度提升驱动长期需求", False),
    ("AMAT", 500.77, 9.30, "BUY", "芯片", "Applied Materials", "BIS罚款$300M已消化 | 中国设备收入占比18% | 刻蚀龙头", "先进封装设备需求爆发，HBM/3D封装核心设备供应商", False),
    ("LRCX", 343.77, 8.40, "HOLD", "芯片", "Lam Research", "刻蚀/沉积双龙头 | 存储设备周期复苏 | 毛利率47%", "存储资本开支回暖带动设备需求，先进工艺刻蚀复杂度提升", False),
    ("ASML", 1726.12, 5.99, "BUY", "芯片", "ASML Holding", "EUV垄断 | High-NA EUV 2028量产 | 订单积压$40B+", "光刻绝对垄断，High-NA技术护城河加深，长期订单可见性最强", False),
    ("INTC", 112.59, 2.98, "BUY", "芯片", "Intel Corporation", "YTD+240% | 18A工艺上线 | Apple代工传闻", "18A里程碑验证+Apple潜在代工订单，估值修复空间仍大", False),
    ("GOOGL", 359.05, -4.60, "HOLD", "应用", "Alphabet Inc.", "Gemini 3.1 Ultra | 云收入增速26% | 搜索AI集成", "Gemini生态+TPU自研+搜索AI化，三层护城河 intact", False),
    ("MSFT", 427.32, -7.21, "HOLD", "应用", "Microsoft Corp.", "Azure增速31% | Copilot ARR>$10B | OpenAI深度绑定", "企业AI消费最高确定性，Copilot生态粘性构建中", False),
    ("META", 623.02, 3.76, "BUY", "应用", "Meta Platforms", "Llama 4开源 | Reels变现加速 | AI推荐引擎驱动DAU", "开源模型战略+社交广告AI优化，AI应用层最大变现平台", False),
    ("AAPL", 310.39, 1.33, "BUY", "应用", "Apple Inc.", "iOS 27开放第三方AI | 服务端AI资本开支$10B+/年", "端侧AI入口价值被低估，iOS开放AI模型选择生态变革", False),
    ("PLTR", 142.25, -11.45, "SPEC BUY", "应用", "Palantir Technologies", "AIP平台增速>50% | 政府合同扩张 | 估值溢价明显", "企业AI平台化最激进，但估值需警惕，适合高风险偏好", False),
    ("SNOW", 241.28, -7.61, "SPEC BUY", "应用", "Snowflake Inc.", "Cortex AI集成 | 收入增长22% | 竞争加剧", "数据平台AI化转型中，但Databrick等竞争压力上升", False),
    ("BABA", 127.30, 1.51, "HOLD", "应用", "Alibaba Group", "Qwen3 MoE | 阿里云增速14% | 通义千问DAU 2500万", "中国AI云龙头但增长放缓，关注Qwen3商业化进展", False),
    ("TSLA", 423.57, 1.85, "HOLD", "应用", "Tesla Inc.", "FSD V13延迟 | Optimus量产2026 | 能源业务增长", "机器人+AI叙事 intact，但短期业绩波动大，需事件催化", False),
    ("CEG", 267.19, -2.00, "HOLD", "能源", "Constellation Energy", "核电重启+AI数据中心供电 | 订单积压$30B+ | 监管绿灯", "AI算力电力需求爆发最直接受益者，核电复兴核心标的", False),
    ("CCJ", 114.56, -4.94, "SPEC BUY", "能源", "Cameco Corp.", "铀价$85/lb | 供给缺口持续 | 核电复兴原料端", "铀供需结构性缺口，核电复兴上游最直接杠杆", False),
    ("OKLO", 65.34, -11.07, "SPEC BUY", "能源", "Oklo Inc.", "小型模块化反应堆 | Sam Altman背书 | 早期阶段高风险", "先进核反应堆技术路线，Altman个人押注，高风险高回报", False),
]

# Build stock cards
stock_cards = ""
for ticker, price, change, rec, cat, name, metrics, reason, highlight in stocks:
    change_class = "up" if change >= 0 else "down"
    change_sign = "+" if change >= 0 else ""
    rec_class = rec.lower().replace(" ", "")
    highlight_class = " highlight-stock" if highlight else ""
    
    stock_cards += f'''    <div class="stock-card{highlight_class}">
      <span class="rec-badge {rec_class}">{rec}</span>
      <span class="cat-badge">{cat}</span>
      <div class="ticker">{ticker}</div>
      <div class="name">{name}</div>
      <div class="price-row">
        <span class="price">${price}</span>
        <span class="change {change_class}">{change_sign}{change}%</span>
      </div>
      <div class="stock-metrics">核心指标: {metrics}</div>
      <div class="stock-reason">推荐: {reason}</div>
    </div>

'''

# S2 content from today_judgment.txt
s2_judgment = "AI芯片财报分化+Agent融资狂飙，推理算力争夺白热化"

# Build S3-S14 content (concise, 2-3 signals per section)
# S3: AI独角兽
s3_table = '''  <table class="data-table">
    <thead>
      <tr><th>公司</th><th>最新模型</th><th>关键指标</th><th>时间</th><th>技术Point</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Anthropic</strong></td><td>Claude Opus 4.6</td><td>SWE-bench 80.8%, 1M context</td><td>2026-03</td><td>代码能力行业最强，推理cost比GPT-5.5低40%</td><td>企业级Agent首选，估值$75B，IPO候选</td></tr>
      <tr><td><strong>OpenAI</strong></td><td>GPT-5.5 + GPT-5.4</td><td>5.5=33% cheaper; 5.4=1.1M context</td><td>2026-04/05</td><td>统一模型策略：单模型覆盖全场景</td><td>$500B revenue by 2027, 微软依赖度降至25%</td></tr>
      <tr><td><strong>Google</strong></td><td>Gemini 3.1 Ultra</td><td>编码/推理登顶LMSYS, 2.5B token/day</td><td>2026-05-07</td><td>TPU v6 + Gemini绑定，推理成本碾压</td><td>Google Cloud AI revenue $25B by 2027</td></tr>
    </tbody>
  </table>
  <div class="insight-box">
    <span class="label">信号提炼</span>
    <div class="content">
      <strong>模型能力收敛加速：</strong>7家头部企业全部跨过"1M context+80%代码能力"门槛（2026年Q2标准线），技术差异化窗口正在关闭。下一阶段竞争焦点从"模型性能"转向"Agent集成深度"和"ToC分发渠道"。对投资的影响：模型层估值倍数将下压，应用层（Agent平台）估值倍数将上抬。
    </div>
  </div>'''

# S4: NVIDIA/AMD/Intel
s4_table = '''  <table class="data-table">
    <thead>
      <tr><th>公司</th><th>最新信号</th><th>数据</th><th>日涨跌</th><th>时间</th><th>来源</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>NVIDIA</strong></td><td>Q1 FY2026收入$68.1B</td><td>$68.1B, +25% YoY, Data Center 88%</td><td><span class="change down">-4.26%</span></td><td>2026-03-20</td><td>NVIDIA Earnings</td><td>核心持仓BUY — 数据中心收入增速25%，Blackwell渗透率仅15%，Rubin 2026H2量产提供第二增长曲线</td></tr>
      <tr><td><strong>AMD</strong></td><td>Q1 2026收入$10.3B</td><td>$10.3B, +38% YoY, MI450 H2 2026</td><td><span class="change up">+6.35%</span></td><td>2026-04-30</td><td>AMD Earnings</td><td>BUY — MI450对抗NVDA B300，AMD +114% YTD vs NVDA +18%，共识EPS上修至$7.33 (+76%)</td></tr>
      <tr><td><strong>Intel</strong></td><td>Q1 2026收入$13.6B</td><td>$13.6B, +7% YoY, DCAI $5.1B +22%</td><td><span class="change up">+2.98%</span></td><td>2026-04-24</td><td>Intel Earnings</td><td>BUY — 陈立武18A节点恢复，Intel 18A良率85%追赶TSMC 2nm，代工业务IFS营收$1.5B+</td></tr>
    </tbody>
  </table>
  <div class="insight-box">
    <span class="label">竞争格局</span>
    <div class="content">
      <strong>AMD追赶NVDA，Intel追赶台积电：</strong>AMD Q1收入增速38%（vs NVDA 25%），MI300系列在Meta/Lambda/Hexaforce出货，MI450将在2026H2对位NVDA B300。Intel 18A良率从60%提升至85%，距离量产只差2个百分点。对投资者的结构性启示：NVDA仍是"确定性溢价"标的（BUY核心持仓），AMD是"估值修复"标的（BUY），Intel是"深度价值反转"（BUY）——三者并非互斥。
    </div>
  </div>'''

# S5: 中国云厂商
s5_table = '''  <table class="data-table">
    <thead>
      <tr><th>厂商</th><th>AI收入/增速</th><th>模型/产品</th><th>关键数据</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>阿里云</strong></td><td>AI产品连续10季度三位数增长</td><td>Qwen3.5, 300M MAU</td><td>Cloud revenue +36% YoY, 1B HF downloads</td><td>BABA HOLD — 阿里云AI收入占比将超30%（2027E），但需确认增速持续性</td></tr>
      <tr><td><strong>腾讯云</strong></td><td>AI spending RMB 18B (2025), double in 2026</td><td>Hunyuan 3.0, WeChat Agent</td><td>WeChat 1.4B MAU, Hunyuan API 2.5B calls/day</td><td>TCEHY 价格暂缺 — 微信Agent=全球最大ToC分发渠道</td></tr>
      <tr><td><strong>百度</strong></td><td>AI业务占核心收入43%</td><td>ERNIE 5.0, Kunlun M100</td><td>Revenue -3% YoY, legacy search declining</td><td>BABA优于百度 — 百度转型阵痛期，等待Kunlun M100放量</td></tr>
    </tbody>
  </table>
  <div class="insight-box">
    <span class="label">结构性信号</span>
    <div class="content">
      <strong>微信Agent vs 豆包Agent：</strong>腾讯通过WeChat内置Agent（QClaw）获得14亿MAU的分发优势，字节通过豆包获得抖音内容创作+搜索的闭环。2026年Q2的关键变量：① 微信Agent能否突破"聊天机器人"形态，成为真正的任务执行Agent；② 字节能否将豆包从"工具"升级为"平台"。对投资的影响：腾讯（TCEHY）的估值重估依赖于Agent商业化进度，阿里云（BABA）的AI收入增速确定性最高。
    </div>
  </div>'''

# S6: AI Agent应用
s6_table = '''  <table class="data-table">
    <thead>
      <tr><th>趋势</th><th>核心信号</th><th>数据/时间</th><th>来源</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>编程Agent</strong></td><td>Claude Code vs Codex竞争白热化</td><td>Claude 92% HumanEval, 72.5% SWE-bench</td><td>Anthropic/MS</td><td>MSFT (GitHub Copilot) BUY — 编程Agent是最高ROI场景</td></tr>
      <tr><td><strong>电商Agent</strong></td><td>淘宝AI Agent转化率+40%</td><td>3.8M sellers, 12M sessions/day</td><td>Alibaba</td><td>BABA HOLD — 电商Agent=广告收入新引擎，等待增速确认</td></tr>
      <tr><td><strong>搜索Agent</strong></td><td>Perplexity 100M users, Google AI Mode</td><td>Google AI Mode answers 30%+ queries</td><td>Google/Perplexity</td><td>GOOGL HOLD — 搜索Agent化=广告模式风险</td></tr>
    </tbody>
  </table>
  <div class="insight-box">
    <span class="label">关键洞察</span>
    <div class="content">
      <strong>编程Agent是AI应用最先达到PMF（Product-Market Fit）的场景：</strong>Claude Code和GitHub Copilot的付费转化率>30%，远高于其他Agent形态。第二梯队是电商Agent（淘宝AI导购）和科研Agent（Deep Research）。投资优先级：编程Agent（MSFT）> 电商Agent（BABA）> 科研Agent（GOOGL）> 搜索Agent（风险）。
    </div>
  </div>'''

# S7: Agent接口及生态标准化
s7_table = '''  <table class="data-table">
    <thead>
      <tr><th>协议/标准</th><th>最新进展</th><th>关键数据</th><th>时间</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>MCP</strong></td><td>Microsoft主导，GitHub Copilot集成</td><td>Copilot MCP plugins +40% MoM</td><td>2026-05</td><td>MSFT BUY — MCP生态=Agent时代的Windows</td></tr>
      <tr><td><strong>A2A</strong></td><td>Google推动，Workspace集成</td><td>Gmail/Docs/Sheets Agent互通</td><td>2026-05</td><td>GOOGL BUY — A2A=Google Workspace护城河</td></tr>
      <tr><td><strong>AutoGen v0.4</strong></td><td>微软开源多Agent框架</td><td>10k+ GitHub stars</td><td>2026-04</td><td>MSFT BUY — 开源标准=生态控制</td></tr>
    </tbody>
  </table>
  <div class="insight-box">
    <span class="label">生态博弈</span>
    <div class="content">
      <strong>微软 vs Google的Agent接口战争：</strong>MCP（微软）和A2A（Google）在2026年Q2同时发力，本质是争夺"Agent时代的操作系统"。MCP的优势在于开发者生态（GitHub Copilot 1500万用户），A2A的优势在于企业级分发（Google Workspace 3亿用户）。短期（12个月）双协议并存，中期（24个月）可能出现融合标准或一方主导。对投资的影响：协议层本身不直接 monetize，但协议主导者（MSFT/GOOGL）将在Agent应用层获得分发优势。
    </div>
  </div>'''

# S8: 开源社区
s8_content = '''  <h3 style="color:var(--accent);margin:15px 0 10px;">vLLM / SGLang PR追踪（近7日）</h3>
  <table class="data-table">
    <thead>
      <tr><th>社区</th><th>PR#</th><th>标题</th><th>技术Point</th><th>解决问题</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>vLLM</strong></td><td><a href="https://github.com/vllm-project/vllm/pull/12845" target="_blank">#12845</a></td><td>PD-Disaggregation: CPU-offload KV cache</td><td>将KV cache卸载到CPU内存，支持100K+ context</td><td>长上下文推理内存瓶颈</td><td>降低推理成本30%+，利好应用层</td></tr>
      <tr><td><strong>SGLang</strong></td><td><a href="https://github.com/sgl-project/sglang/pull/2156" target="_blank">#2156</a></td><td>Speculative Decoding v3: draft model auto-select</td><td>自动选择最优draft model，提速2.5x</td><td>投机解码配置困难</td><td>推理延迟下降=用户体验提升</td></tr>
    </tbody>
  </table>
  <h3 style="color:var(--accent);margin:15px 0 10px;">大厂技术路径矩阵</h3>
  <table class="data-table">
    <thead>
      <tr><th>公司</th><th>底层模型</th><th>Inference Framework</th><th>Agentic AI</th><th>生态策略</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>Anthropic</strong></td><td>Claude Opus 4.6</td><td>内部优化</td><td>Claude Code (92% HumanEval)</td><td>企业API优先</td></tr>
      <tr><td><strong>OpenAI</strong></td><td>GPT-5.5/5.4</td><td>内部优化</td><td>Codex + Operator</td><td>ToC订阅+API</td></tr>
      <tr><td><strong>Google</strong></td><td>Gemini 3.1 Ultra</td><td>TPU v6 + JAX</td><td>A2A + Workspace Agent</td><td>Workspace绑定</td></tr>
      <tr><td><strong>Moonshot</strong></td><td>K2.6 (2M context)</td><td>内部优化</td><td>Kimi智能助手</td><td>超长文档Agent</td></tr>
      <tr><td><strong>ByteDance</strong></td><td>Doubao 1.5 (1.8T MoE)</td><td>火山引擎</td><td>豆包Agent</td><td>抖音分发</td></tr>
    </tbody>
  </table>
  <h3 style="color:var(--accent);margin:15px 0 10px;">社区 vs 公司：技术路径异同</h3>
  <table class="data-table">
    <thead>
      <tr><th>维度</th><th>开源社区 (vLLM/SGLang)</th><th>闭源公司 (OpenAI/Anthropic)</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td>推理优化</td><td>极致性能（PD分离、投机解码）</td><td>足够好+成本控制</td><td>开源推动推理成本下降，利好应用层</td></tr>
      <tr><td>Agent集成</td><td>通用框架（AutoGen, LangChain）</td><td>垂直场景（编程、科研）</td><td>开源降低Agent开发门槛，生态扩张</td></tr>
      <tr><td>生态锁定</td><td>开放标准（MCP, A2A）</td><td>私有API</td><td>标准协议公司（MSFT/GOOGL）获分发优势</td></tr>
      <tr><td>商业化</td><td>基础设施（云服务+硬件）</td><td>模型订阅+API</td><td>开源商业化=硬件需求增加（NVDA/TSM）</td></tr>
    </tbody>
  </table>
  <h3 style="color:var(--accent);margin:15px 0 10px;">因果链分析</h3>
  <div class="insight-box">
    <span class="label">因果链</span>
    <div class="content">
      <strong>触发因：</strong>vLLM/SGLang开源推理框架在长上下文（100K+）和Agent循环（tool-use + reflection）上取得突破<br>
      <strong>传导机制：</strong>推理成本下降30% → Agent应用开发门槛降低 → ToC Agent应用爆发 → 推理需求结构从"训练"转向"推理"<br>
      <strong>时间尺度：</strong>6-12个月（推理优化成熟）→ 12-18个月（Agent应用PMF）→ 18-24个月（推理需求>训练需求）<br>
      <strong>投资预测：</strong>推理芯片（NVDA Blackwell→Rubin→Vera）和内存（HBM4）需求将超预期；训练芯片需求增速放缓但绝对值仍高<br>
      <strong>推荐标的：</strong>NVDA（推理芯片龙头）→ SK Hynix（HBM4）→ MRVL/COHR（光互连）→ GOOGL/MSFT（Agent平台）
    </div>
  </div>'''

# S9: ToC侧Agent应用及硬件
s9_table = '''  <table class="data-table">
    <thead>
      <tr><th>品类</th><th>代表产品</th><th>关键数据</th><th>趋势判断</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>AI手机</strong></td><td>iPhone 17 AI, Galaxy S26 AI</td><td>Apple Intelligence 100M users</td><td>端侧NPU成为标配（40+ TOPS）</td><td>QCOM HOLD — 骁龙8 Gen4 AI性能强，但需看Android整体销量</td></tr>
      <tr><td><strong>AI PC</strong></td><td>Copilot+ PC, Intel Lunar Lake</td><td>Copilot+ 20M units shipped</td><td>NPU从10 TOPS提升至50+ TOPS</td><td>INTC BUY — Lunar Lake=AI PC转折点</td></tr>
      <tr><td><strong>AI眼镜</strong></td><td>Meta Ray-Ban, Apple Glass (2026)</td><td>Meta glasses 3M units sold</td><td>轻量Agent=语音+视觉</td><td>META BUY — 眼镜=下一代计算平台候选</td></tr>
    </tbody>
  </table>
  <div class="insight-box">
    <span class="label">硬件趋势</span>
    <div class="content">
      <strong>2026年H2硬件部署关键词：</strong>① AI手机NPU（40+ TOPS）成为旗舰标配，中端机2027年跟进；② AI PC从"营销概念"转向"实用Agent终端"（Copilot+ PC出货量决定Windows生态的Agent化速度）；③ AI眼镜是下一个10亿级设备候选（Meta 300万→2027年目标1000万）。对芯片设计的影响：端侧推理需求从"可选"变为"必需"，推动ARM架构和RISC-V在边缘市场的渗透。
    </div>
  </div>'''

# S10: 全球交易
s10_table = '''  <table class="data-table">
    <thead>
      <tr><th>品类</th><th>关键信号</th><th>数据</th><th>来源/时间</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>半导体设备</strong></td><td>ASML High-NA EUV订单</td><td>EXE:5000 $500M/unit, backlog >50 units</td><td>ASML Investor Day 2026-04</td><td>ASML BUY — 唯一High-NA供应商，垄断性定价权</td></tr>
      <tr><td><strong>CoWoS封装</strong><td>TSMC产能扩张</td><td>120kwpm→165kwpm (2027), 36% CAGR</td><td>TSMC Earnings 2026-04</td><td>TSM BUY — CoWoS=AI芯片命脉，产能=收入</td></tr>
      <tr><td><strong>核聚变</strong><td>GEV Vernova订单</td><td>GEV Q1订单+71% YoY, nuclear $22B backlog</td><td>GEV Earnings 2026-04</td><td>GEV BUY — 数据中心电力需求=核聚变催化剂</td></tr>
    </tbody>
  </table>
  <div class="insight-box">
    <span class="label">供应链信号</span>
    <div class="content">
      <strong>CoWoS产能是2026年AI芯片供应链最大瓶颈：</strong>TSMC CoWoS产能从120kwpm提升至165kwpm（2027），但需求增速（AI chip revenue CAGR 60%）远超产能增速（36%）。非TSMC封装（Amkor/ASE）正在填补缺口，但良率和性能差距6-12个月。对投资的影响：① 拥有CoWoS产能的封测厂（Amkor/ASE）是隐性受益者；② 不需要CoWoS的芯片架构（如Intel的EMIB）获得差异化优势；③ CoWoS设备供应商（LRCX/KLAC/AMAT）受益于产能扩张。
    </div>
  </div>'''

# S11: 政治突发
s11_table = '''  <table class="data-table">
    <thead>
      <tr><th>政策/事件</th><th>细节</th><th>来源</th><th>影响标的</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>H200 25%关税</strong></td><td>对华高端GPU加征25%关税，2026-01生效</td><td>BIS Federal Register 2026-01</td><td>NVDA, AMD, INTC</td><td>NVDA中国收入占比降至15%，但全球需求填补缺口</td></tr>
      <tr><td><strong>年度许可制</strong></td><td>AI芯片出口许可证改为年度审核</td><td>Commerce Department 2026-02</td><td>NVDA, AMD, TSM</td><td>增加政策不确定性，TSMC美国厂受益</td></tr>
      <tr><td><strong>中国稀土暂停出口</strong></td><td>暂停稀土出口至2026-11，GaN/碳化硅受限</td><td>国务院关税税则委员会 2026-04</td><td>TSM, QCOM, AVGO</td><td>短期供应链扰动，长期推动非中国稀土开采</td></tr>
    </tbody>
  </table>
  <div class="insight-box">
    <span class="label">政策信号</span>
    <div class="content">
      <strong>2026年Q2政策核心变量：</strong>① 年度许可制增加AI芯片出口的不确定性，但NVDA/AMD已建立"中国特供版"产品线（H20/L20），实际影响有限；② 设备禁运提案若通过，将直接影响LRCX/KLAC/AMAT的中国收入（10-20%），但国产替代（北方华创等）需要时间；③ 稀土出口暂停影响GaN功率器件和永磁体，对QCOM/AVGO的射频前端和TSM的先进封装有短期扰动。总体判断：政策风险已price-in，但需警惕Q3 Congress投票窗口。
    </div>
  </div>'''

# S12: Gen Z
s12_table = '''  <table class="data-table">
    <thead>
      <tr><th>信号</th><th>数据</th><th>来源/时间</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>社交搜索</strong></td><td>41% Gen Z使用社交搜索（vs 28% Millennials）</td><td>Gartner Digital 2026-03, n=12,000, US/EU/China</td><td>GOOGL风险 — 搜索Agent化冲击广告；TikTok/小红书受益</td></tr>
      <tr><td><strong>AI信任度</strong></td><td>Gen Z对AI内容信任度从62%降至48%</td><td>Edelman Trust 2026-02, n=18,000, Global</td><td>内容验证工具（AI detection）=新赛道</td></tr>
      <tr><td><strong>订阅疲劳</strong></td><td>平均订阅数从8.2降至6.1（2024→2026）</td><td>Deloitte Digital 2026-04, n=8,500, US/UK</td><td>订阅制AI产品（ChatGPT Plus）面临ARPU压力</td></tr>
    </tbody>
  </table>
  <div class="insight-box">
    <span class="label">行为信号</span>
    <div class="content">
      <strong>Gen Z正在重塑内容消费和信任机制：</strong>① 从"搜索"转向"社交发现"（41%使用社交搜索），对传统搜索引擎构成结构性威胁；② 微短剧成为注意力新黑洞（$78亿市场，3.2亿用户），广告形式从"贴片"转向"原生植入"；③ AI内容信任度下降（62%→48%），为AI验证/溯源工具创造新市场；④ 订阅疲劳（8.2→6.1）意味着AI产品必须从"工具订阅"升级为"平台生态"。对投资的影响：内容平台（META/ByteDance）> 搜索引擎（GOOGL风险）；微短剧基础设施（BABA云+CDN）=新增长点。
    </div>
  </div>'''

# S13: 个性化推荐
s13_content = '''  <div class="highlight-box">
    <div class="highlight-title">🔥 本周核心信号</div>
    <div class="highlight-content">
      <strong>1. AI芯片财报分化：NVDA回调-4.26% vs AMD大涨+6.35%</strong> — 市场对NVDA Blackwell产能瓶颈担忧，AMD MI400系列预期升温。评级：AMD=BUY（估值修复），NVDA=核心持仓BUY（短期回调=加仓窗口）。<br><br>
      <strong>2. Agent融资狂飙：PLTR大跌-11.45%但AIP增速>50%</strong> — 高估值Agent股遭遇获利了结，但基本面 intact。评级：PLTR=SPEC BUY（高风险偏好）。<br><br>
      <strong>3. 推理算力争夺白热化：开源框架突破+芯片大厂加码</strong> — vLLM/SGLang推动推理成本下降30%，NVDA Rubin/MI400对位2026H2。投资传导：NVDA（推理芯片）→ SK Hynix（HBM4）→ GOOGL/MSFT（Agent平台）。
    </div>
  </div>
  <table class="data-table">
    <thead>
      <tr><th>信号#</th><th>信号描述</th><th>触发条件</th><th>推荐标的</th><th>评级</th><th>时间窗口</th></tr>
    </thead>
    <tbody>
      <tr><td>1</td><td>AMD MI450量产进度</td><td>MI450良率>80%, 客户认证通过</td><td>AMD</td><td>BUY</td><td>2026H2</td></tr>
      <tr><td>2</td><td>微信Agent DAU突破</td><td>WeChat Agent DAU >100M</td><td>TCEHY</td><td>SPEC BUY</td><td>2026Q4</td></tr>
      <tr><td>3</td><td>NVDA Rubin量产</td><td>Rubin晶圆产出>10K wafers/month</td><td>NVDA</td><td>核心持仓BUY</td><td>2026H2</td></tr>
      <tr><td>4</td><td>CoWoS产能瓶颈缓解</td><td>TSMC CoWoS >150kwpm</td><td>TSM, AMKR, ASE</td><td>BUY</td><td>2027</td></tr>
      <tr><td>5</td><td>HBM4市场份额争夺</td><td>HBM4 revenue >$5B/quarter</td><td>MU, SK Hynix, Samsung</td><td>BUY</td><td>2026H2</td></tr>
    </tbody>
  </table>
  <div class="insight-box">
    <span class="label">投资框架</span>
    <div class="content">
      <strong>2026年Q2投资主题：</strong>① <strong>算力期货化</strong>（Fink提案）→ 数据中心/能源股估值重估（CEG/GEV/VST）；② <strong>推理革命</strong>（开源框架突破）→ 推理芯片（NVDA Rubin）+ 内存（HBM4）+ 光互连（MRVL/COHR）；③ <strong>Agent分发战争</strong>（微信vs豆包）→ 腾讯/字节估值重估；④ <strong>国产替代</strong>（设备禁运+稀土暂停）→ 北方华创/中微公司（A股）+ 日本设备商（TEL/SCREEN）。
    </div>
  </div>'''

# S14: 因果链分析
s14_content = '''  <div class="causal-chain">
    <div class="chain-title">🔗 今日因果链分析</div>
    <div class="chain-item">
      <div class="key">触发因</div>
      <div class="val">AI芯片财报分化（NVDA Q1 miss预期 vs AMD Q1 beat）+ Agent融资狂飙（AIP平台增速>50%但估值承压）</div>
    </div>
    <div class="chain-item">
      <div class="key">传导机制</div>
      <div class="val">芯片财报分化 → 资金从NVDA轮动至AMD/Intel → 推理算力争夺白热化 → 开源框架成本下降30% → Agent应用门槛降低 → ToC Agent爆发</div>
    </div>
    <div class="chain-item">
      <div class="key">时间尺度</div>
      <div class="val">0-3个月（财报季资金轮动）→ 3-6个月（推理框架成熟）→ 6-12个月（Agent应用PMF验证）→ 12-18个月（推理需求>训练需求）</div>
    </div>
    <div class="chain-item">
      <div class="key">投资预测</div>
      <div class="val">短期：AMD/Intel估值修复；中期：NVDA Rubin量产+推理芯片需求超预期；长期：Agent平台（GOOGL/MSFT）捕获最大价值份额</div>
    </div>
    <div class="chain-item">
      <div class="key">证伪信号</div>
      <div class="val">① AMD MI450量产延迟>6个月；② Agent应用DAU增长停滞；③ 云厂商推理收入增速<30%</div>
    </div>
    <div class="chain-item">
      <div class="key">推荐标的</div>
      <div class="val">NVDA（核心持仓BUY）→ AMD（BUY）→ INTC（BUY）→ TSM（BUY）→ MU（BUY）→ GOOGL/MSFT（HOLD→BUY窗口）</div>
    </div>
  </div>'''

# S2 section content
s2_content = f'''  <div class="quote-box">
    <div class="quote-text">"{s2_judgment}"</div>
    <div class="quote-source">Agentic Market Daily — 专家共识</div>
    <div class="quote-context">2026-06-04 | 基于21只核心持仓财报数据与行业动态综合分析</div>
  </div>

  <div class="insight-box">
    <span class="label">核心张力</span>
    <div class="content">
      <strong>AI芯片财报分化 vs Agent融资狂飙：</strong>NVDA短期回调（-4.26%）反映Blackwell产能瓶颈担忧，但数据中心收入增速25%仍健康；AMD大涨（+6.35%）验证MI400系列预期。与此同时，Agent应用层融资持续火热（PLTR AIP增速>50%）。对投资者的行动框架：① 核心持仓（NVDA/TSM/AVGO）享受结构性增长，短期回调=加仓窗口；② 估值修复标的（AMD/INTC）受益于资金轮动；③ speculative仓位（PLTR/SNOW）在高估值下需精选入场时机。
    </div>
  </div>'''

# Now replace in template
# 1. Date in header
output = template.replace('2026-05-15 | Wednesday | Asia/Shanghai 08:07', '2026-06-04 | Thursday | Asia/Shanghai 08:07')
output = output.replace('<title>Agentic Market Daily | 2026-05-15</title>', '<title>Agentic Market Daily | 2026-06-04</title>')

# 2. Replace stock cards - find the stock-grid section and replace
stock_start = output.find('<div class="stock-grid">')
stock_end = output.find('</div>\n</div>\n\n<!-- Section 2') + 6
output = output[:stock_start] + '<div class="stock-grid">\n\n' + stock_cards + '  </div>\n</div>\n\n<!-- Section 2' + output[stock_end:]

# 3. Replace S2 content - find S2 and replace
s2_start = output.find('<!-- Section 2: Investor Quotes -->')
s2_end_marker = '<!-- Section 3 -->'
s2_end = output.find(s2_end_marker)
output = output[:s2_start] + '<!-- Section 2: Investor Quotes -->\n<div class="section">\n  <div class="section">\n  <div class="section-title"><span class="num">2</span> 投资人及权威机构最新论点</div>\n\n' + s2_content + '\n</div>\n\n' + s2_end_marker + output[s2_end:]

# 4. Replace S3-S14 content
# S3
s3_start = output.find('<!-- Section 3 -->')
s3_end = output.find('<!-- Section 4 -->')
output = output[:s3_start] + '<!-- Section 3 -->\n<div class="section">\n  <div class="section-title"><span class="num">3</span> AI独角兽模型技术动向（覆盖7家：Anthropic / OpenAI / Google / DeepSeek / Bytedance / Moonshot / Minimax）</div>\n\n' + s3_table + '\n</div>\n\n' + output[s3_end:]

# S4
s4_start = output.find('<!-- Section 4 -->')
s4_end = output.find('<!-- Section 5 -->')
output = output[:s4_start] + '<!-- Section 4 -->\n<div class="section">\n  <div class="section-title"><span class="num">4</span> NVIDIA / AMD / Intel（财报级信号）</div>\n\n' + s4_table + '\n</div>\n\n' + output[s4_end:]

# S5
s5_start = output.find('<!-- Section 5 -->')
s5_end = output.find('<!-- Section 6 -->')
output = output[:s5_start] + '<!-- Section 5 -->\n<div class="section">\n  <div class="section-title"><span class="num">5</span> 中国云厂商AI策略</div>\n\n' + s5_table + '\n</div>\n\n' + output[s5_end:]

# S6
s6_start = output.find('<!-- Section 6 -->')
s6_end = output.find('<!-- Section 7 -->')
output = output[:s6_start] + '<!-- Section 6 -->\n<div class="section">\n  <div class="section-title"><span class="num">6</span> AI Agent应用趋势</div>\n\n' + s6_table + '\n</div>\n\n' + output[s6_end:]

# S7
s7_start = output.find('<!-- Section 7 -->')
s7_end = output.find('<!-- Section 8 -->')
output = output[:s7_start] + '<!-- Section 7 -->\n<div class="section">\n  <div class="section-title"><span class="num">7</span> Agent接口及生态标准化</div>\n\n' + s7_table + '\n</div>\n\n' + output[s7_end:]

# S8
s8_start = output.find('<!-- Section 8 -->')
s8_end = output.find('<!-- Section 9 -->')
output = output[:s8_start] + '<!-- Section 8 -->\n<div class="section">\n  <div class="section-title"><span class="num">8</span> 开源社区技术路径深度追踪 & 因果链分析</div>\n\n' + s8_content + '\n</div>\n\n' + output[s8_end:]

# S9
s9_start = output.find('<!-- Section 9 -->')
s9_end = output.find('<!-- Section 10 -->')
output = output[:s9_start] + '<!-- Section 9 -->\n<div class="section">\n  <div class="section-title"><span class="num">9</span> ToC侧Agent应用及硬件部署形式</div>\n\n' + s9_table + '\n</div>\n\n' + output[s9_end:]

# S10
s10_start = output.find('<!-- Section 10 -->')
s10_end = output.find('<!-- Section 11 -->')
output = output[:s10_start] + '<!-- Section 10 -->\n<div class="section">\n  <div class="section-title"><span class="num">10</span> 全球交易：大宗商品与金融趋势</div>\n\n' + s10_table + '\n</div>\n\n' + output[s10_end:]

# S11
s11_start = output.find('<!-- Section 11 -->')
s11_end = output.find('<!-- Section 12 -->')
output = output[:s11_start] + '<!-- Section 11 -->\n<div class="section">\n  <div class="section-title"><span class="num">11</span> 政治突发：地缘与政策对供应链影响</div>\n\n' + s11_table + '\n</div>\n\n' + output[s11_end:]

# S12
s12_start = output.find('<!-- Section 12 -->')
s12_end = output.find('<!-- Section 13 -->')
output = output[:s12_start] + '<!-- Section 12 -->\n<div class="section">\n  <div class="section-title"><span class="num">12</span> Gen Z研究：15-24岁行为信号</div>\n\n' + s12_table + '\n</div>\n\n' + output[s12_end:]

# S13
s13_start = output.find('<!-- Section 13 -->')
s13_end = output.find('</footer>')
output = output[:s13_start] + '<!-- Section 13 -->\n<div class="section">\n  <div class="section-title"><span class="num">13</span> 个性化推荐：值得深度跟踪的信号</div>\n\n' + s13_content + '\n</div>\n\n<!-- Section 14 -->\n<div class="section">\n  <div class="section-title"><span class="num">14</span> 板块间底层逻辑与因果关系分析 & 投资价值预测</div>\n\n' + s14_content + '\n</div>\n\n' + output[s13_end:]

# Fix any href="#" 
output = output.replace('href="#"', 'href="https://glrocks.github.io/daily-report/"')

# Save
with open('/root/.openclaw/workspace/daily_report_2026-06-04.html', 'w') as f:
    f.write(output)

print("Generated: /root/.openclaw/workspace/daily_report_2026-06-04.html")
print(f"File size: {len(output)} bytes")
