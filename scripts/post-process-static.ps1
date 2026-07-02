# Post-process static HTML files after Simply Static export
# Fixes: search bar injection, breadcrumbs, share links, shortcodes, dummy content cleanup

$staticDir = "D:\Coding Zone\digitrust-lab-static"

# --- Phase 0: Inject search bar into header (Simply Static strips form/input tags) ---
# SAFETY NET: As of 2026-07-02, Simply Static preserves <form> tags inside Bricks code
# elements, so this phase injects 0 files. Kept as a safety net in case a future
# Simply Static update reverts to stripping form tags.
$searchBarHTML = '<div style="display:flex;align-items:center;gap:12px;"><form action="/" method="get" style="display:flex;align-items:center;position:relative;"><input type="text" name="s" placeholder="Cari..." style="border:1px solid #EBEBEB;border-radius:6px;padding:5px 12px;font-size:12px;font-family:' + "'Plus Jakarta Sans'" + ',system-ui,sans-serif;width:180px;outline:none;height:32px;box-sizing:border-box;"><button type="submit" style="background:none;border:none;cursor:pointer;position:absolute;right:8px;top:50%;transform:translateY(-50%);padding:0;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6B6B6B" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.35-4.35"></path></svg></button></form><a href="#" style="background:#E8621A;color:#fff;font-family:' + "'Plus Jakarta Sans'" + ',system-ui,sans-serif;font-size:12px;font-weight:600;padding:7px 14px;border-radius:6px;text-decoration:none;white-space:nowrap;">Dapatkan Panduan Percuma</a></div>'

Write-Host "`n--- Phase 0: Inject search bar into headers ---" -ForegroundColor Cyan
$allHtmlForSearch = Get-ChildItem $staticDir -Filter "*.html" -Recurse | Where-Object { $_.FullName -notmatch 'wp-content|wp-includes' }
$searchFixCount = 0
foreach ($file in $allHtmlForSearch) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    # Check if header has nav but is missing the search form (Simply Static strips it)
    if ($content -match 'brxe-hdr001' -and $content -notmatch 'name="s"') {
        # Replace: </nav><a href="#" style="background:#E8621A...>...</a></div></div></header>
        # With:   </nav><SEARCH_BAR_HTML</div></div></header>
        $pattern = '</nav><a href="#" style="background:#E8621A[^"]*"[^>]*>Dapatkan Panduan Percuma</a></div></div></header>'
        $content = $content -replace $pattern, "</nav>$searchBarHTML</div></div></header>"
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
        $searchFixCount++
        Write-Host "  Injected search bar: $($file.Name)" -ForegroundColor Green
    }
}
Write-Host "Injected search bar into $searchFixCount files" -ForegroundColor Green

# --- Phase 2: Add breadcrumbs to post pages ---
$postPages = @(
    "simply-static-export-pipeline-will-be-deleted-after-testing"
)

# Find all post HTML files (not pages like privasi/disclaimer/hubungi/tentang)
$allHtmlFiles = Get-ChildItem $staticDir -Filter "index.html" -Recurse | Where-Object {
    $relPath = $_.FullName.Replace($staticDir, "").TrimStart('\')
    # Exclude known pages, templates, author, category, wp-content, wp-includes
    $relPath -notmatch '^(privasi|disclaimer|hubungi|tentang|template|author|category|wp-content|wp-includes|index\.html)' -and
    $relPath -notmatch 'wp-content|wp-includes'
}

Write-Host "Found $($allHtmlFiles.Count) potential post pages to process" -ForegroundColor Cyan

foreach ($file in $allHtmlFiles) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    $modified = $false

    # --- Fix share links: remove /blog/ prefix ---
    if ($content -match '%2Fblog%2F') {
        $content = $content -replace '%2Fblog%2F', '%2F'
        $modified = $true
        Write-Host "  Fixed share links in: $($file.Name)" -ForegroundColor Yellow
    }

    # --- Fix raw shortcodes ---
    # [rank_math_reading_time] -> "X min bacaan" (estimate from content)
    if ($content -match '\[rank_math_reading_time\]') {
        # Count words in the main content area
        $wordCount = ($content -replace '<[^>]+>', ' ' -replace '\s+', ' ' -split ' ').Count
        $readTime = [math]::Max(1, [math]::Round($wordCount / 200))
        $content = $content -replace '\[rank_math_reading_time\]', "$readTime min bacaan"
        $modified = $true
        Write-Host "  Fixed reading time shortcode in: $($file.Name)" -ForegroundColor Yellow
    }

    # [rank_math_toc] -> Remove (TOC needs JS, skip for now)
    if ($content -match '\[rank_math_toc\]') {
        $content = $content -replace '\[rank_math_toc\]', ''
        $modified = $true
        Write-Host "  Removed TOC shortcode in: $($file.Name)" -ForegroundColor Yellow
    }

    # --- Add breadcrumbs (if not already present) ---
    if ($content -notmatch 'dtl-breadcrumb' -and $content -match 'dtl-post-wrap') {
        $breadcrumbHTML = '<div class="dtl-breadcrumb" style="max-width:620px;margin:0 auto;padding:12px 20px 0;font-family:' + "'Plus Jakarta Sans'" + ',system-ui,sans-serif;font-size:12px;color:#6B6B6B;"><a href="/" style="color:#6B6B6B;text-decoration:none;">Beranda</a> <span style="color:#CCC;">&rsaquo;</span> <span style="color:#1A1A1A;font-weight:500;">Artikel</span></div>'
        $content = $content -replace '(<div class="dtl-post-wrap")', "$breadcrumbHTML`$1"
        $modified = $true
        Write-Host "  Added breadcrumbs to: $($file.Name)" -ForegroundColor Green
    }

    if ($modified) {
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
        Write-Host "  Saved: $($file.FullName)" -ForegroundColor Green
    }
}

