#!/usr/bin/env python3
"""
Generate 2026-05-15 daily report by replacing template content
"""
import re

with open('/root/.openclaw/workspace/agentic_market_daily_template_v12.html', 'r') as f:
    template = f.read()

# Replace date
template = template.replace('Agentic Market Daily | 2026-05-12', 'Agentic Market Daily | 2026-05-15')
template = template.replace('2026-05-12 | 半导体投资级技术情报', '2026-05-15 | 半导体投资级技术情报')
template = template.replace('生成时间: 2026-05-12 08:07 CST', '生成时间: 2026-05-15 08:07 CST')
template = template.replace('数据来源: ifind, Bloomberg, LME, SEMI, SemiAnalysis', '数据来源: ifind, Bloomberg, Morgan Stanley, SEMI, SemiAnalysis')

# Stock prices
prices = {
    'NVDA': '$235.77', 'AMD': '$450.95', 'INTC': '$115.95', 'TSM': '$417.58',
    'AVGO': '$439.98', 'QCOM': '$200.11', 'MU': '$775.91', 'MRVL': '$182.58',
    'COHR': '$404.26', 'LRCX': '$299.15', 'KLAC': '$1892.94', 'ASML': '$1584.51',
    'AMAT': '$440.89', 'GOOGL': '$400.66', 'MSFT': '$409.32', 'META': '$618.44',
    'AMZN': '$267.03', 'BABA': '$141.07', 'SMCI': '$33.03', 'CEG': '$275.50',
    'TCEHY': '价格暂缺'
}

for ticker, price in prices.items():
    pattern = rf'(<div class="ticker">{ticker}</div>.*?<span class="price">)[^<]+(</span>)'
    template = re.sub(pattern, rf'\g<1>{price}\g<2>', template, count=1, flags=re.DOTALL)

# Write result
with open('/root/.openclaw/workspace/daily_report_2026-05-15.html', 'w') as f:
    f.write(template)

print('Daily report base generated successfully')
