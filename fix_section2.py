#!/usr/bin/env python3
"""Fix missing Section 2 in daily report HTML"""

import re

with open('/root/.openclaw/workspace/daily_report_2026-08-16.html', 'r') as f:
    html = f.read()

# Section 2 content to insert
s2_content = '''
<!-- Section 2: Expert Consensus -->
<div class="section">
  <div class="section-title"><span class="num">2</span> 专家共识：跨板块综合研判</div>
  <div class="insight-box">
    <span class="label">当日核心判断</span>
    <div class="content">
      <strong>芯片反弹验证AI基建韧性，关注下周NVDA财报及OpenAI S-1。</strong>周五MU/LRCX/INTC暴力反弹，存储与设备双龙头共振确认AI资本开支未放缓。应用层分化BABA领跌，能源避险 intact。整体判断：周末市场清淡，芯片进入财报验证期，8/26 NVDA财报为下半年关键节点。
    </div>
  </div>
  <div class="insight-box">
    <span class="label">因果链速览</span>
    <div class="content">
      <strong>触发因：</strong>CoreWeave/SMCI财报超预期 → AI数据中心资本开支确认 → 存储/设备订单能见度至2027。<br>
      <strong>传导机制：</strong>OpenAI IPO预期 → 资本涌入AI基础设施 → 数据中心电力需求激增 → 核电基荷价值重估。<br>
      <strong>时间尺度：</strong>短期（8/26 NVDA财报）→ 中期（Q4 Agent商业化拐点）→ 长期（2027推理需求>训练需求）。<br>
      <strong>证伪信号：</strong>① NVDA财报miss或guidance下调；② Agent应用DAU增长停滞；③ 云厂商推理收入增速<30%。<br>
      <strong>推荐标的：</strong>NVDA（核心持仓）→ MU（存储周期反转）→ CEG（电力刚需）→ PLTR（Agent平台）。
    </div>
  </div>
  <table class="data-table">
    <thead><tr><th>维度</th><th>判断</th><th>置信度</th><th>关键支撑板块</th></tr></thead>
    <tbody>
      <tr><td>技术趋势</td><td>AI芯片需求结构性增长 intact</td><td>🟢 高</td><td>S1/S5/S9</td></tr>
      <tr><td>投资行为</td><td>资金轮动至存储/设备，应用层分化</td><td>🟡 中</td><td>S1/S6</td></tr>
      <tr><td>风险预警</td><td>NVDA财报高预期下的miss风险</td><td>🔴 高</td><td>S5/S14</td></tr>
      <tr><td>时间窗口</td><td>8/26 NVDA财报为关键催化剂</td><td>🟢 高</td><td>S5/S14</td></tr>
    </tbody>
  </table>
</div>
'''

# Find the insertion point: after S1 closing </div> and before <!-- Section 2
pattern = r'(</div>\s*)(<!-- Section 2: Investor Quotes -->)'
match = re.search(pattern, html)
if match:
    insert_pos = match.start(2)
    html = html[:insert_pos] + s2_content + '\n' + html[insert_pos:]
    print("Inserted Section 2 at position", insert_pos)
else:
    # Try alternative pattern
    pattern2 = r'(</div>\s+)(<div class="section">\s+<div class="section-title"><span class="num">2</span> 投资人)'
    match = re.search(pattern2, html)
    if match:
        insert_pos = match.start(2)
        html = html[:insert_pos] + s2_content + '\n' + html[insert_pos:]
        print("Inserted Section 2 at position", insert_pos)
    else:
        print("ERROR: Could not find insertion point")
        exit(1)

# Now renumber sections: 2→3, 3→4, ..., 13→14
# Process in reverse order to avoid overlapping replacements
for old_num in range(13, 1, -1):
    new_num = old_num + 1
    # Replace section titles
    html = html.replace(f'<span class="num">{old_num}</span>', f'<span class="num">{new_num}</span>', 1)

# Save
with open('/root/.openclaw/workspace/daily_report_2026-08-16.html', 'w') as f:
    f.write(html)

# Also copy to index.html
with open('/root/.openclaw/workspace/index.html', 'w') as f:
    f.write(html)

print("Fixed and saved daily_report_2026-08-16.html and index.html")
print("Section count check:", html.count('class="section-title"'))
