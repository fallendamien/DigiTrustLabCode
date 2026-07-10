---
description: Deploy static site to Cloudflare Pages with verification
---

# Deploy Static Site

Run the hardened deploy script that uploads to Cloudflare Pages and verifies the live site.

## When to Use

- After completing a Simply Static export
- When you need to push static content changes to production

## Prerequisites

- Simply Static export completed (WP Admin → Simply Static → Generate → wait for "Done!")
- If CSS/template/global settings were changed: Bricks cache cleared first (Regenerate CSS files + Regenerate code signatures in Bricks → Settings)

## Steps

1. **Check if Bricks cache clear is needed:**
   - If only text/links/images changed → skip to step 2
   - If CSS, templates, or `bricks_global_settings` changed → clear cache first:
     - WP Admin → Bricks → Settings → click "Regenerate CSS files"
     - Same page → click "Regenerate code signatures" (accept the dialog)

2. **Ensure Simply Static export is done:**
   - WP Admin → Simply Static → Generate
   - Wait for "Done!" before proceeding

3. **Run the deploy script:**
   ```powershell
   & "D:\Coding Zone\digitrust-lab-static\deploy.ps1"
   ```

4. **Trust the PASS/FAIL output:**
   - ✅ **PASS** (green) — deploy verified, live site has the expected CSS marker
   - ❌ **FAIL** (red) — follow the remediation steps printed by the script:
     1. Clear Bricks cache (Regenerate CSS files + Regenerate code signatures)
     2. Re-run Simply Static export
     3. Re-run `deploy.ps1`
   - If FAIL persists after cache clear → re-save `bricks_global_settings` option via Respira MCP (`respira_update_option`), then repeat from step 1

## What the Script Does

- Hardcodes the static directory (`D:\Coding Zone\digitrust-lab-static`) — runs from anywhere
- Pre-deploy freshness guard — warns if newest static file is older than 10 minutes
- Deploys via `npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main`
- Post-deploy verification — fetches `https://www.digitrustlab.com/privasi/` and checks for CSS marker `overflow-x: clip`
- Prints green PASS or red FAIL with remediation instructions

## Configurable Marker

The expected CSS marker is in `deploy.ps1` line 10:
```powershell
$ExpectedMarker = "overflow-x: clip"
```
Update this when the CSS changes. Must match the exact string Bricks renders (note the space after the colon).

## Constraints

- Script only deploys + verifies — never modifies CSS or HTML content
- No post-processing scripts, no template edits
- Fully compliant with AGENTS.md Bricks-only policy
