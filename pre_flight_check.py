#!/usr/bin/env python3
"""
pre_flight_check.py — Automated quality gate before deployment
Updated 2026-05-16: 14 sections, no stock change%, no S4 daily change column
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
    structure_checks = {
        'section-title': 14,
        'stock-card': 21,
        'rec-badge': 21,
        'cat-badge': 21,
    }
    
    for cls, expected in structure_checks.items():
        if cls in ('stock-card', 'rec-badge', 'cat-badge'):
            actual = len(re.findall(rf'class="{cls}(?:\s+[^\"]*?)?"', html))
        else:
            actual = html.count(f'class="{cls}"')
        if actual != expected:
            fatal(f"{cls}: expected {expected}, found {actual}")
        print(f"PASS: {cls} = {actual}")
    
    # === SECTION 2: EXPERT CONSENSUS CHECK ===
    s2 = re.search(r'<span class="num">2</span>.*?</div>', html, re.DOTALL)
    if not s2:
        fatal("S2 (专家共识) missing — must be present as section 2")
    s2_html = s2.group(0)
    if '当日核心判断' not in s2_html and '核心判断' not in s2_html:
        warn("S2 may be missing '当日核心判断'")
    if '因果链' not in s2_html:
        warn("S2 may be missing '因果链速览'")
    print("PASS: S2 (专家共识) present")
    
    # === INSIGHT-BOX COUNT ===
    insight_count = html.count('class="insight-box"')
    if insight_count < 8:
        fatal(f"insight-box: expected at least 8 (sections 2-14), found {insight_count}")
    print(f"PASS: insight-box = {insight_count} (sections 2-14)")
    
    # === DATA-TABLE COUNT ===
    table_count = html.count('<table class="data-table">')
    if table_count < 2:
        fatal(f"data-table: expected at least 2, found {table_count}")
    print(f"PASS: data-table = {table_count}")
    
    # === NO STOCK CHANGE% (P0 fix 2026-05-15) - RELAXED per user task 2026-06-04 ===
    stock_changes = re.findall(r'class="change[^"]*"', html)
    if stock_changes:
        print(f"INFO: Stock change% found: {len(stock_changes)} — per template V12, S1 cards show change%")
    else:
        print("INFO: No stock change% elements")
    
    # === S5 TABLE: 日涨跌 COLUMN CHECK (template V12 requires this) ===
    s5_section = re.search(r'<span class="num">5</span>.*?</table>', html, re.DOTALL)
    if s5_section:
        if '日涨跌' in s5_section.group(0):
            print("PASS: S5 table has 日涨跌 column (template V12 compliant)")
        else:
            print("WARN: S5 table missing 日涨跌 column — per template V12 requirement")
    
    # === S9 PR LINK CHECK (open source section, per template V12) ===
    s9_section = re.search(r'<span class="num">9</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s9_section:
        s9_html = s9_section.group(0)
        pr_links = re.findall(r'github\.com/(vllm-project|sgl-project)/[^"]+/pull/\d+', s9_html)
        if len(pr_links) < 2:
            fatal(f"S9 PR links missing: expected >=2 GitHub PR URLs, found {len(pr_links)}")
        print(f"PASS: S9 PR links = {len(pr_links)}")
    
    # === SOURCE LINKS VALIDITY ===
    bad_links = html.count('href="#"')
    if bad_links > 0:
        fatal(f"{bad_links} links have href='#' — must be real URLs")
    print("PASS: No href='#' placeholder links")
    
    # === PLAY-BTN CLICKABILITY ===
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
    total = chip_count + app_count + energy_count
    if total != 21:
        fatal(f"Total stock cards = {total}, expected 21")
    if chip_count != 10 or app_count != 8 or energy_count != 3:
        warn(f"Category counts: 芯片={chip_count}, 应用={app_count}, 能源={energy_count} (target: 10/8/3)")
    else:
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
                fatal(f"CSV only has {len(rows)} stocks, expected at least 20")
            if len(missing_price) > 1:
                fatal(f"Stocks missing price: {', '.join(missing_price)} — max 1 allowed (TCEHY)")
            print(f"PASS: Stock CSV valid — {len(rows)} stocks, {len(missing_price)} without price (allowed)")
    
    # === RATING CONSISTENCY ===
    s1_ratings = {}
    s1_cards = re.findall(r'<div class="stock-card[^"]*"[^>]*>.*?<span class="rec-badge[^"]*">([^<]+)</span>.*?<div class="ticker">([^<]+)</div>', html, re.DOTALL)
    for badge, ticker in s1_cards:
        s1_ratings[ticker] = badge.strip()
    
    inconsistencies = []
    for ticker, s1_rating in s1_ratings.items():
        s14_matches = re.findall(rf'{ticker}[^。]*?([B|S][^\s]*)', html)
        for m in s14_matches:
            if 'BUY' in m or 'HOLD' in m or 'SPEC' in m:
                s14_rating = m.strip()
                if s14_rating != s1_rating and not (s1_rating == 'BUY' and s14_rating == 'BUY'):
                    if s1_rating not in s14_rating and s14_rating not in s1_rating:
                        inconsistencies.append(f"{ticker}: S1={s1_rating} vs S14 text='{s14_rating}'")
    
    if inconsistencies:
        for inc in inconsistencies[:3]:
            warn(f"Rating inconsistency: {inc}")
    else:
        print("PASS: No obvious rating inconsistencies")
    
    # === POLICY SOURCE CHECK (S12, was S11) ===
    s12_section = re.search(r'<span class="num">12</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s12_section:
        s12_html = s12_section.group(0)
        bad_sources = ['ASML 2025年报', 'ASML年报']
        for bad in bad_sources:
            if bad in s12_html:
                fatal(f"S12 contains prohibited source: '{bad}'")
        print("PASS: S12 no prohibited sources detected")
    
    # === GEN-Z SOURCE CHECK (S13, was S12) ===
    s13_section = re.search(r'<span class="num">13</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s13_section:
        s13_html = s13_section.group(0)
        sq_count = s13_html.count('SQ Magazine')
        if sq_count >= 3:
            fatal(f"S13 cites 'SQ Magazine' {sq_count} times — max 2 per section")
        print(f"PASS: S13 SQ Magazine citations = {sq_count} (max 2)")
    
    # === CONTENT QUALITY CHECKS ===
    print("\n=== CONTENT QUALITY CHECKS ===")
    
    # CQ1: Model version (S4, was S3)
    s4_section = re.search(r'<span class="num">4</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s4_section:
        s4_html = s4_section.group(0)
        outdated_patterns = ['GPT-4', 'GPT-4.1', 'Claude 3', 'Kimi K2.5', 'Gemini 1.5']
        for pattern in outdated_patterns:
            if pattern in s4_html:
                if '历史' not in s4_html and '此前' not in s4_html:
                    print(f"WARN: S4 may contain outdated model version '{pattern}'")
    print("CQ1: Model version check completed")
    
    # CQ2: Earnings data (S5, was S4)
    s5_section = re.search(r'<span class="num">5</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s5_section:
        s5_html = s5_section.group(0)
        q1_count = len(re.findall(r'Q1\s+2026', s5_html))
        if q1_count > 0:
            print(f"INFO: S5 contains {q1_count} Q1 2026 references — verify Q2 not yet available")
    print("CQ2: Earnings data freshness check completed")
    
    # CQ3: PR verification (S9 — open source section with PR links)
    s9_section = re.search(r'<span class="num">9</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s9_section:
        s9_html = s9_section.group(0)
        pr_no_links = re.findall(r'PR\s+#(\d+)(?![0-9])(?!\s*<)', s9_html)
        if pr_no_links:
            fatal(f"S9 contains PR numbers without hyperlinks: {pr_no_links}")
        non_github_links = re.findall(r'href="(?!https://github\.com)[^"]*pull[^"]*"', s9_html)
        if non_github_links:
            fatal(f"S9 contains non-GitHub PR links: {non_github_links}")
        github_links = re.findall(r'github\.com/(vllm-project|sgl-project)/[^"]+/pull/\d+', s9_html)
        if len(github_links) < 2:
            fatal(f"S9 PR links insufficient: {len(github_links)} found, minimum 2 required")
        print(f"CQ3: S9 GitHub PR links = {len(github_links)} — OK")
    
    # CQ4: Policy source ban (S12)
    s12_section = re.search(r'<span class="num">12</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s12_section:
        s12_html = s12_section.group(0)
        banned_sources = ['ASML 2025年报', 'ASML年报', '设备商财报']
        for bad in banned_sources:
            if bad in s12_html:
                fatal(f"CQ4: S12 contains banned source '{bad}'")
        print("CQ4: S12 policy sources OK")
    
    # CQ5: Research sample size (S13)
    s13_section = re.search(r'<span class="num">13</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s13_section:
        s13_html = s13_section.group(0)
        research_patterns = re.findall(r'([\d,]+\s*(?:users|people|respondents|participants))', s13_html)
        if not research_patterns:
            survey_claims = re.findall(r'(survey|study|research|poll)', s13_html, re.IGNORECASE)
            if survey_claims:
                print(f"WARN: CQ5: S13 contains {len(survey_claims)} survey references — verify all have sample sizes")
        else:
            print(f"CQ5: S13 sample sizes found: {len(research_patterns)} — OK")
    
    # CQ6: International source ratio
    domestic_patterns = ['36kr', '钛媒体', '品玩', '雷锋网', '第一财经', '财新']
    domestic_count = sum(html.count(p) for p in domestic_patterns)
    if domestic_count > 5:
        print(f"WARN: CQ6: {domestic_count} domestic source references found — verify international ratio >=80%")
    else:
        print("CQ6: International source ratio OK")
    
    print("\n=== ALL CRITICAL CHECKS PASSED ===")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 pre_flight_check.py <report.html>")
        sys.exit(1)
    check(sys.argv[1])
