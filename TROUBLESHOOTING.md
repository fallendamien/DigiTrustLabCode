# DigiTrust Lab — Troubleshooting

> Project-specific issues and solutions. Not a development project — no global lessons needed.
>
> ⚠️ **POLICY UPDATE (2026-07-06):** Wrangler CLI is **ALLOWED** for Cloudflare Pages deployment only (per AGENTS.md). Post-process scripts and PowerShell CSS injection remain **BANNED** — all styling via Bricks GUI or Respira MCP. Historical entries below may reference banned tools, but those approaches must NOT be used.
>
> **Old Bricks MCP is DECOMMISSIONED (2026-07-05).** Use Respira MCP only. The bridge script entries below are kept for historical reference but are no longer relevant.

---

## Simply Static `/blog/` Prefix Issue

**Date:** 2026-06-29  
**Severity:** High (all internal links broken on live site)

### Problem

Simply Static was configured with "Relative Path" set to `/blog`, which prepended `/blog/` to all internal links in the exported static HTML. Since the site is served at the root of `blog.digitrustlab.com`, all links like `/blog/privasi`, `/blog/disclaimer`, `/blog/hubungi` resulted in 404 errors.

### Root Cause

Simply Static → Settings → General → "Relative Path" field was set to `/blog` instead of `/`. This was likely a leftover from initial setup when the blog was planned to live under a `/blog/` subdirectory.

### Fix

1. **Simply Static config:** Changed Relative Path from `/blog` to `/` in WP Admin → Simply Static → Settings → General
2. **Existing static files:** Ran PowerShell to replace all `/blog/` with `/` across 12 `index.html` files:
   ```powershell
   $files = Get-ChildItem -Recurse -Filter "index.html" -Path "D:\Coding Zone\digitrust-lab-static"
   foreach ($file in $files) {
       $content = [System.IO.File]::ReadAllText($file.FullName)
       if ($content.Contains('/blog/')) {
           $content = $content.Replace('/blog/', '/')
           [System.IO.File]::WriteAllText($file.FullName, $content)
       }
   }
   ```
3. **Deployed via Wrangler:** `npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main`

### Prevention

Future Simply Static exports will now use `/` as the base path. No manual post-export fixes needed.

---

## Missing Static Pages (privasi, hubungi)

**Date:** 2026-06-29  
**Severity:** Medium (2 of 4 core pages missing from export)

### Problem

Simply Static's Enhanced Crawl did not pick up the `privasi` and `hubungi` pages despite them being published in WordPress. The `tentang` and `disclaimer` pages exported fine.

### Root Cause

Unknown — likely the Simply Static crawler didn't follow internal links to these pages. The footer links pointed to `/blog/privasi` (wrong path) which may have caused the crawler to miss them.

### Fix

Manually fetched HTML from WordPress and saved to static directory:
```powershell
$privasi = Invoke-WebRequest -Uri "https://digitrust-lab.local/privasi/" -UseBasicParsing
$privasi.Content -replace 'https://digitrust-lab\.local/', '/' | Out-File -FilePath "privasi\index.html" -Encoding utf8
```

### Prevention

- After each Simply Static export, verify all core pages exist in the static output
- Check: `Get-ChildItem -Recurse -Filter "index.html" | Where-Object { $_.DirectoryName -match "privasi|hubungi|tentang|disclaimer" }`

---

## Cloudflare Pages Git Disconnect

**Date:** 2026-06-29  
**Severity:** High (auto-deploy broken)

### Problem

Cloudflare Pages project `digitrust-lab-static` was disconnected from GitHub. Pushing to `main` did not trigger auto-deploys. The live site showed stale content.

### Root Cause

GitHub integration in Cloudflare Pages was disconnected (possibly during project settings change or token expiry).

### Fix

Deployed directly using Wrangler CLI, bypassing Git integration:
```powershell
cd "D:\Coding Zone\digitrust-lab-static"
npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main
```

### Prevention

- Use `wrangler pages deploy` or Cloudflare dashboard for deployment

---

## Footer Floating in Middle of Page

**Date:** 2026-06-29  
**Severity:** Low (cosmetic)

### Problem

On pages with short content (e.g., homepage with only 1 post), the footer floated in the middle of the viewport instead of sticking to the bottom.

### Root Cause

No `min-height` on `body` element. The body only grew as tall as its content, leaving empty space below the footer.

### Fix

Added CSS to Bricks Settings → Custom Code → Custom CSS:
```css
html, body { min-height: 100vh; }
body { display: flex; flex-direction: column; }
footer { margin-top: auto; }
```

Also patched existing static files with the same CSS.

### Prevention

Future exports will include this CSS automatically since it's saved in Bricks global settings.

---

## PowerShell Command Hanging (Select-String with Escaped Quotes)

**Date:** 2026-06-29  
**Severity:** Low (workflow annoyance)

### Problem

The following PowerShell command hung indefinitely:
```powershell
Select-String -Path "file.html" -Pattern "href=\"/" | Select-Object -First 10
```

### Root Cause

PowerShell interprets `\"` differently from other shells. The escaped double quote inside a double-quoted string creates an invalid regex pattern, causing the command to hang or produce unexpected results.

### Fix

Use single quotes for the pattern, or use `-SimpleMatch` switch:
```powershell
# Option 1: Single quotes
Select-String -Path "file.html" -Pattern 'href="/' | Select-Object -First 10

# Option 2: SimpleMatch (no regex)
Select-String -Path "file.html" -Pattern 'href="/' -SimpleMatch | Select-Object -First 10
```

### Prevention

Always use single quotes for regex patterns in PowerShell `Select-String` commands.

---

## Bricks Header Template Not Rendering (Static Export)

**Date:** 2026-06-30  
**Severity:** High (missing site navigation)

### Problem

The Bricks Builder header template (ID 21) was configured correctly:
- Post status: `publish`
- Template type: `header`
- Template condition: `main: "any"` (Entire website)
- Template content existed in `_bricks_page_content_2`

But the header was completely missing from all static exported pages — body went straight from `<body>` to skip-links to `<article>` with no `<header>` element.

### Root Cause

Bricks uses different meta keys for different template areas:
- **Header**: `_bricks_page_header_2` (`BRICKS_DB_PAGE_HEADER`)
- **Content**: `_bricks_page_content_2` (`BRICKS_DB_PAGE_CONTENT`)
- **Footer**: `_bricks_page_footer_2` (`BRICKS_DB_PAGE_FOOTER`)

The header content was stored in `_bricks_page_content_2` instead of `_bricks_page_header_2`. When Bricks' `render_header()` function calls `Database::get_template_data('header')`, it looks for `BRICKS_DB_PAGE_HEADER`, finds nothing, and returns early.

**Why footer worked:** The footer had its content in the correct key `_bricks_page_footer_2`.

### Fix

1. **Inserted correct meta key** by copying content from `_bricks_page_content_2` to `_bricks_page_header_2`:
```sql
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
SELECT 21, '_bricks_page_header_2', meta_value
FROM wp_postmeta WHERE post_id = 21 AND meta_key = '_bricks_page_content_2';
```

2. **Fixed corrupted serialized data** — the original copy had an `a:4:` array with a non-existent parent reference (`flpxva`). Rebuilt clean serialized data using PHP's `serialize()` with a single code element matching the footer structure:
```php
$data = [[
    'id' => 'hdr001',
    'name' => 'code',
    'parent' => 0,
    'children' => [],
    'settings' => [
        'code' => $headerHTML,
        'executeCode' => true,
        '_cssCustom' => "#brxe-hdr001 { display: contents; }",
    ],
]];
$serialized = serialize($data);
```

3. **Updated both meta keys** to the clean data:
```sql
UPDATE wp_postmeta SET meta_value = '$serialized'
WHERE post_id = 21 AND meta_key IN ('_bricks_page_header_2', '_bricks_page_content_2');
```

4. **Re-exported** via Simply Static and deployed.

### Prevention

- When creating Bricks header/footer templates, always verify the correct meta key is populated:
```sql
SELECT meta_key FROM wp_postmeta WHERE post_id = <template_id> AND meta_key LIKE '_bricks_page%';
```
- Header templates must use `_bricks_page_header_2`
- Footer templates must use `_bricks_page_footer_2`
- Content templates use `_bricks_page_content_2`

---

## Category Labels on Static Pages

**Date:** 2026-06-29  
**Severity:** Low (cosmetic / design)

### Problem

Static pages (Privasi, Disclaimer, Hubungi) had orange `dtl-category` labels above their titles:
- "MAKLUMAT PENTING" above "Polisi Privasi"
- "HUBUNGI KAMI" above "Hubungi DigiTrust Lab"

These labels looked awkward and out of place — they're designed for blog post categories (e.g., "Digital Side Hustle" above an article), not standalone legal/info pages.

### Root Cause

Reused the blog post layout CSS class pattern for static pages without considering the context. Category labels make sense on posts but are nonsensical on pages that have no "category".

### Fix

Removed `dtl-category` divs from all three static pages using regex:
```powershell
$content = $content -replace '<div class="dtl-category"[^>]*>[^<]*</div>', ''
```

**New page flow:**
```
Polisi Privasi              ← h1 (28px, 700 weight)
Privasi anda penting...     ← excerpt with orange left border
Data yang Dikumpul          ← h2 section heading
...
```

### Prevention

- Static pages should NOT use category labels
- Only use `dtl-category` on blog post templates
- Static pages: h1 → excerpt → body content
- Blog posts: category label → h1 → excerpt → body content

---

## Bricks Code Element Not Rendering + Duplicate Meta Rows + Simply Static Stripping Form Tags

**Date:** 2026-07-01
**Category:** bricks-code-signature
**Severity:** Critical (header completely empty on live site)
**Time Spent:** ~45 minutes

### Symptoms

- Bricks header template (post_id=21) outputs empty `<div class="brxe-code"></div>` — no HTML content
- `update_post_meta()` returns `false` — data not saving
- Duplicate rows in `wp_postmeta` (2 rows per meta_key instead of 1)
- Simply Static export strips `<form>` and `<input>` tags from code element output
- Search bar present in WordPress frontend but missing from static export

### Root Cause

**Three separate issues:**

1. **Missing `signature` field** — Bricks code element with `executeCode: true` requires a valid `signature` field (computed as `wp_hash($code_content)`). Without it, Bricks renders the container div but skips code execution entirely. The footer works because it was created via Bricks editor (which auto-generates the signature).

2. **`update_post_meta()` returning false** — When the existing serialized data in the DB is corrupted or the meta_id sequence is broken, `update_post_meta()` silently fails (returns `false`). This caused the previous session to try `add_post_meta()` instead, which created **duplicate rows** (2 per meta_key). WordPress expects exactly 1 row per meta_key per post_id when using `get_post_meta($id, $key, true)`.

3. **Simply Static strips `<form>`/`<input>` tags** — When Bricks code element outputs HTML containing form elements, Simply Static's HTML processing strips them (likely for security). The `<form>`, `<input>`, and `<button>` tags are removed during the static export crawl.

### Solution

**Step 1: Fix DB duplicates and generate valid signature**

Create a one-shot mu-plugin (triggered via `?fix_header=1` URL parameter, then deleted):

