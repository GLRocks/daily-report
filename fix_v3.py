#!/usr/bin/env python3
"""
Fix the daily report by replacing stock prices in template using exact position method.
"""

with open('/root/.openclaw/workspace/agentic_market_daily_template_v12.html', 'r') as f:
    template = f.read()

with open('/root/.openclaw/workspace/daily_report_2026-05-14.html', 'r') as f:
    broken = f.read()

# Extract stock data from broken report
import re
stock_data = {}
for m in re.finditer(
    r'<span class="stock-ticker">(\w+)</span>.*?'
    r'<div class="stock-price">\$([\d.]+)</div>.*?'
    r'<div class="stock-change[^"]*">[▲▼]\s*([+-]?[\d.]+%)</div>', 
    broken, re.DOTALL):
    stock_data[m.group(1)] = {
        'price': m.group(2),
        'change': m.group(3),
        'up': m.group(3).startswith('+')
    }

# Find all stock cards in template and replace one by one
result = template
offset = 0

for m in re.finditer(r'<div class="stock-card[^"]*">', template):
    start = m.start() + offset
    # Find matching closing </div></div>
    depth = 1
    pos = m.end() + offset
    while depth > 0 and pos < len(result):
        open_tag = result.find('<div', pos)
        close_tag = result.find('</div>', pos)
        if close_tag == -1:
            break
        if open_tag != -1 and open_tag < close_tag:
            depth += 1
            pos = open_tag + 4
        else:
            depth -= 1
            pos = close_tag + 6
    
    card_start = start
    card_end = pos
    card_html = result[card_start:card_end]
    
    ticker_match = re.search(r'<div class="ticker">(\w+)</div>', card_html)
    if ticker_match and ticker_match.group(1) in stock_data:
        d = stock_data[ticker_match.group(1)]
        
        # Replace price
        new_card = re.sub(
            r'<span class="price">[\d.,$]+</span>',
            f'<span class="price">${d["price"]}</span>',
            card_html
        )
        # Replace change
        old_change = re.search(r'<span class="change (up|down)">[\d.+%\s▲▼+-]+</span>', new_card)
        if old_change:
            direction = 'up' if d['up'] else 'down'
            sign = '+' if d['up'] else ''
            change_val = d['change'].lstrip('+-')
            new_card = new_card.replace(
                old_change.group(0),
                f'<span class="change {direction}">{sign}{change_val}</span>'
            )
        
        # Apply replacement
        result = result[:card_start] + new_card + result[card_end:]
        offset += len(new_card) - len(card_html)

# Update date
result = re.sub(r'title>Agentic Market Daily \| \d{4}-\d{2}-\d{2}', 
                'title>Agentic Market Daily | 2026-05-14', result)
result = re.sub(r'<span class="date-badge">.*?</span>', 
                '<span class="date-badge">2026-05-14 | Wednesday | Asia/Shanghai 08:07</span>', 
                result, count=1)

# Write
with open('/root/.openclaw/workspace/daily_report_2026-05-14_v3.html', 'w') as f:
    f.write(result)

print(f"Written: {len(result)} bytes")

# Verify
for m in re.finditer(r'<div class="ticker">(\w+)</div>.*?<span class="price">\$([\d.]+)</span>.*?<span class="change (up|down)">([\d.+%\s-]+)</span>', result, re.DOTALL):
    print(f"  {m.group(1)}: ${m.group(2)} {m.group(4)} ({m.group(3)})")
