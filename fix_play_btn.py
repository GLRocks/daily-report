import re

with open('/root/.openclaw/workspace/index.html', 'r') as f:
    html = f.read()

# Check if there's already a </body> tag to insert JS before
if '</body>' in html:
    # Add JavaScript to make play-btn clickable
    js_code = '''
<script>
// Play button click handler
document.querySelectorAll('.play-btn').forEach(function(btn) {
    btn.style.cursor = 'pointer';
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        // Find the closest quote-box and look for a source link
        var quoteBox = btn.closest('.quote-box');
        if (quoteBox) {
            var sourceLink = quoteBox.querySelector('.source-link, a[href^="http"]');
            if (sourceLink && sourceLink.href) {
                window.open(sourceLink.href, '_blank');
                return;
            }
        }
        // Fallback: show tooltip or alert
        alert('原声内容请访问上方来源链接');
    });
});
</script>
'''
    
    # Insert before </body>
    html = html.replace('</body>', js_code + '</body>')
    
    print("Added JavaScript for play-btn click handling")

# Also convert play-btn div to button or span with cursor pointer for better UX
html = html.replace('<div class="play-btn"', '<span class="play-btn"')
html = html.replace('</div>\n    </div>\n    <div class="quote-box">', '</span>\n    </div>\n    <div class="quote-box">')
# Fix closing tags
html = html.replace('</span>\n      </div>\n      <div class="quote-source">', '</span>\n      </div>\n      <div class="quote-source">')

# Add CSS to make play-btn look clickable
if '</style>' in html:
    css_addition = '''
.play-btn {
  cursor: pointer;
  user-select: none;
}
.play-btn:active {
  transform: scale(0.95);
}
'''
    html = html.replace('</style>', css_addition + '</style>')

with open('/root/.openclaw/workspace/index.html', 'w') as f:
    f.write(html)

print("Fixed play-btn click handling")
print(f"File size: {len(html)} bytes")