```php
add_action('init', function() {
    if (!isset($_GET['fix_header'])) return;

    $headerHTML = '<div style="...">...header with search bar...</div>';

    // Generate valid signature — THIS IS THE KEY FIX
    $signature = wp_hash($headerHTML);

    $data = [[
        'id'       => 'hdr001',
        'name'     => 'code',
        'parent'   => 0,
        'children' => [],
        'settings' => [
            'code'        => $headerHTML,
            'executeCode' => true,
            'signature'   => $signature,  // Required by Bricks!
            'user_id'     => 1,
            'time'        => time(),
        ],
    ]];

    global $wpdb;
    // Delete ALL existing rows first (fixes duplicates)
    $wpdb->query($wpdb->prepare(
        "DELETE FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key IN ('_bricks_page_header_2', '_bricks_page_content_2')",
        21
    ));

    // Insert single clean row
    add_post_meta(21, '_bricks_page_header_2', $data);
    add_post_meta(21, '_bricks_page_content_2', $data);

    die("Header updated! Signature: $signature");
});
```

**Step 2: Post-process static files to re-inject search bar**

Added Phase 0 to `scripts/post-process-static.ps1`:

```powershell
# Detect header without search form, inject it
if ($content -match 'brxe-hdr001' -and $content -notmatch 'name="s"') {
    $pattern = '</nav><a href="#" style="background:#E8621A[^"]*"[^>]*>Dapatkan Panduan Percuma</a></div></div></header>'
    $content = $content -replace $pattern, "</nav>$searchBarHTML</div></div></header>"
}
```

**Step 3: Re-export via Simply Static + run post-process + deploy**

### Prevention

- **Always include `signature`, `user_id`, `time`** when creating Bricks code elements programmatically. The signature is `wp_hash($code_content)` — must be generated within WordPress context (not hardcoded).
- **Use `delete_post_meta()` + `add_post_meta()`** instead of `update_post_meta()` when dealing with corrupted meta data. `update_post_meta()` silently fails if the existing value comparison fails.
- **Check for duplicate rows** after any programmatic meta update:
  ```sql
  SELECT meta_key, COUNT(*) as cnt FROM wp_postmeta
  WHERE post_id = 21 GROUP BY meta_key HAVING cnt > 1;
  ```
- **Simply Static strips form/input tags** — always post-process static exports to re-inject any form elements that were removed.
- **Never leave one-shot scripts as mu-plugins** — they run on every page load. Use URL-triggered guards (`?fix_header=1`) and delete after use.
- **Clean up temp files** — the previous session left 25+ temp files in `%TEMP%` (SQL, PHP, TXT) from failed database update attempts.

---

## Simply Static Double-Slash Links (`//disclaimer` instead of `/disclaimer`)

**Date:** 2026-07-01
**Category:** simply-static-url-replacement
**Severity:** High (all internal links broken on static pages)

### Symptoms

- Internal links on static pages rendered as `//disclaimer`, `//hubungi`, `//privasi` (double slash)
- Links in header nav, footer, and `<head>` (RSS, oEmbed, REST API) all affected
- Browser interprets `//disclaimer` as protocol-relative URL → broken navigation

### Root Cause

Simply Static replaces the WordPress origin URL (`https://digitrust-lab.local`) with `/` during static export. When WordPress outputs links like `https://digitrust-lab.local/disclaimer/`, the replacement produces `//disclaimer/` — a double-slash prefix.

This affects all `href` and `src` attributes where WordPress outputs the full site URL followed by a path.

### Solution

Added Phase 6 to `scripts/post-process-static.ps1`:

```powershell
# Fix href="//path" -> href="/path" (but NOT https://)
if ($content -match 'href="//(?!/)') {
    $content = $content -replace 'href="//(?!/)', 'href="/'
}
# Same for src attributes
if ($content -match 'src="//(?!/)') {
    $content = $content -replace 'src="//(?!/)', 'src="/'
}
```

The negative lookahead `(?!/)` ensures `https://` links are not affected.

### Prevention

- **Post-process scripts are BANNED** — all fixes must be done via Bricks GUI or Respira MCP before export.
- After export, verify links with:
  ```powershell
  $c = [System.IO.File]::ReadAllText("D:\Coding Zone\digitrust-lab-static\privasi\index.html")
  ([regex]::Matches($c, 'href="//[^"]*"')).Count  # Should be 0
  ```

---

## Footer Template: Old Code Element Overriding Native Bricks Elements

**Date:** 2026-07-02
**Category:** bricks-template-content-conflict
**Severity:** High (footer styling not reflecting GUI changes on live site)
**Time Spent:** ~30 minutes

### Symptoms

- Footer template (post ID 46) was modified via Bricks Builder GUI to use native Section/Container/Block/Text-link elements with `13px` font size
- Local WordPress frontend showed correct `13px` styling
- After Simply Static export + deploy, live site still showed old `11px` hardcoded footer
- Static HTML files contained both the old code element (`brxe-rmdoll`) AND the new native elements (`brxe-bzutch`), with the code element rendering first and overriding

### Root Cause

Bricks stores template data in three separate meta keys:
- `_bricks_page_header_2` — header area elements
- `_bricks_page_content_2` — content area elements
- `_bricks_page_footer_2` — footer area elements

The footer template had:
- `_bricks_page_footer_2` → new native Bricks elements (Section, Container, Block, Text links) with `13px` styling ✅
- `_bricks_page_content_2` → old hardcoded HTML "code" element (`rmdoll`) with `11px` styling ❌

When Simply Static exports, it renders ALL three areas. The content area's code element appeared in the `<main id="brx-content">` section, and the footer area's native elements appeared in `<footer id="brx-footer">`. However, the code element's HTML included its own `<footer>` tag with inline styles, which visually overrode the native footer.

The Bricks Builder GUI only shows the footer area elements in the structure tree when editing a footer template — the content area elements are invisible in the editor, making this a "hidden" conflict with no GUI fix.

### Solution

Since there's no GUI way to edit or delete content area elements from a footer template (Bricks only shows footer area elements in the editor), a one-shot mu-plugin was used to delete the `_bricks_page_content_2` meta key:

```php
// One-shot: Clear _bricks_page_content_2 from footer template (post 46)
// Trigger: http://digitrust-lab.local/?fix_footer_content=1
// Then DELETE
add_action('init', function() {
    if (!isset($_GET['fix_footer_content'])) return;
    global $wpdb;
    $deleted = $wpdb->query($wpdb->prepare(
        "DELETE FROM {$wpdb->postmeta} WHERE post_id = %d AND meta_key = '_bricks_page_content_2'",
        46
    ));
    die("Deleted _bricks_page_content_2 from footer template. Rows: " . $deleted);
});
```

After deleting the meta key, re-exported via Simply Static, ran post-process script, deployed via wrangler — live site now shows native Bricks footer with correct `13px` styling.

### Prevention

- When migrating Bricks templates from code elements to native elements, check ALL three meta keys (`_bricks_page_header_2`, `_bricks_page_content_2`, `_bricks_page_footer_2`) for leftover code elements
- The Bricks GUI only shows the area matching the template type (header templates show header area, footer templates show footer area) — content area elements are hidden
- If GUI changes don't reflect after export, inspect the static HTML for duplicate rendering (e.g., both `brxe-rmdoll` and `brxe-bzutch` present)
- Use this SQL to check for leftover content area elements:
  ```sql
  SELECT meta_key FROM wp_postmeta WHERE post_id = 46 AND meta_key LIKE '_bricks_page%';
  ```

---

## Static Export Bloat Optimization (2,694 → 1,836 files)

**Date:** 2026-07-02
**Category:** export-optimization
**Severity:** Low (deployment speed + storage)
**Time Spent:** ~20 minutes

### Problem

Simply Static exported 2,694 files per build, but only 11 were actual content pages. 68% of files were `wp-includes/` core assets not used by Bricks Builder, and 163 were Bricks editor-only SVG icons.

### Root Cause

1. **`wp-includes/blocks/` (705 files)** — Simply Static's `Wp_Includes_Crawler` hardcodes `$dirs = ['css/', 'js/', 'fonts/', 'images/', 'blocks/']` with no filter to exclude `blocks/`. The `is_core_include_asset()` function short-circuits exclusion checks for all wp-includes URLs, so Simply Static's "Exclude URLs" setting cannot remove them.

2. **Bricks `assets/svg/builder/` (163 files)** — Theme Assets Crawler recursively scans all theme directories. The `ss_skip_crawl_theme_directories` filter exists but doesn't include `assets/svg/builder` by default.

### Solution

**Two-part approach:**

1. **Mu-plugin** (`mu-plugins/ss-skip-dirs.php`) — Uses `ss_skip_crawl_theme_directories` filter to skip `assets/svg/builder` at crawl time. Prevents 163 files from being discovered.

2. **Post-process Phase 8** (`post-process-static.ps1`) — Deletes `wp-includes/blocks/` from the static export directory after Simply Static transfers files. This is necessary because `is_core_include_asset()` prevents URL-level exclusion.

### Result

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total files | 2,694 | 1,836 | -868 (32%) |
| Deploy upload time | ~3.5 sec | ~1.6 sec | 54% faster |

### Prevention

- The mu-plugin (`ss-skip-dirs.php`) is permanent — it runs on every export
- Phase 8 post-process is BANNED — all export optimization must be done via Bricks/Simply Static settings.
- If Bricks adds new builder-only directories, add them to the `ss_skip_crawl_theme_directories` filter
- Verify file count after each export: should be ~1,830-1,850 range

---

## Bricks MCP — `missing_name` Error on `content` Add Action

**Date:** 2026-07-02
**Severity:** Low (wasted 3 retries)

### Problem

When using the Bricks MCP `content` tool with `action: "add"`, passing `name` inside the `element` JSON object results in:
```
{"code":"missing_name","message":"name is required. Provide the Bricks element type (e.g. heading, container, section)."}
```

### Root Cause

The `content` tool schema lists `name` as a **top-level parameter**, not a field inside `element`. I kept nesting it: `element: {"name": "block"}` instead of passing `name: "block"` directly.

### Fix

Pass `name` as a top-level parameter:
```
✅ name: "block", parent_id: "eptixc", post_id: 21
❌ element: {"name": "block", ...}
```

### Prevention Rule

**ALWAYS read MCP tool schema parameter names before calling.** When a tool returns `missing_X`, check if `X` is a top-level parameter in the schema — don't assume it goes inside a nested object. Retry with the correct structure on the first error, don't repeat the same mistake.

---

## Bricks MCP — Claude Desktop Connection (3 Issues Resolved)

**Date:** 2026-07-02
**Severity:** High (blocked all Claude Desktop ↔ Bricks MCP communication)
**Time to resolve:** ~30 minutes

### Problem

Claude Desktop could not connect to Bricks MCP on LocalWP. Three separate issues were encountered:

1. **Self-signed certificate rejection** — `DEPTH_ZERO_SELF_SIGNED_CERT`
2. **OAuth discovery timeout** — `mcp-remote` spent 60+ seconds on OAuth discovery, exceeding Claude Desktop's 60s timeout
3. **SSE format mismatch** — Bricks MCP returns `text/event-stream` (SSE) but Claude Desktop expects plain JSON over stdio

