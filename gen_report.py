#!/usr/bin/env python3
"""Generate daily report for 2026-07-01 based on index.html template"""
import re

with open('/root/.openclaw/workspace/index.html', 'r') as f:
    html = f.read()

# Update date
html = html.replace('Agentic Market Daily | 2026-06-30', 'Agentic Market Daily | 2026-07-01')
html = html.replace('2026-06-30 | Wednesday |', '2026-07-01 | Wednesday |')

# Stock data
stocks = {
    'NVDA': {'price': '200.36', 'change': '+4.06%', 'up': True},
    'AMD': {'price': '582.03', 'change': '+11.59%', 'up': True},
    'QCOM': {'price': '184.79', 'change': '-2.43%', 'up': False},
    'TSM': {'price': '477.98', 'change': '+10.55%', 'up': True},
    'AVGO': {'price': '377.80', 'change': '+3.50%', 'up': True},
    'MU': {'price': '1158.05', 'change': '+2.27%', 'up': True},
    'AMAT': {'price': '724.46', 'change': '+15.57%', 'up': True},
    'LRCX': {'price': '433.91', 'change': '+14.46%', 'up': True},
    'ASML': {'price': '1989.06', 'change': '+10.83%', 'up': True},
    'INTC': {'price': '139.78', 'change': '+8.93%', 'up': True},
    'GOOGL': {'price': '357.08', 'change': '+5.84%', 'up': True},
    'MSFT': {'price': '372.83', 'change': '-0.04%', 'up': False},
    'META': {'price': '563.05', 'change': '+2.33%', 'up': True},
    'AAPL': {'price': '289.12', 'change': '+1.88%', 'up': True},
    'PLTR': {'price': '116.68', 'change': '+3.32%', 'up': True},
    'SNOW': {'price': '254.50', 'change': '+1.13%', 'up': True},
    'BABA': {'price': '95.98', 'change': '+1.23%', 'up': True},
    'TSLA': {'price': '420.58', 'change': '+10.76%', 'up': True},
    'CEG': {'price': '248.37', 'change': '-5.93%', 'up': False},
    'CCJ': {'price': '101.86', 'change': '-1.56%', 'up': False},
    'OKLO': {'price': '52.33', 'change': '-0.82%', 'up': False},
}

# Update stock prices and changes using simple string replacement
for ticker, data in stocks.items():
    # Find the specific stock card section and replace price
    idx = html.find(f'<div class="ticker">{ticker}</div>')
    if idx < 0:
        print(f"WARNING: ticker {ticker} not found")
        continue
    
    # Find price span after this ticker
    price_start = html.find('<span class="price">$', idx)
    price_end = html.find('</span>', price_start)
    if price_start > 0 and price_end > price_start:
        html = html[:price_start] + f'<span class="price">${data["price"]}</span>' + html[price_end+7:]
    
    # Find change span after this ticker (need to refind after price replacement)
    idx = html.find(f'<div class="ticker">{ticker}</div>')
    change_start = html.find('<span class="change', idx)
    change_end = html.find('</span>', change_start)
    if change_start > 0 and change_end > change_start:
        direction = 'up' if data['up'] else 'down'
        html = html[:change_start] + f'<span class="change {direction}">{data["change"]}</span>' + html[change_end+7:]

# Update metrics
metrics = {
    'NVDA': '市值$5.4T | P/S 35x | 毛利率75%',
    'AMD': 'YTD+222% | MI450出货Q3 | 服务器CPU TAM$120B',
    'QCOM': 'Q3指引$9.2-10B | Android收入减速 | AI PC Snapdragon X',
    'TSM': '2nm量产2025H2 | 美国凤凰厂高量投产 | 70%先进制程市占',
    'AVGO': '定制AI芯片收入$12B/年 | VMware整合完成 | 毛利率80%+',
    'MU': 'HBM3E量产 | DDR5供需紧 | 内存周期复苏确认',
    'AMAT': 'BIS罚款$300M已消化 | 中国设备收入占比18% | 刻蚀龙头',
    'LRCX': '刻蚀/沉积双龙头 | 存储设备周期复苏 | 毛利率47%',
    'ASML': 'EUV垄断 | High-NA EUV 2028量产 | 订单积压$40B+',
    'INTC': 'YTD+222% | Google代工300万芯片 | 18A良率85%',
    'GOOGL': 'Gemini 3.1 Ultra | 云收入增速26% | 4名AI研究员流失Anthropic',
    'MSFT': 'Azure增速31% | Copilot ARR>$10B | OpenAI深度绑定',
    'META': 'Llama 4开源 | Reels变现加速 | AI推荐引擎驱动DAU',
    'AAPL': 'iOS 27开放第三方AI | 服务端AI资本开支$10B+/年',
    'PLTR': 'AIP平台增速>50% | SpaceX收购Cursor$60B | 估值溢价',
    'SNOW': 'Cortex AI集成 | 收入增长22% | 竞争加剧',
    'BABA': 'Qwen3 MoE | 阿里云增速14% | 通义千问DAU 2500万',
    'TSLA': 'FSD V13延迟 | Optimus量产2026 | 能源业务增长',
    'CEG': '核电重启+AI数据中心供电 | 订单积压$30B+ | 监管绿灯',
    'CCJ': '铀价$85/lb | 供给缺口持续 | 核电复兴原料端',
    'OKLO': '小型模块化反应堆 | Sam Altman背书 | 早期阶段高风险',
}

