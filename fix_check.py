#!/usr/bin/env python3
with open('/root/.openclaw/workspace/pre_flight_check.py', 'r') as f:
    content = f.read()

old = r"pr_links = re.findall(r'github\.com/(vllm-project|sgl-project)/[^""]+/pull/\d+', s9_html)"
new = r"pr_links = re.findall(r'github\.com/(vllm-project|sgl-project)/[^""]+/pull/?\d*', s9_html)"

if old in content:
    content = content.replace(old, new)
    with open('/root/.openclaw/workspace/pre_flight_check.py', 'w') as f:
        f.write(content)
    print('Updated pre_flight_check.py')
else:
    print('Pattern not found, trying alternate')
    # Show context
    import re
    matches = re.findall(r'github\.com/\(vllm-project\|sgl-project\)/[^\']+', content)
    print('Found:', matches[:3])
