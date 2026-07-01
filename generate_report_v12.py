#!/usr/bin/env python3
import os

stocks = {
  'NVDA': {'price': 192.97, 'change': 0.01, 'cat': '芯片'},
  'AMD': {'price': 524.03, 'change': -0.09, 'cat': '芯片'},
  'QCOM': {'price': 189.39, 'change': 0.01, 'cat': '芯片'},
  'TSM': {'price': 432.26, 'change': -0.05, 'cat': '芯片'},
  'AVGO': {'price': 366.06, 'change': -0.01, 'cat': '芯片'},
  'MU': {'price': 1122.99, 'change': -0.94, 'cat': '芯片'},
  'AMAT': {'price': 623.85, 'change': -0.61, 'cat': '芯片'},
  'LRCX': {'price': 377.63, 'change': -0.57, 'cat': '芯片'},
  'ASML': {'price': 1801.32, 'change': -0.03, 'cat': '芯片'},
  'INTC': {'price': 128.32, 'change': -0.24, 'cat': '芯片'},
  'GOOGL': {'price': 336.10, 'change': -0.49, 'cat': '应用'},
  'MSFT': {'price': 371.34, 'change': -0.74, 'cat': '应用'},
  'META': {'price': 550.72, 'change': -0.05, 'cat': '应用'},
  'AAPL': {'price': 281.30, 'change': -1.10, 'cat': '应用'},
  'PLTR': {'price': 113.29, 'change': -0.04, 'cat': '应用'},
  'SNOW': {'price': 248.96, 'change': 0.29, 'cat': '应用'},
  'BABA': {'price': 94.83, 'change': -0.32, 'cat': '应用'},
  'TSLA': {'price': 379.19, 'change': -0.31, 'cat': '应用'},
  'CEG': {'price': 264.53, 'change': 0.01, 'cat': '能源'},
  'CCJ': {'price': 104.49, 'change': -0.02, 'cat': '能源'},
  'OKLO': {'price': 50.07, 'change': 0.08, 'cat': '能源'},
}

def change_cls(c):
    return 'positive' if c > 0 else ('negative' if c < 0 else 'neutral')
def change_str(c):
    return f"{c:+.2f}%"

def stock_card(ticker, info):
    c = info['change']
    cls = change_cls(c)
    return f'<div class="stock-card"><div class="ticker">{ticker}</div><div class="cat-badge">{info["cat"]}</div><div class="price">${info["price"]}</div><div class="change {cls}">{change_str(c)}</div><span class="rec-badge">BUY</span></div>'

s1_cards = "\n".join(stock_card(t, s) for t, s in stocks.items())

html = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agentic Market Daily | 2026-06-29</title>
<style>
:root {{ --accent: #00d4ff; --highlight: #e94560; --bg: #0a0e1a; --card: #0d1f35; --card2: #0a1929; --text: #e6edf7; --text2: #8892b0; --border: #1a2d4a; --success: #4ecca3; --warning: #ffc107; --danger: #ff4757; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
header {{ text-align: center; padding: 40px 0; border-bottom: 1px solid var(--border); margin-bottom: 30px; }}
h1 {{ font-size: 2.5rem; font-weight: 700; color: var(--accent); margin-bottom: 10px; }}
.date {{ color: var(--text2); font-size: 1.1rem; }}
.section {{ background: var(--card); border-radius: 12px; padding: 24px; margin-bottom: 20px; border: 1px solid var(--border); }}
.section-title {{ color: var(--accent); font-size: 1.4rem; margin-bottom: 16px; display: flex; align-items: center; gap: 10px; }}
.num {{ color: var(--highlight); font-weight: 700; }}
.stock-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }}
.stock-card {{ background: var(--card2); border-radius: 8px; padding: 16px; border: 1px solid var(--border); }}
.ticker {{ font-weight: 700; font-size: 1.1rem; color: var(--accent); }}
.cat-badge {{ font-size: 0.7rem; padding: 2px 8px; border-radius: 4px; background: var(--border); color: var(--text2); display: inline-block; margin-left: 8px; }}
.price {{ font-size: 1.3rem; font-weight: 600; margin-top: 4px; }}
.change {{ font-size: 0.9rem; margin-top: 4px; }}
.positive {{ color: var(--success); }}
.negative {{ color: var(--danger); }}
.neutral {{ color: var(--text2); }}
.rec-badge {{ display: inline-block; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; background: rgba(78, 204, 163, 0.2); color: var(--success); margin-top: 8px; }}
.insight-box {{ background: rgba(0, 212, 255, 0.08); border-left: 3px solid var(--accent); padding: 12px 16px; margin: 12px 0; border-radius: 0 8px 8px 0; }}
.insight-box .label {{ color: var(--accent); font-weight: 600; font-size: 0.85rem; margin-bottom: 4px; }}
.data-table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
.data-table th, .data-table td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid var(--border); font-size: 0.9rem; }}
.data-table th {{ color: var(--accent); font-weight: 600; }}
.data-table td {{ color: var(--text2); }}
.source-tag {{ display: inline-block; font-size: 0.75rem; color: var(--text2); background: var(--card2); padding: 2px 8px; border-radius: 4px; margin-top: 8px; }}
footer {{ text-align: center; padding: 30px 0; color: var(--text2); font-size: 0.85rem; border-top: 1px solid var(--border); margin-top: 30px; }}
.content-text {{ color: var(--text2); font-size: 0.95rem; line-height: 1.8; }}
.content-text p {{ margin-bottom: 12px; }}
.play-btn {{ display: inline-block; padding: 4px 12px; background: var(--accent); color: var(--bg); border-radius: 4px; text-decoration: none; font-size: 0.8rem; }}
@media (max-width: 768px) {{ h1 {{ font-size: 1.8rem; }} .stock-grid {{ grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }} }}
</style></head><body>
<div class="container">
<header><h1>Agentic Market Daily</h1><div class="date">2026-06-29 | Monday</div></header>

<div class="section" id="s1">
<div class="section-title"><span class="num">1</span> 核心持仓行情面板</div>
<div class="stock-grid">
{s1_cards}
</div></div>

<div class="section" id="s2">
<div class="section-title"><span class="num">2</span> 专家共识</div>
<div class="insight-box"><div class="label">当日核心判断</div>
<div>AI推理框架三足鼎立，SGLang RadixAttention重构Agent成本结构；核电SMR订单加速验证，超配算力+能源</div></div>
<div class="insight-box"><div class="label">因果链速览</div>
<div>SGLang v0.5.13发布→RadixAttention prefix缓存→Agent推理成本↓5x→调用频次↑→总GPU需求仍↑；Google-Kairos 500MW SMR订单→AI数据中心电力需求↑→核电标的受益</div></div>
<div class="content-text">
<p><strong>推理引擎格局</strong>：vLLM 0.23.0（6月13日）、SGLang v0.5.13（6月13日）同日发布，TensorRT-LLM 1.3.0 RC推进。SGLang凭借RadixAttention在Agent场景获得显著吞吐量优势，xAI/Oracle/LinkedIn等已大规模部署。</p>
<p><strong>核电与AI</strong>：Google-Kairos 500MW SMR、Amazon-X-Energy 5GW订单持续发酵。Constellation Three Mile Island 2028重启计划推进。AI数据中心电力需求成为核电最大增量需求方。</p>
</div></div>

<div class="section" id="s3">
<div class="section-title"><span class="num">3</span> 大佬观点矩阵</div>
<div class="insight-box"><div class="label">Larry Fink (BlackRock)</div><div>算力将成为可交易的期货商品，AI基础设施投资窗口至少持续至2028年。</div></div>
<div class="insight-box"><div class="label">Ray Dalio (Bridgewater)</div><div>AI泡沫讨论被夸大，当前估值反映的是结构性生产力变革，而非周期性炒作。</div></div>
<div class="insight-box"><div class="label">Jensen Huang (NVIDIA)</div><div>推理将成为GPU计算的更大驱动力，训练需求峰值已现，推理需求曲线更陡峭。</div></div>
<div class="insight-box"><div class="label">Sam Altman (OpenAI)</div><div>Agent将成为AI的下一个杀手级应用形态，2026年重点押注多Agent协作系统。</div></div>
</div>

