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
    # === STRUCTURE CHECKS ===
    structure_checks = {
        'section-title': 13,
        'stock-card': 21,
        'rec-badge': 21,
        'cat-badge': 21,
        'quote-box': 4,
    }
    
    for cls, expected in structure_checks.items():
        if cls in ('stock-card', 'rec-badge', 'cat-badge'):
            actual = len(re.findall(rf'class="{cls}(?:\s+[^\"]*?)?"', html))
        else:
            actual = html.count(f'class="{cls}"')
        if actual != expected:
            fatal(f"{cls}: expected {expected}, found {actual}")
        print(f"PASS: {cls} = {actual}")
    
    # === INSIGHT-BOX COUNT ===
    # S1 (stock panel) may not have insight-box, so check sections 2-13
    insight_count = html.count('class="insight-box"')
    if insight_count < 12:
        fatal(f"insight-box: expected at least 12 (sections 2-13), found {insight_count}")
    print(f"PASS: insight-box = {insight_count} (sections 2-13)")
    
    # === DATA-TABLE COUNT ===
    table_count = html.count('<table class="data-table">')
    if table_count < 13:
        fatal(f"data-table: expected at least 13, found {table_count}")
    print(f"PASS: data-table = {table_count}")
    
    # === STOCK CHANGE% CHECK ===
    stock_changes = re.findall(r'class="change[^"]*"', html)
    if len(stock_changes) < 20:
        fatal(f"Stock change% missing: expected ≥20, found {len(stock_changes)} — each stock card must show daily change% from CSV pct_change")
    print(f"PASS: Stock change% present = {len(stock_changes)}")
    
    # === S4 TABLE CHANGE COLUMN CHECK ===
    s4_section = re.search(r'<span class="num">4</span>.*?</table>', html, re.DOTALL)
    if s4_section:
        if '日涨跌' not in s4_section.group(0):
            fatal("S4 table missing '日涨跌' column — must show daily price change")
        print("PASS: S4 table has 日涨跌 column")
    
    # === S8 PR LINK CHECK ===
    s8_section = re.search(r'<span class="num">8</span>.*?<!-- Section 9 -->', html, re.DOTALL)
    if s8_section:
        s8_html = s8_section.group(0)
        # Check for PR links
        pr_links = re.findall(r'github\.com/(vllm-project|sgl-project)/[^"]+/pull/\d+', s8_html)
        if len(pr_links) < 2:
            fatal(f"S8 PR links missing: expected ≥2 GitHub PR URLs, found {len(pr_links)} — vLLM/SGLang PRs must be clickable links")
        print(f"PASS: S8 PR links = {len(pr_links)}")
    
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
    
    # === CONTENT QUALITY CHECKS (CQ1-CQ6) ===
    print("\n=== CONTENT QUALITY CHECKS ===")
    
    # CQ1: Model version verification (S3)
    s3_section = re.search(r'<div class="section">.*?<span class="num">3</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s3_section:
        s3_html = s3_section.group(0)
        # Check for potentially outdated model versions
        outdated_patterns = ['GPT-4', 'GPT-4.1', 'Claude 3', 'Kimi K2.5', 'Gemini 1.5']
        for pattern in outdated_patterns:
            if pattern in s3_html:
                # Allow if explicitly marked as historical/context
                if '历史' not in s3_html and '此前' not in s3_html:
                    print(f"WARN: S3 may contain outdated model version '{pattern}' — verify against official latest")
    print("CQ1: Model version check completed")
    
    # CQ2: Earnings data freshness (S4)
    s4_section = re.search(r'<div class="section">.*?<span class="num">4</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s4_section:
        s4_html = s4_section.group(0)
        # Check for Q1 references when Q2 may be available (as of May 2026)
        q1_count = len(re.findall(r'Q1\s+2026', s4_html))
        if q1_count > 0:
            # May 2026 = Q1 earnings season just ended, Q2 not yet available
            # This is acceptable, but flag for verification
            print(f"INFO: S4 contains {q1_count} Q1 2026 references — verify Q2 not yet available")
    print("CQ2: Earnings data freshness check completed")
    
    # CQ3: PR verification placeholder (S8)
    s8_section = re.search(r'<div class="section">.*?<span class="num">8</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s8_section:
        s8_html = s8_section.group(0)
        # Check for PR numbers without links
        pr_no_links = re.findall(r'PR\s+#(\d+)[^<]', s8_html)
        if pr_no_links:
            fatal(f"S8 contains PR numbers without hyperlinks: {pr_no_links} — all PRs must link to github.com")
        # Check for PR links that are not github.com
        non_github_links = re.findall(r'href="(?!https://github\.com)[^"]*pull[^"]*"', s8_html)
        if non_github_links:
            fatal(f"S8 contains non-GitHub PR links: {non_github_links}")
        # Count GitHub PR links
        github_links = re.findall(r'github\.com/(vllm-project|sgl-project)/[^"]+/pull/\d+', s8_html)
        if len(github_links) < 2:
            fatal(f"S8 PR links insufficient: {len(github_links)} found, minimum 2 required")
        print(f"CQ3: S8 GitHub PR links = {len(github_links)} — OK")
    
    # CQ4: Policy source ban (S11)
    s11_section = re.search(r'<div class="section">.*?<span class="num">11</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s11_section:
        s11_html = s11_section.group(0)
        banned_sources = ['ASML 2025年报', 'ASML年报', '设备商财报']
        for bad in banned_sources:
            if bad in s11_html:
                fatal(f"CQ4: S11 contains banned source '{bad}' — policy info must cite government sources")
        print("CQ4: S11 policy sources OK")
    
    # CQ5: Research sample size (S12)
    s12_section = re.search(r'<div class="section">.*?<span class="num">12</span>.*?</div>\s*</div>', html, re.DOTALL)
    if s12_section:
        s12_html = s12_section.group(0)
        # Check for research claims without sample size
        research_patterns = re.findall(r'([\d,]+\s*(?:users|people|respondents|participants))', s12_html)
        if not research_patterns:
            # Check if there are survey claims at all
            survey_claims = re.findall(r'(survey|study|research|poll)', s12_html, re.IGNORECASE)
            if survey_claims:
                print(f"WARN: CQ5: S12 contains {len(survey_claims)} survey references — verify all have sample sizes")
        else:
            print(f"CQ5: S12 sample sizes found: {len(research_patterns)} — OK")
    
    # CQ6: International source ratio (全文)
    # Count domestic sources (Chinese media)
    domestic_patterns = ['36kr', '钛媒体', '品玩', '雷锋网', '第一财经', '财新']
    domestic_count = sum(html.count(p) for p in domestic_patterns)
    # This is a simplified check — full implementation would need NLP analysis
    if domestic_count > 5:
        print(f"WARN: CQ6: {domestic_count} domestic source references found — verify international ratio ≥80%")
    else:
        print("CQ6: International source ratio OK")
    
    print("\n=== ALL CRITICAL CHECKS PASSED ===")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 pre_flight_check.py <report.html>")
        sys.exit(1)
    check(sys.argv[1])