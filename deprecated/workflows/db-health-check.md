---
description: Run a DB health check and cleanup on Local WP — checks table sizes, cleans stale records, temp files, and logs
---

# DB Health Check & Cleanup

Run this after 3+ Simply Static exports, when Local WP feels sluggish, or when user requests cleanup/optimization.

## Steps

1. **Check DB table sizes** — Open Adminer (Local → Database → Open Adminer → SQL command), run the diagnostic query from `.devin/skills/db-health-check/SKILL.md`
2. **If bloated** — Run the cleanup SQL (TRUNCATE `wp_simply_static_pages`, keep last 10 Respira snapshots, keep last 50 audit logs, delete completed Action Scheduler tasks, delete expired transients, OPTIMIZE TABLE)
3. **Clean filesystem** — Delete Simply Static temp files (`simply-static/temp-files/*`), truncate PHP and Nginx error logs
4. **WP CLI cleanup** — In Site Shell: `wp transient delete --all` + `wp cache flush`
5. **Verify** — Check site responds with HTTP 200

## When NOT to run

- Before a Simply Static export (table is used during export)
- When you need Respira rollback snapshots
- During active debugging (logs still needed)

## Full procedure

See `.devin/skills/db-health-check/SKILL.md` for complete SQL and PowerShell commands.
