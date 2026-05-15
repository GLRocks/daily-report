# GitHub部署配置（2026-05-13生效）

## 仓库信息
- **GitHub Pages地址**: https://glrocks.github.io/daily-report/
- **仓库**: https://github.com/glrocks/daily-report
- **部署分支**: master
- **推送方式**: git push --force

## 每日晨报部署流程（强制）
1. 生成HTML: `/root/.openclaw/workspace/daily_report_YYYY-MM-DD.html`
2. 复制到index.html: `cp daily_report_YYYY-MM-DD.html index.html`
3. git push到GitHub:
   ```bash
   cd /root/.openclaw/workspace
   git remote set-url origin https://TOKEN@github.com/glrocks/daily-report.git
   git add -f index.html daily_report_YYYY-MM-DD.html
   git commit -m "Daily report YYYY-MM-DD"
   git push origin master --force
   ```
4. 向用户推送固定链接: `https://glrocks.github.io/daily-report/`

## 注意
- 不再使用Cloudflare Tunnel临时链接
- GitHub Pages CDN缓存可能需要5-30分钟刷新
- 如需立即验证，访问raw.githubusercontent.com或加?nocache=1参数
- 每日晨报cron jobs.json中输出流程已同步更新

## 生效日期
2026-05-13