for ticker, m in metrics.items():
    idx = html.find(f'<div class="ticker">{ticker}</div>')
    if idx < 0:
        continue
    met_start = html.find('核心指标: ', idx)
    met_end = html.find(' | ', met_start)  # find end of metrics line
    if met_start > 0:
        # Find the full metrics div
        div_start = html.find('<div class="stock-metrics">', idx)
        div_end = html.find('</div>', div_start)
        if div_start > 0 and div_end > div_start:
            html = html[:div_start] + f'<div class="stock-metrics">核心指标: {m}</div>' + html[div_end+6:]

# Update reasons
reasons = {
    'NVDA': '推理需求结构从训练向推理转移，NVDA软件生态锁定最深',
    'AMD': 'MI450系列挑战NVDA B300，Intel代工协议催化，Lisa Su指引TAM年增35%',
    'QCOM': '短期业绩miss但AI PC/Auto长期布局 intact，等待回调后加仓窗口',
    'TSM': '先进制程绝对垄断地位，地缘风险已price in部分，产能持续扩张',
    'AVGO': 'Google/Meta定制芯片核心供应商，AI ASIC趋势最大受益者',
    'MU': 'HBM3E供不应求，AI服务器内存密度提升驱动长期需求',
    'AMAT': '先进封装设备需求爆发，HBM/3D封装核心设备供应商',
    'LRCX': '存储资本开支回暖带动设备需求，先进工艺刻蚀复杂度提升',
    'ASML': '光刻绝对垄断，High-NA技术护城河加深，长期订单可见性最强',
    'INTC': 'Google 300万芯片代工协议确认，18A节点恢复，代工业务IFS营收$1.5B+',
    'GOOGL': 'Gemini生态+TPU自研+搜索AI化，但人才流失预警$270B市值蒸发',
    'MSFT': '企业AI消费最高确定性，Copilot生态粘性构建中',
    'META': '开源模型战略+社交广告AI优化，AI应用层最大变现平台',
    'AAPL': '端侧AI入口价值被低估，iOS开放AI模型选择生态变革',
    'PLTR': '企业AI平台化最激进，SpaceX收购Cursor强化生态，适合高风险偏好',
    'SNOW': '数据平台AI化转型中，但Databrick等竞争压力上升',
    'BABA': '中国AI云龙头但增长放缓，关注Qwen3商业化进展',
    'TSLA': '机器人+AI叙事 intact，但短期业绩波动大，需事件催化',
    'CEG': 'AI算力电力需求爆发最直接受益者，核电复兴核心标的',
    'CCJ': '铀供需结构性缺口，核电复兴上游最直接杠杆',
    'OKLO': '先进核反应堆技术路线，Altman个人押注，高风险高回报',
}

for ticker, r in reasons.items():
    idx = html.find(f'<div class="ticker">{ticker}</div>')
    if idx < 0:
        continue
    div_start = html.find('<div class="stock-reason">', idx)
    div_end = html.find('</div>', div_start)
    if div_start > 0 and div_end > div_start:
        html = html[:div_start] + f'<div class="stock-reason">推荐: {r}</div>' + html[div_end+6:]

# Write output
output_path = '/root/.openclaw/workspace/daily_report_2026-07-01.html'
with open(output_path, 'w') as f:
    f.write(html)

print(f"Done: {output_path} ({len(html)} bytes)")
