import re

with open('/root/.openclaw/workspace/index.html', 'r') as f:
    html = f.read()

# Step 1: Update CSS for signal-list
old_signal_css = """/* Signal List */
.signal-list { list-style:none; }
.signal-list li {
  padding:10px 0; border-bottom:1px solid var(--border); display:flex; gap:12px; align-items:flex-start;
}
.signal-list li:last-child { border-bottom:none; }"""

new_signal_css = """/* Signal List */
.signal-list { list-style:none; }
.signal-list li {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 12px;
  align-items: start;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
}
.signal-list li:last-child { border-bottom:none; }
.signal-list li .tag {
  align-self: start;
  margin-top: 2px;
  white-space: nowrap;
}
.signal-list li .signal-body {
  line-height: 1.6;
}
.signal-list li .signal-body strong {
  white-space: nowrap;
}
.signal-list li .signal-source {
  align-self: start;
  text-align: right;
  white-space: nowrap;
  font-size: 0.85em;
  color: var(--text2);
  margin-top: 2px;
}
.signal-list li .signal-source a {
  color: var(--accent);
}"""

html = html.replace(old_signal_css, new_signal_css)

# Step 2: Restructure signal-list li items
# Pattern: <li><span class="tag ...">...</span> <strong>...</strong>：...<em><a>来源</a>：...</em></li>

def restructure_li(match):
    full = match.group(0)
    
    # Extract tag
    tag_match = re.search(r'<span class="tag[^"]*"[^>]*>[^<]*</span>', full)
    tag = tag_match.group(0) if tag_match else ''
    
    # Extract source (em with a + text)
    source_match = re.search(r'<em>.*?</em>', full)
    source = source_match.group(0) if source_match else ''
    
    # Remove tag, source, and li tags to get body
    body = full
    body = re.sub(r'<li[^>]*>', '', body)
    body = re.sub(r'</li>', '', body)
    if tag:
        body = body.replace(tag, '', 1)
    if source:
        body = body.replace(source, '', 1)
    body = body.strip()
    # Remove leading space/： that might be left
    body = re.sub(r'^[\s：]+', '', body)
    
    return f'<li>{tag}<div class="signal-body">{body}</div><div class="signal-source">{source}</div></li>'

# Find all signal-list items
new_html = re.sub(
    r'<li><span class="tag[^"]*"[^>]*>[^<]*</span>.*?</li>',
    restructure_li,
    html,
    flags=re.DOTALL
)

with open('/root/.openclaw/workspace/index.html', 'w') as f:
    f.write(new_html)

print(f"Restructured signal-list items")
print(f"Original size: {len(html)}, New size: {len(new_html)}")

# Verify
import subprocess
result = subprocess.run(['grep', '-c', 'signal-body', '/root/.openclaw/workspace/index.html'], 
                       capture_output=True, text=True)
print(f"signal-body count: {result.stdout.strip()}")