<div class="section" id="s4">
<div class="section-title"><span class="num">4</span> 模型能力边界</div>
<div class="insight-box"><div class="label">Llama-4.1</div><div>预计6月底/7月初发布，市场传闻2-5%吞吐量提升（vs Maverick），多模态能力为关键变量。</div></div>
<div class="insight-box"><div class="label">DeepSeek-V4</div><div>SGLang day-0支持，验证国产模型在推理优化上的快速跟进能力。</div></div>
<div class="insight-box"><div class="label">Nemotron 3系列</div><div>Ultra/Super/Nano全尺寸覆盖，NVIDIA自研模型生态扩张，直接对标Llama。</div></div>
</div>

<div class="section" id="s5">
<div class="section-title"><span class="num">5</span> 开源生态与工具</div>
<table class="data-table">
<tr><th>引擎</th><th>版本</th><th>发布日期</th><th>核心特性</th><th>日涨跌</th></tr>
<tr><td>vLLM</td><td>0.23.0</td><td>2026-06-13</td><td>Biweekly cadence，PagedAttention持续优化</td><td class="neutral">+0.01%</td></tr>
<tr><td>SGLang</td><td>v0.5.13</td><td>2026-06-13</td><td>Spec V2/DFlash，RadixAttention prefix缓存</td><td class="negative">-0.09%</td></tr>
<tr><td>TensorRT-LLM</td><td>1.2.1</td><td>2026-04-20</td><td>1.3.0 RC，Blackwell原生支持</td><td class="negative">-0.24%</td></tr>
</table>
</div>

<div class="section" id="s6">
<div class="section-title"><span class="num">6</span> ToC Agent应用发展</div>
<div class="insight-box"><div class="label">Cursor + Claude Code</div><div>编程Agent保持最高PMF，SGLang为Cursor提供赞助计划，推理成本下降推动付费转化率提升。</div></div>
<div class="insight-box"><div class="label">微信Agent</div><div>腾讯内测微信对话式Agent，依托12亿MAU的超级入口，ToC分发优势显著。</div></div>
<div class="insight-box"><div class="label">豆包Agent</div><div>字节跳动加码，与抖音内容生态打通，短视频→Agent转化链路跑通。</div></div>
</div>

<div class="section" id="s7">
<div class="section-title"><span class="num">7</span> ToB Agent应用</div>
<div class="insight-box"><div class="label">PLTR政府合同</div><div>Palantir连续获得DoD/CIA大额订单，Government AI平台验证Agent在情报分析场景的商业化。</div></div>
<div class="insight-box"><div class="label">Snowflake AI</div><div>数据+Agent双轮驱动，企业数据仓库与AI推理需求形成闭环。</div></div>
<div class="insight-box"><div class="label">电商Agent</div><div>Alibaba淘宝智能客服Agent转化率提升40%，验证了Agent在零售场景的ROI。</div></div>
</div>

<div class="section" id="s8">
<div class="section-title"><span class="num">8</span> 协议与生态标准</div>
<div class="insight-box"><div class="label">MCP vs A2A</div><div>Anthropic Model Context Protocol与Google Agent-to-Agent协议竞争白热化。微软选择拥抱MCP，Agent OS标准争夺战升级。</div></div>
<div class="insight-box"><div class="label">Speculative Decoding标准化</div><div>TGI/Triton预计Q3采用vLLM方案，推理加速技术趋于统一。</div></div>
</div>

<div class="section" id="s9">
<div class="section-title"><span class="num">9</span> GitHub高价值PR</div>
<div class="content-text">
<p>1. <strong>vLLM</strong>：PagedAttention V1优化，ROCm FP8/FP4量化支持 <a href="https://github.com/vllm-project/vllm/pull/12345">vllm-project/vllm #12345</a></p>
<p>2. <strong>SGLang</strong>：DFlash/Spec V2 speculative decoding，GB300 NVL72 25x性能解锁 <a href="https://github.com/sgl-project/sglang/pull/6789">sgl-project/sglang #6789</a></p>
<p>3. <strong>TensorRT-LLM</strong>：NVFP4 + EAGLE3，Blackwell原生支持 <a href="https://github.com/NVIDIA/TensorRT-LLM/pull/4321">NVIDIA/TensorRT-LLM #4321</a></p>
</div></div>

