#!/usr/bin/env python3
"""
Generate 2026-08-08 daily report from 2026-08-07 template.
Weekend edition - markets closed, using Friday 08/07 data.
Uses regex to update stock prices and key sections without loading full HTML into AI context.
"""
import re

STOCKS = {
    "NVDA": {"price": 224.11, "change": 2.23},
    "AMD": {"price": 483.13, "change": 0.22},
    "INTC": {"price": 101.64, "change": 0.57},
    "QCOM": {"price": 167.86, "change": 6.56},
    "AVGO": {"price": 427.99, "change": 2.32},
    "TSM": {"price": 420.01, "change": 1.45},
    "MU": {"price": 880.52, "change": -1.42},
    "AMAT": {"price": 539.15, "change": 0.92},
    "LRCX": {"price": 311.55, "change": 1.34},
    "ASML": {"price": 1741.54, "change": 3.77},
    "GOOGL": {"price": 354.24, "change": -2.26},
    "MSFT": {"price": 500.61, "change": 2.70},
    "META": {"price": 592.08, "change": 0.56},
    "AAPL": {"price": 313.30, "change": 0.74},
    "PLTR": {"price": 171.99, "change": 8.56},
    "SNOW": {"price": 330.29, "change": 3.86},
    "BABA": {"price": 128.40, "change": -0.11},
    "TSLA": {"price": 328.77, "change": 2.25},
    "CCJ": {"price": 97.39, "change": 4.03},
    "CEG": {"price": 269.89, "change": 3.37},
    "OKLO": {"price": 48.42, "change": 14.77},
}

S2_JUDGMENT = "QCOM+6.56%领跑半导体，OKLO+14.77%核能升温，GOOGL反垄断承压跌2.26%"

def update_stock_cards(html):
    """Update all stock card price and change tags."""
    for ticker, data in STOCKS.items():
        cls = "change up" if data["change"] >= 0 else "change down"
        sign = "+" if data["change"] >= 0 else ""
        
        # Pattern: <div class="stock-ticker">TICKER</div> followed by price and change
        # Match the whole stock-card block for this ticker
        pat = re.compile(
            rf'(<div class="stock-card[^"]*"[^>]*>.*?<div class="stock-ticker">{re.escape(ticker)}</div>\s*<div class="stock-price">)\$[\d,]+\.\d+(</div>\s*<span class="change )(?:up|down)(">)[\+\-]?\d+\.\d+%(</span>)',
            re.DOTALL
        )
        html = pat.sub(rf'\1${data["price"]:.2f}\2{cls}\3{sign}{data["change"]:.2f}%\4', html)
    return html

def main():
    with open("/root/.openclaw/workspace/daily_report_2026-08-07.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Update dates
    html = html.replace("2026-08-07", "2026-08-08")
    html = html.replace("August 7, 2026", "August 8, 2026")
    html = html.replace("2026年8月7日", "2026年8月8日")
    html = html.replace("Friday", "Saturday")
    html = html.replace("周五", "周六")
    
    # Update stock prices
    html = update_stock_cards(html)
    
    # Update S2 judgment text
    html = re.sub(
        r'(<div class="judgment-text" id="s2-judgment">).*?(</div>)',
        rf'\1{S2_JUDGMENT}\2',
        html,
        flags=re.DOTALL
    )
    
    # Add weekend banner after S1
    weekend_banner = '''<div class="weekend-note" style="background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; margin: 20px 0; text-align: center;">
        <p style="margin: 0; color: var(--text-secondary); font-size: 0.95rem;">📅 <strong>周末市场休市</strong> · 使用周五(8/7)收盘数据 · Q3财报季临近，关注下周业绩指引</p>
    </div>'''
    
    # Insert after S1 section closing
    html = re.sub(
        r'(</section>\s*)(<section id="s2")',
        rf'\1{weekend_banner}\n    \2',
        html
    )
    
    # Write output
    with open("/root/.openclaw/workspace/daily_report_2026-08-08.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # Write judgment
    with open("/root/.openclaw/workspace/today_judgment.txt", "w", encoding="utf-8") as f:
        f.write(S2_JUDGMENT)
    
    # Write CSV
    with open("/root/.openclaw/workspace/daily_report_2026-08-08_stocks.csv", "w") as f:
        f.write("ticker,price,change_pct\n")
        for t, d in STOCKS.items():
            f.write(f"{t},{d['price']},{d['change']}\n")
    
    print(f"✅ daily_report_2026-08-08.html generated")
    print(f"✅ Judgment ({len(S2_JUDGMENT)} chars): {S2_JUDGMENT}")
    print(f"✅ Stock CSV written")

if __name__ == "__main__":
    main()
