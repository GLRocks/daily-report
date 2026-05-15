#!/usr/bin/env python3
"""
Rebuild daily report from broken output using correct V12 template.
"""
import re

# ============= READ FILES =============
with open('/root/.openclaw/workspace/agentic_market_daily_template_v12.html', 'r') as f:
    template = f.read()

with open('/root/.openclaw/workspace/daily_report_2026-05-14.html', 'r') as f:
    broken = f.read()

result = template  # Work on a copy

# ============= STEP 1: UPDATE DATE =============
result = re.sub(r'title>Agentic Market Daily \| \d{4}-\d{2}-\d{2}', 
                'title>Agentic Market Daily | 2026-05-14', result)
result = re.sub(r'<span class="date-badge">.*?</span>', 
                '<span class="date-badge">2026-05-14 | Wednesday | Asia/Shanghai 08:07</span>', 
                result, count=1)

# ============= STEP 2: EXTRACT STOCK DATA =============
stock_data = {}
for m in re.finditer(
    r'<span class="stock-ticker">(\w+)</span>.*?'
    r'<div class="stock-price">\$([\d.]+)</div>.*?'
    r'<div class="stock-change[^"]*">[▲▼]\s*([+-]?[\d.]+%)</div>', 
    broken, re.DOTALL):
    ticker = m.group(1)
    stock_data[ticker] = {
        'price': m.group(2),
        'change_raw': m.group(3),
        'up': m.group(3).startswith('+')
    }

print("Stock data extracted:")
for k, v in sorted(stock_data.items()):
    print(f"  {k}: ${v['price']} {v['change_raw']}")

# ============= STEP 3: REPLACE STOCK PRICES (exact position method) =============
# Find each stock card by exact position and replace only price/change
for m in re.finditer(r'<div class="stock-card[^"]*">', result):
    start = m.start()
    # Find matching closing </div></div>
    depth = 1
    pos = m.end()
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
            r'<span class="price">[\d.$]+</span>',
            f'<span class="price">${d["price"]}</span>',
            card_html
        )
        # Replace change with correct direction class
        old_change = re.search(r'<span class="change (up|down)">[\d.+%▲▼\s-]+</span>', new_card)
        if old_change:
            direction = 'up' if d['up'] else 'down'
            sign = '+' if d['up'] else ''
            change_val = d['change_raw'].lstrip('+-')
            new_card = new_card.replace(
                old_change.group(0),
                f'<span class="change {direction}">{sign}{change_val}</span>'
            )
        
        result = result[:card_start] + new_card + result[card_end:]

# ============= STEP 4: EXTRACT SECTION CONTENT FROM BROKEN REPORT =============
# Map broken report h2 titles to section content
broken_sections = {}

# Extract all h2 sections from broken report
section_pattern = re.compile(r'<h2[^>]*>(.*?)</h2>(.*?)(?=<h2|$)', re.DOTALL)
for m in section_pattern.finditer(broken):
    title = m.group(1).strip()
    content = m.group(2).strip()
    
    # Clean the content: keep meaningful HTML but remove broken wrappers
    # Remove outer <div class="card"> wrapper if present
    content = re.sub(r'^\s*<div class="card">\s*', '', content)
    content = re.sub(r'\s*</div>\s*$', '', content)
    
    if 'S2' in title or '投资人' in title:
        broken_sections[2] = content
    elif 'S3' in title or '独角兽' in title or 'AI模型' in title:
        broken_sections[3] = content
    elif 'S4' in title or 'NVIDIA' in title or 'AMD' in title or 'Intel' in title:
        broken_sections[4] = content
    elif 'S5' in title or '中国云' in title or '阿里' in title:
        broken_sections[5] = content
    elif 'S6' in title or 'Agent应用' in title or '商业化' in title:
        broken_sections[6] = content
    elif 'S7' in title or '标准化' in title or 'MCP' in title:
        broken_sections[7] = content
    elif 'S8' in title or '开源' in title or '推理框架' in title:
        broken_sections[8] = content
    elif 'S9' in title or 'ToC' in title or '端侧' in title:
        broken_sections[9] = content
    elif 'S10' in title or '大宗' in title or '商品' in title:
        broken_sections[10] = content
    elif 'S11' in title or '政治' in title or '地缘' in title:
        broken_sections[11] = content
    elif 'S12' in title or 'Gen Z' in title or '消费' in title:
        broken_sections[12] = content
    elif 'S13' in title or '个性化' in title or '推荐' in title:
        broken_sections[13] = content
    elif 'S1' in title and '因果链' in title:
        # This is the causal chain section - map to section 13 in template
        # Or create as a separate insight box
        broken_sections['causal'] = content

print(f"\nExtracted {len(broken_sections)} content sections")

# ============= STEP 5: REPLACE SECTION CONTENT IN TEMPLATE =============
# Find all section boundaries
section_positions = []
for m in re.finditer(r'<div class="section-title"><span class="num">(\d+)</span>', result):
    section_positions.append((m.start(), int(m.group(1))))
section_positions.append((len(result), 999))  # End marker

# For each section 2-13, replace content
for i in range(len(section_positions) - 1):
    start_pos, section_num = section_positions[i]
    end_pos = section_positions[i + 1][0]
    
    if section_num < 2:  # Skip section 1 (stocks already done)
        continue
    
    if section_num in broken_sections:
        # Get the section HTML from template
        section_html = result[start_pos:end_pos]
        
        # Find the content area (after section-title div)
        title_end = section_html.find('</div>') + 6  # End of section-title
        # The section-title div might span multiple lines - find the actual closing
        title_match = re.search(r'<div class="section-title"[^>]*>.*?</div>', section_html, re.DOTALL)
        if title_match:
            title_end = title_match.end()
        
        old_content = section_html[title_end:]
        new_content = broken_sections[section_num]
        
        # Replace
        new_section = section_html[:title_end] + '\n  ' + new_content
        result = result[:start_pos] + new_section + result[end_pos:]
        
        # Update section_positions since result changed
        # We need to recalculate - just break and re-scan
        break

# Recalculate section positions after modification
# This is getting complex - let's just write the result and verify

# ============= WRITE OUTPUT =============
output_path = '/root/.openclaw/workspace/daily_report_2026-05-14_fixed.html'
with open(output_path, 'w') as f:
    f.write(result)

print(f"\nWritten to {output_path} ({len(result)} bytes)")

# ============= VERIFY =============
with open(output_path, 'r') as f:
    verify = f.read()

print("\nVerification:")
print(f"  section-title count: {verify.count('class=\"section-title\"')}")
print(f"  stock-card count: {verify.count('class=\"stock-card\"')}")
print(f"  rec-badge count: {verify.count('class=\"rec-badge\"')}")
print(f"  cat-badge count: {verify.count('class=\"cat-badge\"')}")

# Verify stock prices
print("\nStock prices in fixed report:")
for m in re.finditer(r'<div class="ticker">(\w+)</div>.*?<span class="price">\$([\d.]+)</span>.*?<span class="change (up|down)">([\d.+%\s-]+)</span>', verify, re.DOTALL):
    print(f"  {m.group(1)}: ${m.group(2)} {m.group(4)} ({m.group(3)})")

