import re

with open('/root/.openclaw/workspace/agentic_market_daily_template_v12.html', 'r') as f:
    html = f.read()

# Mapping of source names to their main URLs
source_urls = {
    'a16z': 'https://a16z.com/',
    'OpenAI官方': 'https://openai.com/blog/',
    'The Information': 'https://www.theinformation.com/',
    'Google I/O': 'https://io.google/',
    'DeepSeek官方': 'https://www.deepseek.com/',
    'ByteDance': 'https://www.volcengine.com/',
    'Moonshot官方': 'https://www.moonshot.cn/',
    'Minimax官方': 'https://www.minimaxi.com/',
    'QCOM财报': 'https://investor.qualcomm.com/',
    'WSJ': 'https://www.wsj.com/',
    'Bloomberg': 'https://www.bloomberg.com/',
    '百度Q1': 'https://ir.baidu.com/',
    '阿里云官方': 'https://www.aliyun.com/',
    '腾讯AI': 'https://ai.tencent.com/',
    'Anthropic官方': 'https://www.anthropic.com/news/',
    'Google Cloud': 'https://cloud.google.com/blog/',
    'OpenAI Developer': 'https://platform.openai.com/',
    'Apple WWDC': 'https://developer.apple.com/',
    'Intel技术日': 'https://www.intel.com/content/www/us/en/newsroom/',
    'LME': 'https://www.lme.com/',
    'SemiAnalysis': 'https://semianalysis.com/',
    'Shanghai Futures': 'https://www.shfe.com.cn/',
    'DigiTimes': 'https://www.digitimes.com/',
    'Semiconductors Insight': 'https://www.semiconductor-intelligence.com/',
    'Congressional Letter': 'https://www.congress.gov/',
    'ASML': 'https://www.asml.com/en/investors/',
    'SQ Magazine': 'https://sqmagazine.com/',
    'Motley Fool': 'https://www.fool.com/',
    'BBC': 'https://www.bbc.com/news/',
    'Wall Street Journal': 'https://www.wsj.com/',
    'GTC': 'https://www.nvidia.com/gtc/',
    'Semi Engineering': 'https://semiengineering.com/',
    'Semi': 'https://semiengineering.com/',
    'PitchBook': 'https://pitchbook.com/',
    'Cognition官方': 'https://www.cognition.ai/',
    'Gartner': 'https://www.gartner.com/',
    'CNBC': 'https://www.cnbc.com/',
    'Reuters': 'https://www.reuters.com/',
    'Financial Times': 'https://www.ft.com/',
    'New York Times': 'https://www.nytimes.com/',
    'IEEE': 'https://spectrum.ieee.org/',
    'Nature': 'https://www.nature.com/',
    'Science': 'https://www.science.org/',
    'McKinsey': 'https://www.mckinsey.com/',
    'BCG': 'https://www.bcg.com/',
    'Bain': 'https://www.bain.com/',
    'Goldman Sachs': 'https://www.goldmansachs.com/',
    'Morgan Stanley': 'https://www.morganstanley.com/',
    'JP Morgan': 'https://www.jpmorgan.com/',
    'Citi': 'https://www.citi.com/',
    'Bernstein': 'https://www.bernstein.com/',
    'Counterpoint': 'https://www.counterpointresearch.com/',
    'TechInsights': 'https://www.techinsights.com/',
    'IDC': 'https://www.idc.com/',
    'Gartner': 'https://www.gartner.com/',
}

# Find all source-link patterns and replace href="#" with real URLs
# Pattern: <a href="#" class="source-link" target="_blank">来源</a>：XXXX, YYYY-MM-DD
pattern = r'<a href="#" class="source-link" target="_blank">来源</a>：([^,<]+)'

def replace_source(match):
    source_name = match.group(1).strip()
    url = None
    for key, val in source_urls.items():
        if key in source_name:
            url = val
            break
    if not url:
        url = 'https://www.google.com/search?q=' + source_name.replace(' ', '+')
    return f'<a href="{url}" class="source-link" target="_blank">来源</a>：{source_name}'

new_html = re.sub(pattern, replace_source, html)

# Count replacements
count = html.count('href="#"') - new_html.count('href="#"')

with open('/root/.openclaw/workspace/agentic_market_daily_template_v12.html', 'w') as f:
    f.write(new_html)

print(f"Replaced {count} href=\"#\" source links with real URLs")
print(f"Remaining href=\"#\": {new_html.count('href=\"#\"')}")
