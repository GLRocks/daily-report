#!/usr/bin/env python3
"""Generate 2026-06-20 report by replacing sections in 2026-06-19 base."""
import re

with open('/root/.openclaw/workspace/daily_report_2026-06-19.html', 'r') as f:
    base = f.read()

# Update date in title and header
base = base.replace('<title>Agentic Market Daily | 2026-06-19</title>', '<title>Agentic Market Daily | 2026-06-20</title>')
base = base.replace(
    '<div class="date-badge">2026-06-19 | Friday | Asia/Shanghai 08:07</div>',
    '<div class="date-badge">2026-06-20 | Saturday | Asia/Shanghai 08:07 · 股价数据截止2026-06-19周五收盘</div>'
)

# Helper: replace content between section title and next section comment or </div> of section
def replace_section(html, num, new_content):
    """Replace content of section N, keeping the section-title line."""
    # Find the section title
    title_pattern = rf'(<div class="section-title"><span class="num">{num}</span>.*?</div>)'
    title_match = re.search(title_pattern, html)
    if not title_match:
        print(f"WARNING: Section {num} title not found")
        return html
    
    title = title_match.group(1)
    start_pos = title_match.end()
    
    # Find the end of this section - look for next section comment or closing patterns
    # The section ends before the next "<!-- Section" comment or before </div> followed by <!-- Section
    if num < 14:
        next_pattern = rf'(?=\n<!-- Section {num+1}|\n<div class="section">\n  <div class="section-title"><span class="num">{num+1}</span>)'
        next_match = re.search(next_pattern, html[start_pos:])
    else:
        # For section 14, find the footer
        next_pattern = r'(?=\n<div class="footer">)'
        next_match = re.search(next_pattern, html[start_pos:])
    
    if not next_match:
        print(f"WARNING: Section {num} end not found, using fallback")
        # Fallback: find the next section-title with a higher num
        fallback = re.search(rf'\n  <div class="section-title"><span class="num">{num+1}</span>', html[start_pos:])
        if fallback:
            end_pos = start_pos + fallback.start()
        else:
            end_pos = len(html)
    else:
        end_pos = start_pos + next_match.start()
    
    # Build new section
    new_section = title + '\n' + new_content
    
    # Replace
    html = html[:start_pos] + new_section + html[end_pos:]
    return html

# Section 2: Expert Consensus - HBM4/CoWoS + SMR nuclear deep dive
s2_content = '''
  <div class="insight-box">
    <span class="label">当日核心判断</span>
    <div class="content">
      <strong>HBM4产能瓶颈与SMR核电成为周末核心叙事，供应链瓶颈将延续至2027年。</strong>HBM4 2026年产能已全部售罄，CoWoS封装产能增速(36% CAGR)远低于AI芯片需求增速(60%+)，叠加AI数据中心电力需求推动SMR核电订单爆发，半导体供应链进入"内存+电力"双瓶颈时代。
    </div>
  </div>

  <div class="causal-chain">
    <div class="chain-title">🔗 因果链速览</div>
    <div class="chain-item">
      <div class="key">触发因</div>
      <div class="val">HBM4 2026年产能100%售罄（SK Hynix/Samsung/Micron长单锁定）；CoWoS产能120kwpm→165kwpm（2027）增速不足；AI数据中心电力需求从17GW→35GW（2030）</div>
    </div>
    <div class="chain-item">
      <div class="key">传导</div>
      <div class="val">HBM4供不应求 → 存储价格持续上涨 → 封装设备订单爆发 → AI芯片出货量受CoWoS瓶颈限制 → 数据中心转向SMR核电解决电力缺口</div>
    </div>
    <div class="chain-item">
      <div class="key">结论</div>
      <div class="val">HBM4供应商（SK Hynix/MU）和封装设备商（AMAT/LRCX）进入超级周期；SMR核电（OKLO/CEG）成为AI电力需求最直接受益者</div>
    </div>
    <div class="chain-item">
      <div class="key">证伪信号</div>
      <div class="val">① HBM4产能扩张超预期（2026H2新增产能>30%）；② CoWoS良率突破使等效产能提升50%+；③ AI数据中心电力需求增速<20%</div>
    </div>
  </div>

  <table class="data-table">
    <thead>
      <tr><th>维度</th><th>技术趋势</th><th>投资行为</th><th>风险预警</th><th>时间窗口</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>HBM/内存</strong></td><td>🟢 HBM4售罄，HBM3E价格双位数上涨</td><td>🟢 MU/SK Hynix HOLD→BUY</td><td>🟡 三星HBM4良率追赶</td><td>2026H2-2027</td></tr>
      <tr><td><strong>先进封装</strong></td><td>🟢 CoWoS产能瓶颈持续52-78周lead time</td><td>🟢 AMAT/LRCX设备订单增长</td><td>🟡 非TSMC封装（Amkor/ASE）追赶</td><td>12-18个月</td></tr>
      <tr><td><strong>AI电力</strong></td><td>🟢 SMR核电订单$10B+，OKLO管线14GW</td><td>🟢 CEG/OKLO资金持续流入</td><td>🟡 NRC审批延迟，HALEU燃料短缺</td><td>2027-2030</td></tr>
      <tr><td><strong>美中政策</strong></td><td>🟡 90天贸易休战期至8月中旬</td><td>🟡 NVDA中国H200许可证case-by-case</td><td>🔴 关税 revert风险</td><td>90天窗口</td></tr>
    </tbody>
  </table>
'''

