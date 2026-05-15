import re

with open('/root/.openclaw/workspace/index.html', 'r') as f:
    html = f.read()

# Step 1: Update CSS
old_css = """.signal-list li {
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

new_css = """.signal-list li {
  display: grid;
  grid-template-columns: auto auto 1fr auto;
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
.signal-list li .signal-title {
  white-space: nowrap;
  font-weight: bold;
  color: var(--text);
  align-self: start;
  margin-top: 2px;
}
.signal-list li .signal-desc {
  line-height: 1.6;
  color: var(--text);
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

html = html.replace(old_css, new_css)

# Step 2: Restructure each signal-list li
# Pattern: <li><span class="tag ...">...</span><div class="signal-body"><strong>TITLE</strong>：DESC</div><div class="signal-source">...</div></li>

def split_body(match):
    full = match.group(0)
    # Extract tag
    tag_match = re.search(r'<span class="tag[^"]*"[^>]*>[^<]*</span>', full)
    tag = tag_match.group(0) if tag_match else ''
    
    # Extract source
    source_match = re.search(r'<div class="signal-source">.*?</div>', full, re.DOTALL)
    source = source_match.group(0) if source_match else ''
    
    # Extract body content
    body_match = re.search(r'<div class="signal-body">(.*?)</div>', full, re.DOTALL)
    if not body_match:
        return full
    
    body_content = body_match.group(1)
    
    # Split title (strong) and desc
    # Pattern: <strong>TITLE</strong>：DESC
    title_match = re.match(r'(<strong>.*?</strong>)[：:](.*)', body_content.strip(), re.DOTALL)
    if title_match:
        title = title_match.group(1)
        desc = title_match.group(2).strip()
        # Remove <strong> tags, keep text
        title_text = re.sub(r'</?strong>', '', title)
        return f'<li>{tag}<div class="signal-title">{title_text}</div><div class="signal-desc">{desc}</div>{source}</li>'
    else:
        # No strong separator, keep as desc
        return f'<li>{tag}<div class="signal-title"></div><div class="signal-desc">{body_content}</div>{source}</li>'

new_html = re.sub(
    r'<li><span class="tag[^"]*"[^>]*>[^<]*</span><div class="signal-body">.*?</div><div class="signal-source">.*?</div></li>',
    split_body,
    html,
    flags=re.DOTALL
)

with open('/root/.openclaw/workspace/index.html', 'w') as f:
    f.write(new_html)

print(f"Converted signal-list to 4-column layout")
print(f"Original size: {len(html)}, New size: {len(new_html)}")

# Verify
result = subprocess.run(['grep', '-c', 'signal-title', '/root/.openclaw/workspace/index.html'], 
                       capture_output=True, text=True)
print(f"signal-title count: {result.stdout.strip()}")