### Root Cause

| Issue | Cause |
|-------|-------|
| Self-signed cert | LocalWP uses its own SSL cert; Node.js rejects by default |
| OAuth timeout | `mcp-remote` always does OAuth discovery first, which is slow with self-signed certs |
| SSE mismatch | Bricks MCP endpoint returns SSE format; `mcp-remote` handles this but the custom bridge needed explicit SSE parsing |

### Solution: Custom stdio ↔ SSE Bridge

`mcp-remote` doesn't work for LocalWP + Claude Desktop because OAuth discovery takes too long. Instead, use a custom Node.js bridge script that:
- Skips OAuth entirely (direct HTTP POST with Basic auth)
- Bypasses self-signed cert via `NODE_TLS_REJECT_UNAUTHORIZED=0`
- Parses SSE responses and outputs clean JSON to stdout

**Bridge file:** `C:\Users\Zamri\bricks-mcp-bridge.mjs`

**Claude Desktop config (`claude_desktop_config.json`):**
```json
"bricks-mcp": {
  "command": "C:\\nvm4w\\nodejs\\node.exe",
  "args": ["C:\\Users\\Zamri\\bricks-mcp-bridge.mjs"]
}
```

(The bridge itself sets `NODE_TLS_REJECT_UNAUTHORIZED=0`, so no `env` block is required.)

**Bridge script key logic:**
```javascript
// 1. Content-Length framing in both directions
// 2. Stream SSE responses via response.body.getReader()
// 3. Race the reader against a deadline so it cannot hang forever
// 4. Fire-and-forget notifications (no id → no response expected)
// 5. keepalive: false on every fetch to avoid stuck reused connections
```

### What Was Tried (Failed Approaches)

| Approach | Result | Why It Failed |
|----------|--------|---------------|
| `type: "http"` + `url` | Not recognized | Claude Desktop doesn't support HTTP MCP natively |
| `npx mcp-remote` (no env) | Cert error | `DEPTH_ZERO_SELF_SIGNED_CERT` |
| `npx mcp-remote` + `NODE_TLS_REJECT_UNAUTHORIZED=0` | 60s timeout | OAuth discovery too slow |
| `npx mcp-remote` + `--transport http-only` | 60s timeout | Still does OAuth discovery |
| `mcp-remote` via wrapper.bat | 60s timeout | Same OAuth issue |
| Custom bridge (v1, no SSE parsing) | JSON parse errors | Output raw `event:`/`data:` lines |
| **Custom bridge (v2, SSE parsing)** | ✅ **Works** | Correctly extracts JSON from SSE |

### Prevention Rules

1. **ALWAYS set `NODE_TLS_REJECT_UNAUTHORIZED=0`** for any MCP server connecting to LocalWP from Claude Desktop
2. **NEVER use `mcp-remote` for LocalWP sites** — OAuth discovery takes 60+ seconds with self-signed certs, exceeding Claude Desktop's timeout
3. **ALWAYS parse SSE format** when bridging HTTP MCP endpoints to stdio — Bricks MCP returns `text/event-stream`, not plain JSON
4. **Use the custom bridge script** (`bricks-mcp-bridge.mjs`) as the standard approach for Claude Desktop ↔ Bricks MCP on LocalWP

---

## Bricks MCP — Bridge Works, Claude Desktop Still Says "Could Not Attach"

**Date:** 2026-07-02
**Category:** mcp-client-session-binding
**Severity:** High (Claude Desktop cannot expose Bricks MCP tools despite working bridge)

### Symptoms

- Claude Desktop shows `Could not attach to MCP server: bricks-mcp`
- MCP log shows older failed `mcp-remote` attempts with:
  - `DEPTH_ZERO_SELF_SIGNED_CERT`
  - `MCP error -32001: Request timed out`
- Later log entries use the custom bridge (`C:\Users\Zamri\bricks-mcp-bridge.mjs`) and sometimes succeed:
  - `Message from server: id=0 result`
  - `tools/list`
  - `tools/call`
- The latest failing launches show only:
  - `Message from client: method="initialize"`
  - about 60 seconds later, `notifications/cancelled`
  - `Server transport closed (renderer released port)`

### Root Cause

The Bricks MCP endpoint and custom bridge were reachable, but the bridge used `await response.text()` for normal JSON-RPC requests. Bricks MCP returns `text/event-stream` responses, and some SSE responses remain open instead of closing immediately. When that happened, the bridge received the server response but did not write it back to Claude Desktop until the stream ended.

Claude Desktop then waited about 60 seconds, sent `notifications/cancelled`, and released the renderer port.

This made the issue look like a Claude Desktop attach/session problem, but the sharper root cause was bridge-side SSE handling: the bridge needed to stream `data:` lines and forward the matching JSON-RPC response immediately.

### Verified Current Config

Claude Desktop config path:

```text
C:\Users\Zamri\AppData\Roaming\Claude\claude_desktop_config.json
```

Current `bricks-mcp` entry is correct:

```json
"bricks-mcp": {
  "command": "C:\\nvm4w\\nodejs\\node.exe",
  "args": ["C:\\Users\\Zamri\\bricks-mcp-bridge.mjs"]
}
```

(The bridge itself sets `NODE_TLS_REJECT_UNAUTHORIZED=0`, so no `env` block is needed in the config.)

### Fix

Patched `C:\Users\Zamri\bricks-mcp-bridge.mjs`:

- Added streaming SSE handling via `response.body.getReader()`
- Parses `data:` lines as they arrive
- Writes Content-Length-framed JSON-RPC responses immediately
- Cancels the stream after the response matching the request ID is forwarded
- Added a **real deadline inside the SSE reader** — the fetch timeout only aborts the HTTP request, but a slow/open SSE body can still hang the reader, so the reader is now raced against the same deadline
- Sends **notifications as fire-and-forget** (`notifications/initialized` has no `id`; the server never replies, so the bridge no longer waits for a response)
- Disabled **HTTP keep-alive** (`keepalive: false`) so a cancelled SSE reader cannot leave a reused connection in a stuck state
- Uses a 30 second bridge-side timeout so Claude gets an explicit JSON-RPC error instead of a silent 60s hang

After patching, a direct local test returned:

- `initialize` response from `bricks-mcp` version `1.5.1`
- successful `tools/list` response with the Bricks MCP tools

Then fully restart Claude Desktop:

1. Quit Claude Desktop from the system tray.
2. In Task Manager, end any remaining `Claude.exe` and Bricks MCP `node.exe` processes.
3. Reopen Claude Desktop.
4. Start a brand-new conversation.
5. Test with a simple Bricks request such as `list bricks templates`.

### Prevention

- Do not return to `mcp-remote` for LocalWP; the custom bridge is the working path.
- If the log shows `initialize` then `notifications/cancelled` about 60 seconds later, check whether the bridge is:
  - streaming SSE responses instead of waiting for `response.text()`
  - treating notifications as fire-and-forget instead of waiting for a server response
  - racing the SSE reader against a timeout instead of letting it hang forever
- Keep secrets out of chat/log summaries. Redact `Authorization: Basic ...` values when sharing logs.
- After editing the bridge, fully restart Claude Desktop (kill all `Claude.exe` and `node.exe` processes) so the new bridge is loaded.

---

## Bricks MCP — THE Root Cause: Wrong stdio Framing (Content-Length vs NDJSON)

**Date:** 2026-07-02
**Category:** mcp-stdio-framing
**Severity:** Critical (bridge silently ignored every Claude message → 60s timeout on every launch)
**Time Spent:** Several hours across multiple sessions

### Symptoms

- Every Claude Desktop launch: `Message from client: method="initialize" id=0` → **60 seconds of total silence** → `notifications/cancelled` → `Server transport closed (renderer released port)`
- The bridge logged `Server started and connected successfully`, so it *looked* fine
- One lucky window (12:54–13:17) worked (initialize + tools/list + 4 tool calls), which wrongly pointed suspicion at LocalWP/PHP-FPM hangs
- Direct `curl`/`node fetch` to the endpoint returned **200 in ~420ms** with valid SSE — proving the **server was healthy** the whole time

### Root Cause (the real one)

The **MCP stdio transport uses newline-delimited JSON (NDJSON)** — one JSON object per line, delimited by `\n`. It does **NOT** use LSP-style `Content-Length:` framing.

The bridge was doing the opposite on **both** sides:

1. **Input parser bug (fatal):** `tryParseMessages()` started with `readBuffer.indexOf('\r\n\r\n')` and `return`ed immediately when not found. NDJSON never contains `\r\n\r\n`, so the parser bailed **before** reaching its newline fallback. Result: `handleMessage()` was **never called** — the bridge silently discarded every message Claude sent.
2. **Output framing bug:** `writeMessage()` wrote `Content-Length: N\r\n\r\n` + body. Even if a response was produced, Claude's NDJSON reader could not parse a Content-Length frame, so it waited and cancelled at 60s.

### Diagnosis Method (repeatable)

Spawn the bridge exactly as Claude does and feed it a newline-terminated `initialize`, dumping raw stdout:

```js
// bridge-framing-test.mjs — spawn bridge, send NDJSON initialize, print raw stdout
const child = spawn('C:\\nvm4w\\nodejs\\node.exe', ['C:\\Users\\Zamri\\bricks-mcp-bridge.mjs']);
child.stdin.write(JSON.stringify({jsonrpc:'2.0',id:0,method:'initialize',params:{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'t',version:'1'}}}) + '\n');
```

- **Before fix:** `Total bytes received: 0` + no `[bridge]` stderr → parser never dispatched the message
- **After fix:** `[bridge] in req initialize id=0`, `SSE out 0 result`, and raw NDJSON `{"jsonrpc":"2.0","id":0,"result":{...}}\n` → `OUTPUT FRAMING: raw/NDJSON`

### Fix

In `C:\Users\Zamri\bricks-mcp-bridge.mjs`:

```javascript
// OUTPUT: newline-delimited JSON, not Content-Length
function writeMessage(obj) {
  stdout.write(JSON.stringify(obj) + '\n');
}

// INPUT: split on newlines, one JSON object per line
function tryParseMessages() {
  while (true) {
    const nlIdx = readBuffer.indexOf('\n');
    if (nlIdx === -1) return;                 // wait for a complete line
    const line = readBuffer.slice(0, nlIdx).toString('utf8').trim();
    readBuffer = readBuffer.slice(nlIdx + 1);
    if (line) handleMessage(line);
  }
}
```

The SSE streaming logic (`streamSseResponse`), fire-and-forget notifications, timeout race, and `keepalive:false` from the previous fix were all correct and were kept.

### Prevention Rules

