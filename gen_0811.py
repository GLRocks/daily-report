#!/usr/bin/env python3
"""Generate 2026-08-11 daily report from 2026-08-10 template."""
import re
import csv

def main():
    # Read template (Aug 10 report)
    with open("/root/.openclaw/workspace/daily_report_2026-08-10.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Update title date
    html = html.replace("Agentic Market Daily | 2026-08-10", "Agentic Market Daily | 2026-08-11")
    
    # Update header date badge
    html = html.replace("2026-08-10 | Monday | Asia/Shanghai 08:07", "2026-08-11 | Tuesday | Asia/Shanghai 08:07")
    
    # Update footer date
    html = html.replace("数据截止日期: 2026-08-08", "数据截止日期: 2026-08-10")
    
    # Read stock data from CSV
    stocks = {}
    with open("/root/.openclaw/workspace/stock_data_2026-08-10.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticker = row['ts_code'].replace('.US', '')
            stocks[ticker] = {
                'price': float(row['close']),
                'change': float(row['pct_change'])
            }
    
    # Update stock prices using regex - match the price-row structure
    for ticker, data in stocks.items():
        price = data['price']
        change = data['change']
        change_class = 'up' if change >= 0 else 'down'
        change_str = f'+{change:.2f}%' if change >= 0 else f'{change:.2f}%'
        
        # Pattern to match the price and change span within a stock card
        # Look for ticker, then price, then change
        pattern = rf'(<div class="ticker">{ticker}</div>.*?<span class="price">)\$[\d.,]+(</span>\s*<span class="change )[\w]+(">)[+-]?[\d.]+%(</span>)'
        repl = rf'\1${price:.2f}\2{change_class}\3{change_str}\4'
        html = re.sub(pattern, repl, html, flags=re.DOTALL, count=1)
    
    # Read S2 judgment
    with open("/root/.openclaw/workspace/today_judgment.txt", "r") as f:
        judgment = f.read().strip()
    
    # Update S2 core judgment - try to find and replace the insight-box content
    # Find the S2 section and replace the core judgment text
    s2_start = html.find('<div class="section-title"><span class="num">2</span>')
    s2_end = html.find('<div class="section-title"><span class="num">3</span>')
    
    if s2_start > 0 and s2_end > 0:
        s2_html = html[s2_start:s2_end]
        # Try to find the strong tag with judgment and replace
        # Match: <strong>...</strong> within the insight-box content
        old_strong_pattern = r'(<div class="insight-box">.*?<span class="label">核心判断</span>.*?<div class="content">\s*<strong>)(.*?)(</strong>)'
        match = re.search(old_strong_pattern, s2_html, re.DOTALL)
        if match:
            old_judgment = match.group(2)
            s2_html = s2_html.replace(old_judgment, judgment)
            html = html[:s2_start] + s2_html + html[s2_end:]
            print(f"S2 judgment updated: {judgment}")
        else:
            print("WARNING: Could not find S2 judgment to replace")
    
    # Write output
    output_path = "/root/.openclaw/workspace/daily_report_2026-08-11.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ {output_path} generated")
    print(f"✅ Judgment ({len(judgment)} chars): {judgment}")
    print(f"✅ Stock prices updated for {len(stocks)} tickers")

if __name__ == "__main__":
    main()
