#!/usr/bin/env python3
"""Inject section content from broken report into correct V12 template."""
import re

with open('/root/.openclaw/workspace/daily_report_2026-05-14.html', 'r') as f:
    broken = f.read()

with open('/root/.openclaw/workspace/daily_report_2026-05-14_final.html', 'r') as f:
    template = f.read()

result = template

# ============= EXTRACT SECTION CONTENT FROM BROKEN REPORT =============
# The broken report uses h2 headers and card divs
section_content = {}

for m in re.finditer(r'<h2[^>]*>(.*?)</h2>(.*?)(?=<h2|$)', broken, re.DOTALL):
    title = m.group(1).strip()
    content = m.group(2).strip()
    
    # Map to section number
    section_num = None
    if 'S2' in title or '投资人' in title:
        section_num = 2
    elif 'S3' in title or '独角兽' in title:
        section_num = 3
    elif 'S4' in title or 'NVIDIA' in title or 'AMD' in title:
        section_num = 4
    elif 'S5' in title or '中国云' in title:
        section_num = 5
    elif 'S6' in title or 'Agent应用' in title or '商业化' in title:
        section_num = 6
    elif 'S7' in title or '标准化' in title or 'MCP' in title:
        section_num = 7
    elif 'S8' in title or '开源' in title or '推理框架' in title:
        section_num = 8
    elif 'S9' in title or 'ToC' in title or '端侧' in title:
        section_num = 9
    elif 'S10' in title or '大宗' in title or '商品' in title:
        section_num = 10
    elif 'S11' in title or '政治' in title or '地缘' in title:
        section_num = 11
    elif 'S12' in title or 'Gen Z' in title or '消费' in title:
        section_num = 12
    elif 'S13' in title or '个性化' in title or '推荐' in title:
        section_num = 13
    elif 'S1' in title and '因果链' in title:
        section_num = 'causal'  # Special handling
    
    if section_num:
        # Clean content: remove outer card wrapper, keep inner HTML
        content = re.sub(r'^\s*<div class="card">\s*', '', content)
        content = re.sub(r'\s*</div>\s*$', '', content)
        section_content[section_num] = content

print(f"Extracted {len(section_content)} content sections")

# ============= REPLACE SECTION CONTENT IN TEMPLATE =============
# Find all section boundaries
section_positions = []
for m in re.finditer(r'<div class="section-title"><span class="num">(\d+)</span>', result):
    section_positions.append((m.start(), int(m.group(1))))
section_positions.append((len(result), 999))

print(f"Found {len(section_positions)-1} sections in template")

# Process from end to start to maintain position offsets
for i in range(len(section_positions) - 2, 0, -1):  # Skip section 1 (stocks)
    start_pos, section_num = section_positions[i]
    end_pos = section_positions[i + 1][0]
    
    if section_num in section_content:
        section_html = result[start_pos:end_pos]
        
        # Find the section-title closing div
        title_match = re.search(r'<div class="section-title"[^>]*>.*?</div>', section_html, re.DOTALL)
        if title_match:
            title_end = title_match.end()
            old_content = section_html[title_end:]
            new_content = '\n  ' + section_content[section_num]
            
            new_section = section_html[:title_end] + new_content
            result = result[:start_pos] + new_section + result[end_pos:]
            print(f"  Replaced section {section_num}: {len(old_content)} -> {len(new_content)} bytes")

# ============= WRITE OUTPUT =============
output_path = '/root/.openclaw/workspace/daily_report_2026-05-14_complete.html'
with open(output_path, 'w') as f:
    f.write(result)

print(f"\nSaved to {output_path} ({len(result)} bytes)")

# Verify
with open(output_path, 'r') as f:
    verify = f.read()

print(f"Verification:")
print(f"  section-title: {verify.count('class=\"section-title\"')}")
print(f"  stock-card: {verify.count('class=\"stock-card\"')}")
print(f"  rec-badge: {verify.count('class=\"rec-badge\"')}")
print(f"  cat-badge: {verify.count('class=\"cat-badge\"')}")

# Check a sample section
s2_start = verify.find('<div class="section-title"><span class="num">2</span>')
s3_start = verify.find('<div class="section-title"><span class="num">3</span>', s2_start)
if s2_start > 0 and s3_start > s2_start:
    s2_content = verify[s2_start:s3_start]
    print(f"\nSection 2 preview (first 200 chars):")
    print(s2_content[200:400].replace('\n', ' '))
