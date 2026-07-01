#!/usr/bin/env python3
import re

with open('/root/.openclaw/workspace/daily_report_2026-06-02.html', 'r') as f:
    html = f.read()

# Add data-table to S7 (after causal-chain)
s7_insert = '''  </div>
  <table class="data-table">
    <thead>
      <tr><th>协议</th><th>版本</th><th>支持方</th><th>关键特性</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>MCP</strong></td><td>v2.0</td><td>OpenAI/Anthropic/Google/MS</td><td>Agent互操作标准化</td><td>PLTR BUY</td></tr>
      <tr><td><strong>A2A</strong></td><td>Draft</td><td>Google</td><td>Agent-to-Agent通信</td><td>GOOGL BUY</td></tr>
      <tr><td><strong>vLLM</strong></td><td>v0.10</td><td>开源社区</td><td>1000K+上下文</td><td>NVDA BUY</td></tr>
    </tbody>
  </table>
</div>'''
html = html.replace('''  </div>
</div>

<!-- ==================== S8:''', s7_insert + '\n\n<!-- ==================== S8:')

# Add data-table to S8 (after causal-chain)
s8_insert = '''  </div>
  <table class="data-table">
    <thead>
      <tr><th>项目</th><th>版本</th><th>关键突破</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>vLLM</strong></td><td>v0.10</td><td>1000K context, Agent循环+40%</td><td>NVDA BUY</td></tr>
      <tr><td><strong>SGLang</strong></td><td>v0.8</td><td>多Agent并行调度</td><td>AMD BUY</td></tr>
      <tr><td><strong>DeepSeek V4</strong></td><td>2026-05</td><td>MoE 1.2T, 推理成本↓70%</td><td>BABA HOLD</td></tr>
    </tbody>
  </table>
</div>'''
html = html.replace('''  </div>
</div>

<!-- ==================== S9:''', s8_insert + '\n\n<!-- ==================== S9:')

# Add data-table to S12 (after quote-box)
s12_insert = '''  </div>
  <table class="data-table">
    <thead>
      <tr><th>指标</th><th>2025</th><th>2026</th><th>变化</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>日均AI使用时长</strong></td><td>23min</td><td>67min</td><td>+191%</td><td>AI应用渗透深化</td></tr>
      <tr><td><strong>AI滤镜使用率</strong></td><td>72%</td><td>85%</td><td>+13pp</td><td>META/SNAP受益</td></tr>
      <tr><td><strong>AI疲劳比例</strong></td><td>12%</td><td>35%</td><td>+23pp</td><td>产品差异化关键</td></tr>
    </tbody>
  </table>
</div>'''
html = html.replace('''  </div>
</div>

<!-- ==================== S13:''', s12_insert + '\n\n<!-- ==================== S13:')

with open('/root/.openclaw/workspace/daily_report_2026-06-02.html', 'w') as f:
    f.write(html)

print("HTML updated with additional data-table elements.")