# --- Phase 5: Fix share links in ALL html files (including non-post pages) ---
Write-Host "`nFixing share links in all HTML files..." -ForegroundColor Cyan
$allFiles = Get-ChildItem $staticDir -Filter "*.html" -Recurse
$shareFixCount = 0
foreach ($file in $allFiles) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    if ($content -match '/blog/' -and $content -match 'share') {
        $content = $content -replace '/blog/', '/'
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
        $shareFixCount++
    }
}
Write-Host "Fixed share links in $shareFixCount files" -ForegroundColor Green

# --- Phase 6: Fix double-slash links (Simply Static replaces https://domain -> / creating //path) ---
Write-Host "`n--- Phase 6: Fix double-slash links ---" -ForegroundColor Cyan
$allFilesForSlash = Get-ChildItem $staticDir -Filter "*.html" -Recurse | Where-Object { $_.FullName -notmatch 'wp-content|wp-includes' }
$slashFixCount = 0
foreach ($file in $allFilesForSlash) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    $modified = $false
    # Fix href="//path" -> href="/path" (but NOT https://)
    if ($content -match 'href="//(?!/)') {
        $content = $content -replace 'href="//(?!/)', 'href="/'
        $modified = $true
    }
    # Fix src="//path" -> src="/path" (but NOT https://)
    if ($content -match 'src="//(?!/)') {
        $content = $content -replace 'src="//(?!/)', 'src="/'
        $modified = $true
    }
    if ($modified) {
        [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
        $slashFixCount++
        Write-Host "  Fixed double-slash: $($file.Name)" -ForegroundColor Green
    }
}
Write-Host "Fixed double-slash links in $slashFixCount files" -ForegroundColor Green

# --- Phase 7: Remove dummy post static files ---
$dummyPostPath = "$staticDir\simply-static-export-pipeline-will-be-deleted-after-testing"
if (Test-Path $dummyPostPath) {
    Remove-Item $dummyPostPath -Recurse -Force
    Write-Host "`nRemoved dummy post directory" -ForegroundColor Green
}

# --- Phase 8: Remove wp-includes/blocks/ (Gutenberg block assets not used by Bricks) ---
# Saves ~705 files. Bricks Builder doesn't use Gutenberg blocks.
$blocksPath = "$staticDir\wp-includes\blocks"
if (Test-Path $blocksPath) {
    $blockFiles = (Get-ChildItem $blocksPath -Recurse -File).Count
    Remove-Item $blocksPath -Recurse -Force
    Write-Host "`n--- Phase 8: Strip unused wp-includes/blocks/ ---" -ForegroundColor Cyan
    Write-Host "  Removed $blockFiles files from wp-includes/blocks/" -ForegroundColor Green
}

# --- Phase 9: Strip unused wp-includes/ assets (jQuery, TinyMCE, admin images, etc.) ---
# Frontend only loads wp-emoji-release.min.js and wp-emoji-loader.min.js from wp-includes/js/
# Everything else is WordPress admin/editor assets not needed on a static Bricks frontend.
Write-Host "`n--- Phase 9: Strip unused wp-includes/ assets ---" -ForegroundColor Cyan
$phase9Count = 0

