---
trigger: model_decision
description: Run DB health check and cleanup after 3+ Simply Static exports, heavy Respira sessions, or when Local WP feels sluggish — cleans stale records, temp files, and logs
---

# DB Health Check Rule

**Priority:** MEDIUM — Activates after 3+ Simply Static exports, when Local WP feels sluggish, or when user says "cleanup", "health check", "optimize", "bloated".

## Core Principle

Local by Flywheel's 2 PHP-FPM workers are easily overwhelmed by DB bloat. After 3+ exports or heavy Respira sessions, run a DB health check and cleanup.

## Key Rules

1. **Check before cleaning** — Run the diagnostic query first to see what's bloated
2. **Use Adminer for SQL** — `wp db query` does NOT work on Local Windows (MySQL socket issue)
3. **Never clean before a Simply Static export** — `wp_simply_static_pages` is used during export
4. **Keep last 10 Respira snapshots** — needed for `respira_restore_snapshot` rollback
5. **Truncate logs after debugging is done** — PHP/Nginx error logs grow fast during debugging
6. **Clean temp files from filesystem** — 70+ MB of temp HTML files accumulate in `simply-static/temp-files/`

## Skill Activation

When this rule triggers, auto-load:

| Skill | Path | Purpose |
|-------|------|---------|
| `db-health-check` | `.devin/skills/db-health-check/SKILL.md` | Full cleanup procedure with SQL, PowerShell, and WP CLI commands |
