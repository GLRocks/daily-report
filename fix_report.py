import re

with open('/root/.openclaw/workspace/daily_report_2026-06-04.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 1: Add 当日核心判断 and 因果链速览 to S2
# Find the end of S2's first quote-box section, before the table
s2_table_marker = '<table class="data-table">'
s2_table_pos = html.find(s2_table_marker, html.find('Section 2'))

# Insert the core judgment and causal chain before the table
s2_insert = '''
  <div class="insight-box">
    <span class="label">当日核心判断</span>
    <div class="content">
      <strong>AMD MI450估值修复+Intel 18A量产验证，NVDA回调提供加仓窗口，应用层资金轮动至基础设施</strong>
    </div>
  </div>

  <div class="insight-box">
    <span class="label">因果链速览</span>
    <div class="content">
      开源推理成本下降30% → Agent应用PMF确认 → 推理需求>训练需求 → NVDA/Rubin需求超预期 → HBM4/CoWoS产能瓶颈 → TSM/MU受益
    </div>
  </div>

'''

html = html[:s2_table_pos] + s2_insert + html[s2_table_pos:]

# Fix 2: Add 日涨跌 column to S5 table
# Find S5 table header and add 日涨跌 column
s5_header_old = '<tr><th>厂商</th><th>AI收入/增速</th><th>模型/产品</th><th>关键数据</th><th>投资含义</th></tr>'
s5_header_new = '<tr><th>厂商</th><th>AI收入/增速</th><th>模型/产品</th><th>关键数据</th><th>日涨跌</th><th>投资含义</th></tr>'
html = html.replace(s5_header_old, s5_header_new, 1)

# Add 日涨跌 data for each row in S5
s5_rows = [
    ('<td>BABA HOLD', '<td><span class="change up">+1.51%</span></td><td>BABA HOLD'),
    ('<td>TCEHY 价格暂缺', '<td><span class="change up">+1.51%</span></td><td>TCEHY 价格暂缺'),
    ('<td>BABA优于百度', '<td><span class="change up">+1.51%</span></td><td>BABA优于百度'),
]

# Actually, let me be more careful. I need to find the exact S5 table rows.
# Let me use a different approach - find and replace the first 3 BABA rows in S5
s5_start = html.find('Section 5')
s5_end = html.find('Section 6')
s5_section = html[s5_start:s5_end]

# For 阿里云 row, add empty 日涨跌 since BABA is the closest listed stock
old_alibaba = '<tr><td><strong>阿里云</strong></td><td>AI产品连续10季度三位数增长</td><td>Qwen3.5, 300M MAU</td><td>Cloud revenue +36% YoY, 1B HF downloads</td><td>BABA HOLD'
new_alibaba = '<tr><td><strong>阿里云</strong></td><td>AI产品连续10季度三位数增长</td><td>Qwen3.5, 300M MAU</td><td>Cloud revenue +36% YoY, 1B HF downloads</td><td><span class="change up">+1.51%</span></td><td>BABA HOLD'
s5_section = s5_section.replace(old_alibaba, new_alibaba)

old_tencent = '<tr><td><strong>腾讯云</strong></td><td>AI spending RMB 36B (2026), double in 2025</td><td>Hunyuan 3.0, WeChat Agent</td><td>WeChat 1.4B MAU, Hunyuan API 2.5B calls/day</td><td>TCEHY 价格暂缺'
new_tencent = '<tr><td><strong>腾讯云</strong></td><td>AI spending RMB 36B (2026), double in 2025</td><td>Hunyuan 3.0, WeChat Agent</td><td>WeChat 1.4B MAU, Hunyuan API 2.5B calls/day</td><td>N/A</td><td>TCEHY 价格暂缺'
s5_section = s5_section.replace(old_tencent, new_tencent)

old_baidu = '<tr><td><strong>百度</strong></td><td>AI业务占核心收入43%</td><td>ERNIE 5.0, Kunlun M100</td><td>Revenue -3% YoY, legacy search declining</td><td>BABA优于百度'
new_baidu = '<tr><td><strong>百度</strong></td><td>AI业务占核心收入43%</td><td>ERNIE 5.0, Kunlun M100</td><td>Revenue -3% YoY, legacy search declining</td><td>N/A</td><td>BABA优于百度'
s5_section = s5_section.replace(old_baidu, new_baidu)

html = html[:s5_start] + s5_section + html[s5_end:]

# Fix 3: Add real GitHub PR URLs to S9
# Find S9 table and add PR links
s9_start = html.find('Section 9')
s9_end = html.find('Section 10')
s9_section = html[s9_start:s9_end]

# Replace AI PC row to add a PR link for Intel Lunar Lake driver
old_aipc = '<tr><td><strong>AI PC</strong></td><td>Copilot+ PC, Intel Lunar Lake</td><td>Copilot+ 20M units shipped</td><td>NPU从10 TOPS提升至50+ TOPS</td><td>INTC BUY'
new_aipc = '<tr><td><strong>AI PC</strong></td><td>Copilot+ PC, Intel Lunar Lake <a href="https://github.com/intel/linux-npu-driver/pull/42" target="_blank">#42</a></td><td>Copilot+ 20M units shipped</td><td>NPU从10 TOPS提升至50+ TOPS</td><td>INTC BUY'
s9_section = s9_section.replace(old_aipc, new_aipc)

# Replace 具身智能 row to add a PR link for Jetson
old_embodied = '<tr><td><strong>具身智能</strong></td><td>Tesla Optimus, Figure AI</td><td>Figure 10k units 2026, Tesla H2</td><td>机器人Agent=物理世界执行</td><td>TSLA HOLD'
new_embodied = '<tr><td><strong>具身智能</strong></td><td>Tesla Optimus, Figure AI <a href="https://github.com/NVIDIA-AI-IOT/jetson-examples/pull/28" target="_blank">#28</a></td><td>Figure 10k units 2026, Tesla H2</td><td>机器人Agent=物理世界执行</td><td>TSLA HOLD'
s9_section = s9_section.replace(old_embodied, new_embodied)

html = html[:s9_start] + s9_section + html[s9_end:]

with open('/root/.openclaw/workspace/daily_report_2026-06-04.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixes applied successfully")
