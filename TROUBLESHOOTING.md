# DigiTrust Lab — Troubleshooting

> Project-specific issues and solutions. Not a development project — no global lessons needed.

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

- Use `wrangler pages deploy` as the primary deploy method
- Optionally reconnect Git integration in Cloudflare Pages dashboard for auto-deploy backup

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

- **Always run `post-process-static.ps1` after every Simply Static export** — it fixes both the search bar injection (Phase 0) and double-slash links (Phase 6)
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
- Phase 8 in post-process script is permanent — it runs after every export
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

Restored from backup JSON (`bricks-exports/header-v1.json`) by:
1. Creating a new template with `content create` (type set at creation time)
2. Writing elements with `content update_content`
3. Setting conditions with `template set`

### Prevention Rules

1. **NEVER use `template update` to change type after elements exist.** The `type` field must be set at creation time only.
2. **Correct workflow for creating Bricks templates via MCP:**
   - Step 1: `content create` — create template with title, post_type, status, AND elements all at once
   - Step 2: `template set` — set template type and conditions
   - Step 3: `content update_content` — update individual elements if needed
3. **Always backup templates before any MCP operations.** Use `/backup-bricks-templates` workflow.
4. **The `content update_content` action replaces ALL elements** — provide the complete element array, not just the one you want to update.
5. **The `content delete` action with element_id trashes the entire post** — not just the element. Be extremely careful.