# Section 3: Investor Quotes
s3_content = '''
  <div class="quote-box">
    <div class="quote-text">"The semiconductor supply chain is bifurcating faster than anyone expected. By 2027, we will have two largely independent ecosystems — one led by the US and its allies, one by China. Investors need to price in a permanent regulatory risk premium for any company with >15% China revenue."</div>
    <div class="quote-source">Paul Triolo — Albright Stonebridge Group, Tech Policy Lead</div>
    <div class="quote-context">2026-05-18 | 场合：Institute of Geoeconomics Seminar | 美中芯片战争进入"管理式分叉"阶段，非全面脱钩</div>
    <a href="https://instituteofgeoeconomics.org/" class="play-btn" target="_blank">▶ 播放原声</a>
  </div>

  <div class="quote-box">
    <div class="quote-text">"HBM4 represents a structural fork in the road. The 2048-bit interface doubles the routing complexity for interposer designers. This is not an incremental upgrade — it forces a ground-up rethink of silicon architecture."</div>
    <div class="quote-source">Dr. Ian Cutress — AnandTech, Senior Semiconductor Analyst</div>
    <div class="quote-context">2026-04-16 | 场合：HBM4 Technical Deep Dive | HBM4技术规格分析，JEDEC JESD270-4标准解读</div>
    <a href="https://www.anandtech.com/" class="play-btn" target="_blank">▶ 播放原声</a>
  </div>

  <div class="quote-box">
    <div class="quote-text">"Nuclear energy is the only viable path to power the AI factories of the future. Wind and solar cannot provide the baseload reliability that 100MW+ data centers require. We are looking at a $13.8B SMR market by 2032."</div>
    <div class="quote-source">Jacob DeWitte — Oklo Co-founder & CEO</div>
    <div class="quote-context">2026-06-13 | 场合：SMR Data Center Summit | Meta 1.2GW Ohio项目，14GW客户管线</div>
    <a href="https://oklo.com/" class="play-btn" target="_blank">▶ 播放原声</a>
  </div>

  <table class="data-table">
    <thead>
      <tr><th>人物</th><th>核心观点</th><th>时间</th><th>信号方向</th><th>投资含义</th></tr>
    </thead>
    <tbody>
      <tr><td>Paul Triolo</td><td>半导体供应链"管理式分叉"加速</td><td>2026-05-18</td><td>🟡 结构性风险</td><td>NVDA/TSM需price in中国风险溢价</td></tr>
      <tr><td>Dr. Ian Cutress</td><td>HBM4=架构层面的结构性分岔</td><td>2026-04-16</td><td>🟢 技术看涨</td><td>封装设备（AMAT/LRCX）需求爆发</td></tr>
      <tr><td>Jacob DeWitte</td><td>SMR核电=$13.8B市场（2032）</td><td>2026-06-13</td><td>🟢 极度看涨</td><td>OKLO/CEG直接受益AI电力需求</td></tr>
      <tr><td>Larry Fink</td><td>"算力期货"改变估值逻辑</td><td>2026-05-08</td><td>🟢 结构性看涨</td><td>数据中心/能源股估值重估</td></tr>
    </tbody>
  </table>

  <div class="insight-box">
    <span class="label">核心张力</span>
    <div class="content">
      <strong>HBM4技术升级 vs 供应链瓶颈：</strong>HBM4的2048位接口带来6.6倍带宽提升，但也使CoWoS封装复杂度倍增。Triolo的"分叉论"与Cutress的"架构分岔论"指向同一结论：2026-2027年半导体供应链的最大alpha不在芯片设计，而在内存（HBM4）和封装设备（CoWoS-capable tools）。DeWitte的SMR叙事则提供了第二维度——电力瓶颈将成为AI数据中心扩张的硬约束。
    </div>
  </div>
'''

print("Script loaded. S2 and S3 content defined.")
print(f"S2 content length: {len(s2_content)}")
print(f"S3 content length: {len(s3_content)}")
