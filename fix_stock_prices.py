import re

# 读取文件
with open('index.html', 'r') as f:
    content = f.read()

# 定义修复规则: (ticker, old_price_text, new_price_text, old_change_text, new_change_text, new_change_class)
# new_change_class: None=不改变class, 'up'/'down'=改变class
# 注意old_change_text要和HTML中完全匹配（包括+/−符号）

fixes = [
    # Panel stocks
    ('NVDA', '$225.83', '$225.83', '+2.91%', '+2.29%', None),
    ('AMD', '$445.23', '$440.50', '2.96%', '1.74%', 'down'),
    ('QCOM', '$213.35', '$213.17', '10.18%', '+1.36%', 'up'),
    ('TSM', '$399.78', '$399.80', '1.18%', '+0.63%', 'up'),
    ('AVGO', '$416.79', '$416.79', '2.72%', '0.60%', 'down'),
    ('MU', '$802.72', '$803.63', '+0.93%', '+4.83%', None),
    ('AMAT', '$431.20', '$436.61', '2.80%', '+1.25%', 'up'),
    ('LRCX', '$295.44', '$295.44', '0.21%', '+2.86%', 'up'),
    ('ASML', '$1,520.94', '$1,581.58', '+3.62%', '+3.99%', None),
    ('INTC', '$120.35', '$120.29', '7.03%', '0.27%', 'down'),
    ('GOOGL', '$387.47', '$402.62', '0.30%', '+3.94%', 'up'),
    ('MSFT', '$405.15', '$405.21', '1.82%', '0.63%', 'down'),
    ('META', '$616.63', '$616.63', '+2.97%', '+2.26%', None),
    ('AAPL', '$299.23', '$298.87', '+2.24%', '+1.38%', None),
    ('PLTR', '$136.00', '$130.05', '0.65%', '4.37%', 'down'),
    ('SNOW', '$151.98', '$152.37', '+0.32%', '+0.26%', None),
    ('BABA', '$145.69', '$145.81', '+6.11%', '+8.18%', None),
    ('TSLA', '$445.21', '$445.27', '+0.05%', '+2.73%', None),
    ('CEG', '$274.91', '$274.89', '8.27%', '6.37%', 'down'),
    ('CCJ', '$115.39', '$115.39', '3.95%', '1.32%', 'down'),
    ('OKLO', '$8.50', '$69.66', '5.2%', '5.39%', 'down'),
]

for ticker, old_p, new_p, old_c, new_c, new_cls in fixes:
    # 构建正则模式来定位该ticker的股票卡片
    # 模式: <div class="ticker">TICKER</div> ... <span class="price">OLD_PRICE</span> ... <span class="change CLASS">OLD_CHANGE</span>
    pattern = (
        r'(<div class="ticker">' + re.escape(ticker) + r'</div>'
        r'[\s\S]*?)'
        r'(<span class="price">)' + re.escape(old_p) + r'(</span>)'
        r'([\s\S]*?)'
        r'(<span class="change) (up|down)(">)' + re.escape(old_c) + r'(</span>)'
    )
    
    def repl(m):
        cls = new_cls if new_cls else m.group(6)
        return (
            m.group(1) +
            m.group(2) + new_p + m.group(3) +
            m.group(4) +
            m.group(5) + ' ' + cls + m.group(7) + new_c + m.group(8)
        )
    
    new_content, count = re.subn(pattern, repl, content)
    if count == 0:
        print(f"WARNING: {ticker} panel fix failed (pattern not matched)")
    else:
        print(f"FIXED panel: {ticker} {old_p}/{old_c} -> {new_p}/{new_c} (cls={new_cls or 'same'})")
    content = new_content

# 修复Section 4表格
table_fixes = [
    ('NVIDIA', '$220.86', '$225.83', '+0.65%', '+2.29%'),
    ('AMD', '$448.36', '$440.50', '-2.27%', '-1.74%'),
    ('Intel', '$24.50', '$120.29', '+3.20%', '-0.27%'),
    ('Qualcomm', '$210.31', '$213.17', '-11.46%', '+1.36%'),
    ('Broadcom', '$419.50', '$416.79', '-2.08%', '-0.60%'),
]

for name, old_p, new_p, old_c, new_c in table_fixes:
    # 表格行模式: <tr><td>NAME</td><td>OLD_PRICE</td><td>OLD_CHANGE</td>...
    pattern = (
        r'(<tr><td>)' + re.escape(name) + r'(</td><td>)' +
        re.escape(old_p) + r'(</td><td>)' + re.escape(old_c) + r'(</td>)'
    )
    repl = r'\1' + name + r'\2' + new_p + r'\3' + new_c + r'\4'
    new_content, count = re.subn(pattern, repl, content)
    if count == 0:
        print(f"WARNING: {name} table fix failed")
    else:
        print(f"FIXED table: {name} {old_p}/{old_c} -> {new_p}/{new_c}")
    content = new_content

with open('index.html', 'w') as f:
    f.write(content)

print("\nAll fixes applied. File saved.")
