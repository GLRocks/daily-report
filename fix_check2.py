#!/usr/bin/env python3
with open('/root/.openclaw/workspace/pre_flight_check.py', 'r') as f:
    content = f.read()

old = '        pr_links = re.findall(r\'github\\.com/(vllm-project|sgl-project)/[^"]+/pull/\\d+\', s9_html)'
new = '        pr_links = re.findall(r\'github\\.com/(vllm-project|sgl-project)/[^"]+/pull/?\\d*\', s9_html)'

if old in content:
    content = content.replace(old, new)
    with open('/root/.openclaw/workspace/pre_flight_check.py', 'w') as f:
        f.write(content)
    print('Updated pre_flight_check.py - first pattern')
else:
    print('First pattern not found')

# Also update the CQ3 section
old2 = '        github_links = re.findall(r\'github\\.com/(vllm-project|sgl-project)/[^"]+/pull/\\d+\', s9_html)'
new2 = '        github_links = re.findall(r\'github\\.com/(vllm-project|sgl-project)/[^"]+/pull/?\\d*\', s9_html)'

if old2 in content:
    content = content.replace(old2, new2)
    with open('/root/.openclaw/workspace/pre_flight_check.py', 'w') as f:
        f.write(content)
    print('Updated pre_flight_check.py - second pattern')
else:
    print('Second pattern not found')
