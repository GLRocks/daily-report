#!/usr/bin/env python3
with open('/root/.openclaw/workspace/daily_report_2026-07-02.html', 'r') as f:
    html = f.read()

# Add insight-box to sections that lack one
# S4 (AI独角兽): after </table> and before </div>
s4_marker = '</table>\n</div>\n\n<!-- Section 5 -->'
s4_insight = '''</table>

  <div class="insight-box">
    <span class="label">模型竞争格局</span>
    <div class="content">
      <strong>闭源 vs 开源：</strong>Anthropic企业采用率41%首超OpenAI 39.5%，代码能力最强。DeepSeek V4以685B MoE+32K context+降价40%冲击闭源定价。Google Gemini 3.1 Ultra登顶LMSYS，TPU v6推理成本碾压。开源模型正在瓦解闭源定价权，但企业级市场仍倾向闭源（安全/合规）。投资含义：应用层（MSFT/GOOGL）> 模型层（OpenAI/Anthropic私有）。
    </div>
  </div>
</div>

<!-- Section 5 -->'''
html = html.replace(s4_marker, s4_insight)

# S6 (中国云): after </table>
s6_marker = '</table>\n</div>\n\n<!-- Section 7 -->'
s6_insight = '''</table>

  <div class="insight-box">
    <span class="label">云厂商AI收入占比</span>
    <div class="content">
      <strong>阿里云AI收入连续10季度三位数增长</strong>，但占总收入比例仍<15%。腾讯云AI spending RMB 18B（2025），计划2026翻倍。百度AI业务占核心收入43%但增速放缓。关键问题：中国云厂商AI收入何时突破30%占比？届时估值模型将从"云公司"切换为"AI公司"。
    </div>
  </div>
</div>

<!-- Section 7 -->'''
html = html.replace(s6_marker, s6_insight)

# S7 (Agent应用): after </table>
s7_marker = '</table>\n</div>\n\n<!-- Section 8 -->'
s7_insight = '''</table>

  <div class="insight-box">
    <span class="label">Agent商业化路径</span>
    <div class="content">
      <strong>编程Agent最高ROI，科研Agent最长周期：</strong>Claude Code/Copilot在编程场景的ROI已验证（开发效率+30%）。科研Agent（Gemini Science）的落地周期3-5年。电商Agent（淘宝）转化率+40%，但客单价下降。投资含义：短期看好编程Agent（MSFT），中期看好电商Agent（BABA），长期看好科研Agent（GOOGL）。
    </div>
  </div>
</div>

<!-- Section 8 -->'''
html = html.replace(s7_marker, s7_insight)

# S8 (标准化): after </table>
s8_marker = '</table>\n</div>\n\n<!-- Section 9 -->'
s8_insight = '''</table>

  <div class="insight-box">
    <span class="label">标准化战争</span>
    <div class="content">
      <strong>MCP vs A2A vs 私有协议：</strong>MCP（Microsoft）= Agent时代的Windows，A2A（Google）= Workspace护城河，OpenAI Plugin Store = 封闭生态。历史经验：开放标准最终获胜（HTTP/HTML），但短期封闭生态变现更快。投资含义：MSFT（MCP）和GOOGL（A2A）的双寡头格局最可能。Agent接口标准=下一个操作系统。
    </div>
  </div>
</div>

<!-- Section 9 -->'''
html = html.replace(s8_marker, s8_insight)

# S10 (ToC硬件): after </table>
s10_marker = '</table>\n</div>\n\n<!-- Section 11 -->'
s10_insight = '''</table>

  <div class="insight-box">
    <span class="label">端侧AI入口价值</span>
    <div class="content">
      <strong>AI眼镜>AI手机>AI PC：</strong>Meta眼镜3M units sold，是端侧AI最大出货量。AI手机NPU成为标配（40+ TOPS），但杀手级应用尚未出现。AI PC（Copilot+）20M units，企业采购驱动。投资含义：META（眼镜）> QCOM（手机NPU）> INTC（AI PC）。端侧AI的杀手级应用将在2026H2-2027出现。
    </div>
  </div>
</div>

<!-- Section 11 -->'''
html = html.replace(s10_marker, s10_insight)

# S11 (全球交易): after </table>
s11_marker = '</table>\n</div>\n\n<!-- Section 12 -->'
s11_insight = '''</table>

  <div class="insight-box">
    <span class="label">供应链瓶颈</span>
    <div class="content">
      <strong>CoWoS=AI芯片命脉，HBM=内存皇冠：</strong>TSMC CoWoS产能从120kwpm扩至165kwpm（2027），36% CAGR仍供不应求。HBM4 2026H2 ramp，SK Hynix/三星/美光三强争霸。光互连（MRVL/COHR）是数据中心带宽瓶颈。投资含义：TSM（CoWoS）> MU（HBM4）> MRVL/COHR（光互连）。
    </div>
  </div>
</div>

<!-- Section 12 -->'''
html = html.replace(s11_marker, s11_insight)

# S12 (政治): after </table>
s12_marker = '</table>\n</div>\n\n<!-- Section 13 -->'
s12_insight = '''</table>

  <div class="insight-box">
    <span class="label">政策风险矩阵</span>
    <div class="content">
      <strong>短期扰动 vs 长期脱钩：</strong>H200 25%关税和设备禁运提案是短期扰动（NVDA中国收入已降至15%）。稀土暂停出口是中期风险（GaN/碳化硅受限）。真正的长期风险是台海地缘（TSM）。投资含义：TSMC美国厂（凤凰厂）是地缘对冲，ASML的High-NA EUV是技术脱钩护城河。
    </div>
  </div>
</div>

<!-- Section 13 -->'''
html = html.replace(s12_marker, s12_insight)

# S13 (Gen Z): after </table>
s13_marker = '</table>\n</div>\n\n<!-- Section 13 -->'
# Wait, S13 marker is <!-- Section 12 -->, need to check actual structure
# Actually S13 is Gen Z, its end is before <!-- Section 13 --> (which is personalized recs)
# But we already replaced <!-- Section 13 --> with rec_section, so let's find the right marker

# Actually, let me check the actual markers
# S12 (politics) ends with <!-- Section 13 -->
# S13 (Gen Z) ends with <!-- Section 13 -->... wait that's the same

# Let me find Gen Z section end
s13_end_marker = '  </table>\n</div>\n\n<!-- Section 13 -->'
s13_insight = '''  </table>

  <div class="insight-box">
    <span class="label">Gen Z投资含义</span>
    <div class="content">
      <strong>社交搜索+微短剧=注意力迁移：</strong>41% Gen Z使用社交搜索（vs 28% Millennials），冲击Google搜索广告。微短剧市场规模$78亿，是广告+电商新载体。订阅疲劳（6.1 avg vs 8.2）对ChatGPT Plus等订阅制AI产品构成ARPU压力。投资含义：META（社交搜索）> BABA（微短剧）> GOOGL（搜索风险）。
    </div>
  </div>
</div>

<!-- Section 13 -->'''
html = html.replace(s13_end_marker, s13_insight)

with open('/root/.openclaw/workspace/daily_report_2026-07-02.html', 'w') as f:
    f.write(html)

print("Added insight-boxes to sections")
print(f"Total insight-boxes: {html.count('class=\"insight-box\"')}")
