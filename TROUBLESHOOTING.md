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
