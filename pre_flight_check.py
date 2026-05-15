#!/usr/bin/env python3
"""
pre_flight_check.py — Automated quality gate before deployment
FAIL = stop deployment, do not pass go
called by cron after report generation and before git push
"""
import sys
import re
import os
import csv

def fatal(msg):
    print(f"FATAL: {msg}")
    sys.exit(1)

def warn(msg):
    print(f"WARN: {msg}")

def check(report_path):
    if not os.path.exists(report_path):
        fatal(f"Report file not found: {report_path}")
    
    with open(report_path, 'r') as f:
        html = f.read()
    
    # === STRUCTURE CHECKS ===
    checks = {
        'section-title': 13,
        'stock-card': 21,
        'rec-badge': 21,
        'cat-badge': 21,
        'quote-box': 4,
        'insight-box': 13,
        'data-table': 13,
    }
    
    for cls, expected in checks.items():
        actual = html.count(f'class="{cls}"')
        if actual != expected:
            fatal(f"{cls}: expected {expected}, found {actual}")
        print(f"PASS: {cls} = {actual}")
    
    # === SOURCE LINKS VALIDITY ===
    bad_links = html.count('href="#"')
    if bad_links > 0:
        fatal(f"{bad_links} links have href='#' — must be real URLs")
    print("PASS: No href='#' placeholder links")
    
    # === PLAY-BTN CLICKABILITY (V12: must be <a> tag with href) ===
    play_btns = re.findall(r'<[^>]*class="play-btn"[^>]*>', html)
    for btn in play_btns:
        if '<a ' not in btn:
            fatal(f"play-btn must be <a> tag with href, found: {btn}")
    print(f"PASS: All {len(play_btns)} play-btn(s) are clickable <a> tags")
    
    # === CSS VARIABLES ===
    required_vars = ['--accent: #00d4ff', '--highlight: #e94560', '--bg: #0a0e1a']
    for var in required_vars:
        if var not in html:
            fatal(f"CSS variable missing: {var}")
    print("PASS: CSS variables intact")
    
    # === DATE CHECK ===
    title_date = re.search(r'title>Agentic Market Daily \| (\d{4}-\d{2}-\d{2})', html)
    if not title_date:
        fatal("Date not found in title")
    print(f"PASS: Date = {title_date.group(1)}")
    
    # === NO BROKEN ENTITIES ===
    if '&lt;div' in html or '&gt;div' in html:
        fatal("Escaped HTML entities found — template corrupted")
    print("PASS: No escaped entities")
    
    # === STOCK COUNT BY CATEGORY ===
    chip_count = html.count('cat-badge">芯片')
    app_count = html.count('cat-badge">应用')
    energy_count = html.count('cat-badge">能源')
    if chip_count != 10 or app_count != 8 or energy_count != 3:
        fatal(f"Category counts wrong: 芯片={chip_count}, 应用={app_count}, 能源={energy_count}")
    print(f"PASS: Categories 芯片={chip_count} 应用={app_count} 能源={energy_count}")
    
    # === STOCK DATA CSV VALIDATION ===
    csv_path = report_path.replace('.html', '_stocks.csv')
    if not os.path.exists(csv_path):
        warn(f"Stock CSV not found: {csv_path} — stock prices may be hardcoded")
    else:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            tickers = [r.get('ticker', '') for r in rows]
            missing_price = [r.get('ticker', '?') for r in rows if not r.get('close') or r.get('close') == '']
            if len(rows) < 20:
                fatal(f"CSV only has {len(rows)} stocks, expected 21")
            if missing_price:
                fatal(f"Stocks missing price: {', '.join(missing_price)}")
            print(f"PASS: Stock CSV valid — {len(rows)} stocks, all have close price")
    
    # === RATING CONSISTENCY (basic: check S1 vs S13) ===
    s1_ratings = {}
    s1_cards = re.findall(r'<div class="stock-card[^"]*"[^>]*>.*?<span class="rec-badge[^"]*">([^<]+)</span>.*?<div class="ticker">([^<]+)</div>', html, re.DOTALL)
    for badge, ticker in s1_cards:
        s1_ratings[ticker] = badge.strip()
    
    # Check S13 mentions of same tickers
    inconsistencies = []
    for ticker, s1_rating in s1_ratings.items():
        # Look for explicit rating mentions in S13 insight boxes
        s13_matches = re.findall(rf'{ticker}[^。]*?([B|S][^\s]*)', html)
        for m in s13_matches:
            if 'BUY' in m or 'HOLD' in m or 'SPEC' in m:
                s13_rating = m.strip()
                if s13_rating != s1_rating and not (s1_rating == 'BUY' and s13_rating == 'BUY'):
                    # Allow partial match (e.g. "维持BUY" contains BUY)
                    if s1_rating not in s13_rating and s13_rating not in s1_rating:
                        inconsistencies.append(f"{ticker}: S1={s1_rating} vs S13 text='{s13_rating}'")
    
    if inconsistencies:
        for inc in inconsistencies[:3]:
            warn(f"Rating inconsistency: {inc}")
    else:
        print("PASS: No obvious rating inconsistencies")
    
    # === POLICY SOURCE CHECK (S11) ===
    s11_section = re.search(r'<div class="section">.*?<span class="num">11</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s11_section:
        s11_html = s11_section.group(0)
        # Check for known bad sources
        bad_sources = ['ASML 2025年报', 'ASML年报']
        for bad in bad_sources:
            if bad in s11_html:
                fatal(f"S11 contains prohibited source: '{bad}' — policy info must cite government sources (BIS/Commerce/EU Commission)")
        print("PASS: S11 no prohibited sources detected")
    
    # === GEN-Z SOURCE CHECK (S12) ===
    s12_section = re.search(r'<div class="section">.*?<span class="num">12</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s12_section:
        s12_html = s12_section.group(0)
        # Check for SQ Magazine repeated use
        sq_count = s12_html.count('SQ Magazine')
        if sq_count >= 3:
            fatal(f"S12 cites 'SQ Magazine' {sq_count} times — max 2 per section, and must verify source credibility")
        print(f"PASS: S12 SQ Magazine citations = {sq_count} (max 2)")
    
    print("\n=== ALL CRITICAL CHECKS PASSED ===")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 pre_flight_check.py <report.html>")
        sys.exit(1)
    check(sys.argv[1])