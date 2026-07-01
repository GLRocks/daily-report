#!/usr/bin/env python3
"""
generate_notify.py — Generate ≤300 char notification for daily report
Reads today_judgment.txt and generates a fixed-format message.
Hard-truncates to 300 characters to ensure delivery.
"""
import sys
import os
import datetime

def generate():
    judgment = "已部署，详见链接"
    if os.path.exists('/root/.openclaw/workspace/today_judgment.txt'):
        with open('/root/.openclaw/workspace/today_judgment.txt', 'r') as f:
            judgment = f.read().strip()
    if not judgment:
        judgment = "已部署，详见链接"
    
    # Truncate judgment to 150 chars to keep total under 300
    if len(judgment) > 150:
        judgment = judgment[:147] + "..."
    
    date_str = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    msg = f"Agentic Market Daily | {date_str} 已部署完成 ✅\n\n核心判断：{judgment}\n\n固定链接：https://glrocks.github.io/daily-report/"
    
    # Hard truncate to 300 characters
    if len(msg) > 300:
        msg = msg[:297] + "..."
    
    print(msg)
    return msg

if __name__ == '__main__':
    generate()