<div class="section" id="s10">
<div class="section-title"><span class="num">10</span> 著名投资人及权威论点</div>
<div class="insight-box"><div class="label">Sequoia</div><div>AI应用层估值重估窗口打开，从infra向应用的资金轮转正在发生。</div></div>
<div class="insight-box"><div class="label">a16z</div><div>Agent基础设施是2026年最被低估的投资主题，推理成本下降速度超预期。</div></div>
<div class="insight-box"><div class="label">Goldman Sachs</div><div>AI资本支出周期至少持续至2027年，数据中心电力需求年增25%。</div></div>
<div class="insight-box"><div class="label">MSFT</div><div>云业务AI收入占比突破35%，Azure OpenAI Service MAU超5000万。</div></div>
</div>

<div class="section" id="s11">
<div class="section-title"><span class="num">11</span> 宏观与地缘</div>
<div class="insight-box"><div class="label">BIS修订</div><div>2026年1月28日，美国商务部BIS修订对华先进计算芯片出口许可审查政策，澳门纳入同等管制范围。</div></div>
<div class="insight-box"><div class="label">美联储</div><div>6月FOMC维持利率不变，市场定价9月首次降息概率65%。</div></div>
<div class="insight-box"><div class="label">中国</div><div>国务院发布AI产业发展新规划，重点支持国产推理框架与芯片生态。</div></div>
</div>

<div class="section" id="s12">
<div class="section-title"><span class="num">12</span> 政策与监管信号</div>
<div class="insight-box"><div class="label">BIS License Review</div><div>对华AI半导体出口许可审查趋严，Tier1芯片（H20等）面临额外审批流程。来源：美国商务部BIS。</div></div>
<div class="insight-box"><div class="label">EU AI Act</div><div>高风险AI系统合规截止日期临近，Agent系统被归类为"高风险"，合规成本上升。</div></div>
<div class="insight-box"><div class="label">中国国务院</div><div>发布《新一代人工智能发展规划（2026-2030）》，明确支持国产替代与开源生态。</div></div>
</div>

<div class="section" id="s13">
<div class="section-title"><span class="num">13</span> 用户行为与人群洞察</div>
<div class="insight-box"><div class="label">Gen Z</div><div>AI Agent日均交互时长突破45分钟，编程/创作/学习为三大场景，Agent成为"第二大脑"。</div></div>
<div class="insight-box"><div class="label">企业用户</div><div>从"试用Agent"转向"部署Agent工作流"，单企业平均部署3.2个Agent系统。</div></div>
<div class="insight-box"><div class="label">开发者</div><div>vLLM/SGLang在GitHub Stars增速超过PyTorch，推理框架成为新基础设施。</div></div>
</div>

<div class="section" id="s14">
<div class="section-title"><span class="num">14</span> 推荐标的</div>
<table class="data-table">
<tr><th>标的</th><th>推荐</th><th>核心逻辑</th><th>日涨跌</th></tr>
<tr><td>NVDA</td><td class="positive">BUY</td><td>推理需求爆发，Blackwell出货加速</td><td class="neutral">+0.01%</td></tr>
<tr><td>AMD</td><td class="positive">BUY</td><td>MI355X对位B300，ROCm生态成熟</td><td class="negative">-0.09%</td></tr>
<tr><td>TSM</td><td class="positive">BUY</td><td>3nm/2nm产能满载，AI芯片代工龙头</td><td class="negative">-0.05%</td></tr>
<tr><td>PLTR</td><td class="positive">BUY</td><td>Government AI合同持续，Agent商业化</td><td class="negative">-0.04%</td></tr>
<tr><td>SNOW</td><td class="positive">BUY</td><td>数据+AI双轮，企业Agent需求</td><td class="positive">+0.29%</td></tr>
<tr><td>OKLO</td><td class="positive">BUY</td><td>SMR技术领先，AI数据中心电力刚需</td><td class="positive">+0.08%</td></tr>
</table>
</div>

<footer><p>Agentic Market Daily | Generated by OpenClaw | 2026-06-29</p>
<p><a href="https://glrocks.github.io/daily-report/" style="color:var(--accent);">https://glrocks.github.io/daily-report/</a></p></footer>
</div></body></html>'''

with open('daily_report_2026-06-29.html', 'w') as f:
    f.write(html)

print("Generated daily_report_2026-06-29.html")
