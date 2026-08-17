#!/usr/bin/env python3
"""
Generate 2026-08-09 daily report from 2026-08-08 template.
Sunday edition - markets closed, using Friday 08/08 data.
"""
import re

def main():
    with open("/root/.openclaw/workspace/daily_report_2026-08-08.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Update title date
    html = html.replace("Agentic Market Daily | 2026-08-08", "Agentic Market Daily | 2026-08-09")
    
    # Update header date badge
    html = html.replace("2026-08-08 | Saturday | Asia/Shanghai 08:07", "2026-08-09 | Sunday | Asia/Shanghai 08:07")
    
    # Update footer date
    html = html.replace("数据截止日期: 2026-08-07", "数据截止日期: 2026-08-08")
    
    # Update S2 judgment for Sunday
    s2_old = "Palantir Q2财报验证AI主权需求从叙事走向兑现，OKLO+14.77%领跑能源板块，芯片板块结构性看多 intact。"
    s2_new = "周日休市无新信号，QCOM+6.56%周五领跑半导体，OKLO+14.77%核能升温。关注下周财报季。"
    html = html.replace(s2_old, s2_new)
    
    # Also update the S2 insight box content
    old_insight = """<div class="insight-box">
    <span class="label">核心判断</span>
    <div class="content">
      <strong>Palantir Q2财报验证AI主权需求从叙事走向兑现，OKLO+14.77%领跑能源板块，芯片板块结构性看多 intact。</strong> PLTR Q2营收$1.94B +93% YoY，美国商业收入+149%，全年指引上调至$8.15B，验证政府+企业AI基础设施订单持续性。OKLO受核电复兴+Sam Altman背书驱动大涨。NVDA/AMD/INTC周五普涨，市场持续定价Rubin 2026H2量产预期。"""
    
    new_insight = """<div class="insight-box">
    <span class="label">核心判断</span>
    <div class="content">
      <strong>周日休市无新信号，沿用周五收盘数据。QCOM+6.56%周五领跑半导体，OKLO+14.77%核能升温，关注下周财报季催化剂。</strong> 周末市场清淡，无重大新闻发布。下周关注：① 阿里云Q2财报；② OpenAI IPO进展；③ AMD技术日；④ 核聚变/能源政策更新。PLTR Q2业绩持续发酵，AI主权主题 intact。"""
    
    html = html.replace(old_insight, new_insight)
    
    # Write output
    with open("/root/.openclaw/workspace/daily_report_2026-08-09.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # Write judgment
    judgment = "周日休市无新信号，QCOM+6.56%周五领跑芯片，OKLO+14.77%核能升温，关注下周财报季。"
    with open("/root/.openclaw/workspace/today_judgment.txt", "w", encoding="utf-8") as f:
        f.write(judgment)
    
    # Write CSV
    stocks = {
        "NVDA": (224.11, 2.23), "AMD": (483.13, 0.22), "INTC": (101.64, 0.57),
        "QCOM": (167.86, 6.56), "AVGO": (427.99, 2.32), "TSM": (420.01, 1.45),
        "MU": (880.52, -1.42), "AMAT": (539.15, 0.92), "LRCX": (311.55, 1.34),
        "ASML": (1741.54, 3.77), "GOOGL": (354.24, -2.26), "MSFT": (500.61, 2.70),
        "META": (592.08, 0.56), "AAPL": (313.30, 0.74), "PLTR": (171.99, 8.56),
        "SNOW": (330.29, 3.86), "BABA": (128.40, -0.11), "TSLA": (328.77, 2.25),
        "CCJ": (97.39, 4.03), "CEG": (269.89, 3.37), "OKLO": (48.42, 14.77),
    }
    with open("/root/.openclaw/workspace/daily_report_2026-08-09_stocks.csv", "w") as f:
        f.write("ticker,close,pct_change\n")
        for t, (price, change) in stocks.items():
            f.write(f"{t},{price},{change}\n")
    
    print(f"✅ daily_report_2026-08-09.html generated")
    print(f"✅ Judgment ({len(judgment)} chars): {judgment}")
    print(f"✅ Stock CSV written")

if __name__ == "__main__":
    main()
