# DigiTrust Lab — Export Bloat Optimization Context

## Project Overview

- **Stack:** WordPress + Bricks Builder + Simply Static + Cloudflare Pages
- **Static output:** `D:\Coding Zone\digitrust-lab-static`
- **Live site:** https://blog.digitrustlab.com
- **Deploy:** `npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main`
- **Post-process:** `G:\Zamzam Biznez\DigiTrustLabCode\scripts\post-process-static.ps1`

## The Problem

Simply Static exports **2,694 files** per build, but only **11 are actual content pages**. The rest are WordPress core assets and theme files that Bricks Builder doesn't use.

### File Breakdown (Before Optimization)

| Category | Count | % | Notes |
|----------|-------|---|-------|
| `wp-includes/` (WP core) | 1,832 | 68% | Gutenberg blocks, jQuery, etc. |
| `wp-content/themes/` (Bricks) | 665 | 25% | CSS, JS, SVGs, fonts |
| `wp-content/plugins/` | 186 | 7% | Rank Math SEO (183), Simply Static (3) |
| Content pages (HTML) | 11 | <1% | Homepage, Tentang, Privasi, Disclaimer, Hubungi, etc. |
| XML/Sitemaps | 5 | <1% | |

### Top Bloat Sources

| Source | Files | Why It's Wasted |
|--------|-------|-----------------|
| `wp-includes/blocks/` | 705 | Gutenberg block assets (block.json, style.css, editor.css per block type). Bricks doesn't use Gutenberg at all. |
| `wp-includes/js/` | 551 | WordPress core JS (jQuery, underscore, thickbox). Bricks loads its own JS. |
| `wp-includes/css/` | 162 | WordPress core CSS. Bricks handles all styling. |
| Bricks `assets/svg/builder/` | 163 | Editor-only icons for the Bricks Builder UI itself. Not rendered on frontend. |
| Bricks `assets/js/` | 255 | Some needed (frontend.min.js), some editor-only. |

### By File Extension

| Extension | Count |
|-----------|-------|
| `.css` | 947 |
| `.js` | 865 |
| `.svg` | 607 |
| `.json` | 127 |
| `.png` | 64 |
| `.gif` | 42 |
| `.html` | 11 |

## Why Simply Static Can't Exclude These via Settings

Simply Static's `Wp_Includes_Crawler` hardcodes which directories to scan:

```php
// class-ss-wp-includes-crawler.php line 80
$dirs = [ 'css/', 'js/', 'fonts/', 'images/', 'blocks/' ];
```

Additionally, `is_url_excluded()` in `class-ss-util.php` has a short-circuit:

```php
// line 538
if ( self::is_core_include_asset( $url ) ) {
    return false; // Never exclude wp-includes URLs
}
```

This means Simply Static's "Exclude URLs" setting **cannot exclude wp-includes files** — the core asset check runs before exclusion patterns are evaluated.

## What Was Done (Two-Part Fix)

### Part 1: Mu-Plugin (Prevents Crawl)

**File:** `wp-content/mu-plugins/ss-skip-dirs.php`

```php
<?php
// Skip Bricks builder-only SVGs from Simply Static crawl
add_filter('ss_skip_crawl_theme_directories', function($dirs) {
    $dirs[] = 'assets/svg/builder';
    return $dirs;
});
```

This uses Simply Static's built-in `ss_skip_crawl_theme_directories` filter to skip the `assets/svg/builder/` directory at crawl time. **163 files never discovered.**

### Part 2: Post-Process Phase 8 (Deletes After Transfer)

**File:** `scripts/post-process-static.ps1` (appended at end)

```powershell
# --- Phase 8: Remove wp-includes/blocks/ (Gutenberg block assets not used by Bricks) ---
$blocksPath = "$staticDir\wp-includes\blocks"
if (Test-Path $blocksPath) {
    $blockFiles = (Get-ChildItem $blocksPath -Recurse -File).Count
    Remove-Item $blocksPath -Recurse -Force
    Write-Host "  Removed $blockFiles files from wp-includes/blocks/" -ForegroundColor Green
}
```

This deletes `wp-includes/blocks/` after Simply Static transfers files to the static directory. Necessary because `is_core_include_asset()` prevents URL-level exclusion. **705 files removed post-transfer.**

## Results

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total files | 2,694 | 1,836 | -868 (32%) |
| Deploy upload time | ~3.5 sec | ~1.6 sec | 54% faster |
| Live site | ✅ Working | ✅ Verified | No breakage |

## Further Optimization Opportunities (Not Yet Done)

| Source | Files | Approach | Risk |
|--------|-------|----------|------|
| `wp-includes/js/` | 551 | Add to Phase 8 deletion | Low — but need to verify Bricks doesn't reference any wp-includes JS |
| `wp-includes/css/` | 162 | Add to Phase 8 deletion | Low — Bricks loads its own CSS |
| `wp-includes/images/` | 409 | Add to Phase 8 deletion | Medium — may contain emoji or smiley images referenced by WP |
| Bricks `assets/js/` editor files | ~100 | Filter via `ss_skip_crawl_theme_directories` | Low — need to identify which JS files are frontend vs editor |

## Key Files Reference

| File | Location |
|------|----------|
| Post-process script | `G:\Zamzam Biznez\DigiTrustLabCode\scripts\post-process-static.ps1` |
| Mu-plugin (skip dirs) | `C:\Users\Zamri\Local Sites\digitrust-lab\app\public\wp-content\mu-plugins\ss-skip-dirs.php` |
| Static output dir | `D:\Coding Zone\digitrust-lab-static` |
| Simply Static plugin | `C:\Users\Zamri\Local Sites\digitrust-lab\app\public\wp-content\plugins\simply-static\` |
| WP-Includes Crawler | `simply-static\src\crawler\class-ss-wp-includes-crawler.php` |
| Theme Assets Crawler | `simply-static\src\crawler\class-ss-theme-assets-crawler.php` |
| URL Exclusion Logic | `simply-static\src\class-ss-util.php` (line 536: `is_url_excluded()`) |
| Troubleshooting docs | `G:\Zamzam Biznez\DigiTrustLabCode\TROUBLESHOOTING.md` (entry #11) |

## Export Workflow (Current)

```
1. Make changes in WordPress/Bricks GUI
2. WP Admin → Simply Static → Generate (exports ~2,700 files)
3. Run post-process-static.ps1
   - Phase 0: Inject search bar (safety net, currently 0 files)
   - Phase 2: Breadcrumbs + shortcode fixes for post pages
   - Phase 5: Fix /blog/ prefix in share links
   - Phase 6: Fix double-slash links (Simply Static URL bug)
   - Phase 7: Remove dummy post
   - Phase 8: Delete wp-includes/blocks/ (NEW — saves 705 files)
4. Mu-plugin prevents Bricks builder SVGs from being crawled (saves 163 files)
5. Deploy: npx wrangler pages deploy . --project-name=digitrust-lab-static --branch=main
6. Result: ~1,836 files deployed (was 2,694)
```
