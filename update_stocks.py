import re

with open('/root/.openclaw/workspace/index.html', 'r') as f:
    html = f.read()

# Stock data from today's ifind API
stocks = {
    'NVDA': {'price': '225.83', 'change': '+2.91%', 'up': True},
    'AMD': {'price': '445.23', 'change': '-2.96%', 'up': False},
    'QCOM': {'price': '213.35', 'change': '-10.18%', 'up': False},
    'TSM': {'price': '399.78', 'change': '-1.18%', 'up': False},
    'AVGO': {'price': '416.79', 'change': '-2.72%', 'up': False},
    'MU': {'price': '802.72', 'change': '+0.93%', 'up': True},
    'AMAT': {'price': '431.20', 'change': '-2.80%', 'up': False},
    'LRCX': {'price': '295.44', 'change': '-0.21%', 'up': False},
    'ASML': {'price': '402.73', 'change': '+3.62%', 'up': True},
    'INTC': {'price': '120.35', 'change': '-7.03%', 'up': False},
    'GOOGL': {'price': '387.47', 'change': '-0.30%', 'up': False},
    'MSFT': {'price': '405.15', 'change': '-1.82%', 'up': False},
    'META': {'price': '616.63', 'change': '+2.97%', 'up': True},
    'AAPL': {'price': '299.23', 'change': '+2.24%', 'up': True},
    'PLTR': {'price': '136.00', 'change': '-0.65%', 'up': False},
    'SNOW': {'price': '151.98', 'change': '+0.32%', 'up': True},
    'BABA': {'price': '145.69', 'change': '+6.11%', 'up': True},
    'TSLA': {'price': '445.21', 'change': '+0.05%', 'up': True},
    'CEG': {'price': '274.91', 'change': '-8.27%', 'up': False},
    'CCJ': {'price': '115.39', 'change': '-3.95%', 'up': False},
    'OKLO': {'price': '8.50', 'change': '-5.2%', 'up': False},
}

# Replace each stock's price and change
for ticker, data in stocks.items():
    # Find the stock card for this ticker
    pattern = rf'(<div class="ticker">{ticker}</div>.*?<span class="price">)\$[\d.]+(</span>.*?<span class="change )(?:up|down)(">)[\d.+%\s▲▼+-]*(<\/span>)'
    
    direction = 'up' if data['up'] else 'down'
    sign = '+' if data['up'] else ''
    change_val = data['change'].lstrip('+-')
    
    replacement = rf'\1${data["price"]}\2{direction}\3{sign}{change_val}\4'
    
    html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)
    if count > 0:
        print(f"Updated {ticker}: ${data['price']} {data['change']}")
    else:
        print(f"WARNING: Could not find {ticker}")

with open('/root/.openclaw/workspace/index.html', 'w') as f:
    f.write(html)

print(f"\nSaved: {len(html)} bytes")
