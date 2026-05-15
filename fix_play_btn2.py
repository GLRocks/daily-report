import re

with open('/root/.openclaw/workspace/index.html', 'r') as f:
    html = f.read()

# Step 1: Add cursor:pointer and active state to play-btn CSS
if '.play-btn {' in html:
    html = html.replace(
        '.play-btn {',
        '.play-btn {\n  cursor: pointer;\n  user-select: none;\n  -webkit-user-select: none;'
    )

# Step 2: Add CSS for active state (click feedback)
if '.play-btn:hover::after {' in html:
    # Add after the hover rule
    html = html.replace(
        '.play-btn:hover::after {',
        '.play-btn:active {\n  transform: scale(0.95);\n  opacity: 0.8;\n}\n.play-btn:hover::after {'
    )

# Step 3: Add JavaScript before </body>
js_code = '''
<script>
// Make play buttons clickable
document.querySelectorAll('.play-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Find the parent quote-box
        var quoteBox = btn.closest('.quote-box');
        if (!quoteBox) {
            alert('原声内容请访问上方来源链接');
            return;
        }
        
        // Try to find a source link in the quote-box
        var sourceLink = quoteBox.querySelector('a[href]');
        if (sourceLink && sourceLink.href && sourceLink.href !== '#' && sourceLink.href !== window.location.href + '#') {
            window.open(sourceLink.href, '_blank');
            return;
        }
        
        // Try to extract source from quote-context text
        var context = quoteBox.querySelector('.quote-context');
        if (context) {
            var text = context.textContent || '';
            // Look for source names and construct search URL
            var sources = ['Motley Fool', 'BBC', 'WSJ', 'Wall Street Journal', 'Bloomberg', 'CNBC', 'Reuters', 'FT', 'NYT'];
            var sourceName = '';
            for (var i = 0; i < sources.length; i++) {
                if (text.indexOf(sources[i]) !== -1) {
                    sourceName = sources[i];
                    break;
                }
            }
            
            var person = '';
            var sourceEl = quoteBox.querySelector('.quote-source');
            if (sourceEl) {
                person = sourceEl.textContent || '';
            }
            
            var quoteText = '';
            var quoteEl = quoteBox.querySelector('.quote-text');
            if (quoteEl) {
                quoteText = quoteEl.textContent || '';
                quoteText = quoteText.substring(0, 80);
            }
            
            if (sourceName && person) {
                var searchQuery = encodeURIComponent(person + ' ' + quoteText + ' ' + sourceName);
                window.open('https://www.google.com/search?q=' + searchQuery, '_blank');
                return;
            }
        }
        
        // Fallback: show tooltip message
        alert('原声内容请访问上方来源链接，或点击来源卡片中的超链接');
    });
});
</script>
'''

if '</body>' in html:
    html = html.replace('</body>', js_code + '</body>')
else:
    # Append at end
    html += js_code

with open('/root/.openclaw/workspace/index.html', 'w') as f:
    f.write(html)

print("Fixed play-btn:")
print("  - Added cursor:pointer CSS")
print("  - Added click event listener")
print("  - Click opens source search or source link")
print(f"  - File size: {len(html)} bytes")
