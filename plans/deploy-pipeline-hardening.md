# Deploy Pipeline Hardening

> ⚠️ **DEPRECATED (2026-07-12):** The Simply Static → Wrangler → Cloudflare Pages pipeline was decommissioned when the site migrated to Hostinger WordPress with LiteSpeed Cache + Cloudflare proxy. This plan is kept for historical reference only — the current workflow is: write/publish in WordPress → purge LiteSpeed Cache → verify live.

## Goal
Stop stale-CSS deploys from recurring by eliminating the 3 silent failure points in the Simply Static → Wrangler pipeline: wrong directory, skipped export, and no verification.

## Background (root cause)
The recurring "fixed on local, broken on live" bug is **usually** caused by one of three silent failures in the Simply Static → Wrangler pipeline: wrong directory, skipped export, and no verification. However, Bricks can also cache the inline CSS block (`bricks-frontend-inline-inline-css`), causing Simply Static to crawl a stale version even when the change is live on WordPress. When `deploy.ps1` verification FAILs despite a fresh export, clearing Bricks cache (Regenerate CSS files + Regenerate code signatures in Bricks → Settings) and re-exporting is the correct recovery path.

`bricks_global_settings` edits USUALLY export fresh (the option is read at render time). But "usually" is not "always" — confirmed on 2026-07-09 when `overflow-x: clip` was live on local WP but missing from the export until Bricks cache was cleared. The deploy script's FAIL message includes the full cache-clear recovery sequence.

## Tasks

- [ ] Task 1: Create `deploy.ps1` in `D:\Coding Zone\digitrust-lab-static` with the absolute path hardcoded via `Set-Location`, so it can never run from the wrong directory → Verify: run `.\deploy.ps1` from `C:\Users\Zamri`; it still deploys from the static folder, no EBUSY.

- [ ] Task 2: In `deploy.ps1`, after the wrangler deploy, add a 15s wait then fetch `https://www.digitrustlab.com/privasi/` and assert the response contains `overflow-x: clip` (a marker only present in the post-fix CSS). Print green PASS or red FAIL with remediation text → Verify: deploy after a known-good export prints PASS.

- [ ] Task 3: Make the marker check configurable — store the expected marker string near the top of the script (`$expectedMarker = "overflow-x: clip"`) so future CSS changes can update it → Verify: changing the marker to a nonsense string makes the script print FAIL.

- [ ] Task 4: Add a pre-deploy freshness guard — before deploying, compare the newest file mtime in `D:\Coding Zone\digitrust-lab-static` against the current time. If the newest file is older than 10 minutes, print a yellow warning: "Static export may be stale — did you run Simply Static?" and prompt Y/N to continue → Verify: run without a fresh export; warning appears.

- [ ] Task 5: (Optional, only if WP-CLI is available in Local WP) Add a `regenerate.ps1` that triggers Simply Static export via WP-CLI (`wp simply-static run`) so export + deploy can be chained. If WP-CLI is not available, skip this task and leave export as the manual GUI step → Verify: `wp --info` runs inside the Local site shell; if it errors, skip.

- [ ] Task 6: Document the new workflow in `TROUBLESHOOTING.md` under a new "Deploy Pipeline (correct workflow)" section: (1) run Simply Static export, (2) run `.\deploy.ps1`, (3) trust the PASS/FAIL output → Verify: section exists and references `deploy.ps1`.

## Done When
- [ ] `.\deploy.ps1` deploys correctly from any working directory
- [ ] The script prints a clear PASS/FAIL based on the actual live site, not assumptions
- [ ] A stale static folder triggers a warning before deploy
- [ ] Workflow is documented in TROUBLESHOOTING.md

## Notes

**Hard rules / constraints (do not violate):**
- Wrangler CLI is ALLOWED for deploy. PowerShell CSS injection / post-process scripts remain BANNED — this script only *deploys and verifies*, it never modifies CSS or static HTML content.
- Do NOT touch templates 185 (Header) or 52 (Blog Archive) — frozen.
- All styling stays in Bricks GUI / Respira MCP. This script is deploy-automation only.

**Reference values:**
- Static output folder: `D:\Coding Zone\digitrust-lab-static`
- Wrangler command: `npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main`
- Simply Static generate URL: `https://digitrust-lab.local/wp-admin/admin.php?page=simply-static-generate`
- Live verify URL: `https://www.digitrustlab.com/privasi/`
- Post-fix CSS marker: `overflow-x: clip` (present in `bricks-frontend-inline-inline-css` inline block on every page after the 2026-07-09 overflow fix)

**Why the marker approach works:** since custom CSS is inline on every page, the live HTML itself is the source of truth. If the marker string is missing from the fetched HTML, the deploy shipped stale content — no false positives.

**Known stale copy (informational, not a task):** there is a separate `wp-custom-css` inline block (WordPress Customizer "Additional CSS") that does NOT carry the fix on either local or live. It's harmless because the Bricks inline block wins the cascade. Devin should NOT try to "fix" it unless a future issue traces to it.
