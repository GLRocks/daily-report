#!/bin/bash
# Quick verify script

cd /root/.openclaw/workspace

echo "=== Structure Check ==="
grep -c 'class="section-title"' daily_report_2026-05-14_complete.html
grep -c 'class="stock-card"' daily_report_2026-05-14_complete.html
grep -c 'class="rec-badge"' daily_report_2026-05-14_complete.html
grep -c 'class="cat-badge"' daily_report_2026-05-14_complete.html

echo "=== Stock Prices ==="
grep -A2 'class="ticker">INTC' daily_report_2026-05-14_complete.html | grep -E 'price|change'

echo "=== Deploy ==="
cp daily_report_2026-05-14_complete.html index.html
echo '<!-- deploy: 2026-05-14 11:40 CST | complete v12 | all content injected -->' >> index.html
git add -f index.html daily_report_2026-05-14_complete.html
git commit -m 'Deploy complete: V12 template + all 21 stocks + all 13 sections'
git push origin main

echo "=== Verify Online ==="
sleep 15
curl -s https://glrocks.github.io/daily-report/ | grep -c 'stock-card\|section-title\|rec-badge'
curl -s https://glrocks.github.io/daily-report/ | grep -A2 'ticker.*INTC' | grep -E 'price|change'
