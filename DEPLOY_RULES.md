# DEPLOY_RULES.md — Daily Report Deployment Protocol
# Last updated: 2026-05-14
# Purpose: Prevent the same deployment mistakes from happening again.

## Branch Rule (CRITICAL)
- GitHub Pages is configured to read the `main` branch ONLY.
- NEVER push to `master`. If `master` exists, ignore it.
- Correct command: `git push origin main`

## Template Protection (CRITICAL)
- `agentic_market_daily_template_v12.html` is LOCKED.
- Read-only. Never write, edit, overwrite, or delete.
- Daily reports are generated from this template but saved as separate files.

## Deployment Flow
1. Generate `daily_report_YYYY-MM-DD.html`
2. `cp daily_report_YYYY-MM-DD.html index.html`
3. Append cache-bust comment: `echo "<!-- deploy: $(date +%s) -->" >> index.html`
4. `git add index.html daily_report_YYYY-MM-DD.html`
5. `git commit -m "Daily report YYYY-MM-DD"`
6. `git push origin main`
7. Verify: `curl -s https://glrocks.github.io/daily-report/ | grep INTC`

## Verification Checklist (MUST PASS)
- [ ] INTC price matches ifind data (today: $120.35)
- [ ] Date badge shows correct date
- [ ] Title shows "Agentic Market Daily | YYYY-MM-DD"
- [ ] All 21 stock cards render correctly
- [ ] CDN cache-bust comment present in source

## Past Failures (Do Not Repeat)
- 2026-05-14: Pushed to `master` instead of `main` → user saw stale INTC $24.50
- 2026-05-13: ifind API returned stale INTC $19 → cross-check with Morningstar/Yahoo
- 2026-05-12: Template was accidentally modified during iterative editing

## Data Source Priority
1. ifind realtime API (primary)
2. Morningstar / Yahoo Finance (cross-check for INTC/AMD/QCOM)
3. If discrepancy > 5%, flag and investigate before deploying

## Accountability
- If verification fails, DO NOT deploy.
- Fix first, deploy second.
- User should never see a broken or stale report.
