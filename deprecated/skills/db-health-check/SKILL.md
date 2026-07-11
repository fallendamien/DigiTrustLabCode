---
name: db-health-check
description: Run a DB health check and cleanup on Local WP after heavy sessions. Checks table sizes, cleans stale Simply Static records, old Respira snapshots, expired transients, temp files, and error logs.
---

# DB Health Check & Cleanup

## When to Run

- After 3+ Simply Static exports in one session
- When Local WP feels sluggish or hangs
- User says "cleanup", "health check", "optimize", "bloated"
- Before starting a new work session (optional, as prevention)

## Prerequisites

- Local by Flywheel site must be **running**
- **Adminer** accessible via Local → Database → Open Adminer
- **Site Shell** accessible via Local → Site → Open Site Shell
- **PowerShell** access for filesystem cleanup

## Step 1: Diagnostic Query (Adminer)

Open **Local → Database → Open Adminer → SQL command**, paste:

```sql
SELECT table_name, table_rows,
  ROUND(data_length/1024/1024,2) AS data_mb,
  ROUND(index_length/1024/1024,2) AS index_mb,
  ROUND((data_length+index_length)/1024/1024,2) AS total_mb
FROM information_schema.tables
WHERE table_schema='local'
ORDER BY (data_length+index_length) DESC LIMIT 10;
```

### Decision: Clean or Not?

| Table | Threshold | Action |
|-------|-----------|--------|
| `wp_simply_static_pages` | 1000+ rows | TRUNCATE |
| `wp_respira_snapshots` | 100+ rows | Keep last 10 |
| `wp_respira_audit_log` | 200+ rows | Keep last 50 |
| `wp_actionscheduler_actions` | Any `complete` status | Delete completed |
| `wp_actionscheduler_logs` | Any rows | Delete all |

If none exceed thresholds, skip to Step 3 (filesystem cleanup only).

## Step 2: DB Cleanup (Adminer)

Paste this in Adminer SQL command:

```sql
-- 1. Clear stale Simply Static export records
TRUNCATE TABLE wp_simply_static_pages;

-- 2. Keep only last 10 Respira snapshots
DELETE FROM wp_respira_snapshots WHERE id NOT IN (
  SELECT id FROM (SELECT id FROM wp_respira_snapshots ORDER BY id DESC LIMIT 10) AS t
);

-- 3. Keep only last 50 Respira audit log entries
DELETE FROM wp_respira_audit_log WHERE id NOT IN (
  SELECT id FROM (SELECT id FROM wp_respira_audit_log ORDER BY id DESC LIMIT 50) AS t
);

-- 4. Clear completed Action Scheduler tasks
DELETE FROM wp_actionscheduler_actions WHERE status='complete';
DELETE FROM wp_actionscheduler_logs;

-- 5. Delete expired transients
DELETE FROM wp_options WHERE option_name LIKE '_transient_timeout_%' AND option_value < UNIX_TIMESTAMP();
DELETE FROM wp_options WHERE option_name LIKE '_transient_%' AND option_name NOT LIKE '_transient_timeout_%'
  AND option_name NOT IN (
    SELECT REPLACE(option_name, '_transient_timeout_', '_transient_')
    FROM wp_options WHERE option_name LIKE '_transient_timeout_%' AND option_value >= UNIX_TIMESTAMP()
  );

-- 6. Reclaim disk space
OPTIMIZE TABLE wp_options, wp_postmeta, wp_respira_snapshots, wp_respira_audit_log;
```

## Step 3: Filesystem Cleanup (PowerShell)

```powershell
# Simply Static temp files (can be 70+ MB)
Remove-Item "C:\Users\Zamri\Local Sites\digitrust-lab\app\public\wp-content\uploads\simply-static\temp-files\*" -Recurse -Force

# Truncate error logs (only after debugging is done)
Clear-Content "C:\Users\Zamri\Local Sites\digitrust-lab\logs\php\error.log"
Clear-Content "C:\Users\Zamri\Local Sites\digitrust-lab\logs\nginx\error.log"
```

## Step 4: WP CLI Cleanup (Site Shell)

```bash
wp transient delete --all
wp cache flush
```

## Step 5: Verify

```powershell
# Check site is still healthy
try { $r = Invoke-WebRequest -Uri "https://digitrust-lab.local/" -SkipCertificateCheck -TimeoutSec 10 -UseBasicParsing; Write-Host "Homepage: $($r.StatusCode)" } catch { Write-Host "Error: $($_.Exception.Message)" }
```

Expect: `Homepage: 200`

## When NOT to Clean

- **Before a Simply Static export** — `wp_simply_static_pages` is used during export
- **When you need Respira rollback** — old snapshots needed for `respira_restore_snapshot`
- **During active debugging** — error logs may still be needed for diagnosis

## Healthy Baseline

| Table | Rows | Size |
|-------|------|------|
| `wp_options` | ~234 | ~6 MB |
| `wp_simply_static_pages` | 0 | 0 MB |
| `wp_respira_snapshots` | 10 | ~0.1 MB |
| `wp_respira_audit_log` | 50 | ~0.02 MB |
| `wp_postmeta` | ~355 | ~1.4 MB |
| `wp_posts` | ~169 | ~0.27 MB |

**Total DB: ~8 MB** (healthy state)