1. **MCP stdio = NDJSON, always.** Read and write one JSON object per `\n`. Never use `Content-Length:` framing for MCP stdio (that's the LSP convention, a different protocol).
2. **When `initialize` → 60s silence → `notifications/cancelled` with the bridge logging "started successfully", suspect FRAMING, not the server.** Silence for the full 60s (with no bridge-side error) means Claude's messages never reached `handleMessage`, or its responses were unparseable.
3. **Prove server health independently first** — a direct `node fetch`/`curl` to the endpoint isolates server vs. bridge in seconds. Here it returned 200 in ~420ms, immediately ruling out LocalWP.
4. **Test the bridge in isolation** by spawning it and piping a `\n`-terminated `initialize`; confirm raw stdout is NDJSON before blaming Claude.

---

## Claude Desktop "Failed to call tool" — stdio buffer limit (2026-07-03)

**Symptom:** Claude Desktop UI shows "Failed to call tool 'template'" for every tool call, despite bridge logs showing successful responses (`hasResult=true hasError=false`, `result(1 blocks)`). Claude's AI hallucinates causes like "server not connected" or "auth missing".

**Root cause:** Claude Desktop (v1.18286.0) has a **stdio buffer size limit** (~8KB). The Bricks MCP server's `tools/list` response was **19.5KB** (11 tools with full schemas, enums, annotations, outputSchema). This caused Claude Desktop to silently fail processing the tools/list response, which in turn caused all subsequent tool calls to fail — even though the bridge correctly sent the tool call results.

**Full root cause chain (why tool calls failed even though bridge returned success):**
1. Claude Desktop launches bridge → bridge sends `tools/list` response (19.5KB) → **Claude Desktop silently fails to parse it** (exceeds ~8KB stdio buffer)
2. Claude Desktop never registers the tools properly → **tool registry is broken from startup**
3. Every `tools/call` after that fails with "Failed to call tool 'template'" — not because the call fails, but because Claude Desktop's tool registry was never populated
4. The bridge keeps working perfectly — logs show `hasResult=true hasError=false` — but Claude Desktop can't process the results because it doesn't recognize the tool
5. Claude's AI hallucinates causes → "server not connected", "auth missing", "MCP server isn't running" — all wrong. The server was never the problem.

**Key insight:** The fix was NOT in the tool call path. It was in the **tool discovery phase** (`tools/list`) that happens at startup. Once Claude Desktop could properly load all 11 tools (trimmed to 7.5KB), everything else worked automatically.

**Debugging journey:**
1. Logs showed every tool call succeeding on the bridge side (`WRITE stdout ... hasResult=true hasError=false`)
2. Added `isError: false` injection — didn't fix it
3. Downgraded `protocolVersion` from `2025-03-26` to `2024-11-05` — didn't fix it
4. Created a **mock bridge** with hardcoded minimal responses (235 bytes tools/list) — **worked!**
5. This proved the issue was in the response size, not the bridge logic
6. Truncated tools/list to 3 tools (4KB) — worked but `template` tool was missing
7. Final fix: trim all 11 tools' schemas (descriptions to 80 chars, remove annotations/outputSchema, keep only `action` enum + `response_format` + param name hints) → 7.5KB — **all 11 tools visible and callable**

**Fix applied in `bricks-mcp-bridge.mjs`:**
- `processLine()`: When `tools/list` response > 8KB, strip each tool to minimal schema — keep all param names + types, truncate action enum to 5 values, strip descriptions (except action), remove annotations/outputSchema → 7.9KB
- `processLine()`: Inject `isError: false` on all tool call results (defensive)
- `processLine()`: Downgrade `protocolVersion` to `2024-11-05` (defensive)
- `handleMessage()`: Parse `_additional_params` string into structured arguments before forwarding to WordPress (safety net for any params Claude sends as fallback string)
- Same trims applied to non-SSE response path
- Suppressed Node.js TLS warning on stderr (Claude Desktop may interpret stderr as bridge error)

**Prevention rules:**
1. **Claude Desktop has a stdio buffer limit (~8KB).** Any single NDJSON message larger than this will silently fail. Always trim large MCP responses in the bridge.
2. **Mock bridge test is the definitive isolation test.** If a hardcoded minimal bridge works but the real one doesn't, the issue is in response formatting/size — not protocol or transport.
3. **Claude's AI hallucinates causes for MCP failures.** It will say "server not connected" or "auth missing" even when logs prove otherwise. Trust the logs, not Claude's diagnosis.
4. **tools/list is the most likely response to exceed the limit** because it contains all tool schemas with full property descriptions, enums, and annotations.
5. **When trimming tool schemas, ALWAYS keep real parameter names.** Replacing params with a `_additional_params` hint string causes WordPress to reject tool calls (`isError=true`) because it doesn't recognize the parameters. Keep all param names + types, only strip descriptions and non-action enums.

---

## Bricks MCP `template update` Wipes Elements

**Date:** 2026-07-03
**Severity:** High (header template completely lost all elements)

### Problem

Using Bricks MCP `template update` action to change the template type (e.g., from `content` to `header`) **silently deletes all elements** in the template. The API returns success but `elements: []` is empty.

### Root Cause

The Bricks MCP `template update` action clears the elements array when changing the `type` field. This is destructive and irreversible — the elements are gone with no warning.

### Fix

Restored by:
1. Creating a new template with `content create` (type set at creation time)
2. Writing elements with `content update_content`
3. Setting conditions with `template set`

### Prevention Rules

1. **NEVER use `template update` to change type after elements exist.** The `type` field must be set at creation time only.
2. **Correct workflow for creating Bricks templates via MCP:**
   - Step 1: `content create` — create template with title, post_type, status, AND elements all at once
   - Step 2: `template set` — set template type and conditions
   - Step 3: `content update_content` — update individual elements if needed
3. **The `content update_content` action replaces ALL elements** — provide the complete element array, not just the one you want to update.
4. **The `content delete` action with element_id trashes the entire post** — not just the element. Be extremely careful.

---

## Bricks MCP `design` Tool — Wrong Domain Names Cause Silent Failure

**Date:** 2026-07-04
**Severity:** Medium (blocks design token management via MCP)

### Problem

The `design` MCP tool fails with a generic `"Tool execution failed"` error when using guessed domain names like `colors`, `variables`, `classes`, or `global_css`. Only `theme_style` works because it happens to be the correct name.

### Root Cause

The plugin's `Router.php` (line 4885) uses a PHP `match()` expression with strict domain matching. Only 6 exact strings are accepted:

```
'theme_style', 'global_class', 'color_palette', 'global_variable', 'typography_scale', 'font'
```

Any other value hits the `default` branch returning a `WP_Error`, which the MCP bridge converts to a generic failure message — swallowing the actual error text that would have listed the valid domains.

### Solution

Use the exact domain names from the table below:

| Wrong Name | Correct Domain |
|------------|---------------|
| `colors` | `color_palette` |
| `variables` | `global_variable` |
| `classes` / `global_classes` | `global_class` |
| `global_css` | (no equivalent — use `global_class` with `import_css` action) |

### Prevention

- Always reference `BRICKS-BUILDER-GUIDE.md` → "Design" section for valid domain names
- The `design` tool schema exposes parameters like `color_id`, `variable_id`, `classes_data` — these are for specific actions within valid domains, not indicators of domain names

### Verified Working (2026-07-04)

```
design(action="list", domain="theme_style")      → ✅ 200 OK
design(action="list", domain="color_palette")    → ✅ 200 OK
design(action="list", domain="global_variable")  → ✅ 200 OK
design(action="list", domain="global_class")     → ✅ 200 OK
design(action="list", domain="typography_scale") → ✅ 200 OK
design(action="get_status", domain="font")       → ✅ 200 OK
```

---

## Bricks MCP `template:update` Silently Ignores `elements` Parameter

**Date:** 2026-07-04
**Severity:** High (silent data loss — writes appear to succeed but don't persist)

### Problem

Calling `template` with `action: "update"`, a `template_id`, and an `elements` array returns a success response with template metadata — but the elements are never written. A subsequent `template:get` shows the template unchanged.

### Root Cause

`template:update` calls `update_template_meta()` in `BricksService.php:851-937`. This function only handles:
- `title` → `post_title`
- `status` → `post_status`
- `slug` → `post_name`
- `type` → `_bricks_template_type` meta
- `tags` / `bundles` → taxonomy terms

**The `elements` key is never read.** It's present in the MCP schema but not wired to any write logic. The function returns `true` (success), then `tool_update_template` fetches the unchanged template content and returns it — making it look like a successful response.

### Solution

Use `content:update_content` with `post_id` to write/replace elements:

```
content(action="update_content", post_id=<template_id>, elements=[...])
```

**NOT:**
```
template(action="update", template_id=<id>, elements=[...])  ← silently ignores elements
```

### Tool Responsibility Matrix

| Task | Tool | Action |
|------|------|--------|
| Update template title/status/slug | `template` | `update` |
| Update template type | `template` | `update` (⚠️ wipes elements if type changes) |
| Update template tags/bundles | `template` | `update` |
| Write/replace elements | `content` | `update_content` |
| Set template conditions | `template` | `set` |
| Create new template with elements | `content` | `create` (include elements at creation time) |

### Prevention

- **NEVER** use `template:update` to write elements — it's a metadata-only operation
- **ALWAYS** use `content:update_content` with `post_id` for element changes
- The `elements` parameter in `template:update`'s schema is misleading — ignore it

---

## Bricks MCP `template:list` — Invalid `type: "single"` Filter

**Date:** 2026-07-04
**Severity:** Low (clear error message, easy to identify)

### Problem

Using `type: "single"` with `template:list` fails with "invalid arguments" error.

### Root Cause

The MCP schema enforces a strict enum for the `type` parameter. `"single"` is not a valid Bricks template type — Bricks calls single-post templates `content`, not `single`.

### Valid Template Types

```
header, footer, archive, search, error, content, section, popup, password_protection
```

### Solution

Use `type: "content"` instead of `type: "single"` when filtering for single post templates.

---

## Bricks MCP `content update_content` Flattens Element Structure

**Date:** 2026-07-04
**Severity:** Critical (template structure destroyed, CSS selectors broken)
**Affected Template:** ID 52 (Blog Archive) — broken TWICE

### Symptoms

- After calling `content update_content` with a full element array (including `children` and `parent` fields), a subsequent `template get` shows:
  - ALL elements have `parent: 0` (flattened — no nesting)
  - ALL `children` arrays are missing
  - Element IDs have been regenerated (e.g., `b3hdbl` → `dppqck`)
- `_cssCustom` selectors referencing old IDs (e.g., `#brxe-b3hdbl`) no longer match any element
- Title/subtitle render left-aligned instead of centered
- The template appears to have no structure — just a flat list of elements

### Root Cause

The Bricks MCP `content update_content` action regenerates element IDs on save, even when explicit IDs are passed in the element array. When IDs are regenerated:

1. The `parent` field references (which used old IDs) become invalid
2. Bricks resets all `parent` fields to `0` since the referenced IDs no longer exist
3. `children` arrays are not preserved — they're derived from `parent` fields during rendering
4. `_cssCustom` selectors using `#brxe-{old_id}` break because the elements now have new IDs

This can also be triggered by opening a template in the Bricks visual editor and saving — the GUI appears to regenerate IDs on save.

### Prevention Rules

1. **ALWAYS `template get` BEFORE writing** — verify current structure and element IDs
2. **When writing, ALWAYS include explicit `children` arrays and correct `parent` refs** — never partially edit
3. **ALWAYS `template get` AFTER writing** — confirm nesting held and IDs haven't changed
4. **NEVER open/save a template in Bricks GUI** without verifying structure first — GUI saves can trigger the same flattening
5. **If IDs regenerate on every save**, update `_cssCustom` selectors to match the NEW IDs after each write
6. **Consider using Bricks GUI for structural edits** on templates with complex `_cssCustom` dependencies — MCP writes may not preserve IDs reliably

### Documented In

- `AGENTS.md` → "CRITICAL: Blog Archive Template (ID 52) — READ BEFORE TOUCHING"
- `.devin/skills/bricks-mcp-absolute/SKILL.md` → Step 2.5: Pre-Write Verification
- `.devin/rules/bricks-mcp-absolute.md` → NEVER Allowed section

---

## Global Horizontal Overflow on All Pages (Mobile)

**Date:** 2026-07-09
**Category:** css-overflow
**Severity:** High (all pages horizontally scrollable on mobile)
**Time Spent:** ~45 minutes

### Symptoms

- Every page on the site had horizontal scroll on mobile
- Content clipped on left edge, text/elements bleeding off right edge
- Affected all page types: blog archive, Gutenberg content pages, static pages
- Gutenberg content pages (Hubungi Kami, Polisi Privasi, Disclaimer) worst affected

### Root Cause (multi-layered)

Three separate issues compounding each other:

1. **`body { display: flex; flex-direction: column }` in Global CSS** — the original sticky footer fix created a flex formatting context on body. This caused child elements to behave as flex items, breaking normal block layout and contributing to overflow on mobile.

2. **`.bricks-mobile-menu-overlay` at `left: -300px`** — Bricks' off-canvas mobile menu drawer sits 300px off the left edge of the viewport. Browsers count this in `scrollWidth`, making every page appear horizontally scrollable even when no real content overflows.

3. **`#brx-content.wordpress { max-width: 800px; margin: 0 auto }` without `width: 100%`** — The Gutenberg content pages CSS set `max-width: 800px` but didn't constrain `width`. On a 412px mobile viewport, the element rendered at its natural 800px width and bled off both sides.

### Diagnosis Method

Used claude-in-chrome JS injection to find every overflowing element:

```javascript
const vw = document.documentElement.clientWidth;
document.querySelectorAll('*').forEach(el => {
  const rect = el.getBoundingClientRect();
  if (rect.right > vw + 2) {
    console.log(el.tagName, el.className, rect.right);
  }
});
```

Also confirmed `overflow-x: hidden` on a parent collapses `min-height: 100vh` in Chromium — use `overflow-x: clip` instead (same visual effect, doesn't create a new formatting context).

### Fix

Updated `bricks_global_settings.customCss` via Respira MCP (`respira_update_option`). **No Bricks cache clearing needed** — `bricks_global_settings` is in the WP options table, not Bricks' CSS cache. Simply Static picks it up fresh on next export.

**Final working CSS:**

```css
/* === BASE === */
body {
  background: var(--dtl-bg);
  font-family: var(--dtl-font);
  color: var(--dtl-text);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-x: clip; /* clip not hidden — hidden collapses min-height in Chromium */
}

/* === STICKY FOOTER === */
#brx-content {
  flex: 1 1 auto;
}

/* === OVERFLOW FIX === */
#brx-header,
#brx-footer {
  overflow-x: clip;
  box-sizing: border-box;
}

/* Mobile off-canvas menu — prevent it contributing to scroll width */
.bricks-mobile-menu-wrapper,
.bricks-mobile-menu-overlay {
  overflow: hidden;
}

img, video, iframe, embed, object {
  max-width: 100%;
  height: auto;
}

/* === GUTENBERG CONTENT PAGES === */
#brx-content.wordpress,
#brx-content.post-type-page {
  width: 100%;           /* CRITICAL — without this, renders at max-width on mobile */
  padding: 60px 24px 80px;
  max-width: 800px;
  margin: 0 auto;
  box-sizing: border-box;
}
```

### Key Learnings

- **`overflow-x: hidden` vs `overflow-x: clip`** — `hidden` creates a Block Formatting Context which collapses `min-height: 100vh` on the element in Chromium. Always use `clip` for horizontal overflow suppression on layout-critical elements.
- **`max-width` without `width: 100%` on flex/block children** — on mobile, `max-width: 800px` without `width: 100%` allows the element to render at its natural/content width. Always pair with `width: 100%; box-sizing: border-box`.
- **Bricks off-canvas menu always causes `scrollWidth > viewport`** — `.bricks-mobile-menu-overlay` and `.bricks-mobile-menu-wrapper` sit off-canvas at `left: -300px`. Must apply `overflow: hidden` to these classes globally.
- **`bricks_global_settings` edits USUALLY export fresh without cache clearing** — this option is read directly from the WP options table at render time. However, Bricks sometimes caches the inline CSS block (`bricks-frontend-inline-inline-css`), causing Simply Static to crawl a stale version. If a CSS change is missing from the export despite being live on WordPress, clear Bricks cache (Regenerate CSS files + Regenerate code signatures in Bricks → Settings) and re-export. Confirmed on 2026-07-09: `overflow-x:clip` was live on local WP but missing from the Simply Static export until cache was cleared.
- **Sticky footer: target `#brx-content { flex: 1 1 auto }`, not `body { display: flex }`** — Bricks already sets `display: flex; flex-direction: column` on body via `.brx-body`. We only need to ensure `#brx-content` grows to fill available space.

### Prevention

- When adding any `max-width` constraint to a block-level element, always include `width: 100%; box-sizing: border-box`
- Never use `overflow-x: hidden` on `html` or `body` — use `clip` instead
- After any global CSS change, run the JS overflow detector on both the blog archive AND a Gutenberg content page before deploying

---

## CSS Grid `1fr` Tracks Expand to Fit Content (Mobile Overflow)

**Date:** 2026-07-11
**Category:** css-overflow
**Severity:** High (blog archive + homepage + category pages all had horizontal scroll on mobile)

### Problem

Blog archive (`/blog/`), category pages (`/category/ai-tools/`), and homepage all had `body.scrollWidth: 1120px` on a 375px mobile viewport — massive horizontal overflow.

### Root Cause

Two issues combined:

1. **Bricks query loop containers lose `id` attribute in rendered HTML** — elements like `d5grid` and `qefl9u` render with class `brxe-d5grid` but NO `id="brxe-d5grid"`. CSS selectors using `#brxe-d5grid` don't match. Must use class selector `.brxe-d5grid` instead.

2. **CSS Grid `1fr` tracks expand to fit intrinsic content** — `grid-template-columns: repeat(3, 1fr)` creates tracks that expand to fit the largest child's intrinsic width (e.g., a 1100px-wide post card). This is per CSS Grid spec: `1fr` is equivalent to `minmax(auto, 1fr)`, and `auto` minimum means the track will never shrink below the content's intrinsic size.

### Fix

Use `minmax(0, 1fr)` instead of `1fr` to allow tracks to shrink below content size, plus `min-width: 0` on grid children:

```css
.brxe-d5grid {
  grid-template-columns: minmax(0,1fr) minmax(0,1fr) minmax(0,1fr) !important;
  width: 100% !important;
  max-width: 100% !important;
}
.brxe-d5grid > * {
  min-width: 0 !important;
  overflow: hidden;
}
@media (max-width: 767px) {
  .brxe-d5grid {
    grid-template-columns: minmax(0,1fr) !important;
  }
}
```

### Key Learnings

- **Bricks query loop containers lose `id` attributes** — always use `.brxe-{id}` class selectors, never `#brxe-{id}` ID selectors for query loop elements
- **`1fr` ≠ `minmax(0, 1fr)`** — `1fr` expands to fit content, `minmax(0, 1fr)` respects container width
- **`min-width: 0` on grid children** — prevents children from forcing the grid track wider than the container
- **Bricks `_display: "grid"` native setting** — adds `brx-grid` class and generates `.brxe-{id}.brxe-container { display: grid }` CSS, but does NOT set `grid-template-columns` — you must add that via `_cssCustom`

### Prevention

- Always use `minmax(0, 1fr)` in `grid-template-columns` for responsive grids
- Always use class selectors `.brxe-{id}` not ID selectors `#brxe-{id}` for Bricks query loop elements
- Add `min-width: 0` to grid children to prevent content from expanding tracks

---

## Deploy Pipeline (correct workflow)

**Date:** 2026-07-09
**Category:** deploy-automation
**Severity:** Prevention (stops recurring stale-deploy issues)

### The Problem

Three silent failure points caused "fixed on local, broken on live" repeatedly:

1. **Wrong directory** — `wrangler` run from `C:\Users\Zamri` hits `EBUSY: NTUSER.DAT` and never deploys
2. **Skipped Simply Static** — deploying without re-exporting ships the previous static folder
3. **No verification** — local is assumed equal to live; nothing checks

### The Fix: `deploy.ps1`

A deploy script at `D:\Coding Zone\digitrust-lab-static\deploy.ps1` that:

1. **Hardcodes the static directory** via `Set-Location` — can be run from any directory
2. **Pre-deploy freshness guard** — checks newest file mtime; warns if older than 10 minutes
3. **Post-deploy verification** — fetches the live site after a 15s CDN wait and checks for a CSS marker (`overflow-x: clip`). Prints green PASS or red FAIL with remediation instructions

### Correct Workflow

1. **(If CSS/template changed) Clear Bricks cache** — WP Admin → Bricks → Settings → click "Regenerate CSS files" → click "Regenerate code signatures" (accept the dialog)
2. **Run Simply Static export** — WP Admin → Simply Static → Generate (wait for "Done!")
3. **Run `.\deploy.ps1`** — from `D:\Coding Zone\digitrust-lab-static` (or any directory, the script hardcodes the path)
4. **Trust the PASS/FAIL output** — green PASS means live site verified; red FAIL means follow the remediation steps printed by the script (clear Bricks cache → re-export → re-deploy)

### Configurable Marker

The expected CSS marker is stored near the top of `deploy.ps1`:

```powershell
$ExpectedMarker = "overflow-x: clip"
```

Update this when the CSS changes. The marker must match the **exact** string Bricks renders (note the space after the colon). The marker must be a string unique to the post-fix inline CSS that appears on every page.

### What the Script Does NOT Do

- ❌ Does NOT modify CSS or HTML content
- ❌ Does NOT run post-processing scripts
- ❌ Does NOT edit Bricks templates
- ❌ Does NOT clear Bricks cache

It is deploy-automation and verification only — fully compliant with AGENTS.md Bricks-only policy.

---

## Blog Page 404 — Missing Posts Page Setting (2026-07-09)

**Symptom:** Published post "Apa Itu AI?" (ID 256) exists in WP Admin → Posts with status "Publish", but `/blog/` returns 404 and the post URL also returns 404 on local WordPress.

**Root cause:** Two issues:
1. **No Blog page existed** — WordPress had no page with slug `blog` to serve as the posts archive
2. **No posts page set in Reading Settings** — Settings → Reading → "Posts page" was set to "— Select —" (0), meaning WordPress didn't know which page to use for the blog archive

**Fix (3 steps):**

1. **Create a Blog page** via Respira MCP:
   ```
   respira_create_custom_post(type: "page", title: "Blog", slug: "blog", status: "publish")
   ```
   Result: Page ID 277 created at `/blog/` (original page ID 260 was deleted and recreated)

2. **Set Blog page as posts page** in Settings → Reading:
   - WP Admin → Settings → Reading
   - Set "Posts page" to "Blog" (ID 277)
   - Click Save

3. **Flush permalinks:**
   - WP Admin → Settings → Permalinks
   - Click Save (no changes needed — just re-saves to flush rewrite rules)

**Verification:**
- `/blog/` → ✅ Returns "Blog - DigiTrust Lab" with post listed
- `/apa-itu-ai/` → ✅ Returns the published post

**Note on post slug:** The post slug is `apa-itu-ai` (short), NOT the full title-based slug `apa-itu-ai-dan-kenapa-ia-bukan-setakat-robot-dalam-filem`. Always check the actual slug via `respira_read_post` before testing URLs.

**When to do this:** Any time a published post doesn't appear on the blog page or returns 404. Check Settings → Reading first — if "Posts page" is unset, that's the cause.

**Prevention:** Always ensure a Blog page exists and is set as the posts page before publishing any blog posts.

---

## Blog Archive Template 52 Not Rendering — 3 Root Causes (2026-07-09)

**Symptom:** `/blog/` shows the default Bricks `posts` widget (random element IDs like `brxe-b91484`, `brxe-af1efa`) instead of our custom Template 52 design (heading "Blog DigiTrust Lab", tagline, post card grid with elements `d1sect`, `d4titl`, `d5grid`, etc.).

**Root cause — 3 issues found and fixed:**

### Issue 1: Template status was `private` (PRIMARY CAUSE)

Bricks queries templates with `post_status: 'publish'` only in `get_all_templates_by_type()` (`includes/database.php` line 766). Template 52 was set to `private`, making it **completely invisible** to Bricks' template matching system. No condition could ever match because the template was never in the candidate list.

**Fix:** `respira_update_custom_post(type: "bricks_template", id: 52, status: "publish")`

### Issue 2: `archiveType: any` does NOT match the WordPress posts page

WordPress `is_home()` (the posts page at `/blog/`) returns `false` for `is_archive()`. Bricks treats `is_home()` as `content_type: 'content'` (`database.php` line 492), NOT as an archive. The `archiveType` condition is only evaluated inside `if ( is_archive() && $condition['main'] === 'archiveType' )` (`database.php` line 961). Since `is_home()` returns `false` for `is_archive()`, the `archiveType: any` condition can **NEVER** match on `/blog/`.

**Fix:** Removed `archiveType: any` condition entirely.

### Issue 3: Old `ids` condition referenced deleted page ID 260

Previous template conditions included `ids: ['260']` for a Blog page that was deleted and recreated as page ID 277. The stale ID meant the `ids` condition never matched the current posts page.

**Fix:** Set `ids: ['277']` as the sole condition. On `is_home()`, Bricks sets `$post_id = get_option('page_for_posts')` (277) (`database.php` line 438-439). The `ids` condition matches this with score 10 (highest priority, `database.php` line 911-913).

### How conditions were saved

The `_bricks_template_settings` meta key (which stores `templateConditions`) is protected. Direct Respira meta updates appeared to succeed but didn't reliably persist. The reliable method is Bricks' own AJAX save endpoint:

```javascript
// Run in browser console on a WP admin page
const formData = new FormData();
formData.append('action', 'bricks_save_post');
formData.append('postId', '52');
formData.append('nonce', window.bricksData?.nonce || '36dae4decb');
formData.append('templateSettings', JSON.stringify({
  templateConditions: [
    { id: 'cond001', main: 'ids', ids: ['277'] }
  ]
}));
fetch('/wp-admin/admin-ajax.php', { method: 'POST', body: formData })
  .then(r => r.json()).then(console.log);
```

### Verification

- `/blog/` → ✅ Shows "Blog DigiTrust Lab" heading, tagline, and post card grid
- `/apa-itu-ai/` → ✅ Single post still works correctly
- No default `brxe-posts` widget visible

### Key Bricks Source Code References

| File | Line(s) | What it does |
|------|---------|--------------|
| `includes/database.php` | 438-439 | Sets `$post_id = page_for_posts` on `is_home()` |
| `includes/database.php` | 492 | Maps `is_home` to `content_type: 'content'` |
| `includes/database.php` | 766 | Queries templates with `post_status: 'publish'` only |
| `includes/database.php` | 897-928 | `ids` condition matching — score 10 (highest) |
| `includes/database.php` | 961 | `archiveType` condition — gated behind `if ( is_archive() )` |
| `includes/ajax.php` | 2306-2313 | Bricks AJAX save for `templateSettings` |

**When to do this:** Any time a Bricks template is not rendering on a page where it should. Check:
1. Template status is `publish` (not `private`)
2. Condition type matches the WordPress page type (`ids` for posts page, `archiveType` for actual archives)
3. `ids` condition references the current page ID (not a deleted/recreated one)

**Prevention:** Always verify template status is `publish` after creating or importing Bricks templates. Never use `archiveType` conditions for the WordPress posts page (`is_home()`) — use `ids` targeting the Blog page ID instead.

## Template 10 — Broken Dynamic Tags on Single Post (2026-07-10)

**Symptom:** On every single post page (e.g. `/apa-itu-ai/`), three meta elements showed raw dynamic tag text instead of resolved values:
- Orange avatar circle: `{post_author:initial}` (raw text, not "Z")
- Author name: `{post_author}` (raw text, not "Zed")
- Date/reading time: `{rank_math_reading_time}` (raw text, not a date)

### Root Causes (3 independent issues)

**1. `{post_author:initial}` — invalid tag syntax**

Bricks has no `:initial` modifier. The available author tags are: `author_id`, `author_name`, `author_bio`, `author_email`, `author_website`, `author_archive_url`, `author_avatar`, `author_meta` (see `provider-wp.php` lines 117-152). No character-level filter exists (`num_words` exists for word trimming, but no `num_chars` or `:initial`).

**Fix:** Hardcoded `"Z"` — single-author blog, no dynamic tag available.

**2. `{post_author}` — wrong tag name**

The correct Bricks tag for author display name is `{author_name}`, NOT `{post_author}` or `{post_author:name}`. Bricks registers author tags with the `author_` prefix (not `post_author:`). The tag resolves via `get_author_tag_value()` in `provider-wp.php` line 1562-1581, which checks `first_name + last_name` first, then falls back to `display_name`.

**Fix:** Changed to `{author_name}` → resolves to "Zed".

**3. `{rank_math_reading_time}` — no such dynamic tag exists**

Rank Math does not register any Bricks dynamic data tag. And `{post_reading_time}` is NOT a dynamic data tag either — it's a Bricks **element type** (`post-reading-time`). The element calculates reading time via JavaScript on the frontend (or server-side inside query loops using `str_word_count` / `ceil`). There is no way to output reading time inside a `text-basic` element's `text` field.

**Fix:** Restructured `mtxtcl` (meta text column) into a flex-wrap row:
- `mnamet` (author name) → `width: 100%` (takes full line 1)
- `minfot` (date) → text changed to `{post_date} ·` (date + separator)
- Injected native `post-reading-time` element (ID: `891b1e`) into `mtxtcl` → styled with `color: #6B6B6B`, `font-size: 12px`, `suffix: " min baca"`, `contentSelector: "#brxe-bodycn"`

### Also: Post title link on /blog/ (Template 52)

**Root cause:** Heading element `mnjhh4` on Template 52 had `link: {type: "dynamic", dynamicData: "{post_url}"}`. The `type: "dynamic"` link type does NOT resolve `{post_url}`. Bricks `set_link_attributes()` in `base.php` (lines 2405-2426) requires `type: "external"` when the URL contains a dynamic data tag. The `external` type detects the `{...}` pattern and routes it through `bricks_render_dynamic_data()` with `context: 'link'`.

**Fix:** Changed to `link: {type: "external", url: "{post_url}"}`.

### Key Bricks Source Code References

| File | Line(s) | What it does |
|------|---------|--------------|
| `provider-wp.php` | 117-152 | Registers `author_*` dynamic data tags (NOT `post_author:*`) |
| `provider-wp.php` | 1562-1581 | `get_author_tag_value()` — resolves `author_name` to `first_name + last_name` or `display_name` |
| `provider-wp.php` | 37-94 | Registers `post_*` dynamic data tags (`post_title`, `post_url`, `post_date`, etc.) — no `post_reading_time` |
| `elements/post-reading-time.php` | 66-123 | Native reading time element — JS-based on frontend, `str_word_count` in loops |
| `elements/base.php` | 2405-2426 | `set_link_attributes()` for `type: "external"` — detects `{...}` pattern, routes through `bricks_render_dynamic_data()` |

### Prevention

1. **Always verify tag names** in `provider-wp.php` before using them — Bricks uses `author_*` prefix, not `post_author:*`
2. **Reading time is an element, not a tag** — use the native `post-reading-time` element, not a dynamic data tag in a text field
3. **For post URL links** — use `link: {type: "external", url: "{post_url}"}`, NOT `type: "dynamic"` with `dynamicData`
4. **No character-level extraction** — Bricks has `num_words` filter but no `num_chars` or `:initial` modifier

---

## Bricks `{echo:}` Dynamic Tags — Only First Tag Processed Per Text Field (2026-07-10)

**Symptom:** When combining `{echo:post_date_reading_time}` with another dynamic tag (e.g., `{post_date}`) in the same Bricks `text-basic` element's `text` field, only the first tag resolves. The second `{echo:}` tag renders as raw text or is skipped entirely.

**Root cause:** Bricks' dynamic data parser in `providers.php` processes dynamic tags sequentially but stops parsing after the first `{echo:}` tag by default. The `bricks/code/echo_everywhere` filter (`__return_true`) allows `{echo:}` tags to render everywhere, but the parser still only handles one `{echo:}` tag per field — subsequent `{echo:}` tags in the same field are not parsed.

**Fix:** Create a single PHP function that combines all needed data into one string, then use a single `{echo:function_name}` tag:

```php
// In digitrustlab-archive-title.php plugin
function post_date_reading_time() {
    $post_id = get_the_ID();
    if (!$post_id) return '';
    $date = get_the_date('F j, Y', $post_id);
    $content = get_post_field('post_content', $post_id);
    $word_count = str_word_count(wp_strip_all_tags($content));
    $minutes = max(1, ceil($word_count / 200));
    return $date . ' &middot; ' . $minutes . ' min read';
}
```

Then in Bricks: `{echo:post_date_reading_time}` → outputs "July 9, 2026 · 4 min read"

**Required filters in the plugin:**
```php
add_filter('bricks/code/echo_everywhere', '__return_true');
add_filter('bricks/code/echo_function_names', function ($names) {
    return true; // Allow all echo functions (safe on local dev)
});
```

**Prevention:** Never combine multiple `{echo:}` tags in one text field. Consolidate into a single PHP function that returns the full combined string.

---

## Homepage Query Loop Not Rendering — Bricks Pages Need Editor Save to Activate `hasLoop` (2026-07-10)

**Symptom:** After injecting a "Latest Posts" section with a query loop container (element with `hasLoop: true` and `query` settings) onto the homepage (page ID 280) via Respira MCP, the query loop did not render on the frontend. The settings were correctly stored in the database (confirmed via `respira_extract_builder_content`), but the frontend showed only the static elements — no post cards.

Respira also returned warnings: "Unknown control 'hasLoop' for the Bricks 'container' element" and "Unknown control 'query' for the Bricks 'container' element".

**Root cause:** Bricks' frontend renderer does not automatically process `hasLoop` and `query` settings on **pages** (post_type: `page`) when they're written via MCP/API without a subsequent editor save. The settings exist in the database, but Bricks' rendering pipeline needs a "save event" from the visual editor to register and activate the query loop on the frontend.

This is specific to **pages** — Bricks **templates** (post_type: `bricks_template`) process query loops from database settings without needing an editor save.

**Fix:** Manually open the page in the Bricks editor and save:
1. Navigate to `https://digitrust-lab.local/?bricks=run` (or WP Admin → Pages → Home → Edit with Bricks)
2. Confirm the query loop settings are present in the editor (they will be — they're in the DB)
3. Click Save
4. Frontend now renders the query loop correctly

**Prevention:** After injecting query loops onto pages via Respira MCP, always open the page in the Bricks editor and save once to activate the loop on the frontend. Templates don't need this step — only pages.

---

## `_cssCustom` Selectors in Query Loops — Use `.brxe-{id}` Not `#brxe-{id}` (2026-07-10)

**Symptom:** Custom CSS applied via `_cssCustom` on elements inside a query loop container did not render. The category pill (background color), reading time pill (background color), card hover effect, image sizing, title link color, and excerpt line-clamp all appeared unstyled — transparent backgrounds, no hover effect, no image sizing.

**Root cause:** Elements inside a Bricks query loop get **new element IDs on each iteration**. The original element ID (e.g., `16aef2`) only matches the first iteration. Subsequent iterations have different IDs, so `#brxe-16aef2` (ID selector) only styles the first card.

Additionally, Bricks renders loop elements with **class** selectors (`.brxe-16aef2`) rather than ID selectors in some contexts, meaning `#brxe-{id}` may not match the rendered DOM at all.

**Fix:** Use **class selectors** (`.brxe-{id}`) instead of **ID selectors** (`#brxe-{id}`) in `_cssCustom` for any element inside a query loop:

```css
/* ❌ WRONG — only matches first iteration or doesn't match at all */
#brxe-16aef2 { background: rgba(232,98,26,0.1); }

/* ✅ CORRECT — matches all iterations via class */
.brxe-16aef2 { background: rgba(232,98,26,0.1); }
```

**Elements updated on homepage (ID 280):**

| Element | ID | Purpose | Selector |
|---------|-----|---------|----------|
| Category pill | `16aef2` | Orange pill background | `.brxe-16aef2` |
| Reading time pill | `c66b36` | Black pill background | `.brxe-c66b36` |
| Card container | `4c6189` | Hover effect | `#brxe-4c6189` (OK — container ID is stable) |
| Image | `60b016` | Fixed height + object-fit | `#brxe-60b016 img` (OK) |
| Title | `fa7ecb` | Link color + hover | `#brxe-fa7ecb a` (OK) |
| Excerpt | `ccbefc` | 2-line clamp | `#brxe-ccbefc` (OK) |

**Note:** Container-level elements (card wrapper, image, title, excerpt) worked fine with `#brxe-{id}` because their IDs remain stable. Only the pill elements (which are `text-basic` elements rendered inside the loop) needed class selectors. When in doubt, use `.brxe-{id}` for all elements inside a query loop.

**Prevention:** For any `_cssCustom` on elements inside a query loop, default to `.brxe-{id}` class selectors. Only use `#brxe-{id}` for container/wrapper elements that have stable IDs across iterations.

---

## Simply Static "Push" Button — Not Labeled "Generate" or "Export" (2026-07-10)

**Category:** ui-navigation
**Severity:** Low (workflow confusion)

**Issue:** The Simply Static generate page (`/wp-admin/admin.php?page=simply-static-generate`) does not have a button labeled "Generate" or "Export" or "Generate Static Site". The trigger button is labeled **"Push"** with class `components-button generate`.

**Navigation:**
- WP Admin → Simply Static → Generate → click **"Push"** button (top of the page, next to nav items)
- Page title changes to "(X%) Simply Static - Generate" during export
- Wait for completion (typically 5-8 minutes for ~2,600 files)

**Prevention:** When instructing someone to run a Simply Static export, tell them to click "Push", not "Generate" — the button label is counterintuitive.

---

## Simply Static Homepage Export Bug — `.local` TLD Rejected (2026-07-10)

**Category:** simply-static
**Severity:** Critical (homepage not exported)

**Symptom:** Simply Static export completes successfully (2,590+ files transferred) but `index.html` in the output directory is NOT updated — it retains the old timestamp and old content. No error is reported by Simply Static. Other files (CSS, JS, robots.txt) are updated correctly.

**Root Cause:** `wp_http_validate_url()` silently rejects URLs with `.local` TLD. Simply Static's Homepage URL crawler tries to fetch `https://digitrust-lab.local/` to include in the export, but WordPress's URL validator rejects it as "not a valid URL". The crawler skips the front page with zero error output. The homepage HTML is never fetched, so the existing `index.html` in the output directory is never overwritten.

**Diagnostics:** Simply Static → Diagnostics tab shows "Is not a valid URL" warning for the homepage URL.

**Fix:** Add `https://digitrust-lab.local/` to Simply Static → Settings → General → **Additional URLs** field. This forces Simply Static to include the homepage URL in the export queue, bypassing the `wp_http_validate_url()` rejection.

**After fix:** Homepage exports correctly on every Push. `index.html` timestamp updates to current export time. New content (hero text, pills, etc.) appears in the static output.

**Verification:** After export, check `D:\Coding Zone\digitrust-lab-static\index.html`:
- `LastWriteTime` must be today
- Search for recent content keywords (e.g. "warga Malaysia", "brxe-b8bfe4")
- If still stale → re-save page via Respira + re-export

**Prevention:** The `additional_urls` workaround is permanently in place. No action needed on future exports. If the homepage stops exporting again, check the Additional URLs setting first.

---

## Blog Archive Horizontal Scroll on Mobile — CSS Grid `min-width: auto` Gotcha (2026-07-11)

**Category:** layout, mobile, css-grid  
**Severity:** High (layout broken on all mobile viewports)  
**Affected URL:** `/blog/` and any page using Template 52 (blog archive)  
**Affected element:** `brxe-d5grid` (the 3-column post card grid container)

### Symptom
`/blog/` shows a horizontal scrollbar on mobile. Post cards overflow the viewport width. Problem does not appear on desktop. Previous "fixes" (adding `overflow-x: hidden` to parent section and wrapper container) did not resolve it — scroll remained.

### Why Previous Fixes Failed
Adding `overflow-x: hidden` / `clip` to `brxe-d1sect` (section) and `brxe-d2wrap` (wrapper) only *masks* the overflow visually on the parent. The grid tracks themselves were still computing `gridTemplateColumns: 1100px 0px` instead of the correct `~230px 230px`. Hiding overflow on an ancestor hides symptoms, not the cause.

### Root Cause — CSS Grid `min-width: auto` Track Inflation

This is a CSS Grid specification behaviour that is almost universally misunderstood:

1. `brxe-d5grid` has `grid-template-columns: repeat(2, 1fr)` at `max-width: 991px` — this CSS is correct
2. At 500px viewport each `1fr` track should resolve to `~230px`
3. **BUT:** CSS Grid items default to `min-width: auto`, meaning each grid item refuses to shrink below its **min-content size**
4. The excerpt text element `brxe-61bw2h` inside each card has `white-space: normal` + `word-break: normal` — its min-content width is ~803px (the longest unbreakable character run)
5. Grid tracks cannot shrink below the item's min-content size → tracks inflate to `1100px` each
6. `brxe-qefl9u` (card container) has `overflow: hidden` which hides its internal bleed, creating the illusion of containment — but the `1100px` grid track still causes the page-level scroll

**Live inspection evidence at 500px viewport:**
```
brxe-d5grid  offsetWidth: 460px  scrollWidth: 1100px  computedGrid: "1100px 0px"
brxe-qefl9u  computedWidth: 1100px  (grid item, min-width: auto → inflated)
brxe-61bw2h  computedWidth: 803px   (text block driving min-content expansion)
```

### The Fix — One Line of CSS

Add `min-width: 0` to the grid item container `brxe-qefl9u`. This overrides the `min-width: auto` default and allows grid tracks to shrink freely to their `1fr` allocation.

**Update `_cssCustom` on element `brxe-qefl9u` in Template 52:**
```css
.brxe-qefl9u {
  overflow: hidden;
  min-width: 0;   /* KEY FIX — allow grid item to shrink below min-content */
  transition: transform 0.2s, box-shadow 0.2s;
}
.brxe-qefl9u:hover {
  transform: translateY(-3px);
  box-shadow: rgba(0, 0, 0, 0.08) 0px 8px 20px;
}
```

Or target all direct grid children via the grid container `_cssCustom`:
```css
#brxe-d5grid > * { min-width: 0; }
```

**Do NOT** use `overflow-x: hidden/clip` on the section or wrapper as a substitute — that only masks symptoms and breaks `position: sticky` children.

### Verification Steps
1. Open `https://digitrust-lab.local/blog/` in Chrome DevTools → iPhone SE (375px)
2. Inspect `brxe-d5grid` computed style → `gridTemplateColumns` should show two equal columns (~`177px 177px`) not `1100px 0px`
3. Confirm no horizontal scrollbar
4. Run Simply Static export + Wrangler deploy
5. Verify `https://www.digitrustlab.com/blog/` on real mobile device

### Prevention Rule (add to all future grid builds)
Whenever building a CSS Grid layout in Bricks, always add `min-width: 0` to grid item containers. Bricks containers default to `min-width: auto` which causes track inflation whenever items contain text or images with non-zero intrinsic sizes. Affects post card grids, feature grids, pricing tables — any multi-column grid with text content.

---

## Simply Static — Blog Page (`/blog/`) Never Exported (2026-07-11)

**Category:** simply-static
**Severity:** Critical (`/blog/` missing entirely from static output)
**Affected URL:** `/blog/` → `D:\Coding Zone\digitrust-lab-static\blog\index.html`

### Symptom
`blog/` folder in the static output directory is completely empty — no `index.html` exists at all. Simply Static runs to completion without errors, but `/blog/` is never written. This is separate from the homepage bug (which was about stale content) — here the file is entirely absent.

### Root Cause — TWO separate problems (both confirmed from debug log)

**Problem 1: URL not in discovery queue**
The WordPress "Blog" page (ID 277, slug `/blog/`) is the **Posts Page** (`page_for_posts = 277`). WordPress's `get_posts()` suppresses this page from query results by default — it's treated as a virtual archive, not a regular page. So the `post_type` crawler never finds it. The `home` crawler only handles the front page. Result: `/blog/` is never discovered.

**Problem 2: Local by Flywheel cURL loopback deadlock (the real blocker)**
Even after adding `/blog/` to `additional_urls` (which correctly queues it), Simply Static's fetcher timed out trying to fetch it:

```
[class-ss-url-fetcher.php:529] Fetching URL: https://digitrust-lab.local/blog/?simply_static_page=171437
[class-ss-url-fetcher.php:204] cURL error 28: Operation timed out after 30005 milliseconds with 0 bytes received
```

Local by Flywheel uses single-threaded PHP-FPM. When Simply Static's background job (occupying the only PHP thread) tries to cURL `https://digitrust-lab.local/blog/`, the request deadlocks — the PHP thread is already busy. The homepage (`/`) is fetched first in the queue before the deadlock window; `/blog/` hits the queue ~3 minutes later when PHP-FPM is locked.

**Why other pages work:** Individual posts and static pages are fetched earlier in the queue, before the loopback deadlock window occurs. `/blog/` specifically gets queued later and always hits the timeout.

### Fix

**Step 1:** Add both URLs to Simply Static `additional_urls` (already done via Respira):
```
https://digitrust-lab.local/
https://digitrust-lab.local/blog/
```

**Step 2:** Install mu-plugin `ss-blog-page-fix.php` at `wp-content/mu-plugins/` with three fixes:
```php
// Fix 1: Allow WordPress loopback requests (WP 5.6+ blocks these by default)
add_filter( 'http_request_host_is_external', '__return_true' );

// Fix 2: Increase cURL timeout for digitrust-lab.local from 30s to 90s
add_filter( 'http_request_args', function ( $args, $url ) {
    if ( strpos( $url, 'digitrust-lab.local' ) !== false ) {
        $args['timeout'] = 90;
    }
    return $args;
}, 10, 2 );

// Fix 3: Always inject blog page URL into Simply Static queue during setup
add_filter( 'ss_setup_task_additional_urls', function ( $additional_urls ) {
    $blog_page_id = (int) get_option( 'page_for_posts' );
    if ( $blog_page_id > 0 ) {
        $blog_url = get_permalink( $blog_page_id );
        if ( is_string( $blog_url ) && strpos( $additional_urls, rtrim( $blog_url, '/' ) ) === false ) {
            $additional_urls .= ( $additional_urls ? "\n" : '' ) . $blog_url;
        }
    }
    return $additional_urls;
} );
```

### Verification
1. After export completes, check debug log at `wp-content/uploads/simply-static/[key]-debug.txt`
2. Should show `/blog/` fetched successfully (no cURL error 28)
3. Check `D:\Coding Zone\digitrust-lab-static\blog\index.html` exists with today's timestamp
4. File should contain `min-width: 0` in the embedded CSS
5. File should contain "Blog DigiTrust Lab" heading text
6. Deploy via Wrangler, verify `https://www.digitrustlab.com/blog/` loads on mobile

### If cURL error 28 persists

**Option 1 — Run export via WP CLI (avoids loopback deadlock entirely):**
Open Local by Flywheel → Site Shell and run:
```bash
wp simply-static run
```
This runs the export in the CLI thread instead of the browser's PHP-FPM thread, avoiding the single-threaded deadlock that causes cURL error 28 on `/blog/`.

**Option 2 — Nuclear option (manual fetch):**
The timeout may still occur even with the mu-plugin. Fetch the blog page HTML manually:
```bash
# On your machine, fetch the rendered blog page and save it
curl -k https://digitrust-lab.local/blog/ -o "D:\Coding Zone\digitrust-lab-static\blog\index.html"
# Then find-replace all digitrust-lab.local with www.digitrustlab.com in that file
# Then Wrangler deploy
```

### Post-Session Cleanup (run after multiple exports)

After 3+ Simply Static exports in one session, Local WP gets sluggish. Run in Site Shell:

```bash
# 1. Clear WP transients and object cache
wp transient delete --all
wp cache flush
```

Then in Adminer (Local → Database → Open Adminer):
```sql
TRUNCATE TABLE wp_simply_static_pages;
```

**Note:** `wp db query` does NOT work in Local by Flywheel Site Shell on Windows — MySQL uses a socket file, not `localhost:3306`. Always use Adminer for direct SQL queries.

Also turn off Simply Static debug mode (`debugging_mode: "0"`) via Respira when diagnosis is complete — the debug log grows fast (6.7MB in one session). Debug mode is currently OFF as of 2026-07-11.

---

## Local WP DB Health Check & Cleanup (2026-07-11)

**Trigger:** After 3+ Simply Static exports in one session, or when Local WP feels sluggish.

**Root cause of bloat:** Each Simply Static export adds ~600-2500 rows to `wp_simply_static_pages`, creates 700+ temp files (73 MB), and leaves expired transients. Respira snapshots accumulate with every write. Audit logs grow indefinitely.

### What to Clean (via Adminer)

Open **Local → Database → Open Adminer → SQL command**, paste:

```sql
-- 1. Clear stale Simply Static export records
TRUNCATE TABLE wp_simply_static_pages;

-- 2. Keep only last 10 Respira snapshots (each is a full page backup)
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

### What to Clean (via PowerShell / File System)

```powershell
# Simply Static temp files (can be 70+ MB after multiple exports)
Remove-Item "C:\Users\Zamri\Local Sites\digitrust-lab\app\public\wp-content\uploads\simply-static\temp-files\*" -Recurse -Force

# Truncate error logs (after debugging is done)
Clear-Content "C:\Users\Zamri\Local Sites\digitrust-lab\logs\php\error.log"
Clear-Content "C:\Users\Zamri\Local Sites\digitrust-lab\logs\nginx\error.log"
```

### What to Clean (via Site Shell / WP CLI)

```bash
wp transient delete --all
wp cache flush
```

### DB Size Baseline (healthy state after cleanup)

| Table | Rows | Size |
|-------|------|------|
| `wp_options` | ~234 | ~6 MB (normal — stores SS config) |
| `wp_simply_static_pages` | 0 | 0 MB (TRUNCATED) |
| `wp_respira_snapshots` | 10 | ~0.1 MB |
| `wp_respira_audit_log` | 50 | ~0.02 MB |
| `wp_postmeta` | ~355 | ~1.4 MB |
| `wp_posts` | ~169 | ~0.27 MB |

**Total DB after cleanup: ~8 MB** (down from ~12 MB bloated)

### Diagnostic Query (check before cleanup)

```sql
SELECT table_name, table_rows,
  ROUND(data_length/1024/1024,2) AS data_mb,
  ROUND(index_length/1024/1024,2) AS index_mb,
  ROUND((data_length+index_length)/1024/1024,2) AS total_mb
FROM information_schema.tables
WHERE table_schema='local'
ORDER BY (data_length+index_length) DESC LIMIT 10;
```

If `wp_simply_static_pages` shows 1000+ rows or `wp_respira_snapshots` shows 100+ rows, run the cleanup.

### When NOT to Clean

- **Before a Simply Static export** — the `wp_simply_static_pages` table is used during export. Clean it AFTER export is complete, not before.
- **If you need to rollback a Respira change** — old snapshots are needed for `respira_restore_snapshot`. Only clean snapshots older than your current working session.

---

## Local WP Hanging — wp-cron + PHP-FPM Worker Exhaustion (2026-07-11)

**Symptom:** Local WP becomes unresponsive after a few seconds of use. All pages timeout (homepage, wp-admin, REST API). PHP-FPM workers alive but not responding. No new errors in any log after restart.

**Root cause:** Two compounding issues:

1. **wp-cron fires on every page load.** On Local by Flywheel with only 2 PHP-FPM workers, a heavy scheduled task (Simply Static or Respira background job) locks both workers. Site works for 2 min after restart, then dies again with zero new errors.

2. **Simply Static admin page polling.** The Simply Static Generate page continuously polls API endpoints (`activity-log`, `is-running`, `export-log`) — 634 requests logged in one session. Combined with wp-cron, workers get overwhelmed and die.

**Evidence:**
- Nginx error log: 1,342 "no live upstreams" errors in one session
- 634 Simply Static polling requests
- 7 wp-cron requests in error log
- Site stable for 60+ seconds after `DISABLE_WP_CRON` applied

**Fix applied:**

1. Added to `wp-config.php` (before "That's all, stop editing!" line):
```php
// Prevent wp-cron from auto-firing on every page load (locks PHP-FPM workers)
define( 'DISABLE_WP_CRON', true );
```

2. Closed Simply Static Generate browser tab after export completed (stops polling flood).

**Run cron manually when needed:**
```bash
wp cron event run --due-now
```

**Impact of DISABLE_WP_CRON:**
- ❌ Background scheduled tasks won't fire automatically (Simply Static scheduled exports, Respira queue processing)
- ✅ Update badges still appear when you visit wp-admin (WP Admin does fresh update checks on page load regardless of cron)
- ✅ Manually run `wp cron event run --due-now` anytime to fire pending jobs
- ✅ For a local dev site, this is the correct tradeoff

**Prevention:**
- Always close Simply Static Generate tab after export is done
- After 3+ exports in one session, run DB health check cleanup (see section above)
- Don't run Respira writes on Post ID 10 (90s PHP-FPM lock per write)
- Consider increasing `pm.max_children` in `php-fpm.d/www.conf.hbs` if hangs persist

---

## Simply Static Admin Page Polling — PHP-FPM Worker Flood (2026-07-11)

**Symptom:** Site becomes sluggish or unresponsive while the Simply Static → Generate page is open in the browser.

**Root cause:** The Simply Static Generate admin page continuously polls REST API endpoints to show export progress:
- `/wp-json/simply-static/v1/activity-log`
- `/wp-json/simply-static/v1/is-running`
- `/wp-json/simply-static/v1/export-log`

Each poll request consumes a PHP-FPM worker. With only 2 workers on Local by Flywheel, the polling flood leaves no workers for actual page requests.

**Evidence:** 634 polling requests in Nginx error log during a single session.

**Fix:** Close the Simply Static Generate browser tab after export is complete. Do not leave it open.

**Alternative:** Use WP CLI instead of the browser UI for exports:
```bash
wp simply-static run
```
This runs the export in the CLI thread and avoids the browser polling entirely.

---

## WP CLI via Local by Flywheel Site Shell (2026-07-11)

**Availability:** Local by Flywheel exposes WP CLI via the "Open Site Shell" button. Working directory: `C:\Users\Zamri\Local Sites\digitrust-lab\app\public`

**Key commands:**

| Command | Purpose |
|---------|---------|
| `wp simply-static run` | Run Simply Static export in CLI (avoids browser PHP-FPM deadlock) |
| `wp cache flush` | Flush WordPress object cache |
| `wp transient delete --all` | Delete all transients |
| `wp cron event run --due-now` | Manually fire pending cron jobs (needed since `DISABLE_WP_CRON`) |
| `wp plugin list` | List installed plugins with status |
| `wp option get simply-static` | Read Simply Static settings |

**Limitation:** `wp db query` does NOT work on Local by Flywheel Site Shell on Windows. MySQL uses a socket file, not `localhost:3306`. Use **Adminer** (Local → Database → Open Adminer) for direct SQL queries instead.

**When to use CLI vs Respira MCP:**
- **CLI:** Simply Static export, cache flush, transient cleanup, plugin audit, cron events
- **Respira MCP:** Element/page/option edits (auto-snapshots), template edits, menu management
- **NEVER** use CLI for template/element edits — always Bricks GUI or Respira MCP