# 9a: Remove wp-includes/js/ EXCEPT emoji files
$jsPath = "$staticDir\wp-includes\js"
if (Test-Path $jsPath) {
    $emojiFiles = @("wp-emoji-release.min.js", "wp-emoji-loader.min.js")
    $jsFiles = Get-ChildItem $jsPath -Recurse -File
    foreach ($f in $jsFiles) {
        if ($emojiFiles -notcontains $f.Name) {
            Remove-Item $f.FullName -Force
            $phase9Count++
        }
    }
    # Clean up empty directories
    Get-ChildItem $jsPath -Directory -Recurse | Sort-Object { $_.FullName.Length } -Descending | Where-Object { (Get-ChildItem $_.FullName -Force).Count -eq 0 } | Remove-Item -Force
    Write-Host "  Stripped wp-includes/js/ (kept emoji files): $phase9Count files removed" -ForegroundColor Green
}

# 9b: Remove wp-includes/images/ entirely (admin icons, smilies, media UI)
$imagesPath = "$staticDir\wp-includes\images"
if (Test-Path $imagesPath) {
    $imgFiles = (Get-ChildItem $imagesPath -Recurse -File).Count
    Remove-Item $imagesPath -Recurse -Force
    $phase9Count += $imgFiles
    Write-Host "  Stripped wp-includes/images/: $imgFiles files removed" -ForegroundColor Green
}

# 9c: Remove wp-includes/css/ entirely (admin styles, classic-themes is only a sourceURL comment)
$cssPath = "$staticDir\wp-includes\css"
if (Test-Path $cssPath) {
    $cssFiles = (Get-ChildItem $cssPath -Recurse -File).Count
    Remove-Item $cssPath -Recurse -Force
    $phase9Count += $cssFiles
    Write-Host "  Stripped wp-includes/css/: $cssFiles files removed" -ForegroundColor Green
}

Write-Host "  Phase 9 total: $phase9Count files removed" -ForegroundColor Green

# --- Phase 10: Strip unused wp-content/plugins/seo-by-rank-math/ ---
# Rank Math only contributes inline JSON-LD schema — no CSS/JS files are loaded by frontend.
Write-Host "`n--- Phase 10: Strip unused rank-math plugin assets ---" -ForegroundColor Cyan
$rankMathPath = "$staticDir\wp-content\plugins\seo-by-rank-math"
if (Test-Path $rankMathPath) {
    $rmFiles = (Get-ChildItem $rankMathPath -Recurse -File).Count
    Remove-Item $rankMathPath -Recurse -Force
    Write-Host "  Stripped seo-by-rank-math/: $rmFiles files removed" -ForegroundColor Green
}

# --- Phase 11: Strip unused Bricks editor assets ---
# Bricks ships ~500 files in assets/ — most are Builder editor JS/CSS/SVG/icons.
# Frontend only loads 3 files: bricks.min.js, frontend-layer.min.css, content-default.min.css
Write-Host "`n--- Phase 11: Strip unused Bricks editor assets ---" -ForegroundColor Cyan
$bricksAssetsPath = "$staticDir\wp-content\themes\bricks\assets"
$phase11Count = 0

if (Test-Path $bricksAssetsPath) {
    # Keep list: only files the frontend HTML actually references
    $keepFiles = @(
        "js\bricks.min.js"
        "css\frontend-layer.min.css"
        "css\frontend\content-default.min.css"
    )

    # Also keep images/ (small, may be referenced by CSS)
    $allFiles = Get-ChildItem $bricksAssetsPath -Recurse -File
    foreach ($f in $allFiles) {
        $relativePath = $f.FullName.Substring($bricksAssetsPath.Length + 1).Replace("/", "\")
        if ($keepFiles -notcontains $relativePath -and $f.Directory.Name -ne "images") {
            Remove-Item $f.FullName -Force
            $phase11Count++
        }
    }

    # Clean up empty directories (preserve images/ folder)
    Get-ChildItem $bricksAssetsPath -Directory -Recurse | Sort-Object { $_.FullName.Length } -Descending | Where-Object {
        (Get-ChildItem $_.FullName -Force).Count -eq 0 -and $_.Name -ne "images"
    } | Remove-Item -Force

    Write-Host "  Stripped unused Bricks editor assets: $phase11Count files removed" -ForegroundColor Green
    Write-Host "  Kept: bricks.min.js, frontend-layer.min.css, content-default.min.css, images/" -ForegroundColor Gray
} else {
    Write-Host "  Bricks assets directory not found - skipping" -ForegroundColor Yellow
}

Write-Host "`n✅ Post-processing complete!" -ForegroundColor Green
